// Gerenciador de Promoções
class PromoManager {
    constructor() {
        // Elementos da UI
        this.modal = document.getElementById('promoModal');
        this.banner = document.getElementById('promoBanner');
        this.countdownContainer = document.querySelector('.promo-timer');
        this.countdownNavContainer = document.querySelector('.promo-countdown');
        this.hoursElement = document.getElementById('promoHours');
        this.minutesElement = document.getElementById('promoMinutes');
        this.secondsElement = document.getElementById('promoSeconds');
        this.countdown = document.getElementById('promoCountdown');
        this.navCountdown = document.getElementById('promoNavCountdown');

        // Configurações
        this.COOKIE_NAME = 'promo_cooldown';
        this.COOLDOWN_DURATION = 6 * 60 * 60 * 1000; // 6h em ms

        this.countdownInterval = null;
        this.initializePromo();
    }

    // Lê cookie
    getCookie(name) {
        const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
        return match ? decodeURIComponent(match[1]) : null;
    }

    // Grava cookie com tempo (ms) de expiração
    setCookie(name, value, maxAgeMs) {
        const expires = new Date(Date.now() + maxAgeMs).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)};expires=${expires};path=/`;
    }

    // Remove cookie
    clearCookie(name) {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
    }

    // Calcula ms restantes
    getRemainingTime() {
        const raw = this.getCookie(this.COOKIE_NAME);
        if (!raw) return null;
        const endTime = parseInt(raw, 10);
        if (isNaN(endTime)) return null;
        return Math.max(0, endTime - Date.now());
    }

    // Formata ms para hh:mm:ss
    formatTime(ms) {
        const h = Math.floor(ms / 3_600_000);
        const m = Math.floor((ms % 3_600_000) / 60_000);
        const s = Math.floor((ms % 60_000) / 1000);
        return {
            hours: String(h).padStart(2, '0'),
            minutes: String(m).padStart(2, '0'),
            seconds: String(s).padStart(2, '0'),
            full: `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
        };
    }

    // Atualiza UI
    updateDisplay(ms) {
        const { hours, minutes, seconds, full } = this.formatTime(ms);
        if (this.hoursElement) this.hoursElement.textContent = hours;
        if (this.minutesElement) this.minutesElement.textContent = minutes;
        if (this.secondsElement) this.secondsElement.textContent = seconds;
        if (this.countdown) this.countdown.textContent = full;
        if (this.navCountdown) this.navCountdown.textContent = full;
    }

    showCountdown() {
        [this.countdownContainer, this.countdownNavContainer, this.countdown, this.navCountdown]
            .forEach(el => el && (el.style.display = 'block'));
    }

    hideCountdown() {
        [this.countdownContainer, this.countdownNavContainer, this.countdown, this.navCountdown]
            .forEach(el => el && (el.style.display = 'none'));
    }

    // Inicia ou reinicia o contador
    startCountdown() {
        // Garante que só exista 1 intervalo ativo
        if (this.countdownInterval) clearInterval(this.countdownInterval);

        const tick = () => {
            const remaining = this.getRemainingTime();
            if (remaining === null || remaining <= 0) {
                clearInterval(this.countdownInterval);
                this.hideCountdown();
                this.clearCookie(this.COOKIE_NAME);
                return;
            }
            this.updateDisplay(remaining);
        };

        this.showCountdown();
        tick(); // update imediato
        this.countdownInterval = setInterval(tick, 1000);
    }

    // Lógica inicial
    initializePromo() {
        // Verificar se a promoção foi fechada pelo usuário
        const promoClosed = this.getCookie('promo_closed');
        if (promoClosed) {
            this.hideBanner();
            this.hideCountdown();
            return;
        }

        // 1) Verifica se já existe cookie válido
        let existing = this.getCookie(this.COOKIE_NAME);
        const now = Date.now();

        // Usar localStorage como backup para persistir entre abas
        const localStorageKey = 'promo_end_time';
        let localEndTime = localStorage.getItem(localStorageKey);

        if (!existing && !localEndTime) {
            // primeira visita: grava com timestamp de expiração
            const endTime = now + this.COOLDOWN_DURATION;
            this.setCookie(this.COOKIE_NAME, endTime, this.COOLDOWN_DURATION);
            localStorage.setItem(localStorageKey, endTime.toString());
            this.showBanner(); // Mostra o banner na primeira visita
        } else if (!existing && localEndTime) {
            // Cookie perdido mas localStorage existe - restaurar
            const endTime = parseInt(localEndTime);
            const remainingTime = endTime - now;
            if (remainingTime > 0) {
                this.setCookie(this.COOKIE_NAME, endTime, remainingTime);
                existing = endTime.toString();
            }
        } else if (existing && !localEndTime) {
            // Cookie existe mas localStorage não - sincronizar
            localStorage.setItem(localStorageKey, existing);
        }

        // 2) Se ainda faltam ms, inicia o countdown; se expirou, limpa tudo
        const remaining = this.getRemainingTime();
        if (remaining && remaining > 0) {
            this.startCountdown();
            this.showBanner(); // Mostra o banner se ainda tem tempo
        } else {
            this.hideCountdown();
            this.hideBanner(); // Esconde o banner se expirou
            this.clearCookie(this.COOKIE_NAME);
            localStorage.removeItem(localStorageKey);
        }
    }

    // Exibe o modal promo
    showPromo() {
        if (this.modal) new bootstrap.Modal(this.modal).show();
    }

    hidePromo() {
        if (this.modal) {
            const m = bootstrap.Modal.getInstance(this.modal);
            if (m) m.hide();
        }
    }

    // Gerencia o banner
    showBanner() {
        if (this.banner) {
            this.banner.classList.add('show');
            // Ajusta o padding-top do body para compensar o banner
            document.body.style.paddingTop = this.banner.offsetHeight + 'px';
        }
    }

    hideBanner() {
        if (this.banner) {
            this.banner.classList.remove('show');
            // Remove o padding-top do body
            document.body.style.paddingTop = '0';
        }
    }

    closePromo() {
        this.hideBanner();
        this.hidePromo();
        this.hideCountdown();
        
        // Marcar como fechado pelo usuário (24h)
        this.setCookie('promo_closed', 'true', 24 * 60 * 60 * 1000);
        
        // Limpar dados da promoção
        this.clearCookie(this.COOKIE_NAME);
        localStorage.removeItem('promo_end_time');
        
        // Parar countdown
        if (this.countdownInterval) {
            clearInterval(this.countdownInterval);
            this.countdownInterval = null;
        }
    }
}

// Inicialização única do PromoManager
// Evita múltiplas instâncias mesmo se o script for carregado mais de uma vez
if (!window.promoManager) {
    window.promoManager = new PromoManager();
}
