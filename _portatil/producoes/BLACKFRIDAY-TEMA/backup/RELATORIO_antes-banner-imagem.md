# Black Friday · Liquidación de stock — chileverificada.com

Data: 09/10/2026 · Frente: COD Chile

## O que foi feito

1. O tema principal **"shr-co PAGINA v4 (cores teste)"** (`166882672896`, MAIN) foi **duplicado** com `themeDuplicate`. O tema ao vivo **não foi alterado** (checksum do `header-group.json` continua `3795e2f4…`).
2. Cópia criada: **"BLACK FRIDAY - shr-co v4 (rascunho)"**, id `167232798976`, **NÃO publicada** (Draft).
3. Pré-visualização: **https://chileverificada.com/?preview_theme_id=167232798976**
   - Produto (exemplo): https://chileverificada.com/products/mopah2o?preview_theme_id=167232798976

## Arquivos alterados no tema cópia (só 2)

| Arquivo | Tipo | O que mudou |
|---|---|---|
| `snippets/bf-black-friday.liquid` | **NOVO** | Contém todo o Black Friday: itens da barra, banner da home, faixa no produto e selo nos cards. Tem o interruptor `bf_activo`. |
| `sections/header-group.json` | Editado | Na seção `custom_liquid_6iyBPK` (a barra preta rolante): 2× `{% render 'bf-black-friday', modo: 'marquee' %}` (um em cada bloco da animação, logo depois de "⏱️ ENTREGA EN 24-72H") + 1× `{% render 'bf-black-friday' %}` no final. Nenhum texto existente foi removido. |

Nenhum template de produto (`templates/product*.json`), `index.json`, `main-product.liquid` ou `settings_data.json` foi tocado: o snippet é carregado pelo grupo do cabeçalho, que aparece em todas as páginas, e por isso vale para **todos** os templates de produto sem editar cada um.

## O que aparece na loja (texto em espanhol do Chile)

- **Barra preta rolante:** as mensagens atuais continuam e entram mais 3 depois delas:
  - "🖤 BLACK FRIDAY · LIQUIDACIÓN DE STOCK" (dourado)
  - "🔥 STOCK LIMITADO — ÚLTIMAS UNIDADES DE LA TEMPORADA" (dourado)
  - "💵 PAGAS AL RECIBIR"
- **Página inicial:** um banner preto e dourado logo abaixo da barra: selo "BLACK FRIDAY", título "LIQUIDACIÓN DE STOCK", subtítulo "Stock limitado — últimas unidades de la temporada.", três selos ("Despacho gratis a todo Chile", "Pagas al recibir", "Entrega en 24-72h") e o botão "VER PRODUCTOS EN LIQUIDACIÓN" (`/collections/all`).
- **Todas as páginas de produto:** uma faixa preta e dourada logo acima do título, com "🖤 BLACK FRIDAY · LIQUIDACIÓN DE STOCK — Unidades limitadas". Testei em 3 produtos (mopah2o, enzimas, bissel-furfinder), no celular e no computador.
- **Cards de produto** (grades e coleções): um selo "BLACK FRIDAY" no canto superior esquerdo da imagem. Ele só aparece onde o tema mostra cards `.card-wrapper` (veja os pontos de atenção).

**O que ficou de fora de propósito:** número de unidades restantes, preço "de/por" novo, avaliações e contador regressivo. Não havia data real de fim da liquidação, e o Black Friday de 2026 cai em 27/11/2026, uma data que não serve como fim da oferta. Nenhum preço ou produto foi mexido.

## Como desfazer

- **Desligar tudo de uma vez (mais rápido):** no tema, Editar código → `snippets/bf-black-friday.liquid` → troque `{%- assign bf_activo = true -%}` por `false`. A barra volta exatamente ao que era.
- **Remover de vez:** apague as 3 linhas `{% render 'bf-black-friday' ... %}` do Liquid personalizado da barra (Personalizar → Cabeçalho → seção Liquid personalizado) ou restaure `backup/sections__header-group.json`. Depois apague o snippet.
- **Alternativa:** continue usando o tema anterior, que segue intacto, ou republique-o depois da campanha.

## Backups (pasta `backup/`)

- `sections__header-group.json`: conteúdo original (antes da edição). A API devolve o JSON reformatado, mas o conteúdo é idêntico.
- O snippet é um arquivo novo e não tinha original. A versão final dele e do header-group estão em `novos/`.
- Prints da pré-visualização: `preview_home.png`, `preview_home_desktop.png`, `preview_produto_*_{mobile,desktop}.png`.

## Pontos de atenção (revisão manual)

1. **O botão do banner leva a `/collections/all`, e essa página hoje não mostra a grade de produtos** (nem no tema ao vivo: só a barra, o título e o rodapé). Antes de publicar, troque o link do botão no snippet (linha do `<a class="bf-hero__b" href=...>`) para uma coleção ou um produto que funcione, ou arrume o template de coleção.
2. Como a coleção não mostra cards e a home também não tem grade de produtos, **o selo "BLACK FRIDAY" nos cards não pôde ser visto funcionando**. O código fica pronto para quando houver grade.
3. **Coisas que já existiam no tema** (não foram criadas por mim, mas vale conferir se continuam verdadeiras): "MÁS VENDIDO EN CHILE 2026", "+10.000 CHILENOS SATISFECHOS", "HASTA 12 CUOTAS SIN INTERÉS", o selo "Solo hoy · <data do dia>" e os preços riscados ("AHORRA $10,000") na página de produto.
4. Erro antigo no tema (também no ao vivo): `Liquid error (layout/theme line 53): invalid url input`, que aparece no HTML. Não foi causado por esta mudança.
5. "Stock limitado / últimas unidades" vem do pedido do dono (liquidação de estoque). Se algum produto tiver reposição contínua, avalie tirar essa frase.

## Próximo passo

O dono abre a pré-visualização, confere o item 1 (link do botão) e publica a cópia em **Shopify admin → Loja virtual → Temas → "BLACK FRIDAY - shr-co v4 (rascunho)" → Publicar**.
