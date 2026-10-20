# Estudo rápido: como as maiores lojas montam a coleção de perfumes árabes

Data: 09/10/2026. Loja alvo: chileverificada.com (Shopify, Chile, COD).
Método: leitura do HTML das páginas de coleção (curl) e WebFetch. Notino.es bloqueou o acesso (403) e ficou de fora; Sephora não vende árabes no Chile e também ficou de fora.

## Lojas olhadas

| Loja | Página | Plataforma |
|---|---|---|
| Dperfumes (referência da dona) | https://dperfumes.cl/?s=arabe&post_type=product | WooCommerce |
| Elite Perfumes | https://www.eliteperfumes.cl/collections/perfumes-arabes | Shopify |
| Falabella | https://www.falabella.com/falabella-cl/collection/perfumes-arabes | marketplace |
| Cosmetic.cl | https://cosmetic.cl/collections/perfumes-arabes | Shopify |
| Yauras | https://yauras.cl/collections/perfumes-arabes | Shopify |

## O que se repete (padrão do mercado)

### Cabeçalho
- Título H1 "Perfumes Árabes" + 1 linha de texto citando as marcas (Lattafa, Armaf, Maison Alhambra...) e "hombre, mujer y unisex" (Elite, Yauras).
- Contador de produtos ao lado do título (Elite: "(302 productos)"; Falabella: "2849 resultados").
- Falabella põe um carrossel de logos das marcas logo abaixo do título (French Avenue, Armaf, Lattafa, Rasasi, Afnan...).
- Banner com foto não é a regra: Elite, Cosmetic e Yauras vão direto ao grid. O que aparece no topo é a faixa de promoção da loja (Dperfumes: "Cyber Week hasta 70% OFF", "6 cuotas sin interés", "envío gratis desde $125.000").

### Card do produto (o mesmo nas 5)
1. Selo de desconto no canto da foto: "-37%" (Dperfumes), "43% OFF" (Elite), "AHORRA UN 72%" (Cosmetic), "Ahorre 61%" (Yauras).
2. Marca acima ou abaixo do nome (Lattafa, Armaf, Afnan).
3. Nome com concentração e ml: "Khamrah Eau de Parfum 100 ml"; Elite usa a linha "EDP · 100 ml · Hombre".
4. Preço atual + preço anterior riscado; Dperfumes e Cosmetic mostram também o valor em cuotas ("En 3 cuotas de $6.633 sin interés").
5. Botão "Añadir/Agregar al carrito" direto no card (Elite também tem "Comprar ahora").
6. Extras: estrelas com número de avaliações (Elite, Cosmetic, Yauras, Falabella), chips de aroma (Dperfumes: "Dulce · Gourmand"), "Inspirado en ..." (Elite), selo de campanha ("Top 10 Cyber"), "Envío gratis" (Falabella).

### Filtros
- Sempre: **Marca**, **Precio**, **Género** (Hombre / Mujer / Unisex).
- Quase sempre: **Familia olfativa/notas** (Dulce, Amaderado, Floral, Cítrico, Ámbar...), **Tamaño/ml** (Elite: 100 ml com 92 itens), **Disponibilidad/En oferta**.
- Falabella acrescenta faixas de desconto (20% a 70%) e faixas de preço fixas.
- No celular os filtros ficam num botão "Filtrar y ordenar" que abre uma gaveta (Elite, Cosmetic, Yauras).

### Ordenação
Opções padrão: Más vendidos, Más relevantes, Precio menor→mayor, Precio mayor→menor, Más recientes; Dperfumes tem também "Mayor descuento". Padrão de entrada: popularidade/mais vendidos (Dperfumes, Elite).

### Grade
- Celular: 2 colunas em todas.
- Desktop: 4 colunas (Elite, Cosmetic, Yauras); Dperfumes deixa escolher 24/48/96 por página.

### Kits e sets
- Dperfumes trata "Sets de regalo" e "Miniaturas/Discovery set" como coleção própria no menu, com filtro por orçamento (hasta $50.000, $50.000–$100.000...).
- Nas lojas árabes o kit aparece no mesmo grid, com o conteúdo no título ("Set Miniaturas Yara Collection 4 x 5 ml – Lattafa").

### Navegação da categoria
- Dperfumes separa **Perfumes (diseñador)**, **Perfumes nicho** e **Sets de regalo**, e dentro de cada um: por género, marca, aroma, temporada, ocasião e "Recién llegados / Más vendidos / En oferta".
- Elite tem atalhos no topo para as marcas árabes (Lattafa, Armaf, Rayhaan).

### SEO
- Title no formato "Perfumes Árabes Originales en Chile | Lattafa, Armaf y Más" (Cosmetic).
- Meta description cita marcas + "originales" + "despacho a Chile" (Cosmetic, Elite, Yauras).
- Texto curto no topo; Yauras tem texto descritivo no card do produto.

## Como adequar à chileverificada.com (o que foi aplicado)

| Prática do mercado | Aplicação na loja | Observação |
|---|---|---|
| H1 + 1 linha com marcas | Banner com título, linha curta e contagem de produtos | Só marcas que a loja vende (Lattafa, Armaf, Afnan) |
| Atalhos de categoria | Chips: Todos · Kits · Unitarios · Mujer · Hombre | Funcionam por tag (`/collections/perfumes-arabes/kit`), entram sozinhos |
| Grade 2 col celular / 4 desktop | Grade do tema com 2/4 colunas e foto quadrada | Igual às 5 lojas |
| Selo de desconto | Selo "AHORRA $X" do tema, só onde existe preço comparativo real | Sem preço antigo inventado |
| Botão no card | "Agregar al carrito" rápido do tema ligado | |
| Filtros marca/precio/género | Filtros do tema ligados (o que o Search & Discovery da loja tiver) + chips por tag | Filtro de Marca/Género depende de configurar o app Search & Discovery (ponto aberto) |
| Ordenar por mais vendidos | Coleção com ordem padrão "Más vendidos" | |
| SEO title/description | Preenchidos em espanhol | |
| Estrelas/avaliações | **Não aplicado** | A loja não tem avaliações reais desses produtos; não inventar |
| Cuotas no card | **Não aplicado** | Loja vende contra entrega; não há parcelamento confirmado |

## Fontes
- https://dperfumes.cl/?s=arabe&post_type=product (acessado com o cookie anti-bot da própria página)
- https://www.eliteperfumes.cl/collections/perfumes-arabes
- https://www.falabella.com/falabella-cl/collection/perfumes-arabes
- https://cosmetic.cl/collections/perfumes-arabes
- https://yauras.cl/collections/perfumes-arabes

---

## Mobile (estudo v2, 09/10/2026)

Método: Playwright + Chrome, tela de 390x844 (iPhone, @2x, es-CL). Os prints estão em `ref-mobile/`: `01_<loja>_fold.png` (primeira tela), `02_<loja>_scroll.png` (rolagem) e `03_<loja>_card.png` (card). As medidas estão em `<loja>_medidas.json`.

**Ressalvas:**
- **Douglas:** bloqueada; a página fica só no esqueleto. Entrou a Ulta no lugar.
- **Sephora:** .es e .com negaram acesso, então foi medida a busca `sephora.com.mx/search?q=perfume`.
- **Notino:** `/perfumes-arabes/` dá 404, então foi medida `notino.es/perfumes/`.
- **Ulta:** um popup cobre parte do topo no print.
- **Falabella:** o banner fixo do app (186px) empurra o conteúdo para baixo.

| | dperfumes (referência) | Falabella | Notino | Sephora MX | Ulta |
|---|---|---|---|---|---|
| 1º produto (y / % da tela) | 375px / **44%** | 729px / 86% (~64% sem o banner do app) | 714px / 85% | 423px / **50%** | 890px / 105% |
| H1 | 18px/600 (Poppins) | 18px/300 (Lato) | 20px/500 (Roboto) | 20px/700 | 20px/500 |
| Descrição no topo | não | não (carrossel de marcas) | não (carrossel promo) | não | não |
| Chips horizontais | não | sim, 30px, 12px | sim, 32–36px, 12px | não | sim, 32px, 14px |
| Filtrar/Ordenar fixo ao rolar | não | sim | sim (2 linhas) | sim (barra de 48px no rodapé) | não |
| Grid | 2 col, gap 10, lateral 15 | 2 col, gap 0 + borda | 2 col, gap ~16 | 2 col, gap 15 | 2 col, gap 18 |
| Imagem | 1:1 | 1:1 | ~1:1 | 1:1 | 1:1 sobre fundo bege |
| Nome | 13,5px/500, 2 linhas, à esquerda | 14px/700, até 3 linhas | 16px + tipo 14px | 12px, até 3 linhas | 14px/300, até 3 linhas |
| Preço | 13,5px/700 | 18px/400 | 16px/700 | 24px/700 | 16px/300 |
| CTA no card | 38px, largura total, 13px/600, raio 35 | não visível | não | não | pílula 32px |
| Texto SEO | não | não visível | embaixo do grid | não | não |

### Regras tiradas do estudo e aplicadas na v2
1. Primeiro produto até ~45% da tela.
   - Melhores medidos: dperfumes com 44% e Sephora com 50%.
   - **v2: 24%** (205px). Antes era 899px, ou 107%: o produto só aparecia na segunda tela.
2. Topo enxuto: título em 1 linha, sem descrição.
   - v2: faixa de 101px com a linha das marcas, o H1 e 3 selos pequenos.
   - A descrição foi para o bloco SEO.
3. Chips com rolagem horizontal de 30–36px.
   - v2: 34px, fonte de 12,5px e snap.
4. Filtrar/Ordenar sempre à mão (3 de 5 lojas fixam).
   - v2: a barra "Filtrar · Ordenar" + chips fica fixa no topo ao rolar, no celular.
5. Grid de 2 colunas com gap de 10–18px.
   - v2: gap de 10px e margem lateral de 14px.
6. Imagem 1:1.
   - v2: 1:1 com cantos de 10px e fundo creme.
7. Nome em 13–14px, até 2 linhas, à esquerda.
   - v2: 13,5px. O nome principal fica em negrito numa linha e o conteúdo do kit em cinza em até 2 linhas.
8. Preço como maior texto do card, 16–18px em negrito.
   - v2: 16px/700 no celular e 17px no desktop.
9. CTA no card opcional; quando tem, 32–40px.
   - v2: Releasit com 40px, preto, texto de 12,5px, sem subtítulo e sem animação de tremer.
10. Selos pequenos.
    - v2: "BLACK FRIDAY" virou etiqueta de 9px acima do nome. As fotos já têm texto, e o selo em cima da foto cobria o título.
11. SEO embaixo do grid.
    - v2: bloco fechado com "Ver más", mostrando 3 linhas.
