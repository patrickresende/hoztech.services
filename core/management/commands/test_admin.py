from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
from core.models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
import logging

logger = logging.getLogger('core.admin')

class Command(BaseCommand):
    help = 'Testa a funcionalidade do admin e conectividade com banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostra informações detalhadas',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        
        self.stdout.write(
            self.style.SUCCESS('=== Teste de Funcionalidade do Admin ===')
        )
        
        # Teste 1: Conexão com banco de dados
        self.stdout.write('\n1. Testando conexão com banco de dados...')
        try:
            connection.ensure_connection()
            self.stdout.write(
                self.style.SUCCESS('✓ Conexão com banco de dados: OK')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro na conexão com banco: {e}')
            )
            return

        # Teste 2: Contagem de registros
        self.stdout.write('\n2. Testando contagem de registros...')
        try:
            cookie_count = Cookie.objects.filter(is_active=True).count()
            session_count = Session.objects.filter(is_active=True).count()
            pageview_count = PageView.objects.filter(is_active=True).count()
            seo_count = SEOMetrics.objects.filter(is_active=True).count()
            export_count = AnalyticsExport.objects.filter(is_active=True).count()
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Cookies ativos: {cookie_count}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Sessões ativas: {session_count}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ PageViews ativos: {pageview_count}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Métricas SEO ativas: {seo_count}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Exports ativos: {export_count}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao contar registros: {e}')
            )

        # Teste 3: Queries complexas
        self.stdout.write('\n3. Testando queries complexas...')
        try:
            # Teste de agregação
            from django.db.models import Count
            top_pages = PageView.objects.filter(is_active=True).values(
                'url', 'title'
            ).annotate(
                total=Count('id')
            ).order_by('-total')[:5]
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Query de top páginas: OK ({len(top_pages)} resultados)')
            )
            
            if verbose and top_pages:
                for page in top_pages:
                    self.stdout.write(f'   - {page["url"]}: {page["total"]} views')
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro em query complexa: {e}')
            )

        # Teste 4: Usuários admin
        self.stdout.write('\n4. Testando usuários admin...')
        try:
            admin_users = User.objects.filter(is_staff=True, is_active=True)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuários admin ativos: {admin_users.count()}')
            )
            
            if verbose:
                for user in admin_users:
                    self.stdout.write(f'   - {user.username} ({user.email})')
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao verificar usuários admin: {e}')
            )

        # Teste 5: Verificar XlsxWriter
        self.stdout.write('\n5. Testando dependências...')
        try:
            import xlsxwriter
            self.stdout.write(
                self.style.SUCCESS('✓ XlsxWriter: Disponível')
            )
        except ImportError:
            self.stdout.write(
                self.style.WARNING('⚠ XlsxWriter: Não disponível (exportação Excel desabilitada)')
            )

        # Teste 6: Verificar configurações
        self.stdout.write('\n6. Verificando configurações...')
        from django.conf import settings
        
        debug_status = "Ativado" if settings.DEBUG else "Desativado"
        self.stdout.write(
            self.style.SUCCESS(f'✓ DEBUG: {debug_status}')
        )
        
        environment = getattr(settings, 'ENVIRONMENT', 'Não definido')
        self.stdout.write(
            self.style.SUCCESS(f'✓ Ambiente: {environment}')
        )

        # Teste 7: Performance
        self.stdout.write('\n7. Teste de performance...')
        import time
        
        try:
            start_time = time.time()
            Session.objects.filter(is_active=True).count()
            session_time = time.time() - start_time
            
            start_time = time.time()
            PageView.objects.filter(is_active=True).count()
            pageview_time = time.time() - start_time
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Query de sessões: {session_time:.3f}s')
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Query de pageviews: {pageview_time:.3f}s')
            )
            
            if session_time > 1.0 or pageview_time > 1.0:
                self.stdout.write(
                    self.style.WARNING('⚠ Queries lentas detectadas')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro no teste de performance: {e}')
            )

        self.stdout.write(
            self.style.SUCCESS('\n=== Teste concluído ===')
        )
        
        if verbose:
            self.stdout.write(
                self.style.SUCCESS('\nPara mais informações, verifique os logs do sistema.')
            ) 