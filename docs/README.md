# 📚 Documentação HOZ TECH

Bem-vindo à documentação do projeto HOZ TECH. Este diretório contém toda a documentação técnica e guias necessários para desenvolvimento, deploy e manutenção do projeto.

## 📑 Índice

1. [Roadmap](roadmap.md) - Planejamento futuro e melhorias
2. [Monitoramento](monitoring.md) - Sistema de monitoramento
3. [Backup](backup.md) - Sistema de backup
4. [Deploy](deployment.md) - Processo de deployment
5. [Arquitetura](architecture.md) - Arquitetura do sistema
6. [Desenvolvimento](development.md) - Guia de desenvolvimento

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- Git
- Redis (opcional)
- PostgreSQL (opcional)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/hoz-tech.git

# Entre no diretório
cd hoz-tech

# Crie um ambiente virtual
python -m venv .hoztech

# Ative o ambiente virtual
# Windows
.hoztech\Scripts\activate
# Linux/Mac
source .hoztech/bin/activate

# Instale as dependências
pip install -r requirements.txt
npm install

# Configure as variáveis de ambiente
cp .env.example .env

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

## 🏗️ Estrutura do Projeto

```
hoz-tech/
├── core/                   # Aplicação principal
│   ├── static/            # Arquivos estáticos
│   ├── templates/         # Templates Django
│   └── ...
├── docs/                  # Documentação
├── scripts/               # Scripts utilitários
└── hoztechsite/          # Configuração do projeto
```

## 🔧 Configuração

O projeto usa variáveis de ambiente para configuração. Copie `.env.example` para `.env` e configure as variáveis necessárias:

```bash
DEBUG=True
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Executar testes com coverage
coverage run manage.py test
coverage report
```

## 📦 Deploy

O projeto está configurado para deploy no Render.com. Veja [deployment.md](deployment.md) para mais detalhes.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.

## 📞 Suporte

- Email: suporte@hoztech.com.br
- Discord: [HOZ TECH Community](https://discord.gg/hoztech)
- GitHub Issues: [Issues](https://github.com/seu-usuario/hoz-tech/issues) 