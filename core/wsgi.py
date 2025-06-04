"""
WSGI config for core project.
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Adiciona o diretório do projeto ao Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_dir not in sys.path:
    sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')

try:
    application = get_wsgi_application()
    print("=== WSGI Application iniciada com sucesso ===")
except Exception as e:
    print(f"=== Erro ao iniciar WSGI Application: {e} ===")
    print(f"Python path: {sys.path}")
    print(f"Diretório atual: {os.getcwd()}")
    print(f"Listagem de arquivos: {os.listdir('.')}")
    raise 