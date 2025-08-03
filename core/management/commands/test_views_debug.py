from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Session, AnalyticsExport, SEOMetrics
from django.db import connection

class Command(BaseCommand):
    help = 'Debug das views problemáticas'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Debug das views problemáticas...')
        
        # Verificar dados no banco
        self.stdout.write('\n📊 Verificação de Dados:')
        
        sessions_count = Session.objects.count()
        exports_count = AnalyticsExport.objects.count()
        seo_count = SEOMetrics.objects.count()
        
        self.stdout.write(f'Sessões no banco: {sessions_count}')
        self.stdout.write(f'Exports no banco: {exports_count}')
        self.stdout.write(f'SEO no banco: {seo_count}')
        
        # Verificar dados ativos
        active_sessions = Session.objects.filter(is_active=True).count()
        active_exports = AnalyticsExport.objects.filter(is_active=True).count()
        active_seo = SEOMetrics.objects.filter(is_active=True).count()
        
        self.stdout.write(f'Sessões ativas: {active_sessions}')
        self.stdout.write(f'Exports ativos: {active_exports}')
        self.stdout.write(f'SEO ativos: {active_seo}')
        
        # Criar usuário de teste
        user, created = User.objects.get_or_create(
            username='debug_user',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            user.set_password('debug123')
            user.save()
            self.stdout.write('✅ Usuário de debug criado')
        
        client = Client()
        client.login(username='debug_user', password='debug123')
        
        # Testar view de sessões
        self.stdout.write('\n🔗 Testando view de sessões:')
        try:
            url = reverse('core_admin:session_list')
            self.stdout.write(f'URL: {url}')
            
            response = client.get(url)
            self.stdout.write(f'Status: {response.status_code}')
            
            if hasattr(response, 'context'):
                context = response.context
                self.stdout.write(f'Context keys: {list(context.keys()) if context else "None"}')
                
                if 'sessions' in context:
                    sessions = context['sessions']
                    self.stdout.write(f'Sessões no contexto: {sessions.count() if hasattr(sessions, "count") else len(sessions)}')
                else:
                    self.stdout.write('❌ Sessões não encontradas no contexto')
            else:
                self.stdout.write('❌ Contexto não disponível')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro na view de sessões: {e}')
        
        # Testar view de exports
        self.stdout.write('\n🔗 Testando view de exports:')
        try:
            url = reverse('core_admin:analyticsexport_list')
            self.stdout.write(f'URL: {url}')
            
            response = client.get(url)
            self.stdout.write(f'Status: {response.status_code}')
            
            if hasattr(response, 'context'):
                context = response.context
                self.stdout.write(f'Context keys: {list(context.keys()) if context else "None"}')
                
                if 'exports' in context:
                    exports = context['exports']
                    self.stdout.write(f'Exports no contexto: {exports.count() if hasattr(exports, "count") else len(exports)}')
                else:
                    self.stdout.write('❌ Exports não encontrados no contexto')
            else:
                self.stdout.write('❌ Contexto não disponível')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro na view de exports: {e}')
        
        # Testar view de SEO
        self.stdout.write('\n🔗 Testando view de SEO:')
        try:
            url = reverse('core_admin:seometrics_list')
            self.stdout.write(f'URL: {url}')
            
            response = client.get(url)
            self.stdout.write(f'Status: {response.status_code}')
            
            if hasattr(response, 'context'):
                context = response.context
                self.stdout.write(f'Context keys: {list(context.keys()) if context else "None"}')
                
                if 'metrics' in context:
                    metrics = context['metrics']
                    self.stdout.write(f'Métricas no contexto: {metrics.count() if hasattr(metrics, "count") else len(metrics)}')
                else:
                    self.stdout.write('❌ Métricas não encontradas no contexto')
            else:
                self.stdout.write('❌ Contexto não disponível')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro na view de SEO: {e}')
        
        # Verificar queries SQL
        self.stdout.write('\n🔍 Verificando queries SQL:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM core_session WHERE is_active = 1")
                active_sessions_db = cursor.fetchone()[0]
                self.stdout.write(f'Sessões ativas (SQL): {active_sessions_db}')
                
                cursor.execute("SELECT COUNT(*) FROM core_analyticsexport WHERE is_active = 1")
                active_exports_db = cursor.fetchone()[0]
                self.stdout.write(f'Exports ativos (SQL): {active_exports_db}')
                
                cursor.execute("SELECT COUNT(*) FROM core_seometrics WHERE is_active = 1")
                active_seo_db = cursor.fetchone()[0]
                self.stdout.write(f'SEO ativos (SQL): {active_seo_db}')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar SQL: {e}')
        
        self.stdout.write('\n✅ Debug concluído!') 