# Integração Stripe - Documentação Completa

## Visão Geral

Este documento contém todas as informações necessárias para configurar e manter a integração com o Stripe no sistema HOZ TECH.

## Configuração de Variáveis de Ambiente

### Desenvolvimento
```env
# Chaves de Teste do Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Produção
```env
# Chaves de Produção do Stripe
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Configurações de Ambiente
ENVIRONMENT=production
DEBUG=False
```

## Configuração do Webhook

### URL do Webhook
- **Desenvolvimento**: `http://localhost:8000/webhook/stripe/`
- **Produção**: `https://hoztech.com.br/webhook/stripe/`

### Eventos Configurados
- `checkout.session.completed`
- `invoice.payment_succeeded`
- `payment_intent.succeeded`
- `payment_intent.payment_failed`

### Configuração no Dashboard Stripe
1. Acesse o Dashboard do Stripe
2. Vá para "Developers" > "Webhooks"
3. Clique em "Add endpoint"
4. Adicione a URL do webhook
5. Selecione os eventos listados acima
6. Copie o "Signing secret" para a variável `STRIPE_WEBHOOK_SECRET`

## Implementação no Código

### Views (core/views.py)
```python
# Função para criar sessão de checkout
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Implementação da sessão de checkout

# Webhook handler
def stripe_webhook(request):
    # Processamento dos webhooks do Stripe
```

### Templates
- `produto_teste.html`: Página do produto de teste (R$ 1,00)
- `services.html`: Página de serviços com integração Stripe
- `base.html`: Template base com scripts do Stripe

### URLs (core/urls.py)
```python
path('produto-teste/', views.produto_teste, name='produto_teste'),
path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
```

## Produtos Configurados

### Produto de Teste
- **Valor**: R$ 1,00
- **Descrição**: Produto para testes de integração
- **Status**: Funcional em desenvolvimento

### Serviços Principais
1. **Consultoria Estratégica**: R$ 150,00
2. **Portfólio Profissional**: R$ 249,90
3. **Landing Page**: R$ 379,90
4. **Site Institucional**: R$ 649,90
5. **Site Empresarial**: R$ 847,00
6. **Loja Virtual**: R$ 1.297,00

## Segurança

### Validação de Webhook
- Verificação de assinatura usando `STRIPE_WEBHOOK_SECRET`
- Proteção CSRF configurada
- Validação de origem das requisições

### Configurações de Produção
- SSL obrigatório (`SECURE_SSL_REDIRECT=True`)
- Cookies seguros (`SESSION_COOKIE_SECURE=True`)
- CSRF cookies seguros (`CSRF_COOKIE_SECURE=True`)

## Testes

### Cartões de Teste
- **Sucesso**: 4242 4242 4242 4242
- **Falha**: 4000 0000 0000 0002
- **3D Secure**: 4000 0000 0000 3220

### Teste Local de Webhook
```bash
# Usando Stripe CLI
stripe listen --forward-to localhost:8000/webhook/stripe/

# Usando script Python
python test_webhook_simple.py
```

## Monitoramento

### Logs
- Transações são logadas no sistema
- Webhooks são registrados para auditoria
- Erros são capturados e reportados

### Dashboard Stripe
- Monitoramento de transações em tempo real
- Relatórios de vendas e análises
- Gestão de disputas e reembolsos

## Solução de Problemas

### Erros Comuns
1. **Webhook não recebido**: Verificar URL e configuração
2. **Pagamento falha**: Verificar chaves de API
3. **CSRF Error**: Verificar configurações de segurança

### Contatos de Suporte
- **Stripe Support**: https://support.stripe.com
- **Documentação**: https://stripe.com/docs

## Migração para Produção

### Checklist
- [ ] Obter chaves de produção do Stripe
- [ ] Configurar webhook de produção
- [ ] Atualizar variáveis de ambiente
- [ ] Testar com valores baixos
- [ ] Monitorar primeiras transações

### Backup e Rollback
- Manter chaves de teste para desenvolvimento
- Documentar configurações anteriores
- Plano de rollback em caso de problemas

---

**Última atualização**: $(date)
**Versão**: 1.0
**Responsável**: Equipe HOZ TECH