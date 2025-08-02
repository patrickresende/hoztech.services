// Gerenciador da Barra de Navegação
class NavbarManager {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.navbarToggler = document.querySelector('.navbar-toggler');
        this.navbarCollapse = document.querySelector('.navbar-collapse');
        this.lastScrollTop = 0;
        this.scrollTimeout = null;
        this.isMenuOpen = false;
        this.init();
    }

    init() {
        if (this.navbar) {
            // Wait for system to force elements first
            const waitForSystem = () => {
                if (window.HOZ_SYSTEM && window.HOZ_SYSTEM.elementsForced) {
                    // System has already forced visibility, don't override
                    console.log('📱 NavbarManager: Sistema já forçou elementos, continuando...');
                    
                    this.setupScrollListener();
                    this.setupResizeListener();
                    this.setupClickListeners();
                    
                    // Signal script loaded
                    if (window.HOZ_SYSTEM) {
                        window.HOZ_SYSTEM.scriptsLoaded++;
                    }
                } else {
                    // Fallback: force visibility if system not ready
                    this.navbar.style.transform = 'translateY(0)';
                    this.navbar.style.display = 'block';
                    this.navbar.style.visibility = 'visible';
                    
                    this.setupScrollListener();
                    this.setupResizeListener();
                    this.setupClickListeners();
                    
                    console.log('📱 NavbarManager: Sistema não pronto, forçando visibilidade');
                }
            };
            
            // Wait up to 1 second for system
            let attempts = 0;
            const checkInterval = setInterval(() => {
                attempts++;
                if ((window.HOZ_SYSTEM && window.HOZ_SYSTEM.elementsForced) || attempts >= 10) {
                    clearInterval(checkInterval);
                    waitForSystem();
                }
            }, 100);
        }
    }

    setupScrollListener() {
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    this.handleScroll();
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }

    setupResizeListener() {
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 250);
        }, { passive: true });
    }

    setupClickListeners() {
        if (this.navbarToggler) {
            this.navbarToggler.addEventListener('click', () => this.handleToggle());
        }

        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => this.closeMenu());
        });

        document.addEventListener('click', (event) => {
            const isClickInside = this.navbar.contains(event.target);
            if (!isClickInside && this.isMenuOpen) {
                this.closeMenu();
            }
        });
    }

    handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 50) {
            this.navbar.classList.add('navbar-scrolled');
        } else {
            this.navbar.classList.remove('navbar-scrolled');
        }

        // Auto-hide navbar desabilitado para manter sempre visível
        // if (scrollTop > this.lastScrollTop && scrollTop > 200) {
        //     this.navbar.style.transform = 'translateY(-100%)';
        // } else {
        //     this.navbar.style.transform = 'translateY(0)';
        // }

        this.lastScrollTop = scrollTop;
    }

    handleResize() {
        if (window.innerWidth >= 992) {
            this.closeMenu();
        }
    }

    handleToggle() {
        if (this.isMenuOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }

    openMenu() {
        if (this.isMenuOpen) return;
        
        const scrollY = window.scrollY;
        this.navbarCollapse.classList.add('show');
        this.navbarToggler.classList.add('collapsed');
        this.navbarToggler.setAttribute('aria-expanded', 'true');
        
        // Verifica se o cookie consent está ativo
        const cookieConsent = document.querySelector('.cookie-consent.show');
        if (!cookieConsent) {
            document.body.style.position = 'fixed';
            document.body.style.top = `-${scrollY}px`;
            document.body.style.width = '100%';
        }
        
        this.isMenuOpen = true;
    }

    closeMenu() {
        if (!this.isMenuOpen) return;
        
        const scrollY = document.body.style.top;
        this.navbarCollapse.classList.remove('show');
        this.navbarToggler.classList.remove('collapsed');
        this.navbarToggler.setAttribute('aria-expanded', 'false');
        
        // Verifica se o cookie consent está ativo
        const cookieConsent = document.querySelector('.cookie-consent.show');
        if (!cookieConsent) {
            document.body.style.position = '';
            document.body.style.top = '';
            document.body.style.width = '';
            window.scrollTo(0, parseInt(scrollY || '0') * -1);
        }
        
        this.isMenuOpen = false;
    }
}

// Inicializar o gerenciador da navbar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    // Evitar inicialização duplicada
    if (!window.navbarManager) {
        window.navbarManager = new NavbarManager();
    }
}); 