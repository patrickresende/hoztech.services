"""
WSGI config for hoztechsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Adiciona o diretório do projeto ao Python path
project_dir = Path(__file__).resolve().parent.parent
if str(project_dir) not in sys.path:
    sys.path.append(str(project_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')

try:
    application = get_wsgi_application()
    application = WhiteNoise(
        application,
        root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles'),
        prefix='static/',
        max_age=31536000
    )
    print("=== WSGI Application iniciada com sucesso ===")
except Exception as e:
    print(f"=== Erro ao iniciar WSGI Application: {e} ===")
    print(f"Python path: {sys.path}")
    print(f"Diretório atual: {os.getcwd()}")
    print(f"Listagem de arquivos: {os.listdir('.')}")
    raise
