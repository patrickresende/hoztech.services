#!/usr/bin/env python
import os
import sys
import argparse
from django.core.management import call_command
import django

def run_dev_server(use_ssl=False, port=8000, host='127.0.0.1'):
    """
    Roda o servidor de desenvolvimento com ou sem SSL.
    
    Args:
        use_ssl (bool): Se True, usa HTTPS. Se False, usa HTTP.
        port (int): Porta para rodar o servidor (padrão: 8000)
        host (str): Host para bind do servidor (padrão: 127.0.0.1)
    """
    # Adicionar diretório do projeto ao PYTHONPATH
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_dir)
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
    os.environ['DJANGO_DEBUG'] = 'True'
    django.setup()
    
    if use_ssl:
        # Verificar certificados
        cert_path = os.path.join(project_dir, 'ssl', 'dev.crt')
        key_path = os.path.join(project_dir, 'ssl', 'dev.key')
        
        if not (os.path.exists(cert_path) and os.path.exists(key_path)):
            print("Certificados SSL não encontrados. Execute scripts/setup_ssl.py primeiro.")
            sys.exit(1)
            
        # Importar e usar o servidor SSL
        from scripts.runserver_ssl import run_ssl_server
        run_ssl_server()
    else:
        # Usar servidor padrão do Django
        addr = f"{host}:{port}"
        print(f"\n=== Iniciando servidor de desenvolvimento (HTTP) ===")
        print(f"Acesse: http://{addr}/")
        print("AVISO: Este é um servidor de desenvolvimento.")
        print("NÃO USE EM PRODUÇÃO!\n")
        
        call_command('runserver', addr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Roda o servidor de desenvolvimento Django')
    parser.add_argument('--ssl', action='store_true', help='Usar HTTPS')
    parser.add_argument('--port', type=int, default=8000, help='Porta para rodar o servidor')
    parser.add_argument('--host', default='127.0.0.1', help='Host para bind do servidor')
    
    args = parser.parse_args()
    run_dev_server(use_ssl=args.ssl, port=args.port, host=args.host)