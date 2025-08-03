from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Cria dados de exemplo para testar a funcionalidade administrativa'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa todos os dados existentes antes de criar novos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('🗑️  Limpando dados existentes...')
            Cookie.objects.all().delete()
            Session.objects.all().delete()
            PageView.objects.all().delete()
            SEOMetrics.objects.all().delete()
            AnalyticsExport.objects.all().delete()
            self.stdout.write('✅ Dados limpos')

        self.stdout.write('📊 Criando dados de exemplo...')

        # Criar usuário de exemplo se não existir
        user, created = User.objects.get_or_create(
            username='admin_user',
            defaults={
                'email': 'admin@hoztech.com.br',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('✅ Usuário admin criado')

        # Criar sessões de exemplo
        sessions = []
        for i in range(50):
            session = Session.objects.create(
                session_key=f'session_key_{i}_{random.randint(1000, 9999)}',
                ip_address=f'192.168.1.{random.randint(1, 255)}',
                user_agent=f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500, 600)}.36',
                referrer=f'https://google.com/search?q=hoztech+{i}' if i % 3 == 0 else None,
                user=user if i % 5 == 0 else None,
                created_at=timezone.now() - timedelta(days=random.randint(0, 30)),
                last_activity=timezone.now() - timedelta(hours=random.randint(0, 24))
            )
            sessions.append(session)

        self.stdout.write(f'✅ {len(sessions)} sessões criadas')

        # Criar cookies de exemplo
        cookies = []
        cookie_names = ['sessionid', 'csrftoken', 'analytics_id', 'preferences', 'language']
        domains = ['.hoztech.com.br', '.www.hoztech.com.br', 'localhost']
        
        for i in range(150):
            session = random.choice(sessions)
            cookie = Cookie.objects.create(
                name=random.choice(cookie_names),
                value=f'value_{i}_{random.randint(1000, 9999)}',
                domain=random.choice(domains),
                path='/',
                secure=random.choice([True, False]),
                httponly=random.choice([True, False]),
                samesite=random.choice(['Lax', 'Strict', 'None']),
                session=session,
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            cookies.append(cookie)

        self.stdout.write(f'✅ {len(cookies)} cookies criados')

        # Criar page views de exemplo
        page_views = []
        urls = [
            '/',
            '/sobre-nos/',
            '/servicos/',
            '/contato/',
            '/privacidade/',
            '/termos/',
            '/faq/',
            '/minha-seguranca/'
        ]
        titles = [
            'HOZ TECH - Desenvolvimento Web',
            'Sobre Nós - HOZ TECH',
            'Serviços - HOZ TECH',
            'Contato - HOZ TECH',
            'Política de Privacidade - HOZ TECH',
            'Termos de Uso - HOZ TECH',
            'FAQ - HOZ TECH',
            'Minha Segurança - HOZ TECH'
        ]

        for i in range(200):
            session = random.choice(sessions)
            url_index = random.randint(0, len(urls) - 1)
            page_view = PageView.objects.create(
                session=session,
                url=urls[url_index],
                title=titles[url_index],
                time_spent=timedelta(seconds=random.randint(30, 300)),
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            page_views.append(page_view)

        self.stdout.write(f'✅ {len(page_views)} page views criados')

        # Criar métricas SEO de exemplo
        seo_metrics = []
        for i in range(10):
            metric = SEOMetrics.objects.create(
                url=f'https://www.hoztech.com.br{urls[i % len(urls)]}?v={i}',
                title=titles[i % len(titles)],
                meta_description=f'Descrição meta para {titles[i % len(titles)]} - HOZ TECH oferece soluções de desenvolvimento web.',
                h1_count=random.randint(1, 3),
                h2_count=random.randint(2, 8),
                h3_count=random.randint(3, 12),
                image_count=random.randint(2, 15),
                word_count=random.randint(200, 1500),
                internal_links=random.randint(5, 25),
                external_links=random.randint(0, 10),
                page_speed_score=random.uniform(60, 95),
                mobile_friendly_score=random.uniform(70, 100),
                created_by=user,
                last_checked=timezone.now() - timedelta(days=random.randint(0, 7))
            )
            seo_metrics.append(metric)

        self.stdout.write(f'✅ {len(seo_metrics)} métricas SEO criadas')

        # Criar exports de exemplo
        exports = []
        formats = ['csv', 'xlsx', 'json']
        for i in range(5):
            export = AnalyticsExport.objects.create(
                name=f'Export {i+1} - {timezone.now().strftime("%Y-%m-%d")}',
                format=random.choice(formats),
                date_range_start=timezone.now().date() - timedelta(days=30),
                date_range_end=timezone.now().date(),
                user=user,
                created_at=timezone.now() - timedelta(days=random.randint(0, 7))
            )
            exports.append(export)

        self.stdout.write(f'✅ {len(exports)} exports criados')

        # Estatísticas finais
        self.stdout.write('\n📊 Estatísticas dos dados criados:')
        self.stdout.write(f'Sessões: {Session.objects.count()}')
        self.stdout.write(f'Cookies: {Cookie.objects.count()}')
        self.stdout.write(f'Page Views: {PageView.objects.count()}')
        self.stdout.write(f'SEO Metrics: {SEOMetrics.objects.count()}')
        self.stdout.write(f'Analytics Exports: {AnalyticsExport.objects.count()}')

        self.stdout.write('\n✅ Dados de exemplo criados com sucesso!')
        self.stdout.write('💡 Use o comando "python manage.py test_admin_functionality" para testar a funcionalidade administrativa') 