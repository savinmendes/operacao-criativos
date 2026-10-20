# Unitário Lattafa Yara Elixir 100ml EDP (Chile): uni-yara-elixir

Data: 09/10/2026. Substitui o Yara Rouge que estava no plano.

## Shopify
- **Produto:** `gid://shopify/Product/10212596547840` (**RASCUNHO**, preço 0, sem canais)
- **Admin:** https://admin.shopify.com/store/13cc83-26/products/10212596547840
- **Título:** Perfume Árabe Lattafa Yara Elixir 100ml EDP Original
- **Handle:** `perfume-arabe-lattafa-yara-elixir-100ml-edp-original`
- **Vendor / tipo:** Lattafa / Perfumes
- **Tags:** perfumes-arabes, lattafa, mujer, unitario, yara
- **SKU:** `LAT-YARA-ELIXIR-100`. Estoque não rastreado e política DENY, como no Kit 1.
- **Galeria:**
  1. hero com frasco e caixa (alt "Perfume árabe Lattafa Yara Elixir 100 ml EDP con su caja");
  2. frasco com os ingredientes das notas;
  3. lifestyle no tocador.
- **Descrição:** blocos 1 a 3 (Files `uni-yara-elixir-bloco1..3`) e depois a mesma `garantia-90-generica.jpg` do Kit 1. Só imagens, sem texto.

## Arquivos
| # | Arquivo | Uso | Textos na imagem |
|---|---|---|---|
| 01 | 01_galeria_hero | Galeria 1, 2048² | YARA ELIXIR / PERFUME ÁRABE LATTAFA / 100 ml EDP · Pagas al recibir · Garantía 90 días · Originales Lattafa |
| 02 | 02_galeria_notas | Galeria 2, 1024² | sem texto (frutilla, grosella negra, jazmín, azahar, vainilla, caramelo) |
| 03 | 03_galeria_lifestyle | Galeria 3, 1024² | sem texto |
| 04 | 04_descricao_bloco1_notas | Descrição 1, 768x1376 | ATRAE Y ENAMORA CON TU AROMA. / Yara Elixir: dulce e intenso. / SUS NOTAS: SALIDA Frutilla y grosella negra · CORAZÓN Jazmín y azahar · FONDO Vainilla y caramelo / 100 ML EDP · PAGAS AL RECIBIR · GARANTÍA 90 DÍAS |
| 05 | 05_descricao_bloco2_como-usar | Descrição 2 | ¿PARA QUIÉN ES? Para la mujer que ama los aromas dulces e intensos. / CÓMO USARLO: 1 Aplica sobre la piel limpia. 2 Rocía en cuello y muñecas. 3 No frotes la piel. / Para el día a día y ocasiones especiales. |
| 06 | 06_descricao_bloco3_que-incluye | Descrição 3 | QUÉ INCLUYE: 1 perfume Yara Elixir Lattafa / Eau de Parfum · 100 ml / 100% original / EL TOQUE FINAL DE TU ESTILO. / Pagas al recibir en tu casa · Garantía de 90 días / YARA ELIXIR |

Também estão na pasta: `00-folha.jpg` (folha de contato), as versões .jpg, `_ref/` (foto real) e `_versoes-anteriores/`.

## Fontes
- **Foto do frasco:** a mesma foto real do Kit 1 (frasco + caixa), no projeto Flora do Kit 1 (`cf49e0c6...jpg`, 1500x1500).
- **Notas:** as mesmas da descrição do Kit 1, como pede o briefing: frutilla, grosella negra, jazmín, azahar, vainilla y caramelo.
  - Conferidas no Fragrantica (https://www.fragrantica.com/perfume/Lattafa-Perfumes/Yara-Elixir-117615.html):
    - saída: Strawberry S'mores e Black Currant;
    - coração: Jasmine e Orange Blossom;
    - fundo: Vanilla, Caramel, Amber e Musk.
  - Âmbar e almíscar ficaram de fora para manter a mesma lista do Kit 1.

## Custo real (charged_cost do Flora)
| Item | US$ |
|---|---|
| 01 hero 2K | 0,108 |
| 02, 03 v1, 04, 05, 06 (5 × 0,072, 1K) | 0,360 |
| 03 refeito (1ª e única refação) | 0,072 |
| **Total** | **0,540** (teto: 0,60) |

- Canvas Flora (compartilhado com o Asad): https://app.flora.ai/projects/ns7d69p9xk7tqewc9s632jzwr18fz305

## QA em tamanho cheio
- **01 hero:** frasco e caixa fiéis (anéis rosé, medalhão "Elixir", "YARA", "Lattafa"), selos corretos e com acento. Aprovado.
  - O texto miúdo do selo da caixa sai embaralhado ("EAU DE PERENUE"). Só aparece com zoom.
- **02:** fiel. Aprovado.
- **03 lifestyle:**
  - A v1 tinha o frasco deformado na mão ("Y'ARA", logo errado).
  - A refação (frasco em pé, mulher desfocada ao fundo) veio com cena boa, mas o frasco saiu **liso, sem caligrafia, medalhão nem textos**.
  - Com o teto de 1 refação, colei localmente (PIL, sem custo) o **frasco da foto real** sobre o frasco liso, com sombra de contato.
  - Ficou um leve contorno claro na borda superior esquerda da tampa, visível com zoom.
  - As duas versões estão em `_versoes-anteriores/`.
- **04:** textos e notas corretos. No card "FONDO", a fava de baunilha passa na frente do frasco. Aprovado.
- **05:**
  - A IA escreveu "Para el día a día y / y ocasiones" (o "y" saiu duplicado). Apaguei localmente o "y" do fim da 1ª linha.
  - Os frascos estão fiéis, mas o "Lattafa" sai pouco legível no frasco pequeno.
- **06:** fiel, textos corretos. Aprovado.
- **Fundo e tipografia:** seguem o Kit 1 (blush/creme, mármore, sans geométrica, etiqueta escura de nome).

## Pendências / conferir
1. Preço e publicação (canais e ACTIVE): ficam com o agente principal e a pessoa.
2. Conferir se a montagem do frasco na 03 está boa o suficiente. Se não estiver, uma nova geração custa US$ 0,072 e passa do teto.
3. A imagem de garantia genérica diz "Envío a todo Chile" e "WhatsApp". É a mesma do Kit 1; confirmar se vale para o unitário.
4. "Para la mujer que ama los aromas dulces e intensos", "Para el día a día y ocasiones especiales" e "Cómo usarlo" são textos de marketing e uso genérico, e não afirmam duração nem fixação.
5. A mulher das imagens 03, 04 e 05 foi gerada por IA, como no Kit 1.
6. Os arquivos da galeria no Shopify ficaram com nome `gen-...jpg` (só estético).
