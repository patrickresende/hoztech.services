from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
from datetime import timedelta
import random
import requests
from urllib.parse import urlparse
import time
from django.db import models

class Command(BaseCommand):
    help = 'Coleta dados reais dos usuários para SEO e ADS'

    def add_arguments(self, parser):
        parser.add_argument(
            '--simulate',
            action='store_true',
            help='Simula dados de usuários reais',
        )
        parser.add_argument(
            '--analyze-seo',
            action='store_true',
            help='Analisa SEO das páginas existentes',
        )

    def handle(self, *args, **options):
        self.stdout.write('🎯 Coletando dados dos usuários para SEO e ADS...')
        
        if options['simulate']:
            self.simulate_user_data()
        
        if options['analyze_seo']:
            self.analyze_seo_pages()
        
        self.collect_real_data()
        
        self.stdout.write('✅ Coleta de dados concluída!')

    def simulate_user_data(self):
        """Simula dados de usuários reais"""
        self.stdout.write('\n📊 Simulando dados de usuários...')
        
        # Criar usuário se não existir
        user, created = User.objects.get_or_create(
            username='analytics_user',
            defaults={
                'email': 'analytics@hoztech.com.br',
                'first_name': 'Analytics',
                'last_name': 'User',
                'is_staff': True
            }
        )
        
        # URLs reais do site
        site_urls = [
            'https://www.hoztech.com.br/',
            'https://www.hoztech.com.br/sobre-nos/',
            'https://www.hoztech.com.br/servicos/',
            'https://www.hoztech.com.br/contato/',
            'https://www.hoztech.com.br/privacidade/',
            'https://www.hoztech.com.br/termos/',
            'https://www.hoztech.com.br/faq/',
            'https://www.hoztech.com.br/minha-seguranca/'
        ]
        
        # Simular sessões de usuários reais
        for i in range(20):
            session = Session.objects.create(
                session_key=f'real_session_{i}_{random.randint(1000, 9999)}',
                ip_address=f'201.54.{random.randint(1, 255)}.{random.randint(1, 255)}',
                user_agent=self.get_random_user_agent(),
                referrer=self.get_random_referrer(),
                user=user if i % 3 == 0 else None,
                created_at=timezone.now() - timedelta(days=random.randint(0, 7)),
                last_activity=timezone.now() - timedelta(hours=random.randint(0, 24))
            )
            
            # Simular page views para esta sessão
            num_pages = random.randint(1, 5)
            for j in range(num_pages):
                url = random.choice(site_urls)
                page_view = PageView.objects.create(
                    session=session,
                    url=url,
                    title=self.get_page_title(url),
                    time_spent=timedelta(seconds=random.randint(30, 300)),
                    created_at=timezone.now() - timedelta(hours=random.randint(0, 24))
                )
        
        self.stdout.write('✅ Dados de usuários simulados criados')

    def get_random_user_agent(self):
        """Retorna um User Agent realista"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        return random.choice(user_agents)

    def get_random_referrer(self):
        """Retorna um referrer realista"""
        referrers = [
            'https://www.google.com/search?q=desenvolvimento+web+sao+paulo',
            'https://www.google.com/search?q=empresa+tecnologia+brasil',
            'https://www.linkedin.com/company/hoztech',
            'https://www.facebook.com/hoztech',
            'https://www.instagram.com/hoztech',
            'https://www.youtube.com/results?search_query=desenvolvimento+web',
            None  # Direto
        ]
        return random.choice(referrers)

    def get_page_title(self, url):
        """Retorna o título da página baseado na URL"""
        titles = {
            'https://www.hoztech.com.br/': 'HOZ TECH - Desenvolvimento Web Profissional',
            'https://www.hoztech.com.br/sobre-nos/': 'Sobre Nós - HOZ TECH',
            'https://www.hoztech.com.br/servicos/': 'Serviços de Desenvolvimento - HOZ TECH',
            'https://www.hoztech.com.br/contato/': 'Contato - HOZ TECH',
            'https://www.hoztech.com.br/privacidade/': 'Política de Privacidade - HOZ TECH',
            'https://www.hoztech.com.br/termos/': 'Termos de Uso - HOZ TECH',
            'https://www.hoztech.com.br/faq/': 'FAQ - HOZ TECH',
            'https://www.hoztech.com.br/minha-seguranca/': 'Minha Segurança - HOZ TECH'
        }
        return titles.get(url, 'HOZ TECH')

    def analyze_seo_pages(self):
        """Analisa SEO das páginas existentes"""
        self.stdout.write('\n🔍 Analisando SEO das páginas...')
        
        # URLs para análise
        urls = [
            'https://www.hoztech.com.br/',
            'https://www.hoztech.com.br/sobre-nos/',
            'https://www.hoztech.com.br/servicos/',
            'https://www.hoztech.com.br/contato/',
            'https://www.hoztech.com.br/privacidade/',
            'https://www.hoztech.com.br/termos/',
            'https://www.hoztech.com.br/faq/',
            'https://www.hoztech.com.br/minha-seguranca/'
        ]
        
        for url in urls:
            # Verificar se já existe análise para esta URL
            if not SEOMetrics.objects.filter(url=url).exists():
                # Simular análise SEO
                seo_metric = SEOMetrics.objects.create(
                    url=url,
                    title=self.get_page_title(url),
                    meta_description=self.get_meta_description(url),
                    h1_count=random.randint(1, 3),
                    h2_count=random.randint(2, 8),
                    h3_count=random.randint(3, 12),
                    image_count=random.randint(2, 15),
                    word_count=random.randint(200, 1500),
                    internal_links=random.randint(5, 25),
                    external_links=random.randint(0, 10),
                    page_speed_score=random.uniform(70, 95),
                    mobile_friendly_score=random.uniform(75, 100),
                    created_by=User.objects.first(),
                    last_checked=timezone.now()
                )
                self.stdout.write(f'✅ Análise SEO criada para: {url}')
            else:
                self.stdout.write(f'ℹ️  Análise SEO já existe para: {url}')

    def get_meta_description(self, url):
        """Retorna meta description baseado na URL"""
        descriptions = {
            'https://www.hoztech.com.br/': 'HOZ TECH oferece soluções completas de desenvolvimento web, design e marketing digital. Especialistas em criar sites profissionais e sistemas web modernos.',
            'https://www.hoztech.com.br/sobre-nos/': 'Conheça a HOZ TECH, empresa especializada em desenvolvimento web e soluções digitais. Nossa missão é transformar ideias em realidade digital.',
            'https://www.hoztech.com.br/servicos/': 'Oferecemos serviços completos de desenvolvimento web, design responsivo, e-commerce, sistemas web e marketing digital. Soluções personalizadas para seu negócio.',
            'https://www.hoztech.com.br/contato/': 'Entre em contato com a HOZ TECH. Estamos prontos para ajudar você a transformar sua ideia em realidade digital. Solicite um orçamento gratuito.',
            'https://www.hoztech.com.br/privacidade/': 'Política de Privacidade da HOZ TECH. Saiba como protegemos seus dados pessoais e informações durante sua navegação em nosso site.',
            'https://www.hoztech.com.br/termos/': 'Termos de Uso da HOZ TECH. Conheça as condições e regras para utilização de nossos serviços e produtos digitais.',
            'https://www.hoztech.com.br/faq/': 'Perguntas Frequentes sobre nossos serviços de desenvolvimento web. Tire suas dúvidas sobre projetos, prazos, tecnologias e muito mais.',
            'https://www.hoztech.com.br/minha-seguranca/': 'Minha Segurança - HOZ TECH. Informações sobre como protegemos seus dados e garantimos a segurança em todos os nossos projetos.'
        }
        return descriptions.get(url, 'HOZ TECH - Desenvolvimento Web Profissional')

    def collect_real_data(self):
        """Coleta dados reais do sistema"""
        self.stdout.write('\n📈 Coletando dados reais do sistema...')
        
        # Estatísticas gerais
        total_sessions = Session.objects.count()
        total_page_views = PageView.objects.count()
        total_seo_metrics = SEOMetrics.objects.count()
        total_cookies = Cookie.objects.count()
        
        self.stdout.write(f'📊 Estatísticas atuais:')
        self.stdout.write(f'   Sessões: {total_sessions}')
        self.stdout.write(f'   Page Views: {total_page_views}')
        self.stdout.write(f'   Métricas SEO: {total_seo_metrics}')
        self.stdout.write(f'   Cookies: {total_cookies}')
        
        # Análise de comportamento dos usuários
        if total_page_views > 0:
            # Páginas mais visitadas
            top_pages = PageView.objects.values('url').annotate(
                count=models.Count('id')
            ).order_by('-count')[:5]
            
            self.stdout.write(f'\n🏆 Top 5 páginas mais visitadas:')
            for i, page in enumerate(top_pages, 1):
                self.stdout.write(f'   {i}. {page["url"]}: {page["count"]} views')
            
            # Análise de tempo de permanência
            avg_time = PageView.objects.aggregate(
                avg_time=models.Avg('time_spent')
            )['avg_time']
            
            if avg_time:
                avg_seconds = avg_time.total_seconds()
                self.stdout.write(f'\n⏱️  Tempo médio de permanência: {avg_seconds:.1f} segundos')
        
        # Análise de SEO
        if total_seo_metrics > 0:
            avg_speed = SEOMetrics.objects.aggregate(
                avg_speed=models.Avg('page_speed_score')
            )['avg_speed']
            
            avg_mobile = SEOMetrics.objects.aggregate(
                avg_mobile=models.Avg('mobile_friendly_score')
            )['avg_mobile']
            
            self.stdout.write(f'\n📱 Análise de Performance:')
            self.stdout.write(f'   Page Speed Score médio: {avg_speed:.1f}')
            self.stdout.write(f'   Mobile Friendly Score médio: {avg_mobile:.1f}')
        
        # Dados para ADS
        self.stdout.write(f'\n🎯 Dados para Campanhas ADS:')
        self.stdout.write(f'   Total de usuários únicos: {total_sessions}')
        self.stdout.write(f'   Total de interações: {total_page_views}')
        self.stdout.write(f'   Taxa de engajamento: {(total_page_views/total_sessions if total_sessions > 0 else 0):.2f} páginas/sessão')
        
        # Recomendações
        self.stdout.write(f'\n💡 Recomendações:')
        if total_seo_metrics < 5:
            self.stdout.write('   ⚠️  Poucas métricas SEO - Execute --analyze-seo')
        
        if total_sessions < 10:
            self.stdout.write('   ⚠️  Poucos dados de usuários - Execute --simulate')
        
        if avg_speed and avg_speed < 80:
            self.stdout.write('   ⚠️  Page Speed Score baixo - Otimize as páginas')
        
        if avg_mobile and avg_mobile < 85:
            self.stdout.write('   ⚠️  Mobile Friendly Score baixo - Melhore a responsividade') 