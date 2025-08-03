// Configurações por Navegador - Pode ser modificado facilmente
window.BROWSER_CONFIG = {
    // Configurações para Brave
    'Brave': {
        disableConsent: false,        // true = desabilita cookie consent
        cspRelaxed: true,             // true = CSP mais flexível
        autoAccept: false,            // true = aceita cookies automaticamente
        showDebugInfo: true,          // true = mostra debug no console
        sameSite: 'Lax',              // 'Lax', 'Strict', ou 'None'
        cookieExpiry: 365             // dias para expiração dos cookies
    },
    
    // Configurações para Firefox
    'Firefox': {
        disableConsent: false,
        cspRelaxed: false,
        autoAccept: false,
        showDebugInfo: false,
        sameSite: 'Strict',
        cookieExpiry: 365
    },
    
    // Configurações para Chrome
    'Chrome': {
        disableConsent: false,
        cspRelaxed: false,
        autoAccept: false,
        showDebugInfo: false,
        sameSite: 'Strict',
        cookieExpiry: 365
    },
    
    // Configurações para Safari
    'Safari': {
        disableConsent: false,
        cspRelaxed: false,
        autoAccept: false,
        showDebugInfo: false,
        sameSite: 'Strict',
        cookieExpiry: 365
    },
    
    // Configurações para Edge
    'Edge': {
        disableConsent: false,
        cspRelaxed: false,
        autoAccept: false,
        showDebugInfo: false,
        sameSite: 'Strict',
        cookieExpiry: 365
    },
    
    // Configuração padrão para navegadores desconhecidos
    'Unknown': {
        disableConsent: false,
        cspRelaxed: false,
        autoAccept: false,
        showDebugInfo: false,
        sameSite: 'Strict',
        cookieExpiry: 365
    }
};

// Função para obter configuração do navegador
window.getBrowserConfig = function(browserName) {
    return window.BROWSER_CONFIG[browserName] || window.BROWSER_CONFIG['Unknown'];
};

// Função para modificar configuração em tempo de execução
window.updateBrowserConfig = function(browserName, newConfig) {
    if (window.BROWSER_CONFIG[browserName]) {
        window.BROWSER_CONFIG[browserName] = { ...window.BROWSER_CONFIG[browserName], ...newConfig };
        console.log(`🍪 Configuração atualizada para ${browserName}:`, window.BROWSER_CONFIG[browserName]);
    }
};

// Função para desabilitar cookie consent para um navegador específico
window.disableCookieConsent = function(browserName) {
    window.updateBrowserConfig(browserName, { disableConsent: true });
    console.log(`🍪 Cookie consent desabilitado para ${browserName}`);
};

// Função para habilitar cookie consent para um navegador específico
window.enableCookieConsent = function(browserName) {
    window.updateBrowserConfig(browserName, { disableConsent: false });
    console.log(`🍪 Cookie consent habilitado para ${browserName}`);
};

// Exemplo de uso:
// window.disableCookieConsent('Brave');  // Desabilita para Brave
// window.enableCookieConsent('Brave');   // Habilita para Brave 