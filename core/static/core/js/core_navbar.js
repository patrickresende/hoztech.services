document.addEventListener('DOMContentLoaded', function() {
    // Variáveis
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');
    let lastScroll = 0;

    // Função para controlar a visibilidade da navbar no scroll
    function handleScroll() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            navbar.classList.remove('scrolled-up');
            navbar.classList.remove('scrolled-down');
            return;
        }
        
        if (currentScroll > lastScroll && !navbar.classList.contains('scrolled-down')) {
            // Scroll Down
            navbar.classList.remove('scrolled-up');
            navbar.classList.add('scrolled-down');
        } else if (currentScroll < lastScroll && navbar.classList.contains('scrolled-down')) {
            // Scroll Up
            navbar.classList.remove('scrolled-down');
            navbar.classList.add('scrolled-up');
        }
        
        lastScroll = currentScroll;
    }

    // Função para fechar o menu mobile ao clicar em um link
    function closeNavbarOnClick() {
        if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
            navbarToggler.click();
        }
    }

    // Função para adicionar classe active ao link atual
    function setActiveLink() {
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Função para adicionar classe quando a navbar está no topo
    function handleNavbarTop() {
        if (window.scrollY > 50) {
            navbar.classList.add('not-top');
        } else {
            navbar.classList.remove('not-top');
        }
    }

    // Event Listeners
    window.addEventListener('scroll', () => {
        handleScroll();
        handleNavbarTop();
    });

    navLinks.forEach(link => {
        link.addEventListener('click', closeNavbarOnClick);
    });

    // Inicialização
    setActiveLink();
    handleNavbarTop();

    // Adicionar classe para animação após carregamento
    setTimeout(() => {
        navbar.classList.add('loaded');
    }, 100);

    // Suporte a gestos touch para o menu mobile
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, false);

    document.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, false);

    function handleSwipe() {
        const swipeThreshold = 100;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) < swipeThreshold) return;

        if (diff > 0) {
            // Swipe left - fecha o menu
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        } else {
            // Swipe right - abre o menu
            if (!navbarCollapse.classList.contains('show') && window.innerWidth < 992) {
                navbarToggler.click();
            }
        }
    }
}); 