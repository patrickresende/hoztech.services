"""
Views para o sistema de chatbot WhatsApp
Backend seguro sem renderização de links públicos
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Count
from django.conf import settings

from .whatsapp_service import whatsapp_service, webhook_handler
from .models import (
    WhatsAppContact, WhatsAppSession, WhatsAppMessage, 
    WhatsAppTemplate, WhatsAppConfig, WhatsAppLog
)

logger = logging.getLogger(__name__)


class WhatsAppWebhookView(View):
    """View para receber webhooks do WhatsApp Web"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        """Verificação do webhook (WhatsApp verification) ou status"""
        try:
            # Parâmetros de verificação do WhatsApp
            mode = request.GET.get('hub.mode')
            token = request.GET.get('hub.verify_token')
            challenge = request.GET.get('hub.challenge')
            
            # Se há parâmetros de verificação do WhatsApp
            if mode and token and challenge:
                # Token de verificação configurado
                verify_token = WhatsAppConfig.get_value('webhook_verify_token', 'default_token')
                
                if mode == 'subscribe' and token == verify_token:
                    logger.info("Webhook verificado com sucesso")
                    return HttpResponse(challenge, content_type='text/plain')
                else:
                    logger.warning(f"Falha na verificação do webhook: mode={mode}, token={token}")
                    return HttpResponse('Forbidden', status=403)
            else:
                # Retornar status do webhook para testes
                return JsonResponse({
                    'status': 'webhook_ready',
                    'message': 'Webhook está funcionando',
                    'timestamp': timezone.now().isoformat(),
                    'verify_token_configured': bool(WhatsAppConfig.get_value('webhook_verify_token'))
                })
                
        except Exception as e:
            logger.error(f"Erro na verificação do webhook: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    def post(self, request):
        """Processar webhook recebido"""
        try:
            # Parse do JSON
            webhook_data = json.loads(request.body.decode('utf-8'))
            
            # Log do webhook recebido
            logger.info(f"Webhook recebido: {json.dumps(webhook_data, indent=2)}")
            
            # Processar webhook
            result = webhook_handler.handle_webhook(webhook_data)
            
            # Retornar resposta
            return JsonResponse(result, status=200)
            
        except json.JSONDecodeError:
            logger.error("Erro ao decodificar JSON do webhook")
            return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro ao processar webhook: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@method_decorator(login_required, name='dispatch')
class WhatsAppDashboardView(View):
    """Dashboard administrativo do chatbot (apenas para usuários autenticados)"""
    
    def get(self, request):
        """Obter dados do dashboard"""
        try:
            # Estatísticas gerais
            stats = whatsapp_service.get_session_stats()
            
            # Sessões recentes
            recent_sessions = WhatsAppSession.objects.filter(
                is_active=True
            ).select_related('contact').order_by('-last_activity')[:10]
            
            # Mensagens recentes
            recent_messages = WhatsAppMessage.objects.filter(
                is_active=True
            ).select_related('session__contact').order_by('-created_at')[:20]
            
            # Logs recentes
            recent_logs = WhatsAppLog.objects.filter(
                is_active=True
            ).order_by('-timestamp')[:15]
            
            # Preparar dados para resposta
            dashboard_data = {
                'stats': stats,
                'recent_sessions': [
                    {
                        'id': session.id,
                        'session_id': session.session_id,
                        'contact_phone': session.contact.phone_number,
                        'contact_name': session.contact.name or 'N/A',
                        'status': session.status,
                        'current_step': session.current_step,
                        'last_activity': session.last_activity.isoformat(),
                        'started_at': session.started_at.isoformat()
                    }
                    for session in recent_sessions
                ],
                'recent_messages': [
                    {
                        'id': message.id,
                        'direction': message.direction,
                        'content': message.content[:100] + '...' if len(message.content) > 100 else message.content,
                        'is_automated': message.is_automated,
                        'contact_phone': message.session.contact.phone_number,
                        'timestamp': message.timestamp.isoformat()
                    }
                    for message in recent_messages
                ],
                'recent_logs': [
                    {
                        'id': log.id,
                        'level': log.level,
                        'message': log.message,
                        'timestamp': log.timestamp.isoformat()
                    }
                    for log in recent_logs
                ]
            }
            
            return JsonResponse(dashboard_data)
            
        except Exception as e:
            logger.error(f"Erro ao obter dados do dashboard: {e}")
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(login_required, name='dispatch')
class WhatsAppSendMessagePageView(TemplateView):
    """Página para envio de mensagens"""
    template_name = 'whatsapp/send_message.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Enviar Mensagem WhatsApp'
        
        # Obter templates disponíveis
        templates = WhatsAppTemplate.objects.filter(is_active=True).order_by('step_number')
        context['templates'] = templates
        
        # Obter contatos recentes
        recent_contacts = WhatsAppContact.objects.filter(
            is_active=True
        ).order_by('-updated_at')[:20]
        context['recent_contacts'] = recent_contacts
        
        return context


@method_decorator(login_required, name='dispatch')
class WhatsAppContactsView(View):
    """Gerenciamento de contatos"""
    
    def get(self, request):
        """Listar contatos com filtros"""
        try:
            # Parâmetros de filtro
            page = int(request.GET.get('page', 1))
            per_page = min(int(request.GET.get('per_page', 20)), 100)
            search = request.GET.get('search', '')
            filter_type = request.GET.get('filter', 'all')  # all, my_contacts, blocked, active
            
            # Query base
            contacts = WhatsAppContact.objects.filter(is_active=True)
            
            # Aplicar filtros
            if search:
                contacts = contacts.filter(
                    Q(phone_number__icontains=search) | 
                    Q(name__icontains=search)
                )
            
            if filter_type == 'my_contacts':
                contacts = contacts.filter(is_my_contact=True)
            elif filter_type == 'blocked':
                contacts = contacts.filter(is_blocked=True)
            elif filter_type == 'active':
                contacts = contacts.filter(is_my_contact=False, is_blocked=False)
            
            # Ordenar
            contacts = contacts.order_by('-updated_at')
            
            # Paginação
            paginator = Paginator(contacts, per_page)
            page_obj = paginator.get_page(page)
            
            # Preparar dados
            contacts_data = [
                {
                    'id': contact.id,
                    'phone_number': contact.phone_number,
                    'name': contact.name or '',
                    'is_my_contact': contact.is_my_contact,
                    'is_blocked': contact.is_blocked,
                    'created_at': contact.created_at.isoformat(),
                    'updated_at': contact.updated_at.isoformat()
                }
                for contact in page_obj
            ]
            
            return JsonResponse({
                'contacts': contacts_data,
                'pagination': {
                    'current_page': page_obj.number,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous()
                }
            })
            
        except Exception as e:
            logger.error(f"Erro ao listar contatos: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    def post(self, request):
        """Adicionar/atualizar contato"""
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            phone_number = data.get('phone_number', '').strip()
            name = data.get('name', '').strip()
            is_my_contact = data.get('is_my_contact', False)
            is_blocked = data.get('is_blocked', False)
            
            if not phone_number:
                return JsonResponse({'error': 'Número de telefone é obrigatório'}, status=400)
            
            # Criar ou atualizar contato
            contact, created = WhatsAppContact.objects.get_or_create(
                phone_number=phone_number,
                defaults={
                    'name': name,
                    'is_my_contact': is_my_contact,
                    'is_blocked': is_blocked
                }
            )
            
            if not created:
                contact.name = name or contact.name
                contact.is_my_contact = is_my_contact
                contact.is_blocked = is_blocked
                contact.save()
            
            return JsonResponse({
                'success': True,
                'contact': {
                    'id': contact.id,
                    'phone_number': contact.phone_number,
                    'name': contact.name,
                    'is_my_contact': contact.is_my_contact,
                    'is_blocked': contact.is_blocked,
                    'created': created
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro ao adicionar/atualizar contato: {e}")
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(login_required, name='dispatch')
class WhatsAppTemplatesView(View):
    """Gerenciamento de templates de mensagem"""
    
    def get(self, request):
        """Listar templates"""
        try:
            templates = WhatsAppTemplate.objects.filter(is_active=True).order_by('step_number')
            
            templates_data = [
                {
                    'id': template.id,
                    'name': template.name,
                    'step_number': template.step_number,
                    'content': template.content,
                    'delay_seconds': template.delay_seconds,
                    'is_active': template.is_active,
                    'created_at': template.created_at.isoformat()
                }
                for template in templates
            ]
            
            return JsonResponse({'templates': templates_data})
            
        except Exception as e:
            logger.error(f"Erro ao listar templates: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    def post(self, request):
        """Criar/atualizar template"""
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            template_id = data.get('id')
            name = data.get('name', '').strip()
            step_number = data.get('step_number', 0)
            content = data.get('content', '').strip()
            delay_seconds = data.get('delay_seconds', 5)
            
            if not name or not content:
                return JsonResponse({'error': 'Nome e conteúdo são obrigatórios'}, status=400)
            
            if template_id:
                # Atualizar template existente
                template = WhatsAppTemplate.objects.get(id=template_id, is_active=True)
                template.name = name
                template.step_number = step_number
                template.content = content
                template.delay_seconds = delay_seconds
                template.save()
                created = False
            else:
                # Criar novo template
                template = WhatsAppTemplate.objects.create(
                    name=name,
                    step_number=step_number,
                    content=content,
                    delay_seconds=delay_seconds
                )
                created = True
            
            return JsonResponse({
                'success': True,
                'template': {
                    'id': template.id,
                    'name': template.name,
                    'step_number': template.step_number,
                    'content': template.content,
                    'delay_seconds': template.delay_seconds,
                    'created': created
                }
            })
            
        except WhatsAppTemplate.DoesNotExist:
            return JsonResponse({'error': 'Template não encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro ao criar/atualizar template: {e}")
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(login_required, name='dispatch')
class WhatsAppConfigView(View):
    """Gerenciamento de configurações"""
    
    def get(self, request):
        """Obter configurações"""
        try:
            configs = WhatsAppConfig.objects.filter(is_active=True)
            
            config_data = {
                config.key: config.value
                for config in configs
            }
            
            return JsonResponse({'config': config_data})
            
        except Exception as e:
            logger.error(f"Erro ao obter configurações: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    def post(self, request):
        """Atualizar configurações"""
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            updated_configs = []
            
            for key, value in data.items():
                config, created = WhatsAppConfig.objects.get_or_create(
                    key=key,
                    defaults={'value': str(value)}
                )
                
                if not created:
                    config.value = str(value)
                    config.save()
                
                updated_configs.append({
                    'key': key,
                    'value': config.value,
                    'created': created
                })
            
            return JsonResponse({
                'success': True,
                'updated_configs': updated_configs
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro ao atualizar configurações: {e}")
            return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
@csrf_exempt
def whatsapp_cleanup(request):
    """Limpeza de dados antigos"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        days = int(data.get('days', 7))
        
        if days < 1:
            return JsonResponse({'error': 'Dias deve ser maior que 0'}, status=400)
        
        cleaned_count = whatsapp_service.cleanup_old_sessions(days)
        
        return JsonResponse({
            'success': True,
            'cleaned_sessions': cleaned_count,
            'message': f'{cleaned_count} sessões antigas foram removidas'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        logger.error(f"Erro na limpeza: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@method_decorator(login_required, name='dispatch')
class WhatsAppSendMessageView(View):
    """View para envio de mensagens via interface web"""
    
    def post(self, request):
        """Processar envio de mensagem"""
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            phone_number = data.get('phone_number', '').strip()
            message = data.get('message', '').strip()
            message_type = data.get('message_type', 'text')
            template_name = data.get('template_name', '').strip()
            parameters = data.get('parameters', [])
            
            if not phone_number:
                return JsonResponse({
                    'success': False,
                    'error': 'Número de telefone é obrigatório'
                }, status=400)
            
            # Validar formato do número
            if not phone_number.startswith('+'):
                phone_number = '+55' + phone_number.lstrip('0')
            
            if message_type == 'template' and template_name:
                # Enviar template
                result = whatsapp_service.send_template_message(
                    phone_number=phone_number,
                    template_name=template_name,
                    parameters=parameters
                )
            else:
                # Enviar mensagem de texto
                if not message:
                    return JsonResponse({
                        'success': False,
                        'error': 'Mensagem é obrigatória'
                    }, status=400)
                
                result = whatsapp_service.send_message_via_api(
                    phone_number=phone_number,
                    message=message
                )
            
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@require_http_methods(["GET"])
def whatsapp_health(request):
    """Health check do sistema"""
    try:
        # Verificar se o serviço está ativo
        is_active = whatsapp_service.is_active
        
        # Estatísticas básicas
        stats = whatsapp_service.get_session_stats()
        
        return JsonResponse({
            'status': 'healthy' if is_active else 'inactive',
            'chatbot_active': is_active,
            'timestamp': timezone.now().isoformat(),
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)