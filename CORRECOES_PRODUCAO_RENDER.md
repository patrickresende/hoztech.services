# Correções para Problemas de Produção no Render

## Problemas Identificados

Com base nos logs de erro fornecidos, foram identificados os seguintes problemas no ambiente de produção do Render:

1. **Erros 500** nas URLs `/admin/core/analyticsexport/` e `/admin/core/session/`
2. **"Error handling request"** genéricos
3. **"Internal Server Error: /admin/login/"** 
4. Problemas de configuração de ambiente entre desenvolvimento e produção

## Correções Implementadas

### 1. Configuração de Ambiente (settings.py)

#### Problema: DEBUG sempre False
**Antes:**
```python
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
```

**Correção:**
```python
# Configuração de DEBUG baseada no ambiente
if ENVIRONMENT == 'production':
    DEBUG = False
else:
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
```

#### Problema: CSRF_TRUSTED_ORIGINS vazio
**Correção:**
```python
# Garantir que CSRF_TRUSTED_ORIGINS não esteja vazio
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = DEFAULT_CSRF_TRUSTED_ORIGINS
```

### 2. Configurações de Segurança

#### Problema: Configurações de segurança conflitantes
**Correção:** Removida a duplicação de CSRF_TRUSTED_ORIGINS nas configurações de desenvolvimento.

### 3. Configurações de Arquivos Estáticos

#### Problema: WhiteNoise muito restritivo
**Correção:**
```python
if ENVIRONMENT == 'production':
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_KEEP_ONLY_HASHED_FILES = False
    WHITENOISE_MANIFEST_STRICT = False  # Não falhar se arquivo não encontrado
    WHITENOISE_AUTOREFRESH = False  # Desabilitar auto-refresh em produção
```

### 4. Configurações de Banco de Dados

#### Problema: Configurações PostgreSQL inadequadas
**Correção:**
```python
# Configurações adicionais para PostgreSQL em produção
if ENVIRONMENT == 'production':
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
        'connect_timeout': 10,
    }
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['ATOMIC_REQUESTS'] = True
```

### 5. Configurações de Logging

#### Problema: Logging inadequado para produção
**Correção:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'railway_json': {
            '()': RailwayJSONFormatter,
        },
        'simple': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'railway_json' if ENVIRONMENT == 'production' else 'simple',
            'stream': sys.stdout,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

### 6. Content Security Policy (CSP)

#### Problema: CSP muito restritivo
**Correção:**
```python
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com")
CSP_IMG_SRC = ("'self'", "data:", "https:", "blob:")
CSP_CONNECT_SRC = ("'self'", "https:")
CSP_SCRIPT_SRC_ELEM = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com")
```

### 7. Configuração do Render (render.yaml)

#### Problema: Configuração complexa e problemática
**Correção:**
- Simplificado o buildCommand removendo Nginx e Node.js
- Corrigido o startCommand para usar Gunicorn diretamente
- Adicionadas variáveis de ambiente essenciais
- Configurado WHITENOISE_MANIFEST_STRICT como false

**Antes:**
```yaml
buildCommand: |
  npm install
  npm run build
  service nginx start
  newrelic-admin run-program gunicorn hoztechsite.wsgi:application --workers 2 --threads 2 --timeout 60 --bind 127.0.0.1:8000
```

**Depois:**
```yaml
buildCommand: |
  pip install -r requirements.txt
  python manage.py collectstatic --noinput --clear
  python manage.py migrate
startCommand: |
  gunicorn hoztechsite.wsgi:application --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:$PORT --access-logfile - --error-logfile - --log-level info
```

### 8. Health Check Endpoint

#### Problema: Falta de endpoint de health check
**Correção:** Adicionado endpoint `/health/` para monitoramento do Render:

```python
def health_check(request):
    """Health check endpoint for Render"""
    try:
        # Verificar conexão com banco de dados
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Verificar se os modelos principais estão funcionando
        session_count = Session.objects.count()
        pageview_count = PageView.objects.count()
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'session_count': session_count,
            'pageview_count': pageview_count,
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)
```

## Comandos de Teste Criados

### 1. test_production_debug.py
Comando para testar configurações de produção localmente:
```bash
python manage.py test_production_debug
```

### 2. test_production_settings.py
Comando para simular ambiente de produção:
```bash
python manage.py test_production_settings
```

## Variáveis de Ambiente Críticas

### Para o Render, configurar:

```bash
ENVIRONMENT=production
DJANGO_DEBUG=false
DATABASE_URL=<postgresql_url>
CSRF_TRUSTED_ORIGINS=https://*.onrender.com,https://hoztech.com.br,https://www.hoztech.com.br
DJANGO_ALLOWED_HOSTS=.onrender.com,hoztech.com.br,www.hoztech.com.br
WHITENOISE_MANIFEST_STRICT=false
DJANGO_LOG_LEVEL=INFO
```

## Verificações Pós-Deploy

1. **Health Check:** Acessar `/health/` para verificar status
2. **Admin Login:** Testar login no `/admin/`
3. **Admin Customizado:** Testar `/core_admin/`
4. **Logs:** Verificar logs do Render para erros específicos

## Monitoramento

### Logs Importantes:
- `django.request` - Erros de requisição
- `django.security` - Problemas de segurança
- `core` - Logs da aplicação principal

### Métricas:
- Status do health check
- Contagem de sessões e pageviews
- Tempo de resposta das requisições

## Próximos Passos

1. **Deploy no Render** com as novas configurações
2. **Monitorar logs** para identificar problemas remanescentes
3. **Testar funcionalidades** críticas (admin, analytics)
4. **Configurar alertas** para problemas de saúde

## Resumo das Correções

- ✅ Configuração de ambiente corrigida
- ✅ Configurações de segurança ajustadas
- ✅ WhiteNoise configurado adequadamente
- ✅ PostgreSQL configurado para produção
- ✅ Logging melhorado
- ✅ CSP menos restritivo
- ✅ Render.yaml simplificado
- ✅ Health check implementado
- ✅ Comandos de teste criados

Essas correções devem resolver os erros 500 e problemas de configuração identificados nos logs do Render. 