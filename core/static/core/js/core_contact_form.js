// Gerenciador do Formulário de Contato
class ContactForm {
    constructor() {
        this.form = document.querySelector('#contactForm');
        this.submitButton = this.form ? this.form.querySelector('button[type="submit"]') : null;
        this.isAutoFilling = false;
        this.validationTimeout = null;
        this.init();
    }

    init() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
            this.setupInputValidation();
            this.setupPhoneInput();
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
            input.addEventListener('input', () => {
                clearTimeout(this.validationTimeout);
                this.validationTimeout = setTimeout(() => {
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
                    // Converter para maiúsculas
                    value = value.toUpperCase();
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
                    let value = e.target.value.toLowerCase();
                    // Limitar a 60 caracteres
                    value = value.substring(0, 60);
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
            observer.observe(emailInput, { attributes: true });
        }
    }

    setupPhoneInput() {
        const phoneInput = this.form.querySelector('#phone');
        if (phoneInput) {
            let isUserInput = true;
            phoneInput.addEventListener('input', (e) => {
                if (isUserInput && !this.isAutoFilling) {
                    // Permitir apenas números
                    let value = e.target.value.replace(/\D/g, '');
                    // Limitar a 15 dígitos
                    value = value.substring(0, 15);
                    e.target.value = value;
                }
            });

            // Validação de DDD com delay
            let dddTimeout;
            phoneInput.addEventListener('blur', (e) => {
                clearTimeout(dddTimeout);
                dddTimeout = setTimeout(() => {
                    if (!this.isAutoFilling) {
                        const digits = e.target.value.replace(/\D/g, '');
                        if (digits.length >= 2) {
                            const dddNum = parseInt(digits.substring(0, 2));
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
                input.value = cleanName.substring(0, 50).toUpperCase();
                break;
            case 'email':
                input.value = pastedText.toLowerCase().substring(0, 60);
                break;
            case 'phone':
                const digits = pastedText.replace(/\D/g, '');
                input.value = digits.substring(0, 15);
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
                    if (value.length > 60) {
                        errorMessage = 'O email deve ter no máximo 60 caracteres';
                    } else if (!this.isValidEmail(value)) {
                        errorMessage = 'Por favor, insira um email válido';
                    }
                    break;

                case 'phone':
                    const digits = value.replace(/\D/g, '');
                    if (digits.length < 8) {
                        errorMessage = 'O telefone deve ter pelo menos 8 dígitos';
                    } else if (digits.length > 15) {
                        errorMessage = 'O telefone deve ter no máximo 15 dígitos';
                    } else if (digits.length >= 2) {
                        const dddNum = parseInt(digits.substring(0, 2));
                        if (dddNum < 11 || dddNum > 99) {
                            errorMessage = 'DDD inválido';
                        }
                    }
                    break;

                case 'subject':
                    if (value.length > 50) {
                        errorMessage = 'O assunto deve ter no máximo 50 caracteres';
                    } else if (this.containsSuspiciousContent(value)) {
                        errorMessage = 'O assunto contém conteúdo suspeito';
                    }
                    break;

                case 'message':
                    if (value.length < 50) {
                        errorMessage = 'A mensagem deve ter pelo menos 50 caracteres';
                    } else if (value.length > 5000) {
                        errorMessage = 'A mensagem deve ter no máximo 5000 caracteres';
                    } else if (this.containsSuspiciousContent(value)) {
                        errorMessage = 'A mensagem contém conteúdo suspeito';
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

    containsSuspiciousContent(text) {
        const suspiciousPatterns = [
            /<script/i,
            /javascript:/i,
            /on\w+\s*=/i,
            /data:/i,
            /http[s]?:\/\//i,
            /www\./i,
            /\.com/i,
            /\.br/i,
            /\.org/i,
            /\.net/i,
            /\.io/i,
            /\.co/i,
            /\.me/i,
            /\.tv/i,
            /\.info/i,
            /\.biz/i,
            /\.cc/i,
            /\.tk/i,
            /\.ml/i,
            /\.ga/i,
            /\.cf/i,
            /\.gq/i,
            /\.xyz/i,
            /\.top/i,
            /\.club/i,
            /\.online/i,
            /\.site/i,
            /\.web/i,
            /\.app/i,
            /\.dev/i,
            /\.tech/i,
            /\.digital/i,
            /\.cloud/i,
            /\.ai/i,
            /\.ly/i,
            /\.bit/i,
            /\.goo/i,
            /\.gl/i,
            /\.tiny/i,
            /\.url/i,
            /\.short/i,
            /\.link/i,
            /\.click/i,
            /\.to/i,
            /\.at/i,
            /\.by/i,
            /\.is/i,
            /\.it/i,
            /\.in/i,
            /\.on/i,
            /\.up/i,
            /\.down/i,
            /\.out/i,
            /\.off/i,
            /\.over/i,
            /\.under/i,
            /\.back/i,
            /\.forward/i,
            /\.next/i,
            /\.prev/i,
            /\.first/i,
            /\.last/i,
            /\.new/i,
            /\.old/i,
            /\.good/i,
            /\.bad/i,
            /\.best/i,
            /\.worst/i,
            /\.big/i,
            /\.small/i,
            /\.high/i,
            /\.low/i,
            /\.fast/i,
            /\.slow/i,
            /\.hot/i,
            /\.cold/i,
            /\.warm/i,
            /\.cool/i,
            /\.soft/i,
            /\.hard/i,
            /\.easy/i,
            /\.simple/i,
            /\.complex/i,
            /\.basic/i,
            /\.advanced/i,
            /\.pro/i,
            /\.premium/i,
            /\.vip/i,
            /\.exclusive/i,
            /\.limited/i,
            /\.special/i,
            /\.unique/i,
            /\.rare/i,
            /\.common/i,
            /\.popular/i,
            /\.trending/i,
            /\.viral/i,
            /\.famous/i,
            /\.known/i,
            /\.unknown/i,
            /\.hidden/i,
            /\.visible/i,
            /\.public/i,
            /\.private/i,
            /\.secret/i,
            /\.open/i,
            /\.closed/i,
            /\.locked/i,
            /\.unlocked/i,
            /\.secure/i,
            /\.safe/i,
            /\.dangerous/i,
            /\.risky/i,
            /\.careful/i,
            /\.careless/i,
            /\.smart/i,
            /\.stupid/i,
            /\.clever/i,
            /\.dumb/i,
            /\.wise/i,
            /\.foolish/i,
            /\.genius/i,
            /\.idiot/i,
            /\.expert/i,
            /\.amateur/i,
            /\.professional/i,
            /\.beginner/i,
            /\.master/i,
            /\.student/i,
            /\.teacher/i,
            /\.leader/i,
            /\.follower/i,
            /\.boss/i,
            /\.employee/i,
            /\.manager/i,
            /\.worker/i,
            /\.director/i,
            /\.assistant/i,
            /\.helper/i,
            /\.supporter/i,
            /\.partner/i,
            /\.friend/i,
            /\.enemy/i,
            /\.ally/i,
            /\.rival/i,
            /\.competitor/i,
            /\.opponent/i,
            /\.challenger/i,
            /\.defender/i,
            /\.attacker/i,
            /\.winner/i,
            /\.loser/i,
            /\.champion/i,
            /\.hero/i,
            /\.villain/i,
            /\.savior/i,
            /\.destroyer/i,
            /\.creator/i,
            /\.builder/i,
            /\.breaker/i,
            /\.fixer/i,
            /\.damager/i,
            /\.healer/i,
            /\.killer/i,
            /\.protector/i,
            /\.guardian/i,
            /\.warrior/i,
            /\.fighter/i,
            /\.soldier/i,
            /\.commander/i,
            /\.general/i,
            /\.captain/i,
            /\.lieutenant/i,
            /\.sergeant/i,
            /\.private/i,
            /\.officer/i,
            /\.agent/i,
            /\.spy/i,
            /\.detective/i,
            /\.investigator/i,
            /\.researcher/i,
            /\.scientist/i,
            /\.engineer/i,
            /\.developer/i,
            /\.programmer/i,
            /\.coder/i,
            /\.hacker/i,
            /\.cracker/i,
            /\.phisher/i,
            /\.spammer/i,
            /\.scammer/i,
            /\.fraudster/i,
            /\.thief/i,
            /\.robber/i,
            /\.burglar/i,
            /\.kidnapper/i,
            /\.murderer/i,
            /\.assassin/i,
            /\.hitman/i,
            /\.terrorist/i,
            /\.extremist/i,
            /\.radical/i,
            /\.fanatic/i,
            /\.zealot/i,
            /\.cultist/i,
            /\.worshipper/i,
            /\.believer/i,
            /\.skeptic/i,
            /\.cynic/i,
            /\.optimist/i,
            /\.pessimist/i,
            /\.realist/i,
            /\.idealist/i,
            /\.pragmatist/i,
            /\.theorist/i,
            /\.practitioner/i,
            /\.academic/i,
            /\.scholar/i,
            /\.intellectual/i,
            /\.philosopher/i,
            /\.thinker/i,
            /\.dreamer/i,
            /\.visionary/i,
            /\.prophet/i,
            /\.oracle/i,
            /\.seer/i,
            /\.psychic/i,
            /\.medium/i,
            /\.shaman/i,
            /\.witch/i,
            /\.wizard/i,
            /\.magician/i,
            /\.sorcerer/i,
            /\.warlock/i,
            /\.necromancer/i,
            /\.summoner/i,
            /\.conjurer/i,
            /\.enchanter/i,
            /\.illusionist/i,
            /\.transmuter/i,
            /\.evoker/i,
            /\.abjurer/i,
            /\.diviner/i
        ];
        
        return suspiciousPatterns.some(pattern => pattern.test(text));
    }

    isValidEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
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

        // Criar modal de sucesso mais visível
        if (type === 'success') {
            this.showSuccessModal(message);
        } else {
            // Toast para erros
            const toast = document.createElement('div');
            toast.className = `toast align-items-center text-white bg-${type} border-0 show position-fixed top-0 end-0 m-3`;
            toast.role = 'alert';
            toast.style.zIndex = '9999';
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
    }

    showSuccessModal(message) {
        // Detectar Brave browser
        const isBrave = navigator.brave && navigator.brave.isBrave;
        
        if (isBrave) {
            // Fallback para Brave: usar notificação nativa do browser
            this.showBraveCompatibleSuccess(message);
        } else {
            // Modal normal para outros browsers
            this.showNormalModal(message);
        }
    }

    showBraveCompatibleSuccess(message) {
        // Criar overlay simples sem elementos que o Brave pode bloquear
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: Arial, sans-serif;
        `;

        const successBox = document.createElement('div');
        successBox.style.cssText = `
            background: white;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            max-width: 400px;
            margin: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        `;

        successBox.innerHTML = `
            <div style="color: #28a745; font-size: 60px; margin-bottom: 20px;">✓</div>
            <h2 style="color: #333; margin-bottom: 15px;">Mensagem Enviada!</h2>
            <p style="color: #666; margin-bottom: 25px;">${message}</p>
            <p style="color: #999; font-size: 14px; margin-bottom: 25px;">Entraremos em contato em breve.</p>
            <button onclick="this.closest('div[style*=\"position: fixed\"]').remove(); document.body.style.overflow = 'auto';" 
                    style="background: #28a745; color: white; border: none; padding: 12px 30px; border-radius: 5px; cursor: pointer; font-size: 16px;">
                OK
            </button>
        `;

        overlay.appendChild(successBox);
        document.body.appendChild(overlay);
        document.body.style.overflow = 'hidden';

        // Auto-remover após 10 segundos
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.remove();
                document.body.style.overflow = 'auto';
            }
        }, 10000);
    }

    showNormalModal(message) {
        // Criar modal de sucesso
        const modal = document.createElement('div');
        modal.className = 'modal fade show';
        modal.style.display = 'block';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        modal.style.zIndex = '9999';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content" style="background: linear-gradient(135deg, #00f7ff, #ff073a); border: none; color: white;">
                    <div class="modal-header border-0">
                        <h5 class="modal-title">
                            <i class="bi bi-check-circle-fill me-2" style="color: #28a745;"></i>
                            Sucesso!
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <div class="mb-3">
                            <i class="bi bi-envelope-check" style="font-size: 3rem; color: #28a745;"></i>
                        </div>
                        <h4 class="mb-3">Mensagem Enviada!</h4>
                        <p class="mb-0">${message}</p>
                        <p class="small mt-2">Entraremos em contato em breve.</p>
                    </div>
                    <div class="modal-footer border-0 justify-content-center">
                        <button type="button" class="btn btn-light" onclick="this.closest('.modal').remove(); document.body.style.overflow = 'auto';">
                            <i class="bi bi-check me-2"></i>OK
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';

        // Auto-remover após 8 segundos
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
                document.body.style.overflow = 'auto';
            }
        }, 8000);

        // Adicionar efeito de confete
        this.createConfetti();
    }

    createConfetti() {
        // Criar efeito de confete
        const colors = ['#00f7ff', '#ff073a', '#28a745', '#ffc107', '#17a2b8'];
        
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.style.position = 'fixed';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.top = '-10px';
                confetti.style.width = '10px';
                confetti.style.height = '10px';
                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.borderRadius = '50%';
                confetti.style.pointerEvents = 'none';
                confetti.style.zIndex = '9998';
                confetti.style.animation = 'confetti-fall 3s linear forwards';
                
                document.body.appendChild(confetti);
                
                setTimeout(() => {
                    if (confetti.parentNode) {
                        confetti.remove();
                    }
                }, 3000);
            }, i * 100);
        }

        // Adicionar CSS para animação
        if (!document.getElementById('confetti-css')) {
            const style = document.createElement('style');
            style.id = 'confetti-css';
            style.textContent = `
                @keyframes confetti-fall {
                    to {
                        transform: translateY(100vh) rotate(360deg);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    clearAlerts() {
        const existingToasts = document.querySelectorAll('.toast');
        existingToasts.forEach(toast => toast.remove());
        
        // Limpar modais também
        const existingModals = document.querySelectorAll('.modal');
        existingModals.forEach(modal => modal.remove());
        
        // Restaurar overflow do body
        document.body.style.overflow = 'auto';
    }
}

// Inicializar o gerenciador do formulário quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new ContactForm();
    
    // Signal script loaded to system
    if (window.HOZ_SYSTEM) {
        window.HOZ_SYSTEM.scriptsLoaded++;
        console.log('📧 ContactForm carregado, scripts:', window.HOZ_SYSTEM.scriptsLoaded);
    }
});
