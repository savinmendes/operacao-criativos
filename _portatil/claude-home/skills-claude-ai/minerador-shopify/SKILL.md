---
name: "minerador-shopify"
description: "Pesquisa COMPLETA de mercado (produtos, lojas, marcas, países, anúncios) com WinningHunter + DropKiller + Minerador, com protocolo anti-pesquisa-rasa e links da Ad Library que funcionam."
---

# Minerador Shopify — pesquisa completa, nunca rasa

Use para: produtos que escalam num país, maiores lojas/marcas de um nicho, loja por trás
de um print/valor, país análogo (demanda sem dono), países que mais consomem um nicho,
links da Ad Library das maiores. Complementa benchmarking-mercado, espiao-de-funil e
dissecacao-de-criativo.

**Regra-mãe:** nenhuma afirmação de "maiores", "não existe", "é o único" ou "top" sem
passar pelo Protocolo de Varredura Completa (§2) e pela Autoauditoria (§9). Se a varredura
não saturou, a resposta diz "parcial" e o que falta — nunca apresenta parcial como final.

---

## 1. Erros que NÃO podem se repetir (aconteceram de verdade)

| Erro | Regra |
|---|---|
| Chamar de "maiores" o resultado de 1 página (20 anúncios) de 1 palavra num só país | Varredura mínima do §2 antes de ranquear |
| Usar 1 ferramenta tendo 3 (WinningHunter, DropKiller, Minerador) | Toda pesquisa de ranking usa as 3 fontes (§2.1) |
| Link da Ad Library com `view_all_page_id` do WinningHunter abrindo marca errada | Só links por `q=<marca>` ou `?id=<anúncio>` (§8) |
| Ruído de palavra ("watch" = "watch what happens"; "knife" = "knie") entrando no ranking | Filtro local por regex + categoria em todo resultado (§3) |
| Filtro de preço "US$ 120" deixando passar DKK/PLN | Conferir `shopify_currency` sempre |
| Concluir "não existe" porque uma base voltou vazia (TikTok Shop GHK-Cu) | Vazio de 1 base = "sem dado nessa base", buscar nas outras |
| Listar a marca do próprio usuário como concorrente | Checar memória/perfil e marcar "(sua)" |
| Faturamento estimado apresentado como fato | Priorizar anúncios ativos, crescimento, visitas; rotular estimativa |
| Mercado subestimado por viés da amostra (Emirados, Ásia) | Busca dedicada por país antes de excluir (§6) |
| Ficar tentando ferramenta que falha | Máx. 1 alternativa; falhou → parar e avisar |

---

## 2. Protocolo de Varredura Completa (obrigatório para ranking)

### 2.1 Fontes — as três, sempre
- **WinningHunter**: `search_facebook_ads`, `find_winning_products`, `search_shopify_stores`,
  `get_store_details`, TikTok (`search_tiktok_*`).
- **DropKiller**: `search_ads` (com `countryCodes` + `distinctAdvertisers`), `search_stores`
  (`sort=activeAds|activeImageAds`), `search_ad_publishers`, `get_store`.
- **Minerador**: `listar_oportunidades`/`consultar_banco` (já minerado antes?),
  `presenca_meta_paises`, `google_trends_*`, `raiox_*`, `puxar_top_criativos`,
  `fornecedor_por_imagem` (custo). Ferramentas pagas: avisar custo antes.

### 2.2 Termos — matriz, não 1 palavra
Monte e execute a matriz antes de começar:
- Sinônimos e variações (ex.: watch, watches, timepiece, chronograph, automatic watch, luxury watch).
- Idiomas dos países-alvo (EN, ES "reloj", PT "relógio", FR "montre", DE "Uhr", IT "orologio", AR "ساعة").
- Nome de produto + nome de domínio quando houver marca.

### 2.3 Países — cobrir os relevantes
- EUA + anglos (GB, CA, AU, NZ) + Europa (FR, DE, IT, ES, NL, nórdicos) + Oriente Médio
  (AE, SA) + LATAM (MX, CO, CL, BR, AR) + os mercados do usuário.
- WinningHunter Meta não tem MX/CO/CL → usar `store_based_in` ou DropKiller `countryCodes`.

### 2.4 Profundidade — paginar até saturar
- Paginar com `scroll` (WinningHunter) / `cursor` (DropKiller) até **2 páginas seguidas
  sem anunciante novo** relevante, ou no mínimo 3 páginas por consulta-chave.
- Ordenar por quantidade de anúncios da página (`sort_by=pageactiveads`) E por gasto/crescimento
  — os dois rankings, porque medem coisas diferentes.
- Usar `distinctAdvertisers:true` na DropKiller para ranquear anunciantes, não anúncios.

### 2.5 Validação cruzada
- Cada nome do top precisa aparecer em ≥ 2 fontes OU ter loja/anúncio aberto e confirmado
  (WebFetch da página, `get_store_details`, `get_ad`).
- Conferir que o produto é do nicho certo (pulseira de Apple Watch ≠ relógio).

### 2.6 Registro de cobertura (vai na resposta)
Tabela curta: fonte × termos × países × páginas × resultados úteis. Se algo não pôde rodar
(timeout, 403, vazio), aparece ali com o motivo.

---

## 3. Higiene dos dados

**Saídas grandes** são salvas em arquivo: nunca ler inteiro; agregar com Python
(`python3 -I script.py arquivo`), script salvo no scratchpad e reutilizado:

```python
import json,sys,re
from urllib.parse import urlparse
NICHO=re.compile(sys.argv[2],re.I)          # ex.: 'watch|reloj|rel[oó]gio|montre|uhr'
EXCL=re.compile(sys.argv[3],re.I) if len(sys.argv)>3 else None  # ex.: 'band|strap|cable'
d=json.load(open(sys.argv[1])); agg={}
for a in d.get('data',[]):
  txt=' '.join(str(a.get(k) or '') for k in ('product_url','urlStore','caption','copy','title','copyPreview','landingUrl'))
  if not NICHO.search(txt) or (EXCL and EXCL.search(txt)): continue
  dom=urlparse(a.get('product_url') or a.get('urlStore') or a.get('landingUrl') or '').netloc
  cur=a.get('shopify_currency'); cur=cur.get('active') if isinstance(cur,dict) else ''
  g=agg.setdefault(dom,{'page':a.get('pageName') or a.get('advertiserName'),'n':0,'spend':0,
    'active':a.get('total_active_ads_on_page'),'g1m':a.get('total_active_ads_on_page_growth_1m'),
    'price':a.get('shopify_productprice'),'cur':cur,'fmt':set(),
    'ad':a.get('productid') or a.get('externalId'),'ctry':a.get('countries')})
  g['n']+=1; g['spend']+=a.get('total_eu_adspend') or 0; g['fmt'].add(a.get('display_format') or a.get('mediaType'))
for dom,g in sorted(agg.items(),key=lambda x:-(x[1]['active'] or 0)): print(dom,g)
```

- `min_price`/`max_price` são na moeda da loja → converter/descartar.
- `total_eu_adspend` = estimativa só Europa. Faturamento de loja = estimativa fraca.
- `searchkeyword="productname"` no WinningHunter para cortar ruído de copy.
- Busca de lojas por keyword no WinningHunter é ruidosa → filtrar por `category_v2_l3`.
- `product_taxonomy_l*` só com valor exato de `list_shopify_store_filter_options`; vazio → seguir com filtro local.
- DropKiller `search_ads` sem `countryCodes` dá timeout.

---

## 4. Tipo A — produtos que escalam num país
1. Varredura §2 com `find_winning_products` + DropKiller `find_winning_products`/`search_ads` no país.
2. Separar marca própria × drop. Para drop: custo provável (`fornecedor_por_imagem`),
   frete/peso, margem alta/média/apertada.
3. Destacar crescimento de anúncios no mês (escalando agora).

## 5. Tipo C — loja por trás de print/valor
- Converter valor (ex.: R$ 938 ≈ US$ 190 → checkout em USD).
- Buscar pela assinatura (gancho, formato, faixa de preço, últimos dias) nas 3 fontes.
- Confirmar candidato abrindo a página (WebFetch) e comparando produto/preço/kit com a foto.
- Sem confirmação → dizer "candidatos prováveis" e pedir domínio/anúncio.

## 6. Tipo D/E — países (análogo ou maiores consumidores)
- Demanda: Minerador `google_trends_iniciar` (≤10 países; avisar ~US$ 0,13/país) → esperar com
  `sleep` → `google_trends_coletar`. Trends é relativo por país. Ler "buscas em alta".
- Concorrência: `presenca_meta_paises` → `contar_resultado_paises`; comparar anunciantes
  (local × estrangeiro), pois o limite satura.
- Consumo: agregar `top_countries` × visitas das lojas do nicho + países de segmentação dos anúncios.
- **Rodar busca dedicada** para AE, SA, HK, JP, SG e LATAM antes de concluir que são pequenos
  (`visitor_country_main`, `country`, DropKiller `countryCodes`).

## 7. Tipo B — maiores lojas/marcas
Varredura §2 completa + tabela com: marca, anúncios ativos (+1m), formato (imagem/vídeo),
perfil (marca/drop/varejo), países, visitas, link. Lista separada de vizinhos/descartados e por quê.

## 8. Links da Ad Library — só estes formatos
- Marca (todos): `https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q=<marca>&search_type=keyword_unordered`
- Só ativos: trocar para `active_status=active`. Vazio → separar palavras com `%20`.
- Anúncio: `https://www.facebook.com/ads/library/?id=<id do anúncio>`
- NUNCA `view_all_page_id` com page_id do WinningHunter; nunca `media_type` na URL.
- "Por extenso" = bloco de código, um link por marca.

## 9. Autoauditoria antes de responder (checar item a item)
- [ ] Usei as 3 fontes?
- [ ] Rodei a matriz de termos e idiomas?
- [ ] Cobri os países relevantes, incluindo os subestimados?
- [ ] Paginei até saturar (2 páginas sem novidade)?
- [ ] Filtrei ruído, moeda e nicho vizinho?
- [ ] Cada nome do top foi confirmado em 2 fontes ou aberto?
- [ ] Marquei as marcas do usuário como "(sua)"?
- [ ] Links no formato §8?
- [ ] Rotulei estimativas e escrevi os limites?
- [ ] Se algo ficou parcial, a resposta diz "parcial" e o que falta?
Qualquer "não" → voltar e completar antes de entregar.

## 10. Bandeiras vermelhas (sinalizar, não replicar)
- "Closing sale" falso, história de artesão inventada, "Made in Japan" em produto chinês,
  preço "de" inventado → estorno e retenção/banimento no processador.
- Réplica de marca de luxo → não ajudar; propor marca própria com estética premium.
- Saúde: promessa terapêutica; peptídeo injetável misturado a cosmético.
- Print de "venda aprovada" ≠ lucro.
Mostrar sempre a versão honesta da estrutura que funciona.

## 11. Formato de entrega
1. Registro de cobertura (§2.6) em 3–5 linhas.
2. Tabela principal com links.
3. Vizinhos/descartados e motivo.
4. "O que isso mostra" — 3–4 bullets acionáveis para a operação (COD/cartão/país).
5. Limites honestos. Fontes web quando houver.
Português do Brasil, direto, sem recapitular passos. Custo de ferramenta paga informado antes.