class PromoManager {
    constructor() {
        this.modal = document.getElementById('promoModal');
        this.countdown = document.getElementById('promoCountdown');
        this.hoursElement = document.getElementById('promoHours');
        this.minutesElement = document.getElementById('promoMinutes');
        this.secondsElement = document.getElementById('promoSeconds');
        this.endTime = new Date();
        this.endTime.setHours(this.endTime.getHours() + 6); // 6 horas de cooldown
        this.checkPromoStatus();
        this.startCountdown();
    }

    checkPromoStatus() {
        const lastShown = localStorage.getItem('promoLastShown');
        const now = new Date().getTime();
        
        if (!lastShown || (now - parseInt(lastShown)) > (6 * 60 * 60 * 1000)) {
            this.showModal();
            localStorage.setItem('promoLastShown', now.toString());
        }
    }

    showModal() {
        const modal = new bootstrap.Modal(this.modal);
        modal.show();
    }

    startCountdown() {
        const updateCountdown = () => {
            const now = new Date();
            const timeLeft = this.endTime - now;

            if (timeLeft <= 0) {
                this.hideModal();
                return;
            }

            const hours = Math.floor(timeLeft / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            this.hoursElement.textContent = hours.toString().padStart(2, '0');
            this.minutesElement.textContent = minutes.toString().padStart(2, '0');
            this.secondsElement.textContent = seconds.toString().padStart(2, '0');
            this.countdown.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        };

        updateCountdown();
        this.countdownInterval = setInterval(updateCountdown, 1000);
    }

    hideModal() {
        const modal = bootstrap.Modal.getInstance(this.modal);
        if (modal) {
            modal.hide();
        }
        if (this.countdownInterval) {
            clearInterval(this.countdownInterval);
        }
    }

    // Método para resetar o cooldown (útil para testes)
    resetCooldown() {
        localStorage.removeItem('promoLastShown');
        this.checkPromoStatus();
    }
}

// Inicializar PromoManager quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    window.promoManager = new PromoManager();
}); 