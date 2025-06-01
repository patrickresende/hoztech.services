from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    # Generate a secure secret key
    secret_key = get_random_secret_key()
    
    # Print the key
    print("\n=== Sua Nova Secret Key Django ===")
    print(f"\n{secret_key}\n")
    
    # Print instructions
    print("Instruções:")
    print("1. Copie esta chave")
    print("2. No arquivo .env, adicione:")
    print(f'SECRET_KEY="{secret_key}"')
    print("\n3. No Render, adicione como variável de ambiente")
    print("   Nome: SECRET_KEY")
    print(f"   Valor: {secret_key}")
    print("\nGuarde esta chave em um local seguro!")
    print("==========================================\n") 