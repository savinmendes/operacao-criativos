---
name: "clonar-pagina-entre-paises"
description: "Clona uma ou várias páginas de produto (e sincroniza o tema) de uma loja Shopify do Savin para outra de outro país/língua, gravando no tema via API (themeFilesUpsert): produto, variantes, template, card de envio, moeda, textos e estilo, com checksum."
---

# Clonar página de produto entre lojas de países diferentes

Use quando o Savin pedir para levar uma ou várias páginas/produtos de uma loja (ex.: Chile) para outra (ex.: Guatemala, México, Colômbia) ou para deixar o tema de uma loja igual ao de outra. Fale em português do Brasil, execute direto, e entregue no fim UMA lista com tudo que ficou para ele fazer.

## Regras fixas (não perguntar)
- Lojas COD: **sem parcelamento** em nenhum texto.
- **Preço riscado (compareAtPrice) = 2× o preço de venda** da oferta, arredondado para o formato do país.
- Garantia sempre 90 dias. Sem hora do dia nos textos.
- Galeria do produto sempre 1:1; blocos 9:16 só na descrição.
- Nunca duplicar, publicar ou apagar tema. Só editar o tema ativo.

## 0. Entradas (pedir tudo de uma vez se faltar)
- Loja ORIGEM e loja DESTINO (país, moeda, língua).
- Lista de produtos: para cada um, URL da página de referência (ou handle) e os preços de venda das ofertas na moeda do destino (ele define; nunca inventar). Com mais de um produto, pedir numa tabela única: `handle | COMPRE 1 | COMPRE 2 | COMPRE 3`.
- Mês da oferta (padrão: mês atual em espanhol, ex. OCTUBRE).
- Transportadoras do destino, só se o país ainda não tiver card pronto na seção "Cards de envio por país".
- Para sincronizar tema: o .zip do tema da ORIGEM (Temas → ⋯ → Baixar arquivo do tema).

## Lote (mais de um produto)
Separar o que é da LOJA (faz uma vez) do que é do PRODUTO (repete por item):
- **Uma vez por loja:** passos 1, 5 (sincronizar tema/snippets de estilo) e o card de envio do país. Fazer isso ANTES do primeiro produto.
- **Por produto:** passos 2, 3 e 4 (produto, template, gravação). Fazer o **primeiro produto completo até a verificação final (passo 6)** e mostrar ao Savin; só depois rodar o restante em sequência, no mesmo molde.
- Reaproveitar: o template adaptado do primeiro produto vira base dos seguintes (trocar só handle, textos específicos, preços e `breaks_benefits`). Gravar os templates dos demais numa só chamada de `themeFilesUpsert` (vários `files`), depois conferir todos os md5 de uma vez.
- Ao final do lote, UMA verificação: tabela `produto | URL destino | preços conferidos | status` + prints origem × destino de cada um. Qualquer produto com problema fica marcado na tabela; não parar o lote por ele.
- Se o produto já existir no destino (mesmo handle), NÃO criar de novo: avisar e usar `productUpdate` só no que mudou (template, preços, fotos).

## 1. Conectar e conferir
1. `get-shop-info`. Loja errada: `switch-shop` → `get-shop-info` (se pedir login, ele reconecta em Configurações → Conectores → Shopify e escolhe a loja certa).
2. Confirmar moeda do destino.
3. Tema ativo: `themes(roles:[MAIN]){id name}` + ler `theme_name/theme_version` em `config/settings_schema.json` (grep no arquivo salvo, não ler inteiro). Se o tema não for o mesmo da origem (ex. Shrine Pro), PARAR e avisar.
4. Guardar o `id` do tema (gid://shopify/OnlineStoreTheme/…) para o passo 4.

## 2. Produto (MCP)
- `productCreate` com title, handle, productType, vendor, status ACTIVE e `media` (URLs das fotos da origem, na mesma ordem).
- Variantes de oferta: NÃO usar `productVariantsBulkCreate` direto (dá "A opção não existe"). Fazer `productOptionsCreate` com `variantStrategy: CREATE` (opção "Oferta": COMPRE 1, RECIBA 2 / COMPRE 2, RECIBA 4 / COMPRE 3, RECIBA 6) e depois `productVariantsBulkUpdate` com price, compareAtPrice (2×), `inventoryPolicy: CONTINUE`, `inventoryItem: {tracked:false}` (senão aparece "Agotado").
- `publishablePublish` na publicação "Loja virtual".
- Depois que o template existir: `productUpdate` com `templateSuffix`.
- Conferir preço por unidade (preço ÷ unidades). O selo "MAYOR AHORRO" tem que estar na oferta mais barata por unidade; se não estiver, avisar e propor ajuste.

## 3. Adaptar o template JSON (sandbox)
- Pegar o template da origem (zip ou `files(filenames:[...]){body{...on OnlineStoreThemeFileBodyText{content}}}` na loja origem) e trocar: país em selos/títulos ("Más vendido en <País> 2026", "Envío a toda <País>"), cidades dos depoimentos e bandeira, moeda e formato numérico, mês da oferta, preço por unidade (`breaks_benefits`), card de envio do país.
- Para editar um bloco do template JSON, localizar o valor de `custom_liquid` do bloco e substituir com `JSON.stringify(novoHtml)`.
- Validar com `JSON.parse` e procurar restos da origem (nome do país, cidades, transportadoras, símbolo de moeda, bandeira): tem que dar zero.
- Guardar sempre o conteúdo original do arquivo no sandbox antes de sobrescrever (para reverter).

## 4. Gravar no tema ativo (API, método principal)
Usar a mutation `themeFilesUpsert` pelo `graphql_mutation` do conector (fluxo: `graphql_schema` → montar → `validate_graphql_codeblocks` → executar):
```graphql
mutation($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    userErrors { filename code message }
  }
}
```
`files: [{ filename: "templates/product.<sufixo>.json", body: { type: TEXT, value: "<conteúdo>" } }]`. Serve para arquivo novo e para sobrescrever existente (templates, sections, snippets, assets de texto). Vários arquivos na mesma chamada. Arquivo grande: montar no sandbox e mandar o valor inteiro na chamada (não colar no chat).
- Depois, conferir `files(filenames:[...]){checksumMd5 size}` contra o md5 calculado no sandbox. Tem que bater.
- Erro de Liquid/JSON vem em `userErrors`: corrigir no sandbox e reenviar; nunca deixar arquivo quebrado salvo. Se já gravou errado, reenviar o original guardado.
- **Access denied / escopo:** o conector pode não ter `write_themes`. Plano B: app custom na loja (Configurações → Apps e canais de vendas → Desenvolver apps → Criar app → Configurar escopos da Admin API: `write_themes`, `read_themes` → Instalar app → copiar o token de acesso da Admin API). Passar ao Savin esse passo a passo completo de uma vez. Com o token, chamar a mesma mutation do sandbox em `https://<loja>.myshopify.com/admin/api/2025-07/graphql.json` com header `X-Shopify-Access-Token`. O token fica só no sandbox da sessão; não repetir no chat.
- **Plano C (só se A e B falharem):** editor de código do admin via extensão do Chrome, conforme "Anexo: método pelo Chrome".

## 5. Sincronizar tema com a origem (quando a página "não fica igual")
- Com o zip da origem: comparar md5 dos arquivos ligados à página de produto (main-product, variant-picker, snippets renderizados, assets) com o destino via `files(filenames:[...]){checksumMd5}`. O que diferir, enviar pelo passo 4.
- Não confiar só em `main-product.liquid`: a diferença costuma estar em snippets de estilo carregados por `snippets/meta-tags.liquid` (ex. `pagina-produto-estilo.liquid` e `pagina-produto-extra.liquid` com `{% render %}` dentro de `if request.page_type == 'product'`). `grep` no zip pelas classes vistas na referência (ex. `jbl-badges`, `envio-cl`) para achar quem estiliza.
- Diferença em `main-product.liquid` pode ser só reescrita automática da Shopify (comentário "This file has been rewritten…"), sem efeito visual.
- App de COD diferente da origem (ex. Releasit em vez de buy_buttons nativo): se o CSS da origem colocar o botão no lugar errado, ajustar com regra no bloco do card de envio, ex. `@media (max-width:749px){product-info.product__info-container>.shopify-app-block[class*="rsi-app"]{order:4}}`.

## 6. Verificação final (obrigatória)
- Na loja destino (via JS + print): textos do país, nada da origem, sem "Agotado", sem imagem quebrada, logos carregados, sem rolagem horizontal, fonte do título/preço e ordem dos blocos iguais à referência.
- Abrir o formulário do app COD com uma oferta selecionada e conferir o preço (fechar sem enviar).
- Conferir também outro produto que use o mesmo `main-product`.
- Mandar prints do celular origem × destino (SendUserFile) e listar o que ficou diferente. Em lote, a tabela da seção "Lote".

## Cards de envio por país
O card de envio é o bloco da página com "Envío a todo <País>" e as logos das transportadoras. Padrão visual: logos em cards brancos com borda `#E3E5E8` e logo `height:34px;width:auto;max-width:90%`. Logo branco/transparente → card com fundo `#1E2328` (classe modificadora). Se faltar arte, gerar no Flora com o print das logos como referência (avisar custo, ~US$0,18 Nano Banana Pro) e subir em Arquivos com `fileCreate`.
Na primeira clonagem de cada país, colar aqui o HTML final do bloco e as URLs das logos em Arquivos, para reaproveitar sem refazer:
- **Chile (chileverificada):** preencher com o bloco `envio-cl` da origem.
- **Guatemala:** preencher.
- **México:** preencher.
- **Colômbia:** preencher.

## Armadilhas já vividas
- Economizar tokens: nunca puxar arquivo grande do tema para o contexto; grep/diff no sandbox e ler só o necessário. Em lote, nunca reler o mesmo arquivo do tema para cada produto: ler uma vez, guardar no sandbox.
- `themeFilesUpsert` só grava arquivos; não cria, publica nem apaga tema. Qualquer coisa além disso é proibida por esta skill.
- Em erro de Liquid/JSON, reverter para o conteúdo original guardado e mostrar o erro.

## Anexo: método pelo Chrome (plano C)
A extensão do Chrome NÃO funciona em páginas claude.ai (artifact); não usar artifact como fonte de cópia. Botão de copiar injetado na aba do admin da loja destino (`admin.shopify.com/store/<id>/themes/<themeId>`, editor de código estilo VS Code):
1. Montar o conteúdo via `javascript_tool` na aba do admin: arquivo existente → `fetch('/store/<id>/themes/<themeId>/assets.json?asset%5Bkey%5D=<key>',{credentials:'include'})` → `.asset.value` e aplicar a troca em JS; arquivo novo → gzip+base64 e `DecompressionStream('gzip')`; arquivo grande nos dois lados → só o patch.
2. Botão fixo no topo com `navigator.clipboard.writeText(conteudo)` que muda para "COPIADO"; clicar com clique real e CONFERIR via JS antes de colar.
3. No editor: clicar no texto, Ctrl+P → caminho (ex. `sections/main-product.liquid`) → Enter. Arquivo novo: abrir um da pasta e usar "Novo arquivo" no Explorer, digitar o nome, Enter.
4. Clicar no texto → Ctrl+A → Ctrl+V → conferir pelo zoom → só então Ctrl+S. Conferir md5/size pelo MCP (arquivo novo pelo editor pode sair com CRLF: checksum diferente, conteúdo igual).
- Editor não responde / prints velhos: `document.visibilityState` = "hidden"; pedir para deixar o Chrome na frente com a aba do admin selecionada e não usar o PC durante a colagem.
- Ele copiar algo no PC troca a área de transferência: conferir o colado antes de Ctrl+S; se colou errado, Ctrl+Z e não salvar; se já salvou, Ctrl+Z + Ctrl+S e conferir o checksum original.
- Atalho com foco fora do editor abre "Adicionar página": fechar sem salvar e conferir com `pages(first:5)`.
- Coordenadas: usar o frame do screenshot atual; se a janela mudar, refazer o screenshot. Não usar "substituir tudo".