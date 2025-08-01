#!/usr/bin/env python3
"""
Script para testar a entrega de e-mails e identificar problemas de spam/filtros
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime
import time

# Configurar Django
def setup_django():
    """Configura o ambiente Django"""
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
    django.setup()

def test_email_delivery_to_different_addresses():
    """Testa envio para diferentes endereços de e-mail"""
    print("\n" + "="*60)
    print("📧 TESTE DE ENTREGA PARA DIFERENTES ENDEREÇOS")
    print("="*60)
    
    from django.core.mail import send_mail
    from django.conf import settings
    
    # Lista de e-mails para testar
    test_emails = [
        "hoztech.services@gmail.com",  # E-mail principal
        "contato@hoztech.com.br",      # E-mail do domínio
        "admin@hoztech.com.br",        # E-mail admin
        "teste@hoztech.com.br",        # E-mail de teste
    ]
    
    results = []
    
    for email in test_emails:
        try:
            print(f"\n📤 Testando envio para: {email}")
            
            subject = f'Teste de Entrega - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            message = f"""
            Teste de entrega de e-mail
            
            Data/Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            De: {settings.DEFAULT_FROM_EMAIL}
            Para: {email}
            
            Este é um teste para verificar se o e-mail está sendo entregue corretamente.
            
            Se você recebeu este e-mail, o sistema está funcionando.
            """
            
            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #2c3e50;">Teste de Entrega - HOZ TECH</h2>
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                    <p><strong>Data/Hora:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    <p><strong>De:</strong> {settings.DEFAULT_FROM_EMAIL}</p>
                    <p><strong>Para:</strong> {email}</p>
                    <p><strong>Status:</strong> Teste de entrega</p>
                </div>
                <p style="color: #666; font-size: 0.9em; margin-top: 20px;">
                    Se você recebeu este e-mail, o sistema está funcionando corretamente.
                </p>
            </body>
            </html>
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
                html_message=html_message,
            )
            
            print(f"✅ E-mail enviado para {email}")
            results.append((email, True, "Enviado com sucesso"))
            
            # Aguardar um pouco entre os envios
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Erro ao enviar para {email}: {e}")
            results.append((email, False, str(e)))
    
    return results

def test_spam_filters():
    """Testa diferentes configurações para evitar spam"""
    print("\n" + "="*60)
    print("🛡️ TESTE DE CONFIGURAÇÕES ANTI-SPAM")
    print("="*60)
    
    from django.core.mail import send_mail
    from django.conf import settings
    
    # Teste com diferentes configurações de cabeçalho
    test_configs = [
        {
            'name': 'Configuração Padrão',
            'subject': f'Contato via Site - Teste {datetime.now().strftime("%H:%M:%S")}',
            'from_email': settings.DEFAULT_FROM_EMAIL,
        },
        {
            'name': 'Configuração com Nome',
            'subject': f'Contato via Site - Teste {datetime.now().strftime("%H:%M:%S")}',
            'from_email': f'HOZ TECH <{settings.DEFAULT_FROM_EMAIL}>',
        },
        {
            'name': 'Configuração com Reply-To',
            'subject': f'Contato via Site - Teste {datetime.now().strftime("%H:%M:%S")}',
            'from_email': settings.DEFAULT_FROM_EMAIL,
        },
    ]
    
    results = []
    
    for config in test_configs:
        try:
            print(f"\n📤 Testando: {config['name']}")
            
            message = f"""
            Teste de configuração anti-spam
            
            Configuração: {config['name']}
            Data/Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            De: {config['from_email']}
            Para: {settings.CONTACT_EMAIL}
            
            Este é um teste para verificar se as configurações anti-spam estão funcionando.
            """
            
            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #2c3e50;">Teste Anti-Spam - HOZ TECH</h2>
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                    <p><strong>Configuração:</strong> {config['name']}</p>
                    <p><strong>Data/Hora:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    <p><strong>De:</strong> {config['from_email']}</p>
                    <p><strong>Para:</strong> {settings.CONTACT_EMAIL}</p>
                </div>
                <p style="color: #666; font-size: 0.9em; margin-top: 20px;">
                    Teste de configuração anti-spam.
                </p>
            </body>
            </html>
            """
            
            send_mail(
                subject=config['subject'],
                message=message,
                from_email=config['from_email'],
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
                html_message=html_message,
            )
            
            print(f"✅ {config['name']} - Enviado com sucesso")
            results.append((config['name'], True, "Enviado com sucesso"))
            
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ {config['name']} - Erro: {e}")
            results.append((config['name'], False, str(e)))
    
    return results

def check_email_logs():
    """Verifica logs de e-mail"""
    print("\n" + "="*60)
    print("📋 VERIFICAÇÃO DE LOGS")
    print("="*60)
    
    from django.conf import settings
    
    print("📧 Configurações atuais:")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  CONTACT_EMAIL: {settings.CONTACT_EMAIL}")
    
    # Verificar se há logs de e-mail
    log_files = [
        'django.log',
        'debug.log',
        'email.log'
    ]
    
    print("\n📄 Verificando arquivos de log:")
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"  ✅ {log_file} - Existe")
            # Mostrar últimas linhas relacionadas a e-mail
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    email_lines = [line for line in lines[-50:] if 'email' in line.lower() or 'mail' in line.lower()]
                    if email_lines:
                        print(f"    Últimas linhas relacionadas a e-mail:")
                        for line in email_lines[-5:]:
                            print(f"      {line.strip()}")
            except Exception as e:
                print(f"    Erro ao ler log: {e}")
        else:
            print(f"  ❌ {log_file} - Não existe")

def generate_delivery_report():
    """Gera relatório de entrega"""
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE ENTREGA")
    print("="*60)
    
    print("🔍 Problemas comuns de entrega:")
    print("1. E-mails indo para spam/lixo eletrônico")
    print("2. Filtros de e-mail bloqueando")
    print("3. Configurações de DNS incorretas")
    print("4. Autenticação SPF/DKIM não configurada")
    print("5. Reputação do IP/domínio")
    
    print("\n💡 Soluções recomendadas:")
    print("1. Verificar pasta de spam/lixo eletrônico")
    print("2. Adicionar e-mail aos contatos")
    print("3. Configurar SPF, DKIM e DMARC")
    print("4. Usar serviço de e-mail transacional (SendGrid, Mailgun)")
    print("5. Verificar logs do servidor de e-mail")
    
    print("\n📧 Configurações recomendadas para produção:")
    print("- Usar serviço de e-mail transacional")
    print("- Configurar autenticação adequada")
    print("- Implementar retry automático")
    print("- Monitorar taxas de entrega")

def main():
    """Função principal"""
    print("🚀 TESTE DE ENTREGA DE E-MAIL - HOZ TECH")
    print("="*60)
    
    # Configurar Django
    try:
        setup_django()
        print("✅ Django configurado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao configurar Django: {e}")
        return
    
    # Executar testes
    print("\n🔍 Iniciando testes de entrega...")
    
    # Teste de entrega para diferentes endereços
    delivery_results = test_email_delivery_to_different_addresses()
    
    # Teste de configurações anti-spam
    spam_results = test_spam_filters()
    
    # Verificar logs
    check_email_logs()
    
    # Gerar relatório
    generate_delivery_report()
    
    # Relatório final
    print("\n" + "="*60)
    print("📈 RELATÓRIO FINAL")
    print("="*60)
    
    print("📧 Testes de Entrega:")
    for email, success, message in delivery_results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"  {email}: {status}")
        if not success:
            print(f"    Erro: {message}")
    
    print("\n🛡️ Testes Anti-Spam:")
    for config, success, message in spam_results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"  {config}: {status}")
        if not success:
            print(f"    Erro: {message}")
    
    # Resumo
    delivery_passed = sum(1 for _, success, _ in delivery_results if success)
    spam_passed = sum(1 for _, success, _ in spam_results if success)
    
    print(f"\n📊 Resultado:")
    print(f"  Entrega: {delivery_passed}/{len(delivery_results)} passaram")
    print(f"  Anti-Spam: {spam_passed}/{len(spam_results)} passaram")
    
    if delivery_passed == len(delivery_results) and spam_passed == len(spam_results):
        print("\n🎉 Todos os testes passaram!")
        print("💡 Verifique as pastas de spam/lixo eletrônico dos e-mails de destino.")
    else:
        print("\n⚠️ Alguns testes falharam.")
        print("🔧 Verifique as configurações e tente novamente.")

if __name__ == "__main__":
    main() 