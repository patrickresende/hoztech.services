// Gerenciador do Formulário de Contato
class ContactForm {
    constructor() {
        this.form = document.querySelector('#contactForm');
        this.submitButton = this.form ? this.form.querySelector('button[type="submit"]') : null;
        this.isAutoFilling = false;
        this.init();
    }

    init() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
            this.setupInputValidation();
            this.setupCharacterCounters();
            this.setupPhoneMask();
            this.setupNameFormat();
            this.setupEmailFormat();
            this.setupAutoFillDetection();
        }
    }

    setupAutoFillDetection() {
        // Detecta autopreenchimento
        const inputs = this.form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('animationstart', (e) => {
                if (e.animationName === 'onAutoFillStart') {
                    this.isAutoFilling = true;
                    this.validateInput(input);
                }
            });
            input.addEventListener('animationend', (e) => {
                if (e.animationName === 'onAutoFillEnd') {
                    this.isAutoFilling = false;
                    this.validateInput(input);
                }
            });
        });
    }

    setupInputValidation() {
        const inputs = this.form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            // Adiciona delay na validação para evitar conflitos com autopreenchimento
            let validationTimeout;
            input.addEventListener('input', () => {
                clearTimeout(validationTimeout);
                validationTimeout = setTimeout(() => {
                    if (!this.isAutoFilling) {
                        this.validateInput(input);
                    }
                }, 300);
            });
            
            input.addEventListener('blur', () => {
                if (!this.isAutoFilling) {
                    this.validateInput(input);
                }
            });
            
            input.addEventListener('paste', (e) => this.handlePaste(e, input));
        });
    }

    setupNameFormat() {
        const nameInput = this.form.querySelector('#name');
        if (nameInput) {
            let isUserInput = true;
            nameInput.addEventListener('input', (e) => {
                if (isUserInput && !this.isAutoFilling) {
                    let value = e.target.value.replace(/[^A-Za-zÀ-ÿ\s]/g, '');
                    value = value.replace(/\s+/g, ' ').trim();
                    value = value.substring(0, 50);
                    e.target.value = value;
                }
            });
            
            // Detecta mudanças programáticas
            const observer = new MutationObserver(() => {
                isUserInput = false;
                setTimeout(() => {
                    isUserInput = true;
                }, 100);
            });
            observer.observe(nameInput, { attributes: true });
        }
    }

    setupEmailFormat() {
        const emailInput = this.form.querySelector('#email');
        if (emailInput) {
            let isUserInput = true;
            emailInput.addEventListener('input', (e) => {
                if (isUserInput && !this.isAutoFilling) {
                    e.target.value = e.target.value.toLowerCase();
                }
            });
            
            // Detecta mudanças programáticas
            const observer = new MutationObserver(() => {
                isUserInput = false;
                setTimeout(() => {
                    isUserInput = true;
                }, 100);
            });
            observer.observe(emailInput, { attributes: true });
        }
    }

    setupPhoneMask() {
        const phoneInput = this.form.querySelector('#phone');
        if (phoneInput) {
            let isUserInput = true;
            phoneInput.addEventListener('input', (e) => {
                if (isUserInput && !this.isAutoFilling) {
                    let value = e.target.value.replace(/\D/g, '');
                    if (value.length <= 11) {
                        if (value.length > 2) {
                            value = `(${value.substring(0, 2)}) ${value.substring(2)}`;
                        }
                        if (value.length > 9) {
                            value = `${value.substring(0, 10)}-${value.substring(10)}`;
                        }
                        e.target.value = value;
                    }
                }
            });

            // Validação de DDD com delay
            let dddTimeout;
            phoneInput.addEventListener('blur', (e) => {
                clearTimeout(dddTimeout);
                dddTimeout = setTimeout(() => {
                    if (!this.isAutoFilling) {
                        const ddd = e.target.value.match(/\((\d{2})\)/);
                        if (ddd) {
                            const dddNum = parseInt(ddd[1]);
                            if (dddNum < 11 || dddNum > 99) {
                                this.showError(phoneInput, 'DDD inválido');
                            }
                        }
                    }
                }, 300);
            });
            
            // Detecta mudanças programáticas
            const observer = new MutationObserver(() => {
                isUserInput = false;
                setTimeout(() => {
                    isUserInput = true;
                }, 100);
            });
            observer.observe(phoneInput, { attributes: true });
        }
    }

    handlePaste(e, input) {
        e.preventDefault();
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        
        switch(input.name) {
            case 'name':
                const cleanName = pastedText.replace(/[^A-Za-zÀ-ÿ\s]/g, '').trim();
                input.value = cleanName.substring(0, 50);
                break;
            case 'email':
                input.value = pastedText.toLowerCase();
                break;
            case 'phone':
                const digits = pastedText.replace(/\D/g, '');
                if (digits.length <= 11) {
                    let formatted = digits;
                    if (digits.length > 2) {
                        formatted = `(${digits.substring(0, 2)}) ${digits.substring(2)}`;
                    }
                    if (digits.length > 9) {
                        formatted = `${formatted.substring(0, 10)}-${formatted.substring(10)}`;
                    }
                    input.value = formatted;
                }
                break;
            default:
                input.value = pastedText;
        }
        
        // Delay na validação após colar
        setTimeout(() => {
            this.validateInput(input);
        }, 100);
    }

    validateInput(input) {
        const value = input.value.trim();
        let errorMessage = '';

        if (!value) {
            errorMessage = 'Este campo é obrigatório';
        } else {
            switch(input.name) {
                case 'name':
                    if (value.length < 3) {
                        errorMessage = 'O nome deve ter pelo menos 3 caracteres';
                    } else if (value.length > 50) {
                        errorMessage = 'O nome deve ter no máximo 50 caracteres';
                    } else if (!/^[A-Za-zÀ-ÿ\s]+$/.test(value)) {
                        errorMessage = 'O nome deve conter apenas letras e espaços';
                    }
                    break;

                case 'email':
                    if (!this.isValidEmail(value)) {
                        errorMessage = 'Por favor, insira um email válido';
                    }
                    break;

                case 'phone':
                    if (!this.isValidPhone(value)) {
                        errorMessage = 'Telefone inválido. Use o formato: (99) 99999-9999 ou (99) 9999-9999';
                    }
                    break;

                case 'subject':
                    if (value.length > 50) {
                        errorMessage = 'O assunto deve ter no máximo 50 caracteres';
                    }
                    break;

                case 'message':
                    if (value.length < 10) {
                        errorMessage = 'A mensagem deve ter pelo menos 10 caracteres';
                    } else if (value.length > 5000) {
                        errorMessage = 'A mensagem deve ter no máximo 5000 caracteres';
                    }
                    break;
            }
        }

        if (errorMessage) {
            this.showError(input, errorMessage);
            return false;
        }

        this.hideError(input);
        return true;
    }

    isValidEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }

    isValidPhone(phone) {
        const digits = phone.replace(/\D/g, '');
        if (digits.length !== 10 && digits.length !== 11) {
            return false;
        }
        const ddd = parseInt(digits.substring(0, 2));
        return ddd >= 11 && ddd <= 99;
    }

    showError(input, message) {
        input.classList.add('is-invalid');
        const errorElement = input.nextElementSibling;
        if (errorElement && errorElement.classList.contains('invalid-feedback')) {
            errorElement.textContent = message;
        }
    }

    hideError(input) {
        input.classList.remove('is-invalid');
        const errorElement = input.nextElementSibling;
        if (errorElement && errorElement.classList.contains('invalid-feedback')) {
            errorElement.textContent = '';
        }
    }

    async handleSubmit(e) {
        e.preventDefault();

        if (!this.validateForm()) {
            this.showToast('Preencha corretamente todos os campos obrigatórios.', 'danger');
            return;
        }

        this.setLoadingState(true);

        const formData = new FormData(this.form);
        
        // Limpa o campo honeypot antes do envio
        formData.set('website', '');

        try {
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            const data = await response.json();

            if (response.ok) {
                this.form.reset();
                this.showToast('Mensagem enviada com sucesso!', 'success');
                this.updateCharacterCounters();
                // Limpa o campo honeypot após o envio
                const websiteInput = this.form.querySelector('#website');
                if (websiteInput) {
                    websiteInput.value = '';
                }
            } else {
                if (data.errors) {
                    Object.entries(data.errors).forEach(([field, errors]) => {
                        const input = this.form.querySelector(`[name="${field}"]`);
                        if (input) {
                            this.showError(input, errors[0]);
                        }
                    });
                } else {
                    this.showToast(data.message || 'Erro ao enviar mensagem. Por favor, tente novamente.', 'danger');
                }
            }
        } catch (error) {
            console.error('Erro:', error);
            this.showToast('Erro ao enviar mensagem. Por favor, tente novamente.', 'danger');
        } finally {
            this.setLoadingState(false);
        }
    }

    updateCharacterCounters() {
        const subjectInput = this.form.querySelector('#subject');
        const messageInput = this.form.querySelector('#message');
        const websiteInput = this.form.querySelector('#website');
        
        if (subjectInput) {
            const subjectCounter = subjectInput.parentNode.querySelector('.text-muted');
            if (subjectCounter) {
                subjectCounter.textContent = '0/50 caracteres';
                subjectCounter.style.color = 'rgba(224, 251, 252, 0.7)';
            }
        }
        
        if (messageInput) {
            const messageCounter = messageInput.parentNode.querySelector('.text-muted');
            if (messageCounter) {
                messageCounter.textContent = '0/5000 caracteres';
                messageCounter.style.color = 'rgba(224, 251, 252, 0.7)';
            }
        }

        // Limpa o campo honeypot
        if (websiteInput) {
            websiteInput.value = '';
        }
    }

    validateForm() {
        const inputs = this.form.querySelectorAll('input, textarea');
        let isValid = true;

        inputs.forEach(input => {
            if (input.name !== 'website' && !this.validateInput(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    setLoadingState(loading) {
        if (this.submitButton) {
            this.submitButton.disabled = loading;
            this.submitButton.innerHTML = loading ?
                '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...' :
                'Enviar Mensagem';
        }
    }

    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='));
        return cookieValue ? cookieValue.split('=')[1] : '';
    }

    showToast(message, type = 'danger') {
        this.clearAlerts();

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0 show position-fixed top-0 end-0 m-3`;
        toast.role = 'alert';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    clearAlerts() {
        const existingToasts = document.querySelectorAll('.toast');
        existingToasts.forEach(toast => toast.remove());
    }
}

// Inicializar o gerenciador do formulário quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new ContactForm();
});
