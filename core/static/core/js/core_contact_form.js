// Gerenciador do Formulário de Contato
class ContactForm {
    constructor() {
        this.form = document.querySelector('#contact-form');
        this.submitButton = this.form ? this.form.querySelector('button[type="submit"]') : null;
        this.init();
    }

    init() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
            this.setupInputValidation();
        }
    }

    setupInputValidation() {
        const inputs = this.form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', () => this.validateInput(input));
            input.addEventListener('blur', () => this.validateInput(input));
        });
    }

    validateInput(input) {
        const value = input.value.trim();
        const errorElement = input.nextElementSibling;
        
        if (!value) {
            this.showError(input, 'Este campo é obrigatório');
            return false;
        }

        if (input.type === 'email' && !this.isValidEmail(value)) {
            this.showError(input, 'Por favor, insira um email válido');
            return false;
        }

        this.hideError(input);
        return true;
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
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
            return;
        }

        this.setLoadingState(true);

        const formData = new FormData(this.form);
        
        try {
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (!response.ok) {
                throw new Error('Erro ao enviar formulário');
            }

            const data = await response.json();
            this.showSuccess('Mensagem enviada com sucesso!');
            this.form.reset();

        } catch (error) {
            this.showError(this.form, 'Erro ao enviar mensagem. Por favor, tente novamente.');
            console.error('Erro:', error);
        } finally {
            this.setLoadingState(false);
        }
    }

    validateForm() {
        const inputs = this.form.querySelectorAll('input, textarea');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateInput(input)) {
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

    showSuccess(message) {
        const alertElement = document.createElement('div');
        alertElement.className = 'alert alert-success mt-3';
        alertElement.role = 'alert';
        alertElement.textContent = message;

        this.form.insertAdjacentElement('beforebegin', alertElement);

        setTimeout(() => {
            alertElement.remove();
        }, 5000);
    }
}

// Inicializar o gerenciador do formulário quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new ContactForm();
}); 