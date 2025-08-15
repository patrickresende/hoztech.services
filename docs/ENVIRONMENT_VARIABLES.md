# Variáveis de Ambiente - HOZ TECH

## Configurações Essenciais

### Django Core
```env
# Chave secreta do Django (obrigatória)
DJANGO_SECRET_KEY=your-secret-key-here

# Modo de debug (False em produção)
DJANGO_DEBUG=False

# Ambiente de execução
ENVIRONMENT=production

# Hosts permitidos (separados por vírgula)
ALLOWED_HOSTS=hoztech.com.br,www.hoztech.com.br

# Origens confiáveis para CSRF
CSRF_TRUSTED_ORIGINS=https://hoztech.com.br,https://www.hoztech.com.br
```

### Segurança
```env
# SSL e HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Content Security Policy
CSP_DEFAULT_SRC="'self'"
CSP_SCRIPT_SRC="'self' 'unsafe-inline' js.stripe.com"
CSP_STYLE_SRC="'self' 'unsafe-inline'"
CSP_IMG_SRC="'self' data: https:"
CSP_CONNECT_SRC="'self' api.stripe.com"
```

### Stripe (Pagamentos)
```env
# Chaves de Produção
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Email (SMTP)
```env
# Configurações de Email
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_HOST_USER=contato@hoztech.com.br
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=contato@hoztech.com.br
```

### WhatsApp Business API
```env
# Tokens e IDs do WhatsApp
WHATSAPP_ACCESS_TOKEN=your-access-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
WHATSAPP_BUSINESS_ACCOUNT_ID=your-business-id
WHATSAPP_APP_SECRET=your-app-secret
WHATSAPP_VERIFY_TOKEN=your-verify-token
```

### Arquivos Estáticos e Media
```env
# Caminhos para arquivos
STATIC_ROOT=/var/www/hoztech/static
MEDIA_ROOT=/var/www/hoztech/media
STATIC_URL=/static/
MEDIA_URL=/media/
```

### Banco de Dados
```env
# PostgreSQL (Produção)
DATABASE_URL=postgresql://user:password@localhost:5432/hoztech_db

# ou configuração manual
DB_NAME=hoztech_db
DB_USER=hoztech_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### Redis (Cache e Sessões)
```env
# Redis para cache
REDIS_URL=redis://localhost:6379/0
CACHE_URL=redis://localhost:6379/1
SESSION_REDIS_URL=redis://localhost:6379/2
```

### Monitoramento
```env
# Sentry (Error Tracking)
SENTRY_DSN=your-sentry-dsn

# New Relic (Performance)
NEW_RELIC_LICENSE_KEY=your-newrelic-key
NEW_RELIC_APP_NAME=HOZ-TECH-Production
```

### Configurações Administrativas
```env
# Personalização do Admin
ADMIN_SITE_HEADER=HOZ TECH - Painel Administrativo
ADMIN_SITE_TITLE=HOZ TECH Admin
ADMIN_INDEX_TITLE=Bem-vindo ao Painel HOZ TECH
```

## Exemplo de Arquivo .env para Produção

```env
# Django Core
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
ENVIRONMENT=production
ALLOWED_HOSTS=hoztech.com.br,www.hoztech.com.br
CSRF_TRUSTED_ORIGINS=https://hoztech.com.br,https://www.hoztech.com.br

# Segurança
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_HOST_USER=contato@hoztech.com.br
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True

# WhatsApp
WHATSAPP_ACCESS_TOKEN=your-access-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
WHATSAPP_BUSINESS_ACCOUNT_ID=your-business-id
WHATSAPP_APP_SECRET=your-app-secret

# Banco de Dados
DATABASE_URL=postgresql://user:password@localhost:5432/hoztech_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Monitoramento
SENTRY_DSN=your-sentry-dsn
NEW_RELIC_LICENSE_KEY=your-newrelic-key

# Admin
ADMIN_SITE_HEADER=HOZ TECH - Painel Administrativo
```

## Segurança das Variáveis

### Boas Práticas
1. **Nunca commitar** arquivos .env no Git
2. **Usar gerenciadores** de secrets em produção
3. **Rotacionar chaves** periodicamente
4. **Limitar acesso** às variáveis sensíveis
5. **Monitorar uso** das APIs

### Backup
- Manter backup seguro das variáveis
- Documentar todas as chaves e tokens
- Ter plano de recuperação em caso de comprometimento

---

**Importante**: Este arquivo contém informações sensíveis. Mantenha-o seguro e acessível apenas à equipe autorizada.