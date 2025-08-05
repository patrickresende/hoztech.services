"""
Serviço de Chatbot WhatsApp para HOZ TECH
Sistema de automação de mensagens com filtragem de contatos
"""

import json
import time
import uuid
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import (
    WhatsAppContact, WhatsAppSession, WhatsAppMessage, 
    WhatsAppTemplate, WhatsAppConfig, WhatsAppLog
)

# Configurar logging
logger = logging.getLogger(__name__)


class WhatsAppChatbotService:
    """Serviço principal do chatbot WhatsApp"""
    
    def __init__(self):
        self._is_active = None
        self._auto_response_delay = None
        self._max_session_duration = None
    
    @property
    def is_active(self):
        """Verificar se o chatbot está ativo"""
        if self._is_active is None:
            self._is_active = self._get_config('chatbot_active', 'false').lower() == 'true'
        return self._is_active
    
    @property
    def auto_response_delay(self):
        """Obter delay de resposta automática"""
        if self._auto_response_delay is None:
            self._auto_response_delay = int(self._get_config('auto_response_delay', '5'))
        return self._auto_response_delay
    
    @property
    def max_session_duration(self):
        """Obter duração máxima da sessão"""
        if self._max_session_duration is None:
            self._max_session_duration = int(self._get_config('max_session_duration', '3600'))  # 1 hora
        return self._max_session_duration
        
    def _get_config(self, key: str, default: str = '') -> str:
        """Obter configuração do sistema"""
        return WhatsAppConfig.get_value(key, default)
    
    def _log(self, level: str, message: str, session=None, contact=None, metadata=None):
        """Registrar log de atividade"""
        try:
            WhatsAppLog.objects.create(
                level=level,
                message=message,
                session=session,
                contact=contact,
                metadata=metadata or {}
            )
        except Exception as e:
            logger.error(f"Erro ao registrar log: {e}")
    
    def is_contact_filtered(self, phone_number: str) -> bool:
        """Verificar se o contato deve ser filtrado (ignorado)"""
        try:
            contact = WhatsAppContact.objects.get(
                phone_number=phone_number,
                is_active=True
            )
            
            # Filtrar se for da sua lista de contatos ou estiver bloqueado
            if contact.is_my_contact or contact.is_blocked:
                self._log('info', f'Contato filtrado: {phone_number}', contact=contact)
                return True
                
            return False
            
        except WhatsAppContact.DoesNotExist:
            # Contato não existe, criar como novo contato não filtrado
            contact = WhatsAppContact.objects.create(
                phone_number=phone_number,
                is_my_contact=False,
                is_blocked=False
            )
            self._log('info', f'Novo contato criado: {phone_number}', contact=contact)
            return False
    
    def process_incoming_message(self, message_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processar mensagem recebida do WhatsApp"""
        if not self.is_active:
            self._log('debug', 'Chatbot inativo, ignorando mensagem')
            return None
        
        try:
            phone_number = message_data.get('from')
            message_content = message_data.get('body', '')
            message_id = message_data.get('id', str(uuid.uuid4()))
            timestamp = datetime.fromtimestamp(message_data.get('timestamp', time.time()))
            
            # Verificar se o contato deve ser filtrado
            if self.is_contact_filtered(phone_number):
                return None
            
            # Obter ou criar contato
            contact, created = WhatsAppContact.objects.get_or_create(
                phone_number=phone_number,
                defaults={'is_my_contact': False, 'is_blocked': False}
            )
            
            # Obter ou criar sessão ativa
            session = self._get_or_create_session(contact)
            
            # Registrar mensagem recebida
            incoming_message = WhatsAppMessage.objects.create(
                session=session,
                message_id=message_id,
                direction='incoming',
                message_type=message_data.get('type', 'text'),
                content=message_content,
                timestamp=timestamp,
                is_automated=False,
                metadata=message_data
            )
            
            self._log('info', f'Mensagem recebida de {phone_number}: {message_content[:50]}...', 
                     session=session, contact=contact)
            
            # Processar resposta automática
            response = self._generate_automated_response(session, incoming_message)
            
            return response
            
        except Exception as e:
            self._log('error', f'Erro ao processar mensagem: {str(e)}', metadata={'error': str(e)})
            logger.error(f"Erro ao processar mensagem: {e}")
            return None
    
    def _get_or_create_session(self, contact: WhatsAppContact) -> WhatsAppSession:
        """Obter sessão ativa ou criar nova"""
        # Verificar se existe sessão ativa recente
        recent_session = WhatsAppSession.objects.filter(
            contact=contact,
            status='active',
            last_activity__gte=timezone.now() - timedelta(seconds=self.max_session_duration),
            is_active=True
        ).first()
        
        if recent_session:
            return recent_session
        
        # Criar nova sessão
        session = WhatsAppSession.objects.create(
            contact=contact,
            session_id=f"session_{contact.id}_{int(time.time())}",
            status='active',
            current_step=0,
            context_data={}
        )
        
        self._log('info', f'Nova sessão criada: {session.session_id}', session=session, contact=contact)
        return session
    
    def _generate_automated_response(self, session: WhatsAppSession, incoming_message: WhatsAppMessage) -> Optional[Dict[str, Any]]:
        """Gerar resposta automatizada baseada no template"""
        try:
            # Obter template para o passo atual
            template = WhatsAppTemplate.objects.filter(
                step_number=session.current_step,
                is_active=True
            ).first()
            
            if not template:
                # Não há template para este passo, finalizar sessão
                session.status = 'completed'
                session.completed_at = timezone.now()
                session.save()
                self._log('info', f'Sessão finalizada - sem template para passo {session.current_step}', 
                         session=session)
                return None
            
            # Preparar contexto para o template
            context_data = {
                'contact_name': session.contact.name or 'Cliente',
                'phone_number': session.contact.phone_number,
                'current_step': session.current_step,
                'session_id': session.session_id,
                **session.context_data
            }
            
            # Renderizar conteúdo do template
            response_content = template.render_content(context_data)
            
            # Criar mensagem de resposta
            response_message = WhatsAppMessage.objects.create(
                session=session,
                message_id=f"auto_{session.session_id}_{int(time.time())}",
                direction='outgoing',
                message_type='text',
                content=response_content,
                timestamp=timezone.now(),
                is_automated=True,
                metadata={'template_id': template.id, 'template_name': template.name}
            )
            
            # Atualizar sessão
            session.current_step += 1
            session.last_activity = timezone.now()
            session.save()
            
            self._log('info', f'Resposta automática gerada: {template.name}', 
                     session=session, contact=session.contact)
            
            # Preparar resposta para envio
            response_data = {
                'to': session.contact.phone_number,
                'body': response_content,
                'delay': template.delay_seconds,
                'message_id': response_message.message_id
            }
            
            return response_data
            
        except Exception as e:
            session.status = 'error'
            session.error_message = str(e)
            session.save()
            self._log('error', f'Erro ao gerar resposta automática: {str(e)}', 
                     session=session, metadata={'error': str(e)})
            return None
    
    def add_contact_to_filter(self, phone_number: str, name: str = '', is_my_contact: bool = True) -> bool:
        """Adicionar contato à lista de filtros"""
        try:
            contact, created = WhatsAppContact.objects.get_or_create(
                phone_number=phone_number,
                defaults={
                    'name': name,
                    'is_my_contact': is_my_contact,
                    'is_blocked': False
                }
            )
            
            if not created:
                contact.is_my_contact = is_my_contact
                contact.name = name or contact.name
                contact.save()
            
            self._log('info', f'Contato adicionado ao filtro: {phone_number}', contact=contact)
            return True
            
        except Exception as e:
            self._log('error', f'Erro ao adicionar contato ao filtro: {str(e)}', 
                     metadata={'phone_number': phone_number, 'error': str(e)})
            return False
    
    def block_contact(self, phone_number: str) -> bool:
        """Bloquear contato"""
        try:
            contact = WhatsAppContact.objects.get(phone_number=phone_number, is_active=True)
            contact.is_blocked = True
            contact.save()
            
            # Pausar sessões ativas
            WhatsAppSession.objects.filter(
                contact=contact,
                status='active',
                is_active=True
            ).update(status='paused')
            
            self._log('info', f'Contato bloqueado: {phone_number}', contact=contact)
            return True
            
        except WhatsAppContact.DoesNotExist:
            self._log('warning', f'Tentativa de bloquear contato inexistente: {phone_number}')
            return False
        except Exception as e:
            self._log('error', f'Erro ao bloquear contato: {str(e)}', 
                     metadata={'phone_number': phone_number, 'error': str(e)})
            return False
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obter estatísticas das sessões"""
        try:
            stats = {
                'active_sessions': WhatsAppSession.objects.filter(status='active', is_active=True).count(),
                'completed_sessions': WhatsAppSession.objects.filter(status='completed', is_active=True).count(),
                'total_contacts': WhatsAppContact.objects.filter(is_active=True).count(),
                'filtered_contacts': WhatsAppContact.objects.filter(
                    is_my_contact=True, is_active=True
                ).count(),
                'blocked_contacts': WhatsAppContact.objects.filter(
                    is_blocked=True, is_active=True
                ).count(),
                'messages_today': WhatsAppMessage.objects.filter(
                    created_at__date=timezone.now().date(),
                    is_active=True
                ).count(),
                'automated_messages_today': WhatsAppMessage.objects.filter(
                    created_at__date=timezone.now().date(),
                    is_automated=True,
                    is_active=True
                ).count()
            }
            
            return stats
            
        except Exception as e:
            self._log('error', f'Erro ao obter estatísticas: {str(e)}')
            return {}
    
    def cleanup_old_sessions(self, days: int = 7) -> int:
        """Limpar sessões antigas"""
        try:
            cutoff_date = timezone.now() - timedelta(days=days)
            
            # Marcar sessões antigas como inativas
            old_sessions = WhatsAppSession.objects.filter(
                last_activity__lt=cutoff_date,
                is_active=True
            )
            
            count = old_sessions.count()
            old_sessions.update(is_active=False)
            
            self._log('info', f'Limpeza realizada: {count} sessões antigas removidas')
            return count
            
        except Exception as e:
            self._log('error', f'Erro na limpeza de sessões: {str(e)}')
            return 0
    
    def send_message_via_api(self, phone_number: str, message: str, message_type: str = 'text') -> Dict[str, Any]:
        """Enviar mensagem via WhatsApp Business API"""
        try:
            # Obter configurações da API
            access_token = self._get_config('whatsapp_access_token')
            phone_number_id = self._get_config('whatsapp_phone_number_id')
            
            if not access_token or not phone_number_id:
                return {
                    'success': False,
                    'error': 'Configurações da API não encontradas'
                }
            
            # Preparar URL da API
            url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
            
            # Preparar headers
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Preparar payload
            payload = {
                'messaging_product': 'whatsapp',
                'to': phone_number,
                'type': message_type,
                'text': {
                    'body': message
                }
            }
            
            # Fazer requisição
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                message_id = response_data.get('messages', [{}])[0].get('id')
                
                # Registrar mensagem enviada
                contact, _ = WhatsAppContact.objects.get_or_create(
                    phone_number=phone_number,
                    defaults={'is_my_contact': False, 'is_blocked': False}
                )
                
                session = self._get_or_create_session(contact)
                
                WhatsAppMessage.objects.create(
                    session=session,
                    message_id=message_id or f"api_{int(time.time())}",
                    direction='outgoing',
                    message_type=message_type,
                    content=message,
                    timestamp=timezone.now(),
                    is_automated=False,
                    metadata={'api_response': response_data}
                )
                
                self._log('info', f'Mensagem enviada via API para {phone_number}', 
                         session=session, contact=contact)
                
                return {
                    'success': True,
                    'message_id': message_id,
                    'response': response_data
                }
            else:
                error_msg = f"Erro na API: {response.status_code} - {response.text}"
                self._log('error', error_msg, metadata={'phone_number': phone_number})
                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro de conexão: {str(e)}"
            self._log('error', error_msg, metadata={'phone_number': phone_number})
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            self._log('error', error_msg, metadata={'phone_number': phone_number})
            return {
                'success': False,
                'error': error_msg
            }
    
    def send_template_message(self, phone_number: str, template_name: str, language_code: str = 'pt_BR', parameters: List[str] = None) -> Dict[str, Any]:
        """Enviar mensagem template via WhatsApp Business API"""
        try:
            # Obter configurações da API
            access_token = self._get_config('whatsapp_access_token')
            phone_number_id = self._get_config('whatsapp_phone_number_id')
            
            if not access_token or not phone_number_id:
                return {
                    'success': False,
                    'error': 'Configurações da API não encontradas'
                }
            
            # Preparar URL da API
            url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
            
            # Preparar headers
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Preparar componentes do template
            components = []
            if parameters:
                components.append({
                    'type': 'body',
                    'parameters': [{'type': 'text', 'text': param} for param in parameters]
                })
            
            # Preparar payload
            payload = {
                'messaging_product': 'whatsapp',
                'to': phone_number,
                'type': 'template',
                'template': {
                    'name': template_name,
                    'language': {
                        'code': language_code
                    },
                    'components': components
                }
            }
            
            # Fazer requisição
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                message_id = response_data.get('messages', [{}])[0].get('id')
                
                # Registrar mensagem enviada
                contact, _ = WhatsAppContact.objects.get_or_create(
                    phone_number=phone_number,
                    defaults={'is_my_contact': False, 'is_blocked': False}
                )
                
                session = self._get_or_create_session(contact)
                
                WhatsAppMessage.objects.create(
                    session=session,
                    message_id=message_id or f"template_{int(time.time())}",
                    direction='outgoing',
                    message_type='template',
                    content=f"Template: {template_name}",
                    timestamp=timezone.now(),
                    is_automated=False,
                    metadata={
                        'template_name': template_name,
                        'parameters': parameters,
                        'api_response': response_data
                    }
                )
                
                self._log('info', f'Template enviado via API para {phone_number}: {template_name}', 
                         session=session, contact=contact)
                
                return {
                    'success': True,
                    'message_id': message_id,
                    'response': response_data
                }
            else:
                error_msg = f"Erro na API: {response.status_code} - {response.text}"
                self._log('error', error_msg, metadata={'phone_number': phone_number, 'template': template_name})
                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro de conexão: {str(e)}"
            self._log('error', error_msg, metadata={'phone_number': phone_number, 'template': template_name})
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            self._log('error', error_msg, metadata={'phone_number': phone_number, 'template': template_name})
            return {
                'success': False,
                'error': error_msg
            }


class WhatsAppWebhookHandler:
    """Handler para webhooks do WhatsApp Web"""
    
    def __init__(self):
        self.chatbot_service = WhatsAppChatbotService()
    
    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processar webhook recebido"""
        try:
            # Validar estrutura do webhook
            if not self._validate_webhook(webhook_data):
                return {'status': 'error', 'message': 'Webhook inválido'}
            
            # Extrair dados da mensagem
            message_data = self._extract_message_data(webhook_data)
            
            if not message_data:
                return {'status': 'ignored', 'message': 'Nenhuma mensagem para processar'}
            
            # Processar mensagem
            response = self.chatbot_service.process_incoming_message(message_data)
            
            if response:
                return {
                    'status': 'success',
                    'response': response,
                    'message': 'Mensagem processada com sucesso'
                }
            else:
                return {
                    'status': 'filtered',
                    'message': 'Mensagem filtrada ou chatbot inativo'
                }
                
        except Exception as e:
            logger.error(f"Erro no webhook handler: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _validate_webhook(self, data: Dict[str, Any]) -> bool:
        """Validar estrutura do webhook"""
        required_fields = ['entry']
        return all(field in data for field in required_fields)
    
    def _extract_message_data(self, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extrair dados da mensagem do webhook"""
        try:
            entry = webhook_data.get('entry', [])
            if not entry:
                return None
            
            changes = entry[0].get('changes', [])
            if not changes:
                return None
            
            value = changes[0].get('value', {})
            messages = value.get('messages', [])
            
            if not messages:
                return None
            
            message = messages[0]
            
            return {
                'id': message.get('id'),
                'from': message.get('from'),
                'timestamp': message.get('timestamp'),
                'type': message.get('type', 'text'),
                'body': message.get('text', {}).get('body', '') if message.get('type') == 'text' else '',
                'raw_data': message
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados da mensagem: {e}")
            return None


# Instância global do serviço
whatsapp_service = WhatsAppChatbotService()
webhook_handler = WhatsAppWebhookHandler()