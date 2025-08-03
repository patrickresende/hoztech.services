from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Testa a funcionalidade administrativa e identifica problemas'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Testando funcionalidade administrativa...')
        
        # Verificar configurações de banco de dados
        self.stdout.write('\n📊 Configurações de Banco de Dados:')
        self.stdout.write(f'DATABASE ENGINE: {settings.DATABASES["default"]["ENGINE"]}')
        self.stdout.write(f'DATABASE NAME: {settings.DATABASES["default"]["NAME"]}')
        
        # Verificar se o banco SQLite existe
        if settings.DATABASES["default"]["ENGINE"] == 'django.db.backends.sqlite3':
            db_path = settings.DATABASES["default"]["NAME"]
            if os.path.exists(db_path):
                self.stdout.write(f'✅ Banco SQLite encontrado: {db_path}')
            else:
                self.stdout.write(f'❌ Banco SQLite não encontrado: {db_path}')
        
        # Verificar modelos
        self.stdout.write('\n📋 Verificação de Modelos:')
        try:
            from core.models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
            
            # Verificar se as tabelas existem
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                
            required_tables = ['core_cookie', 'core_session', 'core_pageview', 'core_seometrics', 'core_analyticsexport']
            
            for table in required_tables:
                if table in tables:
                    self.stdout.write(f'✅ Tabela {table} existe')
                else:
                    self.stdout.write(f'❌ Tabela {table} não encontrada')
                    
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar modelos: {e}')
        
        # Verificar views administrativas
        self.stdout.write('\n🔧 Verificação de Views Administrativas:')
        
        try:
            from core.admin_views import (
                admin_dashboard, cookie_list, session_list, 
                seometrics_list, analyticsexport_list,
                export_cookies, export_sessions, export_seo, export_data
            )
            self.stdout.write('✅ Views administrativas importadas com sucesso')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao importar views: {e}')
        
        # Verificar templates administrativos
        self.stdout.write('\n📄 Verificação de Templates Administrativos:')
        admin_templates = [
            'admin/dashboard.html',
            'admin/cookie_list.html',
            'admin/session_list.html',
            'admin/seometrics_list.html',
            'admin/analyticsexport_list.html',
            'admin/export.html',
            'admin/base.html'
        ]
        
        for template in admin_templates:
            template_path = os.path.join(settings.BASE_DIR, 'core', 'templates', template)
            if os.path.exists(template_path):
                self.stdout.write(f'✅ {template}')
            else:
                self.stdout.write(f'❌ {template}')
        
        # Verificar URLs administrativas
        self.stdout.write('\n🔗 Verificação de URLs Administrativas:')
        try:
            from django.urls import reverse
            from django.test import Client
            
            # Criar usuário de teste se não existir
            user, created = User.objects.get_or_create(
                username='admin_test',
                defaults={'is_staff': True, 'is_superuser': True}
            )
            if created:
                user.set_password('admin_test_123')
                user.save()
                self.stdout.write('✅ Usuário de teste criado')
            
            client = Client()
            client.login(username='admin_test', password='admin_test_123')
            
            # Testar URLs administrativas
            admin_urls = [
                ('core_admin:admin_dashboard', '/core_admin/'),
                ('core_admin:cookie_list', '/core_admin/cookies/'),
                ('core_admin:session_list', '/core_admin/sessions/'),
                ('core_admin:seometrics_list', '/core_admin/seo/'),
                ('core_admin:analyticsexport_list', '/core_admin/exports/'),
            ]
            
            for url_name, expected_path in admin_urls:
                try:
                    url = reverse(url_name)
                    response = client.get(url)
                    if response.status_code == 200:
                        self.stdout.write(f'✅ {url_name} - {url}')
                    else:
                        self.stdout.write(f'⚠️  {url_name} - Status: {response.status_code}')
                except Exception as e:
                    self.stdout.write(f'❌ {url_name} - Erro: {e}')
                    
        except Exception as e:
            self.stdout.write(f'❌ Erro ao testar URLs: {e}')
        
        # Verificar configurações de admin
        self.stdout.write('\n⚙️  Configurações de Admin:')
        try:
            from django.contrib import admin
            self.stdout.write(f'ADMIN_SITE_HEADER: {admin.site.site_header}')
            self.stdout.write(f'ADMIN_SITE_TITLE: {admin.site.site_title}')
            self.stdout.write(f'ADMIN_INDEX_TITLE: {admin.site.index_title}')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar configurações de admin: {e}')
        
        # Verificar se há dados de exemplo
        self.stdout.write('\n📊 Verificação de Dados:')
        try:
            cookie_count = Cookie.objects.count()
            session_count = Session.objects.count()
            pageview_count = PageView.objects.count()
            seo_count = SEOMetrics.objects.count()
            export_count = AnalyticsExport.objects.count()
            
            self.stdout.write(f'Cookies: {cookie_count}')
            self.stdout.write(f'Sessões: {session_count}')
            self.stdout.write(f'Page Views: {pageview_count}')
            self.stdout.write(f'SEO Metrics: {seo_count}')
            self.stdout.write(f'Analytics Exports: {export_count}')
            
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar dados: {e}')
        
        # Recomendações
        self.stdout.write('\n💡 Recomendações:')
        self.stdout.write('1. Verificar se o banco SQLite está funcionando')
        self.stdout.write('2. Executar migrações se necessário')
        self.stdout.write('3. Criar superusuário para acesso admin')
        self.stdout.write('4. Verificar permissões de arquivos')
        self.stdout.write('5. Testar funcionalidades de export')
        
        self.stdout.write('\n✅ Teste de funcionalidade administrativa concluído!') 