# 🚀 Guia de Integração - MercadoPago CardForm

## 📋 Visão Geral

Este guia explica como integrar o snippet JavaScript do MercadoPago CardForm no seu projeto HOZ TECH, garantindo detecção automática de campos e compatibilidade com renderização dinâmica.

## 📁 Arquivos Criados

1. **`mercadopago_cardform.js`** - Classe principal do CardForm
2. **`exemplo_cardform.html`** - Exemplo completo de implementação
3. **`CARDFORM_INTEGRATION_GUIDE.md`** - Este guia

## 🔧 Integração no Projeto Existente

### 1. Incluir o Script no Template

Adicione no seu template `services.html` ou onde necessário:

```html
<!-- Após o SDK do MercadoPago -->
<script src="https://sdk.mercadopago.com/js/v2"></script>
<script src="{% static 'core/js/mercadopago_cardform.js' %}"></script>
```

### 2. HTML dos Campos

Certifique-se de que seus campos tenham os IDs corretos:

```html
<form id="mercadopago-form">
    <!-- Campos obrigatórios -->
    <div id="cardNumber"></div>
    <div id="cardExpirationDate"></div>
    <div id="cardSecurityCode"></div>
    
    <!-- Campos opcionais -->
    <input type="text" id="cardholderName" placeholder="Nome do portador">
    <select id="issuer"></select>
    <select id="installments"></select>
    <select id="identificationType"></select>
    <input type="text" id="identificationNumber">
    
    <!-- Containers para feedback -->
    <div id="mp-error-container"></div>
    <div id="mp-loading" style="display: none;">Carregando...</div>
    
    <button type="submit">Pagar</button>
</form>
```

### 3. Inicialização JavaScript

```javascript
// Inicialização básica
const cardForm = initMercadoPagoCardForm('{{ MERCADO_PAGO_PUBLIC_KEY }}');

// Com observador para mudanças no DOM
const observer = observeMercadoPagoFields(cardForm);

// Event listeners
document.addEventListener('mp:cardFormMounted', function(event) {
    console.log('✅ CardForm montado!', event.detail);
    // Habilitar botão de pagamento
    document.getElementById('pay-button').disabled = false;
});

document.addEventListener('mp:cardTokenReceived', function(event) {
    console.log('🎯 Token recebido:', event.detail.token);
    // Enviar token para seu backend
    processPayment(event.detail.token);
});

document.addEventListener('mp:cardFormError', function(event) {
    console.error('❌ Erro:', event.detail);
    // Mostrar erro para o usuário
    showError(event.detail.message);
});
```

## 🎯 Integração com o Sistema Atual

### Modificar `services.html`

1. **Substituir a inicialização atual** do MercadoPago:

```javascript
// ANTES (código atual)
window.createMercadoPagoCheckout = function(serviceType) {
    // código atual...
};

// DEPOIS (novo código)
let cardFormInstance = null;

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    initCardForm();
});

function initCardForm() {
    const publicKey = '{{ MERCADO_PAGO_PUBLIC_KEY }}';
    
    if (!publicKey) {
        console.error('Chave pública não encontrada');
        return;
    }
    
    cardFormInstance = initMercadoPagoCardForm(publicKey, {
        processingMode: 'aggregator',
        locale: 'pt-BR'
    });
    
    // Observar mudanças no DOM
    observeMercadoPagoFields(cardFormInstance);
}
```

2. **Atualizar os botões de serviço**:

```html
<!-- ANTES -->
<button class="btn-cta" onclick="createMercadoPagoCheckout('portfolio')">
    Contratar Agora
</button>

<!-- DEPOIS -->
<button class="btn-cta" onclick="openPaymentModal('portfolio', 249.90)">
    Contratar Agora
</button>
```

3. **Criar modal de pagamento**:

```javascript
function openPaymentModal(serviceType, amount) {
    // Atualizar valor
    if (cardFormInstance) {
        cardFormInstance.updateAmount(amount);
    }
    
    // Abrir modal
    const modal = new bootstrap.Modal(document.getElementById('paymentModal'));
    modal.show();
    
    // Remontar CardForm quando modal abrir
    document.getElementById('paymentModal').addEventListener('shown.bs.modal', function() {
        if (cardFormInstance) {
            cardFormInstance.remount();
        }
    });
}
```

### Integração com Backend Django

1. **Atualizar a view `create_mercado_pago_preference`**:

```python
@csrf_exempt
@require_POST
def process_card_payment(request):
    """Processa pagamento com token do cartão"""
    try:
        data = json.loads(request.body)
        token = data.get('token')
        amount = float(data.get('amount', 0))
        installments = int(data.get('installments', 1))
        
        # Configurar SDK
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        
        # Criar pagamento
        payment_data = {
            "transaction_amount": amount,
            "token": token,
            "installments": installments,
            "payment_method_id": data.get('payment_method_id'),
            "issuer_id": data.get('issuer_id'),
            "payer": {
                "email": data.get('payer_email', 'test@test.com')
            }
        }
        
        payment_response = sdk.payment().create(payment_data)
        
        if payment_response["status"] == 201:
            payment = payment_response["response"]
            return JsonResponse({
                'success': True,
                'payment_id': payment['id'],
                'status': payment['status']
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Erro ao processar pagamento'
            })
            
    except Exception as e:
        logger.error(f"Erro no pagamento: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        })
```

2. **Adicionar nova URL**:

```python
# core/urls.py
path('mercado-pago/process-card-payment/', views.process_card_payment, name='process_card_payment'),
```

## 🔄 Casos de Uso Especiais

### 1. Modais Dinâmicos

```javascript
// Quando abrir modal
$('#paymentModal').on('shown.bs.modal', function() {
    if (cardFormInstance) {
        cardFormInstance.remount();
    }
});

// Quando fechar modal
$('#paymentModal').on('hidden.bs.modal', function() {
    if (cardFormInstance) {
        cardFormInstance.destroy();
    }
});
```

### 2. Single Page Applications (SPA)

```javascript
// Ao navegar para nova página/seção
function navigateToPayment() {
    // Destruir instância atual
    if (cardFormInstance) {
        cardFormInstance.destroy();
    }
    
    // Aguardar DOM atualizar
    setTimeout(() => {
        // Criar nova instância
        cardFormInstance = initMercadoPagoCardForm(PUBLIC_KEY);
        observeMercadoPagoFields(cardFormInstance);
    }, 100);
}
```

### 3. Formulários Condicionais

```javascript
// Quando mostrar campos de cartão
function showCardFields() {
    document.getElementById('card-fields').style.display = 'block';
    
    // Remontar CardForm
    if (cardFormInstance) {
        cardFormInstance.remount();
    }
}
```

## 🎨 Estilos CSS Recomendados

```css
/* Campos do MercadoPago */
.mp-field {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.mp-field:focus {
    outline: none;
    border-color: #009ee3;
    box-shadow: 0 0 0 3px rgba(0, 158, 227, 0.1);
}

/* Estados de erro */
.mp-field.mp-form-control.mp-error {
    border-color: #dc3545;
}

/* Loading */
.mp-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

/* Responsivo */
@media (max-width: 768px) {
    .mp-field {
        font-size: 16px; /* Evita zoom no iOS */
    }
}
```

## 🧪 Testes

### Dados de Teste

```javascript
// Cartões de teste
const testCards = {
    approved: {
        number: '4509 9535 6623 3704',
        cvv: '123',
        expiry: '11/25',
        name: 'APRO'
    },
    rejected: {
        number: '4774 0015 4285 4747',
        cvv: '123',
        expiry: '11/25',
        name: 'OTHE'
    }
};
```

### Função de Debug

```javascript
// Adicionar ao console para debug
window.debugCardForm = function() {
    console.log('🔍 Debug CardForm:', {
        instance: cardFormInstance,
        isMounted: cardFormInstance?.isMounted,
        sdkLoaded: typeof MercadoPago !== 'undefined',
        fieldsAvailable: cardFormInstance?.areFieldsAvailable()
    });
};
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Campos não detectados**:
   - Verificar se os IDs estão corretos
   - Chamar `remount()` após mudanças no DOM
   - Usar o observador de mutações

2. **SDK não carrega**:
   - Verificar conexão com internet
   - Verificar se não há bloqueadores de script
   - Verificar console para erros

3. **Formulário não monta em modais**:
   - Chamar `remount()` no evento `shown.bs.modal`
   - Aguardar DOM estar pronto
   - Verificar se os campos existem no modal

### Logs de Debug

```javascript
// Habilitar logs detalhados
window.MP_DEBUG = true;

// Escutar todos os eventos
['mp:cardFormMounted', 'mp:cardFormError', 'mp:cardTokenReceived', 'mp:loadingStateChanged']
.forEach(event => {
    document.addEventListener(event, (e) => {
        console.log(`🎯 ${event}:`, e.detail);
    });
});
```

## 📱 Compatibilidade

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ iOS Safari 13+
- ✅ Android Chrome 80+

## 🔐 Segurança

- ✅ Tokens são gerados no frontend
- ✅ Dados sensíveis não trafegam pelo seu servidor
- ✅ Comunicação direta com MercadoPago
- ✅ Validação no backend obrigatória

---

**Desenvolvido por HOZ TECH** 🚀

*Para suporte, consulte a documentação oficial do MercadoPago ou entre em contato com a equipe de desenvolvimento.*