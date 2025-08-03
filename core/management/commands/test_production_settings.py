from django.core.management.base import BaseCommand
from django.conf import settings
from django.test import RequestFactory
from django.contrib.auth.models import User
from core.admin_views import admin_dashboard, session_list, analyticsexport_list
import os
import sys

class Command(BaseCommand):
    help = 'Teste específico para configurações de produção'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Teste de Configurações de Produção')
        
        # Simular ambiente de produção
        os.environ['ENVIRONMENT'] = 'production'
        os.environ['DEBUG'] = 'False'
        
        # Recarregar configurações
        from django.conf import settings
        from django import setup
        setup()
        
        self.stdout.write('\n📋 Configurações de Produção:')
        self.stdout.write(f'ENVIRONMENT: {getattr(settings, "ENVIRONMENT", "N/A")}')
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        self.stdout.write(f'CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}')
        
        # Verificar configurações de segurança
        self.stdout.write('\n🔒 Configurações de Segurança:')
        self.stdout.write(f'SECURE_SSL_REDIRECT: {getattr(settings, "SECURE_SSL_REDIRECT", "N/A")}')
        self.stdout.write(f'SESSION_COOKIE_SECURE: {getattr(settings, "SESSION_COOKIE_SECURE", "N/A")}')
        self.stdout.write(f'CSRF_COOKIE_SECURE: {getattr(settings, "CSRF_COOKIE_SECURE", "N/A")}')
        
        # Verificar configurações de banco
        self.stdout.write('\n🗄️ Configurações de Banco:')
        db_engine = settings.DATABASES['default']['ENGINE']
        self.stdout.write(f'Database Engine: {db_engine}')
        
        # Verificar configurações de arquivos estáticos
        self.stdout.write('\n📁 Configurações de Arquivos Estáticos:')
        self.stdout.write(f'STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}')
        self.stdout.write(f'WHITENOISE_USE_FINDERS: {getattr(settings, "WHITENOISE_USE_FINDERS", "N/A")}')
        
        # Testar views com configurações de produção
        self.stdout.write('\n🔧 Testando Views com Configurações de Produção:')
        
        try:
            # Criar usuário de teste
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
            
            # Criar request factory
            factory = RequestFactory()
            
            # Testar dashboard
            request = factory.get('/core_admin/')
            request.user = user
            response = admin_dashboard(request)
            self.stdout.write(f'Dashboard - Status: {response.status_code}')
            
            # Testar session list
            request = factory.get('/core_admin/sessions/')
            request.user = user
            response = session_list(request)
            self.stdout.write(f'Session List - Status: {response.status_code}')
            
            # Testar analytics export list
            request = factory.get('/core_admin/exports/')
            request.user = user
            response = analyticsexport_list(request)
            self.stdout.write(f'Analytics Export - Status: {response.status_code}')
            
        except Exception as e:
            self.stdout.write(f'❌ Erro ao testar views: {e}')
            import traceback
            self.stdout.write(traceback.format_exc())
        
        # Verificar middleware
        self.stdout.write('\n⚙️ Middleware:')
        for middleware in settings.MIDDLEWARE:
            self.stdout.write(f'  - {middleware}')
        
        # Verificar templates
        self.stdout.write('\n📄 Verificando Templates:')
        from django.template.loader import get_template
        
        templates_to_check = [
            'admin/base.html',
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
        
        # Verificar configurações do admin
        self.stdout.write('\n⚙️ Configurações do Admin:')
        from django.contrib import admin
        self.stdout.write(f'Site Header: {admin.site.site_header}')
        self.stdout.write(f'Site Title: {admin.site.site_title}')
        self.stdout.write(f'Index Title: {admin.site.index_title}')
        
        self.stdout.write('\n✅ Teste de configurações de produção concluído!') 