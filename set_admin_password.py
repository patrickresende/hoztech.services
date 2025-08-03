import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
django.setup()

# Importar o modelo User após configurar o ambiente
from django.contrib.auth.models import User

# Definir a senha do usuário admin
try:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    # Desativar validação de senha
    user._password = 'admin123'
    user.save()
    print(f"Senha do usuário {user.username} alterada com sucesso!")
except User.DoesNotExist:
    # Criar o usuário se não existir
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print(f"Usuário {user.username} criado com sucesso!")
except Exception as e:
    print(f"Erro: {e}")