# 🚀 Integração com WhatsApp Business Cloud API

## 📋 Pré-requisitos

### 1. Conta Facebook Developer
- Acesse [Facebook Developers](https://developers.facebook.com/)
- Crie uma conta de desenvolvedor
- Crie um novo App Business

### 2. WhatsApp Business Account
- Configure uma conta WhatsApp Business
- Adicione um número de telefone business

### 3. Sistema HOZ TECH
- ✅ Chatbot já implementado e funcionando
- ✅ Webhook endpoint configurado: `/chatbot/webhook/`
- ✅ Token de verificação: `hoz_tech_secure_token_2024`

## 🔧 Configuração no Facebook Developer

### Passo 1: Configurar WhatsApp Business API

1. **Acesse seu App no Facebook Developer Console**
2. **Adicione o produto "WhatsApp"**
3. **Configure o número de telefone business**

### Passo 2: Configurar Webhook

1. **Vá para WhatsApp > Configuration**
2. **Configure o Webhook URL:**
   ```
   https://seu-dominio.com/chatbot/webhook/
   ```
   
3. **Configure o Verify Token:**
   ```
   hoz_tech_secure_token_2024
   ```

4. **Subscreva aos eventos:**
   - ✅ messages
   - ✅ message_deliveries
   - ✅ message_reads
   - ✅ message_reactions

### Passo 3: Obter Tokens de Acesso

1. **Token Temporário (24h):**
   - Disponível na página "Getting Started"
   - Use para testes iniciais

2. **Token Permanente:**
   - Vá para "System Users" no Business Manager
   - Crie um System User
   - Gere um token permanente com permissões WhatsApp

## 🌐 Configuração do Servidor

### 1. Variáveis de Ambiente

Adicione ao seu arquivo `.env` ou configurações:

```env
# WhatsApp Business API
WHATSAPP_ACCESS_TOKEN=seu_token_permanente_aqui
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id
WHATSAPP_BUSINESS_ACCOUNT_ID=seu_business_account_id
WHATSAPP_APP_SECRET=seu_app_secret

# Webhook (já configurado)
WEBHOOK_VERIFY_TOKEN=hoz_tech_secure_token_2024
```

### 2. Configuração Django

Adicione ao `settings.py`:

```python
# WhatsApp Business API Settings
WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
WHATSAPP_APP_SECRET = os.getenv('WHATSAPP_APP_SECRET')
```

## 📡 Endpoints Disponíveis

### 1. Webhook (Já Implementado)
- **URL**: `/chatbot/webhook/`
- **Métodos**: GET (verificação), POST (receber mensagens)
- **Status**: ✅ Funcionando

### 2. Dashboard
- **URL**: `/chatbot/dashboard/`
- **Função**: Monitoramento em tempo real

### 3. Envio de Mensagens
- **URL**: `/chatbot/send/`
- **Método**: POST
- **Função**: Enviar mensagens via API

## 🔄 Fluxo de Integração

### 1. Verificação do Webhook
```
WhatsApp → GET /chatbot/webhook/ → Verificação do token → Resposta
```

### 2. Recebimento de Mensagens
```
WhatsApp → POST /chatbot/webhook/ → Processamento → Resposta automática
```

### 3. Envio de Mensagens
```
Sistema → WhatsApp API → Entrega → Status callback
```

## 🧪 Teste da Integração

### 1. Verificação do Webhook
```bash
# O WhatsApp fará esta requisição automaticamente
GET https://seu-dominio.com/chatbot/webhook/?hub.mode=subscribe&hub.verify_token=hoz_tech_secure_token_2024&hub.challenge=CHALLENGE_STRING
```

### 2. Teste de Mensagem
1. Envie uma mensagem para o número WhatsApp Business
2. Verifique os logs no dashboard: `/chatbot/dashboard/`
3. Confirme o recebimento no banco de dados

### 3. Teste de Resposta Automática
1. O sistema deve responder automaticamente
2. Verificar templates configurados
3. Monitorar sessões ativas

## 🔐 Segurança

### 1. Verificação de Assinatura
O sistema já implementa:
- ✅ Verificação do token webhook
- ✅ Validação de origem das requisições
- ✅ Filtragem automática de spam

### 2. Rate Limiting
- Configure limites de requisições
- Monitore uso da API
- Implemente cache quando necessário

## 📊 Monitoramento

### 1. Dashboard em Tempo Real
- Acesse: `/chatbot/dashboard/`
- Monitore mensagens, sessões e logs

### 2. Health Check
- Acesse: `/chatbot/health/`
- Verifique status do sistema

### 3. Logs Detalhados
- Todas as interações são registradas
- Análise de performance disponível

## 🚀 Deploy em Produção

### 1. Domínio HTTPS
- WhatsApp exige HTTPS
- Configure SSL/TLS
- Use serviços como Render, Heroku, ou AWS

### 2. Configuração de DNS
```
webhook.hoztech.com.br → seu-servidor
```

### 3. Variáveis de Produção
- Configure todas as variáveis de ambiente
- Use secrets manager para tokens
- Configure backup automático

## 📞 Suporte e Troubleshooting

### 1. Logs de Erro
```bash
# Verificar logs do Django
python manage.py whatsapp_chatbot status

# Verificar logs do webhook
tail -f logs/webhook.log
```

### 2. Problemas Comuns

**Webhook não verifica:**
- Confirme o token de verificação
- Verifique se o endpoint está acessível
- Confirme HTTPS funcionando

**Mensagens não chegam:**
- Verifique permissões da API
- Confirme subscription aos eventos
- Verifique rate limits

**Respostas não funcionam:**
- Confirme templates aprovados
- Verifique token de acesso
- Monitore logs de erro

### 3. Contato de Suporte
- Dashboard: `/chatbot/dashboard/`
- Health Check: `/chatbot/health/`
- Logs: Disponíveis no sistema

## 🎯 Próximos Passos

1. **Configure o domínio HTTPS**
2. **Obtenha os tokens da API**
3. **Configure o webhook no Facebook Developer**
4. **Teste a integração completa**
5. **Deploy em produção**
6. **Monitore e otimize**

---

**Sistema desenvolvido pela HOZ TECH** 🚀
**Status**: ✅ Pronto para integração
**Documentação**: Completa e atualizada