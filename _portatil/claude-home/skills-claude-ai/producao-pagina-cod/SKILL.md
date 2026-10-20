---
name: "producao-pagina-cod"
description: "Produz a página de produto COD completa no Flora (14 blocos 9:16 com texto na imagem + foto principal 1:1 da variante + galeria) a partir de link ou fotos do produto, e entrega HTML e imagens baixadas."
---

# Produção de página COD (Flora → Shopify)

Use quando o Savin mandar um link de produto (marca, concorrente, AliExpress, TikTok Shop) ou fotos e pedir página, foto principal ou galeria. Mercado padrão: Chile, espanhol chileno (travar o idioma em todo prompt). Exemplo pronto: canvas "Câmera Solar Pan 2K — Página Chile" (prj_ns72ykdmqkxp97r73tmjfpj5ws8fpaz2). Padrão visual validado: CAM-TTK Chile (prj_ns7bz5gzwgdm5mw6ke6ds7ramn8fk90q).

## Entregas (sempre as três)
1. **Página completa — 14 blocos 9:16** (texto de venda DENTRO da imagem). Página de 5 blocos ele achou simples demais.
2. **Foto principal da variante 1:1** (padrão "caixa", abaixo).
3. **Galeria 1:1** (6–7 imagens) + HTML da descrição + imagens baixadas no Chrome dele.

## Estrutura dos 14 blocos
1 Hero (promessa + produto na cena do país + uso + faixa com 3 ícones) · 2 Problema (dor, sem produto) · 3 Mecanismo principal + 3 ícones com números reais · 4 Uso/controle central · 5 Benefício 2 · 6 Prova visual (antes/depois, dia/noite) · 7 Benefício 3 · 8 Colagem "feita para…" (3 painéis, 1 legenda cada) · 9 Ficha técnica em 6 cards (≤4 palavras) · 10 Uso/instalação em 3 passos · 11 Comparativo comum × este (3 linhas ✗/✓) · 12 O que vem na caixa · 13 FAQ (3 perguntas) · 14 "Compra sin riesgo": selo 90 días de garantía + "Paga al recibir" + "Envío a todo Chile".

## Foto principal da variante (padrão aprovado)
- Fundo claro; título no topo em 2 linhas (navy + ciano), ex.: "Cámara de Seguridad Panorámica" / "Solar 360°".
- CAIXA PEQUENA de papelão aberta (~20×15×10 cm, cabe na mão — os pacotes reais COD são pequenos), produto DESMONTADO e bem justo dentro: corpo, painel solto, antenas, suporte/placa de parede, parafusos, cabo, chip quando for 4G. + o produto MONTADO ao lado.
- Selo de peso fixo (um número, informado por ele, ex.: 180 g / 196 g / 210 g) + "Nanotecnología súper liviana". Sem frase "Todo llega en una caja".
- Vários produtos parecidos: mesma ideia, composição e peso DIFERENTES para cada (mão segurando / caixa apoiada / duas mãos apresentando; faixa / selo redondo / etiqueta vertical).
- Conferir: peças no formato real (ex.: painel solar QUADRADO), placa traseira de parede visível no montado e solta na caixa, nenhuma peça duplicada.

## Regras
- Foto ORIGINAL do produto como referência de toda geração (image-to-image); sem foto, parar e pedir.
- Remover logos de marca (WYZE, AOC…) e grafismos digitais ("4G LTE" desenhado no painel, setas, diagramas).
- Só claims da ficha da referência ou ditos por ele; os que ele inventar (peso, nanotecnologia) usar, mas avisar uma vez que precisam bater com o produto real (risco de recusa no COD). Não colocar "2K"/Wi-Fi/4G sem confirmação.
- Público sênior: texto GRANDE, máx. 2 mensagens + 3 rótulos por bloco. Sem hora do dia. Sem preço na arte. Garantia 90 dias.
- Modelo: GPT Image 2.5 Sunburst (`is2i-gpt-image-2-5-sunburst`, high, 1k) ≈ US$ 0,064–0,073/imagem. Avisar o custo da leva antes; se for refazer além do estimado, avisar.
- Lote: gerar 1 bloco + a foto principal, revisar, depois o resto junto (até 20 por chamada).
- Correções pontuais: editar usando a própria imagem gerada como referência 1 (+ foto original como ref. 2), pedindo "keep everything identical, change only…".
- Se ele mudar o pedido no meio de uma geração lenta, gerar já a versão com tudo junto em vez de esperar.

## Detalhes técnicos do ambiente
- A nuvem NÃO acessa media.flora.ai nem storage.googleapis.com (proxy bloqueia). Então:
  - **Revisar**: injetar overlay com as imagens na aba do Chrome dele via `javascript_tool`, screenshot, remover overlay.
  - **Baixar**: no Chrome dele, `fetch(url)` → blob → `<a download>`; uma imagem por chamada (várias juntas pode falhar). Avisar o nome dos arquivos e mandar os links como reserva.
  - **Fotos que ele anexa no chat**: não dá para subir daqui. Pedir que ele arraste no canvas do Flora (ou abra os links `upload_page` do `flora_create_asset`), achar os nós novos com `flora_get_canvas` e usar o `output_url` como `content_url` de static_image no projeto do produto.
- Mostrar as imagens no chat com markdown `![](url)` via SendUserMessage.
- Fotos de etiqueta de transportadora (Starken etc.) têm dados de clientes: usar só como referência de tamanho, nunca como entrada de geração.

## Passo a passo
1. Ler a referência: Shopify `<url>.json` (fotos) + WebFetch da página (features, ficha, caixa, FAQ).
2. Conector Shopify: checar `get-shop-info`; se não for a loja do mercado, entregar HTML em vez de publicar.
3. Canvas: `flora_create_project` "[Produto] — Página [País]", fotos originais como static_image.
4. Bloco 1 + foto principal → revisar → resto em lote → revisar tudo → corrigir só o que errou.
5. Organizar: rótulos "02 Bloco NN · tema", "03 Galeria NN", "04 PRINCIPAL · produto · peso", "99 DESCARTE · motivo"; `flora_arrange_canvas` em linhas; nota "COMECE AQUI" com claims, custo e pendências.
6. Entregar: HTML (`<img>` 100%, alt = headline, lazy a partir do 2º), lista de links na ordem, imagens baixadas no Chrome, e a lista COMPLETA do que ele faz na mão (confirmar specs/peso com fornecedor, subir em Shopify > Arquivos e trocar links, galeria 1:1 na ordem com a principal primeiro, preço).

## Template de prompt
```
INTERNAL INSTRUCTIONS — DO NOT RENDER ANY OF THIS TEXT EXCEPT THE SPANISH COPY IN QUOTES.
Create <block N (9:16) | square (1:1) main image> for an online store in Chile: <PAPEL>.
Visual system: navy #0B1F3A, cyan #22C3E6, white; extra-bold sans-serif; realistic commercial photo.
PRODUCT FIDELITY (most important): EXACTLY the product in reference 1 — <descrição física curta>. Do not redesign. REMOVE every brand logo and digital graphics.
SCENE/LAYOUT: <cena/composição>.
TEXT (Spanish for Chile, exactly as written, nothing else): <linhas entre aspas>
TYPOGRAPHY: big, high contrast, readable at ~390 px / as thumbnail. No other text, no prices, no watermark.
```