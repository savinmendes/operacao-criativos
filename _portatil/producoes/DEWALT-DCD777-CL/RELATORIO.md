# DeWalt DCD777 / DCD7771: página da loja Chile (chileverificada.com)

Data: 09/10/2026
- **Produto Shopify:** `gid://shopify/Product/10212654645504`, em **RASCUNHO** (DRAFT) e sem publicação em nenhum canal.
- **Admin:** https://admin.shopify.com/store/13cc83-26/products/10212654645504
- **Handle:** `taladro-atornillador-inalambrico-dewalt-dcd7771-20v-max-brushless-2-baterias-cargador`
- **Canvas Flora:** https://app.flora.ai/projects/ns7ab410xj4bjhat3s83z5km758fyq5q (projeto "DeWalt DCD777 – Chile")
- **Estudo completo** (especificações, preços e fontes): `ESTUDO.md`.

O produto de teste `/products/dewalt` (kit genérico 28V) **não foi usado nem alterado**. Nenhum outro produto, página ou arquivo de tema foi mexido.

## Decisão de kit e preço
- **Kit:** DCD7771D2-B2, com 1 taladro atornillador brushless de 1/2", 2 baterias DCB203 de 2.0 Ah, carregador DCB107 e maleta plástica.
  - O DCD777 saiu do dewalt.cl (a página dá 404).
  - O DCD7771 é o atornillador compacto brushless 20V MAX que a DeWalt Chile lista hoje, com o mesmo corpo do DCD777 nas fotos oficiais.
  - O DCD776C2-B2 continua no site oficial, mas com dados contraditórios (bolsa × maleta, 15 × 16 posições, "sin carbones" × carcaça sem "BRUSHLESS") e preços de lojas sem estoque. Não foi escolhido.
- **Preço no rascunho:** CLP **179.990**. É o "normal" da Easy e o preço de venda da Sodimac e da Ripley.
  - Lista mais alta comprovada: 257.990 (Sodimac).
  - **O compare-at não foi aplicado.**
- Evidência completa na tabela do `ESTUDO.md` §3.

## Shopify
- **Título:** "Taladro Atornillador Inalámbrico DeWalt DCD7771 20V MAX Brushless + 2 Baterías 2.0Ah + Cargador + Maletín (Original)"
- **Dados do produto:** vendor DeWalt · tipo Herramientas · tags `dewalt`, `herramientas` · SKU `DCD7771D2-B2` · preço 179990 · estoque não rastreado (igual ao Kit 1) · status DRAFT.
- **Galeria 1:1** (alt em espanhol):
  - 01: hero do kit;
  - 02: detalhe do taladro;
  - 03: em uso, madeira;
  - 04: qué incluye.
- **Descrição** (padrão das páginas de perfume):
  - 3 blocos 9:16 em Files: `dewalt-dcd7771-bloco1-ficha-tecnica.jpg`, `-bloco2-usos.jpg` e `-bloco3-que-incluye-pagas-al-recibir.jpg`;
  - tabela HTML curta com os números oficiais;
  - nota do 20V MAX* (18 V nominal).
- A imagem genérica "90 días de garantía" das páginas de perfume **não foi colocada**, porque não há garantia confirmada para este produto.

## Imagens (`C:\Users\PICHAU\Downloads\DEWALT-DCD777-CL\`)
| # | Arquivo | Onde | Textos na imagem |
|---|---|---|---|
| 01 | 01_galeria_kit-hero.png (2048²) | Galeria 1 | TALADRO ATORNILLADOR DEWALT / 20V MAX* BRUSHLESS · DCD7771 / Original DeWalt · 2 baterías 2.0 Ah · Pagas al recibir |
| 02 | 02_galeria_taladro-detalle.png (1024²) | Galeria 2 | sem texto |
| 03 | 03_galeria_en-uso-madera.png (1024²) | Galeria 3 | sem texto |
| 04 | 04_galeria_que-incluye.png/.jpg (2048²) | Galeria 4 | QUÉ INCLUYE TU KIT / 1 Caja Plástica de Transporte / 1 Cargador DCB107 / 2 Baterías de 20V MAX 2.0 Ah / 1 Taladro/Atornillador DCD7771 |
| 05 | 05_descricao_bloco1_ficha-tecnica (1536x2752) | Descrição 1 | FICHA TÉCNICA / 20V MAX* / Motor sin carbones (Brushless) / Mandril 1/2" (13 mm) / 2 velocidades · hasta 1.750 rpm / 15 posiciones de torque / Luz LED / nota 18 V nominal |
| 06 | 06_descricao_bloco2_usos | Descrição 2 | PERFORA Y ATORNILLA / Compacto y liviano para trabajos en casa y en obra / MADERA · METAL · ATORNILLAR |
| 07 | 07_descricao_bloco3_kit-pagas-al-recibir | Descrição 3 | QUÉ INCLUYE TU KIT (4 itens) / PRODUCTO ORIGINAL DEWALT / Pagas al recibir · Envío a domicilio |

- **Referências usadas no Flora:** fotos oficiais `assets.dewalt.cl` DCD7771D2_K1 (kit), DCD7771B_2, DCD7771B_1 e o gráfico GEC1. Cópias locais em `_ref\`.
- `00-folha.jpg`: folha de contato das 7 imagens.

## QA em tamanho real
- **Fidelidade:** em todas as imagens o taladro bate com a foto oficial (corpo amarelo/preto, logo DEWALT no motor, selo "20V MAX | BRUSHLESS", anel 1–15, empunhadura). A maleta tem o logo amarelo grande, as baterias são compactas com "20V" e "2 Ah", e o carregador é o DCB107 preto e amarelo. A quantidade de itens está certa (1 taladro, 2 baterias, 1 carregador, 1 maleta).
- **Selo do motor ilegível:** a IA escreveu o selo "BRUSHLESS" errado na 04, nos três painéis da 06 e na 07 ("BRUSIILESS", "20vMAN"). **Corrigi localmente com PIL, sem custo:** reescrevi o selo no mesmo ângulo. Os originais do Flora estão em `_versoes-anteriores\`. No zoom de 4–5× ainda se nota uma leve diferença de fonte, mas no tamanho real fica correto.
- **03 refeita 1 vez:** a 1ª versão tinha mãos a mais (4 mãos) e está em `_versoes-anteriores\03_v1_manos-extra.png`. A 2ª tem uma pessoa e duas mãos; o taladro aponta para baixo, com o punho na horizontal. Aprovada.
- **Textos:** espanhol com acentos corretos (TÉCNICA, Baterías, maletín, Envío, QUÉ). Sem preço, sem depoimento e sem avaliações.
- **Números:** só os oficiais. Torque em Nm, peso da ferramenta e golpes/min não aparecem, porque não há fonte oficial.
- 05 tem uma moldura cinza fina nas bordas (estético, não refeito).
- 06 traz o logo DEWALT no rodapé e o selo "Envío a domicilio" vem na 07. **Confirmar se a loja entrega a domicílio em todo o Chile.**

## Custo real (charged_cost do Flora)
| Item | US$ |
|---|---|
| 01, 04, 05, 06, 07 em 2K (5 × 0,108) | 0,540 |
| 02, 03 v1, 03 v2 em 1K (3 × 0,072) | 0,216 |
| **Total** | **0,756** (teto 1,20) |

## Pendências e pontos abertos
1. **Modelo físico do fornecedor:** confirmar que a unidade é o **DCD7771D2-B2** (maleta e 2 baterias de 2.0 Ah).
   - Se vier DCD777D2 (bolsa e baterias compactas) ou DCD776C2 (percutor, 2 × 1.5 Ah), é preciso trocar título, SKU, a tabela e as imagens 01, 04 e 07.
   - A Dropi estava fora do ar nesta sessão (erro 502), por isso não deu para procurar fornecedor.
2. **Garantia:** a garantia oficial da DeWalt Chile (3 anos limitada, 1 ano de serviço, 90 dias de satisfação; baterias só 30 dias) **exige fatura original de distribuidor autorizado**. Por isso **nenhuma imagem diz "Garantía oficial"**. Se o fornecedor for distribuidor autorizado e emitir boleta/factura, dá para acrescentar o selo.
3. **Estoque:** a variante está sem rastreio de estoque. Definir quantidade/local quando o fornecedor for confirmado.
4. **Preço riscado (compare-at):** decidir se usa 257.990 (normal da Sodimac). Não foi aplicado.
5. **MercadoLibre, Imperial e Construmart** não puderam ser lidos (bloqueio ou erro). Os preços do ML vêm só do trecho do buscador.
6. **Publicação:** fica com a dona (status, canais e handle final).
7. "Original" aparece no título e nas imagens 01 e 07 com base na confirmação da dona. Manter a prova de origem (nota do fornecedor) guardada.
