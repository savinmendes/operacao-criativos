# Briefing: kits 2–5 e perfumes unitários Lattafa (loja Chile, 09/10/2026)

A pessoa aprovou.
- **Não pergunte nada.** Na dúvida, escolha o lado seguro e registre.
- **Nunca leia `.env`.**
- **Nunca invente fatos:** notas olfativas, ml, concentração, avaliações, preço antigo, estoque.

## O que existe e serve de modelo
- **Kit 1 pronto e no ar:** https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml (produto `gid://shopify/Product/10212552179968`).
  - O processo, as decisões e os textos estão em `C:\Users\PICHAU\Downloads\KIT1-YARA-PERFUMES\RELATORIO.md`. **Leia antes.**
  - Padrão a copiar:
    - **galeria 1:1:** hero do kit, com o nome sob cada frasco e os selos, e depois 1 foto por frasco;
    - **descrição:** 4 blocos 9:16 + a imagem genérica de garantia de 90 dias;
    - fundo, tipografia, etiquetas de nome e cards de notas iguais aos do Kit 1.
- **Projeto Flora do Kit 1:** `prj_ns72zge7hvbtq4mb73es6nkgm98fyfzn`, com as fotos originais de Yara, Yara Moi e Yara Elixir e todos os prompts que funcionaram.
- **Workspace Flora:** `ws_qd750nr5tby8qpnr1kbqj7aft17v8ey8`.
  - **Modelo:** Nano Banana 2 (`i2i-gemini-3.1-flash-image`, ~US$ 0,072 em 1K e 0,108 em 2K).
  - **Para vários frascos na mesma imagem:** use `is2i-gemini-3.1-flash-image` com várias referências.

## Regras de conteúdo
- **Os perfumes são ORIGINAIS** (confirmado pela pessoa). Pode usar "Originales Lattafa" / "100% originales".
- **O Yara ROUGE (vermelho) NÃO entra:** onde o plano tinha Rouge, entra o **Yara ELIXIR** (frasco rosa com anéis rosé/cobre e medalhão "Elixir").
- **Fidelidade do frasco em 1º lugar:** cada frasco tem que ser igual ao real (cor, anéis, faixa, medalhão, rótulo).
  - Use **foto real** como referência: a do projeto Flora do Kit 1, ou a foto oficial do produto, baixada do site da Lattafa ou de uma loja confiável, em boa resolução.
  - Suba no Flora antes de gerar.
  - Confira cada imagem em tamanho cheio contra a referência.
- **Notas olfativas:** só as oficiais. Fontes: a página oficial da Lattafa ou o Fragrantica; cite a fonte no relatório.
  - As notas do Yara, do Yara Moi e do Yara Elixir já estão na descrição do Kit 1. Use as mesmas.
  - A imagem de referência que a pessoa mandou tem notas resumidas e às vezes erradas. **Não copie dela.**
- **Selos:** "100 ml cada uno" (ou "100 ml EDP" no unitário), "Pagas al recibir", "Garantía 90 días", "Originales Lattafa".
  - Sem preço na imagem.
  - Sem depoimento.
  - Sem "envío gratis", a menos que a página base do Kit 1 tenha.
- **Idioma:** espanhol do Chile, acentos certos e texto grande (público amplo).

## Shopify (`mcp__claude_ai_Shopify__*`; antes de cada GraphQL, `graphql_schema` e `validate_graphql_codeblocks`)
- **Crie o produto como RASCUNHO**, com preço 0 se não houver preço. **Não publique.** A publicação e os preços quem faz é o agente principal, com a pessoa.
- **Título** no padrão do Kit 1. Exemplos:
  - "Kit 3 Perfumes Árabes Mujer | Yara + Yara Tous + Yara Elixir Lattafa 100ml";
  - unitário: "Perfume Árabe Lattafa Yara Tous 100ml EDP Original".
- **Handle** limpo, sem "rouge".
- **Vendor** "Lattafa", product type "Perfumes".
- **Tags:** `perfumes-arabes`, `lattafa`, `mujer` ou `hombre` (Asad = hombre) e `kit` ou `unitario`.
- **SKU:**
  - kits: `KIT2-...`;
  - unitários: `LAT-YARA-TOUS-100` etc.
- **Mídia:** galeria em ordem, alt text em espanhol.
- **Descrição:** só os blocos em imagem + a imagem de garantia, como no Kit 1. Use os mesmos arquivos de garantia que o Kit 1 usa.

## Unitário: estrutura
- **Galeria 1:1:**
  - hero do frasco com a caixa (se a foto real tiver a caixa), nome e selos;
  - foto do frasco com os ingredientes das notas;
  - foto lifestyle.
- **Descrição, 3 blocos 9:16:**
  1. gancho + notas;
  2. "cómo usar / para quién";
  3. "qué incluye" + garantia.

## Painel ao vivo (a pessoa acompanha)
Use `<ID>` = kit2, kit3, kit4, kit5, uni-yara-candy etc.
- python "C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py" etapa <ID> "<título>" --texto "..." --k N --n M
- `img <ID> <url> --legenda ...`
- `custo <ID> <usd>`
- `link <ID> "Rascunho" <url admin>`
  - O admin da loja é `https://admin.shopify.com/store/13cc83-26/products/<id numérico>`.
- No fim: `fim <ID> --aguardando "preço e publicar"`.

## Teto e entrega
- **Teto por produto:** US$ 1,00 (kit) e US$ 0,60 (unitário). Refaça cada imagem no máximo 1 vez.
- **Arquivos locais:** `C:\Users\PICHAU\Downloads\KITS-PERFUMES\<ID>\`, com as imagens numeradas, `00-folha.jpg` e `RELATORIO.md` (textos, fontes das notas, custo real, QA e pendências).
- **Relate ao agente principal:**
  - id e handle do produto;
  - custo;
  - o que falta conferir.
