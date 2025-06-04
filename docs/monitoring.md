# Sistema de Monitoramento

Este documento detalha o sistema de monitoramento para a aplicação Django no Render.com.

## 📋 Pré-requisitos

- Python 3.11+
- Conta no Render.com
- Acesso ao banco de dados
- Redis configurado

## 🔧 Configuração

### Variáveis de Ambiente

```bash
MONITOR_LOG_LEVEL=INFO
ALERT_EMAIL=alerts@seudominio.com
SLACK_WEBHOOK_URL=sua_url_webhook
REDIS_URL=redis://localhost:6379/0
```

### Métricas Monitoradas

1. **Sistema**
   - CPU Usage
   - Memória
   - Disco
   - Network I/O

2. **Aplicação**
   - Response Time
   - Error Rate
   - Request Rate
   - Active Users

3. **Banco de Dados**
   - Conexões
   - Query Time
   - Cache Hit Rate
   - Table Size

4. **Cache (Redis)**
   - Memory Usage
   - Hit Rate
   - Eviction Rate
   - Connected Clients

## 🚀 Scripts

### Monitor Principal (monitor.py)

```bash
python scripts/monitoring/monitor.py <app_url>
```

### Verificação de Saúde (health_check.py)

```bash
python scripts/monitoring/health_check.py <app_url>
```

## 🔄 Processo de Monitoramento

### 1. Coleta de Dados

- Métricas do sistema
- Logs da aplicação
- Métricas do Render
- Dados do banco

### 2. Processamento

- Agregação
- Cálculo de médias
- Detecção de anomalias
- Correlação de eventos

### 3. Armazenamento

- Time series database
- Log aggregation
- Métricas em Redis
- Backup de dados

### 4. Visualização

- Dashboards
- Gráficos em tempo real
- Relatórios
- Alertas visuais

## 📊 Dashboards

### Sistema

```
+----------------+----------------+
|     CPU       |    Memory     |
|   [Graph]     |    [Graph]    |
+----------------+----------------+
|     Disk      |   Network     |
|   [Graph]     |    [Graph]    |
+----------------+----------------+
```

### Aplicação

```
+----------------+----------------+
|  Response Time |   Error Rate  |
|   [Graph]     |    [Graph]    |
+----------------+----------------+
| Active Users  | Request Rate  |
|   [Graph]     |    [Graph]    |
+----------------+----------------+
```

## ⚠️ Alertas

### Níveis

1. **INFO**
   - Eventos normais
   - Métricas regulares
   - Updates do sistema

2. **WARNING**
   - Alta utilização
   - Latência aumentada
   - Erros não críticos

3. **ERROR**
   - Serviço down
   - Erros críticos
   - Falhas de backup

4. **CRITICAL**
   - Sistema indisponível
   - Perda de dados
   - Violações de segurança

### Canais

1. **Email**
   - Relatórios diários
   - Alertas críticos
   - Resumos semanais

2. **Slack**
   - Alertas em tempo real
   - Updates de deploy
   - Notificações de erro

3. **SMS**
   - Alertas críticos
   - Falhas de sistema
   - Problemas de segurança

## 🔍 Health Checks

### Endpoints

1. **/health**
   - Status geral
   - Tempo de resposta
   - Versão da aplicação

2. **/health/db**
   - Conexão com banco
   - Tempo de query
   - Migrations status

3. **/health/cache**
   - Status do Redis
   - Hit rate
   - Memory usage

### Verificações

```python
@api_view(['GET'])
def health_check(request):
    return {
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now()
    }
```

## 📈 Performance

### Métricas Chave

1. **Apdex Score**
   - Satisfeito: < 500ms
   - Tolerável: < 1500ms
   - Frustrante: > 1500ms

2. **Error Budget**
   - 99.9% uptime
   - 43.8 minutos/mês
   - Monitoramento contínuo

3. **SLOs**
   - Latência < 200ms
   - Erro rate < 0.1%
   - Disponibilidade 99.9%

## 🔐 Segurança

### Monitoramento

1. **Acessos**
   - Login attempts
   - Failed logins
   - Admin actions

2. **Vulnerabilidades**
   - SSL/TLS status
   - Security headers
   - Dependencies

3. **Compliance**
   - Audit logs
   - Data access
   - Retention policy

## 📝 Logs

### Estrutura

```json
{
  "timestamp": "2024-03-20T10:00:00Z",
  "level": "INFO",
  "service": "web",
  "message": "Request processed",
  "metadata": {
    "path": "/api/v1/users",
    "method": "GET",
    "duration_ms": 45
  }
}
```

### Retenção

- 7 dias: logs completos
- 30 dias: agregados
- 365 dias: métricas

## 🔄 Automação

### Cron Jobs

```bash
# Verificação a cada 5 minutos
*/5 * * * * /usr/bin/python /path/to/scripts/monitoring/health_check.py

# Relatório diário
0 0 * * * /usr/bin/python /path/to/scripts/monitoring/daily_report.py
```

### Systemd Service

```ini
[Unit]
Description=Application Monitoring

[Service]
ExecStart=/usr/bin/python /path/to/scripts/monitoring/monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📊 Relatórios

### Diário

- Uptime
- Error rate
- Performance
- Recursos

### Semanal

- Tendências
- Problemas
- Melhorias
- Custos

## 🔍 Troubleshooting

### Problemas Comuns

1. **Alto Response Time**
   ```
   Causa: Database queries lentas
   Solução: Otimizar queries, adicionar índices
   ```

2. **Memory Leak**
   ```
   Causa: Objetos não liberados
   Solução: Debug com memory profiler
   ```

3. **High CPU**
   ```
   Causa: Processos em loop
   Solução: Identificar e otimizar código
   ```

## 📚 Referências

- [Django Monitoring](https://docs.djangoproject.com/en/stable/howto/deployment/monitoring/)
- [Render Metrics API](https://api-docs.render.com)
- [Redis Monitoring](https://redis.io/topics/monitoring)
- [PostgreSQL Monitoring](https://www.postgresql.org/docs/current/monitoring.html) 