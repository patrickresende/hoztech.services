class PromoManager {
    constructor() {
        // Initialize properties
        this.modal = null;
        this.banner = null;
        this.countdownElement = null;
        this.endTime = null;
        this.isInitialized = false;

        // Bind methods to preserve context
        this.closeModal = this.closeModal.bind(this);
        this.handleOutsideClick = this.handleOutsideClick.bind(this);
        this.handleEscapeKey = this.handleEscapeKey.bind(this);

        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    init() {
        console.log('Initializing PromoManager...'); // Debug log
        
        // Get DOM elements
        this.modal = document.getElementById('promoOverlay');
        this.banner = document.getElementById('promoBanner');
        this.countdownElement = document.getElementById('promoCountdown');

        if (!this.modal && !this.banner) {
            console.warn('No promo elements found in the DOM');
            return;
        }

        // Check if promo has been closed before
        const modalClosed = this.getCookie('modal_closed');
        const promoEndTime = this.getCookie('promo_end_time');
        
        // Set end time if not set
        if (!promoEndTime) {
            this.endTime = Date.now() + (48 * 60 * 60 * 1000); // 48 hours
            this.setCookie('promo_end_time', this.endTime, 2); // 2 days
        } else {
            this.endTime = parseInt(promoEndTime);
        }

        // Show modal if not closed
        if (this.modal && !modalClosed) {
            this.showModal();
        }

        // Show banner always
        if (this.banner) {
            this.showBanner();
        }

        // Start countdown if either element is visible
        if ((this.modal && !modalClosed) || this.banner) {
            this.startCountdown();
        }

        this.addEventListeners();
        this.isInitialized = true;
        console.log('PromoManager initialized successfully'); // Debug log
    }

    showModal() {
        if (!this.modal) return;
        
        // Ensure modal is visible in the DOM
        this.modal.style.display = 'flex';
        
        // Use requestAnimationFrame for smooth animation
        requestAnimationFrame(() => {
            setTimeout(() => {
                this.modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }, 3000);
        });
    }

    showBanner() {
        if (!this.banner) return;
        this.banner.classList.add('active');
    }

    hideModal() {
        if (!this.modal) return;
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    closeModal() {
        console.log('Closing modal...'); // Debug log
        this.setCookie('modal_closed', 'true', 2); // 2 days
        this.hideModal();
    }

    handleOutsideClick(e) {
        if (this.modal && e.target === this.modal) {
            this.closeModal();
        }
    }

    handleEscapeKey(e) {
        if (e.key === 'Escape') {
            this.closeModal();
        }
    }

    startCountdown() {
        if (!this.countdownElement) return;

        const updateCountdown = () => {
            const now = Date.now();
            const distance = this.endTime - now;

            if (distance <= 0) {
                this.closeModal();
                return;
            }

            const hours = Math.floor(distance / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            this.countdownElement.textContent = `${hours}h ${minutes}m ${seconds}s`;
            requestAnimationFrame(updateCountdown);
        };

        updateCountdown();
    }

    addEventListeners() {
        // Close modal on X button click
        const modalCloseButtons = document.querySelectorAll('.promo-close');
        modalCloseButtons.forEach(button => {
            button.addEventListener('click', this.closeModal);
        });

        // Close modal on outside click
        if (this.modal) {
            this.modal.addEventListener('click', this.handleOutsideClick);
        }

        // Close modal on escape key
        document.addEventListener('keydown', this.handleEscapeKey);
    }

    setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/;SameSite=Lax`;
    }

    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
}

// Initialize when DOM is ready
if (typeof window.promoManager === 'undefined') {
    window.promoManager = new PromoManager();
}
