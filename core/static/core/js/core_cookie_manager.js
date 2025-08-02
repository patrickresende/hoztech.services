// Gerenciador de Cookies
class CookieManager {
    constructor() {
        this.cookieConsent = document.getElementById('cookieConsent');
        this.cookieSettingsModal = document.getElementById('cookieSettingsModal');
        this.cookiePolicyModal = document.getElementById('cookiePolicyModal');
        this.saveCookieSettings = document.getElementById('saveCookieSettings');
        this.init();
    }

    init() {
        if (!this.getCookie('cookie-consent')) {
            this.showConsent();
        }

        // Event Listeners
        if (this.saveCookieSettings) {
            this.saveCookieSettings.addEventListener('click', () => this.saveSettings());
        }

        // Initialize cookie settings
        this.initializeCookieSettings();
    }

    showConsent() {
        if (this.cookieConsent) {
            this.cookieConsent.classList.add('active');
        }
    }

    hideConsent() {
        if (this.cookieConsent) {
            this.cookieConsent.classList.remove('active');
        }
    }

    setCookie(name, value, days = 365) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/;SameSite=Lax`;
    }

    getCookie(name) {
        const nameEQ = `${name}=`;
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1, c.length);
            }
            if (c.indexOf(nameEQ) === 0) {
                return c.substring(nameEQ.length, c.length);
            }
        }
        return null;
    }

    initializeCookieSettings() {
        // Set default values if not already set
        if (!this.getCookie('performanceCookies')) {
            this.setCookie('performanceCookies', 'false');
        }
        if (!this.getCookie('marketingCookies')) {
            this.setCookie('marketingCookies', 'false');
        }

        // Update UI to reflect current settings
        const performanceCheckbox = document.getElementById('performanceCookies');
        const marketingCheckbox = document.getElementById('marketingCookies');

        if (performanceCheckbox) {
            performanceCheckbox.checked = this.getCookie('performanceCookies') === 'true';
        }
        if (marketingCheckbox) {
            marketingCheckbox.checked = this.getCookie('marketingCookies') === 'true';
        }
    }

    saveSettings() {
        const performanceCheckbox = document.getElementById('performanceCookies');
        const marketingCheckbox = document.getElementById('marketingCookies');

        if (performanceCheckbox && marketingCheckbox) {
            const performanceCookies = performanceCheckbox.checked;
            const marketingCookies = marketingCheckbox.checked;

            this.setCookie('performanceCookies', performanceCookies.toString());
            this.setCookie('marketingCookies', marketingCookies.toString());
            this.setCookie('cookie-consent', 'accepted');

            // Close modals
            if (this.cookieSettingsModal) {
                const modal = bootstrap.Modal.getInstance(this.cookieSettingsModal);
                if (modal) {
                    modal.hide();
                }
            }
            this.hideConsent();

            // Mostrar confirmação sem reload
            this.showSaveConfirmation();
        }
    }

    showSaveConfirmation() {
        // Criar notificação de confirmação
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            z-index: 99999;
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        notification.textContent = 'Configurações de cookies salvas com sucesso!';
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }
}

// Funções globais para uso nos botões
function acceptAllCookies() {
    if (window.cookieManager) {
        window.cookieManager.setCookie('cookie-consent', 'accepted');
        window.cookieManager.setCookie('performanceCookies', 'true');
        window.cookieManager.setCookie('marketingCookies', 'true');
        window.cookieManager.hideConsent();
        window.cookieManager.showSaveConfirmation();
    }
}

function openCookieSettings() {
    const cookieSettingsModal = new bootstrap.Modal(document.getElementById('cookieSettingsModal'));
    cookieSettingsModal.show();
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.cookieManager = new CookieManager();
    
    // Signal script loaded to system
    if (window.HOZ_SYSTEM) {
        window.HOZ_SYSTEM.scriptsLoaded++;
        console.log('🍪 CookieManager carregado, scripts:', window.HOZ_SYSTEM.scriptsLoaded);
    }
}); 