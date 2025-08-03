from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Session, AnalyticsExport, SEOMetrics, Cookie, PageView
from django.db import connection

class Command(BaseCommand):
    help = 'Teste final do admin - Verificação completa'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Teste Final do Admin - Verificação Completa')
        
        # Verificar dados no banco
        self.stdout.write('\n📊 Verificação de Dados:')
        
        sessions_count = Session.objects.count()
        exports_count = AnalyticsExport.objects.count()
        seo_count = SEOMetrics.objects.count()
        cookies_count = Cookie.objects.count()
        pageviews_count = PageView.objects.count()
        
        self.stdout.write(f'Sessões no banco: {sessions_count}')
        self.stdout.write(f'Exports no banco: {exports_count}')
        self.stdout.write(f'SEO no banco: {seo_count}')
        self.stdout.write(f'Cookies no banco: {cookies_count}')
        self.stdout.write(f'Page Views no banco: {pageviews_count}')
        
        # Criar usuário de teste
        self.stdout.write('\n👤 Criando usuário de teste...')
        try:
            # Remover usuário existente se houver
            User.objects.filter(username='admin_test').delete()
            
            user = User.objects.create_user(
                username='admin_test',
                email='admin@test.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write('✅ Usuário de teste criado com sucesso')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao criar usuário: {e}')
            return
        
        client = Client()
        
        # Fazer login primeiro
        self.stdout.write('\n🔐 Fazendo login...')
        login_success = client.login(username='admin_test', password='admin123')
        if login_success:
            self.stdout.write('✅ Login realizado com sucesso')
        else:
            self.stdout.write('❌ Falha no login')
            return
        
        # Testar admin padrão do Django
        self.stdout.write('\n🔗 Testando Admin Padrão do Django:')
        try:
            response = client.get('/admin/')
            self.stdout.write(f'Admin padrão - Status: {response.status_code}')
            if response.status_code == 200:
                self.stdout.write('✅ Admin padrão funcionando')
            else:
                self.stdout.write('❌ Admin padrão com problema')
        except Exception as e:
            self.stdout.write(f'❌ Erro no admin padrão: {e}')
        
        # Testar admin customizado
        self.stdout.write('\n🔗 Testando Admin Customizado:')
        try:
            response = client.get('/core_admin/')
            self.stdout.write(f'Admin customizado - Status: {response.status_code}')
            if response.status_code == 200:
                self.stdout.write('✅ Admin customizado funcionando')
            else:
                self.stdout.write('❌ Admin customizado com problema')
        except Exception as e:
            self.stdout.write(f'❌ Erro no admin customizado: {e}')
        
        # Testar URLs específicas do admin padrão
        self.stdout.write('\n🔗 Testando URLs do Admin Padrão:')
        
        admin_urls = [
            '/admin/core/session/',
            '/admin/core/analyticsexport/',
            '/admin/core/seometrics/',
            '/admin/core/cookie/',
            '/admin/core/pageview/',
        ]
        
        for url in admin_urls:
            try:
                response = client.get(url)
                self.stdout.write(f'{url} - Status: {response.status_code}')
                if response.status_code == 200:
                    self.stdout.write(f'✅ {url} funcionando')
                elif response.status_code == 302:
                    self.stdout.write(f'⚠️ {url} redirecionando (normal)')
                else:
                    self.stdout.write(f'❌ {url} com problema')
            except Exception as e:
                self.stdout.write(f'❌ Erro em {url}: {e}')
        
        # Testar URLs do admin customizado
        self.stdout.write('\n🔗 Testando URLs do Admin Customizado:')
        
        custom_urls = [
            '/core_admin/',
            '/core_admin/sessions/',
            '/core_admin/exports/',
            '/core_admin/seo/',
            '/core_admin/cookies/',
        ]
        
        for url in custom_urls:
            try:
                response = client.get(url)
                self.stdout.write(f'{url} - Status: {response.status_code}')
                if response.status_code == 200:
                    self.stdout.write(f'✅ {url} funcionando')
                else:
                    self.stdout.write(f'❌ {url} com problema')
            except Exception as e:
                self.stdout.write(f'❌ Erro em {url}: {e}')
        
        # Verificar configurações do admin
        self.stdout.write('\n🔧 Verificando Configurações do Admin:')
        try:
            from django.contrib import admin
            self.stdout.write(f'Site Header: {admin.site.site_header}')
            self.stdout.write(f'Site Title: {admin.site.site_title}')
            self.stdout.write(f'Index Title: {admin.site.index_title}')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar configurações: {e}')
        
        # Verificar templates
        self.stdout.write('\n📄 Verificando Templates:')
        try:
            from django.template.loader import get_template
            templates = [
                'admin/base.html',
                'admin/base_site.html',
                'admin/dashboard.html',
                'admin/session_list_simple.html',
                'admin/analyticsexport_list_simple.html',
            ]
            
            for template_name in templates:
                try:
                    template = get_template(template_name)
                    self.stdout.write(f'✅ {template_name} encontrado')
                except Exception as e:
                    self.stdout.write(f'❌ {template_name} não encontrado: {e}')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar templates: {e}')
        
        # Testar acesso direto às views
        self.stdout.write('\n🔗 Testando Views Diretamente:')
        try:
            from core.admin_views import admin_dashboard, session_list, analyticsexport_list
            from django.http import HttpRequest
            
            # Criar request mock
            request = HttpRequest()
            request.user = user
            
            # Testar dashboard
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
        
        self.stdout.write('\n✅ Teste final concluído!') 