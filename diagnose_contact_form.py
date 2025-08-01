#!/usr/bin/env python3
"""
Script de diagnóstico completo para o formulário de contato
"""

import os
import sys
import django
from pathlib import Path
import requests
from datetime import datetime

# Configurar Django
def setup_django():
    """Configura o ambiente Django"""
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
    django.setup()

def test_form_submission():
    """Testa o envio do formulário via HTTP"""
    print("\n" + "="*60)
    print("🌐 TESTE DE ENVIO VIA HTTP")
    print("="*60)
    
    from django.test import Client
    from django.urls import reverse
    
    client = Client()
    
    # Dados de teste
    test_data = {
        'name': 'Teste Automático',
        'email': 'test@example.com',
        'phone': '11999999999',
        'subject': 'Teste de Diagnóstico',
        'message': f'Este é um teste de diagnóstico do formulário enviado em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        'website': ''  # Campo honeypot vazio
    }
    
    try:
        print("📤 Enviando formulário via POST...")
        print(f"URL: {reverse('core:contact')}")
        print(f"Dados: {test_data}")
        
        response = client.post(reverse('core:contact'), test_data)
        
        print(f"\n📊 Resposta:")
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Response: {data}")
                
                if data.get('success'):
                    print("✅ Formulário enviado com sucesso!")
                else:
                    print(f"❌ Erro no formulário: {data.get('message', 'Erro desconhecido')}")
                    if data.get('errors'):
                        print(f"Erros de validação: {data['errors']}")
            except Exception as e:
                print(f"❌ Erro ao processar JSON: {e}")
                print(f"Conteúdo da resposta: {response.content[:500]}")
        else:
            print(f"❌ Status code inesperado: {response.status_code}")
            print(f"Conteúdo da resposta: {response.content[:500]}")
            
    except Exception as e:
        print(f"❌ Erro no teste HTTP: {e}")

def test_form_validation():
    """Testa a validação do formulário"""
    print("\n" + "="*60)
    print("✅ TESTE DE VALIDAÇÃO DO FORMULÁRIO")
    print("="*60)
    
    from core.forms import ContactForm
    
    # Teste com dados válidos
    valid_data = {
        'name': 'João Silva',
        'email': 'joao@example.com',
        'phone': '11999999999',
        'subject': 'Teste Válido',
        'message': 'Esta é uma mensagem de teste válida com mais de 50 caracteres para verificar se a validação está funcionando corretamente.',
        'website': ''
    }
    
    print("📋 Testando dados válidos...")
    form = ContactForm(valid_data)
    if form.is_valid():
        print("✅ Dados válidos aceitos")
        print(f"Dados limpos: {form.cleaned_data}")
    else:
        print("❌ Dados válidos rejeitados")
        print(f"Erros: {form.errors}")
    
    # Teste com dados inválidos
    invalid_data = {
        'name': 'Jo',  # Muito curto
        'email': 'email-invalido',
        'phone': '123',  # Muito curto
        'subject': '',  # Vazio
        'message': 'Curta',  # Muito curta
        'website': ''
    }
    
    print("\n📋 Testando dados inválidos...")
    form = ContactForm(invalid_data)
    if not form.is_valid():
        print("✅ Dados inválidos rejeitados corretamente")
        print(f"Erros: {form.errors}")
    else:
        print("❌ Dados inválidos aceitos incorretamente")

def test_email_handler():
    """Testa o handler de e-mail"""
    print("\n" + "="*60)
    print("📧 TESTE DO HANDLER DE E-MAIL")
    print("="*60)
    
    from core.views import ContactFormHandler
    
    test_data = {
        'name': 'Teste Handler',
        'email': 'test@example.com',
        'phone': '11999999999',
        'subject': 'Teste Handler',
        'message': f'Teste do handler de e-mail em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    }
    
    try:
        print("🔧 Testando formatação de conteúdo...")
        content = ContactFormHandler.format_email_content(test_data)
        print("✅ Conteúdo formatado com sucesso")
        print(f"Tamanho do conteúdo: {len(content)} caracteres")
        
        print("\n📤 Testando envio de e-mail...")
        ContactFormHandler.send_email(test_data)
        print("✅ E-mail enviado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro no handler: {e}")

def check_settings():
    """Verifica configurações importantes"""
    print("\n" + "="*60)
    print("⚙️ VERIFICAÇÃO DE CONFIGURAÇÕES")
    print("="*60)
    
    from django.conf import settings
    
    print("🔧 Configurações Django:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"  CSRF_TRUSTED_ORIGINS: {getattr(settings, 'CSRF_TRUSTED_ORIGINS', 'Não definido')}")
    
    print("\n📧 Configurações de E-mail:")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  CONTACT_EMAIL: {settings.CONTACT_EMAIL}")
    
    print("\n🔒 Configurações de Segurança:")
    print(f"  SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', 'Não definido')}")
    print(f"  SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', 'Não definido')}")
    print(f"  CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', 'Não definido')}")

def test_urls():
    """Testa as URLs do projeto"""
    print("\n" + "="*60)
    print("🔗 TESTE DE URLs")
    print("="*60)
    
    from django.urls import reverse
    from django.test import Client
    
    client = Client()
    
    urls_to_test = [
        ('core:home', 'GET'),
        ('core:contact', 'GET'),
        ('core:sobre_nos', 'GET'),
        ('core:services', 'GET'),
    ]
    
    for url_name, method in urls_to_test:
        try:
            if method == 'GET':
                response = client.get(reverse(url_name))
            else:
                response = client.post(reverse(url_name))
            
            print(f"  {url_name}: {response.status_code}")
            
            if response.status_code != 200:
                print(f"    ⚠️ Status inesperado: {response.status_code}")
                
        except Exception as e:
            print(f"  {url_name}: ❌ Erro - {e}")

def main():
    """Função principal"""
    print("🔍 DIAGNÓSTICO COMPLETO DO FORMULÁRIO DE CONTATO")
    print("="*60)
    
    # Configurar Django
    try:
        setup_django()
        print("✅ Django configurado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao configurar Django: {e}")
        return
    
    # Executar testes
    check_settings()
    test_urls()
    test_form_validation()
    test_email_handler()
    test_form_submission()
    
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL")
    print("="*60)
    
    print("💡 Possíveis problemas identificados:")
    print("1. Verificar se o JavaScript está carregando corretamente")
    print("2. Verificar se o CSRF token está sendo enviado")
    print("3. Verificar se as configurações de e-mail estão corretas")
    print("4. Verificar se há erros no console do navegador")
    print("5. Verificar se o formulário está sendo submetido corretamente")
    
    print("\n🔧 Próximos passos:")
    print("1. Verificar o console do navegador para erros JavaScript")
    print("2. Verificar os logs do servidor")
    print("3. Testar o formulário manualmente no site")
    print("4. Verificar se o e-mail está chegando na caixa de entrada")

if __name__ == "__main__":
    main() 