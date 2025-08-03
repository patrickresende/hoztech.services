from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.db import connection
from core.models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
import os
from django.db import models

class Command(BaseCommand):
    help = 'Teste detalhado das funcionalidades administrativas problemáticas'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Teste detalhado das funcionalidades administrativas...')
        
        # Verificar dados específicos
        self.stdout.write('\n📊 Verificação Detalhada de Dados:')
        
        # Verificar sessões
        sessions = Session.objects.all()
        self.stdout.write(f'Total de sessões: {sessions.count()}')
        if sessions.exists():
            session = sessions.first()
            self.stdout.write(f'Exemplo de sessão: {session.session_key} - {session.ip_address}')
        
        # Verificar exports
        exports = AnalyticsExport.objects.all()
        self.stdout.write(f'Total de exports: {exports.count()}')
        if exports.exists():
            export = exports.first()
            self.stdout.write(f'Exemplo de export: {export.name} - {export.format}')
        
        # Verificar se há dados para SEO
        seo_metrics = SEOMetrics.objects.all()
        self.stdout.write(f'Total de métricas SEO: {seo_metrics.count()}')
        if seo_metrics.exists():
            seo = seo_metrics.first()
            self.stdout.write(f'Exemplo de SEO: {seo.url} - Score: {seo.page_speed_score}')
        
        # Verificar se há dados para ADS (page views)
        page_views = PageView.objects.all()
        self.stdout.write(f'Total de page views: {page_views.count()}')
        if page_views.exists():
            pv = page_views.first()
            self.stdout.write(f'Exemplo de page view: {pv.url} - {pv.title}')
        
        # Testar URLs específicas
        self.stdout.write('\n🔗 Teste de URLs Específicas:')
        
        try:
            # Criar usuário de teste
            user, created = User.objects.get_or_create(
                username='admin_test_detailed',
                defaults={'is_staff': True, 'is_superuser': True}
            )
            if created:
                user.set_password('admin_test_123')
                user.save()
            
            client = Client()
            client.login(username='admin_test_detailed', password='admin_test_123')
            
            # Testar URLs problemáticas
            test_urls = [
                ('core_admin:session_list', 'Sessões'),
                ('core_admin:analyticsexport_list', 'Analytics Exports'),
                ('core_admin:seometrics_list', 'SEO Metrics'),
                ('core_admin:export_sessions', 'Export Sessões'),
                ('core_admin:export_seo', 'Export SEO'),
                ('core_admin:export_data', 'Export Completo'),
            ]
            
            for url_name, description in test_urls:
                try:
                    url = reverse(url_name)
                    response = client.get(url)
                    if response.status_code == 200:
                        self.stdout.write(f'✅ {description}: {url} - Status: {response.status_code}')
                        
                        # Verificar se há conteúdo na resposta
                        if hasattr(response, 'content'):
                            content_length = len(response.content)
                            self.stdout.write(f'   📄 Conteúdo: {content_length} bytes')
                            
                            # Verificar se há dados na resposta
                            if hasattr(response, 'context') and response.context:
                                context_data = response.context
                                if 'sessions' in context_data or 'exports' in context_data or 'metrics' in context_data:
                                    self.stdout.write(f'   📊 Dados encontrados no contexto')
                                else:
                                    self.stdout.write(f'   ⚠️  Nenhum dado encontrado no contexto')
                            else:
                                self.stdout.write(f'   ⚠️  Contexto não disponível')
                    else:
                        self.stdout.write(f'❌ {description}: {url} - Status: {response.status_code}')
                        
                except Exception as e:
                    self.stdout.write(f'❌ {description}: Erro - {e}')
                    
        except Exception as e:
            self.stdout.write(f'❌ Erro ao testar URLs: {e}')
        
        # Verificar templates
        self.stdout.write('\n📄 Verificação de Templates:')
        template_files = [
            'admin/session_list.html',
            'admin/analyticsexport_list.html',
            'admin/seometrics_list.html',
            'admin/base.html',
            'admin/dashboard.html'
        ]
        
        for template in template_files:
            template_path = os.path.join(settings.BASE_DIR, 'core', 'templates', template)
            if os.path.exists(template_path):
                file_size = os.path.getsize(template_path)
                self.stdout.write(f'✅ {template} - {file_size} bytes')
            else:
                self.stdout.write(f'❌ {template} - Não encontrado')
        
        # Verificar views administrativas
        self.stdout.write('\n🔧 Verificação de Views:')
        try:
            from core.admin_views import (
                session_list, analyticsexport_list, seometrics_list,
                export_sessions, export_seo, export_data
            )
            self.stdout.write('✅ Views administrativas importadas')
            
            # Verificar se as funções são callable
            views_to_check = [
                (session_list, 'session_list'),
                (analyticsexport_list, 'analyticsexport_list'),
                (seometrics_list, 'seometrics_list'),
                (export_sessions, 'export_sessions'),
                (export_seo, 'export_seo'),
                (export_data, 'export_data'),
            ]
            
            for view_func, name in views_to_check:
                if callable(view_func):
                    self.stdout.write(f'✅ {name} é callable')
                else:
                    self.stdout.write(f'❌ {name} não é callable')
                    
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar views: {e}')
        
        # Verificar dados para SEO e ADS
        self.stdout.write('\n🎯 Verificação de Dados para SEO e ADS:')
        
        # Dados para SEO
        seo_data = {
            'total_pages': SEOMetrics.objects.count(),
            'pages_with_scores': SEOMetrics.objects.filter(page_speed_score__isnull=False).count(),
            'avg_speed_score': SEOMetrics.objects.filter(page_speed_score__isnull=False).aggregate(avg=models.Avg('page_speed_score'))['avg'],
            'mobile_friendly_pages': SEOMetrics.objects.filter(mobile_friendly_score__gte=80).count(),
        }
        
        self.stdout.write('📊 Dados para SEO:')
        for key, value in seo_data.items():
            self.stdout.write(f'   {key}: {value}')
        
        # Dados para ADS
        ads_data = {
            'total_page_views': PageView.objects.count(),
            'unique_sessions': Session.objects.count(),
            'top_pages': PageView.objects.values('url').annotate(count=models.Count('id')).order_by('-count')[:5],
            'recent_activity': Session.objects.filter(is_active=True).count(),
        }
        
        self.stdout.write('📊 Dados para ADS:')
        for key, value in ads_data.items():
            if key == 'top_pages':
                self.stdout.write(f'   {key}:')
                for page in value:
                    self.stdout.write(f'     {page["url"]}: {page["count"]} views')
            else:
                self.stdout.write(f'   {key}: {value}')
        
        # Recomendações específicas
        self.stdout.write('\n💡 Recomendações Específicas:')
        
        if seo_data['total_pages'] == 0:
            self.stdout.write('⚠️  Nenhuma métrica SEO encontrada - Execute create_sample_data')
        
        if ads_data['total_page_views'] == 0:
            self.stdout.write('⚠️  Nenhum page view encontrado - Execute create_sample_data')
        
        if exports.count() == 0:
            self.stdout.write('⚠️  Nenhum export encontrado - Teste as funcionalidades de export')
        
        self.stdout.write('\n✅ Teste detalhado concluído!') 