# HOZ TECH - Website

Site institucional da HOZ TECH, desenvolvido com Django 5.2 e otimizado para performance e segurança.

## 🚀 Características

- Design responsivo e moderno
- Otimização SEO
- SSL/HTTPS automático
- Cache com Redis
- Monitoramento em tempo real
- Backup automático
- API REST
- Painel administrativo personalizado

## 📋 Pré-requisitos

- Python 3.11+
- Redis
- PostgreSQL
- Git

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/hoztechsite.git
cd hoztechsite
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
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

7. Colete os arquivos estáticos:
```bash
python manage.py collectstatic
```

## 🏃‍♂️ Desenvolvimento

1. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

2. Para desenvolvimento com SSL:
```bash
python scripts/runserver_ssl.py
```

## 🚀 Deploy

### Render

1. Configure as variáveis de ambiente:
```bash
export RENDER_API_KEY=seu_api_key
export RENDER_SERVICE_ID=seu_service_id
```

2. Execute o script de deploy:
```bash
# Windows
scripts\deployment\deploy.bat .

# Linux/Mac
./scripts/deployment/deploy.sh .

# Ou diretamente com Python
python scripts/deployment/deploy.py .
```

### Testes de Deploy

```bash
# Windows
scripts\test_render_deployment.bat myapp.onrender.com

# Linux/Mac
./scripts/test_render_deployment.sh myapp.onrender.com

# Ou diretamente com Python
python scripts/test_render_deployment.py myapp.onrender.com
```

## 📊 Monitoramento

```bash
python scripts/monitoring/monitor.py myapp.onrender.com
```

## 💾 Backup

```bash
python scripts/backup/backup.py /caminho/do/projeto [s3_bucket]
```

## 🔄 Restauração

```bash
python scripts/backup/restore.py /caminho/do/projeto nome_do_backup [s3_bucket]
```

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
hoztechsite/
├── core/               # Aplicação principal
├── scripts/           # Scripts de utilidade
│   ├── backup/        # Scripts de backup
│   ├── deployment/    # Scripts de deploy
│   └── monitoring/    # Scripts de monitoramento
├── static/            # Arquivos estáticos
├── media/            # Uploads de usuários
├── templates/        # Templates HTML
└── docs/            # Documentação
```

### Comandos Úteis

```bash
# Testes
python manage.py test
pytest

# Lint
flake8
black .

# Coverage
pytest --cov=.
```

## 📝 Documentação

A documentação completa está disponível em `docs/` e inclui:
- Guia de Desenvolvimento
- Guia de Deploy
- Referência da API
- Guia de Segurança

## 🔐 Segurança

- SSL/TLS configurado
- Headers de segurança
- CSRF protection
- Rate limiting
- Backup automático
- Monitoramento

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## ✨ Contribuindo

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 