from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Testa a compatibilidade CSP com navegadores restritivos como Brave'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Testando compatibilidade CSP...')
        
        # Verificar configurações CSP
        self.stdout.write('\n📊 Configurações CSP:')
        
        if hasattr(settings, 'CSP_SCRIPT_SRC'):
            self.stdout.write(f'CSP_SCRIPT_SRC: {settings.CSP_SCRIPT_SRC}')
            if "'unsafe-eval'" in settings.CSP_SCRIPT_SRC:
                self.stdout.write('⚠️  AVISO: unsafe-eval detectado - pode causar problemas no Brave')
            else:
                self.stdout.write('✅ unsafe-eval não encontrado - compatível com Brave')
        
        if hasattr(settings, 'CSP_STYLE_SRC'):
            self.stdout.write(f'CSP_STYLE_SRC: {settings.CSP_STYLE_SRC}')
        
        if hasattr(settings, 'CSP_FONT_SRC'):
            self.stdout.write(f'CSP_FONT_SRC: {settings.CSP_FONT_SRC}')
        
        # Verificar middleware CSP
        self.stdout.write('\n🔧 Middleware CSP:')
        if 'csp.middleware.CSPMiddleware' in settings.MIDDLEWARE:
            self.stdout.write('✅ CSP Middleware ativo')
        else:
            self.stdout.write('❌ CSP Middleware não encontrado')
        
        # Verificar ambiente
        self.stdout.write('\n🌍 Ambiente:')
        self.stdout.write(f'ENVIRONMENT: {getattr(settings, "ENVIRONMENT", "N/A")}')
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        
        # Verificar configurações de segurança
        self.stdout.write('\n🛡️  Configurações de Segurança:')
        security_settings = [
            'SECURE_SSL_REDIRECT',
            'SECURE_BROWSER_XSS_FILTER',
            'SECURE_CONTENT_TYPE_NOSNIFF',
            'SESSION_COOKIE_SECURE',
            'CSRF_COOKIE_SECURE',
            'SECURE_HSTS_SECONDS',
            'SECURE_HSTS_INCLUDE_SUBDOMAINS',
            'SECURE_HSTS_PRELOAD'
        ]
        
        for setting in security_settings:
            value = getattr(settings, setting, 'N/A')
            self.stdout.write(f'{setting}: {value}')
        
        # Recomendações
        self.stdout.write('\n💡 Recomendações para compatibilidade com Brave:')
        self.stdout.write('1. ✅ Remover unsafe-eval do CSP_SCRIPT_SRC')
        self.stdout.write('2. ✅ Usar event listeners em vez de onclick inline')
        self.stdout.write('3. ✅ Configurar SameSite=Lax para cookies')
        self.stdout.write('4. ✅ Usar HTTPS em produção')
        self.stdout.write('5. ✅ Implementar headers de segurança adequados')
        
        # Verificar arquivos estáticos
        self.stdout.write('\n📁 Verificação de Arquivos Estáticos:')
        static_files = [
            'core/static/core/js/core_cookie_manager.js',
            'core/static/core/js/promo_manager.js',
            'core/static/core/css/cookie_modals.css'
        ]
        
        for file_path in static_files:
            full_path = os.path.join(settings.BASE_DIR, file_path)
            if os.path.exists(full_path):
                self.stdout.write(f'✅ {file_path}')
            else:
                self.stdout.write(f'❌ {file_path}')
        
        self.stdout.write('\n✅ Teste de compatibilidade CSP concluído!') 