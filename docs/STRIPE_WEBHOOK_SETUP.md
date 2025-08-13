# 🚀 Configuração do Webhook Stripe - HOZ TECH

## 📋 Visão Geral

Este documento explica como configurar e usar o endpoint de webhook do Stripe no projeto HOZ TECH para processar eventos de pagamento automaticamente.

## 🔗 Endpoint do Webhook

**URL do Webhook:** `https://seu-dominio.com/webhook/stripe/`

**Método:** POST
**Content-Type:** application/json

## ⚙️ Configuração no Stripe Dashboard

### 1. Acessar o Dashboard do Stripe
1. Acesse: https://dashboard.stripe.com/webhooks
2. Clique em "Add endpoint"

### 2. Configurar o Endpoint
- **Endpoint URL:** `https://seu-dominio.com/webhook/stripe/`
- **Version:** Use a versão mais recente da API
- **Events to send:** Selecione os eventos desejados:
  - `checkout.session.completed`
  - `checkout.session.async_payment_succeeded`
  - `checkout.session.expired`
  - `invoice.payment_succeeded`
  - `invoice.payment_failed`

### 3. Obter o Webhook Secret
Após criar o endpoint, copie o **Signing secret** (começa com `whsec_`) e adicione ao arquivo `.env`:

```bash
STRIPE_WEBHOOK_SECRET=whsec_seu_webhook_secret_aqui
```

## 🧪 Testes Locais

### Usando o Script de Teste
Execute o script de teste para verificar o webhook:

```bash
# Testar com evento padrão (checkout.session.completed)
python test_stripe_webhook.py

# Testar com evento específico
python test_stripe_webhook.py checkout.session.async_payment_succeeded
```

### Usando o Stripe CLI (Recomendado)

1. **Instalar o Stripe CLI:**
   - Windows: Baixe em https://github.com/stripe/stripe-cli/releases
   - macOS: `brew install stripe/stripe-cli/stripe`
   - Linux: `curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg && echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee /etc/apt/sources.list.d/stripe.list && sudo apt update && sudo apt install stripe`

2. **Fazer login:**
   ```bash
   stripe login
   ```

3. **Ouvir webhooks localmente:**
   ```bash
   stripe listen --forward-to localhost:8000/webhook/stripe
   ```

4. **Disparar eventos de teste:**
   ```bash
   stripe trigger checkout.session.completed
   stripe trigger invoice.payment_failed
   stripe trigger invoice.payment_succeeded
   ```

## 📊 Eventos Processados

### 1. checkout.session.completed
**Descrição:** Pagamento concluído com sucesso
**Ação:** Liberar produto, criar pedido no banco

### 2. checkout.session.async_payment_succeeded
**Descrição:** Pagamento assíncrono (boleto/Pix) concluído
**Ação:** Confirmar pagamento e liberar produto

### 3. checkout.session.expired
**Descrição:** Sessão de checkout expirou
**Ação:** Limpar carrinho ou notificar cliente

### 4. invoice.payment_succeeded
**Descrição:** Assinatura paga com sucesso
**Ação:** Renovar assinatura, atualizar status

### 5. invoice.payment_failed
**Descrição:** Falha no pagamento de assinatura
**Ação:** Notificar cliente sobre falha

## 🔐 Segurança

### Verificação de Assinatura
O webhook verifica automaticamente a assinatura de cada requisição usando o `STRIPE_WEBHOOK_SECRET`.

### CSRF Protection
O endpoint está marcado com `@csrf_exempt` pois as requisições vêm de fora do Django.

## 🛠️ Personalização

### Adicionar Novos Eventos
Para adicionar novos eventos, edite a função `stripe_webhook` em `core/views.py`:

```python
elif event_type == "novo.evento":
    # Sua lógica aqui
    print("Processando novo evento")
```

### Integração com Banco de Dados
Para salvar pedidos no banco:

```python
from .models import Pedido

# Em checkout.session.completed
Pedido.objects.create(
    stripe_session_id=session['id'],
    email=session['customer_details']['email'],
    valor=session['amount_total'] / 100,
    status='pago'
)
```

### Notificações por Email
Para enviar email após pagamento:

```python
from django.core.mail import send_mail

# Em checkout.session.completed
send_mail(
    'Pagamento Confirmado - HOZ TECH',
    f'Obrigado pelo seu pedido! ID: {session["id"]}',
    'noreply@hoztech.com.br',
    [session['customer_details']['email']],
    fail_silently=False,
)
```

## 🐛 Solução de Problemas

### Webhook não recebe eventos
1. Verifique se o `STRIPE_WEBHOOK_SECRET` está correto no `.env`
2. Confirme se a URL está acessível publicamente
3. Verifique os logs do servidor

### Assinatura inválida
1. Certifique-se de usar o webhook secret correto
2. Verifique se não há proxies ou firewalls bloqueando
3. Teste com Stripe CLI para validar

### Eventos não processados
1. Verifique os logs do servidor
2. Confirme se o evento está sendo enviado pelo Stripe
3. Teste manualmente com o script de teste

## 📞 Suporte

Para dúvidas sobre a integração:
- Documentação Stripe: https://stripe.com/docs/webhooks
- Testar webhooks: https://stripe.com/docs/webhooks/test
- Comunidade Stripe: https://stripe.com/docs/support

## 🔄 Atualização

Para atualizar o webhook:
1. Mantenha o endpoint sempre disponível
2. Teste em ambiente de desenvolvimento antes de produção
3. Monitore os logs regularmente
4. Mantenha o Stripe CLI atualizado