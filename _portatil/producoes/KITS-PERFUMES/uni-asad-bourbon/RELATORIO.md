# Unitário Lattafa Asad Bourbon 100ml EDP (Chile) — uni-asad-bourbon

Data: 09/10/2026
- **Produto Shopify:** `gid://shopify/Product/10212597137664`, status **RASCUNHO (DRAFT)**, preço 0, sem canais.
- **Admin:** https://admin.shopify.com/store/13cc83-26/products/10212597137664
- **Canvas Flora** (compartilhado com o Asad Zanzibar): https://app.flora.ai/projects/ns7fzf64sbdvc89qnh2n4vty2s8fz8tt

## Dados do produto
| Campo | Valor |
|---|---|
| Título | Perfume Árabe Lattafa Asad Bourbon 100ml EDP Original |
| Handle | `perfume-arabe-lattafa-asad-bourbon-100ml-edp-original` |
| Vendor / tipo | Lattafa / Perfumes |
| Tags | perfumes-arabes, lattafa, hombre, unitario, asad |
| SKU | `LAT-ASAD-BOURBON-100` (sem controle de estoque, DENY, requer envio, como no Kit 1) |

## Referências reais (fidelidade do frasco)
Foram usadas as fotos oficiais do site da Lattafa (https://lattafa.com/product/asad-bourbon/):
- `Asad-Bourbon-Bottle-scaled.jpg`, só o frasco (1214x2560), salva como `_ref_oficial_frasco.jpg`;
- `Asad-Bourbon-scaled.jpg`, frasco e caixa (2560x2426), salva como `_ref_oficial_frasco-caixa.jpg`.

As duas foram enviadas ao Flora antes de gerar as imagens.

## Notas olfativas (oficiais)
- **Fonte 1:** página oficial da Lattafa: Top: Pink Pepper, Lavender, Mirabelle Plum · Middle: Cacao, Davana, Nutmeg · Base: Vetiver, Vanilla Bourbon, Amber.
- **Fonte 2:** o Fragrantica (https://www.fragrantica.com/perfume/Lattafa-Perfumes/Asad-Bourbon-101124.html) dá as mesmas notas.
- **Em espanhol:**
  - Salida: pimienta rosa, lavanda y ciruela mirabel.
  - Corazón: cacao, davana y nuez moscada.
  - Fondo: vetiver, vainilla bourbon y ámbar.

## Imagens
| # | Arquivo | Onde | Formato | Textos |
|---|---|---|---|---|
| 01 | 01_galeria_hero.png | Galeria 1 | 1:1 2048 | ASAD BOURBON / PERFUME ÁRABE LATTAFA / etiqueta ASAD BOURBON / 100 ml EDP · Pagas al recibir · Garantía 90 días · Originales Lattafa |
| 02 | 02_galeria_notas.png | Galeria 2 | 1:1 1024 | sem texto; ingredientes: pimienta rosa, lavanda, ciruelas mirabel, cacao, nuez moscada, vainilla, ámbar, vetiver |
| 03 | 03_galeria_lifestyle.png | Galeria 3 | 1:1 1024 | sem texto; homem em ambiente quente (poltrona, lareira, livros) |
| 04 | 04_descricao_bloco1_notas.png | Descrição 1 | 9:16 768x1376 | UN AROMA QUE DEJA HUELLA. / Cálido, especiado y dulce. Perfume árabe para hombre. / NOTAS OLFATIVAS / SALIDA, CORAZÓN, FONDO (notas oficiais) / 100 ML EDP · PAGAS AL RECIBIR · GARANTÍA 90 DÍAS |
| 05 | 05_descricao_bloco2_como-usar.png | Descrição 2 | 9:16 | CÓMO USARLO: 2 a 3 atomizaciones en cuello y muñecas / Sobre la piel limpia e hidratada / No frotes: deja que el aroma se asiente · PARA QUIÉN ES: Para el hombre que prefiere aromas cálidos y especiados. Ideal para la tarde, la noche y ocasiones especiales. |
| 06 | 06_descricao_bloco3_que-incluye.png | Descrição 3 | 9:16 | QUÉ INCLUYE: 1 perfume Lattafa Asad Bourbon / Eau de Parfum de 100 ml / Original Lattafa · EL TOQUE FINAL DE TU ESTILO. · Pagas al recibir en tu casa · Garantía de 90 días · etiqueta ASAD BOURBON |
| — | garantia-90-generica.jpg (já estava em Files) | Descrição 4 | 720x1280 | a mesma imagem genérica do Kit 1 |

- **Shopify:** galeria com 01→03 e alt em espanhol.
- **Files:** `uni-asad-bourbon-04-bloco1-notas.jpg`, `-05-bloco2-como-usar.jpg` e `-06-bloco3-que-incluye.jpg`.
- **Descrição:** só as imagens (blocos 1–3 + a garantia genérica), no mesmo HTML do Kit 1.
- **Sem:** preço, depoimentos, "envío gratis" e afirmações de duração ou fixação.

## QA em tamanho cheio (contra a foto oficial)
- **01 hero:** frasco e caixa fiéis.
  - Frasco: marrom fosco, anéis bronze, faixa cruzada com medalhão do leão, caligrafia dourada, "ASAD / BOURBON / Lattafa".
  - Caixa: medalhão gravado, "EAU DE PARFUM 100ml", BOURBON, ASAD, Lattafa.
  - Texto em espanhol correto. Aprovado.
- **02:** frasco fiel e ingredientes coerentes com as notas. A davana não aparece (não dá para representar visualmente). Aprovado.
- **03 lifestyle:** o frasco está fiel, mas no rótulo minúsculo o texto saiu ilegível.
  - Corrigi localmente, sem custo: apaguei o texto e reescrevi "BOURBON" e "Lattafa" no rótulo com PIL.
  - O original sem correção está em `_versoes-anteriores/`.
  - No fundo aparecem decanters de vidro com bebida (cena de lareira). Se preferir evitar álcool, troque essa imagem.
- **04–06:** frascos fiéis, sem texto embaralhado, acentos corretos (Cálido, CORAZÓN, ámbar, CÓMO, QUIÉN, muñecas, Garantía, días). Aprovados na 1ª tentativa.
- **Pessoas:** os homens das imagens 03 e 05 foram gerados por IA, como no Kit 1.

## Custo real (charged_cost do Flora, Nano Banana 2)
| Item | US$ |
|---|---|
| 01 hero 2K | 0,108 |
| 02, 03 galeria 1K (2 × 0,072) | 0,144 |
| 04, 05, 06 descrição 1K (3 × 0,072) | 0,216 |
| **Total** | **0,468** (teto: 0,60) |

Nenhuma imagem foi refeita no Flora.

## Pendências (para o agente principal e a pessoa)
1. Definir o preço (está em 0) e publicar, incluindo os canais.
2. Os blocos da descrição estão em 1K (768x1376), e não em 2K como os do Kit 1. Foi para caber no teto. Ficam nítidos no celular.
3. Confirmar se a imagem genérica de garantia ("Envío a todo Chile", "WhatsApp") vale para este produto. É a mesma do Kit 1.
4. "Para quién es" ("tarde, noche, ocasiones especiales") é uma recomendação de uso, não um dado oficial. Revisar se quiser.
5. A tag extra `asad` foi adicionada para agrupar a linha Asad. Remova se não quiser.
