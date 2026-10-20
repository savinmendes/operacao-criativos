---
name: "paginas-produto-shopify"
description: "Página de produto Shopify COD de ponta a ponta: produzir a página no Flora (blocos 9:16, foto principal e galeria 1:1) e espelhar produtos e tema entre lojas próprias de países diferentes."
---

# Páginas de produto Shopify — produzir e espelhar

Junta 4 skills que se complementam (producao-pagina-cod, pagina-produto-flora,
espelhar-lojas-cod, clonar-pagina-entre-paises). Copiar o design de uma loja ou
página de referência (inclusive de concorrente) e o pós-clone ficam na skill
separada `replicar-loja-ecommerce`, que continua valendo como está.

## Qual modo usar

| Pedido | Modo |
|---|---|
| Link ou fotos de um produto + "faz a página", "foto principal", "galeria", "refaz a página de vendas" | **A — Produzir página (Flora)** |
| "leva esse produto da loja X para a loja Y", "deixa o tema da Guatemala igual ao do Chile", várias páginas para outro país | **B — Espelhar entre lojas próprias** |
| "copia / clona / replica essa loja/página/seção", "quero igual a essa", relançar loja com outra marca | Use a skill `replicar-loja-ecommerce` |

Fluxo comum: **A → B** — página pronta numa loja (ex.: Chile) e depois levada
para as outras (Guatemala, México, Colômbia). Quando também houver replicar
design: primeiro a estrutura (`replicar-loja-ecommerce`), depois o conteúdo
(Modo A) — nunca os dois num disparo só.

---

## Regras comuns (valem para os dois modos)

**Forma de trabalhar**
- Fale em português do Brasil. Execute direto; pergunte só o que for essencial e não der para inferir, e pergunte tudo de uma vez.
- No fim, entregue UMA lista completa do que ficou para a pessoa fazer à mão.
- Lote: termine o primeiro item completo (até a verificação), mostre, ajuste o máximo possível e só depois rode o resto no mesmo molde.
- Ferramenta ou navegador travou (clique que não responde, erro repetido, bloqueio): no máximo 1 tentativa alternativa; falhou de novo → pare e diga o que travou e o que a pessoa precisa fazer. Nunca fique em loop.
- Economize tokens: arquivo grande do tema nunca entra no contexto — salve no sandbox, use grep/diff e leia só o necessário. Em lote, leia cada arquivo uma vez.
- Gastos com geração: informe o custo estimado da leva ANTES de gerar e avise antes de passar do valor informado (re-tentativas, modelo extra).

**Regras da operação (padrões do dono; troque se for outra operação)**
- Lojas COD: sem parcelamento em nenhum texto; nada que dependa do checkout padrão (upsell de checkout, order bump, one-click).
- Garantia sempre 90 dias. Sem hora do dia nos textos ("esta noche" não). Preço quem define é o dono — nunca inventar.
- Preço riscado (compareAtPrice) = 2× o preço de venda da oferta, arredondado ao formato do país.
- Galeria/foto principal do produto SEMPRE 1:1. Blocos verticais 9:16 só na descrição.
- Público sênior: textos grandes e de alto contraste.
- Tema: o dono acha arriscado duplicar/trocar tema. Padrão = trabalhar no tema ATIVO só com arquivos novos ou trocas reversíveis (seções com prefixo próprio, template alternativo `product.<nome>.json`, bloco "Liquid personalizado" pequeno), guardando o conteúdo original de cada arquivo antes de sobrescrever. Nunca publicar, apagar ou trocar tema. (Em outra operação, o padrão seguro é duplicar o tema ativo para rascunho antes de mexer.)
- Imagens sempre nos Arquivos da própria loja, nunca em host externo (postimg, imgur).
- Toda geração de imagem parte da FOTO ORIGINAL do produto (image-to-image). Sem foto, pare e peça.
- Vídeo gerado por IA: validar com análise de vídeo (ex.: Gemini) antes de publicar — física, deformação, coerência.

**Modelo de venda — determine sempre antes de construir**

| Modelo | Consequência |
|---|---|
| Pagamento antecipado (cartão, Pix) | Upsell de checkout, order bump e one-click fazem sentido |
| Pagamento na entrega (COD) | Checkout vira formulário (ex.: app Releasit). Não construa nada do checkout padrão |
| Venda por conversa (WhatsApp, closer) | A página só apoia; o botão leva ao canal, não ao carrinho |

Também não reproduza recurso que a loja não cumpre (ex.: "Subscribe & save" sem app de assinatura).

**Identidade e limites**
- Loja de origem é do próprio dono → pode copiar tudo: seções, paleta, textos, fotos, marca, avaliações, rótulo.
- Loja de terceiro (concorrente) → copie estrutura, layout e ângulo; escreva o texto do zero e não use logo, nome de marca, fotos originais nem fonte licenciada. Se pedirem identidade de terceiro, recuse só essa parte em uma frase e siga com o resto.
- Não use nome de marca de terceiro em imagem ou texto se o produto não é da marca (inclusive a marca que aparece na caixa do fornecedor).
- Só claims confirmados (ficha da referência ou ditos pelo dono). Não inventar watts, bateria, certificação, avaliações. Se o dono inventar um claim (peso, "nanotecnologia"), use, mas avise uma vez que precisa bater com o produto real (risco de recusa no COD).
- Aparência não é causa de venda: oferta, ângulo, preço e tráfego decidem. Se virar "clonei e não vende", diga isso.
- Preço e margem: use a calculadora/ferramenta própria do negócio, não fórmula de tutorial (que pressupõe pagamento antecipado e superestima lucro em COD).

---

## Conector Shopify (os dois modos)

1. `get-shop-info` antes de tudo. Loja errada → `switch-shop` → `get-shop-info` (se pedir login, a pessoa reconecta em Configurações → Conectores → Shopify e escolhe a loja). Se a loja conectada não for a do mercado, entregue HTML em vez de publicar.
2. Faça uma leitura trivial antes de construir. Se não volta dado, resolva a conexão antes — senão todo erro vai parecer erro de código. "Disse que fez e nada aparece" = suspeite de permissão antes do código.
3. Permissões necessárias: temas e código do tema, produtos, arquivos, conteúdo (leitura e escrita).
4. GraphQL: `graphql_schema` → montar → `validate_graphql_codeblocks` → `graphql_mutation`/`graphql_query`.

**Gravar arquivos de tema — método principal (`themeFilesUpsert`)**
```graphql
mutation($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    userErrors { filename code message }
  }
}
```
- `files: [{ filename: "templates/product.<sufixo>.json", body: { type: TEXT, value: "<conteúdo>" } }]` — vale para arquivo novo e para sobrescrever (templates, sections, snippets, assets de texto). Vários arquivos por chamada. Arquivo grande: monte no sandbox e mande o valor inteiro, sem colar no chat.
- Tema ativo: `themes(roles:[MAIN]){id name}`; guarde o gid.
- Depois de gravar, confira `files(filenames:[...]){checksumMd5 size}` contra o md5 calculado no sandbox.
- Erro de Liquid/JSON vem em `userErrors`: corrija e reenvie; nunca deixe arquivo quebrado. Se gravou errado, reenvie o original guardado.
- `themeFilesUpsert` só grava arquivo; não cria, publica nem apaga tema.

**Plano B — sem escopo `write_themes` (access denied):** app custom na loja (Configurações → Apps e canais de vendas → Desenvolver apps → Criar app → escopos Admin API `write_themes`, `read_themes` → Instalar → copiar token). Passe esse passo a passo inteiro de uma vez. Com o token, a mesma mutation em `https://<loja>.myshopify.com/admin/api/2025-07/graphql.json` com header `X-Shopify-Access-Token`. O token fica só no sandbox; nunca repetir no chat.

**Plano C — pelo admin no navegador (extensão), sem trocar tema:**
```
csrf = fetch(location.href) → HTML → /"csrfToken":"([^"]+)"/
GET  /store/<loja>/themes/<id>/assets.json?asset[key]=<arquivo>
     → .asset.value (template JSON vem com comentário /* */ no topo: remover antes do JSON.parse)
PUT  mesma URL sem query; headers Content-Type/Accept JSON + X-CSRF-Token; body {asset:{key,value}}
DELETE mesma URL com ?asset[key]=<arquivo>
```
- 403 "CSRF": busque o token de novo. Conteúdo grande: em pedaços com String.raw numa variável `window`, conferir tamanho e fazer o PUT numa chamada separada.
- Sempre releia o arquivo atual antes de gravar e altere só a sua parte (a pessoa pode ter editado pelo painel).
- **Editor aberto sobrescreve:** se a pessoa estiver no "Personalizar tema" e salvar, a versão antiga volta. Depois de gravar, peça F5; se acontecer, regrave só a sua parte.
- Alternativa manual (copiar/colar no editor de código): botão injetado na aba do admin com `navigator.clipboard.writeText(conteudo)`; Ctrl+P abre o arquivo; Ctrl+A → Ctrl+V → conferir pelo zoom → Ctrl+S; conferir md5 depois (arquivo criado pelo editor pode sair com CRLF). Se o editor não responde, `document.visibilityState` está "hidden": peça para deixar o Chrome na frente e não usar o PC durante a colagem. Atalho com foco fora do editor abre "Adicionar página": feche sem salvar. Não usar "substituir tudo".

**Automação pelo navegador — macetes**
- Admin usa web components com shadow DOM: percorra `shadowRoot` recursivamente.
- Input de arquivo escondido ("Substituir"): intercepte `HTMLInputElement.prototype.click`, monte o `File` com `fetch(url).blob()` + `DataTransfer` e dispare `change`.
- Campos React: setter nativo + eventos `input`/`change`, ou digitar teclas de verdade (melhor no editor em massa).
- Sempre passe `tabId` no navigate; rode `tabs_context_mcp` depois de criar aba.
- Retorno de JS com URL contendo `?` vem bloqueado: corte a query (`.split('?')[0]`).
- `fetch` de `/products.json` e `/products/<handle>.js` da loja de referência funciona pela aba dela (dados, imagens, preços).
- A extensão do Chrome não funciona em páginas claude.ai: não use artifact como fonte de cópia.

---

## Modo A — Produzir página de produto (Flora → Shopify)

**Entrada:** link do produto (marca, concorrente, AliExpress, TikTok Shop — para Kalodata use a página pública `https://shop.tiktok.com/view/product/<id>`) ou fotos originais (ideal 6 a 11). Mercado padrão: Chile, espanhol chileno — trave o idioma em todo prompt. Oferta (kits 1/2/3, frete): se faltar, marcador e aviso.

**Entregas (sempre as três)**
1. Página — blocos 9:16 com o texto de venda DENTRO da imagem. Padrão: 14 blocos (5 ficou simples demais). O número não é fixo: só faça o bloco se houver informação real para ele; não invente para completar.
2. Foto principal da variante 1:1.
3. Galeria 1:1 (6–7 imagens) + HTML da descrição + imagens baixadas.

**Estrutura dos 14 blocos**
1 Hero (promessa + produto na cena do país + uso + faixa com 3 ícones) · 2 Problema (dor, sem produto) · 3 Mecanismo + 3 ícones com números reais · 4 Uso/controle central · 5 Benefício 2 · 6 Prova visual (antes/depois, dia/noite) · 7 Benefício 3 · 8 Colagem "feita para…" (3 painéis, 1 legenda cada) · 9 Ficha técnica em 6 cards (≤4 palavras) · 10 Uso/instalação em 3 passos · 11 Comparativo comum × este (3 linhas ✗/✓) · 12 O que vem na caixa · 13 FAQ (3 perguntas) · 14 "Compra sin riesgo": selo 90 días de garantía + "Paga al recibir" + "Envío a todo <País>".

**Foto principal da variante (padrão aprovado)**
- Fundo claro; título no topo em 2 linhas (navy + ciano).
- CAIXA PEQUENA de papelão aberta (~20×15×10 cm — pacotes COD reais são pequenos), produto DESMONTADO e justo dentro (corpo, peças, suporte, parafusos, cabo, chip se 4G) + produto MONTADO ao lado.
- Selo de peso fixo (número dado pelo dono) + "Nanotecnología súper liviana". Sem a frase "Todo llega en una caja".
- Vários produtos parecidos: mesma ideia, composição e peso DIFERENTES para cada (mão segurando / caixa apoiada / duas mãos; faixa / selo redondo / etiqueta vertical).
- Conferir: peças no formato real, placa de parede visível, nenhuma peça duplicada.

**Regras de geração**
- Fidelidade > criatividade: mesmo produto das fotos (cor, formato, peças). Entradas dos blocos = FOTOS ORIGINAIS, não referências geradas (o produto muda).
- Remover logos de marca e grafismos digitais ("4G LTE" desenhado, setas, diagramas). Não pôr "2K"/Wi-Fi/4G sem confirmação.
- Máx. 2 mensagens + 3 rótulos por bloco; headline ~1/10 da altura; sem preço na arte; nenhum texto de produção (bloco, hero, CRO) na arte.
- Modelo dos blocos com texto: GPT Image 2.5 Sunburst (`is2i-gpt-image-2-5-sunburst`, high, 1k; ~US$ 0,06–0,13/img — confira o `run_cost` real). Referências sem texto (360, ficha do kit): Nano Banana Pro (`is2i-gemini-3-pro`, ~US$ 0,18). Um modelo por tipo de geração; só troque se falhar, avisando.
- Lote: bloco 1 + foto principal → revisar → resto junto (até 20 por chamada).
- Correção pontual: editar com a própria imagem gerada como ref. 1 (+ foto original como ref. 2), "keep everything identical, change only…".
- Se o pedido mudar no meio de uma geração lenta, gere já a versão com tudo junto.
- Foto de etiqueta de transportadora tem dados de cliente: só referência de tamanho, nunca entrada de geração.

**Template de prompt**
```
INTERNAL INSTRUCTIONS — DO NOT RENDER ANY OF THIS TEXT EXCEPT THE SPANISH COPY IN QUOTES.
Create <block N (9:16) | square (1:1) main image> for an online store in <País>: <PAPEL DO BLOCO>.
Visual system: navy #0B1F3A, cyan #22C3E6, white; extra-bold sans-serif; realistic commercial photo.
PRODUCT FIDELITY (most important): EXACTLY the product in reference 1 — <descrição física curta>.
Same shape, colors, parts and markings. Do not redesign, add or remove parts. REMOVE every brand logo and digital graphics.
SCENE/LAYOUT: <cena; pessoa 45–70 anos quando houver; cenário do país; enquadramento>.
TEXT (Spanish for <País>, exactly as written, nothing else): Headline "…" Subheadline "…" Badges (máx. 3) "…"
TYPOGRAPHY: big, high contrast, readable at ~390 px wide by an older audience. No other text, no prices, no watermark, no layout labels.
```

**Passo a passo**
1. Ler a referência: `<url>.json` da Shopify (fotos) + WebFetch da página (features, ficha, caixa, FAQ).
2. Conector Shopify (ver acima).
3. Canvas: um projeto Flora POR PRODUTO, `flora_create_project` "[Produto] — Página [País]"; fotos originais como static_image na coluna "00 Foto original NN".
4. Bloco 1 + foto principal → revisar ao lado da foto original → resto em lote → revisar tudo → corrigir só o que errou.
5. Organizar: rótulos "02 Bloco NN · tema", "03 Galeria NN", "04 PRINCIPAL · produto · peso", "99 DESCARTE · motivo"; `flora_arrange_canvas` em linhas; nota "COMECE AQUI" com claims, custo e pendências. Salvar imagens finais + prompts na base local de arquivos do dono, no padrão de nomes dela.
6. Publicar: `descriptionHtml` = sequência dos blocos (`<img>` 100%, `alt` = headline, `loading="lazy"` a partir do 2º). Mostrar antes de gravar; produto novo entra como rascunho; galeria 1:1 com a principal primeiro. Conferir a página publicada no mobile.
7. Entregar: HTML, links na ordem, imagens baixadas e a lista do que fica manual (confirmar specs/peso com fornecedor, subir em Arquivos e trocar links, preço).

**Ambiente (nuvem)**
- A nuvem pode não acessar media.flora.ai / storage.googleapis.com. Revisar: injetar overlay com as imagens na aba do Chrome do dono e tirar screenshot. Baixar: no Chrome dele, `fetch(url)` → blob → `<a download>`, uma imagem por chamada; mande os links como reserva.
- Fotos anexadas no chat: peça para arrastar no canvas do Flora (ou usar o `upload_page` do `flora_create_asset`), ache os nós com `flora_get_canvas` e use o `output_url`.
- Mostrar imagens no chat com `![](url)`.
- Depois de publicar, com tráfego: ler Clarity (rolagem e cliques) e efetividade real (Shopify × logística pelo nº do pedido) para decidir qual bloco trocar.

---

## Modo B — Espelhar produtos e tema entre lojas próprias de países diferentes

Leva uma ou várias páginas de uma loja do dono (ex.: Chile) para outra (Guatemala, México, Colômbia), ou deixa o tema de uma igual ao da outra. Não é para concorrente nem para copiar design de referência (isso é a `replicar-loja-ecommerce`).

**0. Entradas (pedir tudo de uma vez)**
- Loja ORIGEM e DESTINO (país, moeda, língua).
- Produtos: URL ou handle + preços das ofertas na moeda do destino (o dono define). Vários: tabela `handle | COMPRE 1 | COMPRE 2 | COMPRE 3`.
- Mês da oferta (padrão: mês atual em espanhol, ex. OCTUBRE).
- Transportadoras do destino, se o país ainda não tiver card de envio pronto.
- Para sincronizar tema: .zip do tema da ORIGEM (Temas → ⋯ → Baixar arquivo do tema).

**Lote**
- Uma vez por loja: passo 1, passo 5 (sincronizar tema/snippets de estilo) e card de envio do país — ANTES do primeiro produto.
- Por produto: passos 2, 3 e 4. Primeiro produto completo até o passo 6, mostrar, depois o resto.
- O template adaptado do primeiro vira base dos seguintes (trocar handle, textos específicos, preços, `breaks_benefits`); gravar todos numa só chamada e conferir os md5 de uma vez.
- Fim do lote: tabela `produto | URL destino | preços conferidos | status` + prints origem × destino. Produto com problema fica marcado; não para o lote.
- Produto já existe no destino (mesmo handle): não criar de novo; `productUpdate` só no que mudou.

**1. Conectar e conferir** — `get-shop-info` / `switch-shop`; confirmar moeda; tema ativo + `theme_name/theme_version` em `config/settings_schema.json` (grep). Tema diferente da origem → PARAR e avisar. Guardar o gid do tema.

**2. Produto**
- `productCreate` (title, handle, productType, vendor, ACTIVE, `media` com as URLs da origem na mesma ordem).
- Variantes de oferta: NÃO usar `productVariantsBulkCreate` direto ("A opção não existe"). `productOptionsCreate` com `variantStrategy: CREATE` (opção "Oferta": COMPRE 1, RECIBA 2 / COMPRE 2, RECIBA 4 / COMPRE 3, RECIBA 6) → `productVariantsBulkUpdate` com price, compareAtPrice (2×), `inventoryPolicy: CONTINUE`, `inventoryItem:{tracked:false}` (senão "Agotado").
- `publishablePublish` na publicação "Loja virtual". Depois do template: `productUpdate` com `templateSuffix`.
- Preço por unidade: o selo "MAYOR AHORRO" tem que estar na oferta mais barata por unidade; se não, avisar e propor ajuste.

**3. Adaptar o template JSON (sandbox)**
- Pegar o template da origem (zip ou `files(filenames:[...]){body{...on OnlineStoreThemeFileBodyText{content}}}`) e trocar: país em selos/títulos ("Más vendido en <País> 2026", "Envío a toda <País>"), cidades e bandeira dos depoimentos, moeda e formato numérico, mês da oferta, preço por unidade (`breaks_benefits`), card de envio.
- Editar bloco: localizar o `custom_liquid` e substituir com `JSON.stringify(novoHtml)`.
- `JSON.parse` para validar e procurar restos da origem (país, cidades, transportadoras, moeda, bandeira): zero.
- Guardar o original antes de sobrescrever.

**4. Gravar** — `themeFilesUpsert` + checksum (ver "Conector Shopify"), com planos B e C se faltar escopo.

**5. Sincronizar tema com a origem (quando "não fica igual")**
- Comparar md5 dos arquivos ligados à página de produto (main-product, variant-picker, snippets renderizados, assets) entre o zip da origem e o destino; enviar o que diferir.
- A diferença costuma estar em snippets de estilo carregados por `snippets/meta-tags.liquid` (ex. `pagina-produto-estilo.liquid`, `pagina-produto-extra.liquid` dentro de `if request.page_type == 'product'`). `grep` no zip pelas classes vistas na referência.
- Diferença em `main-product.liquid` pode ser só reescrita automática da Shopify ("This file has been rewritten…").
- App de COD diferente da origem (ex. Releasit vs buy_buttons): ajustar posição do botão, ex. `@media (max-width:749px){product-info.product__info-container>.shopify-app-block[class*="rsi-app"]{order:4}}`.

**6. Verificação final (obrigatória)**
- No destino (JS + print): textos do país, nada da origem, sem "Agotado", sem imagem quebrada, logos carregados, sem rolagem horizontal, fonte e ordem dos blocos iguais à referência.
- Abrir o formulário do app COD com uma oferta e conferir o preço (fechar sem enviar).
- Conferir outro produto que use o mesmo `main-product`.
- Prints do celular origem × destino e lista do que ficou diferente.

**Cards de envio por país** — bloco "Envío a todo <País>" com logos das transportadoras: cards brancos, borda `#E3E5E8`, logo `height:34px;width:auto;max-width:90%`; logo branco/transparente → card `#1E2328`. Falta arte → gerar no Flora com o print das logos como referência (avisar custo) e subir com `fileCreate`. Na primeira vez de cada país, registrar aqui o HTML final e as URLs das logos:
- Chile: bloco `envio-cl` da origem.
- Guatemala / México / Colômbia: preencher.

---

## Pegadinhas da Shopify

| Erro | Correção |
|---|---|
| `name é muito longo (máximo de 25 caracteres)` | Nome de seção, preset e bloco ≤ 25 caracteres |
| `Variable ... was not properly terminated` | Não usar `{palavra}` dentro de `{{ }}`; usar `[price]` |
| setting `url` recusa `mailto:` | Usar `text` para mailto/tel |
| `Namespace é muito curto` em `metafieldsSet` | Namespace com 3+ letras |
| Coleção nova dá 404 | `publishablePublish` na "Loja virtual" |
| Coleção automática enche devagar | Coleção manual + `collectionAddProducts` na ordem da referência |
| Imagem do template não aparece | `fileCreate` pode trocar a extensão: consultar `files(query:"filename:prefixo-*")` e usar o nome real em `shopify://shop_images/<arquivo>` |
| Banner com altura 0 | `aspect-ratio` em vez de altura fixa |
| App de carrinho (Rapid Cart, Upcart) abre por cima | Só no template: esconder o app por CSS e ouvir o clique em captura (`addEventListener('click',fn,true)` + `stopImmediatePropagation`); avisar que o seguro do app some ali |
| Imagem esticada com `image_tag` | `height:auto!important;aspect-ratio:1/1;object-fit:cover` |
| Variantes "A opção não existe" | `productOptionsCreate` antes de atualizar variantes |
| Produto "Agotado" | `inventoryPolicy: CONTINUE` + `tracked:false` |
| Upload para storage externo bloqueado | Colar o conteúdo em String.raw (sem crase nem `${`) e PUT; um arquivo grande por chamada |

---

## Checklist antes de entregar

**Sempre**
- [ ] Modo certo; nada fora do escopo alterado (home e outro produto conferidos)
- [ ] Tema ativo intacto fora dos arquivos novos/alterados; originais guardados; checksums conferidos
- [ ] Mobile conferido (cards com selo, sem rolagem horizontal, imagens sem esticar)
- [ ] Idioma, moeda, formato de preço e textos do país corretos; nada da origem sobrando
- [ ] COD: sem parcelamento, nada de checkout padrão; garantia 90 dias; sem hora do dia
- [ ] Galeria 1:1; 9:16 só na descrição; imagens nos Arquivos da loja
- [ ] Custos de geração avisados antes; nenhum gasto extra sem aviso
- [ ] Lista COMPLETA do que ficou manual

**Modo A**
- [ ] Produto fiel às fotos originais; sem logo de terceiro; só claims confirmados
- [ ] Texto grande, máx. 2 mensagens + 3 rótulos por bloco, sem preço na arte
- [ ] Canvas organizado e arquivos + prompts salvos na base local

**Modo B**
- [ ] Preços conferidos no formulário COD; selo "MAYOR AHORRO" na oferta certa
- [ ] Card de envio do país correto; prints origem × destino enviados; tabela do lote