# HOZ TECH Shop - Estrutura de Templates

Esta pasta contém os templates para a seção de loja da HOZ TECH, que redireciona para `shop.hoztech.com.br`.

## Arquivos Criados

### 1. `shop.html`
- **Propósito**: Template principal de redirecionamento para a loja
- **URL**: `/loja/`
- **Funcionalidades**:
  - Design responsivo com animações
  - Contador regressivo de lançamento
  - Efeitos visuais de partículas
  - Botão de redirecionamento para `https://shop.hoztech.com.br`
  - Seções destacando produtos digitais, serviços premium e cursos

### 2. `index.html`
- **Propósito**: Página principal da shop com categorias de produtos
- **URL**: `/shop/`
- **Funcionalidades**:
  - Grid de categorias de produtos
  - Cards interativos com animações
  - Links para diferentes seções da loja externa
  - Design moderno com gradientes e efeitos visuais
  - Seção de redirecionamento para loja completa

### 3. `products.html`
- **Propósito**: Página de produtos com filtros e showcase
- **Funcionalidades**:
  - Sistema de filtros por categoria
  - Cards de produtos com informações detalhadas
  - Produtos disponíveis e "em breve"
  - Animações de entrada e transições
  - Design responsivo mobile-first

## Categorias de Produtos

### Disponíveis
1. **Templates & Temas**
   - Templates profissionais para sites
   - Landing pages responsivas
   - Designs modernos

2. **Plugins & Extensões**
   - Plugins para WordPress
   - Extensões para Shopify
   - Funcionalidades avançadas

3. **Serviços Digitais**
   - Desenvolvimento personalizado
   - Consultoria técnica
   - Suporte especializado

### Em Desenvolvimento
1. **Cursos Online**
   - Programação
   - Design
   - Marketing digital

2. **Ferramentas Digitais**
   - Software de produtividade
   - Ferramentas de design
   - Utilitários de desenvolvimento

3. **E-books & Guias**
   - Materiais educativos
   - Guias técnicos
   - Documentação especializada

## Views Criadas

### `shop_index(request)`
- **Template**: `shop/index.html`
- **URL**: `/shop/`
- **Contexto**: Categorias de produtos, URLs da loja, metadados SEO

### `shop_redirect(request)`
- **Template**: `shop/shop.html`
- **URL**: `/loja/`
- **Contexto**: URL de redirecionamento, metadados

## URLs Configuradas

```python
# Shop URLs
path('shop/', views.shop_index, name='shop_index'),
path('loja/', views.shop_redirect, name='shop_redirect'),
```

## Integração com o Site

### Navbar
- Link "SHOP" adicionado na navegação principal
- Ícone: `bi bi-shop`
- Estado ativo para páginas da shop

### Rodapé
- Link "Loja Online" adicionado na seção de links úteis
- Redirecionamento para página principal da shop

## Características Técnicas

### Design
- **Mobile-first**: Responsivo para todos os dispositivos
- **Gradientes**: Uso de cores da identidade HOZ TECH
- **Animações**: Transições suaves e efeitos visuais
- **Tipografia**: Hierarquia clara e legibilidade otimizada

### Performance
- **CSS otimizado**: Estilos inline para carregamento rápido
- **Lazy loading**: Imagens e elementos carregados sob demanda
- **Animações GPU**: Uso de `transform` e `opacity` para performance

### SEO
- **Meta tags**: Descrições e palavras-chave otimizadas
- **Open Graph**: Metadados para redes sociais
- **Canonical URLs**: Links canônicos para SEO
- **Structured data**: Preparado para dados estruturados

### Acessibilidade
- **ARIA labels**: Atributos de acessibilidade
- **Navegação por teclado**: Suporte completo
- **Contraste**: Cores com contraste adequado
- **Semântica**: HTML semântico e estruturado

## Próximos Passos

1. **Implementar loja externa**: Desenvolver `shop.hoztech.com.br`
2. **Adicionar produtos reais**: Substituir produtos de exemplo
3. **Sistema de pagamento**: Integrar gateway de pagamento
4. **Dashboard admin**: Painel para gerenciar produtos
5. **Analytics**: Implementar tracking de conversões

## Manutenção

- **Atualizar produtos**: Modificar contexto nas views
- **Adicionar categorias**: Expandir lista de categorias
- **Melhorar SEO**: Otimizar meta tags e conteúdo
- **Performance**: Monitorar e otimizar carregamento

---

**Desenvolvido por HOZ TECH**  
*Soluções tecnológicas inovadoras*