import os
import django
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
django.setup()

# Importar modelos após configurar o Django
from core.models import Cookie, Session, PageView, SEOMetrics
from django.utils import timezone

fake = Faker('pt_BR')  # Usando localização brasileira

def generate_sessions(num_sessions=100):
    print("Gerando sessões...")
    browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']
    referrers = [
        'https://google.com.br',
        'https://facebook.com',
        'https://instagram.com',
        'https://linkedin.com',
        'https://github.com',
        None
    ]
    
    sessions = []
    for _ in range(num_sessions):
        start_time = timezone.now() - timedelta(days=random.randint(0, 30))
        session = Session.objects.create(
            session_key=str(uuid.uuid4()),
            ip_address=fake.ipv4(),
            user_agent=f"{random.choice(browsers)}/{fake.numerify('#.#.###.#')} ({fake.user_agent()})",
            referrer=random.choice(referrers),
            created_at=start_time,
            last_activity=start_time + timedelta(minutes=random.randint(1, 120)),
            is_active=random.choice([True, False])
        )
        sessions.append(session)
    return sessions

def generate_cookies(sessions, num_cookies=50):
    print("Gerando cookies...")
    domains = ['hoztech.com.br', 'app.hoztech.com.br', 'blog.hoztech.com.br', 'localhost:8000']
    cookie_names = ['sessionid', 'csrftoken', 'user_preferences', 'cart_id', 'analytics_id']
    
    if not sessions:
        print("Erro: Nenhuma sessão encontrada. Gere sessões antes de cookies.")
        return
    
    for _ in range(num_cookies):
        Cookie.objects.create(
            name=random.choice(cookie_names),
            domain=random.choice(domains),
            value=fake.uuid4(),
            expires=timezone.now() + timedelta(days=random.randint(1, 365)),
            secure=random.choice([True, False]),
            httponly=random.choice([True, False]),
            samesite=random.choice(['Strict', 'Lax', 'None']),
            session=random.choice(sessions),
            created_at=timezone.now() - timedelta(days=random.randint(0, 30))
        )

def generate_page_views(sessions, num_views=200):
    print("Gerando visualizações de página...")
    if not sessions:
        print("Erro: Nenhuma sessão encontrada. Gere sessões antes das visualizações.")
        return

    urls = [
        '/',
        '/sobre',
        '/contato',
        '/produtos',
        '/servicos',
        '/blog',
        '/blog/tecnologia',
        '/blog/inovacao',
        '/orcamento',
        '/faq'
    ]
    
    titles = {
        '/': 'HOZ TECH - Soluções em Tecnologia',
        '/sobre': 'Sobre Nós | HOZ TECH',
        '/contato': 'Entre em Contato | HOZ TECH',
        '/produtos': 'Nossos Produtos | HOZ TECH',
        '/servicos': 'Serviços de TI | HOZ TECH',
        '/blog': 'Blog de Tecnologia | HOZ TECH',
        '/blog/tecnologia': 'Tendências em Tecnologia | HOZ TECH',
        '/blog/inovacao': 'Inovação Digital | HOZ TECH',
        '/orcamento': 'Solicite um Orçamento | HOZ TECH',
        '/faq': 'Perguntas Frequentes | HOZ TECH'
    }
    
    for _ in range(num_views):
        url = random.choice(urls)
        session = random.choice(sessions)
        PageView.objects.create(
            url=url,
            title=titles.get(url, fake.sentence()),
            time_spent=timedelta(seconds=random.randint(10, 3600)),
            session=session,
            created_at=timezone.now() - timedelta(days=random.randint(0, 30))
        )

def generate_seo_metrics(num_metrics=30):
    print("Gerando métricas SEO...")
    urls = [
        '/',
        '/sobre',
        '/contato',
        '/produtos',
        '/servicos',
        '/blog',
        '/blog/tecnologia',
        '/blog/inovacao',
        '/orcamento',
        '/faq'
    ]
    
    meta_descriptions = {
        '/': 'HOZ TECH - Soluções inovadoras em tecnologia para sua empresa. Desenvolvimento web, aplicativos e consultoria em TI.',
        '/sobre': 'Conheça a HOZ TECH, empresa especializada em soluções tecnológicas personalizadas para o seu negócio.',
        '/contato': 'Entre em contato com a HOZ TECH. Estamos prontos para ajudar com suas necessidades em tecnologia.',
        '/produtos': 'Produtos e soluções tecnológicas da HOZ TECH. Software, hardware e serviços para sua empresa.',
        '/servicos': 'Serviços de TI da HOZ TECH. Desenvolvimento, consultoria, suporte e manutenção.',
        '/blog': 'Blog da HOZ TECH - Artigos e notícias sobre tecnologia, inovação e tendências do mercado.',
    }
    
    for url in urls:
        SEOMetrics.objects.create(
            url=url,
            title=f"{url.replace('/', ' ').strip().title()} | HOZ TECH" if url != '/' else 'HOZ TECH - Soluções em Tecnologia',
            meta_description=meta_descriptions.get(url, fake.paragraph()),
            h1_count=random.randint(1, 3),
            h2_count=random.randint(2, 8),
            h3_count=random.randint(3, 12),
            image_count=random.randint(1, 15),
            word_count=random.randint(300, 2000),
            internal_links=random.randint(5, 20),
            external_links=random.randint(0, 10),
            page_speed_score=random.randint(70, 100),
            mobile_friendly_score=random.randint(70, 100),
            last_checked=timezone.now() - timedelta(days=random.randint(0, 30))
        )

def main():
    print("Iniciando geração de dados de teste...")
    
    # Limpar dados existentes
    print("Limpando dados existentes...")
    Cookie.objects.all().delete()
    Session.objects.all().delete()
    PageView.objects.all().delete()
    SEOMetrics.objects.all().delete()
    
    # Gerar novos dados na ordem correta
    print("\nGerando novos dados...")
    sessions = generate_sessions(100)  # Gerar sessões primeiro
    generate_cookies(sessions, 150)    # Depois cookies, associados às sessões
    generate_page_views(sessions, 200)  # Visualizações de página
    generate_seo_metrics()             # Métricas SEO
    
    print("\nGeração de dados de teste concluída!")
    print(f"- Sessões geradas: {Session.objects.count()}")
    print(f"- Cookies gerados: {Cookie.objects.count()}")
    print(f"- Visualizações de página geradas: {PageView.objects.count()}")
    print(f"- Métricas SEO geradas: {SEOMetrics.objects.count()}")

if __name__ == '__main__':
    main() 