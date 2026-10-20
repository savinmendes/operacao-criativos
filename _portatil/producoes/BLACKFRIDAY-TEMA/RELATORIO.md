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
- **Página inicial:** ~~banner em HTML/texto~~ → **banner em imagem** (atualizado em 09/10, ver seção "Banner em imagem" abaixo). Clique leva a `/collections/perfumes-arabes`.
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

1. ~~Link do botão para `/collections/all`~~: resolvido. O banner agora leva a `/collections/perfumes-arabes` (coleção ativa, 3 produtos). Para trocar, edite só a linha `bf_banner_link` no topo do snippet.
2. Como a coleção não mostra cards e a home também não tem grade de produtos, **o selo "BLACK FRIDAY" nos cards não pôde ser visto funcionando**. O código fica pronto para quando houver grade.
3. **Coisas que já existiam no tema** (não foram criadas por mim, mas vale conferir se continuam verdadeiras): "MÁS VENDIDO EN CHILE 2026", "+10.000 CHILENOS SATISFECHOS", "HASTA 12 CUOTAS SIN INTERÉS", o selo "Solo hoy · <data do dia>" e os preços riscados ("AHORRA $10,000") na página de produto.
4. Erro antigo no tema (também no ao vivo): `Liquid error (layout/theme line 53): invalid url input`, que aparece no HTML. Não foi causado por esta mudança.
5. "Stock limitado / últimas unidades" vem do pedido do dono (liquidação de estoque). Se algum produto tiver reposição contínua, avalie tirar essa frase.

## Próximo passo

O dono abre a pré-visualização, confere o item 1 (link do botão) e publica a cópia em **Shopify admin → Loja virtual → Temas → "BLACK FRIDAY - shr-co v4 (rascunho)" → Publicar**.

## Banner em imagem (atualização 09/10/2026)

O dono achou o banner em HTML feio. Foi feito um estudo rápido (`ESTUDO-BANNERS.md`) e o banner virou imagem gerada no Flora.

- **Conceito escolhido:** "A" — wordmark BLACK FRIDAY dourado gigante à esquerda, "LIQUIDACIÓN DE STOCK", selo "Stock limitado", botão "VER OFERTAS", 3 selos verdadeiros no rodapé e produtos genéricos (2 perfumes sem rótulo, caixa de presente, aspiradora sem marca) num pedestal à direita. Os outros dois conceitos (B só tipografia, C produtos à esquerda com confete) ficaram em `banners/conceitos/`.
- **Arquivos finais** (2K, Nano Banana 2), em `banners/` e no Shopify (Conteúdo → Arquivos):
  - Computador 21:9 (3168×1344): https://cdn.shopify.com/s/files/1/0699/7282/0224/files/2026-10_cod_banner_black-friday-desktop.jpg?v=1791579131
  - Celular 1:1 (2048×2048): https://cdn.shopify.com/s/files/1/0699/7282/0224/files/2026-10_cod_banner_black-friday-mobile.jpg?v=1791579131
- **Projeto Flora:** https://app.flora.ai/projects/ns74xg21q4fnxdr9j3dt7zybqn8fy9dy
- **Custo real:** US$ 0,432 (3 conceitos 1K × 0,072 + 2 finais 2K × 0,108). Nenhuma nova tentativa foi necessária.
- **Código:** em `snippets/bf-black-friday.liquid` o bloco da home virou `<picture>` (fonte de celular até 749 px, fonte de computador acima), com `width/height` (sem salto de layout), `loading="eager"` + `fetchpriority="high"` (é o LCP), `srcset` com larguras do CDN e texto alternativo em espanhol. Tudo dentro de um link. No topo do snippet ficam 3 variáveis: `bf_banner_link` (destino do clique), `bf_img_desktop` e `bf_img_mobile`. `bf_activo` continua desligando tudo. A barra rolante e a faixa da página de produto não mudaram.
- **Backup:** `backup/snippets__bf-black-friday_v1-banner-html.liquid` (versão anterior, md5 `bb18432…`). Versão nova em `novos/` (md5 `ed6e1d1f…`, igual ao tema).
- **Prints:** `preview_home_banner-imagem_desktop.png`, `preview_home_banner-imagem_mobile.png`, `preview_clique-banner_{desktop,mobile}.png` (destino do clique).

### Pontos de atenção do banner
- No celular, os 3 selos do rodapé da imagem ficam pequenos (~8 px de altura de letra). Eles são repetidos na barra rolante, então não se perdem, mas não dá para aumentar sem gerar outra imagem.
- O banner mostra perfumes **e uma aspiradora**, mas o clique vai para a coleção de perfumes. Se o destino ficar só perfumes, vale gerar uma versão só com perfumes (~US$ 0,22) ou apontar para uma coleção mista.
- O texto da imagem não é editável pelo editor do tema: qualquer mudança de frase exige gerar outra imagem.
