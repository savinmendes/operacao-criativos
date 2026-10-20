# Relatório: coleção Perfumes Árabes (chileverificada.com)

Data: 09/10/2026

## 1. Por que a coleção não mostra produtos no tema publicado (e /collections/all também não)

**Causa:** no tema publicado ("shr-co PAGINA v4 (cores teste)"), o arquivo `templates/collection.json` está com a seção **Grade de produtos** (`main-collection-product-grid`) **desativada** (`"disabled": true`). Toda página de coleção usa esse modelo, então aparecem só o título e a descrição, sem nenhum produto. A coleção em si está certa: `/collections/perfumes-arabes/products.json` devolve os 3 produtos ativos.

Pela API não dá para corrigir isso (gravação no tema publicado bloqueada). **A dona precisa fazer o seguinte (1 minuto):**
1. Shopify Admin → Loja virtual → Temas → tema publicado → **Personalizar**.
2. No seletor do topo: **Coleções → Coleção padrão**.
3. Na lista de seções à esquerda, a seção **"Grade de produtos"** aparece apagada. Clique no ícone de olho para **mostrar** a seção e depois em **Salvar**.

Isso corrige `/collections/perfumes-arabes` (que no tema publicado cai no modelo padrão) e também `/collections/all` e todas as outras coleções.

Outra saída: quando a cópia "BLACK FRIDAY - shr-co v4 (rascunho)" for publicada, a coleção já sai com o modelo próprio descrito abaixo.

## 2. O que foi feito

### Estudo
O estudo está em `ESTUDO-COLECOES.md`. Lojas olhadas: Dperfumes, Elite Perfumes, Falabella, Cosmetic.cl e Yauras. A Notino bloqueou o acesso.

### Na Shopify (já está no ar, vale para qualquer tema)
- **Coleção inteligente** "Perfumes Árabes", com handle `perfumes-arabes` e ID `gid://shopify/Collection/492347851008`.
  - Regra: tag igual a `perfumes-arabes`. Produto novo com essa tag entra sozinho quando for publicado.
  - Ordem: Más vendidos.
  - Publicada na Loja virtual.
  - Modelo: `perfumes-arabes`. No tema publicado esse modelo não existe, então ele usa o padrão.
- Descrição em espanhol, SEO title "Perfumes Árabes Originales en Chile | Lattafa, Armaf y Afnan" e meta description.
- Imagem da coleção: banner gerado no Flora (frascos sem rótulo, incenso de oud, sem logos nem texto).
- Tags acrescentadas a 2 produtos que já existiam:
  - `lattafa` (Pack 3x1 Hombre Armaf CDNI + Asad + 9PM): `perfumes-arabes, kit, hombre, lattafa, armaf, afnan`
  - `yara` (Pack 3x1 Mujer Yara + Fakhar Rose + Sabah Al Ward): `perfumes-arabes, kit, mujer, lattafa, yara`

### Produtos na coleção hoje
| Produto | Status |
|---|---|
| Pack 3x1 Perfumes Hombre (Armaf Club de Nuit Intense + Lattafa Asad + Afnan 9PM) | ativo, aparece |
| Pack 3x1 Perfumes Árabes Mujer (Yara + Fakhar Rose + Sabah Al Ward) | ativo, aparece |
| Kit 3 Perfumes Árabes Mujer (Yara + Yara Moi + Yara Elixir) | ativo, aparece |
| Kits 2–5 e os unitários criados pelos outros agentes | rascunho: entram sozinhos quando forem publicados |

**Ficaram de fora:**
- "...cada uno teste": duplicata de teste.
- Kits de colágeno: não são perfume.
- Kits de perfumes de grife (Invictus + 1 Million + Bleu de Chanel; Kit 3 Premium Hombre; One Million + Sauvage): não são árabes. Também não foi criada a coleção ampla "Perfumes", ver pontos abertos.

### No tema cópia (BLACK FRIDAY, ainda não publicado)
Novo arquivo `templates/collection.perfumes-arabes.json`. Nenhum modelo global foi mexido, e `bf-black-friday.liquid` e `header-group.json` não foram tocados. A página tem:
1. **Banner**: imagem da coleção, "LATTAFA · ARMAF · AFNAN", H1, descrição, contagem de produtos e 3 selos verdadeiros:
   - "Perfumes originales": confirmado pela dona.
   - "Paga al recibir": o app de pagamento contra entrega Releasit está ativo.
   - "Despacho gratis a todo Chile": já está escrito na própria loja.
2. **Chips**: Todos · Kits y packs · Unitarios · Mujer · Hombre.
   - Filtram por tag (`/collections/perfumes-arabes/kit` etc.).
   - Cada chip só aparece se algum produto tiver a tag. "Unitarios" vai aparecer quando os unitários forem publicados.
3. **Grade**: 2 colunas no celular e 4 no desktop, foto quadrada, segunda foto ao passar o mouse, compra rápida, filtros e ordenação ("Más vendidos").
4. **Texto SEO curto** no rodapé ("Perfumes árabes originales en Chile", "¿Kit o unitario?", "¿Cómo pago?").

Os arquivos-fonte estão em `tema/`: `hero.liquid`, `seo.liquid` e `collection.perfumes-arabes.json`.

### Verificação
- Prévia do tema cópia (`?preview_theme_id=167232798976`): 3 cards, chips Todos/Kits/Mujer/Hombre. Prints: `preview_desktop.png` e `preview_mobile.png`.
- Tema publicado: título e descrição aparecem, mas 0 cards por causa da seção desativada (item 1). Prints: `live_desktop.png` e `live_mobile.png`.

## 3. Custo
2 imagens Nano Banana 2 em 2K, US$ 0,108 cada: **US$ 0,216** (limite era US$ 1,00). Foi usada a `banner_a.png`; a `banner_b.png` ficou de reserva.

## 4. Pontos abertos
1. **Ativar a seção "Grade de produtos"** no modelo padrão de coleção do tema publicado (passo a passo no item 1).
2. **Rótulos dos filtros em português** ("Disponibilidade", "Preço"). Corrigir no app Search & Discovery → Filtros, renomeando para "Disponibilidad" e "Precio".
   - No mesmo app dá para acrescentar filtros por **Tag** (Mujer/Hombre/Kit/Unitario) e **Marca/Fornecedor**. Hoje o fornecedor dos packs é "Chile", então um filtro de Marca ficaria ruim.
3. **Botão do Releasit no card** ("Pide y Paga al Recibir", verde e grande) ocupa muito espaço no celular. Ele vem do app com estilo inline e não dá para ajustar pelo tema: diminuir ou desligar o botão em páginas de coleção nas configurações do Releasit.
4. **Coleção ampla "Perfumes" (Árabes × Diseñador)**: o estudo recomenda separar assim, mas os kits de grife (Invictus, 1 Million, Bleu de Chanel, Sauvage a CLP 49.900–69.900 por 2–3 frascos) não foram incluídos nem divulgados. A dona precisa confirmar a origem desses produtos antes.
5. Preço comparativo: o Pack Hombre tem compare_at igual ao preço (59.900) e não mostra selo; os demais não têm compare_at. Não foi inventado preço antigo.
6. Estrelas e avaliações não foram ligadas: não há avaliações reais desses produtos.

---

# v2: coleção mobile-first (09/10/2026)

O pedido da dona, depois de ver a página no celular: "tá comendo muita tela, muito texto com fonte simples, botão de compra muito grande e desconexo". A referência dela é a dperfumes.cl. O estudo mobile com dperfumes, Falabella, Notino, Sephora e Ulta está em `ESTUDO-COLECOES.md`, seção "Mobile", com os prints em `ref-mobile/`.

## Resultado medido (celular 390x844)
| | v1 | v2 |
|---|---|---|
| Topo do 1º produto | 899px (107% da tela, só aparecia na 2ª tela) | **205px (24%)**. O 1º card aparece inteiro na primeira tela, com botão |
| Altura do topo (banner + texto) | 779px | 101px de faixa + 51px de barra |
| Rolagem horizontal | sim (a página tinha 397px de largura) | não (390px) |
| Fonte do título | Inter, padrão | Cormorant Garamond 600 (32px no celular, 52px no desktop) |
| Nome no card | centralizado, grande, até 6 linhas | 13,5px, à esquerda: nome em 1 linha e detalhe em cinza em até 2 |
| Preço | grande, centralizado | 16px/700, à esquerda |
| Botão Releasit no card | verde, ~90px de altura, 17,6px, sombra, tremendo, sobrepondo o card | 40px, preto com ícone dourado, 12,5px, sem subtítulo, sem animação, alinhado ao card |
| Texto SEO | 4 blocos abertos, ~700px | fechado em 3 linhas com "Ver más" |

O formulário do Releasit continua abrindo pelo botão do card: o teste clicou e o formulário "Completa tus datos y paga al recibir" abriu. Nenhum pedido foi enviado.

## O que mudou
Tudo fica só no tema cópia `gid://shopify/OnlineStoreTheme/167232798976` e só vale para o modelo `collection.perfumes-arabes`.
- Nenhum arquivo existente do tema foi alterado: nem `bf-black-friday.liquid`, nem `header-group.json`, nem `card-product`, nem os modelos globais.
- A página de produto continua igual: o Releasit segue verde, e nenhum CSS ou fonte da coleção carrega lá.

| Arquivo no tema | O que é |
|---|---|
| `sections/pa-colecao-topo.liquid` (novo) | Faixa do topo e barra fixa, mais o CSS/JS dos cards (detalhes abaixo). Editável no editor do tema: linha das marcas, subtítulo, 3 selos, imagem liga/desliga, botão de filtro liga/desliga |
| `sections/pa-colecao-seo.liquid` (novo) | Texto SEO fechado com "Ver más". Começa pela descrição da coleção, seguida do texto editável |
| `templates/collection.perfumes-arabes.json` | Passou a usar as 2 seções novas no lugar das 2 "Liquid personalizado". A grade ficou com padding de topo 0 |

**A faixa do topo** tem a imagem da coleção com degradê escuro, a linha "Lattafa · Armaf · Afnan", o H1 em Cormorant Garamond e 3 selos com ícone: Originales, Paga al recibir, Envío gratis. O subtítulo de 1 linha aparece só no desktop.

**A barra** junta "Filtrar · Ordenar" com os chips (Todos, Kits y packs, Unitarios, Mujer, Hombre).
- No celular ela fica fixa no topo ao rolar.
- O botão abre a gaveta de filtros do próprio tema. A gaveta também ganhou tipografia nova.

**Os cards da grade:**
- Grade de 2 colunas no celular com gap de 10px, e de 4 no desktop, com largura máxima de 1240px.
- Os cards da mesma linha têm a mesma altura.
- Título "Nome | detalhe" dividido em nome e detalhe só na tela, sem mudar o nome do produto.
- O selo BLACK FRIDAY saiu de cima da foto e virou etiqueta pequena acima do nome.
- Botão do Releasit compacto: o app grava cor e tamanho inline com `!important`, então um script reaplica o estilo só dentro de `#product-grid`.
- Rótulos de filtro corrigidos só na tela: "Disponibilidade" virou "Disponibilidad" e "Preço" virou "Precio".

Fontes locais (mesmo conteúdo gravado no tema): `tema/v2/sections/` e `tema/v2/templates/`.

## Prints (`v2/`)
- Antes:
  - `antes_mobile_fold.png`
  - `antes_mobile_full.png`
  - `antes_desktop_fold.png`
  - `antes_desktop_full.png`
- Depois:
  - `depois_mobile_fold.png`
  - `depois_mobile_scroll.png` (barra fixa)
  - `depois_mobile_full.png`
  - `depois_desktop_fold.png`
  - `depois_desktop_full.png`
- Comparativo: `comparativo_mobile_antes_depois.jpg`
- Testes:
  - `teste_gaveta_filtro.png`
  - `teste_releasit_formulario.png`
  - `produto_mobile_depois.png` (página de produto sem alteração)
- Iterações intermediárias: `v2/iteracoes/`

## Como desfazer
1. Gravar no tema cópia o conteúdo de `backup-v2/templates__collection.perfumes-arabes.json` como `templates/collection.perfumes-arabes.json`, pela API `themeFilesUpsert` ou pelo editor de código do tema. Isso volta exatamente à v1.
2. Opcional: apagar `sections/pa-colecao-topo.liquid` e `sections/pa-colecao-seo.liquid`. Sem o modelo usando, elas não têm efeito nenhum.

O backup da v1 (template, `hero.liquid` e `seo.liquid`) está em `backup-v2/`, com uma nota em `LEIA.txt`.

## Pontos abertos (v2)
1. **Publicar o tema cópia** depois da aprovação. O tema publicado continua com a grade desligada (item 1 da v1).
2. **Rótulos dos filtros no app Search & Discovery:** a página corrige na tela, mas o certo é renomear no app para "Disponibilidad" e "Precio". Assim vale para todas as coleções.
3. **Ordem de compra no card:** o card mantém o botão do Releasit, que abre o formulário de pagamento contra entrega.
   - 3 das 5 lojas grandes não usam botão no card. Se a dona preferir, dá para trocar por "Ver producto" ou tirar o botão, mudando só o CSS da seção.
   - Se o Releasit mudar o código do botão, ele volta ao estilo do app, mas continua funcionando.
4. **O tema cópia não tem cabeçalho com logo e menu**, só a faixa de anúncios da Black Friday. Isso vale para a loja inteira, não só para a coleção.
5. **A página de produto mostra "4.9 (193 opiniones)".** Não faz parte desta tarefa e não foi verificado, mas vale a dona confirmar se as avaliações são reais.
6. A coleção já tem **15 produtos ativos** (eram 3 na v1): os unitários e kits publicados depois entraram sozinhos pela tag.
