# HOZ TECH Website

Site institucional da HOZ TECH, desenvolvido com Django.

## 🚀 Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- virtualenv ou venv

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/hoztechsite.git
cd hoztechsite
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
# Copie o arquivo de exemplo
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

### Rodando o Servidor de Desenvolvimento

Você tem duas opções para rodar o servidor de desenvolvimento:

#### Usando o script de conveniência

O script `scripts/dev.py` oferece várias opções:

1. HTTP básico (padrão):
```bash
python scripts/dev.py
```

2. Com HTTPS:
```bash
python scripts/dev.py --ssl
```

3. Em uma porta específica:
```bash
python scripts/dev.py --ssl --port 8443
```

4. Permitindo acesso externo:
```bash
python scripts/dev.py --ssl --host 0.0.0.0
```

#### Usando os comandos tradicionais

1. Servidor HTTP padrão:
```bash
python manage.py runserver
```

2. Servidor HTTPS para desenvolvimento:
```bash
python scripts/runserver_ssl.py
```

### Certificados SSL para Desenvolvimento

Para usar HTTPS em desenvolvimento:

1. Gere os certificados:
```bash
python scripts/setup_ssl.py
```

2. Aceite o certificado auto-assinado no navegador:
- Chrome: Digite 'thisisunsafe' na página de aviso
- Firefox/Edge: Clique em "Avançado" > "Aceitar o Risco"

## 🌐 Configuração de Produção

### Requisitos de Produção

- Servidor Linux (recomendado Ubuntu 20.04+)
- Nginx ou Apache
- Gunicorn ou uWSGI
- Certificado SSL válido (Let's Encrypt recomendado)
- PostgreSQL (recomendado) ou MySQL

### Configuração do Servidor de Produção

1. Instale as dependências do sistema:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

2. Configure o banco de dados PostgreSQL:
```bash
sudo -u postgres createdb hoztechdb
sudo -u postgres createuser hoztech
```

3. Configure o Gunicorn:
```bash
# Instale o Gunicorn
pip install gunicorn

# Teste o Gunicorn
gunicorn hoztechsite.wsgi:application
```

4. Configure o Nginx:
```nginx
server {
    listen 80;
    server_name seudominio.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /caminho/para/seu/projeto;
    }
    
    location /media/ {
        root /caminho/para/seu/projeto;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

5. Configure SSL com Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com
```

### Variáveis de Ambiente para Produção

Configure as seguintes variáveis em produção:
```
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=sua-chave-secreta-muito-segura
ALLOWED_HOSTS=seudominio.com
DATABASE_URL=postgres://usuario:senha@localhost:5432/hoztechdb
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Checklist de Segurança para Produção

- [ ] DEBUG está desativado
- [ ] SECRET_KEY foi alterada
- [ ] ALLOWED_HOSTS está configurado corretamente
- [ ] Certificado SSL válido instalado
- [ ] Configurações de segurança do Django ativadas
- [ ] Banco de dados seguro e com backup
- [ ] Arquivos estáticos sendo servidos pelo Nginx
- [ ] Logs configurados e monitorados

## 📝 Manutenção

### Backup do Banco de Dados

```bash
# PostgreSQL
pg_dump hoztechdb > backup.sql

# Restauração
psql hoztechdb < backup.sql
```

### Atualizando o Site

```bash
# Ative o ambiente virtual
source venv/bin/activate

# Puxe as alterações
git pull

# Atualize dependências
pip install -r requirements.txt

# Aplique migrações
python manage.py migrate

# Colete arquivos estáticos
python manage.py collectstatic --noinput

# Reinicie o Gunicorn
sudo systemctl restart gunicorn
```

## 🤝 Contribuindo

1. Crie um branch para sua feature
2. Faça commit das alterações
3. Envie um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## 📞 Suporte

Para suporte, envie um email para suporte@hoztech.com 