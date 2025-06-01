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

### Passos para Deploy

1. **Preparação do Repositório**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/seu-repositorio.git
   git push -u origin main
   ```

2. **Configuração no Render**
   - Acesse [dashboard.render.com](https://dashboard.render.com)
   - Clique em "New +"
   - Selecione "Web Service"
   - Conecte com seu repositório GitHub
   - Configure as variáveis de ambiente:
     - `DATABASE_URL`: URL do seu banco PostgreSQL
     - `SECRET_KEY`: Sua chave secreta Django
     - `DEBUG`: False
     - `ALLOWED_HOSTS`: seu-app.onrender.com

3. **Banco de Dados**
   - No Render, crie um novo PostgreSQL database
   - Copie a URL de conexão
   - Adicione como `DATABASE_URL` nas variáveis de ambiente

4. **Deploy**
   - O Render vai detectar o arquivo `render.yaml`
   - Build e deploy automático será iniciado
   - Acompanhe os logs para verificar o progresso

### Arquivos de Configuração
- `render.yaml`: Configuração do serviço
- `requirements.txt`: Dependências Python
- `Procfile`: Comando para iniciar a aplicação
- `.gitignore`: Arquivos ignorados no Git

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