import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
django.setup()

from django.contrib.auth.models import User

# Verifica se o usuário já existe
if not User.objects.filter(username='patrickresende').exists():
    # Cria o superusuário
    User.objects.create_superuser(
        username='patrickresende',
        email='hoztech.services@gmail.com',
        password='sua_senha_aqui',  # Substitua pela senha desejada
        is_staff=True,
        is_superuser=True
    )
    print("Superusuário criado com sucesso!")
else:
    # Atualiza as permissões se o usuário já existe
    user = User.objects.get(username='patrickresende')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Permissões do usuário atualizadas com sucesso!") 