"""
Comando de gerenciamento para o chatbot WhatsApp
Uso: python manage.py whatsapp_chatbot [comando] [opções]
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from core.models import (
    WhatsAppContact, WhatsAppSession, WhatsAppMessage, 
    WhatsAppTemplate, WhatsAppConfig, WhatsAppLog
)
from core.whatsapp_service import whatsapp_service


class Command(BaseCommand):
    help = 'Gerenciar o sistema de chatbot WhatsApp'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=[
                'status', 'activate', 'deactivate', 'stats', 'cleanup',
                'add_contact', 'block_contact', 'create_template', 'set_config'
            ],
            help='Ação a ser executada'
        )
        
        # Argumentos opcionais
        parser.add_argument('--phone', type=str, help='Número de telefone')
        parser.add_argument('--name', type=str, help='Nome do contato')
        parser.add_argument('--days', type=int, default=7, help='Dias para limpeza')
        parser.add_argument('--step', type=int, help='Número do passo do template')
        parser.add_argument('--content', type=str, help='Conteúdo do template')
        parser.add_argument('--delay', type=int, default=5, help='Delay em segundos')
        parser.add_argument('--key', type=str, help='Chave de configuração')
        parser.add_argument('--value', type=str, help='Valor de configuração')

    def handle(self, *args, **options):
        action = options['action']
        
        try:
            if action == 'status':
                self.show_status()
            elif action == 'activate':
                self.activate_chatbot()
            elif action == 'deactivate':
                self.deactivate_chatbot()
            elif action == 'stats':
                self.show_stats()
            elif action == 'cleanup':
                self.cleanup_data(options['days'])
            elif action == 'add_contact':
                self.add_contact(options['phone'], options['name'])
            elif action == 'block_contact':
                self.block_contact(options['phone'])
            elif action == 'create_template':
                self.create_template(
                    options['name'], options['step'], 
                    options['content'], options['delay']
                )
            elif action == 'set_config':
                self.set_config(options['key'], options['value'])
                
        except Exception as e:
            raise CommandError(f'Erro ao executar comando: {e}')

    def show_status(self):
        """Mostrar status do chatbot"""
        is_active = whatsapp_service.is_active
        
        self.stdout.write(
            self.style.SUCCESS('✓ Chatbot ATIVO') if is_active 
            else self.style.WARNING('⚠ Chatbot INATIVO')
        )
        
        # Configurações importantes
        configs = {
            'chatbot_active': WhatsAppConfig.get_value('chatbot_active', 'false'),
            'auto_response_delay': WhatsAppConfig.get_value('auto_response_delay', '5'),
            'max_session_duration': WhatsAppConfig.get_value('max_session_duration', '3600'),
            'webhook_verify_token': WhatsAppConfig.get_value('webhook_verify_token', 'não configurado')
        }
        
        self.stdout.write('\n📋 Configurações:')
        for key, value in configs.items():
            self.stdout.write(f'  {key}: {value}')

    def activate_chatbot(self):
        """Ativar chatbot"""
        WhatsAppConfig.objects.update_or_create(
            key='chatbot_active',
            defaults={'value': 'true'}
        )
        self.stdout.write(self.style.SUCCESS('✓ Chatbot ativado com sucesso'))

    def deactivate_chatbot(self):
        """Desativar chatbot"""
        WhatsAppConfig.objects.update_or_create(
            key='chatbot_active',
            defaults={'value': 'false'}
        )
        self.stdout.write(self.style.WARNING('⚠ Chatbot desativado'))

    def show_stats(self):
        """Mostrar estatísticas"""
        stats = whatsapp_service.get_session_stats()
        
        self.stdout.write('\n📊 Estatísticas do Chatbot:')
        self.stdout.write(f'  Sessões ativas: {stats.get("active_sessions", 0)}')
        self.stdout.write(f'  Sessões completadas: {stats.get("completed_sessions", 0)}')
        self.stdout.write(f'  Total de contatos: {stats.get("total_contacts", 0)}')
        self.stdout.write(f'  Contatos filtrados: {stats.get("filtered_contacts", 0)}')
        self.stdout.write(f'  Contatos bloqueados: {stats.get("blocked_contacts", 0)}')
        self.stdout.write(f'  Mensagens hoje: {stats.get("messages_today", 0)}')
        self.stdout.write(f'  Mensagens automáticas hoje: {stats.get("automated_messages_today", 0)}')

    def cleanup_data(self, days):
        """Limpar dados antigos"""
        count = whatsapp_service.cleanup_old_sessions(days)
        self.stdout.write(
            self.style.SUCCESS(f'✓ Limpeza concluída: {count} sessões antigas removidas')
        )

    def add_contact(self, phone, name):
        """Adicionar contato à lista de filtros"""
        if not phone:
            raise CommandError('Número de telefone é obrigatório')
        
        success = whatsapp_service.add_contact_to_filter(phone, name or '', True)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Contato {phone} adicionado à lista de filtros')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao adicionar contato {phone}')
            )

    def block_contact(self, phone):
        """Bloquear contato"""
        if not phone:
            raise CommandError('Número de telefone é obrigatório')
        
        success = whatsapp_service.block_contact(phone)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Contato {phone} bloqueado')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao bloquear contato {phone}')
            )

    def create_template(self, name, step, content, delay):
        """Criar template de mensagem"""
        if not all([name, step is not None, content]):
            raise CommandError('Nome, passo e conteúdo são obrigatórios')
        
        try:
            template = WhatsAppTemplate.objects.create(
                name=name,
                step_number=step,
                content=content,
                delay_seconds=delay
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Template "{name}" criado para o passo {step}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao criar template: {e}')
            )

    def set_config(self, key, value):
        """Definir configuração"""
        if not key or value is None:
            raise CommandError('Chave e valor são obrigatórios')
        
        try:
            config, created = WhatsAppConfig.objects.update_or_create(
                key=key,
                defaults={'value': value}
            )
            
            action = 'criada' if created else 'atualizada'
            self.stdout.write(
                self.style.SUCCESS(f'✓ Configuração "{key}" {action}: {value}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao definir configuração: {e}')
            )