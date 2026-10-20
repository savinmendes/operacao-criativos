# Unitário Lattafa Asad Zanzibar 100ml EDP (Chile) — uni-asad-zanzibar

Data: 09/10/2026
- **Produto Shopify:** `gid://shopify/Product/10212597170432`
- **Status:** **RASCUNHO (DRAFT)**, preço 0, sem canais.
- **Admin:** https://admin.shopify.com/store/13cc83-26/products/10212597170432
- **Canvas Flora** (compartilhado com o Asad Bourbon): https://app.flora.ai/projects/ns7fzf64sbdvc89qnh2n4vty2s8fz8tt

## Dados do produto
| Campo | Valor |
|---|---|
| Título | Perfume Árabe Lattafa Asad Zanzibar 100ml EDP Original |
| Handle | `perfume-arabe-lattafa-asad-zanzibar-100ml-edp-original` |
| Vendor / tipo | Lattafa / Perfumes |
| Tags | perfumes-arabes, lattafa, hombre, unitario, asad |
| SKU | `LAT-ASAD-ZANZIBAR-100` (sem controle de estoque, DENY, requer envio, como no Kit 1) |

## Referências reais (fidelidade do frasco)
- As fotos vieram do site oficial da Lattafa (https://lattafa.com/product/asad-zanzibar/), em 2560x2560: `1-95.jpg` (caixa e frasco), `2-95.jpg` (frasco) e `3-95.jpg` (caixa).
- Cortei a margem branca. Os arquivos ficaram como `_ref_oficial_frasco.jpg` e `_ref_oficial_frasco-caixa.jpg`.
- As duas foram enviadas ao Flora antes de gerar.

## Notas olfativas (oficiais)
- **Lattafa USA (loja oficial):**
  - Top: Lavender, Black Pepper.
  - Middle: Coconut Water, Iris, Salt.
  - Base: Vanilla, Incense.
- **Fragrantica:** as notas são as mesmas (https://www.fragrantica.com/perfume/Lattafa-Perfumes/Asad-Zanzibar-90713.html).
- **lattafa.com:** escreve "Black Pepper & Sea lavender / Salty Coconut Water & Iris / Vanilla & Incense". Usei "lavanda", como nas outras duas fontes.
- **Em espanhol:**
  - Salida: pimienta negra y lavanda.
  - Corazón: agua de coco, iris y sal.
  - Fondo: vainilla e incienso.

## Imagens
| # | Arquivo | Onde | Formato | Textos |
|---|---|---|---|---|
| 01 | 01_galeria_hero.png | Galeria 1 | 1:1 2048 | ASAD ZANZIBAR / PERFUME ÁRABE LATTAFA / etiqueta ASAD ZANZIBAR / 100 ml EDP · Pagas al recibir · Garantía 90 días · Originales Lattafa |
| 02 | 02_galeria_notas.png | Galeria 2 | 1:1 1024 | sem texto; ingredientes: pimienta negra, lavanda, coco, iris, sal marina, vainilla, incienso (resina e varetas) |
| 03 | 03_galeria_lifestyle.png | Galeria 3 | 1:1 1024 | sem texto; homem de linho branco num terraço à beira-mar |
| 04 | 04_descricao_bloco1_notas.png | Descrição 1 | 9:16 768x1376 | FRESCURA CON CARÁCTER. / Fresco, salino y especiado. Perfume árabe para hombre. / NOTAS OLFATIVAS / SALIDA, CORAZÓN, FONDO (notas oficiais) / 100 ML EDP · PAGAS AL RECIBIR · 90 DÍAS GARANTÍA 90 DÍAS |
| 05 | 05_descricao_bloco2_como-usar.png | Descrição 2 | 9:16 | CÓMO USARLO (3 itens iguais aos do Bourbon) · PARA QUIÉN ES: Para el hombre que busca un aroma fresco y diferente. Ideal para el día, el calor y el uso diario. |
| 06 | 06_descricao_bloco3_que-incluye.png | Descrição 3 | 9:16 | QUÉ INCLUYE: 1 perfume Lattafa Asad Zanzibar / Eau de Parfum de 100 ml / Original Lattafa · EL TOQUE FINAL DE TU ESTILO. · Pagas al recibir en tu casa · Garantía de 90 días · etiqueta ASAD ZANZIBAR |
| — | garantia-90-generica.jpg (já estava em Files) | Descrição 4 | 720x1280 | a mesma imagem genérica do Kit 1 |

- **Shopify:**
  - Galeria: imagens 01→03, com alt em espanhol.
  - Files: `uni-asad-zanzibar-04/05/06-*.jpg`.
  - Descrição: só imagens, como no Kit 1.
- **Não usado:** preço, depoimentos, "envío gratis", duração/fixação.

## QA em tamanho cheio (contra a foto oficial)
- **01 hero:** frasco fiel (azul royal, anéis e faixa prata, medalhão do leão, caligrafia branca, "ASAD / ZANZIBAR / Lattafa").
  - A caixa também está fiel (azul, medalhão prata, ASAD, Lattafa).
  - Diferença menor: na caixa real, acima do medalhão, há uma linha pequena ("EAU DE PARFUM… ZANZIBAR") que não aparece na gerada.
  - Aprovado.
- **02:** frasco fiel. Aprovado. Detalhe: há uma colher de metal dentro do coco.
- **03 lifestyle:** precisou de correção.
  - **1ª versão** (`_versoes-anteriores/03_galeria_lifestyle_v1.png`): os anéis saíram dourados e o rótulo, ilegível. **Refeita 1 vez** (US$ 0,072).
  - **2ª versão:** os anéis ficaram prata (corretos), mas o rótulo saiu "RANSYDAR". Corrigi localmente, sem custo, reescrevendo "ZANZIBAR" e "Lattafa" com PIL. O original sem correção está em `_versoes-anteriores/`.
- **04–06:** frascos fiéis e acentos corretos. Aprovados.
  - No 06, a caixa mostra "ZANZIBAR" no topo, como a caixa real.
  - No rodapé do 04, o selo da garantia está redundante ("90 DÍAS" + "GARANTÍA 90 DÍAS") e em letra pequena. É aceitável, mas pode ser ajustado.
- **Pessoas:** os homens das imagens 03 e 05 foram gerados por IA.

## Custo real (charged_cost do Flora, Nano Banana 2)
| Item | US$ |
|---|---|
| 01 hero 2K | 0,108 |
| 02, 03 galeria 1K (2 × 0,072) | 0,144 |
| 03 refeita 1K | 0,072 |
| 04, 05, 06 descrição 1K (3 × 0,072) | 0,216 |
| **Total** | **0,540** (teto: 0,60) |

## Pendências
1. Preço (está em 0) e publicação/canais.
2. Os blocos da descrição estão em 1K (768x1376) por causa do teto.
3. Confirmar se a imagem genérica de garantia vale também para este produto.
4. "Para quién es" (día, calor, uso diario) é uma recomendação de uso, não um dado oficial.
5. Existe uma "Limited Edition" do Asad Zanzibar (2025), com outro visual. Este produto é o **Asad Zanzibar regular, de frasco azul**: confirmar com o fornecedor que é esta versão.
