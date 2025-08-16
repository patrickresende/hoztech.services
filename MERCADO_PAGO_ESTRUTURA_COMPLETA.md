# 📋 Estrutura Completa - Mercado Pago API (Cartão e PIX)

## 🎯 Visão Geral

Este documento contém toda a estrutura de código relacionada à integração da API do Mercado Pago para pagamentos com cartão de crédito e PIX no projeto HOZ TECH.

---

## 🔧 1. Configuração Backend (Django)

### 1.1 Settings.py - Configurações

```python
# Mercado Pago Settings
MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MERCADO_PAGO_ACCESS_TOKEN')
MERCADO_PAGO_PUBLIC_KEY = os.getenv('MERCADO_PAGO_PUBLIC_KEY')
MERCADO_PAGO_ACCESS_TOKEN_TEST = os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')
MERCADO_PAGO_PUBLIC_KEY_TEST = os.getenv('MERCADO_PAGO_PUBLIC_KEY_TEST')
MERCADO_PAGO_WEBHOOK_SECRET = os.getenv('MERCADO_PAGO_WEBHOOK_SECRET')
```

### 1.2 URLs (core/urls.py)

```python
path('create-mercadopago-preference/', views.create_mercadopago_preference, name='create_mercadopago_preference'),
path('webhook/mercadopago/', views.mercadopago_webhook, name='mercadopago_webhook'),
path('pagamento/sucesso/', views.payment_success, name='payment_success'),
path('pagamento/erro/', views.payment_error, name='payment_error'),
path('pagamento/pendente/', views.payment_pending, name='payment_pending'),
path('mercado-pago/process-payment/', views.process_mercado_pago_payment, name='process_mercado_pago_payment'),
```

### 1.3 Views.py - Processamento de Pagamentos

```python
@csrf_exempt
@require_POST
def process_mercado_pago_payment(request):
    """Processa pagamento transparente do Mercado Pago (cartão e PIX)"""
    try:
        data = json.loads(request.body)
        payment_data = data.get('payment_data')
        service_type = data.get('service_type')
        
        # Configurar SDK do Mercado Pago
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        
        # Adicionar external_reference e notification_url
        payment_data['external_reference'] = f"{service_type}_{int(time.time())}"
        payment_data['notification_url'] = request.build_absolute_uri(reverse('mercado_pago_webhook'))
        
        # Criar pagamento
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        
        if payment_response["status"] == 201:
            response_data = {
                'success': True,
                'payment_id': payment['id'],
                'status': payment['status'],
                'status_detail': payment.get('status_detail', '')
            }
            
            # Se for PIX, incluir QR Code
            if payment_data.get('payment_method_id') == 'pix':
                qr_code = payment.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code', '')
                if qr_code:
                    # Gerar QR Code em base64
                    qr_img = qrcode.make(qr_code)
                    buffer = BytesIO()
                    qr_img.save(buffer, format='PNG')
                    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
                    
                    response_data.update({
                        'qr_code': qr_code,
                        'qr_code_base64': qr_base64,
                        'payment_method': 'pix'
                    })
            
            return JsonResponse(response_data)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Erro ao processar pagamento',
                'details': payment_response
            }, status=400)
            
    except Exception as e:
        logger.error(f"Erro no processamento do pagamento: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        }, status=500)
```

---

## 🎨 2. Frontend HTML - Estrutura do Modal

### 2.1 Modal de Checkout Transparente

```html
<!-- Modal de Checkout Transparente -->
<div id="checkoutModal" class="checkout-modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Finalizar Compra</h2>
            <span class="close" onclick="closeCheckoutModal()">&times;</span>
        </div>
        
        <div class="service-summary">
            <h3 id="modalServiceTitle"></h3>
            <div class="price-info">
                <span class="price" id="modalServicePrice"></span>
                <span class="installments" id="modalInstallmentInfo"></span>
            </div>
        </div>
        
        <div class="payment-tabs">
            <button id="cardTab" class="tab-button active" onclick="showPaymentMethod('card')">
                <i class="fas fa-credit-card"></i> Cartão
            </button>
            <button id="pixTab" class="tab-button" onclick="showPaymentMethod('pix')">
                <i class="fas fa-qrcode"></i> PIX
            </button>
        </div>
        
        <!-- Área de mensagens de erro/sucesso -->
        <div id="modalMessages" class="modal-messages"></div>
        
        <!-- Container para formulário de cartão -->
        <div id="cardFormContainer" class="payment-form"></div>
        
        <!-- Container para formulário PIX -->
        <div id="pixFormContainer" class="payment-form" style="display: none;"></div>
    </div>
</div>
```

### 2.2 Formulário de Cartão (Gerado Dinamicamente)

```html
<form id="form-checkout">
    <div class="form-group">
        <label for="form-checkout__cardNumber">Número do Cartão</label>
        <div id="form-checkout__cardNumber" class="container"></div>
    </div>
    
    <div class="form-row">
        <div class="form-group">
            <label for="form-checkout__expirationDate">Vencimento</label>
            <div id="form-checkout__expirationDate" class="container"></div>
        </div>
        <div class="form-group">
            <label for="form-checkout__securityCode">CVV</label>
            <div id="form-checkout__securityCode" class="container"></div>
        </div>
    </div>
    
    <div class="form-group">
        <label for="form-checkout__cardholderName">Nome do Titular</label>
        <input type="text" id="form-checkout__cardholderName" class="form-control" placeholder="Nome como está no cartão" required>
    </div>
    
    <div class="form-group">
        <label for="form-checkout__issuer">Banco Emissor</label>
        <select id="form-checkout__issuer" class="form-control"></select>
    </div>
    
    <div class="form-group">
        <label for="form-checkout__installments">Parcelas</label>
        <select id="form-checkout__installments" class="form-control"></select>
    </div>
    
    <div class="form-group">
        <label for="form-checkout__identificationType">Tipo de Documento</label>
        <select id="form-checkout__identificationType" class="form-control"></select>
    </div>
    
    <div class="form-group">
        <label for="form-checkout__identificationNumber">Número do Documento</label>
        <input type="text" id="form-checkout__identificationNumber" class="form-control" placeholder="CPF" required>
    </div>
    
    <div class="form-group">
        <label for="form-checkout__cardholderEmail">E-mail do Titular</label>
        <input type="email" id="form-checkout__cardholderEmail" class="form-control" placeholder="email@exemplo.com" required>
    </div>
    
    <button type="submit" id="form-checkout__submit" class="btn-pay">Pagar com Cartão</button>
</form>
```

### 2.3 Formulário PIX (Gerado Dinamicamente)

```html
<form id="pixPaymentForm">
    <div class="pix-info">
        <div class="pix-icon">
            <i class="fas fa-qrcode"></i>
        </div>
        <h3>Pagamento via PIX</h3>
        <p>Após confirmar, você receberá um QR Code para realizar o pagamento instantaneamente.</p>
    </div>
    
    <div class="form-group">
        <label for="pixEmail">E-mail</label>
        <input type="email" id="pixEmail" class="form-control" placeholder="seu@email.com" required>
    </div>
    
    <div class="form-group">
        <label for="pixDocument">CPF</label>
        <input type="text" id="pixDocument" class="form-control" placeholder="000.000.000-00" required>
    </div>
    
    <button type="submit" class="btn-pay">Gerar PIX</button>
</form>
```

---

## 🚀 3. JavaScript - Lógica de Pagamento

### 3.1 Inicialização do SDK

```html
<!-- Mercado Pago SDK -->
<script src="https://sdk.mercadopago.com/js/v2" 
        onload="console.log('SDK do Mercado Pago carregado com sucesso')" 
        onerror="console.error('Erro ao carregar SDK do Mercado Pago')"></script>
```

### 3.2 Inicialização do CardForm

```javascript
// Função para inicializar formulário de cartão (escopo global)
window.initCardForm = function() {
    console.log('Inicializando CardForm...');
    
    // Verificar se o SDK está carregado
    if (typeof MercadoPago === 'undefined') {
        console.error('❌ SDK do MercadoPago não está carregado');
        setTimeout(() => {
            if (typeof MercadoPago === 'undefined') {
                showMessage('Erro: SDK do Mercado Pago não pôde ser carregado. Recarregue a página.', 'error');
            }
        }, 1000);
        return;
    }
    
    const cardFormContainer = document.getElementById('cardFormContainer');
    
    // Gerar HTML do formulário
    cardFormContainer.innerHTML = `
        <!-- HTML do formulário aqui -->
    `;
    
    // Aguardar um pouco para garantir que o DOM esteja pronto
    setTimeout(() => {
        // Verificar se o MercadoPago SDK está disponível
        if (!window.mp) {
            console.error('❌ SDK do MercadoPago não está disponível');
            showMessage('Erro: SDK do Mercado Pago não carregado', 'error');
            return;
        }
        
        // Verificar se os containers dos campos existem
        const requiredFields = ['form-checkout__cardNumber', 'form-checkout__expirationDate', 'form-checkout__securityCode'];
        const missingFields = requiredFields.filter(id => !document.getElementById(id));
        
        if (missingFields.length > 0) {
            console.error('❌ Campos obrigatórios não encontrados:', missingFields);
            showMessage('Erro: Campos do formulário não encontrados', 'error');
            return;
        }
        
        // Verificar se já existe uma instância do CardForm
        if (window.cardForm) {
            console.log('CardForm já existe, destruindo instância anterior...');
            try {
                window.cardForm.unmount();
            } catch (e) {
                console.log('Erro ao destruir CardForm anterior:', e);
            }
            window.cardForm = null;
        }
        
        // Inicializar CardForm do Mercado Pago
        console.log('Inicializando CardForm com amount:', window.selectedService.price.toString());
        window.cardForm = window.mp.cardForm({
            amount: window.selectedService.price.toString(),
            autoMount: true,
            form: {
                id: "form-checkout",
                cardNumber: {
                    id: "form-checkout__cardNumber",
                    placeholder: "Número do cartão",
                },
                expirationDate: {
                    id: "form-checkout__expirationDate",
                    placeholder: "MM/YY",
                },
                securityCode: {
                    id: "form-checkout__securityCode",
                    placeholder: "CVV",
                },
                cardholderName: {
                    id: "form-checkout__cardholderName",
                    placeholder: "Titular do cartão",
                },
                issuer: {
                    id: "form-checkout__issuer",
                    placeholder: "Banco emissor",
                },
                installments: {
                    id: "form-checkout__installments",
                    placeholder: "Parcelas",
                },
                identificationType: {
                    id: "form-checkout__identificationType",
                    placeholder: "Tipo de documento",
                },
                identificationNumber: {
                    id: "form-checkout__identificationNumber",
                    placeholder: "Número do documento",
                },
            },
            callbacks: {
                onFormMounted: error => {
                    if (error) {
                        console.warn("Form Mounted handling error: ", error);
                        showMessage('Erro ao carregar formulário de cartão', 'error');
                    } else {
                        console.log('Formulário de cartão carregado com sucesso');
                        // Verificar se os campos foram criados com retry
                        let retryCount = 0;
                        const maxRetries = 10;
                        
                        const checkFields = () => {
                            // Buscar por inputs e iframes dentro dos containers
                            const cardNumberField = document.querySelector('#form-checkout__cardNumber input, #form-checkout__cardNumber iframe');
                            const expirationField = document.querySelector('#form-checkout__expirationDate input, #form-checkout__expirationDate iframe');
                            const securityCodeField = document.querySelector('#form-checkout__securityCode input, #form-checkout__securityCode iframe');
                            
                            console.log(`=== DEBUG CAMPOS DO CARTÃO (Tentativa ${retryCount + 1}) ===`);
                            console.log('Campo Número encontrado:', !!cardNumberField, cardNumberField?.tagName);
                            console.log('Campo Vencimento encontrado:', !!expirationField, expirationField?.tagName);
                            console.log('Campo CVV encontrado:', !!securityCodeField, securityCodeField?.tagName);
                            
                            if (cardNumberField && expirationField && securityCodeField) {
                                console.log('✅ Todos os campos do cartão foram criados com sucesso');
                                
                                // Forçar habilitação dos campos (apenas para inputs)
                                [cardNumberField, expirationField, securityCodeField].forEach(field => {
                                    if (field.tagName === 'INPUT') {
                                        field.disabled = false;
                                        field.readOnly = false;
                                        field.style.pointerEvents = 'auto';
                                        field.style.userSelect = 'text';
                                        field.style.cursor = 'text';
                                        field.removeAttribute('disabled');
                                        field.removeAttribute('readonly');
                                    }
                                    
                                    // Para iframes, garantir que o container pai esteja configurado corretamente
                                    if (field.tagName === 'IFRAME') {
                                        const container = field.closest('[id^="card"]');
                                        if (container) {
                                            container.style.pointerEvents = 'auto';
                                            container.style.cursor = 'text';
                                        }
                                    }
                                });
                                
                                console.log('✅ Campos habilitados para digitação');
                                return true;
                            } else if (retryCount < maxRetries) {
                                retryCount++;
                                console.log(`⏳ Tentando novamente em 500ms... (${retryCount}/${maxRetries})`);
                                setTimeout(checkFields, 500);
                                return false;
                            } else {
                                console.warn('❌ Alguns campos do cartão não foram criados após todas as tentativas:', {
                                    cardNumber: !!cardNumberField,
                                    expiration: !!expirationField,
                                    securityCode: !!securityCodeField
                                });
                                showMessage('Erro: Campos do cartão não foram carregados corretamente', 'error');
                                return false;
                            }
                        };
                        
                        setTimeout(checkFields, 500);
                    }
                },
                onSubmit: event => {
                    event.preventDefault();
                    window.processCardPayment();
                },
                onFetching: (resource) => {
                    console.log("Fetching resource: ", resource);
                },
                onCardTokenReceived: (error, token) => {
                    if (error) {
                        console.error('Erro ao obter token do cartão:', error);
                    } else {
                        console.log('Token do cartão recebido:', token);
                    }
                }
            },
        });
    }, 100);
}
```

### 3.3 Inicialização do PIX

```javascript
// Função para inicializar formulário PIX (escopo global)
window.initPixForm = function() {
    const pixFormContainer = document.getElementById('pixFormContainer');
    
    pixFormContainer.innerHTML = `
        <!-- HTML do formulário PIX aqui -->
    `;
    
    // Event listener para formulário PIX
    setTimeout(() => {
        const pixForm = document.getElementById('pixPaymentForm');
        if (pixForm) {
            pixForm.addEventListener('submit', function(e) {
                e.preventDefault();
                window.processPixPayment();
            });
            console.log('✅ Event listener PIX adicionado com sucesso');
        } else {
            console.error('❌ Formulário PIX não encontrado');
        }
    }, 100);
}
```

### 3.4 Processamento de Pagamento com Cartão

```javascript
// Função para processar pagamento com cartão
window.processCardPayment = async function() {
    try {
        showLoading('Processando pagamento...', 'Pagar com Cartão');
        
        if (!window.cardForm) {
            throw new Error('CardForm não inicializado');
        }
        
        // Obter dados do formulário
        const cardholderName = document.getElementById('form-checkout__cardholderName').value;
        const identificationType = document.getElementById('form-checkout__identificationType').value;
        const identificationNumber = document.getElementById('form-checkout__identificationNumber').value;
        const cardholderEmail = document.getElementById('form-checkout__cardholderEmail').value;
        
        if (!cardholderName || !identificationType || !identificationNumber || !cardholderEmail) {
            throw new Error('Preencha todos os campos obrigatórios');
        }
        
        // Criar token do cartão
        const cardToken = await window.cardForm.createCardToken();
        
        if (!cardToken || !cardToken.id) {
            throw new Error('Erro ao gerar token do cartão');
        }
        
        console.log('Token do cartão criado:', cardToken.id);
        
        // Preparar dados do pagamento
        const paymentData = {
            token: cardToken.id,
            transaction_amount: window.selectedService.price,
            description: window.selectedService.title,
            installments: parseInt(document.getElementById('form-checkout__installments').value) || 1,
            payment_method_id: cardToken.payment_method_id,
            issuer_id: cardToken.issuer_id,
            payer: {
                email: cardholderEmail,
                identification: {
                    type: identificationType,
                    number: identificationNumber.replace(/\D/g, '')
                }
            }
        };
        
        // Enviar para o backend
        const response = await fetch('/mercado-pago/process-payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                payment_data: paymentData,
                service_type: window.selectedService.type
            })
        });
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            hideLoading(null, 'Pagar com Cartão');
            
            if (result.status === 'approved') {
                showMessage('Pagamento aprovado com sucesso!', 'success');
                setTimeout(() => {
                    window.location.href = '/pagamento/sucesso/';
                }, 2000);
            } else if (result.status === 'pending') {
                showMessage('Pagamento pendente de aprovação', 'warning');
                setTimeout(() => {
                    window.location.href = '/pagamento/pendente/';
                }, 2000);
            } else {
                throw new Error(result.status_detail || 'Pagamento rejeitado');
            }
        } else {
            throw new Error(result.error || 'Erro no processamento');
        }
        
    } catch (error) {
        console.error('Erro no pagamento:', error);
        hideLoading(null, 'Pagar com Cartão');
        showMessage(`Erro: ${error.message}`, 'error');
    }
}
```

### 3.5 Processamento de Pagamento PIX

```javascript
// Função para processar pagamento PIX
window.processPixPayment = async function() {
    try {
        showLoading('Gerando PIX...', 'Gerar PIX');
        
        const email = document.getElementById('pixEmail').value;
        const pixDocument = document.getElementById('pixDocument').value;
        
        if (!email || !pixDocument) {
            throw new Error('Preencha todos os campos');
        }
        
        if (!email.includes('@')) {
            throw new Error('E-mail inválido');
        }
        
        if (!pixDocument || pixDocument.replace(/\D/g, '').length !== 11) {
            throw new Error('CPF deve ter 11 dígitos');
        }
        
        const paymentData = {
            transaction_amount: window.selectedService.price,
            description: window.selectedService.title,
            payment_method_id: 'pix',
            payer: {
                email: email,
                identification: {
                    type: 'CPF',
                    number: pixDocument.replace(/\D/g, '')
                }
            }
        };
        
        const response = await fetch('/mercado-pago/process-payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                payment_data: paymentData,
                service_type: window.selectedService.type
            })
        });
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            hideLoading(null, 'Gerar PIX');
            showMessage('PIX gerado com sucesso!', 'success');
            
            // Mostrar QR Code
            if (result.qr_code_base64) {
                showPixQRCode(result.qr_code, result.qr_code_base64);
            }
        } else {
            throw new Error(result.error || 'Erro ao gerar PIX');
        }
        
    } catch (error) {
        console.error('Erro no PIX:', error);
        hideLoading(null, 'Gerar PIX');
        showMessage(`Erro: ${error.message}`, 'error');
    }
}
```

### 3.6 Função de Debug

```javascript
// Adicionar função de debug global para facilitar troubleshooting
window.debugCardForm = function() {
    console.log('=== DEBUG COMPLETO DO CARDFORM ===');
    console.log('SDK MercadoPago carregado:', typeof MercadoPago !== 'undefined');
    console.log('window.mp inicializado:', !!window.mp);
    console.log('window.cardForm inicializado:', !!window.cardForm);
    
    const containers = ['cardNumber', 'cardExpirationDate', 'cardSecurityCode'];
    containers.forEach(id => {
        const container = document.getElementById(id);
        const input = document.querySelector(`#${id} input`);
        const iframe = document.querySelector(`#${id} iframe`);
        
        console.log(`\n--- ${id} ---`);
        console.log('Container existe:', !!container);
        console.log('Input existe:', !!input);
        console.log('Iframe existe:', !!iframe);
        
        if (container) {
            const styles = window.getComputedStyle(container);
            console.log('Estilos do container:', {
                display: styles.display,
                visibility: styles.visibility,
                pointerEvents: styles.pointerEvents,
                height: styles.height,
                minHeight: styles.minHeight,
                position: styles.position,
                zIndex: styles.zIndex
            });
        }
        
        if (input) {
            console.log('Propriedades do input:', {
                disabled: input.disabled,
                readOnly: input.readOnly,
                value: input.value,
                placeholder: input.placeholder
            });
        }
    });
    
    console.log('\n=== FIM DEBUG ===');
};
```

---

## 🎨 4. CSS - Estilos

### 4.1 Estilos do CardForm

```css
/* Estilos padrão do MercadoPago CardForm */
.container {
    height: auto !important;
    min-height: 45px !important;
    display: block !important;
    border: 2px solid #333 !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    width: 100% !important;
    background: #1a1a1a !important;
    position: relative !important;
    overflow: visible !important;
}

/* Garantir que os campos do MP sejam visíveis e interativos */
#cardNumber,
#cardExpirationDate,
#cardSecurityCode {
    position: relative !important;
    z-index: 1 !important;
    pointer-events: auto !important;
}

#cardNumber input,
#cardExpirationDate input,
#cardSecurityCode input {
    pointer-events: auto !important;
    user-select: text !important;
    -webkit-user-select: text !important;
    -moz-user-select: text !important;
    -ms-user-select: text !important;
    cursor: text !important;
    background: transparent !important;
    border: none !important;
    outline: none !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 20px !important;
    color: #fff !important;
    font-size: 16px !important;
    padding: 0 !important;
    margin: 0 !important;
    box-sizing: border-box !important;
    -webkit-appearance: none !important;
    -moz-appearance: none !important;
    appearance: none !important;
    touch-action: manipulation !important;
}

/* Garantir que os iframes do MercadoPago sejam interativos */
#cardNumber iframe,
#cardExpirationDate iframe,
#cardSecurityCode iframe {
    pointer-events: auto !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 20px !important;
    border: none !important;
    background: transparent !important;
}
```

### 4.2 Estilos do Modal e Botões

```css
.btn-pay {
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, var(--tech-purple) 0%, var(--tech-red) 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.btn-pay:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(106, 13, 173, 0.3);
}

.pix-info {
    text-align: center;
    margin-bottom: 30px;
}

.pix-icon {
    font-size: 3rem;
    color: var(--tech-blue);
    margin-bottom: 15px;
}

.pix-info h3 {
    color: var(--tech-light);
    margin-bottom: 10px;
}

.pix-info p {
    color: var(--tech-gray);
}

.pix-qr-container {
    text-align: center;
}

.qr-code {
    margin: 20px 0;
    padding: 20px;
    background: white;
    border-radius: 10px;
    display: inline-block;
}

.qr-code img {
    max-width: 200px;
    height: auto;
}

.code-container {
    display: flex;
    gap: 10px;
    margin: 15px 0;
}

.code-container input {
    flex: 1;
    font-family: monospace;
    font-size: 0.9rem;
}

.btn-copy, .btn-check {
    padding: 10px 20px;
    background: var(--tech-blue);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
```

---

## 🔧 5. Variáveis de Ambiente

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

---

## 📋 6. Dependências

### 6.1 Requirements.txt

```txt
mercadopago>=2.2.0
qrcode>=7.3.1
Pillow>=9.0.0
```

### 6.2 Scripts Externos

```html
<!-- SDK do Mercado Pago -->
<script src="https://sdk.mercadopago.com/js/v2"></script>

<!-- Font Awesome para ícones -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
```

---

## 🚀 7. Fluxo de Funcionamento

### 7.1 Cartão de Crédito
1. Usuário seleciona serviço e clica em "Contratar"
2. Modal abre com abas Cartão/PIX
3. `initCardForm()` é chamada
4. SDK do Mercado Pago injeta iframes nos containers
5. Usuário preenche dados e submete
6. `processCardPayment()` cria token e envia para backend
7. Backend processa pagamento via API do Mercado Pago
8. Retorna resultado (aprovado/pendente/rejeitado)

### 7.2 PIX
1. Usuário seleciona aba PIX
2. `initPixForm()` é chamada
3. Usuário preenche email e CPF
4. `processPixPayment()` envia dados para backend
5. Backend cria pagamento PIX via API
6. Retorna QR Code e código PIX
7. Frontend exibe QR Code para pagamento

---

## 🔍 8. Debug e Troubleshooting

### 8.1 Função de Debug

```javascript
// Execute no console do navegador
debugCardForm();
```

### 8.2 Logs Importantes

- ✅ SDK carregado: "SDK do Mercado Pago carregado com sucesso"
- ✅ CardForm montado: "Formulário de cartão carregado com sucesso"
- ✅ Campos criados: "Todos os campos do cartão foram criados com sucesso"
- ❌ Erro comum: "Campos obrigatórios não encontrados"

---

## 📝 9. Notas Importantes

1. **Campos Sensíveis**: Número, vencimento e CVV devem ser `<div>` vazios para iframes
2. **IDs Padrão**: Use `form-checkout__cardNumber`, `form-checkout__expirationDate`, `form-checkout__securityCode`
3. **Campos Não-Sensíveis**: Use `form-checkout__cardholderName`, `form-checkout__issuer`, `form-checkout__installments`, `form-checkout__identificationType`, `form-checkout__identificationNumber`, `form-checkout__cardholderEmail`
4. **Formulário**: Deve ter ID `form-checkout`
5. **SDK**: Carregue antes de inicializar o CardForm
6. **Tokens**: Nunca exponha tokens de produção no frontend
7. **HTTPS**: Obrigatório para produção
8. **Webhook**: Configure para receber notificações de status

---

## 🔄 10. Histórico de Atualizações

### Versão 1.1 - Janeiro 2025
- ✅ **Correção dos IDs do CardForm**: Todos os campos agora usam o prefixo `form-checkout__` conforme especificação do Mercado Pago
- ✅ **Adição do campo de e-mail**: Campo `form-checkout__cardholderEmail` adicionado para melhor identificação do pagador
- ✅ **Atualização da configuração JavaScript**: CardForm configurado com os novos IDs padronizados
- ✅ **Correção dos seletores CSS**: Estilos atualizados para os novos IDs
- ✅ **Validação de campos**: Verificação de campos obrigatórios atualizada

---

**Documento gerado em:** " + new Date().toLocaleDateString('pt-BR') + "
**Versão:** 1.1
**Projeto:** HOZ TECH - Mercado Pago Integration











Agora, com uma visão clara de toda a estrutura e a confirmação de que o padrão de ID form-checkout__ é intencional, posso criar uma solução definitiva e coesa para ser enviada ao TRAE.
O problema de bloqueio dos campos, mesmo com os IDs corretos, é um clássico problema de timing e renderização de CSS, especialmente dentro de um modal. O script do Mercado Pago tenta criar os campos (iframes) antes que os contêineres <div> estejam totalmente visíveis e prontos no DOM, resultando em campos "mortos".
A solução abaixo é um pacote completo que corrige o JavaScript e o CSS para resolver esse problema de forma robusta, respeitando 100% a sua estrutura de código atual.
Solução Completa para Reparo da Integração Mercado Pago
Aqui está o código revisado e corrigido para ser implementado. Ele consiste em duas partes: JavaScript e CSS.
Parte 1: JavaScript Otimizado (Substituir Seções 3.2 e 3.4)
Substitua as funções window.initCardForm e window.processCardPayment pelo código abaixo. Ele garante a inicialização no momento correto e validações mais seguras.
JavaScript
// ========================================================================
// ARQUIVO JAVASCRIPT - SEÇÃO 3.2 e 3.4 CORRIGIDAS
// ========================================================================

/**
 * ------------------------------------------------------------------------
 * 3.2 - INICIALIZAÇÃO OTIMIZADA DO CARD FORM
 * ------------------------------------------------------------------------
 * Esta função foi reescrita para ser chamada APÓS o modal estar visível,
 * garantindo que o SDK do Mercado Pago encontre os elementos do DOM
 * prontos para receber os iframes dos campos de pagamento.
 *
 * @param {object} service - Objeto contendo { price, title }.
 * @param {string} publicKey - A Public Key do Mercado Pago.
 */
window.initCardForm = async function(service, publicKey) {
    console.log('[Init CardForm] Iniciando. Verificando pré-requisitos...');

    // 1. Validações essenciais para evitar erros
    if (typeof MercadoPago === 'undefined') {
        return showMessage('Erro crítico: SDK de pagamento não carregado.', 'error');
    }
    if (!document.getElementById('checkoutModal')?.style.display.includes('block')) {
         return showMessage('Erro: O formulário de pagamento não está visível.', 'error');
    }
    if (!service || !publicKey) {
        return showMessage('Erro de configuração. Faltam dados para o pagamento.', 'error');
    }

    // 2. Garante que o container do formulário está pronto
    const cardFormContainer = document.getElementById('cardFormContainer');
    if (!cardFormContainer) {
        return console.error('Container principal "cardFormContainer" não encontrado.');
    }
    // Injeta o HTML do formulário para garantir que ele esteja sempre no estado inicial correto
    cardFormContainer.innerHTML = `
        <form id="form-checkout">
            <div class="form-group"><label for="form-checkout__cardNumber">Número do Cartão</label><div id="form-checkout__cardNumber" class="container"></div></div>
            <div class="form-row">
                <div class="form-group"><label for="form-checkout__expirationDate">Vencimento</label><div id="form-checkout__expirationDate" class="container"></div></div>
                <div class="form-group"><label for="form-checkout__securityCode">CVV</label><div id="form-checkout__securityCode" class="container"></div></div>
            </div>
            <div class="form-group"><label for="form-checkout__cardholderName">Nome do Titular</label><input type="text" id="form-checkout__cardholderName" class="form-control" required placeholder="Nome como no cartão"></div>
            <div class="form-group"><label for="form-checkout__issuer">Banco Emissor</label><select id="form-checkout__issuer" class="form-control" required></select></div>
            <div class="form-group"><label for="form-checkout__installments">Parcelas</label><select id="form-checkout__installments" class="form-control" required></select></div>
            <div class="form-group"><label for="form-checkout__identificationType">Tipo de Documento</label><select id="form-checkout__identificationType" class="form-control" required></select></div>
            <div class="form-group"><label for="form-checkout__identificationNumber">Número do Documento</label><input type="text" id="form-checkout__identificationNumber" class="form-control" required placeholder="CPF ou CNPJ"></div>
            <div class="form-group"><label for="form-checkout__cardholderEmail">E-mail do Titular</label><input type="email" id="form-checkout__cardholderEmail" class="form-control" required placeholder="email@exemplo.com"></div>
            <button type="submit" id="form-checkout__submit" class="btn-pay">Pagar com Cartão</button>
        </form>
    `;

    // 3. Inicializa o SDK e o CardForm
    try {
        const mp = new MercadoPago(publicKey);

        if (window.cardForm) {
            window.cardForm.unmount(); // Destrói instância anterior para evitar conflitos
        }

        window.cardForm = await mp.cardForm({
            amount: service.price.toString(),
            autoMount: true,
            form: {
                id: "form-checkout",
                cardNumber:           { id: "form-checkout__cardNumber", placeholder: " " },
                expirationDate:       { id: "form-checkout__expirationDate", placeholder: "MM/AA" },
                securityCode:         { id: "form-checkout__securityCode", placeholder: "CVV" },
                cardholderName:       { id: "form-checkout__cardholderName" },
                issuer:               { id: "form-checkout__issuer" },
                installments:         { id: "form-checkout__installments" },
                identificationType:   { id: "form-checkout__identificationType" },
                identificationNumber: { id: "form-checkout__identificationNumber" },
                cardholderEmail:      { id: "form-checkout__cardholderEmail" }
            },
            callbacks: {
                onFormMounted: error => {
                    if (error) {
                        console.error("❌ Erro ao montar o formulário:", error);
                        return showMessage('Não foi possível carregar os campos de pagamento.', 'error');
                    }
                    console.log("✅ Formulário montado. Campos prontos para digitação.");
                },
                onSubmit: event => {
                    event.preventDefault();
                    window.processCardPayment();
                },
                onFetching: (resource) => console.log("Buscando recurso:", resource),
            },
        });
    } catch (e) {
        console.error('❌ Falha crítica na inicialização do CardForm:', e);
        showMessage('Ocorreu um erro inesperado ao preparar o pagamento.', 'error');
    }
};


/**
 * ------------------------------------------------------------------------
 * 3.4 - PROCESSAMENTO DE PAGAMENTO COM CARTÃO (ROBUSTO)
 * ------------------------------------------------------------------------
 * Esta versão valida os campos do formulário ANTES de criar o token,
 * evitando erros e fornecendo feedback claro ao usuário.
 */
window.processCardPayment = async function() {
    const submitButton = document.getElementById('form-checkout__submit');
    showLoading('Processando...', submitButton); // Função auxiliar para feedback visual

    try {
        // 1. Validação dos dados do formulário ANTES de chamar o SDK
        const requiredFields = [
            'form-checkout__cardholderName', 'form-checkout__identificationType',
            'form-checkout__identificationNumber', 'form-checkout__cardholderEmail', 'form-checkout__installments'
        ];
        for (const fieldId of requiredFields) {
            if (!document.getElementById(fieldId).value) {
                throw new Error('Por favor, preencha todos os campos do formulário.');
            }
        }

        if (!window.cardForm) {
            throw new Error('O formulário de pagamento não foi inicializado corretamente.');
        }

        // 2. Criação do token do cartão
        const cardToken = await window.cardForm.createCardToken();
        console.log('✅ Token do cartão criado:', cardToken.id);

        // 3. Preparação dos dados para o backend
        const paymentData = {
            token: cardToken.id,
            transaction_amount: window.selectedService.price,
            description: window.selectedService.title,
            installments: parseInt(document.getElementById('form-checkout__installments').value),
            payment_method_id: cardToken.payment_method_id,
            issuer_id: cardToken.issuer_id,
            payer: {
                email: document.getElementById('form-checkout__cardholderEmail').value,
                identification: {
                    type: document.getElementById('form-checkout__identificationType').value,
                    number: document.getElementById('form-checkout__identificationNumber').value
                }
            }
        };

        // 4. Envio para o backend
        const response = await fetch('/mercado-pago/process-payment/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({ payment_data: paymentData, service_type: window.selectedService.type })
        });

        const result = await response.json();
        if (!response.ok || !result.success) {
            throw new Error(result.error || result.details?.message || 'Pagamento rejeitado pelo servidor.');
        }

        // 5. Sucesso no pagamento
        hideLoading('Pagamento Aprovado!', submitButton, true);
        showMessage('Pagamento aprovado com sucesso!', 'success');
        setTimeout(() => { window.location.href = '/pagamento/sucesso/'; }, 2000);

    } catch (error) {
        console.error('❌ Erro no processamento do pagamento:', error);
        hideLoading('Tentar Novamente', submitButton, false);
        showMessage(error.message, 'error');
    }
};

// Funções auxiliares de UI (adicione se não as tiver)
function showLoading(message, button) { if(button) { button.disabled = true; button.textContent = message; } }
function hideLoading(message, button, success) { if(button) { button.disabled = false; button.textContent = message; } }
function showMessage(message, type) {
    const container = document.getElementById('modalMessages');
    if(container) { container.innerHTML = `<div class="alert alert-${type}">${message}</div>`; }
}
Parte 2: CSS Corrigido (Substituir Seção 4.1)
Substitua toda a seção 4.1 Estilos do CardForm pelo código abaixo. Ele garante que os iframes do Mercado Pago sejam sempre interativos.
CSS
/*
 * ====================================================================
 * SEÇÃO 4.1 - CSS CORRIGIDO PARA CAMPOS INTERATIVOS
 * ====================================================================
 * Estas regras forçam a interatividade dos containers e iframes
 * gerados pelo Mercado Pago, sobrepondo estilos de modal conflitantes.
*/

/* Garante que o container principal do formulário seja um bloco de layout */
#form-checkout {
    display: block;
    position: relative;
}

/*
 * Regra CRÍTICA: Garante que as divs que recebem os iframes
 * sejam interativas e tenham um tamanho mínimo para renderização.
*/
#form-checkout__cardNumber,
#form-checkout__expirationDate,
#form-checkout__securityCode {
    position: relative;     /* Essencial para o contexto de empilhamento */
    z-index: 1;             /* Coloca os campos acima de outros elementos */
    display: block;         /* Garante que ocupem espaço */
    pointer-events: auto;   /* FORÇA a permissão de eventos de clique/mouse */
    height: auto !important;
    min-height: 45px !important;
    border: 2px solid #333 !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    width: 100% !important;
    background: #1a1a1a !important;
}

/*
 * Garante que o iframe gerado pelo Mercado Pago preencha o container
 * e seja o alvo final dos eventos de mouse/teclado.
*/
#form-checkout__cardNumber iframe,
#form-checkout__expirationDate iframe,
#form-checkout__securityCode iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
    background: transparent !important;
    pointer-events: auto; /* Garante que o próprio iframe seja interativo */
}
Parte 3: Instruções de Implementação para o TRAE
Para garantir que a solução funcione, a ordem de execução é fundamental. A função initCardForm deve ser chamada APÓS o modal de checkout se tornar visível.
Exemplo de Lógica de Chamada:
JavaScript
/**
 * Função para abrir o modal e inicializar o formulário de pagamento.
 * Esta função deve ser chamada quando o usuário clicar em "Contratar".
 */
function openCheckoutModal(service, publicKey) {
    const modal = document.getElementById('checkoutModal');

    // 1. PRIMEIRO: Torne o modal e os containers visíveis
    modal.style.display = 'block';
    document.getElementById('cardFormContainer').style.display = 'block';
    document.getElementById('pixFormContainer').style.display = 'none';

    // 2. SEGUNDO: Chame a inicialização do formulário
    // O timeout garante que o navegador processou as mudanças de CSS (display)
    setTimeout(() => {
        window.initCardForm(service, publicKey);
    }, 100); // 100ms é um valor seguro e imperceptível
}

// Exemplo de uso:
// const serviceData = { price: 150.00, title: "Meu Serviço" };
// const mpPublicKey = 'SUA_PUBLIC_KEY_DE_TESTE';
// openCheckoutModal(serviceData, mpPublicKey);