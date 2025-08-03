# Migração para SQLite - HOZ TECH

## Visão Geral

Este documento descreve as alterações realizadas para migrar o sistema HOZ TECH de PostgreSQL para SQLite. A migração foi realizada para simplificar o ambiente de desenvolvimento e produção, eliminando a necessidade de um servidor de banco de dados PostgreSQL.

## Alterações Realizadas

### 1. Configuração do Banco de Dados

- Modificado o arquivo `settings.py` para usar exclusivamente SQLite em todos os ambientes
- Removida a dependência do PostgreSQL (`psycopg2-binary`) do arquivo `requirements.txt`
- Configurado o SQLite com otimizações para melhor desempenho

### 2. Configuração de Deployment

- Atualizado o arquivo `render.yaml` para remover referências ao PostgreSQL
- Removida a configuração de banco de dados PostgreSQL do Render
- Ajustado o processo de build e deploy para trabalhar com SQLite

### 3. Controle de Versão

- Modificado o arquivo `.gitignore` para não ignorar o arquivo de banco de dados SQLite
- Mantido o arquivo `.gitattributes` sem alterações

## Configuração do Ambiente

### Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:

```
# Configurações Gerais
DEBUG=False
ENVIRONMENT=production
DJANGO_SECRET_KEY=your-secret-key-here

# Configurações de Host
ALLOWED_HOSTS=localhost,127.0.0.1,hoztech.com.br,www.hoztech.com.br
CSRF_TRUSTED_ORIGINS=https://localhost,https://127.0.0.1,https://hoztech.com.br,https://www.hoztech.com.br

# Configurações de Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
DEFAULT_FROM_EMAIL=seu-email@gmail.com
CONTACT_EMAIL=seu-email@gmail.com
```

## Comandos para Inicialização

### Desenvolvimento Local

```bash
# Ativar ambiente virtual
# Windows
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (se necessário)
python manage.py createsuperuser

# Iniciar servidor de desenvolvimento
python manage.py runserver
```

### Produção (Render)

O deploy no Render será feito automaticamente a partir do repositório Git. Certifique-se de que o arquivo `db.sqlite3` esteja incluído no repositório.

## Backup e Restauração

### Backup

Para fazer backup do banco de dados SQLite:

```bash
# Copiar o arquivo db.sqlite3
cp db.sqlite3 db.sqlite3.backup
```

### Restauração

Para restaurar o banco de dados a partir de um backup:

```bash
# Restaurar a partir do backup
cp db.sqlite3.backup db.sqlite3
```

## Considerações de Segurança

- O arquivo SQLite deve ter permissões adequadas para evitar acesso não autorizado
- Backups regulares são essenciais, especialmente em ambiente de produção
- Considere criptografar o arquivo SQLite em ambientes sensíveis

## Limitações do SQLite

- Suporta apenas um escritor por vez (não é adequado para alta concorrência)
- Limite de tamanho prático de aproximadamente 100GB
- Não suporta algumas funcionalidades avançadas do PostgreSQL

## Suporte e Manutenção

Para questões relacionadas à migração ou problemas com o banco de dados SQLite, entre em contato com a equipe de desenvolvimento.