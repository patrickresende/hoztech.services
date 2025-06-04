# Sistema de Backup

Este documento detalha o sistema de backup automatizado com integração S3.

## 📋 Pré-requisitos

- Python 3.11+
- Conta AWS (para S3)
- Credenciais AWS configuradas
- Acesso ao banco de dados

## 🔧 Configuração

### Variáveis de Ambiente

```bash
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
AWS_DEFAULT_REGION=sua_regiao
S3_BUCKET_NAME=seu_bucket
DB_BACKUP_PATH=/caminho/backups
```

### Configuração AWS

1. Criar bucket S3
2. Configurar lifecycle rules
3. Configurar encryption
4. Configurar IAM permissions

## 🚀 Scripts

### Backup (backup.py)

```bash
python scripts/backup/backup.py <project_dir> [s3_bucket]
```

### Restauração (restore.py)

```bash
python scripts/backup/restore.py <project_dir> <backup_name> [s3_bucket]
```

## 🔄 Processo de Backup

### 1. Preparação

- Verificação de permissões
- Criação de diretório temporário
- Validação de conexões

### 2. Banco de Dados

- Dump do PostgreSQL
- Compressão do arquivo
- Validação do dump

### 3. Arquivos

- Backup de media files
- Backup de configurações
- Backup de logs importantes

### 4. Upload S3

- Compressão final
- Upload encriptado
- Verificação de integridade

### 5. Limpeza

- Remoção de arquivos temporários
- Atualização de logs
- Notificação de conclusão

## 📊 Monitoramento

### Logs

- Localização: `backup.log`
- Rotação automática
- Níveis de log configuráveis

### Métricas

- Tamanho do backup
- Tempo de execução
- Taxa de sucesso
- Uso de recursos

## ⚠️ Tratamento de Erros

### Tipos de Erro

1. **Erros de Banco**
   - Conexão falhou
   - Dump falhou
   - Espaço insuficiente

2. **Erros de S3**
   - Credenciais inválidas
   - Bucket não existe
   - Upload falhou

3. **Erros de Sistema**
   - Permissões insuficientes
   - Espaço em disco
   - Timeout

### Recuperação

1. **Retry Automático**
   - Tentativas configuráveis
   - Backoff exponencial
   - Notificação de falha

2. **Validação**
   - Checksum dos arquivos
   - Teste de restauração
   - Verificação de integridade

## 🔐 Segurança

### Encriptação

1. **Em Trânsito**
   - SSL/TLS para S3
   - Verificação de certificados

2. **Em Repouso**
   - AES-256 no S3
   - Encriptação de senhas

### Acesso

1. **AWS**
   - IAM roles mínimas
   - Rotação de credenciais
   - MFA quando possível

2. **Local**
   - Permissões de arquivo
   - Segregação de usuários
   - Audit trail

## 📝 Retenção

### Políticas

1. **Local**
   - Últimos 7 dias
   - Rotação automática
   - Compressão progressiva

2. **S3**
   - 30 dias em Standard
   - 60 dias em IA
   - 365 dias em Glacier

### Limpeza

- Remoção automática
- Verificação de dependências
- Logging de exclusões

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de Credenciais**
   ```
   Error: Invalid AWS credentials
   Solution: Verifique AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY
   ```

2. **Erro de Permissão**
   ```
   Error: Permission denied
   Solution: Verifique IAM roles e políticas do bucket
   ```

3. **Erro de Espaço**
   ```
   Error: No space left on device
   Solution: Limpe diretório temporário ou aumente espaço
   ```

### Verificações

1. **Teste de Backup**
   ```bash
   python scripts/backup/test_backup.py
   ```

2. **Verificação de Configuração**
   ```bash
   python scripts/backup/check_config.py
   ```

## 📈 Relatórios

### Diário

- Status dos backups
- Tamanho total
- Erros encontrados
- Tempo de execução

### Mensal

- Tendências de crescimento
- Uso de recursos
- Custos de armazenamento
- Recomendações

## 🔄 Automação

### Cron

```bash
# Backup diário às 2 AM
0 2 * * * /usr/bin/python /path/to/scripts/backup/backup.py
```

### Systemd Timer

```ini
[Unit]
Description=Daily backup

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

## 📚 Referências

- [Documentação AWS S3](https://docs.aws.amazon.com/s3)
- [PostgreSQL Backup](https://www.postgresql.org/docs/current/backup.html)
- [Python Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) 