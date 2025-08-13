"""
Arquivo de configuração rápida para o webhook do Stripe
Este arquivo contém as variáveis de ambiente necessárias e instruções de configuração
"""

# === CONFIGURAÇÃO DO WEBHOOK STRIPE ===

# 1. Adicione estas variáveis ao seu arquivo .env:
"""
# Chave secreta do Stripe (obtida no Dashboard do Stripe)
STRIPE_SECRET_KEY=sk_test_sua_chave_aqui

# Segredo do webhook (obtido no Dashboard do Stripe > Webhooks)
STRIPE_WEBHOOK_SECRET=whsec_seu_segredo_aqui
"""

# 2. Configure o webhook no Dashboard do Stripe:
#    - Acesse: https://dashboard.stripe.com/webhooks
#    - Clique em "Add endpoint"
#    - URL do endpoint: https://seudominio.com/webhook/stripe/
#    - Selecione os eventos:
#      * checkout.session.completed
#      * checkout.session.async_payment_succeeded
#      * checkout.session.expired
#      * invoice.payment_succeeded
#      * invoice.payment_failed

# 3. Teste o webhook:
#    - Execute: python test_webhook_simple.py
#    - Ou use o Stripe CLI: stripe listen --forward-to localhost:8000/webhook/stripe/

# === CÓDIGO DO WEBHOOK ===
# O código do webhook já está implementado em:
# - core/views.py (função stripe_webhook)
# - core/urls.py (path 'webhook/stripe/')

# === ESTRUTURA DO CÓDIGO ===
"""
Localização dos arquivos:

1. Endpoint do webhook:
   - Arquivo: core/views.py
   - Função: stripe_webhook()
   - URL: /webhook/stripe/

2. Processamento de eventos:
   - checkout.session.completed: Pagamento bem-sucedido
   - checkout.session.async_payment_succeeded: Pagamento assíncrono (boleto/Pix)
   - checkout.session.expired: Sessão expirada
   - invoice.payment_succeeded: Assinatura renovada
   - invoice.payment_failed: Falha no pagamento

3. Testes:
   - test_webhook_simple.py: Teste simples local
   - Stripe CLI: Testes avançados
"""

# === EXEMPLO DE INTEGRAÇÃO COM BANCO DE DADOS ===
"""
# Para adicionar integração com banco de dados, modifique a função stripe_webhook:

# Exemplo de processamento:
if event_type == 'checkout.session.completed':
    session = event['data']['object']
    
    # Criar pedido no banco
    from .models import Order
    order = Order.objects.create(
        stripe_session_id=session['id'],
        customer_email=session['customer_details']['email'],
        amount_total=session['amount_total'] / 100,  # Converter centavos
        product_id=session['metadata']['product_id'],
        status='completed'
    )
    
    # Enviar email de confirmação
    send_mail(
        'Pedido Confirmado - HOZ TECH',
        f'Obrigado pelo seu pedido! ID: {order.id}',
        settings.DEFAULT_FROM_EMAIL,
        [order.customer_email]
    )
"""

# === VERIFICAÇÃO DE CONFIGURAÇÃO ===
def check_webhook_config():
    """Verifica se as configurações do webhook estão corretas"""
    import os
    from django.conf import settings
    
    print("🔍 Verificando configuração do webhook...")
    
    # Verificar variáveis de ambiente
    stripe_key = getattr(settings, 'STRIPE_SECRET_KEY', None)
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
    
    if stripe_key and stripe_key.startswith('sk_'):
        print("✅ STRIPE_SECRET_KEY configurada")
    else:
        print("❌ STRIPE_SECRET_KEY não configurada ou inválida")
    
    if webhook_secret and webhook_secret.startswith('whsec_'):
        print("✅ STRIPE_WEBHOOK_SECRET configurada")
    else:
        print("❌ STRIPE_WEBHOOK_SECRET não configurada ou inválida")
    
    print("\n📋 URL do webhook: http://127.0.0.1:8000/webhook/stripe/")
    print("📋 Método HTTP aceito: POST")
    print("📋 Content-Type esperado: application/json")
    print("📋 Headers necessários: Stripe-Signature")

if __name__ == "__main__":
    check_webhook_config()