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
        const performanceCookies = document.getElementById('performanceCookies').checked;
        const marketingCookies = document.getElementById('marketingCookies').checked;

        this.setCookie('performanceCookies', performanceCookies.toString());
        this.setCookie('marketingCookies', marketingCookies.toString());
        this.setCookie('cookie-consent', 'accepted');

        // Close modals
        const modal = bootstrap.Modal.getInstance(this.cookieSettingsModal);
        if (modal) {
            modal.hide();
        }
        this.hideConsent();

        // Reload page to apply new settings
        window.location.reload();
    }
}

// Funções globais para uso nos botões
function acceptAllCookies() {
    const cookieManager = new CookieManager();
    cookieManager.setCookie('cookie-consent', 'accepted');
    cookieManager.setCookie('performanceCookies', 'true');
    cookieManager.setCookie('marketingCookies', 'true');
    cookieManager.hideConsent();
    window.location.reload();
}

function openCookieSettings() {
    const cookieSettingsModal = new bootstrap.Modal(document.getElementById('cookieSettingsModal'));
    cookieSettingsModal.show();
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.cookieManager = new CookieManager();
}); 