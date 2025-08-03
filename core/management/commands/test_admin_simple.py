from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
from core.models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
from django.test import RequestFactory
from django.contrib.admin.views.decorators import staff_member_required
from core import admin_views
import logging

logger = logging.getLogger('core.admin')

class Command(BaseCommand):
    help = 'Testa o admin de forma simples sem middlewares'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostra informações detalhadas',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        
        self.stdout.write(
            self.style.SUCCESS('=== Teste Simples do Admin ===')
        )
        
        # Teste 1: Conexão básica
        self.stdout.write('\n1. Testando conexão básica...')
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('✓ Conexão básica: OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erro na conexão básica: {e}'))
            return

        # Teste 2: Contagem simples
        self.stdout.write('\n2. Testando contagem simples...')
        try:
            session_count = Session.objects.count()
            self.stdout.write(self.style.SUCCESS(f'✓ Total de sessões: {session_count}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erro na contagem: {e}'))
            return

        # Teste 3: Query com filtro
        self.stdout.write('\n3. Testando query com filtro...')
        try:
            active_sessions = Session.objects.filter(is_active=True).count()
            self.stdout.write(self.style.SUCCESS(f'✓ Sessões ativas: {active_sessions}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erro na query com filtro: {e}'))
            return

        # Teste 4: Testar view do dashboard
        self.stdout.write('\n4. Testando view do dashboard...')
        try:
            # Criar request fake
            factory = RequestFactory()
            request = factory.get('/core_admin/')
            request.user = User.objects.filter(is_staff=True).first()
            
            if not request.user:
                self.stdout.write(self.style.WARNING('⚠ Nenhum usuário admin encontrado'))
                return
            
            # Testar view
            response = admin_views.admin_dashboard(request)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✓ View do dashboard: OK'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ View do dashboard: Status {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erro na view do dashboard: {e}'))
            if verbose:
                import traceback
                self.stdout.write(traceback.format_exc())

        # Teste 5: Testar view de cookies
        self.stdout.write('\n5. Testando view de cookies...')
        try:
            response = admin_views.cookie_list(request)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✓ View de cookies: OK'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ View de cookies: Status {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erro na view de cookies: {e}'))

        # Teste 6: Testar view de sessões
        self.stdout.write('\n6. Testando view de sessões...')
        try:
            response = admin_views.session_list(request)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✓ View de sessões: OK'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ View de sessões: Status {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erro na view de sessões: {e}'))

        # Teste 7: Verificar configurações
        self.stdout.write('\n7. Verificando configurações...')
        from django.conf import settings
        
        debug_status = "Ativado" if settings.DEBUG else "Desativado"
        self.stdout.write(f'✓ DEBUG: {debug_status}')
        
        environment = getattr(settings, 'ENVIRONMENT', 'Não definido')
        self.stdout.write(f'✓ Ambiente: {environment}')
        
        # Verificar se os middlewares estão ativos
        admin_middleware_active = any(
            'AdminErrorMiddleware' in middleware 
            for middleware in settings.MIDDLEWARE
        )
        self.stdout.write(f'✓ AdminErrorMiddleware: {"Ativo" if admin_middleware_active else "Inativo"}')

        self.stdout.write(
            self.style.SUCCESS('\n=== Teste simples concluído ===')
        )
        
        if verbose:
            self.stdout.write(
                self.style.SUCCESS('\nPara mais informações, execute: python manage.py check_database --verbose')
            ) 