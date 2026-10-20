# Perfumes Lattafa na chileverificada.com (loja, coleção, Black Friday, carrinho)

> Trabalho de loja (não de criativo) dos perfumes árabes Lattafa no Chile: produtos, coleção, tema Black Friday e carrinho com raspadinha. Pausado pela pessoa. Abra ao retomar a loja de perfumes.

## Contexto de uso
- **Frente:** COD Chile (loja Shopify chileverificada.com). **Feito em 09/10/2026, ajustes em 10/10/2026; pausado pela pessoa** (retomar só se ela pedir).
- **Produtos no ar:** Kits 1–5 (CLP 59.900) e unitários Yara, Moi, Tous, Candy, Elixir, Asad, Bourbon, Zanzibar (CLP 34.900). Yara Rouge foi trocado por Elixir.
- **Coleção:** smart por tag `perfumes-arabes`; handle `p-arabes` (template suffix `perfumes-arabes`); ordem **manual** desde 10/10 (kits primeiro: Pack Hombre, Kit 1 Yara+Moi+Elixir, Pack Mujer, demais kits Yara; depois unitários alternando mulher/homem). Produto novo com a tag entra no fim. Backup em `COLECAO-PERFUMES\v3-ordem\`.
- **Temas:** publicado "BLACK FRIDAY v2 - carrinho"; **v3** (preço com desconto no Releasit, texto "1 por pedido", raspadinha reseta, seção de vídeo recolocada) pronta como rascunho `167236436224`, aguardando a pessoa publicar.
- **Desconto automático:** "Black Friday +1 perfume 50%" (comprou kit → 1 unitário com 50 %, 1 por pedido). Carrinho/raspadinha só para produtos com as tags `perfumes-arabes` + `forn-82275`.
- **Fornecedor Dropi dos Lattafa:** 82275 (packs). Unitários ainda sem venda. Mapa produto → fornecedor em `Downloads\CARRINHO-LOJA\MAPA-FORNECEDORES.md`.
- **Vídeo da loja (avatar)** na coleção = seção `pa-colecao-video` (nasceu no tema "+ video loja"); sumiu no v2 publicado porque ele foi copiado antes; recolocado no v3 em 10/10.
- **Pastas e relatórios:** `Downloads\KIT1-YARA-PERFUMES\RELATORIO.md` (modelo do Kit 1), `Downloads\KITS-PERFUMES\<id>\RELATORIO.md` + `BRIEFING.md` (kits 2–5 e unitários), `Downloads\CARRINHO-LOJA\RELATORIO.md`, `Downloads\COLECAO-PERFUMES\RELATORIO.md` + `ESTUDO-COLECOES.md`, `Downloads\BLACKFRIDAY-TEMA\RELATORIO.md` + `ESTUDO-BANNERS.md`.
- **Pendências:**
  - pedido teste #374749 (Pack Hombre + Zanzibar, 77.350) não cancelado: conferir o import na Dropi e cancelar;
  - publicar o v3;
  - vincular cada produto novo no app Dropi; confirmar se o 82275 vende avulsos;
  - filtros em PT no Search & Discovery;
  - Releasit: botão de card "só produto".

## Lógica de uso
- **Produto novo:** copiar o padrão do Kit 1 (galeria 1:1: hero do kit com nome sob cada frasco e selos + 1 foto por frasco; descrição com 4 blocos 9:16 + imagem de garantia de 90 dias). Imagens no Flora (projeto do Kit 1 `prj_ns72zge7hvbtq4mb73es6nkgm98fyfzn`, Nano Banana 2). **Nunca inventar** notas olfativas, ml, concentração, avaliações, preço antigo ou estoque.
- **Tema:** o conector bloqueia gravar no tema publicado → `themeDuplicate`, gravar na cópia, a pessoa publica. Ao criar tema novo a partir de outro, **levar junto a seção `pa-colecao-video`** (e `pa-produto-video`).
- **Black Friday:** tudo num snippet (`snippets/bf-black-friday.liquid` com interruptor `bf_activo`) chamado pelo `header-group.json`, sem mexer em templates de produto.
- **Carrinho COD:** o Releasit em `product-only` esvazia o carrinho; o carrinho próprio (`snippets/cv-carrito.liquid`) + Releasit em modo carrinho mantém todas as linhas. O checkout do Shopify não tem meio de pagamento ativo — todo fluxo tem que terminar no Releasit.
- **Coleção vazia no tema publicado:** a seção "Grade de produtos" do `collection.json` estava desativada; correção manual no editor (Personalizar → Coleções → mostrar a seção → Salvar).
- **Escopo:** mexer só nas páginas pedidas; expansão é proposta, nunca execução. Avaliações/estrelas sempre visíveis.
- **Se a pessoa pedir para retomar:** começar pelas pendências acima (cancelar o pedido teste e publicar o v3).

## Relacionados
- [yara-bf-chile.md](yara-bf-chile.md) (criativos do Kit 3 Yara)
- [../04-fluxo-producao-criativos.md](../04-fluxo-producao-criativos.md)
