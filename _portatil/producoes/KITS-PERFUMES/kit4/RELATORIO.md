# Kit 4: Yara + Yara Moi + Yara Candy (Chile, mujer)

Data: 09/10/2026
- **Produto Shopify:** `gid://shopify/Product/10212596351232`. Status: **DRAFT**, preço 0, sem canais.
- **Admin:** https://admin.shopify.com/store/13cc83-26/products/10212596351232
- **Handle:** `kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-candy-lattafa-100ml`
- **Título:** Kit 3 Perfumes Árabes Mujer | Yara + Yara Moi + Yara Candy Lattafa 100ml
- **Vendor / tipo:** Lattafa / Perfumes.
- **Tags:** perfumes-arabes, lattafa, mujer, kit, yara.
- **SKU:** `KIT4-YARA-MOI-CANDY` (inventário não rastreado e política DENY, igual ao Kit 1).
- **Canvas Flora:** https://app.flora.ai/projects/ns7an03wxvvs4j4v2wgkphpt7d8fy6cw

## Arquivos
| # | Arquivo | Onde | Origem |
|---|---|---|---|
| 01 | 01_galeria_kit-3-perfumes.png | Galeria 1 (2048²) | Nano Banana 2 (2K) com as 3 refs reais. Textos: KIT 3 PERFUMES / ÁRABES LATTAFA / etiquetas YARA, YARA MOI, YARA CANDY / 100 ml cada uno · Pagas al recibir · Garantía 90 días · Originales Lattafa |
| 02 | 02_galeria_yara.png | Galeria 2 | Reaproveitada do Kit 1, sem custo |
| 03 | 03_galeria_yara-moi.png | Galeria 3 | Reaproveitada do Kit 1 (v2), sem custo |
| 04 | 04_galeria_yara-candy.png | Galeria 4 (1024²) | Nano Banana 2 (1K) com a foto oficial do Candy. Sem texto. Cena: frutilla, grosella negra, mandarina verde, gardenia, vainilla |
| 05 | 05_descricao_bloco1_tres-aromas.jpg | Descrição 1 | Nano Banana 2 (2K). Cartões com as notas: Yara / Yara Moi (iguais ao Kit 1) / Yara Candy |
| 06 | 06_descricao_bloco2_define-tu-estilo.jpg | Descrição 2 | Nano Banana 2 (2K). DULCE & FRUTAL: "Yara suave y Yara Candy llena de alegría." / FLORAL & ELEGANTE: Moi |
| 07 | 07_descricao_bloco3_kit-hero.jpg | Descrição 3 | Nano Banana 2 (2K). 3 PERFUMES ÁRABES LATTAFA / Yara · Yara Moi · Yara Candy / 4 selos |
| 08 | 08_descricao_bloco4_kit-garantia.jpg | Descrição 4 | Nano Banana 2 (2K). QUÉ INCLUYE TU KIT (3 perfumes Lattafa Eau de Parfum / 100 ml cada frasco / os 3 nomes / 100% originales) / EL TOQUE FINAL DE TU ESTILO |
| 09 | 09_descricao_bloco5_garantia-90-generica.jpg | Descrição 5 | Mesmo arquivo de garantia do Kit 1 (`garantia-90-generica.jpg`, já no Shopify Files) |

Shopify Files novos: `kit4-yara-candy-bloco1-tres-aromas.jpg`, `kit4-yara-candy-bloco2-define-tu-estilo.jpg`, `kit4-yara-candy-bloco3-kit.jpg` e `kit4-yara-candy-bloco4-que-incluye.jpg`.

A descrição tem só as imagens (blocos 1–4 e a garantia), como no Kit 1.

## Fontes das notas olfativas
- **Yara e Yara Moi:** mesmo texto da descrição do Kit 1.
  - Yara: orquídea, mandarina, frutas tropicales, vainilla y almizcle.
  - Yara Moi: jazmín, durazno, ámbar y sándalo.
- **Yara Candy:** página oficial do distribuidor Lattafa USA (https://www.lattafa-usa.com/products/yara-candy). O Fragrantica (https://www.fragrantica.com/perfume/Lattafa-Perfumes/Yara-Candy-95752.html) traz as mesmas notas.
  - Saída: Black Currant, Green Tangerine.
  - Coração: Strawberry Fizz Candy, Gardenia.
  - Fundo: Vanilla, Musk, Amber, Sandalwood.
  - Na imagem foi usado um resumo: "Mandarina verde, grosella negra, gardenia, vainilla y almizcle." Ficaram de fora o "caramelo de frutilla", o ámbar e o sándalo, por falta de espaço. As notas que aparecem são todas oficiais.
- **Referência do frasco Candy:** foto oficial em `cdn.shopify.com` da lattafa-usa, 1500×1500, subida no Flora.
- **Referências do Yara e do Moi:** as mesmas fotos reais do projeto Flora do Kit 1.

## Custo real (charged_cost do Flora)
| Item | US$ |
|---|---|
| 01 hero 2K | 0,108 |
| 04 Candy 1K | 0,072 |
| 05, 06, 07, 08 em 2K (4 × 0,108) | 0,432 |
| **Total** | **0,612** (teto: 1,00) |

Nenhuma geração foi refeita. As correções foram feitas localmente, sem custo.

## QA em tamanho cheio
- **01:** os 3 frascos estão fiéis.
  - Yara: rosa claro com anéis prateados.
  - Moi: branco com dourado.
  - Candy: fúcsia com anéis dourados e medalhão rosa "Candy", como na foto oficial.
  - Etiquetas e acentos corretos. Aprovado.
- **04:** fiel à foto oficial (medalhão "Candy", "YARA", "Lattafa"). Aprovado. A mandarina verde parece limão, o que é aceitável.
- **05, 07 e 08:** o modelo escreveu "YARA MOI" no rótulo do frasco branco, mas o frasco real diz só "YARA" (conferido na foto oficial da Lattafa USA). Corrigi localmente com PIL: apaguei o " MOI" e centralizei o "YARA" original, mantendo a mesma fonte. No 08 a correção vale também para o reflexo. Os originais estão em `_versoes-anteriores/`.
- **06:** frascos e textos OK.
- **Textos:** sem preço, sem depoimento e sem "envío gratis" nos blocos novos.

## Pendências e o que conferir
1. **Medalhão do Yara Moi.** A foto oficial atual da Lattafa USA mostra um medalhão branco com "Moi" em script. A foto de referência do Kit 1, que foi reaproveitada na imagem 03 e usada nas imagens 01, 05 e 08, mostra uma roseta dourada. Pode ser um lote ou versão diferente. O bloco 07 saiu com o "Moi" em script. Vale conferir qual versão o fornecedor entrega e deixar tudo igual.
2. **Selo "Originales Lattafa" no bloco 07.** O selo traz um desenho de caligrafia que lembra o logo Lattafa, gerado por IA. Conferir se está aceitável.
3. **Imagem de garantia genérica (09).** Diz "Envío a todo Chile" e cita o WhatsApp. É a mesma do Kit 1.
4. **Preço e publicação:** ficam com o agente principal e a pessoa. O produto continua DRAFT, com preço 0.
5. **Pessoas nas imagens 05 e 06:** são modelos gerados por IA, como no Kit 1.
