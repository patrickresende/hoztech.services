"""
Testes para o sistema de email e outras funcionalidades.
"""
from django.core.mail import send_mail, get_connection
from django.conf import settings
import logging
import time
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

def test_email_connection() -> Tuple[bool, str]:
    """Testa a conexão com o servidor de email"""
    try:
        print("\n=== Testando conexão com servidor de email ===")
        print(f"Host: {settings.EMAIL_HOST}")
        print(f"Port: {settings.EMAIL_PORT}")
        print(f"TLS: {settings.EMAIL_USE_TLS}")
        print(f"SSL: {settings.EMAIL_USE_SSL}")
        print(f"Username: {settings.EMAIL_HOST_USER}")
        print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
        print(f"Contact Email: {settings.CONTACT_EMAIL}")
        
        connection = get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            use_ssl=settings.EMAIL_USE_SSL,
            timeout=settings.EMAIL_TIMEOUT
        )
        print("\nTentando abrir conexão...")
        connection.open()
        print("Conexão aberta com sucesso!")
        connection.close()
        print("Conexão fechada com sucesso!")
        return True, "Conexão com servidor de email estabelecida com sucesso"
    except Exception as e:
        print(f"\nERRO na conexão: {str(e)}")
        logger.error(f"Erro na conexão com servidor de email: {str(e)}", exc_info=True)
        return False, f"Erro na conexão: {str(e)}"

def test_email_sending() -> Tuple[bool, str]:
    """Testa o envio de email com dados de teste"""
    print("\n=== Iniciando teste de envio de email ===")
    
    # Dados de teste
    test_data = {
        'name': 'Teste Automático',
        'email': 'test@example.com',
        'phone': '11999999999',
        'subject': 'Teste de Envio',
        'message': 'Este é um email de teste automático enviado em: ' + time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        print("\n1. Testando conexão...")
        connection_ok, connection_msg = test_email_connection()
        if not connection_ok:
            print(f"Falha na conexão: {connection_msg}")
            return False, connection_msg
        
        print("\n2. Preparando email de teste...")
        email_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2c3e50;">Email de Teste Automático</h2>
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                <p><strong>Nome:</strong> {test_data['name']}</p>
                <p><strong>Email:</strong> {test_data['email']}</p>
                <p><strong>Telefone:</strong> {test_data['phone']}</p>
                <p><strong>Assunto:</strong> {test_data['subject']}</p>
                <div style="margin-top: 20px;">
                    <strong>Mensagem:</strong>
                    <p style="white-space: pre-wrap;">{test_data['message']}</p>
                </div>
            </div>
            <p style="color: #666; font-size: 0.9em; margin-top: 20px;">
                Este é um email de teste automático do sistema de contato.
            </p>
        </body>
        </html>
        """
        
        print("\n3. Configurações de envio:")
        print(f"FROM: {settings.DEFAULT_FROM_EMAIL}")
        print(f"TO: {settings.CONTACT_EMAIL}")
        print(f"SUBJECT: Teste de Envio - {test_data['subject']}")
        
        print("\n4. Tentando enviar email...")
        send_mail(
            subject=f'Teste de Envio - {test_data["subject"]}',
            message=email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
            html_message=email_content,
        )
        
        print("\n5. Email enviado com sucesso!")
        return True, "Email de teste enviado com sucesso"
        
    except Exception as e:
        print(f"\nERRO no teste: {str(e)}")
        logger.error(f'Falha no teste de envio: {str(e)}', exc_info=True)
        return False, f"Erro no teste: {str(e)}"

def run_all_tests() -> Dict[str, Tuple[bool, str]]:
    """Executa todos os testes disponíveis"""
    results = {}
    
    print("\n=== Iniciando suite de testes ===")
    
    # Teste de conexão
    print("\n1. Testando conexão com servidor de email...")
    results['connection'] = test_email_connection()
    
    # Teste de envio
    print("\n2. Testando envio de email...")
    results['sending'] = test_email_sending()
    
    # Resumo dos resultados
    print("\n=== Resumo dos Testes ===")
    for test_name, (success, message) in results.items():
        status = "✅ Sucesso" if success else "❌ Falha"
        print(f"{test_name}: {status} - {message}")
    
    return results

if __name__ == '__main__':
    run_all_tests() 