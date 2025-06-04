# HOZ TECH - Documentação Técnica Detalhada

## 📑 Sumário

1. [Arquitetura do Sistema](#arquitetura-do-sistema)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Modelos de Dados](#modelos-de-dados)
4. [APIs e Endpoints](#apis-e-endpoints)
5. [Interface Administrativa](#interface-administrativa)
6. [Sistema de Analytics](#sistema-de-analytics)
7. [Módulo SEO](#módulo-seo)
8. [Segurança](#segurança)
9. [Performance](#performance)
10. [Deploy e DevOps](#deploy-e-devops)
11. [Testes](#testes)
12. [Manutenção](#manutenção)

## 🏗️ Arquitetura do Sistema

### Visão Geral
O HOZ TECH é construído em uma arquitetura de três camadas:
1. **Frontend**: Interface administrativa Django + Templates Bootstrap
2. **Backend**: Django + Django REST Framework
3. **Persistência**: PostgreSQL + Redis (cache)

### Stack Tecnológico
- **Backend**: Python 3.11+, Django 4.2+
- **Frontend**: Bootstrap 5, JavaScript ES6+
- **Database**: PostgreSQL 14+
- **Cache**: Redis 6+
- **Web Server**: Gunicorn + Nginx
- **Deploy**: Render (PaaS)

### Componentes Principais
```
[Cliente Web] → [Nginx] → [Gunicorn] → [Django App] → [PostgreSQL/Redis]
```

## 📁 Estrutura do Projeto

### Organização de Diretórios
```
hoztechsite/
├── core/                    # Aplicação principal
│   ├── management/         # Comandos personalizados
│   │   └── commands/      
│   │       ├── backup_data.py
│   │       └── cleanup_data.py
│   ├── migrations/        # Migrações do banco de dados
│   ├── static/           # Arquivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/        # Templates HTML
│   │   ├── admin/       # Templates admin customizados
│   │   ├── analytics/   # Templates de analytics
│   │   └── seo/         # Templates de SEO
│   ├── models.py        # Modelos de dados
│   ├── views.py         # Views e lógica
│   ├── urls.py          # Roteamento URL
│   ├── admin.py         # Customização do admin
│   ├── forms.py         # Formulários
│   └── utils.py         # Utilitários
├── hoztechsite/         # Configuração do projeto
│   ├── settings/
│   │   ├── base.py     # Configurações base
│   │   ├── dev.py      # Configurações de desenvolvimento
│   │   └── prod.py     # Configurações de produção
│   ├── urls.py         # URLs do projeto
│   └── wsgi.py         # Configuração WSGI
├── static/             # Arquivos estáticos coletados
├── media/             # Uploads de usuários
├── backups/           # Backups de dados
├── tests/             # Testes
├── requirements/
│   ├── base.txt      # Dependências base
│   ├── dev.txt       # Dependências de desenvolvimento
│   └── prod.txt      # Dependências de produção
├── manage.py
├── render.yaml       # Configuração do Render
└── README.md
```

## 📊 Modelos de Dados

### Session
```python
class Session(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['last_activity']),
        ]
```

### Cookie
```python
class Cookie(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.TextField()
    domain = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    expires = models.DateTimeField(null=True, blank=True)
    secure = models.BooleanField(default=False)
    httponly = models.BooleanField(default=False)
    samesite = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'domain']),
            models.Index(fields=['created_at']),
        ]
```

### PageView
```python
class PageView(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=255)
    time_spent = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['created_at']),
        ]
```

### SEOMetrics
```python
class SEOMetrics(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    meta_description = models.TextField()
    h1_count = models.IntegerField()
    h2_count = models.IntegerField()
    h3_count = models.IntegerField()
    image_count = models.IntegerField()
    word_count = models.IntegerField()
    internal_links = models.IntegerField()
    external_links = models.IntegerField()
    last_checked = models.DateTimeField()
    page_speed_score = models.FloatField()
    mobile_friendly_score = models.FloatField()
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['last_checked']),
            models.Index(fields=['page_speed_score']),
        ]
```

### AnalyticsExport
```python
class AnalyticsExport(models.Model):
    name = models.CharField(max_length=255)
    format = models.CharField(max_length=10)
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='exports/')
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]
```

## 🔌 APIs e Endpoints

### Analytics API

#### Sessões
```python
# GET /api/v1/sessions/
{
    "session_key": "abc123",
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0...",
    "referrer": "https://google.com",
    "created_at": "2024-03-20T10:00:00Z",
    "last_activity": "2024-03-20T10:30:00Z"
}
```

#### Visualizações de Página
```python
# GET /api/v1/pageviews/
{
    "url": "https://hoztech.com/about",
    "title": "Sobre Nós",
    "time_spent": "00:05:30",
    "created_at": "2024-03-20T10:15:00Z"
}
```

#### Métricas SEO
```python
# GET /api/v1/seo-metrics/
{
    "url": "https://hoztech.com/products",
    "title": "Produtos",
    "meta_description": "...",
    "h1_count": 1,
    "page_speed_score": 95.5
}
```

## 🎯 Interface Administrativa

### Customização do Admin
```python
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'ip_address', 'created_at', 'last_activity']
    list_filter = ['created_at', 'last_activity', 'is_active']
    search_fields = ['session_key', 'ip_address']
    readonly_fields = ['created_at', 'last_activity']

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'title', 'session', 'time_spent', 'created_at']
    list_filter = ['created_at', 'is_active']
    search_fields = ['url', 'title']
    readonly_fields = ['created_at']
```

### Templates Personalizados
```html
{% extends "admin/base_site.html" %}

{% block content %}
<div class="dashboard">
    <div class="metrics-summary">
        <h2>Métricas Gerais</h2>
        <div class="card-deck">
            <div class="card">
                <div class="card-body">
                    <h5>Sessões Ativas</h5>
                    <p>{{ active_sessions_count }}</p>
                </div>
            </div>
            <!-- Mais cards de métricas -->
        </div>
    </div>
</div>
{% endblock %}
```

## 📊 Sistema de Analytics

### Rastreamento de Sessões
- Identificação única por session_key
- Detecção de IP e User Agent
- Tracking de referrer
- Monitoramento de atividade

### Rastreamento de Páginas
- URL e título da página
- Tempo de permanência
- Scroll depth
- Interações do usuário

### Cookies
- Gestão completa de cookies
- Conformidade com LGPD
- Políticas de privacidade
- Preferências do usuário

### Exportação de Dados
- Múltiplos formatos (CSV, Excel, JSON)
- Filtros personalizados
- Agendamento de exports
- Armazenamento seguro

## 🔍 Módulo SEO

### Análise de Páginas
- Verificação de meta tags
- Análise de headings
- Contagem de palavras
- Links internos/externos

### Performance
- Page Speed Insights
- Mobile-friendly test
- Core Web Vitals
- Otimização de imagens

### Monitoramento
- Verificações periódicas
- Alertas de problemas
- Recomendações de melhorias
- Histórico de alterações

## 🔒 Segurança

### Proteção de Dados
- Criptografia em trânsito (HTTPS)
- Dados sensíveis criptografados
- Backups seguros
- Política de retenção

### Autenticação e Autorização
- Login seguro
- Controle de acesso por função
- Sessões seguras
- Tokens JWT

### Prevenção de Ataques
- CSRF Protection
- XSS Prevention
- SQL Injection Protection
- Rate Limiting

## ⚡ Performance

### Otimizações
- Caching com Redis
- Compressão Gzip
- Lazy loading
- Minificação de assets

### Índices de Banco
- Índices otimizados
- Queries eficientes
- Connection pooling
- Query caching

### Monitoramento
- APM (Application Performance Monitoring)
- Métricas de servidor
- Logs de performance
- Alertas automáticos

## 🚀 Deploy e DevOps

### Configuração do Render
```yaml
# render.yaml
services:
  - type: web
    name: hoztech
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn hoztechsite.wsgi:application"
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: hoztechsite.settings.prod
      - key: DATABASE_URL
        fromDatabase:
          name: hoztech-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          name: hoztech-redis
          type: redis
          property: connectionString
```

### Pipeline de Deploy
1. Backup automático
2. Testes automatizados
3. Build e collect static
4. Deploy com zero downtime

### Monitoramento
- Logs centralizados
- Métricas de sistema
- Alertas de incidentes
- Dashboards operacionais

## 🧪 Testes

### Testes Unitários
```python
class SessionTests(TestCase):
    def setUp(self):
        self.session = Session.objects.create(
            session_key="test123",
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0"
        )

    def test_session_creation(self):
        self.assertEqual(self.session.is_active, True)
        self.assertIsNotNone(self.session.created_at)
```

### Testes de Integração
```python
class AnalyticsAPITests(APITestCase):
    def test_pageview_creation(self):
        data = {
            "url": "https://test.com",
            "title": "Test Page",
            "time_spent": "00:05:00"
        }
        response = self.client.post('/api/v1/pageviews/', data)
        self.assertEqual(response.status_code, 201)
```

### Testes de Performance
- Load testing com Locust
- Stress testing
- Benchmark de APIs
- Profiling de código

## 🔧 Manutenção

### Backup de Dados
```python
# Comando de backup
python manage.py backup_data --action backup

# Restauração
python manage.py backup_data --action restore --file backup_20240320.json
```

### Limpeza de Dados
```python
# Limpeza automática
python manage.py cleanup_data --days 90
```

### Monitoramento
- Verificação de integridade
- Análise de logs
- Métricas de sistema
- Alertas automáticos

### Atualizações
- Dependências atualizadas
- Patches de segurança
- Migrações de banco
- Documentação atualizada

## 📚 Recursos Adicionais

### Documentação API
- Swagger/OpenAPI
- Postman Collection
- Exemplos de código
- Guias de integração

### Guias de Desenvolvimento
- Setup do ambiente
- Padrões de código
- Fluxo de trabalho
- Best practices

### Troubleshooting
- Logs comuns
- Soluções conhecidas
- Debug guide
- FAQ

## 🤝 Suporte e Contato

### Canais de Suporte
- Email: suporte@hoztech.com
- Documentação: docs.hoztech.com
- GitHub Issues
- Discord Community

### SLA
- Tempo de resposta: 4h
- Resolução crítica: 24h
- Uptime: 99.9%
- Backup: Diário 