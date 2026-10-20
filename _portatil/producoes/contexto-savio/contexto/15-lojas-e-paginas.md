# Lojas e páginas (Shopify, Dropi, Chegou Operações)

> Como trabalhar nas lojas Shopify da pessoa (perfumes árabes no Chile, Pellorini), clonar design de loja, replicar para outro país, o que nunca fazer (sair do escopo, esconder avaliações) e onde entram Dropi e Chegou Operações. Abra antes de mexer em qualquer tema, produto, coleção ou página.

## Contexto de uso

### Lojas conhecidas
- **Perfumes árabes, Chile:** loja Shopify "Chile Verificada" / "Llego la Tienda"; domínio antigo chileverificada.com, hoje a coleção está em https://arabesperfume.cl/collections/p-arabes (handle `p-arabes`; antes `perfumes-arabes`). Trabalho de 09–10/10/2026, **pausado pela pessoa** (retomar só se pedir).
  - 5 kits Yara de 3 × 100 ml (59.900 CLP, tags `kit`, `mujer`) e 8 unitários 100 ml EDP (34.900 CLP): Yara, Moi, Tous, Candy, Elixir (`mujer`); Asad, Bourbon, Zanzibar (`hombre`). Yara Rouge trocado por Yara Elixir em todos os kits. Perfumes **confirmados como originais** pela pessoa (selo "Originales Lattafa"). Notas olfativas só de fonte oficial (lattafa.com, lattafa-usa.com, Fragrantica), com fonte citada.
  - Fornecedor Dropi dos Lattafa: **82275**. Unitários ainda sem venda; falta confirmar se 82275 vende avulsos.
  - Coleção smart por tag `perfumes-arabes`, ordem **manual** desde 10/10 (kits primeiro, depois unitários alternando mulher/homem; produto novo com a tag entra no fim; backup em `COLECAO-PERFUMES\v3-ordem\`).
  - Carrinho com upsell do mesmo fornecedor, raspadinha "+1 perfume a mitad de precio" (reseta a cada kit), desconto automático BXGY "Black Friday +1 perfume 50%" (1 por pedido), Black Friday com interruptor `bf_activo`.
  - Temas: publicado "BLACK FRIDAY v2 - carrinho"; v3 pronta como rascunho `167236436224` aguardando a pessoa publicar. Seção de vídeo da loja na coleção = `pa-colecao-video` (levar junto ao criar tema novo).
  - Pendências: pedido teste #374749 não cancelado (conferir import na Dropi e cancelar); publicar v3; filtros em PT no Search & Discovery; Releasit botão de card "só produto"; em 11/10 todos os 16 produtos apareciam "Agotado" (conferir estoque/"continuar vendendo").
  - Relatórios: `Downloads\KIT1-YARA-PERFUMES\RELATORIO.md` (padrão-mestre de produto), `Downloads\KITS-PERFUMES\BRIEFING.md`, `Downloads\COLECAO-PERFUMES\RELATORIO.md` + `ESTUDO-COLECOES.md` + `tema\v2\`, `Downloads\CARRINHO-LOJA\RELATORIO.md`, `Downloads\BLACKFRIDAY-TEMA\RELATORIO.md`. Handoff para a versão Polônia: `Produtividade com ia/HANDOFF-COLECAO-PERFUMES-ARABES-PL.md`.
- **Pellorini (relógios):** marca da pessoa sobre os best sellers da essiora.com; domínio principal pellorini.com (11/10/2026). Decisões: devolução real de 90 dias, venda/envio para o mundo todo. A pessoa tem as duas marcas (Pelvini e Pellorini). Top 5 vendas: Vittorio, Dominante, Milano, Opulent, Maretti. 85 fotos rebrandeadas e trocadas na loja; avaliações restauradas no tema "garantia 2 anos". Vários temas-cópia aguardando a pessoa publicar. Detalhes em `projetos/`.

### Dropi e Chegou Operações
- **Dropi:** plataforma de fulfillment COD. Produto novo na Shopify precisa ser **vinculado no app Dropi**, senão a venda não vira pedido. Pedido não cancelado é importado pela Dropi; cancelado em menos de 1 h, não.
- **Chegou Operações** (conector `chegou-operacoes` / Dropi no claude.ai): sistema do dia a dia das frentes Drop e X1. Leitura de dados **somente leitura**, com o mesmo alcance do Chat IA do sistema; a única escrita são as **páginas livres** (HTML dentro do Operações), para quem tem a chave de edição. Ex.: calculadoras de margem e efetividade (ver [14-unit-economics-cod.md](14-unit-economics-cod.md)).

### Limitações do conector Shopify (medidas)
- **Não grava no tema publicado e não publica tema.**
- Mutations pedem confirmação da pessoa; subagentes às vezes são bloqueados ao criar desconto ou pedido.
- `orderCreate` (pedido teste) foi bloqueado pelo sistema de segurança.
- `templates/product.json` é usado por todos os produtos.
- Upload staged: o tamanho do arquivo fica travado; re-render exige novo staged upload.
- O conector pode estar apontando para outra loja (em 11/10/2026 estava na Pellorini).

## Lógica de uso

### Regras fixas
1. **Escopo só o pedido.** Mexa apenas nos produtos/páginas que a pessoa pediu. No briefing de agente de loja, escreva o escopo explícito (quais produtos/páginas) e proíba estender. Ideia de expansão → proponha, não execute.
2. **Avaliações sempre visíveis.** Nunca desative seção de review, estrelas, "X reviews", "Based on N orders". Ao duplicar/limpar tema, compare com o original e preserve. Dúvida de compliance sobre review → pergunte.
3. **Nunca invente:** preço na imagem, depoimento, "envío gratis" não confirmado, "100% originales" sem confirmação, notas olfativas fora da fonte oficial.
4. **Compliance → perguntar** (ex.: raspadinha "Fuiste seleccionado" tem risco de prática enganosa na UE).
5. **Vencedores primeiro** ao escolher produtos para página, criativo ou subida.

### Fluxo de edição de tema
1. `get-shop-info` para conferir **qual loja** o conector está acessando. Se for a errada, peça à pessoa para trocar.
2. `themeDuplicate` → grave na cópia → teste com `?preview_theme_id=<id>` → **a pessoa clica em Publicar**. Depois de publicar, a cópia vira o tema ao vivo; a próxima edição exige duplicar de novo.
3. Confira logo no começo se alguma seção está desligada no template (`"disabled": true`); no Chile a grade de produtos estava desligada e toda coleção aparecia vazia.
4. Template próprio por categoria (ex.: `collection.perfumes-arabes.json`) para não mexer nos globais. Para mostrar algo só numa categoria na página de produto, use uma seção no `footer-group.json` com filtro por coleção.
5. Depois de publicar: mande a **URL exata e onde rolar** e confira no ar com Playwright (prints 390 px e 1440 px).

### Página de produto (padrão perfumes)
- Galeria 1:1: hero do kit com o nome sob cada frasco + selos; 1 foto por frasco com ingredientes das notas.
- Descrição: blocos em imagem 9:16 (gancho+notas, define tu estilo, hero, "qué incluye") + imagem de garantia. Sem texto corrido.
- Imagens no Flora com Nano Banana 2 (`i2i-gemini-3.1-flash-image`, US$ 0,072 em 1K, US$ 0,108 em 2K); vários frascos com `is2i-…` e várias referências; **sempre a foto real do frasco como referência**; confira cada imagem em tamanho cheio (erros comuns: medalhão errado, texto inventado no corpo, rótulo trocado). Custo: ~US$ 0,60–0,80 por kit, ~US$ 0,50 por unitário.
- O Gemini reescreve texto pequeno (mostrador de relógio: data, marca, numerais) mesmo pedindo para não mexer: cole a região original de volta, sem regerar.
- Publicação ACTIVE nos canais Loja virtual, Ponto de venda e Google & YouTube. **Vincule no app Dropi.**

### Coleção mobile-first (o que funcionou)
Produto já na 1ª tela do celular; nada de descrição no topo (SEO recolhido com "Ver más" no fim); faixa fina com H1 e 3 selos; barra fixa "Filtrar · Ordenar" + chips com rolagem horizontal filtrando por tag; card 1:1, nome 13–14 px, preço 16–18 px; 2 colunas no celular, 4 no desktop. Resultado no Chile: 1º produto a 24% da tela (antes 107%).

### Releasit (pagamento na entrega)
- Grava estilo inline com `!important`: um script do tema reaplica o estilo só na grade; o clique continua sendo do app.
- Modo carrinho desligado (gaveta usa `_rsi.form.mode='normalCart'; _rsi.form.open()`); botão da página de produto esvazia o carrinho (`addMode: product-only`); botão dos cards manda o carrinho inteiro.
- O app mostra preço cheio por linha e só desconta no resumo: script do tema reescreve a linha com preço riscado + com desconto.

### Carrinho/upsell por fornecedor
- Só funciona em produtos com as tags `perfumes-arabes` **e** `forn-<id do fornecedor Dropi>`. Trava impede misturar fornecedores.
- Em outro país sem Dropi, a trava e a tag `forn-` precisam de outra regra ou ficam desligadas.

### Clonar design de loja (skill `clonar-loja-ecommerce`)
1. Parâmetros: URL de referência (obrigatória), escopo, plataforma/tema, **modelo de venda**, país/idioma/moeda, contexto.
   - Pagamento na entrega: **não construa nada que dependa do checkout padrão** (upsell de checkout, order bump, one-click).
   - Venda por conversa: o botão leva ao canal, não ao carrinho.
2. Capturas de página inteira **desktop e mobile** (o mobile é o passo mais pulado).
3. Duplique o tema ativo para rascunho antes de qualquer alteração.
4. Seções separadas (um arquivo cada), tudo editável por schema/settings, responsivo, sem app pago, sem copiar texto, logo, foto, fonte ou nome de marca de terceiro.
5. Avise antes que a 1ª rodada pode não sair parecida e o que não transfere (avaliações de app, vídeo embutido, fontes licenciadas, seções de app pago, fotos de produto).
6. Se não ficar parecido: aponte a diferença específica → reenvie a captura → quebre em blocos → congele o que deu certo.
7. Peça a lista do que não foi possível reproduzir. Preço validado pela conta do negócio (no COD, [14-unit-economics-cod.md](14-unit-economics-cod.md)), nunca por fórmula de tutorial.

### Replicar loja/página para outro país (ex.: Polônia)
Checklist de abertura numa mensagem só: loja/domínio/tema (conector nela); idioma e moeda; oferta e preços na moeda local (não inventar); app de COD e transportadora; prazo real; fornecedor/logística (existe Dropi?); garantia/devolução local (UE: direito de desistência de 14 dias); compliance local; data e mecânica de Black Friday. Ordem: checklist → estudo das grandes lojas do país no celular → duplicar tema → produtos (traduzir só os textos das imagens existentes com Nano Banana 2: "lista exata de texto original → novo, nada mais muda") → coleção + seções traduzidas → carrinho/upsell só com fornecedor único e COD compatível → prints → a pessoa publica. Skills úteis: `replicar-loja-ecommerce`, `clonar-pagina-entre-paises`.

### Painel
Registre as etapas em `painel/painel.py` (`etapa|img|custo|link|fim|pedido`), com `link` para o rascunho/preview do tema.

### Lacunas
- Lojas das outras frentes (Infoproduto: páginas de VSL/quiz; X1: páginas de apoio): nenhuma nas fontes lidas. **Precisa de revisão manual.**
- Detalhes da loja Polônia (loja, moeda, fornecedor, COD): ainda não definidos. **Precisa de revisão manual.**

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [14-unit-economics-cod.md](14-unit-economics-cod.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
