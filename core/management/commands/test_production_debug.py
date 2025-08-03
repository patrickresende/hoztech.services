from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest
from core.models import Session, AnalyticsExport, SEOMetrics, Cookie, PageView
import os
import sys

class Command(BaseCommand):
    help = 'Teste específico para debug de produção - Verifica configurações críticas'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Teste de Debug de Produção - Verificação de Configurações Críticas')
        
        # 1. Verificar configurações de ambiente
        self.stdout.write('\n📋 Verificando Configurações de Ambiente:')
        self.stdout.write(f'ENVIRONMENT: {getattr(settings, "ENVIRONMENT", "N/A")}')
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        self.stdout.write(f'CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}')
        
        # 2. Verificar configurações de banco de dados
        self.stdout.write('\n🗄️ Verificando Configurações de Banco de Dados:')
        db_engine = settings.DATABASES['default']['ENGINE']
        self.stdout.write(f'Database Engine: {db_engine}')
        
        if 'postgresql' in db_engine:
            self.stdout.write('✅ Usando PostgreSQL (produção)')
        elif 'sqlite' in db_engine:
            self.stdout.write('✅ Usando SQLite (desenvolvimento)')
        else:
            self.stdout.write('⚠️ Engine de banco desconhecido')
        
        # 3. Verificar configurações de arquivos estáticos
        self.stdout.write('\n📁 Verificando Configurações de Arquivos Estáticos:')
        self.stdout.write(f'STATIC_URL: {settings.STATIC_URL}')
        self.stdout.write(f'STATIC_ROOT: {settings.STATIC_ROOT}')
        self.stdout.write(f'STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}')
        
        # 4. Verificar configurações de segurança
        self.stdout.write('\n🔒 Verificando Configurações de Segurança:')
        self.stdout.write(f'SECURE_SSL_REDIRECT: {getattr(settings, "SECURE_SSL_REDIRECT", "N/A")}')
        self.stdout.write(f'SESSION_COOKIE_SECURE: {getattr(settings, "SESSION_COOKIE_SECURE", "N/A")}')
        self.stdout.write(f'CSRF_COOKIE_SECURE: {getattr(settings, "CSRF_COOKIE_SECURE", "N/A")}')
        
        # 5. Verificar middleware
        self.stdout.write('\n⚙️ Verificando Middleware:')
        for middleware in settings.MIDDLEWARE:
            self.stdout.write(f'  - {middleware}')
        
        # 6. Testar conexão com banco de dados
        self.stdout.write('\n🔗 Testando Conexão com Banco de Dados:')
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('✅ Conexão com banco de dados OK')
        except Exception as e:
            self.stdout.write(f'❌ Erro na conexão com banco: {e}')
        
        # 7. Verificar dados no banco
        self.stdout.write('\n📊 Verificando Dados no Banco:')
        try:
            session_count = Session.objects.count()
            export_count = AnalyticsExport.objects.count()
            seo_count = SEOMetrics.objects.count()
            cookie_count = Cookie.objects.count()
            pageview_count = PageView.objects.count()
            
            self.stdout.write(f'Sessões: {session_count}')
            self.stdout.write(f'Exports: {export_count}')
            self.stdout.write(f'SEO Metrics: {seo_count}')
            self.stdout.write(f'Cookies: {cookie_count}')
            self.stdout.write(f'Page Views: {pageview_count}')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao consultar dados: {e}')
        
        # 8. Criar usuário de teste
        self.stdout.write('\n👤 Criando usuário de teste...')
        try:
            user, created = User.objects.get_or_create(
                username='admin_test',
                defaults={
                    'email': 'test@example.com',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                user.set_password('admin123')
                user.save()
                self.stdout.write('✅ Usuário de teste criado')
            else:
                self.stdout.write('✅ Usuário de teste já existe')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao criar usuário: {e}')
            return
        
        # 9. Testar login
        self.stdout.write('\n🔐 Testando login...')
        client = Client()
        login_success = client.login(username='admin_test', password='admin123')
        if login_success:
            self.stdout.write('✅ Login realizado com sucesso')
        else:
            self.stdout.write('❌ Falha no login')
            return
        
        # 10. Testar URLs críticas
        self.stdout.write('\n🔗 Testando URLs Críticas:')
        
        # URLs do admin padrão
        admin_urls = [
            '/admin/',
            '/admin/core/session/',
            '/admin/core/analyticsexport/',
            '/admin/core/seometrics/',
            '/admin/core/cookie/',
            '/admin/core/pageview/',
        ]
        
        for url in admin_urls:
            try:
                response = client.get(url)
                status = response.status_code
                if status == 200:
                    self.stdout.write(f'✅ {url} - Status: {status}')
                elif status == 302:
                    self.stdout.write(f'⚠️ {url} - Status: {status} (redirect)')
                else:
                    self.stdout.write(f'❌ {url} - Status: {status}')
            except Exception as e:
                self.stdout.write(f'❌ {url} - Erro: {e}')
        
        # URLs do admin customizado
        custom_admin_urls = [
            '/core_admin/',
            '/core_admin/sessions/',
            '/core_admin/exports/',
            '/core_admin/seo/',
            '/core_admin/cookies/',
        ]
        
        for url in custom_admin_urls:
            try:
                response = client.get(url)
                status = response.status_code
                if status == 200:
                    self.stdout.write(f'✅ {url} - Status: {status}')
                elif status == 302:
                    self.stdout.write(f'⚠️ {url} - Status: {status} (redirect)')
                else:
                    self.stdout.write(f'❌ {url} - Status: {status}')
            except Exception as e:
                self.stdout.write(f'❌ {url} - Erro: {e}')
        
        # 11. Testar views diretamente
        self.stdout.write('\n🔧 Testando Views Diretamente:')
        try:
            from core.admin_views import admin_dashboard, session_list, analyticsexport_list
            
            # Testar dashboard
            request = HttpRequest()
            request.user = user
            response = admin_dashboard(request)
            self.stdout.write(f'Dashboard view - Status: {response.status_code}')
            
            # Testar session list
            response = session_list(request)
            self.stdout.write(f'Session list view - Status: {response.status_code}')
            
            # Testar analytics export list
            response = analyticsexport_list(request)
            self.stdout.write(f'Analytics export view - Status: {response.status_code}')
            
        except Exception as e:
            self.stdout.write(f'❌ Erro ao testar views: {e}')
        
        # 12. Verificar templates
        self.stdout.write('\n📄 Verificando Templates:')
        from django.template.loader import get_template
        
        templates_to_check = [
            'admin/base.html',
            'admin/base_site.html',
            'admin/dashboard.html',
            'admin/session_list_simple.html',
            'admin/analyticsexport_list_simple.html',
        ]
        
        for template_name in templates_to_check:
            try:
                template = get_template(template_name)
                self.stdout.write(f'✅ {template_name} encontrado')
            except Exception as e:
                self.stdout.write(f'❌ {template_name} não encontrado: {e}')
        
        # 13. Verificar configurações do admin
        self.stdout.write('\n⚙️ Verificando Configurações do Admin:')
        from django.contrib import admin
        self.stdout.write(f'Site Header: {admin.site.site_header}')
        self.stdout.write(f'Site Title: {admin.site.site_title}')
        self.stdout.write(f'Index Title: {admin.site.index_title}')
        
        # 14. Verificar variáveis de ambiente
        self.stdout.write('\n🌍 Verificando Variáveis de Ambiente:')
        env_vars = [
            'DATABASE_URL',
            'SECRET_KEY',
            'ENVIRONMENT',
            'DEBUG',
            'ALLOWED_HOSTS',
            'CSRF_TRUSTED_ORIGINS',
        ]
        
        for var in env_vars:
            value = os.getenv(var, 'NÃO DEFINIDA')
            if var in ['SECRET_KEY', 'DATABASE_URL']:
                # Mascarar valores sensíveis
                if value != 'NÃO DEFINIDA':
                    value = value[:10] + '...' if len(value) > 10 else value
            self.stdout.write(f'{var}: {value}')
        
        self.stdout.write('\n✅ Teste de debug de produção concluído!')
        
        # 15. Resumo de problemas potenciais
        self.stdout.write('\n📋 Resumo de Problemas Potenciais:')
        
        if settings.DEBUG:
            self.stdout.write('⚠️ DEBUG está ativado - pode causar problemas em produção')
        
        if 'sqlite' in db_engine and getattr(settings, 'ENVIRONMENT', '') == 'production':
            self.stdout.write('⚠️ Usando SQLite em produção - não recomendado')
        
        if not settings.ALLOWED_HOSTS:
            self.stdout.write('⚠️ ALLOWED_HOSTS está vazio')
        
        if not settings.CSRF_TRUSTED_ORIGINS:
            self.stdout.write('⚠️ CSRF_TRUSTED_ORIGINS está vazio')
        
        if 'whitenoise' not in str(settings.MIDDLEWARE).lower():
            self.stdout.write('⚠️ WhiteNoise não está no middleware')
        
        self.stdout.write('\n🎯 Recomendações:')
        self.stdout.write('1. Verifique se DEBUG=False em produção')
        self.stdout.write('2. Configure ALLOWED_HOSTS corretamente')
        self.stdout.write('3. Configure CSRF_TRUSTED_ORIGINS para HTTPS')
        self.stdout.write('4. Use PostgreSQL em produção')
        self.stdout.write('5. Configure WhiteNoise para arquivos estáticos') 