/**
 * Cookie Manager para Hoz Tech
 * Gerenciamento seguro de cookies com suporte a GDPR/LGPD
 * @version 2.0.0
 */

class CookieManager {
    constructor() {
        this.cookieConsent = 'hoz_cookie_consent';
        this.cookiePreferences = 'hoz_cookie_preferences';
        this.expireDays = 365;
        this.initialized = false;

        // Categorias de cookies
        this.categories = {
            necessary: {
                name: 'Necessários',
                description: 'Cookies essenciais para o funcionamento do site',
                required: true
            },
            analytics: {
                name: 'Análise',
                description: 'Cookies que nos ajudam a entender como você usa o site',
                required: false
            },
            marketing: {
                name: 'Marketing',
                description: 'Cookies usados para marketing direcionado',
                required: false
            }
        };

        this.init();
    }

    init() {
        if (this.initialized) return;
        this.initialized = true;

        if (!this.getCookie(this.cookieConsent)) {
            this.showBanner();
        }

        this.setupEventListeners();
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-cookie-accept-all]')) {
                this.acceptAll();
            } else if (e.target.matches('[data-cookie-accept-necessary]')) {
                this.acceptNecessary();
            } else if (e.target.matches('[data-cookie-settings]')) {
                this.showPreferences();
            }
        });
    }

    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    setCookie(name, value, days = this.expireDays) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/;SameSite=Strict;Secure`;
    }

    deleteCookie(name) {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
    }

    deleteAllCookies() {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const name = cookie.split('=')[0].trim();
            if (!name.startsWith('hoz_')) {
                this.deleteCookie(name);
            }
        }
    }

    showBanner() {
        const banner = document.createElement('div');
        banner.className = 'cookie-banner';
        banner.innerHTML = `
            <div class="cookie-content">
                <h3>🍪 Sua Privacidade</h3>
                <p>Utilizamos cookies para melhorar sua experiência. Escolha suas preferências de cookies:</p>
                <div class="cookie-buttons">
                    <button class="btn-primary" data-cookie-accept-all>Aceitar Todos</button>
                    <button class="btn-secondary" data-cookie-accept-necessary>Apenas Necessários</button>
                    <button class="btn-link" data-cookie-settings>Configurações</button>
                </div>
            </div>
        `;
        document.body.appendChild(banner);
    }

    showPreferences() {
        const modal = document.createElement('div');
        modal.className = 'cookie-modal';
        modal.innerHTML = `
            <div class="cookie-modal-content">
                <h3>Preferências de Cookies</h3>
                <div class="cookie-preferences">
                    ${Object.entries(this.categories).map(([key, category]) => `
                        <div class="cookie-category">
                            <label class="cookie-switch">
                                <input type="checkbox" 
                                    name="cookie-${key}" 
                                    ${category.required ? 'checked disabled' : ''}
                                    ${this.isAccepted(key) ? 'checked' : ''}>
                                <span class="switch-slider"></span>
                            </label>
                            <div class="category-info">
                                <h4>${category.name}</h4>
                                <p>${category.description}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="cookie-modal-buttons">
                    <button class="btn-primary" onclick="cookieManager.savePreferences()">Salvar Preferências</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    acceptAll() {
        this.setCookie(this.cookieConsent, 'true');
        const preferences = Object.keys(this.categories).reduce((acc, key) => {
            acc[key] = true;
            return acc;
        }, {});
        this.setCookie(this.cookiePreferences, JSON.stringify(preferences));
        this.hideBanner();
        this.applyPreferences(preferences);
    }

    acceptNecessary() {
        this.setCookie(this.cookieConsent, 'true');
        const preferences = Object.keys(this.categories).reduce((acc, key) => {
            acc[key] = this.categories[key].required;
            return acc;
        }, {});
        this.setCookie(this.cookiePreferences, JSON.stringify(preferences));
        this.hideBanner();
        this.applyPreferences(preferences);
    }

    savePreferences() {
        const preferences = {};
        Object.keys(this.categories).forEach(key => {
            const input = document.querySelector(`input[name="cookie-${key}"]`);
            preferences[key] = input ? input.checked : this.categories[key].required;
        });
        
        this.setCookie(this.cookieConsent, 'true');
        this.setCookie(this.cookiePreferences, JSON.stringify(preferences));
        this.hideModal();
        this.applyPreferences(preferences);
    }

    applyPreferences(preferences) {
        if (!preferences.analytics) {
            // Desabilitar Google Analytics
            window['ga-disable-UA-XXXXX-Y'] = true;
        }
        if (!preferences.marketing) {
            // Limpar cookies de marketing
            this.deleteMarketingCookies();
        }
    }

    isAccepted(category) {
        const preferences = this.getCookie(this.cookiePreferences);
        if (!preferences) return this.categories[category].required;
        try {
            return JSON.parse(preferences)[category];
        } catch {
            return this.categories[category].required;
        }
    }

    hideBanner() {
        const banner = document.querySelector('.cookie-banner');
        if (banner) banner.remove();
    }

    hideModal() {
        const modal = document.querySelector('.cookie-modal');
        if (modal) modal.remove();
    }

    deleteMarketingCookies() {
        const marketingCookies = ['_fbp', '_ga', '_gid', '_gat'];
        marketingCookies.forEach(cookie => this.deleteCookie(cookie));
    }
}

// Inicializar o gerenciador de cookies
const cookieManager = new CookieManager();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CookieManager;
} 