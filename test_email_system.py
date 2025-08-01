#!/usr/bin/env python3
"""
Script para testar o sistema de e-mail do HOZ TECH
Este script testa a conexão, configurações e envio de e-mails
"""

import os
import sys
import django
from pathlib import Path
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configurar Django
def setup_django():
    """Configura o ambiente Django"""
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
    django.setup()

def test_smtp_connection_direct():
    """Testa conexão SMTP diretamente"""
    print("\n" + "="*60)
    print("🔍 TESTE DIRETO DE CONEXÃO SMTP")
    print("="*60)
    
    from django.conf import settings
    
    try:
        # Configurações
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        username = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        use_tls = settings.EMAIL_USE_TLS
        use_ssl = settings.EMAIL_USE_SSL
        
        print(f"📧 Servidor SMTP: {smtp_server}:{smtp_port}")
        print(f"👤 Usuário: {username}")
        print(f"🔒 TLS: {use_tls}, SSL: {use_ssl}")
        
        # Criar contexto SSL se necessário
        if use_ssl:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
        
        # Habilitar debug
        server.set_debuglevel(1)
        
        # Iniciar TLS se necessário
        if use_tls and not use_ssl:
            server.starttls(context=ssl.create_default_context())
        
        # Fazer login
        print("\n🔐 Tentando login...")
        server.login(username, password)
        print("✅ Login realizado com sucesso!")
        
        # Testar envio
        print("\n📤 Testando envio de email...")
        
        # Criar mensagem
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Teste de Email - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        msg['From'] = settings.DEFAULT_FROM_EMAIL
        msg['To'] = settings.CONTACT_EMAIL
        
        # Conteúdo HTML
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2c3e50;">Teste de Email - HOZ TECH</h2>
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                <p><strong>Data/Hora:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p><strong>Servidor:</strong> {smtp_server}:{smtp_port}</p>
                <p><strong>De:</strong> {settings.DEFAULT_FROM_EMAIL}</p>
                <p><strong>Para:</strong> {settings.CONTACT_EMAIL}</p>
                <p><strong>TLS:</strong> {use_tls}</p>
                <p><strong>SSL:</strong> {use_ssl}</p>
            </div>
            <p style="color: #666; font-size: 0.9em; margin-top: 20px;">
                Este é um teste automático do sistema de email do HOZ TECH.
            </p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_content, 'html'))
        
        # Enviar email
        server.send_message(msg)
        print("✅ Email enviado com sucesso!")
        
        # Fechar conexão
        server.quit()
        return True, "Teste direto SMTP realizado com sucesso"
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Erro de autenticação: {e}")
        return False, f"Erro de autenticação: {e}"
    except smtplib.SMTPConnectError as e:
        print(f"❌ Erro de conexão: {e}")
        return False, f"Erro de conexão: {e}"
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ Destinatário recusado: {e}")
        return False, f"Destinatário recusado: {e}"
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False, f"Erro geral: {e}"

def test_django_email():
    """Testa envio de email via Django"""
    print("\n" + "="*60)
    print("🐍 TESTE DE EMAIL VIA DJANGO")
    print("="*60)
    
    from django.core.mail import send_mail, get_connection
    from django.conf import settings
    
    try:
        # Testar conexão
        print("🔗 Testando conexão Django...")
        connection = get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            use_ssl=settings.EMAIL_USE_SSL,
            timeout=settings.EMAIL_TIMEOUT
        )
        connection.open()
        print("✅ Conexão Django estabelecida!")
        connection.close()
        
        # Testar envio
        print("\n📤 Testando envio via Django...")
        
        subject = f'Teste Django - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        message = f"""
        Teste de email via Django
        
        Data/Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        Servidor: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}
        De: {settings.DEFAULT_FROM_EMAIL}
        Para: {settings.CONTACT_EMAIL}
        TLS: {settings.EMAIL_USE_TLS}
        SSL: {settings.EMAIL_USE_SSL}
        
        Este é um teste automático do sistema de email do HOZ TECH via Django.
        """
        
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2c3e50;">Teste Django - HOZ TECH</h2>
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                <p><strong>Data/Hora:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p><strong>Servidor:</strong> {settings.EMAIL_HOST}:{settings.EMAIL_PORT}</p>
                <p><strong>De:</strong> {settings.DEFAULT_FROM_EMAIL}</p>
                <p><strong>Para:</strong> {settings.CONTACT_EMAIL}</p>
                <p><strong>TLS:</strong> {settings.EMAIL_USE_TLS}</p>
                <p><strong>SSL:</strong> {settings.EMAIL_USE_SSL}</p>
                <p><strong>Método:</strong> Django send_mail</p>
            </div>
            <p style="color: #666; font-size: 0.9em; margin-top: 20px;">
                Este é um teste automático do sistema de email do HOZ TECH via Django.
            </p>
        </body>
        </html>
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
            html_message=html_message,
        )
        
        print("✅ Email enviado via Django com sucesso!")
        return True, "Teste Django realizado com sucesso"
        
    except Exception as e:
        print(f"❌ Erro no teste Django: {e}")
        return False, f"Erro no teste Django: {e}"

def test_contact_form_handler():
    """Testa o handler do formulário de contato"""
    print("\n" + "="*60)
    print("📝 TESTE DO HANDLER DE FORMULÁRIO")
    print("="*60)
    
    from core.views import ContactFormHandler
    
    try:
        # Dados de teste
        test_data = {
            'name': 'Teste Automático',
            'email': 'test@example.com',
            'phone': '11999999999',
            'subject': 'Teste de Handler',
            'message': f'Este é um teste do handler de formulário enviado em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        }
        
        print("📋 Dados de teste:")
        for key, value in test_data.items():
            print(f"  {key}: {value}")
        
        # Testar formatação
        print("\n🔧 Testando formatação de conteúdo...")
        email_content = ContactFormHandler.format_email_content(test_data)
        print("✅ Conteúdo formatado com sucesso!")
        
        # Testar envio
        print("\n📤 Testando envio via handler...")
        ContactFormHandler.send_email(test_data)
        print("✅ Email enviado via handler com sucesso!")
        
        return True, "Teste do handler realizado com sucesso"
        
    except Exception as e:
        print(f"❌ Erro no teste do handler: {e}")
        return False, f"Erro no teste do handler: {e}"

def check_email_settings():
    """Verifica as configurações de email"""
    print("\n" + "="*60)
    print("⚙️ VERIFICAÇÃO DE CONFIGURAÇÕES")
    print("="*60)
    
    from django.conf import settings
    
    print("📧 Configurações de Email:")
    print(f"  HOST: {settings.EMAIL_HOST}")
    print(f"  PORT: {settings.EMAIL_PORT}")
    print(f"  TLS: {settings.EMAIL_USE_TLS}")
    print(f"  SSL: {settings.EMAIL_USE_SSL}")
    print(f"  USERNAME: {settings.EMAIL_HOST_USER}")
    print(f"  PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Não definida'}")
    print(f"  FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  CONTACT_EMAIL: {settings.CONTACT_EMAIL}")
    print(f"  TIMEOUT: {settings.EMAIL_TIMEOUT}")
    
    # Verificar se as configurações estão corretas
    issues = []
    
    if not settings.EMAIL_HOST:
        issues.append("EMAIL_HOST não definido")
    if not settings.EMAIL_HOST_USER:
        issues.append("EMAIL_HOST_USER não definido")
    if not settings.EMAIL_HOST_PASSWORD:
        issues.append("EMAIL_HOST_PASSWORD não definido")
    if not settings.DEFAULT_FROM_EMAIL:
        issues.append("DEFAULT_FROM_EMAIL não definido")
    if not settings.CONTACT_EMAIL:
        issues.append("CONTACT_EMAIL não definido")
    
    if issues:
        print("\n⚠️ Problemas encontrados:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n✅ Todas as configurações estão definidas!")
        return True

def main():
    """Função principal"""
    print("🚀 INICIANDO TESTE DO SISTEMA DE EMAIL - HOZ TECH")
    print("="*60)
    
    # Configurar Django
    try:
        setup_django()
        print("✅ Django configurado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao configurar Django: {e}")
        return
    
    # Verificar configurações
    config_ok = check_email_settings()
    if not config_ok:
        print("\n❌ Configurações incompletas. Corrija antes de continuar.")
        return
    
    # Executar testes
    tests = [
        ("Teste Direto SMTP", test_smtp_connection_direct),
        ("Teste Django", test_django_email),
        ("Teste Handler", test_contact_form_handler),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success, message = test_func()
            results.append((test_name, success, message))
        except Exception as e:
            results.append((test_name, False, f"Erro inesperado: {e}"))
    
    # Relatório final
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL")
    print("="*60)
    
    for test_name, success, message in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name}: {status}")
        print(f"  {message}")
        print()
    
    # Resumo
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"📈 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O sistema de email está funcionando.")
    else:
        print("⚠️ Alguns testes falharam. Verifique as configurações e tente novamente.")
    
    print("\n💡 Dicas para solução de problemas:")
    print("1. Verifique se a senha do app do Gmail está correta")
    print("2. Confirme se o 2FA está habilitado na conta Gmail")
    print("3. Verifique se o domínio está na lista de hosts permitidos")
    print("4. Teste com uma conta de email diferente")
    print("5. Verifique os logs do servidor para mais detalhes")

if __name__ == "__main__":
    main() 