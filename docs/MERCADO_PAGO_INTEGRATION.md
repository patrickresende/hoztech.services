# Integração Mercado Pago - HOZ TECH

## Visão Geral

Documentação para implementação da integração com Mercado Pago para pagamentos à vista, parcelados e PIX na página de serviços.

## Configuração Inicial

### Variáveis de Ambiente
```env
# Mercado Pago - Desenvolvimento
MERCADO_PAGO_ACCESS_TOKEN_TEST=TEST-...
MERCADO_PAGO_PUBLIC_KEY_TEST=TEST-...

# Mercado Pago - Produção
MERCADO_PAGO_ACCESS_TOKEN=APP_USR-...
MERCADO_PAGO_PUBLIC_KEY=APP_USR-...

# Configurações gerais
MERCADO_PAGO_WEBHOOK_SECRET=your-webhook-secret
MERCADO_PAGO_NOTIFICATION_URL=https://hoztech.com.br/webhook/mercado-pago/
```

### 2. Instalação da SDK

### Opção 1: Via requirements.txt (Recomendado)
O SDK já está incluído no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Opção 2: Instalação individual
```bash
pip install mercadopago>=2.2.0
```

### Configuração no settings.py
```python
# Mercado Pago Settings
MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MERCADO_PAGO_ACCESS_TOKEN')
MERCADO_PAGO_PUBLIC_KEY = os.getenv('MERCADO_PAGO_PUBLIC_KEY')
MERCADO_PAGO_ACCESS_TOKEN_TEST = os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')
MERCADO_PAGO_PUBLIC_KEY_TEST = os.getenv('MERCADO_PAGO_PUBLIC_KEY_TEST')
MERCADO_PAGO_WEBHOOK_SECRET = os.getenv('MERCADO_PAGO_WEBHOOK_SECRET')
```

## Serviços e Preços

### Lista de Serviços Atualizada

| Serviço | Valor Original | Valor Promocional | Desconto | Parcelamento |
|---------|---------------|-------------------|----------|-------------|
| Consultoria Estratégica | R$ 297,00 | R$ 150,00 | 49% OFF | 2x sem juros |
| Portfólio Profissional | R$ 399,00 | R$ 249,90 | 37% OFF | 3x sem juros |
| Landing Page de Alta Conversão | R$ 699,00 | R$ 379,90 | 46% OFF | 4x sem juros |
| Site Institucional Premium | R$ 997,00 | R$ 649,90 | 35% OFF | 5x sem juros |
| Site Empresarial Avançado | R$ 1.497,00 | R$ 847,00 | 33% OFF | 12x |
| Loja Virtual Própria | R$ 2.197,00 | R$ 1.297,00 | 32% OFF | 12x |

## Implementação Técnica

### Views (core/views.py)
```python
import mercadopago
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def create_mercadopago_preference(request):
    """Criar preferência de pagamento no Mercado Pago"""
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    
    service_id = request.POST.get('service_id')
    service_data = get_service_data(service_id)
    
    preference_data = {
        "items": [
            {
                "title": service_data['title'],
                "quantity": 1,
                "unit_price": float(service_data['price']),
                "currency_id": "BRL"
            }
        ],
        "payment_methods": {
            "excluded_payment_types": [],
            "installments": service_data['max_installments']
        },
        "back_urls": {
            "success": request.build_absolute_uri('/pagamento/sucesso/'),
            "failure": request.build_absolute_uri('/pagamento/erro/'),
            "pending": request.build_absolute_uri('/pagamento/pendente/')
        },
        "auto_return": "approved",
        "notification_url": settings.MERCADO_PAGO_NOTIFICATION_URL
    }
    
    preference_response = sdk.preference().create(preference_data)
    
    if preference_response["status"] == 201:
        return JsonResponse({
            'preference_id': preference_response["response"]["id"],
            'init_point': preference_response["response"]["init_point"]
        })
    else:
        return JsonResponse({'error': 'Erro ao criar preferência'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def mercadopago_webhook(request):
    """Webhook para notificações do Mercado Pago"""
    try:
        # Processar notificação
        notification_data = json.loads(request.body)
        
        # Validar e processar pagamento
        if notification_data.get('type') == 'payment':
            payment_id = notification_data.get('data', {}).get('id')
            process_payment_notification(payment_id)
        
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_service_data(service_id):
    """Retorna dados do serviço baseado no ID"""
    services = {
        'consultoria': {
            'title': 'Consultoria Estratégica',
            'price': 150.00,
            'max_installments': 2
        },
        'portfolio': {
            'title': 'Portfólio Profissional',
            'price': 249.90,
            'max_installments': 3
        },
        'landing': {
            'title': 'Landing Page de Alta Conversão',
            'price': 379.90,
            'max_installments': 4
        },
        'institucional': {
            'title': 'Site Institucional Premium',
            'price': 649.90,
            'max_installments': 5
        },
        'empresarial': {
            'title': 'Site Empresarial Avançado',
            'price': 847.00,
            'max_installments': 12
        },
        'loja': {
            'title': 'Loja Virtual Própria',
            'price': 1297.00,
            'max_installments': 12
        }
    }
    return services.get(service_id, {})
```

### URLs (core/urls.py)
```python
path('create-mercadopago-preference/', views.create_mercadopago_preference, name='create_mercadopago_preference'),
path('webhook/mercadopago/', views.mercadopago_webhook, name='mercadopago_webhook'),
path('pagamento/sucesso/', views.payment_success, name='payment_success'),
path('pagamento/erro/', views.payment_error, name='payment_error'),
path('pagamento/pendente/', views.payment_pending, name='payment_pending'),
```

### JavaScript para Frontend
```javascript
// Integração com Mercado Pago Checkout Pro
function initMercadoPago() {
    const mp = new MercadoPago('{{ MERCADO_PAGO_PUBLIC_KEY }}');
    
    // Função para criar preferência e redirecionar
    window.createMercadoPagoCheckout = function(serviceId) {
        fetch('/create-mercadopago-preference/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `service_id=${serviceId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.preference_id) {
                // Redirecionar para checkout
                window.open(data.init_point, '_blank');
            } else {
                alert('Erro ao processar pagamento');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao processar pagamento');
        });
    };
}

// Função auxiliar para CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', initMercadoPago);
```

## Configuração de Webhook

### No Painel do Mercado Pago
1. Acesse sua conta no Mercado Pago
2. Vá para "Integrações" > "Webhooks"
3. Adicione a URL: `https://hoztech.com.br/webhook/mercado-pago/`
4. Selecione os eventos:
   - `payment`
   - `merchant_order`

### Eventos Processados
- **payment.created**: Pagamento criado
- **payment.approved**: Pagamento aprovado
- **payment.rejected**: Pagamento rejeitado
- **payment.pending**: Pagamento pendente

## Métodos de Pagamento Suportados

### PIX
- Pagamento instantâneo
- Disponível 24/7
- QR Code gerado automaticamente

### Cartão de Crédito
- Parcelamento conforme configuração
- Bandeiras: Visa, Mastercard, Elo, etc.
- 3D Secure para segurança

### Cartão de Débito
- Débito online
- Principais bancos brasileiros

### Boleto Bancário
- Vencimento configurável
- Linha digitável e código de barras

## Testes

### Cartões de Teste
```
# Cartão aprovado
4509 9535 6623 3704
CVC: 123
Vencimento: 11/25

# Cartão rejeitado
4774 0015 4285 4747
CVC: 123
Vencimento: 11/25
```

### PIX de Teste
- Use CPF: 12345678909
- Valor mínimo: R$ 0,01
- Valor máximo: R$ 10.000,00

## Monitoramento

### Logs de Transação
- Todas as transações são logadas
- Status de pagamento rastreado
- Webhooks registrados para auditoria

### Dashboard Mercado Pago
- Relatórios de vendas
- Análise de conversão
- Gestão de disputas

## Segurança

### Validação de Webhook
- Verificação de origem
- Validação de assinatura
- Rate limiting

### Dados Sensíveis
- Tokens nunca expostos no frontend
- Comunicação sempre via HTTPS
- Logs sem informações sensíveis

---

**Status**: Documentação preparada para implementação
**Próximos passos**: Implementar código e testar integração