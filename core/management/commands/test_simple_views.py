from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Session, AnalyticsExport, SEOMetrics

class Command(BaseCommand):
    help = 'Teste simples das views'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Teste simples das views...')
        
        # Criar usuário de teste
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            user.set_password('test123')
            user.save()
        
        client = Client()
        client.login(username='test_user', password='test123')
        
        # Testar view de sessões
        self.stdout.write('\n🔗 Testando view de sessões:')
        try:
            from core.admin_views import session_list
            from django.http import HttpRequest
            
            # Criar request mock
            request = HttpRequest()
            request.user = user
            
            # Chamar view diretamente
            response = session_list(request)
            
            self.stdout.write(f'Status: {response.status_code}')
            self.stdout.write(f'Content-Type: {response.get("Content-Type", "N/A")}')
            
            if hasattr(response, 'context'):
                context = response.context
                if context:
                    self.stdout.write(f'Context keys: {list(context.keys())}')
                    if 'sessions' in context:
                        sessions = context['sessions']
                        self.stdout.write(f'Sessões no contexto: {sessions.count()}')
                    else:
                        self.stdout.write('❌ Sessões não encontradas no contexto')
                else:
                    self.stdout.write('❌ Contexto vazio')
            else:
                self.stdout.write('❌ Contexto não disponível')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro na view de sessões: {e}')
            import traceback
            self.stdout.write(traceback.format_exc())
        
        # Testar view de exports
        self.stdout.write('\n🔗 Testando view de exports:')
        try:
            from core.admin_views import analyticsexport_list
            
            # Chamar view diretamente
            response = analyticsexport_list(request)
            
            self.stdout.write(f'Status: {response.status_code}')
            self.stdout.write(f'Content-Type: {response.get("Content-Type", "N/A")}')
            
            if hasattr(response, 'context'):
                context = response.context
                if context:
                    self.stdout.write(f'Context keys: {list(context.keys())}')
                    if 'exports' in context:
                        exports = context['exports']
                        self.stdout.write(f'Exports no contexto: {exports.count()}')
                    else:
                        self.stdout.write('❌ Exports não encontrados no contexto')
                else:
                    self.stdout.write('❌ Contexto vazio')
            else:
                self.stdout.write('❌ Contexto não disponível')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro na view de exports: {e}')
            import traceback
            self.stdout.write(traceback.format_exc())
        
        # Testar view de SEO
        self.stdout.write('\n🔗 Testando view de SEO:')
        try:
            from core.admin_views import seometrics_list
            
            # Chamar view diretamente
            response = seometrics_list(request)
            
            self.stdout.write(f'Status: {response.status_code}')
            self.stdout.write(f'Content-Type: {response.get("Content-Type", "N/A")}')
            
            if hasattr(response, 'context'):
                context = response.context
                if context:
                    self.stdout.write(f'Context keys: {list(context.keys())}')
                    if 'metrics' in context:
                        metrics = context['metrics']
                        self.stdout.write(f'Métricas no contexto: {metrics.count()}')
                    else:
                        self.stdout.write('❌ Métricas não encontradas no contexto')
                else:
                    self.stdout.write('❌ Contexto vazio')
            else:
                self.stdout.write('❌ Contexto não disponível')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro na view de SEO: {e}')
            import traceback
            self.stdout.write(traceback.format_exc())
        
        # Testar view de teste
        self.stdout.write('\n🔗 Testando view de teste:')
        try:
            from core.admin_views import test_view
            
            # Chamar view diretamente
            response = test_view(request)
            
            self.stdout.write(f'Status: {response.status_code}')
            self.stdout.write(f'Content-Type: {response.get("Content-Type", "N/A")}')
            
            if hasattr(response, 'context'):
                context = response.context
                if context:
                    self.stdout.write(f'Context keys: {list(context.keys())}')
                    if 'test_data' in context:
                        test_data = context['test_data']
                        self.stdout.write(f'Dados de teste: {test_data}')
                    if 'sessions' in context:
                        sessions = context['sessions']
                        self.stdout.write(f'Sessões no contexto: {sessions.count()}')
                    if 'exports' in context:
                        exports = context['exports']
                        self.stdout.write(f'Exports no contexto: {exports.count()}')
                    if 'metrics' in context:
                        metrics = context['metrics']
                        self.stdout.write(f'Métricas no contexto: {metrics.count()}')
                else:
                    self.stdout.write('❌ Contexto vazio')
            else:
                self.stdout.write('❌ Contexto não disponível')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro na view de teste: {e}')
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write('\n✅ Teste simples concluído!') 