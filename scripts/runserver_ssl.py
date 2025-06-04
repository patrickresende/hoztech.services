import os
import sys
import django
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.servers.basehttp import WSGIServer
import ssl
import logging
import socket

logger = logging.getLogger(__name__)

def run_ssl_server():
    """Roda o servidor de desenvolvimento com SSL."""
    
    # Adicionar diretório do projeto ao PYTHONPATH
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_dir)
    
    # Verificar se os certificados existem
    cert_path = os.path.join(project_dir, 'ssl', 'dev.crt')
    key_path = os.path.join(project_dir, 'ssl', 'dev.key')
    
    if not (os.path.exists(cert_path) and os.path.exists(key_path)):
        print("Certificados SSL não encontrados. Execute scripts/setup_ssl.py primeiro.")
        sys.exit(1)
    
    # Configurar SSL
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoztechsite.settings')
    
    # Forçar algumas configurações importantes
    os.environ['DJANGO_DEBUG'] = 'True'  # Garantir que debug está ativo para desenvolvimento
    os.environ['SECURE_SSL_REDIRECT'] = 'True'  # Habilitar redirecionamento para HTTPS
    
    django.setup()
    
    # Monkey patch WSGIServer
    original_init = WSGIServer.__init__
    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        try:
            # Criar contexto SSL com configurações mais seguras
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=cert_path, keyfile=key_path)
            
            # Configurar opções de segurança mas manter compatibilidade
            context.options |= (
                ssl.OP_NO_SSLv2 |
                ssl.OP_NO_SSLv3 |
                ssl.OP_NO_COMPRESSION
            )
            context.set_ciphers('ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
            
            # Aplicar contexto ao socket
            self.socket = context.wrap_socket(
                self.socket,
                server_side=True,
                do_handshake_on_connect=False  # Evitar problemas de handshake
            )
            
            logger.info("Configuração SSL aplicada com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao configurar SSL: {str(e)}")
            print(f"\nErro ao configurar SSL: {str(e)}")
            print("Verifique se os certificados são válidos e têm as permissões corretas.")
            sys.exit(1)
            
    # Monkey patch handle_error para melhor tratamento de erros SSL
    original_handle_error = WSGIServer.handle_error
    def handle_error(self, request, client_address):
        try:
            raise
        except ssl.SSLError as e:
            if "HTTP_REQUEST" in str(e):
                logger.warning(f"Tentativa de acesso HTTP em porta HTTPS de {client_address}")
                try:
                    # Enviar redirecionamento 301 para HTTPS
                    host = request.getsockname()[0]
                    port = request.getsockname()[1]
                    location = f"https://{host}:{port}"
                    msg = (
                        "HTTP/1.1 301 Moved Permanently\r\n"
                        f"Location: {location}\r\n"
                        "Content-Type: text/plain\r\n"
                        "Connection: close\r\n\r\n"
                        "Redirecionando para HTTPS...\n"
                        "Redirecting to HTTPS...\n"
                    )
                    request.send(msg.encode('utf-8'))
                except (socket.error, OSError):
                    pass  # Cliente já fechou a conexão
            else:
                logger.error(f"Erro SSL com {client_address}: {e}")
                original_handle_error(request, client_address)
        except Exception as e:
            logger.error(f"Erro não-SSL com {client_address}: {e}")
            original_handle_error(request, client_address)
    
    WSGIServer.__init__ = __init__
    WSGIServer.handle_error = handle_error
    
    # Substituir a mensagem padrão do Django
    def new_log_message(self, format, *args):
        if "Starting development server at http://" in format:
            format = format.replace("http://", "https://")
        return original_log_message(self, format, *args)
    
    from django.core.servers.basehttp import WSGIRequestHandler
    original_log_message = WSGIRequestHandler.log_message
    WSGIRequestHandler.log_message = new_log_message
    
    # Rodar servidor
    print("\n=== Iniciando servidor HTTPS de desenvolvimento ===")
    print("Acesse: https://127.0.0.1:8000/")
    print("\nIMPORTANTE:")
    print("1. Use https:// no início da URL (não http://)")
    print("2. Este é um certificado auto-assinado para desenvolvimento.")
    print("3. Para prosseguir no Chrome: digite 'thisisunsafe' em qualquer lugar da página de aviso")
    print("4. Para outros navegadores: clique em 'Avançado' e depois em 'Prosseguir'")
    print("\nPara encerrar o servidor: pressione Ctrl+C\n")
    
    try:
        # Usar 127.0.0.1 em vez de 0.0.0.0 para acesso local
        call_command('runserver', '127.0.0.1:8000', use_threading=True, use_reloader=True)
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    except Exception as e:
        print(f"\nErro ao iniciar o servidor: {str(e)}")
        logger.error(f"Erro ao iniciar o servidor: {str(e)}")

if __name__ == "__main__":
    run_ssl_server() 