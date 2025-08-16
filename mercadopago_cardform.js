/**
 * MercadoPago CardForm - Inicialização Dinâmica
 * Compatível com renderização dinâmica e modais
 * Autor: HOZ TECH
 */

class MercadoPagoCardForm {
    constructor(publicKey, options = {}) {
        this.publicKey = publicKey;
        this.mp = null;
        this.cardForm = null;
        this.isInitialized = false;
        this.isMounted = false;
        this.retryAttempts = 0;
        this.maxRetries = 10;
        
        // Configurações padrão
        this.config = {
            autoMount: false,
            processingMode: 'aggregator',
            locale: 'pt-BR',
            ...options
        };
        
        // IDs dos campos HTML
        this.fieldIds = {
            cardNumber: 'cardNumber',
            cardExpirationDate: 'cardExpirationDate', 
            cardSecurityCode: 'cardSecurityCode',
            cardholderName: 'cardholderName',
            issuer: 'issuer',
            installments: 'installments',
            identificationType: 'identificationType',
            identificationNumber: 'identificationNumber'
        };
        
        this.init();
    }
    
    /**
     * Inicializa o MercadoPago SDK
     */
    async init() {
        try {
            console.log('🚀 Inicializando MercadoPago CardForm...');
            
            // Aguarda o carregamento do SDK
            await this.waitForMercadoPagoSDK();
            
            // Inicializa o MercadoPago
            this.mp = new MercadoPago(this.publicKey, {
                locale: this.config.locale
            });
            
            this.isInitialized = true;
            console.log('✅ MercadoPago SDK inicializado com sucesso');
            
            // Tenta montar o formulário se os campos já estiverem disponíveis
            this.tryMountForm();
            
        } catch (error) {
            console.error('❌ Erro ao inicializar MercadoPago:', error);
            throw error;
        }
    }
    
    /**
     * Aguarda o carregamento do SDK do MercadoPago
     */
    waitForMercadoPagoSDK() {
        return new Promise((resolve, reject) => {
            let attempts = 0;
            const maxAttempts = 50; // 5 segundos
            
            const checkSDK = () => {
                attempts++;
                
                if (typeof MercadoPago !== 'undefined') {
                    console.log('📦 MercadoPago SDK carregado');
                    resolve();
                } else if (attempts >= maxAttempts) {
                    reject(new Error('Timeout: MercadoPago SDK não foi carregado'));
                } else {
                    setTimeout(checkSDK, 100);
                }
            };
            
            checkSDK();
        });
    }
    
    /**
     * Verifica se todos os campos necessários estão no DOM
     */
    areFieldsAvailable() {
        const requiredFields = ['cardNumber', 'cardExpirationDate', 'cardSecurityCode'];
        
        for (const fieldId of requiredFields) {
            const element = document.getElementById(this.fieldIds[fieldId]);
            if (!element) {
                console.log(`⏳ Campo ${fieldId} não encontrado no DOM`);
                return false;
            }
        }
        
        console.log('✅ Todos os campos necessários estão disponíveis');
        return true;
    }
    
    /**
     * Tenta montar o formulário
     */
    async tryMountForm() {
        if (!this.isInitialized || this.isMounted) {
            return;
        }
        
        if (this.areFieldsAvailable()) {
            await this.mountForm();
        } else {
            // Reagenda tentativa
            this.retryAttempts++;
            if (this.retryAttempts < this.maxRetries) {
                console.log(`🔄 Tentativa ${this.retryAttempts}/${this.maxRetries} - Reagendando montagem...`);
                setTimeout(() => this.tryMountForm(), 500);
            } else {
                console.warn('⚠️ Máximo de tentativas atingido. Campos não encontrados.');
            }
        }
    }
    
    /**
     * Monta o formulário do cartão
     */
    async mountForm() {
        try {
            console.log('🔧 Montando CardForm...');
            
            // Configuração do CardForm
            const cardFormConfig = {
                amount: '100.00', // Valor padrão, será atualizado dinamicamente
                autoMount: this.config.autoMount,
                processingMode: this.config.processingMode,
                form: {
                    id: 'mercadopago-form',
                    cardNumber: {
                        id: this.fieldIds.cardNumber,
                        placeholder: 'Número do cartão'
                    },
                    expirationDate: {
                        id: this.fieldIds.cardExpirationDate,
                        placeholder: 'MM/AA'
                    },
                    securityCode: {
                        id: this.fieldIds.cardSecurityCode,
                        placeholder: 'CVV'
                    },
                    cardholderName: {
                        id: this.fieldIds.cardholderName,
                        placeholder: 'Nome do portador'
                    },
                    issuer: {
                        id: this.fieldIds.issuer,
                        placeholder: 'Banco emissor'
                    },
                    installments: {
                        id: this.fieldIds.installments,
                        placeholder: 'Parcelas'
                    },
                    identificationType: {
                        id: this.fieldIds.identificationType,
                        placeholder: 'Tipo de documento'
                    },
                    identificationNumber: {
                        id: this.fieldIds.identificationNumber,
                        placeholder: 'Número do documento'
                    }
                },
                callbacks: {
                    onFormMounted: (error) => this.onFormMounted(error),
                    onSubmit: (event) => this.onSubmit(event),
                    onFetching: (resource) => this.onFetching(resource),
                    onCardTokenReceived: (error, token) => this.onCardTokenReceived(error, token)
                }
            };
            
            // Cria o CardForm
            this.cardForm = this.mp.cardForm(cardFormConfig);
            
            // Monta o formulário
            await this.cardForm.mount();
            
        } catch (error) {
            console.error('❌ Erro ao montar CardForm:', error);
            throw error;
        }
    }
    
    /**
     * Callback executado quando o formulário é montado
     */
    onFormMounted(error) {
        if (error) {
            console.error('❌ Erro ao montar formulário:', error);
            this.handleError('MOUNT_ERROR', error);
            return;
        }
        
        console.log('✅ CardForm montado com sucesso!');
        this.isMounted = true;
        
        // Dispara evento customizado
        this.dispatchEvent('cardFormMounted', {
            success: true,
            cardForm: this.cardForm
        });
    }
    
    /**
     * Callback executado no submit do formulário
     */
    onSubmit(event) {
        event.preventDefault();
        
        console.log('📤 Processando pagamento...');
        
        // Dispara evento customizado
        this.dispatchEvent('cardFormSubmit', {
            event: event,
            cardForm: this.cardForm
        });
        
        // Aqui você pode adicionar sua lógica de processamento
        this.processPayment();
    }
    
    /**
     * Callback executado durante o carregamento de recursos
     */
    onFetching(resource) {
        console.log('⏳ Carregando recurso:', resource);
        
        // Mostra loading se necessário
        this.showLoading(true);
    }
    
    /**
     * Callback executado quando o token do cartão é recebido
     */
    onCardTokenReceived(error, token) {
        this.showLoading(false);
        
        if (error) {
            console.error('❌ Erro ao obter token do cartão:', error);
            this.handleError('TOKEN_ERROR', error);
            return;
        }
        
        console.log('✅ Token do cartão recebido:', token);
        
        // Dispara evento customizado
        this.dispatchEvent('cardTokenReceived', {
            token: token,
            cardForm: this.cardForm
        });
    }
    
    /**
     * Processa o pagamento
     */
    async processPayment() {
        try {
            if (!this.cardForm) {
                throw new Error('CardForm não está montado');
            }
            
            // Obtém os dados do formulário
            const formData = await this.cardForm.getCardFormData();
            
            console.log('💳 Dados do cartão obtidos:', formData);
            
            // Aqui você implementa a lógica de envio para seu backend
            // Exemplo:
            // const response = await this.sendToBackend(formData);
            
            this.dispatchEvent('paymentProcessed', {
                success: true,
                data: formData
            });
            
        } catch (error) {
            console.error('❌ Erro ao processar pagamento:', error);
            this.handleError('PAYMENT_ERROR', error);
        }
    }
    
    /**
     * Atualiza o valor do pagamento
     */
    updateAmount(amount) {
        if (this.cardForm) {
            this.cardForm.update({ amount: amount.toString() });
            console.log('💰 Valor atualizado:', amount);
        }
    }
    
    /**
     * Mostra/esconde loading
     */
    showLoading(show) {
        const loadingElement = document.getElementById('mp-loading');
        if (loadingElement) {
            loadingElement.style.display = show ? 'block' : 'none';
        }
        
        // Dispara evento customizado
        this.dispatchEvent('loadingStateChanged', { loading: show });
    }
    
    /**
     * Trata erros
     */
    handleError(type, error) {
        const errorInfo = {
            type: type,
            message: error.message || error,
            details: error
        };
        
        console.error(`❌ Erro ${type}:`, errorInfo);
        
        // Dispara evento customizado
        this.dispatchEvent('cardFormError', errorInfo);
        
        // Mostra mensagem de erro para o usuário
        this.showErrorMessage(errorInfo);
    }
    
    /**
     * Mostra mensagem de erro
     */
    showErrorMessage(errorInfo) {
        const errorContainer = document.getElementById('mp-error-container');
        if (errorContainer) {
            errorContainer.innerHTML = `
                <div class="alert alert-danger">
                    <strong>Erro:</strong> ${errorInfo.message}
                </div>
            `;
            errorContainer.style.display = 'block';
        }
    }
    
    /**
     * Limpa mensagens de erro
     */
    clearErrors() {
        const errorContainer = document.getElementById('mp-error-container');
        if (errorContainer) {
            errorContainer.innerHTML = '';
            errorContainer.style.display = 'none';
        }
    }
    
    /**
     * Dispara eventos customizados
     */
    dispatchEvent(eventName, detail) {
        const event = new CustomEvent(`mp:${eventName}`, {
            detail: detail,
            bubbles: true
        });
        document.dispatchEvent(event);
    }
    
    /**
     * Destrói o CardForm
     */
    destroy() {
        if (this.cardForm) {
            this.cardForm.unmount();
            this.cardForm = null;
        }
        
        this.isMounted = false;
        this.retryAttempts = 0;
        
        console.log('🗑️ CardForm destruído');
    }
    
    /**
     * Remonta o formulário (útil para modais)
     */
    async remount() {
        console.log('🔄 Remontando CardForm...');
        
        this.destroy();
        this.retryAttempts = 0;
        
        // Aguarda um pouco antes de tentar remontar
        setTimeout(() => {
            this.tryMountForm();
        }, 100);
    }
}

// Função de inicialização global
window.initMercadoPagoCardForm = function(publicKey, options = {}) {
    console.log('🎯 Inicializando MercadoPago CardForm Global...');
    
    if (!publicKey) {
        console.error('❌ Chave pública do MercadoPago é obrigatória');
        return null;
    }
    
    return new MercadoPagoCardForm(publicKey, options);
};

// Observer para detectar mudanças no DOM (útil para SPAs)
window.observeMercadoPagoFields = function(cardFormInstance) {
    if (!cardFormInstance) return;
    
    const observer = new MutationObserver((mutations) => {
        let shouldRemount = false;
        
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList') {
                // Verifica se algum campo foi adicionado
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // Element node
                        const hasCardFields = node.querySelector && (
                            node.querySelector('#cardNumber') ||
                            node.querySelector('#cardExpirationDate') ||
                            node.querySelector('#cardSecurityCode')
                        );
                        
                        if (hasCardFields) {
                            shouldRemount = true;
                        }
                    }
                });
            }
        });
        
        if (shouldRemount && !cardFormInstance.isMounted) {
            console.log('🔍 Campos detectados no DOM, remontando...');
            cardFormInstance.remount();
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    return observer;
};

// Exemplo de uso:
/*
// Inicialização básica
const cardForm = initMercadoPagoCardForm('YOUR_PUBLIC_KEY');

// Com opções customizadas
const cardForm = initMercadoPagoCardForm('YOUR_PUBLIC_KEY', {
    processingMode: 'aggregator',
    locale: 'pt-BR'
});

// Observar mudanças no DOM
const observer = observeMercadoPagoFields(cardForm);

// Escutar eventos
document.addEventListener('mp:cardFormMounted', (event) => {
    console.log('Formulário montado!', event.detail);
});

document.addEventListener('mp:cardTokenReceived', (event) => {
    console.log('Token recebido!', event.detail.token);
});

document.addEventListener('mp:cardFormError', (event) => {
    console.error('Erro no formulário:', event.detail);
});

// Para modais, chame remount() quando o modal abrir
$('#myModal').on('shown.bs.modal', function() {
    cardForm.remount();
});
*/