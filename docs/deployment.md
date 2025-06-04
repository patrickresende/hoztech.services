# Sistema de Deploy

Este documento detalha o sistema de deploy automatizado para o Render.com.

## 📋 Pré-requisitos

- Python 3.11+
- Conta no Render.com
- API Key do Render
- ID do serviço no Render
- Git configurado

## 🔧 Configuração

### Variáveis de Ambiente

```bash
RENDER_API_KEY=seu_api_key
RENDER_SERVICE_ID=seu_service_id
```

### Arquivos de Configuração

1. `render.yaml` - Configuração do serviço Render
2. `Procfile` - Comandos de inicialização
3. `requirements.txt` - Dependências Python

## 🚀 Scripts de Deploy

### Windows (deploy.bat)

```bash
scripts\deployment\deploy.bat <project_dir>
```

### Linux/Mac (deploy.sh)

```bash
./scripts/deployment/deploy.sh <project_dir>
```

### Python Direto (deploy.py)

```bash
python scripts/deployment/deploy.py <project_dir>
```

## 🔄 Processo de Deploy

1. **Verificação do Git**
   - Verifica mudanças não commitadas
   - Verifica se o branch está atualizado

2. **Testes Automatizados**
   - Executa suite de testes
   - Verifica cobertura de código

3. **Backup**
   - Cria backup do banco de dados
   - Armazena em S3 (se configurado)

4. **Deploy no Render**
   - Verifica serviço
   - Dispara deploy
   - Monitora progresso
   - Verifica status final

## 📊 Monitoramento

### Durante o Deploy

- Status do deploy em tempo real
- Logs do processo
- Métricas de tempo

### Pós-Deploy

- Verificação de saúde
- Testes de endpoint
- Monitoramento de recursos

## ⚠️ Tratamento de Erros

### Tipos de Erro

1. **Erros de Git**
   - Mudanças não commitadas
   - Branch desatualizado

2. **Erros de Teste**
   - Falhas nos testes
   - Cobertura insuficiente

3. **Erros de Backup**
   - Falha na conexão com S3
   - Espaço insuficiente

4. **Erros de Deploy**
   - Timeout
   - Falha na build
   - Erro de configuração

### Recuperação

1. **Rollback Automático**
   - Restauração do último backup
   - Reversão do deploy

2. **Logs**
   - Registro detalhado em `deployment.log`
   - Stacktrace de erros

## 🔐 Segurança

### Boas Práticas

1. **Credenciais**
   - Uso de variáveis de ambiente
   - Rotação regular de API keys

2. **Backups**
   - Criptografia em trânsito
   - Armazenamento seguro

3. **Logs**
   - Sanitização de dados sensíveis
   - Retenção apropriada

## 📝 Logs

### Localização

- `deployment.log` - Log principal
- Console output em tempo real

### Formato

```
YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE
```

### Níveis

- INFO: Informações gerais
- WARNING: Avisos importantes
- ERROR: Erros críticos
- DEBUG: Informações detalhadas

## 🔍 Troubleshooting

### Problemas Comuns

1. **API Key Inválida**
   ```
   Error: Invalid API key
   Solution: Verifique RENDER_API_KEY
   ```

2. **Service ID Incorreto**
   ```
   Error: Service not found
   Solution: Verifique RENDER_SERVICE_ID
   ```

3. **Timeout no Deploy**
   ```
   Error: Deploy timeout
   Solution: Aumente o timeout ou verifique a build
   ```

### Verificações

1. **Pré-Deploy**
   ```bash
   python scripts/test_render_deployment.py check
   ```

2. **Status do Serviço**
   ```bash
   python scripts/test_render_deployment.py status
   ```

## 📈 Métricas

### Deploy

- Tempo total de deploy
- Taxa de sucesso
- Frequência de deploys

### Performance

- Tempo de build
- Uso de recursos
- Tempo de inicialização

## 🔄 Integração Contínua

### GitHub Actions

```yaml
name: Deploy to Render
on:
  push:
    branches: [ main ]
```

### GitLab CI

```yaml
deploy:
  stage: deploy
  script:
    - python scripts/deployment/deploy.py .
```

## 📚 Referências

- [Documentação do Render](https://render.com/docs)
- [API do Render](https://api-docs.render.com)
- [Guia de Deploy Django](https://docs.djangoproject.com/en/stable/howto/deployment/) 