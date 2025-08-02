from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles.finders import find
import os
import glob

class Command(BaseCommand):
    help = 'Verifica se os arquivos estáticos estão sendo servidos corretamente'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Verificando arquivos estáticos...')
        
        # Verificar arquivos CSS críticos
        css_files = [
            'core/css/core_base.css',
            'core/css/core_images.css',
            'core/css/core_cookie_manager.css',
            'core/css/core_output.css',
            'core/css/cookie_modals.css',
            'core/css/style.css'
        ]
        
        for css_file in css_files:
            try:
                found_path = find(css_file)
                if found_path:
                    self.stdout.write(f'✅ {css_file} - Encontrado em: {found_path}')
                else:
                    self.stdout.write(f'❌ {css_file} - NÃO ENCONTRADO')
            except Exception as e:
                self.stdout.write(f'❌ {css_file} - Erro: {e}')
        
        # Verificar arquivos JS críticos
        js_files = [
            'core/js/core_cookie_manager.js',
            'core/js/core_contact_form.js',
            'core/js/core_navbar.js',
            'core/js/promo_manager.js'
        ]
        
        for js_file in js_files:
            try:
                found_path = find(js_file)
                if found_path:
                    self.stdout.write(f'✅ {js_file} - Encontrado em: {found_path}')
                else:
                    self.stdout.write(f'❌ {js_file} - NÃO ENCONTRADO')
            except Exception as e:
                self.stdout.write(f'❌ {js_file} - Erro: {e}')
        
        # Verificar configurações
        self.stdout.write(f'\n📊 Configurações:')
        self.stdout.write(f'STATIC_URL: {settings.STATIC_URL}')
        self.stdout.write(f'STATIC_ROOT: {settings.STATIC_ROOT}')
        self.stdout.write(f'STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}')
        self.stdout.write(f'WHITENOISE_USE_FINDERS: {getattr(settings, "WHITENOISE_USE_FINDERS", "N/A")}')
        
        # Verificar se STATIC_ROOT existe e tem arquivos
        if os.path.exists(settings.STATIC_ROOT):
            static_files = glob.glob(os.path.join(settings.STATIC_ROOT, '**/*'), recursive=True)
            self.stdout.write(f'\n📁 STATIC_ROOT contém {len(static_files)} arquivos')
        else:
            self.stdout.write(f'\n❌ STATIC_ROOT não existe: {settings.STATIC_ROOT}')
        
        self.stdout.write('\n✅ Verificação concluída!') 