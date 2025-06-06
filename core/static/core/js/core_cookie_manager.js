// Gerenciador de Cookies
class CookieManager {
    constructor() {
        this.cookieBanner = document.querySelector('.cookie-banner');
        this.acceptButton = document.querySelector('#accept-cookies');
        this.rejectButton = document.querySelector('#reject-cookies');
        this.init();
    }

    init() {
        if (!this.getCookie('cookie-consent')) {
            this.showBanner();
        }

        if (this.acceptButton) {
            this.acceptButton.addEventListener('click', () => this.acceptCookies());
        }

        if (this.rejectButton) {
            this.rejectButton.addEventListener('click', () => this.rejectCookies());
        }
    }

    showBanner() {
        if (this.cookieBanner) {
            this.cookieBanner.classList.add('show');
        }
    }

    hideBanner() {
        if (this.cookieBanner) {
            this.cookieBanner.classList.remove('show');
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

    acceptCookies() {
        this.setCookie('cookie-consent', 'accepted');
        this.hideBanner();
        // Aqui você pode adicionar código para ativar scripts de análise
    }

    rejectCookies() {
        this.setCookie('cookie-consent', 'rejected');
        this.hideBanner();
        // Aqui você pode adicionar código para desativar scripts de análise
    }
}

// Inicializar o gerenciador de cookies quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new CookieManager();
}); 