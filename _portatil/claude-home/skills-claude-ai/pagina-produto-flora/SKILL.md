---
name: "pagina-produto-flora"
description: "Monta a página de produto COD a partir das fotos do produto: blocos 9:16 com texto dentro da imagem gerados no Flora e publicados na Shopify. Use para criar ou refazer página de vendas de produto."
---

# Página de produto — Flora + Shopify

Pipeline para criar a página de vendas mobile de um produto COD (Chile por padrão) a partir das fotos do produto. Cada bloco é uma imagem vertical 9:16 COM o texto de venda dentro (decisão do Savin). A página na Shopify é a sequência dessas imagens.

## Entrada obrigatória
- Fotos ORIGINAIS do produto (fornecedor/concorrente), idealmente 6 a 11. **Sem foto, pare e peça.** Nunca gere o produto só por descrição em texto. Link do Kalodata pede login: usar a página pública do TikTok Shop, https://shop.tiktok.com/view/product/<id>, que traz título, specs e as URLs das fotos.
- Mercado e idioma (padrão: Chile, espanhol chileno). Travar o idioma em todo prompt.
- Oferta (preço, kits 1/2/3 un, frete) — se faltar, deixar marcador e avisar.
- Specs vindas de anúncio de terceiro: confirmar com o fornecedor antes de publicar.
- Produto na Shopify (handle ou título); se não existir, criar como rascunho no fim.

## Regras que não se quebram
- Fidelidade > criatividade: o produto gerado tem que ser o mesmo das fotos (cor, formato, peças, acessórios). Não inventar especificação (watts, bateria, autonomia, capacidade, certificação, garantia, avaliações) que não esteja confirmada.
- Não usar nome de marca de terceiros (Shark, BISSELL, DREAME etc.) em imagem nem texto se o produto não é da marca — inclusive a marca que aparece na maleta/foto do fornecedor.
- Público sênior: texto GRANDE (headline ~1/10 da altura da imagem), alto contraste, no máximo 2 mensagens + até 3 selos curtos por bloco.
- Nenhum texto de produção na arte (bloco, hero, mobile, CRO, medidas etc.).
- Sem hora do dia no texto (nada de "esta noche").
- Avisar o custo estimado da leva ANTES de gerar, e avisar antes de gastar além do informado (re-tentativas, modelo extra).
- Um modelo por tipo de geração — não gerar o mesmo bloco em vários modelos. Só trocar de modelo se o escolhido falhar, e avisando.
- Em lote: terminar o primeiro bloco, mostrar, ajustar o máximo possível, e só depois gerar os demais.

## Modelos (testado em 26/09/2026 na chave de impacto)
- **Blocos com texto: GPT Image 2.5 Sunburst** (`is2i-gpt-image-2-5-sunburst`, ~US$ 0,133/img) — texto grande e correto em espanhol, produto fiel. Venceu o Nano Banana Pro, que saiu com texto pequeno e pouco contraste.
- **Referências sem texto (360, ficha do kit): Nano Banana Pro** (`is2i-gemini-3-pro`, US$ 0,18) ou GPT Image 2.5.
- **Entradas dos blocos = as FOTOS ORIGINAIS**, não o 360. Usar referência gerada como entrada fez o produto mudar no hero; com as originais ficou fiel.

## Passo a passo

### 1. Canvas do produto
- Um projeto Flora POR PRODUTO (`flora_create_project`), nome: `[Produto] — Página [País]`. Nunca misturar produtos num canvas.
- Colocar as fotos originais com `flora_add_to_canvas` (content_url HTTPS) ou `flora_create_asset` / `flora_complete_asset`, na coluna "00 Foto original NN".

### 2. Referências (opcional, uma vez por produto)
- 360 View (Nano Banana Pro) e ficha do kit (Blueprint, GPT Image 2.5), entradas = todas as fotos originais. Servem para o usuário conferir o produto e para o bloco de kit — não são entrada obrigatória dos blocos.
- Conferir a cor contra as fotos antes de usar qualquer referência gerada. Se a cor saiu errada, corrigir aqui (edição com referência de cor estrita).

### 3. Blocos (9:16, GPT Image 2.5, entradas = fotos originais)
Sequência padrão (ajustar ao produto):
1. Hero — produto em uso real + promessa principal + 3 selos.
2. Problema — a dor que o produto resolve, cena do cotidiano chileno.
3. Solução/demonstração — produto em uso, mostrando o mecanismo.
4. Close-ups — detalhes e componentes reais.
5. Usos/versatilidade — 2 a 4 situações de uso.
6. Kit + oferta — só o que vem de fato, "Paga al recibir".

Estrutura do prompt de cada bloco:
```
INTERNAL INSTRUCTIONS — DO NOT RENDER ANY OF THIS TEXT EXCEPT THE SPANISH COPY IN QUOTES.
Create block N (9:16) of a mobile sales page for Chile.
PRODUCT FIDELITY (most important): the product must be EXACTLY the one in the
reference photos — same shape, colors, parts and markings. Do not redesign, swap,
add or remove parts. No brand names or logos other than those printed on the product itself.
SCENE: <2 a 4 linhas: pessoa 45–70 anos quando houver, cenário chileno, ação, enquadramento>
TEXT IN THE IMAGE (Spanish for Chile, exactly as written, nothing else):
Headline: "..."  Subheadline: "..."  Badges (máx. 3): "..." "..." "..."
TYPOGRAPHY: shown at ~390 px wide to an older audience — every text BIG (headline
~1/10 of image height), high contrast, clean sans-serif. Max two messages plus badges.
No other text, no prices unless given, no watermark, no layout labels.
```

### 4. Conferir
- Ver o bloco ao lado da foto original: no navegador do PC do usuário, montar uma página com as duas imagens e tirar screenshot (se a janela estiver minimizada, o screenshot falha — pedir para restaurar). Checar produto, ortografia do espanhol e tamanho do texto.

### 5. Publicar na Shopify
- `descriptionHtml` = sequência dos blocos: `<img>` com a URL pública do asset do Flora, largura 100%, `alt` com a headline do bloco, `loading="lazy"` a partir do 2º.
- Mostrar ao usuário antes de gravar. Produto novo entra como rascunho. Gravar com `update-product` / `create-product` do conector Shopify.
- Conferir a página publicada no navegador (mobile).

### 6. Organizar e arquivar
- `flora_arrange_canvas` por colunas: 00 Fotos originais · 01 Referências · 02 Blocos (na ordem da página) · 03 Descartes.
- Salvar imagens finais + prompts na base local "Produtividade com ia" (C:\Users\PICHAU\Downloads\Produtividade com ia), seguindo o padrão de nomes do CLAUDE.md dela.

## Depois de publicar
Quando houver tráfego, ler o Clarity (rolagem e cliques) e a efetividade real (Shopify × Dropi pelo nº do pedido) para decidir qual bloco trocar.