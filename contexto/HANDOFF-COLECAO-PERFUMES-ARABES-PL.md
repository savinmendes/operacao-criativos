# Handoff: coleção "Perfumes Árabes" (Chile) → versão Polônia

**Leitor:** outra instância do Claude, que vai usar as skills `replicar-loja-ecommerce` e `clonar-pagina-entre-paises` para montar o equivalente na loja da Polônia.

- **Referência no ar (Chile):** https://arabesperfume.cl/collections/p-arabes
- **Loja Shopify:** Chile Verificada / "Llego la Tienda". Antes era chileverificada.com, e o handle da coleção era `perfumes-arabes`. Hoje a coleção está em `p-arabes`, no domínio arabesperfume.cl.

**Antes de editar:**
- Confira com `get-shop-info` qual loja o conector Shopify está acessando. Em 11/10/2026 o conector estava na loja **Pellorini**.
- Peça à pessoa para trocar para a loja certa (Chile para consultar, Polônia para criar).

## 1. O que foi construído no Chile (09–10/10/2026)

### 1.1 Produtos (13 Lattafa + 2 packs antigos)

**Kits de 3 × 100 ml** (preço 59.900 CLP, tags `kit`, `mujer`):
- Kit 1: Yara + Yara Moi + Yara Elixir.
- Kit 2: Yara + Yara Tous + Yara Elixir.
- Kit 3: Yara + Yara Tous + Yara Moi.
- Kit 4: Yara + Yara Moi + Yara Candy.
- Kit 5: Yara Candy + Yara Moi + Yara Elixir.

**Unitários 100 ml EDP** (34.900 CLP, tag `unitario`):
- Yara, Yara Moi, Yara Tous, Yara Candy e Yara Elixir: `mujer`.
- Asad, Asad Bourbon e Asad Zanzibar: `hombre`.

**Packs antigos que entram na coleção:**
- "Pack 3x1 Hombre Club de Nuit + Asad + 9PM";
- "Pack 3x1 Mujer Yara + Fakhar Rose + Sabah Al Ward".

**Regras de conteúdo:**
- **Yara Rouge (frasco vermelho) foi trocado por Yara Elixir** em todos os kits.
- **Perfumes confirmados como ORIGINAIS** pela pessoa. Selo "Originales Lattafa".
- **Notas olfativas:** só as oficiais, de lattafa.com / lattafa-usa.com ou do Fragrantica, com a fonte citada.

**Padrão da página de produto:**
- **Galeria 1:1:** hero do kit com o nome sob cada frasco e os selos "100 ml cada uno · Pagas al recibir · Garantía 90 días · Originales Lattafa", depois 1 foto por frasco com os ingredientes das notas.
- **Descrição:** 4 blocos em imagem 9:16 (gancho+notas, define tu estilo, hero, "qué incluye") + imagem genérica de garantia de 90 dias. Sem texto.
- **Proibido:** preço na imagem, depoimento inventado e "envío gratis" quando não confirmado.

**Imagens:**
- Flora, com Nano Banana 2 (`i2i-gemini-3.1-flash-image`, US$ 0,072 em 1K, US$ 0,108 em 2K).
- Para vários frascos, usar o `is2i-…` com várias referências.
- Usar sempre a **foto real do frasco como referência** e conferir cada imagem em tamanho cheio. Erros comuns: medalhão errado, "YARA MOI" escrito no corpo (o real diz só "YARA") e rótulo trocado.
- Custo: ~US$ 0,60–0,80 por kit e ~US$ 0,50 por unitário.

**Arquivos:**
- `Downloads\KIT1-YARA-PERFUMES\RELATORIO.md`, que é o padrão-mestre;
- `Downloads\KITS-PERFUMES\BRIEFING.md`, com o briefing usado pelos 8 agentes;
- `Downloads\KITS-PERFUMES\<kit2..5 | uni-*>\` (imagens, `_ref\` com as fotos oficiais e RELATORIO).

**Publicação:** status ACTIVE nos canais Loja virtual, Ponto de venda e Google & YouTube.

**⚠️ Vincular cada produto novo no app Dropi.** Sem vínculo, a venda não vira pedido. Fornecedor Dropi dos Lattafa no Chile: **82275**.

### 1.2 A coleção
- **Smart collection por tag** `perfumes-arabes`. Todo produto com a tag entra sozinho quando é publicado.
- **Ordenação:** mais vendidos.
- **SEO:** título "Perfumes Árabes Originales en Chile | Lattafa, Armaf y Afnan" + meta description + descrição curta.
- **Imagem da coleção:** banner do Flora com frascos sem marca, sem logo e sem texto.
- **Fora da coleção, de propósito:**
  - perfumes de grife (Invictus, 1 Million, Bleu de Chanel, Sauvage), porque não são árabes;
  - o produto "teste".
- **Estudo das grandes lojas:** `Downloads\COLECAO-PERFUMES\ESTUDO-COLECOES.md`, com a seção "Mobile" e prints em `ref-mobile\` de dperfumes.cl (referência da pessoa), Falabella, Notino, Sephora e Ulta. O que vale:
  - produto já na 1ª tela do celular;
  - nada de descrição no topo;
  - chips de 30–36 px;
  - "Filtrar · Ordenar" fixo;
  - card 1:1 com nome de 13–14 px e preço de 16–18 px;
  - 2 colunas no celular e 4 no desktop.

### 1.3 Página da coleção (tema), mobile-first, v2
- **Template próprio:** `templates/collection.perfumes-arabes.json` (no Chile hoje pode ser `collection.p-arabes`; confira o `templateSuffix`). Não mexe nos templates globais.
- **`sections/pa-colecao-topo.liquid`:**
  - **faixa fina** com a imagem da coleção em degradê, a linha "LATTAFA · ARMAF · AFNAN", o H1 em **Cormorant Garamond** (32 px no celular, 52 no desktop) e 3 selos com ícone (Originales · Paga al recibir · Envío gratis);
  - **barra fixa** com "Filtrar · Ordenar" + chips com rolagem horizontal (Todos · Kits y packs · Unitarios · Mujer · Hombre), que filtram por tag via `/collections/<handle>/<tag>`;
  - **cards:** "Nome | detalhe", com o nome em negrito numa linha e o detalhe em cinza em até 2; preço de 16–17 px em negrito; selo "BLACK FRIDAY" pequeno acima do nome.
- **Botão do Releasit** (app de pagamento na entrega, "Pide y Paga al Recibir") nos cards:
  - o app grava estilo inline com `!important`, então um **script reaplica o estilo** só na grade: 40 px, preto, ícone dourado;
  - o clique continua sendo do app.
- **`sections/pa-colecao-seo.liquid`:** texto SEO recolhido com "Ver más", no fim da página.
- **Resultado:** o 1º produto aparece a 24% da tela no celular (antes, 107%), sem rolagem horizontal.
- **Arquivos:**
  - `Downloads\COLECAO-PERFUMES\RELATORIO.md` (seções v1 e v2 + como reverter);
  - `tema\v2\sections\*.liquid` e `tema\v2\templates\collection.perfumes-arabes.json`, prontos para reaproveitar;
  - `backup-v2\`.
- **Também existem `v3-ordem\` e `v3-video\`** na mesma pasta, de outra sessão. Leia o conteúdo antes de reaproveitar.

### 1.4 Carrinho, upsell e Black Friday (ligados à coleção)
- **Carrinho** (`snippets/cv-carrito.liquid`, carregado por `sections/scroll-to-top-btn.liquid`):
  - ícone fixo no topo com contador;
  - botão "Agregar al carrito" **nos cards da coleção**. A pessoa pediu para **tirar da página de produto**, que ficou só com o botão do Releasit;
  - gaveta com "Completa tu pedido": 2 produtos do **mesmo fornecedor Dropi**;
  - trava que não deixa misturar fornecedores no carrinho.
- **Etiquetas exigidas para o carrinho:** só funciona em produtos com as tags `perfumes-arabes` **e** `forn-<id do fornecedor Dropi>`.
  - **Regra da pessoa: mexer só em perfumes e coleção.** Um agente etiquetou 33 produtos de outras categorias e ela mandou remover.
- **Raspadinha** "¡Fuiste seleccionado! 🎁 +1 perfume a mitad de precio":
  - aparece ao adicionar um kit pelo card;
  - opções "Para mí" (mesmo gênero) e "Para regalar" (o outro gênero);
  - **reseta sempre**, a cada kit adicionado;
  - texto "Oferta válida solo para 1 perfume adicional por pedido — el 50% lo asumimos nosotros 🖤".
- **Desconto automático:** "Black Friday +1 perfume 50%", do tipo BXGY (compra 1 da coleção "Promo kits 82275" e leva 1 da "Promo unitarios 82275" com 50%), 1 por pedido.
- **Preço no formulário do Releasit:** o app mostra o preço cheio em cada linha e só desconta no resumo. Um script do tema reescreve a linha com o preço original riscado + o preço com desconto. Não há opção no app.
- **Black Friday** (`snippets/bf-black-friday.liquid`, interruptor `bf_activo`):
  - mensagens na barra de anúncios;
  - faixa nas páginas de produto;
  - **banner de imagem** do Flora na home (desktop 21:9 + mobile 1:1, preto e dourado, sem preço) que leva para a coleção. Estudo em `Downloads\BLACKFRIDAY-TEMA\ESTUDO-BANNERS.md`.
- **Arquivos:** `Downloads\CARRINHO-LOJA\RELATORIO.md` (v1, v2 e v3, mutation do desconto, lógica do upsell) e `Downloads\BLACKFRIDAY-TEMA\RELATORIO.md`.

## 2. Limitações e armadilhas (vão se repetir na Polônia)
1. **Tema publicado:** o conector Shopify **não grava no tema publicado e não publica tema**.
   - Fluxo: `themeDuplicate` → editar a cópia → testar com `?preview_theme_id=<id>` → a pessoa clica em Publicar.
   - Depois que ela publica, a cópia vira o tema ao vivo; a próxima edição exige duplicar de novo.
2. **Seção desligada no tema original:** o template de coleção do Chile tinha a seção "Grade de produtos" desligada (`"disabled": true`), e toda coleção aparecia vazia. Verifique isso logo no começo.
3. **Mutations pela conexão** pedem confirmação da pessoa. Subagentes às vezes são bloqueados ao criar desconto ou pedido: crie você, com aprovação direta dela.
4. **Pedido de teste** (`orderCreate`) foi bloqueado pelo sistema de segurança. Todo pedido não cancelado é importado pela Dropi; cancelado em menos de 1 h, não. Peça à pessoa para fazer o teste pela loja e cancelar.
5. **Releasit:**
   - modo carrinho desligado (a gaveta usa `_rsi.form.mode='normalCart'; _rsi.form.open()`);
   - o botão da página de produto esvazia o carrinho (`addMode: product-only`);
   - o botão dos cards manda o carrinho inteiro;
   - filtros aparecem em português ("Disponibilidade/Preço"): renomeie no app Search & Discovery.
6. **Estoque:** em 11/10 a página do Chile mostrava **todos os 16 produtos como "Agotado"**. Confira estoque/rastreio ("continuar vendendo") antes de copiar a configuração, e avise a pessoa.
7. **Painel ao vivo:** registre as etapas em `Produtividade com ia\painel\painel.py` (`etapa|img|custo|link|fim|pedido`), que fica aberto em http://127.0.0.1:8765.

## 3. Como adaptar para a Polônia (checklist de abertura: pergunte tudo de uma vez)
1. **Loja:** qual loja Shopify, domínio e tema? O conector precisa estar nela.
2. **Idioma e moeda:** polonês (PL) e **PLN**. Traduzir todos os textos de imagem e de tema: selos, chips, SEO, carrinho, raspadinha.
   - "Pagas al recibir" vira **"Płatność przy odbiorze"**.
   - "Envío gratis" vira "Darmowa dostawa".
   - "Originales" vira "Oryginalne".
3. **Oferta e preços em PLN:** kits, unitários e o desconto do 2º perfume. Não invente; pergunte.
4. **Pagamento na entrega na Polônia:**
   - app de COD (Releasit também?) e transportadora (InPost, DPD…);
   - prazo de entrega real.
5. **Fornecedor/logística:**
   - existe Dropi na Polônia? Se não existir, a trava "mesmo fornecedor" e a tag `forn-` precisam de outra regra, ou ficam desligadas;
   - quais perfumes o fornecedor tem: os mesmos Lattafa? Rouge ou Elixir?
6. **Garantia e devolução na UE:** direito de desistência de 14 dias. Confirme os "90 días" e adapte o texto.
7. **Compliance UE:** perfume tem pouca regra de saúde, mas **não use "100% originales" sem a confirmação da pessoa**. A raspadinha "Fuiste seleccionado" (sorteio que todos ganham) tem **risco de prática comercial enganosa na UE**: pergunte se mantém ou suaviza (regra da pessoa: sempre perguntar).
8. **Imagens:** reaproveitar as imagens do Chile trocando só os textos para polonês com Nano Banana 2 (receita testada: lista exata de texto original → novo e "nada mais muda"). Fica mais barato que gerar de novo. Os frascos continuam iguais.
9. **Black Friday:** a data e a mecânica valem na Polônia? O banner e a barra precisam de texto em polonês.

## 4. Ordem sugerida
Checklist (§3) → estudo rápido das grandes lojas de perfume polonesas (Notino.pl, Douglas.pl, Sephora.pl, Perfumesco) no celular → duplicar o tema → produtos (traduzir as imagens do Chile) → coleção smart por tag + template e seções da v2 traduzidos → carrinho/upsell só se houver fornecedor único e app de COD compatível → prints 390 px e 1440 px → a pessoa publica.

## 5. Arquivos para ler primeiro
- `Downloads\COLECAO-PERFUMES\RELATORIO.md` e `ESTUDO-COLECOES.md`
- `Downloads\COLECAO-PERFUMES\tema\v2\` (código da coleção)
- `Downloads\CARRINHO-LOJA\RELATORIO.md`
- `Downloads\KIT1-YARA-PERFUMES\RELATORIO.md` e `Downloads\KITS-PERFUMES\BRIEFING.md`
- `Downloads\BLACKFRIDAY-TEMA\RELATORIO.md`
- `Produtividade com ia\CLAUDE.md` e `contexto\estrategias-criativos.md` (seção Shopify)
