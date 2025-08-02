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
        this.CLOSED_COOKIE_NAME = 'promo_closed';
        this.CLOSED_DURATION = 7 * 24 * 60 * 60 * 1000; // 1 semana em ms

        this.countdownInterval = null;
        this.initializePromo();
        
        // Listener para sincronizar entre abas
        this.setupCrossTabSync();
    }

    setupCrossTabSync() {
        // Escutar mudanças no localStorage para sincronizar entre abas
        window.addEventListener('storage', (e) => {
            if (e.key === 'promo_closed_sync') {
                // Outra aba fechou a promoção
                this.hideBanner();
                this.hideCountdown();
                if (this.countdownInterval) {
                    clearInterval(this.countdownInterval);
                    this.countdownInterval = null;
                }
            }
        });
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
        const now = Date.now();
        
        // Banner sempre visível - não verificar fechamento por usuário

        // 2) Verificar se já existe cookie de cooldown válido
        let existing = this.getCookie(this.COOKIE_NAME);
        
        // Usar localStorage como backup para persistir entre abas
        const localStorageKey = 'promo_end_time';
        let localEndTime = localStorage.getItem(localStorageKey);

        if (!existing && !localEndTime) {
            // Primeira visita: criar novo cooldown
            const endTime = now + this.COOLDOWN_DURATION;
            this.setCookie(this.COOKIE_NAME, endTime, this.COOLDOWN_DURATION);
            localStorage.setItem(localStorageKey, endTime.toString());
            this.showBanner();
        } else if (!existing && localEndTime) {
            // Cookie perdido mas localStorage existe - restaurar
            const endTime = parseInt(localEndTime);
            const remainingTime = endTime - now;
            if (remainingTime > 0) {
                this.setCookie(this.COOKIE_NAME, endTime, remainingTime);
                existing = endTime.toString();
            } else {
                // Tempo expirou, limpar localStorage
                localStorage.removeItem(localStorageKey);
            }
        } else if (existing && !localEndTime) {
            // Cookie existe mas localStorage não - sincronizar
            localStorage.setItem(localStorageKey, existing);
        }

        // 3) Sempre mostrar o banner e verificar se há tempo restante
        this.showBanner(); // Banner sempre visível
        
        const remaining = this.getRemainingTime();
        if (remaining && remaining > 0) {
            this.startCountdown();
        } else {
            // Tempo expirou, iniciar novo ciclo automaticamente
            this.clearCookie(this.COOKIE_NAME);
            localStorage.removeItem(localStorageKey);
            
            // Iniciar novo ciclo automaticamente
            const newEndTime = now + this.COOLDOWN_DURATION;
            this.setCookie(this.COOKIE_NAME, newEndTime, this.COOLDOWN_DURATION);
            localStorage.setItem(localStorageKey, newEndTime.toString());
            this.startCountdown();
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

    // Gerencia o banner - Sempre visível (posicionamento natural)
    showBanner() {
        if (this.banner) {
            // Simplificar a lógica - sempre mostrar o banner
            this.banner.classList.add('show');
            this.banner.style.display = 'block';
            this.banner.style.visibility = 'visible';
            this.banner.style.opacity = '0.85';
            this.banner.style.transform = 'translateY(0)';
            this.banner.style.position = 'relative';
            this.banner.style.zIndex = '9999';
            console.log('🎯 PromoManager: Banner exibido com sucesso');
        }
    }

    hideBanner() {
        // Banner não deve ser escondido - manter sempre visível
        if (this.banner) {
            // Manter visível mas com opacidade reduzida se necessário
            this.banner.style.opacity = '0.85';
        }
    }

    closePromo() {
        // Banner fixo - não permite fechamento
        console.log('Banner promocional é fixo e não pode ser fechado');
        return false;
    }
}

// Inicialização única do PromoManager
// Evita múltiplas instâncias mesmo se o script for carregado mais de uma vez
if (!window.promoManager) {
    window.promoManager = new PromoManager();
    
    // Signal script loaded to system
    if (window.HOZ_SYSTEM) {
        window.HOZ_SYSTEM.scriptsLoaded++;
        console.log('🎯 PromoManager carregado, scripts:', window.HOZ_SYSTEM.scriptsLoaded);
    }
}
