from django.core.management.base import BaseCommand, CommandError
from core.whatsapp_service import WhatsAppChatbotService
import json


class Command(BaseCommand):
    help = 'Enviar mensagem via WhatsApp Business API'

    def add_arguments(self, parser):
        parser.add_argument(
            'phone_number',
            type=str,
            help='Número de telefone (formato: +5511999999999)'
        )
        
        parser.add_argument(
            'message',
            type=str,
            help='Mensagem a ser enviada'
        )
        
        parser.add_argument(
            '--template',
            type=str,
            help='Nome do template (para mensagens template)'
        )
        
        parser.add_argument(
            '--parameters',
            type=str,
            nargs='*',
            help='Parâmetros para o template'
        )
        
        parser.add_argument(
            '--language',
            type=str,
            default='pt_BR',
            help='Código do idioma (padrão: pt_BR)'
        )

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        message = options['message']
        template = options.get('template')
        parameters = options.get('parameters', [])
        language = options['language']

        # Validar formato do número
        if not phone_number.startswith('+'):
            raise CommandError('Número deve começar com + (ex: +5511999999999)')

        service = WhatsAppChatbotService()

        try:
            if template:
                # Enviar mensagem template
                self.stdout.write(f'Enviando template "{template}" para {phone_number}...')
                result = service.send_template_message(
                    phone_number=phone_number,
                    template_name=template,
                    language_code=language,
                    parameters=parameters
                )
            else:
                # Enviar mensagem de texto
                self.stdout.write(f'Enviando mensagem para {phone_number}...')
                result = service.send_message_via_api(
                    phone_number=phone_number,
                    message=message
                )

            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Mensagem enviada com sucesso!\n'
                        f'ID da mensagem: {result.get("message_id", "N/A")}'
                    )
                )
                
                # Mostrar resposta da API se disponível
                if 'response' in result:
                    self.stdout.write(
                        f'Resposta da API:\n{json.dumps(result["response"], indent=2)}'
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Erro ao enviar mensagem: {result["error"]}'
                    )
                )
                
                if 'status_code' in result:
                    self.stdout.write(f'Código de status: {result["status_code"]}')

        except Exception as e:
            raise CommandError(f'Erro inesperado: {str(e)}')