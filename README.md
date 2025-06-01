# HOZ TECH - Website Institucional

## 📋 Sobre o Projeto
Website institucional da Hoz Tech, uma empresa de tecnologia com foco em desenvolvimento web e propósito social. O projeto foi desenvolvido com Django e tecnologias modernas de frontend, oferecendo uma experiência de usuário fluida e responsiva.

## 🚀 Características Principais
- Design moderno e responsivo
- Carrossel de serviços interativo
- Sistema de contato integrado com Gmail SMTP
- Integração com WhatsApp
- Otimização SEO
- Acessibilidade
- Animações e efeitos visuais
- Tema tech com cores neon

## 🚀 Deploy no Render

### Pré-requisitos
- Conta no [Render](https://render.com)
- Repositório do projeto no GitHub
- PostgreSQL database

### Passo a Passo Detalhado

1. **Criar Database no Render**
   - Acesse o [Dashboard do Render](https://dashboard.render.com)
   - Clique em "New +" > "PostgreSQL"
   - Configure:
     - Nome: `hoztech-db`
     - Database: `hoztech`
     - User: `hoztech_admin`
     - Region: `São Paulo (Brazil)`
   - Anote a URL de conexão fornecida

2. **Configurar Web Service**
   - No Dashboard, clique em "New +" > "Web Service"
   - Conecte com seu repositório GitHub
   - Configure:
     - Nome: `hoz-tech`
     - Region: `São Paulo (Brazil)`
     - Branch: `main`
     - Root Directory: `./`
     - Runtime: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn core.wsgi:application`

3. **Configurar Environment Variables**
   ```
   DATABASE_URL=postgres://... (URL fornecida ao criar o database)
   SECRET_KEY=sua-chave-secreta-muito-segura
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   PYTHON_VERSION=3.8.2
   ```

4. **Configurar Domínio Personalizado (Opcional)**
   - Em "Settings" > "Custom Domain"
   - Adicione seu domínio
   - Siga as instruções para configurar os registros DNS

5. **Monitoramento**
   - Monitore os logs durante o deploy
   - Verifique se as migrações foram executadas
   - Confirme se os arquivos estáticos foram coletados

### Verificações Pós-Deploy

1. **Banco de Dados**
   ```bash
   # Verifique se as migrações foram aplicadas
   python manage.py showmigrations

   # Se necessário, aplique manualmente
   python manage.py migrate
   ```

2. **Arquivos Estáticos**
   ```bash
   # Colete os arquivos estáticos
   python manage.py collectstatic --noinput
   ```

3. **Testes de Funcionalidade**
   - [ ] Acesso à página inicial
   - [ ] Formulários funcionando
   - [ ] Emails sendo enviados
   - [ ] Banco de dados conectado
   - [ ] Arquivos estáticos carregando
   - [ ] Cookie manager funcionando

### Manutenção

1. **Monitoramento**
   - Configure alertas de uptime
   - Monitore o uso do banco de dados
   - Verifique os logs regularmente

2. **Backups**
   - Backup automático do banco de dados
   - Backup do código no GitHub
   - Documentação atualizada

3. **Atualizações**
   ```bash
   # Atualize dependências localmente primeiro
   pip install -r requirements.txt --upgrade
   
   # Teste localmente
   python manage.py runserver
   
   # Se tudo ok, commit e push
   git add .
   git commit -m "chore: atualização de dependências"
   git push origin main
   ```

### Troubleshooting

1. **Problemas Comuns**
   - Erro 500: Verifique os logs do Render
   - Erro 503: Verifique se o serviço está rodando
   - Estáticos não carregam: Verifique STATIC_ROOT e collectstatic
   - Banco de dados não conecta: Verifique DATABASE_URL

2. **Logs**
   - Acesse os logs no dashboard do Render
   - Use `print()` ou `logger` para debug
   - Verifique os logs do Gunicorn

3. **Rollback**
   - O Render mantém versões anteriores
   - Use git para reverter commits se necessário
   - Mantenha backups do banco de dados

### Links Úteis
- [Documentação do Render](https://render.com/docs)
- [Django no Render](https://render.com/docs/deploy-django)
- [Configuração do PostgreSQL](https://render.com/docs/databases)
- [Custom Domains](https://render.com/docs/custom-domains)

### Contatos de Suporte
- Suporte Render: support@render.com
- Nosso Email: suporte@hoztech.com.br
- WhatsApp: (21) 97300-7575

---
⚠️ **Importante**: Nunca compartilhe ou comite variáveis de ambiente (.env) ou credenciais!

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.8+
- Django 4.2.7
- Django REST Framework
- SQLite (desenvolvimento)
- PostgreSQL (produção)

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Swiper.js 11
- Bootstrap Icons

### Bibliotecas e Dependências
```txt
asgiref==3.7.2
Django==4.2.7
django-environ==0.11.2
gunicorn==21.2.0
packaging==23.2
psycopg2-binary==2.9.9
sqlparse==0.4.4
tzdata==2023.3
whitenoise==6.6.0
```

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- virtualenv ou venv
- Conta Gmail para envio de emails (opcional)

### Passo a Passo

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/hoz-tech.git
cd hoz-tech
```

2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
```bash
# Crie um arquivo .env na raiz do projeto
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# Configurações de Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
DEFAULT_FROM_EMAIL=seu-email@gmail.com
CONTACT_EMAIL=seu-email@gmail.com
```

5. Execute as migrações
```bash
python manage.py migrate
```

6. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

7. Crie os arquivos JavaScript necessários
```bash
# Crie o arquivo cookie_manager.js em static/js/
touch static/js/cookie_manager.js
```

8. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```

## 📱 Estrutura do Projeto

```
hoz-tech/
├── core/                   # Aplicação principal
│   ├── static/            # Arquivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/         # Templates HTML
│   ├── models.py         
│   ├── views.py
│   └── urls.py
├── hoztech/              # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/              # Arquivos estáticos coletados
├── media/              # Uploads de usuários
├── manage.py
├── requirements.txt
├── render.yaml        # Configuração Render
├── Procfile          # Configuração do servidor
└── README.md
```

## 🎨 Funcionalidades Principais

### Home Page
- Hero section com animações
- Seção de features
- Preview de serviços
- Call-to-action

### Página de Serviços
- Carrossel interativo
- 6 planos diferentes
- Preços e features
- Integração WhatsApp

### Sobre Nós
- História da empresa
- Missão, Visão e Valores
- Timeline interativa
- Estatísticas

### Contato
- Formulário de contato
- Validação em tempo real
- Feedback visual
- Proteção contra spam

## 🔒 Segurança
- CSRF Protection
- XSS Prevention
- Secure Headers
- Rate Limiting
- Form Validation

## 📱 Responsividade
- Mobile First Design
- Breakpoints:
  - 320px (smartphones pequenos)
  - 480px (smartphones)
  - 768px (tablets)
  - 1024px (desktops)
  - 1280px (telas grandes)

## ⚡ Performance
- Lazy Loading de imagens
- Minificação de CSS/JS
- Otimização de fontes
- Cache de templates
- Compressão Gzip

## 🌐 SEO
- Meta tags otimizadas
- Sitemap XML
- robots.txt
- URLs amigáveis
- Schema Markup

## 🔍 Testes
```bash
# Executar testes
python manage.py test

# Cobertura de testes
coverage run manage.py test
coverage report

# Testar configuração de email
python manage.py test_email
```

## 📦 Deploy
1. Configure as variáveis de ambiente de produção
2. Colete arquivos estáticos
```bash
python manage.py collectstatic
```
3. Configure o servidor web (Nginx/Apache)
4. Configure o banco de dados PostgreSQL
5. Use Gunicorn como servidor WSGI

## 🤝 Contribuindo
1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte
- Email: contato@hoztech.com.br
- WhatsApp: (21) 97300-7575
- Site: www.hoztech.com.br

## ✨ Agradecimentos
- Bootstrap Team
- Django Community
- Swiper.js Team
- Todos os contribuidores

## ⚠️ Problemas Conhecidos
- O arquivo `cookie_manager.js` precisa ser criado manualmente em `static/js/`
- Algumas imagens da equipe podem estar faltando em `static/images/team/`
- Certifique-se de configurar corretamente as variáveis de ambiente do email antes de usar o formulário de contato

---
Desenvolvido com 💙 por Hoz Tech 