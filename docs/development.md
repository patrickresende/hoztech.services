# 👨‍💻 Guia de Desenvolvimento

Este documento contém as diretrizes e boas práticas para desenvolvimento no projeto HOZ TECH.

## 📋 Pré-requisitos

### Software

- Python 3.11+
- Node.js 18+
- Git
- VSCode (recomendado)
- Redis (opcional)
- PostgreSQL (opcional)

### Extensões VSCode Recomendadas

- Python
- Django
- ESLint
- Prettier
- GitLens
- Live Server

## 🚀 Configuração do Ambiente

### Windows

```powershell
# Clone o repositório
git clone https://github.com/seu-usuario/hoz-tech.git
cd hoz-tech

# Crie e ative o ambiente virtual
python -m venv .hoztech
.hoztech\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
npm install

# Configure o ambiente
copy .env.example .env
```

### Linux/Mac

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/hoz-tech.git
cd hoz-tech

# Crie e ative o ambiente virtual
python -m venv .hoztech
source .hoztech/bin/activate

# Instale as dependências
pip install -r requirements.txt
npm install

# Configure o ambiente
cp .env.example .env
```

## 🔧 Configuração do Projeto

### Variáveis de Ambiente

```bash
# .env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Banco de Dados

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

## 📝 Padrões de Código

### Python

```python
# Exemplo de classe
class UserProfile:
    """
    Classe para gerenciar perfis de usuário.
    """
    def __init__(self, user):
        self.user = user

    def get_full_name(self):
        """Retorna o nome completo do usuário."""
        return f"{self.user.first_name} {self.user.last_name}"
```

### JavaScript

```javascript
// Exemplo de função
const toggleMenu = () => {
  const menu = document.querySelector('.navbar-collapse');
  if (menu) {
    menu.classList.toggle('show');
  }
};
```

### CSS

```css
/* Exemplo de componente */
.navbar {
  /* Use variáveis CSS */
  background: var(--tech-dark);
  border-bottom: 2px solid var(--tech-blue);
  
  /* Prefira unidades relativas */
  padding: 0.5rem 0;
  
  /* Organize propriedades */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1030;
}
```

## 🧪 Testes

### Unittest

```python
from django.test import TestCase

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_profile_creation(self):
        profile = UserProfile(self.user)
        self.assertEqual(profile.user, self.user)
```

### Coverage

```bash
# Executar testes com coverage
coverage run manage.py test

# Gerar relatório
coverage report

# Gerar relatório HTML
coverage html
```

## 🔍 Debugging

### Django Debug Toolbar

```python
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

### Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

## 📦 Gerenciamento de Dependências

### Python

```bash
# Adicionar dependência
pip install package-name

# Atualizar requirements.txt
pip freeze > requirements.txt

# Instalar em ambiente de desenvolvimento
pip install -r requirements.dev.txt
```

### Node.js

```bash
# Adicionar dependência
npm install package-name

# Adicionar dependência de desenvolvimento
npm install --save-dev package-name

# Atualizar dependências
npm update
```

## 🔄 Controle de Versão

### Branches

- `main`: Produção
- `develop`: Desenvolvimento
- `feature/*`: Novas funcionalidades
- `bugfix/*`: Correções de bugs
- `hotfix/*`: Correções urgentes

### Commits

```bash
# Formato
<tipo>(<escopo>): <descrição>

# Exemplos
feat(auth): adiciona autenticação 2FA
fix(navbar): corrige comportamento do menu mobile
docs(readme): atualiza instruções de instalação
```

## 🚀 Deploy Local

### Desenvolvimento

```bash
# Servidor de desenvolvimento
python manage.py runserver

# Compilar assets
npm run dev
```

### Produção Local

```bash
# Coletar arquivos estáticos
python manage.py collectstatic

# Servidor de produção
gunicorn hoztechsite.wsgi:application
```

## 📝 Documentação

### Docstrings

```python
def calculate_total(items):
    """
    Calcula o total de uma lista de itens.

    Args:
        items (list): Lista de itens com preço.

    Returns:
        float: Soma total dos preços.

    Raises:
        ValueError: Se algum item não tiver preço.
    """
    return sum(item.price for item in items)
```

### Templates

```html
{% extends 'base.html' %}

{% block content %}
<!-- Adicione comentários explicativos -->
{# Seção principal da página #}
<main class="container">
    <h1>{{ page_title }}</h1>
    {% include 'components/feature_list.html' %}
</main>
{% endblock %}
```

## 🔐 Segurança

### Checklist

1. Nunca commite:
   - Chaves secretas
   - Credenciais
   - Arquivos .env
   - Logs
   - Cache

2. Sempre use:
   - HTTPS em produção
   - CSRF tokens
   - Sanitização de input
   - Prepared statements

## 🎨 UI/UX

### Design System

- Cores definidas em variáveis CSS
- Tipografia consistente
- Componentes reutilizáveis
- Animações suaves
- Design responsivo

### Acessibilidade

- ARIA labels
- Alt text em imagens
- Contraste adequado
- Navegação por teclado
- HTML semântico

## 📚 Recursos

### Documentação

- [Django Docs](https://docs.djangoproject.com/)
- [Bootstrap Docs](https://getbootstrap.com/docs/)
- [MDN Web Docs](https://developer.mozilla.org/)

### Ferramentas

- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/) 