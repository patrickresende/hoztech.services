// Gerenciador da Barra de Navegação
class NavbarManager {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.navbarToggler = document.querySelector('.navbar-toggler');
        this.navbarCollapse = document.querySelector('.navbar-collapse');
        this.lastScrollTop = 0;
        this.init();
    }

    init() {
        if (this.navbar) {
            window.addEventListener('scroll', () => this.handleScroll());
            window.addEventListener('resize', () => this.handleResize());
            
            if (this.navbarToggler) {
                this.navbarToggler.addEventListener('click', () => this.handleToggle());
            }

            // Fechar menu ao clicar em um link
            const navLinks = document.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => this.closeMenu());
            });
        }
    }

    handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Adicionar classe quando rolar para baixo
        if (scrollTop > 50) {
            this.navbar.classList.add('navbar-scrolled');
        } else {
            this.navbar.classList.remove('navbar-scrolled');
        }

        // Esconder/mostrar navbar ao rolar
        if (scrollTop > this.lastScrollTop && scrollTop > 200) {
            // Rolando para baixo
            this.navbar.style.transform = 'translateY(-100%)';
        } else {
            // Rolando para cima
            this.navbar.style.transform = 'translateY(0)';
        }

        this.lastScrollTop = scrollTop;
    }

    handleResize() {
        if (window.innerWidth > 991) {
            this.navbarCollapse.classList.remove('show');
            this.navbarToggler.classList.remove('collapsed');
            this.navbarToggler.setAttribute('aria-expanded', 'false');
        }
    }

    handleToggle() {
        const isExpanded = this.navbarToggler.getAttribute('aria-expanded') === 'true';
        
        if (isExpanded) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }

    openMenu() {
        this.navbarCollapse.classList.add('show');
        this.navbarToggler.classList.add('collapsed');
        this.navbarToggler.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
    }

    closeMenu() {
        this.navbarCollapse.classList.remove('show');
        this.navbarToggler.classList.remove('collapsed');
        this.navbarToggler.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }
}

// Inicializar o gerenciador da navbar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new NavbarManager();
}); 