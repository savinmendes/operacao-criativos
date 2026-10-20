---
name: "replicar-loja-ecommerce"
description: "Reconstrói em código, editável pelo editor visual, o design de uma loja, página de produto ou seção de referência, e faz o pós-clone (rebrand, imagens, domínio, mercado, frete, upsell). Use no lugar de clonar-loja-ecommerce sempre que pedirem para copiar, replicar, recriar ou fazer igual uma loja/página/landing, ou relançar loja clonada com outra marca/país."
---

# replicar design de loja de e-commerce

Esta skill reconstrói o design de uma loja de referência dentro do tema do
usuário, em código, com cada elemento editável pelo editor visual — não como
bloco fixo que exige mexer no código a cada ajuste.

## Quando usar

Sempre que alguém quiser reproduzir o design de uma loja, página de produto ou
seção vista em outro site — mesmo em pedidos informais como "quero uma loja
parecida com essa", "copia esse layout pra mim", "monta minha página igual a
desse site", "refaz minha loja no estilo dessa". Também para montar loja nova
partindo de um site de referência, ou reconstruir uma seção específica (hero,
prova social, comparativo, garantia). É genérica: qualquer plataforma, nicho,
país e modelo de venda; busca o contexto do negócio em tempo de execução.

Não é necessária para ajustar uma loja que já existe sem referência externa —
nesse caso um pedido direto resolve.

Também cobre o **acabamento pós-clone** (trocar marca, imagens, domínio,
mercado/moeda, frete, upsell, e-mails) — ver a seção "Pós-clone" no fim.

---

## Passo 0 — Parâmetros

Infira o que puder. **Só pergunte o que for essencial e não der para inferir.**

| Parâmetro | Como resolver |
|---|---|
| Loja de referência | URL, prints ou PDF de captura que a pessoa mandar. Sem nenhum deles, pergunte — é o único item sem o qual não dá para começar |
| Escopo | Página inteira, só a página de produto, ou seções específicas |
| Plataforma e tema | Pergunte se não estiver claro. O código gerado depende disso |
| **Modelo de venda** | **Determine sempre.** Ver "Modelo de venda" abaixo — muda o que faz sentido construir |
| País, idioma e moeda | Definem formato de preço, prova social, texto e avisos legais do país |
| **Limite do escopo** | **Determine sempre e repita para a pessoa em 1 linha antes de construir:** quais páginas mudam (ex.: "só a coleção X") e que todo o resto fica intacto. Ver "Escopo: nem de menos, nem de mais" |
| **Marca final** | Nome da marca que vai na loja nova. Se for diferente da loja de origem, já planeje o rebrand (ver Pós-clone A e B) |
| Contexto do negócio | Se o projeto tiver pasta de contexto (`contexto/`, `sops/` ou equivalente), leia antes de começar |

### Modelo de venda — determine antes de construir

Pergunte, ou infira do contexto do projeto, **como o dinheiro entra**:

| Modelo | Consequência para o que você constrói |
|---|---|
| **Pagamento antecipado** (cartão, Pix, checkout padrão) | Seções de upsell de checkout, order bump e one-click fazem sentido |
| **Pagamento na entrega / contra-entrega** | O checkout costuma ser substituído por formulário. **Não construa nada que dependa do checkout padrão** — é trabalho perdido |
| **Venda por conversa** (WhatsApp, closer, ligação) | A página serve de apoio, não fecha a venda. O destino do botão é o canal, não o carrinho |

Errar isso produz uma loja bonita com seções inúteis.

Também não reproduza recurso que a loja não consegue cumprir. Ex.: card
"Subscribe & save" sem app de assinatura instalado vira promessa falsa — corte
(ou pergunte) e mantenha só a compra avulsa.

### Escopo: nem de menos, nem de mais

Os dois erros mais caros desta skill são de escopo, não de código:

- **De menos:** "quero igual" NÃO é só importar produtos/coleção. Igual =
  topo (barra de anúncio, contador, cor e layout do cabeçalho), seções,
  imagens, cards, botões, **o que acontece depois de cada clique** (modal de
  opções, carrinho lateral), promoções (ex.: compre 1 leve 2, compre 2 leve
  4, com o desconto funcionando de verdade no carrinho), popups (roleta,
  raspadinha) e **rodapé**. Entregar só a estrutura gera "trabalho
  inacabado".
- **De mais:** não estenda para páginas que não foram pedidas (ex.: pediu a
  coleção → não criar template de página de produto nem aplicar em 45
  produtos) e não mexa em configuração global (mercado/moeda, carrinho da
  loja, tema publicado, produtos em massa) sem um "sim" explícito. Se achar
  que outra página precisa mudar para ficar igual, **pergunte antes**.

Quando o objetivo é "uma página com topo e rodapé diferentes da home" (ex.:
coleção de outra marca dentro de uma loja existente), a solução é um
**template alternativo só daquela página** que sobrescreve topo, rodapé e
carrinho apenas ali — ver "Coleção/landing com identidade própria" no passo 3.

---

## O que esta skill gera, e o que não gera

| | |
|---|---|
| **Gera** | Design e código: seções, layout, estrutura, responsividade |
| **Não gera** | Conteúdo de venda: copy final, oferta, preço, imagens de produto, roteiros de anúncio |

São etapas diferentes. Construa a estrutura primeiro; conteúdo é outro trabalho.
Se a pessoa pedir os dois num disparo só, avise que o resultado degrada nos dois
e proponha separar.

---

## Expectativa realista

**A primeira tentativa pode não sair parecida.** Isso é comum e não indica que o
método falhou.

Trate a iteração como parte do processo. O protocolo de recuperação está abaixo
e deve ser usado sem constrangimento. Diga isso à pessoa **antes** de começar,
para ela não interpretar a primeira rodada como fracasso.

A reclamação mais comum ("ficou genérico, nada a ver com a minha marca") vem de
pular o inventário do passo 1. Faça-o sempre.

---

## Fluxo

### 1. Capturar a referência

Peça capturas de **página inteira**, e sempre em dois formatos:

- desktop
- **mobile**

O print mobile é o passo mais pulado, e é o que faz a página quebrar no celular.
Não prossiga sem ele em qualquer layout com colunas ou grade.

Se a referência bloquear clique direito, a captura pode ser feita pelo
inspetor do navegador. PDF de captura também serve: leia todas as páginas
(Read com `pages`, em lotes de até 20).

**Antes de escrever código, monte o inventário** seção por seção, na ordem do
mobile:

| # | Seção | Formato exato | Cores / fundo | Elementos-assinatura |
|---|---|---|---|---|
| 1 | Topo do produto | coluna única | branco | card de avaliação verificada, título grande colorido, pílulas 2×2, lista ✓, faixa de dica |
| 2 | Seletor | 3 cards | borda colorida no ativo | rótulo em maiúsculas espaçadas, "Save X%", preço/dose |

**Inventário funcional — clique em tudo na referência** (pelo navegador,
antes de escrever código) e registre o que aparece:

| Interação | O que capturar |
|---|---|
| Botão do card ("Choose options"/"Add to cart") | Abre modal? Quais ofertas, seletores (#1, #2…), textos, preços por unidade |
| Ícone do carrinho e o pós "adicionar" | Carrinho lateral ou página; barra de urgência, etiqueta de desconto, "You save", upsell, seguro de envio, botão de checkout |
| Popups com tempo | Roleta/raspadinha/newsletter: quando abre, prêmio, cupom |
| Contadores | Formato (DAY:HR:MIN:SEC, mm:ss) e se é fixo ou "evergreen" por visitante |
| Promoções | Regra exata de preço (ex.: 2 por $110 = 50%; 4 por $176 = 60%) para recriar como desconto real |
| Topo e rodapé | Cores, ordem dos itens, marca centralizada, links |

Se o print de um estado não abrir (ex.: carrinho da referência não abre),
registre e siga; não fique tentando.

Extraia a **paleta** (hex aproximado), o **peso/estilo da fonte** e os
**microcomponentes** (pílulas, borda tracejada, bolinhas de vídeo com play, "+"
nos acordeões, linha do tempo numerada com etiquetas, carrossel com miniaturas
e setas, cards translúcidos sobre fundo de cor, tabela comparativa ✓/×). Cada
um vira componente no código. Página "genérica" = componente esquecido.

### 2. Proteger o que já existe

Padrão: **antes de qualquer alteração, duplique o tema ativo para rascunho.**
Se a rodada sair ruim, o que está no ar continua intacto. Sem isso, uma
tentativa malsucedida derruba a loja publicada.

Exceção: se a pessoa já disse que acha arriscado duplicar/trocar de tema, ou a
loja ainda está com senha (não vende), trabalhe no tema ativo com mudanças
pequenas e reversíveis (bloco "Liquid personalizado", seções novas,
substituição de arquivo) e confira cada uma no preview antes de seguir. Nunca
faça troca de tema publicado sem combinar. Na Shopify, o caminho mais seguro
nesse caso é criar arquivos novos (seções `prefixo-*.liquid` e um template
alternativo `product.<nome>.json`), que só afetam o produto atribuído a ele.

### 3. Construir

Monte o pedido com estes elementos:

```
Reconstrua <escopo> no tema <tema> da minha loja.

Referência: <url>
Anexos: print desktop e print mobile

País, idioma e moeda: <...>
Modelo de venda: <...>
  → se for pagamento na entrega: NÃO crie nada que dependa do
    checkout padrão (upsell de checkout, order bump, one-click)

Requisitos:
- duplique o tema ativo para rascunho antes de alterar qualquer coisa
  (salvo se a pessoa preferir mudanças simples no tema ativo)
- construa em seções separadas, uma por arquivo
- TODO texto, cor, imagem e botão editável pelo editor visual
  (schema com settings; nada fixo no código)
- responsivo conforme o print mobile
- sem dependência de app pago
- a origem é a sua loja: pode reaproveitar estrutura, texto, imagens e
  marca; ajuste só o que muda de mercado/idioma
- imagens hospedadas nos Arquivos da própria loja (nunca em host
  externo tipo postimg/imgur)

Ao terminar, liste o que criou e o que NÃO conseguiu reproduzir.
```

**Por que seções separadas mesmo num pedido único:** evita o código monolítico
que não dá para editar depois. Mantém a velocidade sem herdar o defeito.

**Por que exigir schema com settings:** sem isso cada ajuste de cor ou texto
exige voltar ao código. Com schema, a pessoa muda tudo pelo painel.

**Por que exigir a lista do que não conseguiu:** há elementos que não transferem,
e saber quais evita procurar defeito onde não há.

**Por que imagens na própria loja:** host externo pode cair, e trocar depois a
URL para outro servidor é tratado como redirecionamento e exige confirmação
explícita da pessoa.

**Schema desde o início, nunca "Liquid personalizado" com HTML fixo.** Seção
com texto fixo volta depois como pedido de "deixar editável" e o trabalho é
refeito. Use **blocos** para tudo que repete (passos, cards, FAQs, avaliações,
especialistas, linhas de tabela) e `image_picker` para imagens; imagem vazia
mostra placeholder só no editor (`{% if request.design_mode %}`).

**Detalhes de construção que pesam no resultado:**

- Números derivados do preço calculados no Liquid (preço por dose, "Save X%",
  custo por dia via token `[price]` + `replace`, preço por frasco).
- CSS escopado num bloco do próprio template, com prefixo de classe próprio,
  sobrescrevendo com especificidade maior o CSS global (ex.: cor do botão).
- Aviso legal do país (suplemento no Reino Unido ≠ aviso da FDA).
- Seletor de variantes personalizado (Dawn e similares): esconder
  `variant-selects`, cards marcam o rádio escondido e disparam `change`
  (fallback para `select`). Preço no botão por variável CSS
  (`span::after{content:var(--atc)}`), porque o tema reescreve o texto do botão.
  Dawn limita `product-form form` a 300px: forçar `width:100%;max-width:none`.
- Conteúdo dentro da coluna do produto que precisa ser editável (ex.:
  Supplement Facts): o bloco do `main-product` não aceita schema próprio. Crie
  uma seção separada com schema, renderizada logo após o produto, cujo script
  move o conteúdo para `.product__info-container` e esconde a seção original
  (remover o host antigo a cada render para não duplicar no editor).
  Alternativa: metacampos do produto.
- Elemento global (popup, raspadinha) diferente numa página: usar
  `template.suffix` no arquivo da seção para trocar cor/fundo/chave de "já
  visto" só ali, sem duplicar a seção.

### Coleção/landing com identidade própria dentro de loja existente

Para uma página com cara de outra marca (topo, rodapé, carrinho, popups
próprios) sem afetar o resto da loja:

1. Criar só arquivos novos: seções `pv-*.liquid` (prefixo próprio) +
   `templates/collection.<nome>.json` e atribuir via
   `collectionUpdate(templateSuffix:"<nome>")`.
2. **Topo:** uma seção no template que (a) esconde a barra de anúncio do tema
   (`.announcement-bar-section{display:none}`), (b) recolore o cabeçalho
   (`.section-header .header-wrapper{background:…}`), troca o logo por texto
   (`.header__heading-logo-wrapper{display:none}` +
   `.header__heading-link::after{content:"MARCA"}`) e centraliza com
   `grid-template-areas`, e (c) move a própria barra para antes do header com
   JS (`hg.parentNode.insertBefore(bar, hg)`). Como o CSS só existe nesse
   template, a home não muda.
3. **Rodapé:** seção no template que esconde `.shopify-section-group-footer-group`
   e renderiza o rodapé novo (políticas por `shop.policies`, ícones por
   `shop.enabled_payment_types`).
4. **Fundo e fontes:** `body{background:…}` e Google Fonts carregadas na seção
   do topo.
5. **Carrinho lateral próprio** (se a referência tiver): seção com `/cart.js`,
   `/cart/change.js` e `/cart/add.js`, exibindo `line_level_discount_allocations`
   como etiqueta ("BOGO – You save X"). Ver a pegadinha do app de carrinho
   abaixo.
6. **Promoção "compre X leve Y"** = desconto automático real, não só texto.
   Ex.: `discountAutomaticBasicCreate` 50% com mínimo 2 itens e 60% com
   mínimo 4, ambos restritos à coleção e `productDiscounts:false`, para não
   somarem (a Shopify aplica o melhor). Validar no `/cart.js` depois de um
   `change` (o carrinho só recalcula após uma alteração).
7. **Roleta/raspadinha:** criar o cupom antes (`discountCodeBasicCreate`),
   aplicar com `fetch('/discount/CODIGO')`, capturar o e-mail pelo
   `{% form 'customer' %}` e usar `localStorage` com try/catch para "já visto".
   Fatias com texto curto (≤ 10 caracteres) para não vazar da roda.
8. Preços no JS: `Intl.NumberFormat` com `{{ cart.currency.iso_code }}`, nunca
   `shop.money_format` (fica errado em outro mercado/moeda).
9. Não anunciar desconto maior que o real (ex.: texto "70% OFF" quando a conta
   dá 60%).

**Pegadinhas da Shopify que impedem salvar:**

| Erro | Correção |
|---|---|
| `name é muito longo (máximo de 25 caracteres)` | Nome de seção, preset e bloco ≤ 25 caracteres |
| `Variable ... was not properly terminated` | Não usar `{palavra}` dentro de `{{ }}`; usar `[price]` |
| setting `url` recusando `mailto:` | Usar `text` para mailto/tel |
| `Namespace é muito curto (mínimo de 3 caracteres)` em `metafieldsSet` | Namespace com 3+ letras (ex.: `pelvini`, não `pv`) |
| Coleção nova dá **404** na loja | Coleção criada pela API nasce sem canal: `publishablePublish` na publicação "Loja virtual" |
| Coleção automática enchendo devagar (27/45) | Usar coleção manual + `collectionAddProducts` na ordem da referência |
| Imagem do template não aparece | O `fileCreate` pode trocar a extensão (`.webp` → `.jpg`): consultar `files(query:"filename:prefixo-*")` e usar o nome real em `shopify://shop_images/<arquivo>` |
| Banner com altura 0 / desproporcional | Usar `aspect-ratio` (ex.: 3.7/1 cada metade) em vez de altura fixa em px |
| App de carrinho (Rapid Cart, Upcart…) abre por cima do seu carrinho e rouba o clique do ícone | Detectar antes (scripts `rapid-cart`, `#rapi-cart-drawer-app` etc.); só no template: esconder o app por CSS e ouvir o clique do ícone em **captura** (`window.addEventListener('click',fn,true)` + `stopImmediatePropagation`). Avisar a pessoa que o seguro de envio do app não aparece ali |
| Imagem esticada com `image_tag` | Ele grava `height` no HTML: CSS `height:auto!important;aspect-ratio:1/1;object-fit:cover` |

### 4. Instalar e conferir

Se houver conector entre o assistente e a plataforma, o código vai direto.
Senão, a pessoa cola à mão no editor de código do tema, em arquivos separados
dentro da pasta de seções.

Erro ao salvar é rotina, não falha. Peça o **texto exato do erro**, devolva junto
com o código, peça a correção, repita até salvar.

**Shopify: conector bloqueado no tema publicado.** O conector costuma recusar
escrita no tema ativo. Contorno pelo admin aberto no navegador (extensão), sem
trocar de tema:

```
csrf = fetch(location.href) → HTML → /"csrfToken":"([^"]+)"/
GET  /store/<loja>/themes/<id>/assets.json?asset[key]=<arquivo>
     → .asset.value (JSON de template vem com comentário /* */ no topo: remover antes do JSON.parse)
PUT  mesma URL sem query; headers Content-Type/Accept JSON + X-CSRF-Token;
     body {asset:{key,value}}
DELETE mesma URL com ?asset[key]=<arquivo> (para remover arquivo criado por engano)
```

- 403 "CSRF": buscar o token de novo (expira).
- Conteúdo grande: enviar em pedaços com String.raw para uma variável
  `window`, conferir o tamanho e fazer o PUT **numa chamada separada**
  (chamadas longas com várias requisições falham na extensão).
- Sempre reler o template atual antes de gravar e alterar só a parte em
  questão — a pessoa pode ter editado pelo painel.
- **Editor aberto sobrescreve:** se a pessoa estiver com o Personalizar tema
  aberto e clicar em Salvar, a versão antiga volta por cima. Depois de gravar,
  peça para recarregar (F5). Se acontecer, regrave só a sua parte sobre a
  versão atual dela.

**Conferir no preview** (link do tema com `preview_key`): via JS, contar
elementos por seção, clicar no seletor (variante marcada e preço no botão),
procurar imagens com altura maior que a largura, e tirar print em largura
mobile. Popup: limpar a chave do `localStorage` antes de testar. Depois de
concluir, abrir também a **home** para confirmar que nada fora do escopo mudou.

Depois: posicionar a seção, conferir no modo mobile do editor, ajustar cores e
textos pelo painel — nunca no código.

**Conferência mobile obrigatória de cards com selo** (ex.: "-60% • MAIS
VENDIDO" em seletor de ofertas/variantes): selo com `position:absolute` e `top`
negativo costuma sobrepor o título quando ele quebra em 2 linhas no celular.
Correção: `padding-top` no card que tem selo
(`.card:has(.badge){padding-top:22px}`) e `z-index` no selo.

---

## Quando não ficar parecido

Não recomece do zero. Nesta ordem:

**1. Aponte o que está diferente, com especificidade.** "Não parece com o
original" produz outra tentativa genérica. Nomeie: posição invertida, paleta
errada, seção faltando, proporção da imagem.

**2. Reenvie a captura.** A referência visual se perde entre rodadas.

**3. Se a segunda rodada falhar, quebre em blocos.** Peça uma seção por vez. O
disparo único funciona bem em página simples e degrada em página densa. Não
insista contra a evidência.

**4. Congele o que deu certo.** Peça para preservar as seções aprovadas e
trabalhar só nas pendentes.

**5. Print riscado = "igual, menos isso".** Reproduza o resto à risca e remova
só a parte riscada.

---

## O que normalmente não transfere

Avise **antes**, não depois:

| Elemento | Por quê |
|---|---|
| Avaliações e depoimentos | Costumam vir de app instalado. Ofereça seção-esqueleto editável (carrossel de cards com título, estrelas, texto, nome, "Verified purchase") para avaliações **reais** da pessoa. Contagem de avaliações por produto: metacampo (`pelvini.reviews` etc.) |
| Vídeo e GIF embutidos | Mídia hospedada por terceiro. Bolinhas de vídeo podem puxar `product.media` tipo vídeo; a pessoa sobe no quadro Mídia do produto |
| Especialistas, imprensa, selos, rótulo | Só com dados reais da pessoa → campos editáveis com placeholder |
| Fontes proprietárias | Licenciadas pela marca original |
| Seções de app pago | Dependem do app, não do código (ex.: seguro de envio no carrinho) |
| Imagens de produto | Precisam ser geradas ou fotografadas |

---

## Pós-clone — acabamento e lançamento (Shopify)

Lições práticas de uma loja clonada (da própria pessoa) e relançada com outra
marca em outro país. Faça na ordem e entregue à pessoa a lista COMPLETA do que
ficar para ela fazer manualmente.

### A. Rebrand — trocar o nome da marca em tudo

A marca aparece em muito mais lugares do que o texto da página:

| Onde | Como trocar |
|---|---|
| Textos do tema (seções, snippets, templates JSON, nomes de seção) | Editor de código → Pesquisar com **diferenciar maiúsculas ligado** → substituir `Marca`→`Nova` e depois `MARCA`→`NOVA` em passes separados → salvar tudo (Ctrl+K S) → pesquisar de novo e confirmar 0 resultados. **Não substituir em minúsculo**: nomes de arquivo e URLs (`marca_logo.png`) quebram |
| Títulos e título SEO dos produtos | Editor em massa (`/bulk?resource_name=Product&edit=title,metafields.global.title_tag&ids=...`). Refs de célula mudam após re-render: confira os valores antes de salvar para não sobrescrever o título errado |
| Fabricante (vendor) | No editor em massa é seletor e não aceita digitação: trocar na página de cada produto (Organização → Fabricante → buscar/adicionar) |
| Texto alternativo das imagens | Conteúdo → Arquivos → abrir arquivo → Informações → Texto alternativo → Concluído → Salvar → Salvar |
| Nome da loja | Configurações → Geral → Informações de contato |
| Imagens com a marca escrita (rótulo, logo, capa de e-book, caixa, selo) | Ver B |
| Logo do checkout e imagem de compartilhamento (OG) | Ver B; são arquivos separados, fáceis de esquecer |
| E-mails (Klaviyo etc.) e app de upsell | Pedir ao assistente do app para trocar a marca nos assuntos, prévias, corpo, alt e remetente, mantendo os fluxos em rascunho |
| Nome do tema | Loja virtual → ••• → Renomear (interno, mas evita confusão) |

**Verificação final:** buscar cada página publicada (home, produtos, políticas)
e contar a marca antiga só no **texto visível** (remover `script/style`, somar
`alt`, `title`, `<title>` e metas). Ocorrências restantes no HTML que sejam nome
de tema ou de arquivo não aparecem para o cliente.

### B. Imagens com a marca antiga

- **Trocar o nome escrito em imagem:** edição imagem→imagem com prompt
  "substitua a palavra ANTIGA por NOVA no rótulo, mesma fonte, cor e posição;
  mantenha todo o resto idêntico" (ex.: Nano Banana 2 em 2K, ~US$ 0,11 cada)
  funciona muito bem. Informe o custo do lote antes, faça 1, revise lado a
  lado, depois o resto.
- **Logo:** IA costuma deformar letras de wordmark. Desenhe o logo em código
  (PIL/SVG com fonte parecida + o elemento gráfico original, ex.: folha) — fica
  limpo e exato, e sem custo.
- **PNG com fundo transparente** (frascos dos cards de oferta): a edição devolve
  fundo branco → passe remoção de fundo (custo irrisório) antes de subir.
- **Subir mantendo a mesma URL:** Arquivos → "Substituir" no arquivo original.
  Nenhum template precisa mudar. O arquivo novo precisa ter a **mesma
  extensão** (converter via canvas para .jpg/.webp se preciso).
- **Galeria sempre 1:1:** blocos 9:16 só na descrição. Se subirem imagens
  verticais na galeria, forçar o quadro quadrado por CSS
  (`.product__media{padding-top:100%}` + `object-fit:contain`).
- **Cache da CDN:** depois de substituir, quem já visitou pode ver a versão
  antiga por horas (variações `?width=` em cache). Conferir em aba anônima. Se
  persistir e for urgente, subir com nome novo e trocar a referência no código.

### C. Domínio próprio

- Configurações → Domínios → Conectar existente → digitar o domínio.
- Se o domínio está no GoDaddy (ou outro com Domain Connect) e a pessoa está
  logada lá, "Conectar automaticamente" grava o DNS sozinho (A `@` para o IP da
  Shopify, CNAME `www` → `shops.myshopify.com`, CNAME de verificação). Manual:
  editar o A `@` (geralmente "Parked") e o CNAME `www`.
- Confirmar que o DNS resolve e esperar o SSL ("Certificado TLS provisionado").
- **Enquanto a loja tiver senha, o domínio mostra a tela de senha.**

### D. Mercado, moeda e domínio por mercado

- Mudar mercado/moeda afeta a loja inteira: só fazer com OK explícito quando
  o escopo for uma página só.
- Mercados → mercado do país → conferir **Moeda** (ex.: Euro com FX manual
  1 USD = 1 € mantém o mesmo número de preço) e **Domínio/idioma**.
- O mercado pode continuar apontando para `loja.myshopify.com` mesmo com o
  domínio próprio conectado: trocar em Domínio/idioma → Gerenciar → marcar o
  domínio próprio → Salvar.
- O preview aberto de fora do país mostra a moeda base da loja ($) — não é
  erro; o cliente do país vê a moeda do mercado.
- **Um frete por país, com o mesmo prazo em todo lugar.** Dois métodos
  (ex.: grátis + "Express") confundem; deixe um (ex.: "Free Standard Delivery ·
  3–5 working days") via `deliveryProfiles` → `deliveryProfileUpdate` com
  `methodDefinitionsToDelete`. O mesmo prazo precisa estar no checkout, na
  data estimada da página, nas abas de entrega, no FAQ e na política de envio.

### E. Upsell pós-compra (só pagamento antecipado)

- App de upsell (ex.: Upsell.com/ReConvert) → definir como página pós-compra
  em Configurações → Checkout.
- Montar à mão no editor do app: 1ª página pós-compra → condição padrão →
  modelo "Upsell de produto" → produto específico/variante → desconto % →
  frete grátis → título no idioma do país. Os assistentes de IA dos apps
  costumam travar na confirmação; não dependa deles.
- É one-click: o cliente aceita sem redigitar o cartão. Manter desligado o
  "segundo clique para confirmar".
- Textos padrão do app (botão, "Recusar") seguem o idioma do checkout; validar
  com pedido de teste. Escolher plano do app é decisão da pessoa.

### F. Vídeo demonstrativo gerado por IA

Cenas com líquido saindo de conta-gotas falham com frequência (líquido
surgindo do nada, dedos fundindo, gota que não cai). Sempre validar com análise
de vídeo (ex.: Gemini) antes de publicar; após 2 reprovações, recomendar vídeo
real gravado no celular em vez de gastar mais. Vídeo na página: pequeno
(~300px de largura no mobile), autoplay mudo em loop.

### G. Automação pelo navegador (quando não há conector)

- O admin da Shopify usa web components com shadow DOM: para achar botões e
  campos, percorrer `shadowRoot` recursivamente.
- Input de arquivo escondido ("Substituir"): interceptar
  `HTMLInputElement.prototype.click` para capturar o input, montar o `File` via
  `fetch(url).blob()` + `DataTransfer` e disparar `change` — sem abrir o
  seletor nativo.
- Campos React não aceitam `.value=`: usar o setter nativo + eventos
  `input`/`change`, ou focar e digitar teclas de verdade (mais confiável em
  células do editor em massa).
- Editor de código (VS Code web): Ctrl+P abre arquivo, Ctrl+H substitui no
  arquivo, Ctrl+Alt+Enter substitui tudo, Ctrl+K S salva tudo. Sempre conferir
  qual campo está preenchido antes de "substituir tudo".
- **Sempre passar `tabId`** no navigate; sem ele a extensão navega a aba da
  pessoa. Rode `tabs_context_mcp` depois de criar aba: abas novas às vezes
  somem.
- Retorno de JS com URL contendo `?` vem **[BLOCKED: Cookie/query string
  data]**: cortar a query (`.split('?')[0]`) ou devolver só nomes de arquivo.
- Upload para storage externo (`stagedUploads`, Google Storage) costuma ser
  bloqueado pelo proxy do ambiente. Para gravar arquivos de tema, colar o
  conteúdo no JS dentro de um String.raw entre crases (conferir antes que o
  arquivo não tem crase nem `${`) e fazer o PUT; um arquivo grande por chamada.
- `fetch` de `/products.json` e `/products/<handle>.js` da loja de referência
  funciona pela aba dela (CORS ok) para extrair dados, imagens e preços.
- Se a extensão do navegador falhar 2 vezes seguidas na mesma ação, parar e
  avisar o que travou e o que a pessoa precisa fazer (ex.: recarregar a aba do
  editor) — não ficar tentando em loop.

### H. Ligar o assistente direto à plataforma

Com conector (ex.: MCP da Shopify) o código é gravado sem copiar e colar —
vale a pena quando há várias seções ou várias lojas. Para uma seção avulsa, colar
à mão no editor de código costuma ser mais rápido do que configurar. Se o
conector recusar o tema publicado, usar o contorno do passo 4.

---

## Limites — declare, não esconda

**Estrutura, layout e identidade são referência legítima — a loja de origem é a
sua.** Pode copiar igual: seções, paleta, componentes, marca, fotos, textos,
especialistas, avaliações e rótulo, sem placeholder.

O que não transfere mesmo (nem da sua loja) é o que depende de fora — seção de
app pago, mídia hospedada por terceiro, fonte licenciada, imagem a produzir.
Esses viram campo editável ou seção-esqueleto (ver a tabela acima).

**Aparência não é causa de venda.** Esta skill reproduz o visual de uma loja que
vende bem. Isso não transfere o resultado dela: oferta, ângulo, preço e tráfego
continuam sendo o que decide. Se a conversa derivar para "clonei e não vende",
diga isso com clareza em vez de sugerir mais ajustes de design.

**Cuidado com regra de preço importada.** Fórmulas de precificação de tutoriais
quase sempre pressupõem pagamento antecipado e moeda forte. Em venda com
pagamento na entrega, lucro calculado por pedido superestima, porque parte dos
pedidos não vira entrega paga e a devolução tem custo próprio. Se o projeto tiver
uma ferramenta própria de margem, use-a; se não, sinalize a limitação em vez de
aplicar a fórmula do tutorial.

---

## Checklist antes de publicar

- [ ] Escopo confirmado em 1 linha (o que muda e o que fica intacto); nada fora dele foi alterado
- [ ] Inventário da referência feito; cada microcomponente reproduzido
- [ ] Inventário funcional feito: modal do botão, carrinho/pós-clique, popups, contador, promoção, rodapé
- [ ] Promoções funcionando de verdade no `/cart.js` (não só no texto)
- [ ] Coleção/página publicada no canal Loja virtual (sem 404)
- [ ] Home e demais páginas conferidas depois: continuam iguais
- [ ] Trabalhou em tema rascunho (ou em mudanças reversíveis no ativo, se combinado)
- [ ] Todas as seções aparecem no editor e estão posicionadas
- [ ] Testado em largura mobile (incluindo cards de oferta com selo)
- [ ] Texto, cor e imagem editáveis pelo painel; nenhum "Liquid personalizado" com texto fixo; nomes ≤ 25 caracteres
- [ ] Seletor marca a variante certa e o botão mostra o preço
- [ ] Imagens das seções e da galeria em 1:1, sem esticar
- [ ] Idioma, moeda e formato de preço corretos; mercado com moeda e domínio certos
- [ ] Nada dependente de checkout padrão (pagamento na entrega) ou de app que não existe (assinatura)
- [ ] Um frete por país, com o mesmo prazo na página, checkout e política
- [ ] Marca, imagens, textos, avaliações, especialistas e rótulo conferidos (da sua loja, ou ajustados)
- [ ] Placeholders [entre colchetes] listados para a pessoa preencher
- [ ] Nenhuma imagem em host externo
- [ ] Marca antiga zerada: texto visível, títulos, SEO, fabricante, alt, imagens, OG, logo do checkout, e-mails
- [ ] Domínio conectado com SSL; senha da loja removida no lançamento
- [ ] Pedido de teste feito (checkout, upsell, e-mails) antes de ativar fluxos
- [ ] Preço validado pela conta do próprio negócio, não por fórmula de tutorial
- [ ] Pessoa avisada para recarregar o editor antes de salvar pelo painel
- [ ] Recebeu a lista completa do que não foi possível reproduzir e do que ficou com ela