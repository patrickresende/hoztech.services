import os
from OpenSSL import crypto
from datetime import datetime, timedelta

def generate_self_signed_cert():
    """Gera um certificado SSL auto-assinado para desenvolvimento."""
    
    # Obter diretório do projeto
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Criar diretório de certificados se não existir
    cert_dir = os.path.join(project_dir, 'ssl')
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)
    
    # Gerar chave privada
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    
    # Gerar certificado
    cert = crypto.X509()
    cert.get_subject().C = "BR"
    cert.get_subject().ST = "Rio de Janeiro"
    cert.get_subject().L = "Rio de Janeiro"
    cert.get_subject().O = "HOZ TECH"
    cert.get_subject().OU = "Development"
    cert.get_subject().CN = "localhost"
    
    # Configurar validade (1 ano)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)
    
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    
    # Salvar certificado e chave
    cert_path = os.path.join(cert_dir, "dev.crt")
    key_path = os.path.join(cert_dir, "dev.key")
    
    with open(cert_path, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    with open(key_path, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    
    print(f"Certificados SSL gerados com sucesso em:")
    print(f"- Certificado: {cert_path}")
    print(f"- Chave: {key_path}")

if __name__ == "__main__":
    generate_self_signed_cert() 