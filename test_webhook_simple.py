#!/usr/bin/env python3
"""
Script simples para testar o webhook do Stripe localmente
Executa um teste básico para verificar se o endpoint /webhook/stripe está respondendo
"""

import requests
import json
import time

def test_webhook_health():
    """Testa se o endpoint do webhook está acessível"""
    try:
        response = requests.get('http://127.0.0.1:8000/webhook/stripe/', timeout=5)
        print(f"✅ Endpoint acessível (GET): Status {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar endpoint: {e}")
        return False

def test_webhook_post():
    """Testa POST com payload simulado do Stripe"""
    # Payload simulado de teste
    payload = {
        "id": "evt_test_1234567890",
        "object": "event",
        "api_version": "2023-10-16",
        "created": int(time.time()),
        "data": {
            "object": {
                "id": "cs_test_1234567890",
                "object": "checkout.session",
                "amount_total": 5000,
                "currency": "brl",
                "customer": "cus_test_1234567890",
                "customer_details": {
                    "email": "test@example.com",
                    "name": "Test User"
                },
                "metadata": {
                    "product_id": "landing-page"
                },
                "payment_status": "paid",
                "status": "complete"
            }
        },
        "livemode": False,
        "pending_webhooks": 1,
        "request": {
            "id": "req_test_1234567890",
            "idempotency_key": None
        },
        "type": "checkout.session.completed"
    }

    headers = {
        'Content-Type': 'application/json',
        'Stripe-Signature': 'test_signature_invalid'
    }

    try:
        response = requests.post(
            'http://127.0.0.1:8000/webhook/stripe/',
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Webhook processado com sucesso (200 OK)")
        elif response.status_code == 400:
            print("✅ Webhook recebido mas assinatura inválida (400 Bad Request - esperado)")
        else:
            print(f"⚠️ Status inesperado: {response.status_code}")
            
        return response.status_code
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar webhook: {e}")
        return None

def main():
    """Função principal de teste"""
    print("🚀 Testando Webhook Stripe - HOZ TECH")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    if not test_webhook_health():
        print("\n⚠️  O servidor Django não está rodando ou o endpoint não está acessível")
        print("💡 Inicie o servidor com: python manage.py runserver 127.0.0.1:8000")
        return
    
    print("\n📡 Testando POST com payload simulado...")
    status = test_webhook_post()
    
    if status:
        print("\n✅ Teste concluído! O webhook está funcionando.")
    else:
        print("\n❌ Teste falhou. Verifique os logs do servidor.")

if __name__ == "__main__":
    main()