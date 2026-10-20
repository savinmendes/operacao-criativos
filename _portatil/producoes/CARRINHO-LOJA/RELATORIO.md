# Carrinho e compra: chileverificada.com (COD Chile)

Data: 09/10/2026 · Frente: COD Chile
Tema: **"BLACK FRIDAY - shr-co v4 (rascunho)"** (`167232798976`, NÃO publicado). O tema ao vivo não foi alterado.
Pré-visualização: https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml?preview_theme_id=167232798976

## 1. Como era o fluxo (auditoria)

| Ponto | O que encontrei |
|---|---|
| Botões na página de produto | Só o **"Pide y Paga al Recibir"** (Releasit) aparece. "Agregar al carrito" e "Comprar ahora" existem no HTML, mas o Releasit esconde os dois (`hideAddToCartButton` e `hideQuickCheckoutButtons` ligados). Não havia seletor de quantidade. |
| Ícone do carrinho | **Não existe.** O grupo do cabeçalho só tem a barra preta rolante, então o cliente não tinha como ver o carrinho. |
| Gaveta do carrinho (tema Shrine) | Está ligada (`cart_type: drawer`), mas com textos em inglês ("Cart reserved for…", "Spend [amount] more to get FREE shipping!", meta de 50) e um bloco de upsell apontando para um produto que não existe ("dasds"). |
| Página `/cart` | Funciona (adiciona, muda quantidade), mas o botão "Pagar pedido" leva ao checkout do Shopify. |
| Checkout do Shopify | Aparece **"Esta tienda no puede aceptar pagos en este momento"**: não há nenhum meio de pagamento ativo. Ele também soma IVA estimado ($11.381 sobre $59.900). Ou seja, **todo cliente que chegasse ao checkout ficava sem conseguir comprar.** |
| Releasit (formulário COD) | Na página de produto usa `addMode: "product-only"`: **ao clicar, o Releasit esvazia o carrinho** e pede só aquele produto. O modo de carrinho do app (`cartPage.isEnabled`) está **desligado**. Testei o formulário em modo carrinho (`normalCart`): ele abre com **todas as linhas do carrinho** e o total certo (2 kits + 1 perfume = $154.700). |
| Descontos automáticos | Nenhum desconto automático existe hoje. O Releasit está com `disableAutomaticDs: false`, ou seja, lê os descontos automáticos do carrinho. Mais detalhes na seção 5. |

Prints de antes: `antes_produto_{mobile,desktop}.png`, `antes_carrinho-pagina_{mobile,desktop}.png`.

## 2. O que mudou (3 arquivos no tema rascunho)

| Arquivo | Tipo | O que faz |
|---|---|---|
| `snippets/cv-carrito.liquid` | NOVO | Gaveta do carrinho nova, botão flutuante "Carrito (n)", "Agregar al carrito" com quantidade na página de produto, "Completa tu pedido" e o bloco de preço especial. Todos os ajustes ficam no topo do arquivo. |
| `templates/search.cvforn.liquid` | NOVO | Devolve em JSON os produtos de um fornecedor (busca por etiqueta). É a fonte do "Completa tu pedido". |
| `sections/scroll-to-top-btn.liquid` | EDITADO (+2 linhas no topo) | `{%- render 'cv-carrito' -%}`. É uma seção fixa que aparece em todas as páginas. Usei esta para não mexer no `layout/theme.liquid` nem no `header-group.json`. |

Não mexi em `templates/collection.perfumes-arabes.json` (outro agente), `snippets/bf-black-friday.liquid`, `sections/header-group.json`, `main-product.liquid`, templates de produto nem `settings_data.json`.

Os checksums no tema batem com os arquivos locais: `novos/` (cv-carrito `291566dd…`, search.cvforn `0a992bbd…`, scroll-to-top `d7f15efd…`). O original do scroll-to-top está em `backup/sections__scroll-to-top-btn.liquid` (md5 `dc6432a3…`, igual ao tema antes da mudança). Os outros 2 arquivos são novos e não tinham original.

### Página de produto
- Embaixo do botão verde do Releasit, que continua sendo o principal e não foi mexido, aparece: **[ − 1 + ] [ Agregar al carrito ]** (contorno preto) e a frase "Lleva más de uno en el mismo pedido y paga todo al recibir". Quando o carrinho já tem itens, a frase vira "Tienes N en tu carrito · Ver carrito".
- Ao adicionar, a gaveta abre.
- **Trava de fornecedor:** se o carrinho já tem um produto de outro fornecedor (ou sem etiqueta), o produto não é adicionado e aparece um aviso: "Este producto se despacha por separado… Pídelo aparte con «Pide y Paga al Recibir» o revisa tu carrito". Isso evita pedido com vários fornecedores, que nunca aconteceu na Dropi.
- Por padrão o botão só aparece em produtos que têm a etiqueta `forn-…` (`cv_atc_todos = false`). Nos outros produtos o fluxo do Releasit fica exatamente como era.

### Gaveta do carrinho
- Tem foto, título, quantidade (− +), "Eliminar", preço da linha (com o preço riscado se houver desconto) e "c/u" quando a quantidade passa de 1.
- Depois vêm Subtotal, Descuento (só se existir) e Total, além da linha "💵 Pago contra entrega · 🚚 Despacho a todo Chile".
- O CTA único é o verde **"Pide y Paga al Recibir"**, com a legenda "Total $X · pagas al recibir". Ele abre o formulário Releasit com o carrinho inteiro.
- "Pagar con tarjeta" está pronto, mas desligado (`cv_mostrar_checkout = false`), porque o checkout do Shopify não tem meio de pagamento.
- Um botão flutuante "Carrito (n)" aparece quando há itens (canto inferior esquerdo) e sobe se a barra fixa do Releasit estiver embaixo.
- Na página `/cart`, o "Pagar pedido" agora abre o formulário contra entrega em vez do checkout quebrado.
- A gaveta antiga do tema fica escondida por CSS.

## 3. Lógica do "Completa tu pedido" (mesmo fornecedor)
1. Para cada produto do carrinho, a gaveta lê as etiquetas (`/products/<handle>.js`) e procura a que começa com `forn-`.
2. Só continua se **todos** os itens tiverem a **mesma** etiqueta `forn-`. Se houver mistura ou algum item sem etiqueta, não mostra sugestões.
3. Busca os produtos com aquela etiqueta (`/search?q=forn-82275&options[fields]=tag&view=cvforn`, até 50) e confere de novo a etiqueta exata. Descarta os indisponíveis e os que já estão no carrinho.
4. Ordena pelos que compartilham mais etiquetas com o carrinho (ex.: `mujer`, `yara`). Ignora `kit`, `unitario`, `perfumes-arabes` e a própria `forn-`. Mostra **2**, cada um com "+ Agregar".
5. Quando o bloco de preço especial está ligado, os perfumes unitários vão para o bloco e as 2 sugestões ficam com os kits.

**Etiquetas aplicadas:** `forn-82275` nos 13 produtos Lattafa ativos (5 kits + 8 unitários), via `tagsAdd`.

**Como etiquetar outros produtos depois:** no Shopify admin → Produto → Etiquetas, adicione `forn-<ID do fornecedor na Dropi>`, por exemplo `forn-18419` para os kits de grife (Invictus etc.). Pode ser em massa: Produtos → selecionar → "Adicionar etiquetas". Use uma única etiqueta `forn-` por produto. Pronto: a página do produto passa a mostrar "Agregar al carrito" e o carrinho passa a sugerir os produtos do mesmo fornecedor. Os 2 packs antigos (`/products/lattafa` "Pack 3x1 Hombre Armaf + Lattafa + Afnan" e `/products/yara` "Pack 3x1 Mujer Yara + Fakhar Rose + Sabah Al Ward") **não foram etiquetados**, porque não confirmei o fornecedor deles na Dropi (precisa de revisão manual).

## 4. Bloco "Agrega un perfume por $X" (pronto, DESLIGADO)
- Fica no topo de `snippets/cv-carrito.liquid`: `assign bf_addon_precio = ''`. Vazio = bloco escondido. Se um dia existir uma configuração de tema `bf_addon_precio`, ela tem prioridade.
- Aparece quando: o preço está preenchido, o carrinho tem um produto `kit` de um único fornecedor e ainda não tem nenhum `unitario` desse fornecedor. Mostra um seletor com os perfumes unitários do mesmo fornecedor e o botão "Agregar".
- Texto: "Agrega un perfume por $X" / "Precio especial al llevar un kit en el mismo pedido."
- O preço da linha no carrinho vem do próprio Shopify (`final_line_price`): **sem o desconto criado, o carrinho cobra o preço cheio.** Por isso só preencha o X depois de criar o desconto.
- O print `depois_7_SIMULACAO-addon-19900_*.png` usa **$19.900 só como simulação visual**: o valor foi injetado no navegador do teste e nada foi gravado no tema. Não é preço definido.

### Desconto a criar (o agente principal roda depois que o dono confirmar X e que o fornecedor 82275 vende o unitário)
Passo A: criar 2 coleções automáticas (por etiqueta), para o desconto mirar por fornecedor:
```graphql
mutation criarColecoes {
  kits: collectionCreate(input: {
    title: "[desc] Kits forn-82275"
    handle: "desc-kits-forn-82275"
    ruleSet: { appliedDisjunctively: false, rules: [
      { column: TAG, relation: EQUALS, condition: "kit" },
      { column: TAG, relation: EQUALS, condition: "forn-82275" } ] }
  }) { collection { id handle } userErrors { field message } }
  unitarios: collectionCreate(input: {
    title: "[desc] Unitarios forn-82275"
    handle: "desc-unitarios-forn-82275"
    ruleSet: { appliedDisjunctively: false, rules: [
      { column: TAG, relation: EQUALS, condition: "unitario" },
      { column: TAG, relation: EQUALS, condition: "forn-82275" } ] }
  }) { collection { id handle } userErrors { field message } }
}
```
Passo B: desconto automático "compre 1 kit → leve 1 unitário com $ de desconto". O `valorOff` é **34900 − X** (o desconto é um valor fixo por unidade; se o preço do unitário mudar, recalcule):
```graphql
mutation criarDescontoAddon($kits: ID!, $unitarios: ID!, $valorOff: Decimal!) {
  discountAutomaticBxgyCreate(automaticBxgyDiscount: {
    title: "Kit + perfume a precio especial"
    startsAt: "2026-10-10T00:00:00-03:00"
    endsAt: null
    usesPerOrderLimit: "1"
    combinesWith: { productDiscounts: false, orderDiscounts: false, shippingDiscounts: true }
    customerBuys: { value: { quantity: "1" }, items: { collections: { add: [$kits] } } }
    customerGets: {
      value: { discountOnQuantity: { quantity: "1", effect: { amount: $valorOff } } }
      items: { collections: { add: [$unitarios] } }
    }
  }) {
    automaticDiscountNode { id automaticDiscount { ... on DiscountAutomaticBxgy { title status } } }
    userErrors { field code message }
  }
}
```
As duas operações foram validadas no schema do Admin API e **não foram executadas**. O `title` aparece para o cliente. O `usesPerOrderLimit: "1"` faz valer 1 perfume por pedido; para 1 por kit, troque para `null`. Passo C: preencher `bf_addon_precio` com X no snippet.

## 5. Releasit × descontos automáticos
- Pelo código do Releasit carregado na loja (`get-form-script`, versão 455): com `disableAutomaticDs: false` (configuração atual), ao abrir o formulário em **modo carrinho** ele soma os descontos automáticos do `cart.js` (por linha e do carrinho) e mostra uma linha "AUTOMATIC DISCOUNTS" no total. Também bloqueia código de cupom quando há desconto automático ("No se puede combinar con descuentos automáticos").
- **No botão da página de produto (modo product-only) o desconto "kit + unitário" não dispara**, porque o Releasit esvazia o carrinho e manda só aquele produto. O desconto só vale pelo carrinho (gaveta → "Pide y Paga al Recibir").
- **Não testei com pedido real** (por regra, nenhum pedido foi enviado). Antes de anunciar, faça **1 pedido de teste** pelo carrinho com o desconto criado (kit + unitário) e confira no admin e na Dropi: 2 linhas, desconto aplicado, 1 pedido só. Depois, cancele.

## 6. Teste ponta a ponta (pré-visualização, celular 390 px e computador 1440 px)
- Adicionar 2 kits pela página: OK (carrinho com 2 × $59.900 = $119.800).
- "Completa tu pedido" mostrou 2 kits do mesmo fornecedor (Yara + Yara Tous + Yara Elixir / + Yara Moi). "+ Agregar": OK (3 itens, $179.700).
- "Pide y Paga al Recibir" na gaveta abriu o formulário Releasit com as **2 linhas** ($59.900 + $119.800). Não foi enviado.
- `/cart` → "Pagar pedido" abriu o formulário contra entrega: OK.
- Trava de fornecedor: com `mopah2o` (sem etiqueta) no carrinho, o kit não foi adicionado e o aviso apareceu: OK.
- Erros de JS: os 4 erros que aparecem existem também no tema ao vivo (`shrine.null.js` procurando o ícone do carrinho, que não existe, e um `});` sobrando no `theme.liquid`). Não foram causados por esta mudança.

Prints (pasta `CARRINHO-LOJA/`): `depois_1_produto-botoes`, `depois_2_carrinho-2kits`, `depois_3_carrinho-com-upsell`, `depois_4_formulario-cod`, `depois_5_botao-carrinho-flutuante` (todos `_mobile` e `_desktop`), `depois_6_aviso-outro-fornecedor_desktop`, `depois_7_SIMULACAO-addon-19900_*` e `depois_8_pagina-cart-pagar-abre-cod_mobile`. Os scripts de teste ficam em `_trabalho/`.

## 7. Pontos abertos (precisa de revisão manual)
1. **Ligar o "carrinho" no Releasit** (app Releasit → configuração da página de carrinho). Hoje a gaveta chama o formulário em modo carrinho pela função interna do app (`_rsi.form.open`, modo `normalCart`). Funciona, mas não é uma API documentada: se o Releasit atualizar, pode quebrar. Com a opção ligada no app, o uso fica oficial. A gaveta funciona dos dois jeitos.
2. **Releasit na página de produto esvazia o carrinho** (`addMode: product-only`). Quem tem itens no carrinho e clica no verde da página de produto perde o carrinho. A gaveta mostra "Tienes N en tu carrito · Ver carrito" para reduzir isso. A alternativa é mudar no app para "produto + carrinho", mas aí o botão da página passa a pedir o carrinho inteiro (decisão do dono).
3. **Checkout do Shopify sem meio de pagamento.** O botão "Pagar con tarjeta" está pronto, mas escondido. Só ligue (`cv_mostrar_checkout = true`) depois de ativar um meio de pagamento. Note que o checkout soma IVA por cima do preço.
4. **No formulário do Releasit, os títulos dos kits são cortados** ("Kit 3 Perfumes Árabes Mujer |…"), então o cliente não distingue um kit do outro ali. Vale encurtar os títulos ou ajustar no app.
5. Confirmar o fornecedor dos 2 packs antigos (`lattafa`, `yara`) e etiquetar.
6. Valor X do perfume extra + confirmação de que o 82275 vende o unitário → criar o desconto (seção 4) → preencher `bf_addon_precio`.
7. Fazer 1 pedido de teste real pelo carrinho e cancelar (item 5).
8. Publicar o tema rascunho (junto com o Black Friday e a coleção) quando o dono aprovar.

## Como desfazer
- Desligar tudo: em `snippets/cv-carrito.liquid`, troque `assign cv_activo = true` por `false`. A gaveta antiga do tema volta.
- Remover de vez: restaure `backup/sections__scroll-to-top-btn.liquid` e apague os 2 arquivos novos.
- Etiquetas: `tagsRemove` de `forn-82275` nos 13 produtos. Elas não afetam nada fora deste carrinho.

---

# v2: carrinho visível (09/10/2026)

Pedido da dona, olhando `/collections/perfumes-arabes` no celular: "cadê o carrinho?".

- **Tema novo:** "BLACK FRIDAY v2 - carrinho (rascunho)", ID `167234765056`, NÃO publicado.
  - É uma cópia (`themeDuplicate`) do tema que está no ar, "BLACK FRIDAY - shr-co v4 (rascunho)" (`167232798976`, hoje MAIN).
  - O tema ao vivo não foi alterado.
- **Pré-visualização:** https://chileverificada.com/collections/perfumes-arabes?preview_theme_id=167234765056
- **Arquivo alterado:** só `snippets/cv-carrito.liquid`.
  - Antes: md5 `291566dd…`, guardado em `backup-v2/snippets__cv-carrito.liquid`.
  - Depois: md5 `8c407d85…`, fonte em `novos-v2/snippets__cv-carrito.liquid`.
  - O checksum no tema bate com o arquivo local.
- **Gravação:** feita por `stagedUploadsCreate` + `themeFilesUpsert` com body do tipo URL.

## O que mudou
1. **Ícone do carrinho sempre visível**, em todas as páginas.
   - Fica no canto direito da barra preta do topo, com ícone dourado e contador (bolinha dourada). No desktop aparece também a palavra "Carrito".
   - Ao rolar a página, vira um botão redondo preto fixo no canto superior direito.
   - Na coleção, a barra de chips abre espaço para ele no celular.
   - Clicar abre a gaveta cv. Quando entra item, o contador dá um pulinho.
   - O botão flutuante "Carrito (n)" de baixo (v1) foi **desligado** (`cv_fab = false`) para não ter dois botões de carrinho.
2. **Cards da coleção (e de qualquer grade de produtos):** botão "Agregar al carrito" só em produtos com etiqueta `forn-`.
   - Celular (390 px, 2 colunas): fica embaixo do "Pide y Paga al Recibir", em largura total, 36 px, com contorno preto.
   - Desktop (4 colunas): botão quadrado de 44 px com ícone de sacola com "+", ao lado do Releasit (o Releasit ocupa o resto da linha).
   - Adiciona a 1ª variante disponível por `/cart/add.js`, abre a gaveta e mostra a faixa "✓ Agregado al carrito".
   - Respeita a trava de fornecedor: com produto de outro fornecedor no carrinho, não adiciona e mostra um aviso laranja.
   - Produtos sem `forn-` ficam exatamente como antes.
   - Os dados vêm de um JSON da coleção renderizado no snippet. Fora da coleção, busca `/products/<handle>.js`.
3. **Página de produto: o "Agregar al carrito" saiu** (pedido da dona, `cv_atc_producto = false`).
   - Saíram também a quantidade e a frase "Lleva más de uno…".
   - A página volta a ter só o "Pide y Paga al Recibir" do Releasit.
   - Gaveta, "Completa tu pedido", trava de fornecedor e `/cart` continuam iguais.
4. **Correção pequena:** o "Completa tu pedido" dava erro de JS quando o carrinho mudava antes da busca terminar. Agora confere se o bloco ainda existe.
5. **Popup «¡Fuiste seleccionado! 🎁» (rasca y gana): pronto, mas DESLIGADO** (`cv_promo_kit = false`). Ver a seção abaixo.

Ajustes, todos no topo do snippet:

| Ajuste | Valor |
|---|---|
| `cv_icono_header` | `true` |
| `cv_atc_tarjetas` | `true` |
| `cv_fab` | `false` |
| `cv_atc_producto` | `false` |
| `cv_promo_kit` | `false` |
| `cv_promo_forn` | `'forn-82275'` |

## Fornecedor dos 2 packs antigos (Dropi, conector Chegou Operações)
Juntei as vendas da Shopify (`vendas_shopify_itemvendashopify` → `vendashopify`) com os pedidos da Dropi (`metricas_dropi_dropipedido`, via `dados->>'shop_order_id'`, sem pedidos sumidos). Depois li `orderdetails[].product.user_id`.

| Página | Vendas Shopify (25/09–09/10) | Pedidos na Dropi | Fornecedor (`user_id`) |
|---|---|---|---|
| `/products/lattafa` (Pack Hombre) | 161 | 130 | **82275** em 130/130: "PACK DE 3 PERFUMES ÁRABES hombre" (94) + "Pack3 perfume AQUA BOURRON NOIR" (36) |
| `/products/yara` (Pack Mujer) | 17 | 15 | **82275** em 15/15: "Pack3 perfume PINK WHITE CANDY" |

As vendas a mais não têm par na Dropi: são canceladas ou ainda não foram enviadas.

→ Etiqueta `forn-82275` adicionada aos 2 produtos (`tagsAdd`). Eles entraram no grupo do carrinho Lattafa.

**Atenção, perfumes unitários:** nenhum dos 8 unitários (Asad, Asad Bourbon, Asad Zanzibar, Yara, Yara Moi, Yara Tous, Yara Candy, Yara Elixir) tem venda ainda.
- Na Dropi também não há nenhum pedido de perfume unitário Asad/Yara.
- Por isso, **não há prova nos pedidos de que o 82275 vende os unitários**. A etiqueta `forn-82275` deles vem da suposição anterior.
- Também não há prova do contrário.
- Confirmar com o fornecedor antes de ligar a promo.

## Promo «¡Fuiste seleccionado!» (+1 perfume a mitad de precio)
**Referência (linfarele.com, loja da dona):**
- O "scrap" é um **rasca y gana próprio** ("Gratta e vinci"), feito em Liquid personalizado no grupo do rodapé (`#lfs`). **Não é app.**
- Os apps da Linfarele são Rapid Cart (gaveta/upsell) e Klaviyo, mas o popup é código do tema.
- Como funciona: tela cheia com degradê, título grande, cartão dourado em canvas ("GRATTA QUI") que se revela ao raspar cerca de 45%, prêmio por baixo, passo 2 depois de revelar, "No, grazie" e "×".
- Lá, ele abre 5 s depois de carregar a página, 1 vez a cada 7 dias.
- Prints: `v2/ref-linfarele/` (`02_produto_mobile.png` e `lfs_section.html`).
- Como é código simples e a gente já tem a gaveta própria, **replicar no tema é melhor que instalar app**: sem custo, sem outro script e com o mesmo visual.

**Nossa versão** (em `cv-carrito`, mesma mecânica, cores preto/dourado, título em Cormorant Garamond):
- **Quando abre:** ao clicar "Agregar al carrito" num card de **KIT** (`kit` + `forn-82275`).
  - Só abre se o carrinho ainda não tem unitário e o carrinho inteiro é do 82275.
  - Abre 1 vez por sessão por carrinho (`sessionStorage` com `try/catch`). No lugar dele, a gaveta não abre.
- **Passo 1:** "BLACK FRIDAY · ¡Fuiste seleccionado! 🎁 · Raspa aquí abajo y descubre tu premio", com o cartão dourado "RASPA AQUÍ". Enter também revela, para acessibilidade.
- **Passo 2 (prêmio):** "Lleva +1 perfume a mitad de precio" ~~$34,900~~ **$17,450**.
  - Dois botões lado a lado, **Para mí** (mesmo gênero do kit) e **Para regalar** (gênero oposto).
  - Lista com foto e nome dos unitários `forn-82275` daquele gênero.
  - Botão dourado "Agregar por $17,450" e a frase "1 perfume a mitad de precio por pedido · pagas todo al recibir".
- **"No, gracias" / × / Esc:** fecha e abre a gaveta.
- **"Agregar":** põe 1 unitário, fecha o popup e abre a gaveta com "¡Listo! Perfume a mitad de precio agregado".
- O bloco antigo "Agrega un perfume por $X" (`bf_addon_precio`) **continua vazio/desligado**, para não ter duas ofertas. O popup substitui esse bloco.
- O preço aparece no formato da loja (`$17,450`, com vírgula, igual aos outros preços do site).

**Backend:**
- Coleções criadas (automáticas, não publicadas na loja virtual):

  | Coleção | ID | Regra | Produtos |
  |---|---|---|---|
  | "Promo kits 82275" | `gid://shopify/Collection/492350210304` | `kit` E `forn-82275` | 7 |
  | "Promo unitarios 82275" | `gid://shopify/Collection/492350243072` | `unitario` E `forn-82275` | 8 |

- **O desconto automático NÃO foi criado.** A ação `discountAutomaticBxgyCreate` foi **bloqueada pela permissão do Claude Code** (classificador de modo automático), e não tentei por outro caminho.
- A mutation abaixo foi validada no schema. A dona (ou o agente principal, com permissão) roda:

```graphql
mutation criarDesconto($kits: ID!, $unitarios: ID!, $inicio: DateTime!) {
  discountAutomaticBxgyCreate(automaticBxgyDiscount: {
    title: "Black Friday +1 perfume 50%", startsAt: $inicio, endsAt: null, usesPerOrderLimit: "1",
    combinesWith: { productDiscounts: false, orderDiscounts: false, shippingDiscounts: true },
    customerBuys: { value: { quantity: "1" }, items: { collections: { add: [$kits] } } },
    customerGets: { value: { discountOnQuantity: { quantity: "1", effect: { percentage: 0.5 } } },
                    items: { collections: { add: [$unitarios] } } }
  }) { automaticDiscountNode { id } userErrors { field code message } }
}
# variables: {"kits":"gid://shopify/Collection/492350210304","unitarios":"gid://shopify/Collection/492350243072","inicio":"<agora em ISO>"}
```

Outra saída: Admin → Descontos → Criar desconto → Compre X e ganhe Y → Automático.
- Compre 1 item de "Promo kits 82275".
- Ganhe 1 item de "Promo unitarios 82275" com 50%.
- Máximo de 1 uso por pedido, sem data de fim.

**Depois de criar o desconto:**
1. Trocar `assign cv_promo_kit = false` por `true` no snippet do tema v2.
2. Abrir a pré-visualização, adicionar um kit pelo card e escolher um perfume.
3. Conferir na gaveta: preço riscado e linha "Descuento −$17,450".
4. Clicar em "Pide y Paga al Recibir" e conferir que o formulário do Releasit mostra o desconto (linha de descontos automáticos, ver seção 5 da v1). Não enviar.

**Sem o desconto, o carrinho cobra $34,900 pelo perfume.** Por isso o popup ficou desligado.

## Testes (pré-visualização, 390×844 e 1440×900; nenhum pedido enviado)
Scripts: `_trabalho/v2/e2e_v2.py` e `_trabalho/v2/promo_test.py`. Log: `v2/teste_log.txt`.

| Teste | Resultado |
|---|---|
| Coleção | 15 cards, 15 botões "Agregar" (todos são `forn-82275` agora), 15 Releasit. Sem rolagem horizontal (390 px). O texto do Releasit não corta. |
| Ícone no topo | Na barra preta; vira botão redondo ao rolar; abre a gaveta; contador correto. |
| Agregar pelo card | Pack Hombre: carrinho com 1 item, gaveta aberta com "Agregado al carrito". Pack Mujer em seguida: 2 itens. |
| "Completa tu pedido" na gaveta | Sugeriu unitários Asad; "+ Agregar" funcionou. |
| Trava de fornecedor | Com `mopah2o` (sem etiqueta) no carrinho, o card não adicionou e o aviso laranja apareceu. |
| Releasit do card | Abre o formulário. |
| Página de produto | Só "Pide y Paga al Recibir" (sem ATC); o ícone do topo aparece. |
| Popup (SIMULAÇÃO: `cv_promo_kit` trocado para true só no navegador do teste) | Raspar revela. "Para mí" (kit mujer) = 5 Yara; "Para regalar" = 3 Asad; kit hombre → "Para mí" = 3 Asad. "Agregar" põe 1 unitário e abre a gaveta. "No, gracias" abre a gaveta. Não reabre na mesma sessão/carrinho nem com unitário no carrinho. |
| Erros de JS | Os únicos que sobram já existem no tema ao vivo: `'}'` do `theme.liquid`, `closest` do `shrine`, `_0x54d0d7` e o `innerHTML` do formulário Releasit. Medi no tema ao vivo: 5 `innerHTML` ao abrir o Releasit. |

**Prints em `v2/`:**
- `1_colecao-topo_*`
- `2_colecao-cards_*`
- `3_add-card-gaveta-toast_*`
- `4_gaveta-completa_*`
- `4b_gaveta-upsell-adicionado_*`
- `5_icone-com-contador_*`
- `6_releasit-card-abre_*`
- `7_trava-fornecedor_*`
- `8_produto-topo_*`
- `9_produto-botoes_*`
- `10_promo-raspadita_*`
- `11_promo-raspando_*`
- `12_promo-premio-para-mi_*`
- `13_promo-para-regalar_*`
- `14_SIMULACAO-gaveta-apos-promo-sem-desconto_*`
- `15_SIMULACAO-form-cod-carrinho_*`
- `0_antes_colecao_live_mobile.png`

## Pontos abertos (v2)
1. **Criar o desconto automático** (mutation acima) e depois ligar `cv_promo_kit`. Antes de anunciar, fazer 1 pedido de teste (kit + perfume) pelo carrinho e conferir no admin e na Dropi; depois, cancelar.
2. **Confirmar que o fornecedor 82275 vende os 8 unitários.** Não existe pedido de unitário na Dropi para provar isso.
3. **O Releasit no card já manda o carrinho junto.** No tema ao vivo, com 1 item no carrinho, clicar o Releasit de outro card abre o formulário com o item do card **e** os itens do carrinho.
   - Isso é do app, igual antes da v2.
   - Nesse caminho a trava de fornecedor do cv **não atua**: dá para misturar fornecedores pelo botão verde do card.
   - Avaliar no app Releasit, nas configurações do botão em coleção: "solo producto".
4. **Publicar o tema v2** quando a dona aprovar. Ele já inclui tudo do tema ao vivo de hoje (cópia de 09/10 ~21:40 UTC). Alterações feitas no tema ao vivo depois da cópia não estão no v2.

## Promo LIGADA (09/10/2026, depois da aprovação da dona)

**O que foi feito:**
- O agente principal criou o desconto automático "Black Friday +1 perfume 50%" (`gid://shopify/DiscountAutomaticNode/1709331316992`).
- Em `snippets/cv-carrito.liquid` do tema v2: `cv_promo_kit = true`.
  - Backup da versão anterior (promo desligada): `backup-v2/snippets__cv-carrito_v2-promo-off.liquid`, md5 `8c407d85…`.
  - Versão nova: md5 `836b4b63…`. O checksum no tema confere.

**Teste real** na pré-visualização, com o desconto de verdade, em 390 px e em 1440 px. Nenhum pedido foi enviado.

| Etapa | Resultado |
|---|---|
| Card do Pack Mujer | O popup de raspadinha abre. |
| Escolha | "Yara Tous", por "Agregar por $17,450". |
| `cart.js` | Yara Tous $34,900 → **$17,450**, com o desconto "Black Friday +1 perfume 50%". Pack $49,900. `total_discount` = 17.450. Total **$67,350**. |
| Gaveta | Subtotal $84,800 · **Descuento −$17,450** · Total $67,350 · "Total $67,350 · pagas al recibir". |
| Formulário Releasit (modo carrinho, aberto pela gaveta) | Resumo "Total Parcial · **Descuentos − $17.450** · Total $67.350". O botão mostra "¡HACER PEDIDO AHORA! **$67.350**". |

**Ponto de atenção no formulário:** as linhas de produto do formulário mostram o preço cheio de cada item ($34.900 e $49.900). O desconto só aparece no resumo e no total do botão.

**Prints:**
- `v2/20_REAL-promo-raspadita_*`
- `v2/21_REAL-promo-premio_*`
- `v2/22_REAL-gaveta-com-desconto_*`
- `v2/23_REAL-form-releasit-com-desconto_*`
- `v2/24_REAL-form-releasit-totais_desktop.png`

**Antes de anunciar, ainda falta:** 1 pedido de teste real (kit + perfume), conferir no admin e na Dropi (2 linhas, desconto, 1 pedido) e depois cancelar.

**Observação dos testes:** muitos testes seguidos fizeram a Shopify bloquear temporariamente o IP. A página voltou HTTP 429 "Your connection needs to be verified", e liberou depois de cerca de 10 minutos. Isso não é defeito do tema.

## Como desfazer (v2)
- Desligar só a promo: `cv_promo_kit = false`. E desativar o desconto no Admin → Descontos.
- Voltar ao snippet da v1: gravar `backup-v2/snippets__cv-carrito.liquid` como `snippets/cv-carrito.liquid` no tema v2.
- Ou desligar por partes, no topo do snippet:

  | Para desligar | Ajuste |
  |---|---|
  | Ícone do topo | `cv_icono_header = false` |
  | Botão nos cards | `cv_atc_tarjetas = false` |
  | Botão flutuante de baixo (volta) | `cv_fab = true` |
  | ATC na página de produto (volta) | `cv_atc_producto = true` |

- Etiquetas: `tagsRemove` de `forn-82275` em `lattafa` e `yara`.
- Coleções promo: apagar as 2 coleções "Promo … 82275", que não afetam a loja sem o desconto.

---

# v3: preço do upsell no Releasit + texto da raspadinha (09/10/2026)

- **Tema novo:** "BLACK FRIDAY v3 (rascunho)", ID `167236436224`, NÃO publicado.
  - É uma cópia (`themeDuplicate`) do tema que está no ar, "BLACK FRIDAY v2 - carrinho (rascunho)" (`167234765056`, publicado pela dona).
  - O tema ao vivo não foi alterado.
- **Pré-visualização:** https://chileverificada.com/collections/perfumes-arabes?preview_theme_id=167236436224
- **Arquivo alterado:** só `snippets/cv-carrito.liquid`.
  - Antes: md5 `836b4b63…`, guardado em `backup-v3/snippets__cv-carrito.liquid`.
  - Depois: md5 `7e75edfd…`, fonte em `novos-v3/snippets__cv-carrito.liquid`. O checksum no tema confere.

## 1. Preço cheio na linha do formulário Releasit
**Causa:** o script do Releasit (`releasit-cod-form-455/get-form-script.min.js`) monta cada linha do formulário com `original_line_price` fixo no código:
`'<div class="_rsi-modal-line-item-final-price">' + formatMoney(e.original_line_price) + '</div>'`.
- Não existe ajuste no app para trocar por `final_line_price`. Procurei nas configurações carregadas na página (`_rsi.s`): só há `discounts` (campo de cupom, desligado), `checkoutLines` (resumo) e `hideCheckoutLines`.
- Por isso o desconto aparece só no resumo ("Descuentos − $17.450") e no total do botão.
- **Não há nada para a dona ligar no Releasit.**

**Correção (no tema, só dentro do formulário do Releasit):**
- Um observador (`MutationObserver`) percebe quando o formulário desenha ou redesenha as linhas.
- Ele lê `/cart.js` e, em cada linha com desconto, troca o preço por ~~$34.900~~ **$17.450**: o original riscado em cinza e o preço com desconto em vermelho.
- **Trava de segurança:** só mexe quando as linhas do formulário batem 1 a 1 com o carrinho (mesma ordem, variante e quantidade). Se não baterem (por exemplo, no botão da página de produto em modo "só produto"), não muda nada.
- É só visual. O pedido continua sendo calculado pelo Releasit e pelo desconto automático da Shopify.
- Se o desconto sair (ex.: o cliente remove o kit dentro do formulário), a linha volta sozinha para $34.900 sem riscado. Testado.
- Ajuste no topo do snippet: `cv_rsi_precio_linea = true` (false = volta ao comportamento do Releasit).
- O resumo do Releasit continua igual: "Total Parcial $84.800 · Descuentos −$17.450 · Total $67.350".

**Alternativa (NÃO aplicada; decisão da dona):** variante escondida "Promo +1" a $17.450 em cada unitário, adicionada pelo popup, com o desconto BXGY desligado.

| Prós | Contras |
|---|---|
| O preço certo aparece em todo lugar (Releasit, admin, Dropi) sem depender de script. | A variante pode ser comprada sozinha, sem kit (por link, `/cart/add` ou Releasit da página): risco de abuso, que o desconto automático hoje impede. |
| Não depende do desconto automático. | Precisa de trava extra no tema/app para exigir o kit, e ela é contornável. |
| Na Dropi a linha chega com $17.450. | Duplica variantes: estoque, SKU e mapeamento na Dropi por variante. |
| | Os relatórios ficam divididos em 2 variantes por perfume, e a "venda a 50%" deixa de aparecer como desconto. |
| | O limite "1 por pedido" deixa de ser automático. |

Recomendação: manter a correção visual (v3) e o desconto automático.

## 2. Texto da raspadinha
- Depois de raspar, aparece logo abaixo do prêmio: "Oferta válida solo para **1 perfume adicional** por pedido: el 50% lo asumimos nosotros 🖤" (caixa dourada discreta, 2 linhas em 390 px).
- Logo acima do botão "Agregar por $17,450" aparece o selo **"SOLO 1 POR PEDIDO"**.
- O resto do popup não mudou.

## 3. Pedidos da dona durante a v3
- **Só perfumes:** tudo do carrinho cv (botão "Agregar" nos cards, "Completa tu pedido", raspadinha e trava de fornecedor) agora exige a etiqueta `perfumes-arabes` **além** da `forn-`.
  - Um produto com `forn-` e sem `perfumes-arabes` é tratado como "sem fornecedor": não ganha botão, sugestão nem promo.
  - Ajuste no topo do snippet: `cv_cat = 'perfumes-arabes'`.
  - O cache de etiquetas do navegador mudou de nome (`cvTags3`) para não usar etiquetas antigas.
  - Nenhuma etiqueta de produto foi alterada.
- **Raspadinha sem memória:** abre nova (sem raspar) **toda vez** que um kit é adicionado por um card e o carrinho ainda não tem perfume unitário. Isso vale mesmo que o cliente já tenha raspado ou clicado em "No, gracias".
  - As marcas antigas da v2 (`cvPromo:*` no `sessionStorage`/`localStorage`) são apagadas ao carregar a página.
  - O limite de 1 por pedido continua sendo do desconto (`usesPerOrderLimit: 1`).
  - Com um unitário no carrinho, ela não abre.

## Testes (pré-visualização v3, 390×844 e 1440×900; nenhum pedido enviado)
Scripts: `_trabalho/v3/e2e_v3.py`, `extra.py`, `reset_gate.py`, `errcmp.py`. Log: `v3/teste_log.txt`.

| Teste | Resultado |
|---|---|
| Card Pack Mujer → raspar → Yara Tous → "Agregar por $17,450" | `cart.js`: Yara Tous $34.900 → $17.450, Pack $49.900, total **$67.350** |
| Gaveta | Subtotal $84,800 · Descuento −$17,450 · Total $67,350 |
| Formulário Releasit (gaveta → "Pide y Paga al Recibir") | Linha do perfume: ~~$34.900~~ **$17.450**; Pack $49.900; botão "¡HACER PEDIDO AHORA! $67.350". Igual no celular e no desktop. |
| Remover o kit dentro do formulário | O perfume volta a $34.900 sem riscado (o carrinho também volta a $34.900). |
| Raspadinha 3 vezes seguidas (raspar → "No, gracias" → esvaziar → kit de novo) | Abre sem raspar nas 3 vezes. |
| Marcas da v2 na sessão | Apagadas ao carregar. |
| Kit com unitário já no carrinho | O popup não abre. |
| Coleção de perfumes | 15 cards, 15 botões "Agregar". |
| Erros de JS | Os mesmos do tema v2 (comparado lado a lado): `'}'` do `theme.liquid`, `closest` do `shrine`, `_0x54d0d7` e 6 `innerHTML` do Releasit. Nenhum erro novo. |

**Prints em `v3/`:**
- `1_promo-raspadita_*`
- `2_promo-premio-texto-novo_*`
- `3_gaveta-com-desconto_*`
- `4_form-releasit-linha-com-desconto_*`
- `5_form-releasit-totais_*`
- `6_promo-reabre-sem-raspar_mobile.png`

## Como desfazer (v3)
- Só o preço na linha: `cv_rsi_precio_linea = false`.
- Tudo: gravar `backup-v3/snippets__cv-carrito.liquid` como `snippets/cv-carrito.liquid` no tema v3, ou simplesmente não publicar a v3.

## Pontos abertos (v3)
1. **Publicar o tema v3** quando a dona aprovar. Ele é uma cópia do v2 ao vivo feita em 09/10 ~22:45 UTC. Alterações feitas no tema ao vivo depois disso não estão no v3.
2. A correção do preço depende do HTML do Releasit (classe `_rsi-modal-line-item-final-price`). Se o app mudar isso numa atualização, a linha volta a mostrar o preço cheio. Nada quebra: o total continua certo.
3. Continua pendente: 1 pedido de teste real (kit + perfume) conferido no admin e na Dropi, e depois cancelado.
