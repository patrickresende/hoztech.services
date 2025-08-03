# Solução de Problemas - Erro de Banco de Dados

## Problema Reportado
```
Erro de banco de dados. Tente novamente em alguns instantes.
```

## Diagnóstico Rápido

### 1. Verificar Conectividade do Banco
```bash
python manage.py check_database --verbose
```

### 2. Testar Admin Simples
```bash
python manage.py test_admin_simple --verbose
```

### 3. Verificar Logs
```bash
# Em produção, verificar logs do sistema
tail -f /var/log/django.log
# ou
heroku logs --tail  # se estiver no Heroku
```

## Possíveis Causas e Soluções

### 1. Problema de Conexão PostgreSQL

#### Sintomas:
- Erro de timeout na conexão
- Erro de SSL
- Erro de autenticação

#### Soluções:

**A. Verificar DATABASE_URL**
```bash
# Verificar se a variável está correta
echo $DATABASE_URL
```

**B. Testar Conexão Manual**
```bash
# Instalar psql se necessário
psql "postgresql://hoztech_admin:ntDl0L1w2BhPEEDfnZiSznn5dpQBVLVa@dpg-d0ub6gmmcj7s739gqn10-a/hoztech"
```

**C. Verificar Configurações SSL**
```sql
SHOW ssl;
SHOW ssl_cert_file;
SHOW ssl_key_file;
```

### 2. Problema de Timeout

#### Sintomas:
- Conexões lentas
- Timeout em queries complexas

#### Soluções:

**A. Ajustar Timeouts no Settings**
```python
# Em settings.py
DATABASES = {
    'default': {
        # ... outras configurações
        'OPTIONS': {
            'connect_timeout': 30,  # Aumentar timeout
            'application_name': 'hoztech_admin',
        }
    }
}
```

**B. Verificar Timeouts do PostgreSQL**
```sql
SHOW statement_timeout;
SHOW idle_in_transaction_session_timeout;
```

### 3. Problema de Middleware

#### Sintomas:
- Erro ocorre apenas no admin
- Funciona em outras partes do sistema

#### Soluções:

**A. Desabilitar Temporariamente o Middleware**
```python
# Em settings.py, comentar temporariamente:
# 'core.admin_middleware.AdminErrorMiddleware',
# 'core.admin_middleware.AdminPerformanceMiddleware',
```

**B. Verificar Se o Middleware Está Causando o Problema**
```bash
python manage.py test_admin_simple --verbose
```

### 4. Problema de Queries Complexas

#### Sintomas:
- Erro em views específicas
- Timeout em agregações

#### Soluções:

**A. Verificar Queries Problemáticas**
```python
# Em admin_views.py, adicionar logging:
import logging
logger = logging.getLogger('core.admin')

def safe_count(queryset):
    try:
        return queryset.count()
    except Exception as e:
        logger.error(f"Erro na query: {queryset.query}")
        logger.error(f"Erro: {e}")
        return 0
```

**B. Limitar Resultados**
```python
# Já implementado nas views, mas verificar se está funcionando
cookies = safe_queryset(
    Cookie.objects.filter(is_active=True).select_related('session')[:100]
)
```

### 5. Problema de Índices

#### Sintomas:
- Queries lentas
- Timeout em ordenação

#### Soluções:

**A. Verificar Índices**
```sql
-- Verificar índices existentes
SELECT indexname, tablename 
FROM pg_indexes 
WHERE tablename IN ('core_session', 'core_cookie', 'core_pageview');
```

**B. Criar Índices Necessários**
```sql
-- Se necessário, criar índices
CREATE INDEX CONCURRENTLY idx_session_is_active ON core_session(is_active);
CREATE INDEX CONCURRENTLY idx_cookie_is_active ON core_cookie(is_active);
```

## Passos de Resolução

### Passo 1: Diagnóstico Inicial
```bash
# 1. Verificar conectividade
python manage.py check_database --verbose

# 2. Testar admin sem middlewares
python manage.py test_admin_simple --verbose

# 3. Verificar logs
tail -f logs/django.log
```

### Passo 2: Isolar o Problema
```bash
# Se o problema for no admin específico:
python manage.py shell
```

```python
# No shell do Django
from django.db import connection
from core.models import Session, Cookie

# Testar queries básicas
print(Session.objects.count())
print(Cookie.objects.count())

# Testar queries com filtro
print(Session.objects.filter(is_active=True).count())
```

### Passo 3: Aplicar Correções

**A. Se for problema de conexão:**
- Verificar DATABASE_URL
- Ajustar timeouts
- Verificar SSL

**B. Se for problema de middleware:**
- Desabilitar temporariamente
- Ajustar configurações
- Reabilitar gradualmente

**C. Se for problema de queries:**
- Otimizar queries
- Adicionar índices
- Limitar resultados

### Passo 4: Testar Correções
```bash
# 1. Testar conectividade
python manage.py check_database

# 2. Testar admin
python manage.py test_admin_simple

# 3. Testar em produção
# Acessar /core_admin/test/ no navegador
```

## Configurações Recomendadas para Produção

### 1. Settings.py
```python
# Configurações de banco otimizadas
DATABASES = {
    'default': dj_database_url.parse(
        os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}

# Configurações adicionais para PostgreSQL
if not DEBUG:
    DATABASES['default'].update({
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 30,
            'application_name': 'hoztech_admin',
        }
    })
```

### 2. Variáveis de Ambiente
```bash
# Logging
DJANGO_LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Performance
DATABASE_CONN_MAX_AGE=600
```

### 3. Middleware Order
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middlewares do admin por último
    'core.admin_middleware.AdminErrorMiddleware',
    'core.admin_middleware.AdminPerformanceMiddleware',
]
```

## Monitoramento Contínuo

### 1. Logs Importantes
- `core.admin` - Logs específicos do admin
- `django.db.backends` - Logs de banco de dados
- Performance warnings

### 2. Métricas a Monitorar
- Tempo de resposta das queries
- Número de conexões ativas
- Erros de timeout
- Uso de memória

### 3. Alertas Recomendados
- Erros de conexão > 5/min
- Queries > 10s
- Timeout de conexão
- Erros 500 no admin

## Contatos de Suporte

### 1. Logs para Análise
- Logs completos do Django
- Logs do PostgreSQL
- Logs do servidor web

### 2. Informações Úteis
- Versão do Django
- Versão do PostgreSQL
- Configurações de ambiente
- Stack trace completo

---

**Última Atualização:** $(date)  
**Versão:** 1.0  
**Status:** Ativo ✅ 