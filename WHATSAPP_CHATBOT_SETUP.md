# 🤖 Sistema de Chatbot WhatsApp - HOZ TECH

## 📋 Visão Geral

Sistema de chatbot automatizado para WhatsApp Web integrado ao site da HOZ TECH. O sistema oferece:

- ✅ **Backend seguro** sem renderização de links públicos
- ✅ **Filtragem automática** de contatos da sua lista pessoal
- ✅ **Sessões automatizadas** com templates personalizáveis
- ✅ **Dashboard administrativo** para gerenciamento
- ✅ **Logs detalhados** de todas as interações

## 🔧 Configuração Inicial

### 1. Migrações do Banco de Dados
```bash
python manage.py makemigrations core --name whatsapp_chatbot
python manage.py migrate
```

### 2. Ativação do Sistema
```bash
# Ativar o chatbot
python manage.py whatsapp_chatbot activate

# Configurar token de verificação do webhook
python manage.py whatsapp_chatbot set_config --key webhook_verify_token --value "seu_token_seguro"

# Verificar status
python manage.py whatsapp_chatbot status
```

## 🌐 Endpoints Disponíveis

### Webhook do WhatsApp
- **URL**: `http://127.0.0.1:8000//chatbot/webhook/`
- **Métodos**: GET (verificação), POST (receber mensagens)
- **Uso**: Configurar no WhatsApp Business API

### Dashboard Administrativo (Requer Login)
- **URL**: `/chatbot/dashboard/`
- **Método**: GET
- **Retorna**: Estatísticas e dados do chatbot

### Gerenciamento de Contatos (Requer Login)
- **URL**: `/chatbot/contacts/`
- **Métodos**: GET (listar), POST (adicionar/atualizar)

### Templates de Mensagem (Requer Login)
- **URL**: `/chatbot/templates/`
- **Métodos**: GET (listar), POST (criar/atualizar)

### Configurações (Requer Login)
- **URL**: `/chatbot/config/`
- **Métodos**: GET (obter), POST (atualizar)

### Health Check
- **URL**: `/chatbot/health/`
- **Método**: GET
- **Uso**: Verificar status do sistema

## 📱 Configuração do WhatsApp Business API

### 1. Webhook Configuration
```
URL do Webhook: https://seudominio.com/chatbot/webhook/
Token de Verificação: hoz_tech_secure_token_2024
```

### 2. Campos de Webhook
Marque os seguintes campos:
- ✅ messages
- ✅ message_deliveries
- ✅ message_reads

## 🎯 Gerenciamento de Contatos

### Adicionar Contato à Lista de Filtros
```bash
python manage.py whatsapp_chatbot add_contact --phone "5511999999999" --name "João Silva"
```

### Bloquear Contato
```bash
python manage.py whatsapp_chatbot block_contact --phone "5511999999999"
```

## 📝 Criação de Templates

### Template de Boas-vindas (Passo 0)
```bash
python manage.py whatsapp_chatbot create_template \
  --name "Boas-vindas" \
  --step 0 \
  --content "🤖 Olá! Sou o assistente virtual da HOZ TECH!" \
  --delay 3
```

### Template de Informações (Passo 1)
```bash
python manage.py whatsapp_chatbot create_template \
  --name "Serviços" \
  --step 1 \
  --content "🚀 Nossos serviços incluem..." \
  --delay 5
```

## 🔒 Segurança

### Filtragem de Contatos
O sistema automaticamente filtra:
- ✅ Contatos marcados como `is_my_contact=True`
- ✅ Contatos bloqueados (`is_blocked=True`)
- ✅ Números na sua lista pessoal

### Autenticação
- ✅ Endpoints administrativos requerem login
- ✅ Webhook protegido por token de verificação
- ✅ Logs de todas as atividades

## 📊 Monitoramento

### Verificar Estatísticas
```bash
python manage.py whatsapp_chatbot stats
```

### Limpeza de Dados Antigos
```bash
# Remover sessões com mais de 7 dias
python manage.py whatsapp_chatbot cleanup --days 7
```

## 🔧 Configurações Importantes

| Configuração | Descrição | Valor Padrão |
|--------------|-----------|--------------|
| `chatbot_active` | Ativar/desativar chatbot | `false` |
| `auto_response_delay` | Delay entre mensagens (segundos) | `5` |
| `max_session_duration` | Duração máxima da sessão (segundos) | `3600` |
| `webhook_verify_token` | Token de verificação do webhook | `default_token` |

## 📈 Fluxo de Funcionamento

1. **Mensagem Recebida** → Webhook `/chatbot/webhook/`
2. **Verificação de Filtro** → Contato está na lista pessoal?
3. **Criação de Sessão** → Nova sessão ou sessão existente
4. **Template Matching** → Buscar template para o passo atual
5. **Resposta Automática** → Enviar mensagem baseada no template
6. **Log de Atividade** → Registrar toda a interação

## 🚨 Troubleshooting

### Chatbot não responde
```bash
# Verificar se está ativo
python manage.py whatsapp_chatbot status

# Ativar se necessário
python manage.py whatsapp_chatbot activate
```

### Webhook não funciona
1. Verificar URL do webhook
2. Confirmar token de verificação
3. Verificar logs: `/chatbot/health/`

### Contatos não sendo filtrados
```bash
# Adicionar contato à lista de filtros
python manage.py whatsapp_chatbot add_contact --phone "NUMERO" --name "NOME"
```

## 📞 Suporte

Para suporte técnico, acesse o dashboard administrativo em `/chatbot/dashboard/` ou verifique os logs do sistema.

---

**🔐 IMPORTANTE**: Este sistema é completamente backend, sem renderização de links públicos, garantindo máxima segurança para seu serviço.