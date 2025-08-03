"""
Comando personalizado para executar o servidor Django forçando HTTP
"""

import os
import sys
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management.base import CommandError
from django.conf import settings


class Command(RunserverCommand):
    help = 'Executa o servidor de desenvolvimento Django forçando HTTP (sem HTTPS)'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--force-http',
            action='store_true',
            dest='force_http',
            default=True,
            help='Força o uso de HTTP (padrão: True)',
        )

    def handle(self, *args, **options):
        # Forçar configurações HTTP
        self.force_http_settings()
        
        # Mostrar informações de configuração
        self.show_http_config()
        
        # Executar o runserver normal
        super().handle(*args, **options)

    def force_http_settings(self):
        """Força configurações HTTP no Django"""
        
        # Desabilitar todas as configurações HTTPS
        settings.SECURE_SSL_REDIRECT = False
        settings.SECURE_PROXY_SSL_HEADER = None
        settings.SESSION_COOKIE_SECURE = False
        settings.CSRF_COOKIE_SECURE = False
        settings.SECURE_HSTS_SECONDS = 0
        settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = False
        settings.SECURE_HSTS_PRELOAD = False
        settings.SECURE_BROWSER_XSS_FILTER = False
        settings.SECURE_CONTENT_TYPE_NOSNIFF = False
        
        # Garantir que DEBUG está True
        settings.DEBUG = True
        
        # Adicionar origens HTTP ao CSRF_TRUSTED_ORIGINS
        http_origins = [
            'http://localhost:8000',
            'http://127.0.0.1:8000',
            'http://localhost:8080',
            'http://127.0.0.1:8080',
        ]
        
        if hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
            for origin in http_origins:
                if origin not in settings.CSRF_TRUSTED_ORIGINS:
                    settings.CSRF_TRUSTED_ORIGINS.append(origin)
        else:
            settings.CSRF_TRUSTED_ORIGINS = http_origins

    def show_http_config(self):
        """Mostra as configurações HTTP aplicadas"""
        
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("🔧 SERVIDOR HTTP FORÇADO - HOZ TECH"))
        self.stdout.write("=" * 60)
        
        self.stdout.write(f"🌐 Ambiente: {getattr(settings, 'ENVIRONMENT', 'development')}")
        self.stdout.write(f"🐛 DEBUG: {settings.DEBUG}")
        self.stdout.write(f"🔒 SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
        self.stdout.write(f"🍪 SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
        self.stdout.write(f"🛡️  CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
        self.stdout.write(f"⏱️  SECURE_HSTS_SECONDS: {settings.SECURE_HSTS_SECONDS}")
        
        self.stdout.write("\n📋 ALLOWED_HOSTS:")
        for host in settings.ALLOWED_HOSTS:
            self.stdout.write(f"   ✅ {host}")
        
        self.stdout.write("\n🔗 CSRF_TRUSTED_ORIGINS:")
        for origin in getattr(settings, 'CSRF_TRUSTED_ORIGINS', []):
            if origin.startswith('http://'):
                self.stdout.write(f"   ✅ {origin}")
            else:
                self.stdout.write(f"   ⚠️  {origin}")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("🚀 URLs PARA ACESSO HTTP:"))
        self.stdout.write("=" * 60)
        self.stdout.write("✅ http://127.0.0.1:8000/")
        self.stdout.write("✅ http://localhost:8000/")
        self.stdout.write("✅ http://127.0.0.1:8000/admin/")
        self.stdout.write("❌ https://127.0.0.1:8000/ (NÃO FUNCIONARÁ)")
        self.stdout.write("❌ https://localhost:8000/ (NÃO FUNCIONARÁ)")
        self.stdout.write("=" * 60)
        
        self.stdout.write(self.style.WARNING("\n💡 DICAS:"))
        self.stdout.write("• Use uma aba incógnita se houver cache HSTS")
        self.stdout.write("• Limpe o cache do navegador se necessário")
        self.stdout.write("• Para Chrome: chrome://net-internals/#hsts")
        self.stdout.write("")

    def inner_run(self, *args, **options):
        """Override do método inner_run para adicionar verificações HTTP"""
        
        # Verificar se não há configurações HTTPS ativas
        if settings.SECURE_SSL_REDIRECT:
            self.stdout.write(
                self.style.WARNING("⚠️  AVISO: SECURE_SSL_REDIRECT ainda está True!")
            )
        
        # Executar o servidor
        return super().inner_run(*args, **options)