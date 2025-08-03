import os
import django
import getpass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Cria ou atualiza o superusuário de forma segura"""
    
    # Configurações do usuário admin
    username = os.getenv('ADMIN_USERNAME', 'patrickresende')
    email = os.getenv('ADMIN_EMAIL', 'hoztech.services@gmail.com')
    
    # Obter senha de forma segura
    password = os.getenv('ADMIN_PASSWORD')
    if not password:
        print("⚠️  ADMIN_PASSWORD não definida nas variáveis de ambiente")
        print("🔐 Digite a senha para o superusuário:")
        password = getpass.getpass("Senha: ")
        
        if not password:
            print("❌ Senha não pode estar vazia!")
            return
    
    # Verifica se o usuário já existe
    if not User.objects.filter(username=username).exists():
        # Cria o superusuário
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Superusuário '{username}' criado com sucesso!")
        print(f"📧 Email: {email}")
    else:
        # Atualiza as permissões se o usuário já existe
        user = User.objects.get(username=username)
        user.is_staff = True
        user.is_superuser = True
        user.email = email
        user.set_password(password)  # Atualiza a senha
        user.save()
        print(f"✅ Permissões do usuário '{username}' atualizadas com sucesso!")
        print(f"📧 Email: {email}")

if __name__ == '__main__':
    print("🔧 Criando/Atualizando Superusuário Django")
    print("=" * 50)
    create_admin_user()
    print("=" * 50)
    print("✅ Operação concluída!") 