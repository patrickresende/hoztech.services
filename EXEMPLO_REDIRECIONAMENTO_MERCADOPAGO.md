# Redirecionamento Automático Mercado Pago

## Como Funciona

O sistema agora possui duas opções para integração com Mercado Pago:

### 1. Retorno JSON (para AJAX)
**URL:** `/payments/create_preference/`
**Uso:** Para implementações com JavaScript que fazem fetch e redirecionam via JS

```javascript
fetch('/payments/create_preference/?title=Produto&price=100.00')
    .then(response => response.json())
    .then(data => {
        if (data.init_point) {
            window.location.href = data.init_point;
        }
    });
```

### 2. Redirecionamento Automático (Recomendado)
**URL:** `/payments/redirect/`
**Uso:** Para links diretos que redirecionam automaticamente

```html
<a href="/payments/redirect/?title=Produto&price=100.00" class="btn-comprar">
    Comprar Agora
</a>
```

## Parâmetros

- `title`: Nome do produto/serviço
- `price`: Preço em formato decimal (ex: 99.90)

## Exemplos de Uso

### Botão Simples
```html
<a href="/payments/redirect/?title=Template%20E-commerce&price=299.00" class="btn">
    Comprar Template - R$ 299,00
</a>
```

### Card de Produto
```html
<div class="product-card">
    <h3>Desenvolvimento Personalizado</h3>
    <p class="price">R$ 2.500,00</p>
    <a href="/payments/redirect/?title=Desenvolvimento%20Personalizado&price=2500.00" class="btn-primary">
        Contratar Serviço
    </a>
</div>
```

### Com JavaScript (Opcional)
```html
<button onclick="comprarProduto('Mentoria Técnica', 150.00)">
    Comprar Mentoria
</button>

<script>
function comprarProduto(titulo, preco) {
    const url = `/payments/redirect/?title=${encodeURIComponent(titulo)}&price=${preco}`;
    window.location.href = url;
}
</script>
```

## Funcionamento Técnico

1. **Teste (Development):** Usa `sandbox_init_point` do Mercado Pago
2. **Produção:** Usa `init_point` do Mercado Pago
3. **Redirecionamento:** HTTP 302 direto para o checkout
4. **URLs de Retorno:** Configuradas automaticamente para success/failure/pending

## Vantagens

✅ **Simplicidade:** Um link direto, sem JavaScript necessário
✅ **Compatibilidade:** Funciona em qualquer navegador
✅ **Performance:** Redirecionamento direto, sem etapas intermediárias
✅ **SEO Friendly:** Links podem ser indexados
✅ **Mobile:** Funciona perfeitamente em dispositivos móveis

## Migração

### Antes (com JavaScript)
```html
<a href="/payments/create_preference/?title=Produto&price=100" 
   onclick="processPayment(this.href); return false;">
    Comprar
</a>
```

### Depois (redirecionamento direto)
```html
<a href="/payments/redirect/?title=Produto&price=100">
    Comprar
</a>
```

## Testado e Funcionando

- ✅ Ambiente de desenvolvimento (sandbox)
- ✅ Redirecionamento automático
- ✅ URLs de retorno configuradas
- ✅ Compatível com mobile
- ✅ Funciona sem JavaScript