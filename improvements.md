# Melhorias Sugeridas

## 1. Otimizações de Performance

### Modelos
```python
# core/models.py

class Session(models.Model):
    # Adicionar índices
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['last_activity']),
            models.Index(fields=['ip_address']),
        ]

class PageView(models.Model):
    # Adicionar índices
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['url']),
        ]

class SEOMetrics(models.Model):
    # Adicionar campos de auditoria
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seo_metrics_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seo_metrics_updated')
    is_active = models.BooleanField(default=True)  # Para soft delete
```

### Views
```python
# core/views.py
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Adicionar cache para views frequentemente acessadas
@cache_page(60 * 15)  # Cache por 15 minutos
def home(request):
    return render(request, 'home.html')

# Otimizar queries
class SessionListView(ListView):
    def get_queryset(self):
        return Session.objects.select_related('user').prefetch_related('page_views')
```

## 2. Segurança

### Settings
```python
# hoztechsite/settings.py

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True  # Em produção

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_FAIL_OPEN = False
```

### Middleware
```python
# core/middleware.py
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f'rate_limit_{ip}'
        
        if cache.get(key, 0) >= 100:  # 100 requests per minute
            return HttpResponseTooManyRequests()
        
        cache.incr(key, 1)
        cache.expire(key, 60)  # Reset after 1 minute
        
        return self.get_response(request)
```

## 3. Monitoramento

### Logging
```python
# hoztechsite/settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'core': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Checks
```python
# core/health_checks.py
from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse, HttpResponseServerError

def health_check(request):
    try:
        connections['default'].cursor()
        return HttpResponse("OK")
    except OperationalError:
        return HttpResponseServerError("Database unavailable")
```

## 4. Área Administrativa

### Admin
```python
# core/admin.py
from django.contrib import admin
from rangefilter.filter import DateRangeFilter

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'created_at', 'last_activity', 'is_active')
    list_filter = (
        ('created_at', DateRangeFilter),
        'is_active',
        'ip_address',
    )
    search_fields = ('ip_address', 'user_agent', 'session_key')
    actions = ['mark_inactive', 'export_selected']

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Marcar sessões como inativas"

@admin.register(SEOMetrics)
class SEOMetricsAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'page_speed_score', 'last_checked')
    list_filter = (
        ('last_checked', DateRangeFilter),
        'page_speed_score',
    )
    search_fields = ('url', 'title', 'meta_description')
    readonly_fields = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
```

## 5. Deploy e Configurações

### Render.yaml
```yaml
# Adicionar health check
services:
  - type: web
    name: django
    healthCheckPath: /health/
    healthCheckTimeout: 5s
    autoDeploy: true
    envVars:
      - key: SENTRY_DSN
        value: "seu-dsn-do-sentry"
      - key: REDIS_URL
        fromService:
          type: redis
          name: redis
          property: connectionString
```

### Requirements
```txt
# requirements.txt
django-debug-toolbar  # Para desenvolvimento
django-admin-rangefilter  # Filtros avançados no admin
sentry-sdk  # Monitoramento de erros
django-redis  # Cache com Redis
django-health-check  # Health checks
``` 