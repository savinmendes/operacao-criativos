---
name: "mineracao-infoproduto-escalado"
description: "Varre a Ad Library do Meta e devolve as páginas de infoproduto que estão realmente escalando, ranqueadas por assinatura de escala. Use para minerar infoprodutos escalados, achar ofertas rodando ou mapear quem está gastando num nicho."
---

# Mineração de infoproduto escalado

Acha, na Ad Library do Meta, quem está de fato queimando verba num nicho — não quem tem um anúncio bonito. Entrega ranking no chat com snapshot URLs prontos pra inspeção.

**Escopo:** infoproduto, multi-país (BR, LATAM, Europa). Oferta COD física não é alvo desta skill.

## Princípio

Não se procura "anúncio bom". Procura-se **assinatura de escala** — três rastros que aparecem juntos em toda operação que está gastando de verdade:

1. **Duplicação de ad ID** — múltiplos anúncios com o mesmo `ad_creative_link_title` da mesma `page_id`, criados na mesma janela de segundos. É CBO duplicado / Advantage+ multiplicando estrutura. Uma página com 1 criativo excelente é teste; com 15 cópias do mesmo criativo é verba rodando.
2. **Longevidade** — criativo ativo há 30+ dias em resposta direta é matemática, não sorte.
3. **Rotação contínua** — sobe criativo novo toda semana e mantém os antigos no ar. Quem escala nunca para a esteira.

Os três juntos. Um sozinho é ruído.

## Entradas

Antes de rodar, é preciso ter: **nicho** e **país(es)**. Se o usuário não deu, pergunte — uma vez, curto. Opcionais: janela de tempo, idioma se diferente do país, páginas já conhecidas para excluir.

## Passo 1 — Varredura por rastro estrutural

Busque pela **estrutura do funil**, nunca pelo nome do nicho. Nicho traz e-commerce, marca e conteúdo orgânico; estrutura traz só infoproduto rodando.

Use `mcp__Meta_Ads_Co__ads_library_search` com:
- `countries`: ISO-2 do(s) mercado(s)
- `ad_active_status`: `ACTIVE` (sempre — inativo não é escala)
- `limit`: 50 (máximo)
- `client_conversation_id`: mesmo id de 20 caracteres em todas as chamadas da conversa
- `client_model` e `advertiser_request`: conforme a spec do tool

**Dispare 4 a 6 buscas em paralelo**, variando `search_terms`, misturando termos de captura com o nicho. Um termo só devolve uma fatia enviesada.

### Dicionário de captura por idioma

| Idioma | Termos de alta densidade |
|---|---|
| PT-BR | aula gratuita, evento online, masterclass, método, desafio de X dias, últimas vagas, turma fechando, passo a passo, mentoria, do zero |
| ES (LATAM/ES) | clase gratuita, masterclass, evento en vivo, método, reto de X días, últimos cupos, paso a paso, desde cero |
| RO | lecție gratuită, webinar, metodă, curs online, locuri limitate, pas cu pas |
| HU | ingyenes képzés, webinár, módszer, online tanfolyam, korlátozott helyek |
| EN | free training, free masterclass, live workshop, proven method, X-day challenge, doors closing, step by step |

### Rastro de checkout (confirmação, não busca)

Usado no Passo 3 pra confirmar que é infoproduto:
- **BR:** hotmart, kiwify, ticto, cakto, kirvano, payt, braip, monetizze, eduzz, greenn
- **LATAM/ES:** hotmart, kiwify, ticto, thrivecart
- **Europa/global:** thrivecart, samcart, stripe checkout, clickfunnels, systeme.io, kajabi, digistore24

## Passo 2 — Agregação e score

Junte os resultados de todas as buscas e agregue **por `page_id`** (nunca por anúncio). Para cada página calcule:

- `n_ads` — total de anúncios ativos capturados
- `n_criativos` — `ad_creative_link_title` distintos
- `densidade_dup` = `n_ads / n_criativos` → quantas cópias por criativo
- `janela_criacao` — spread de `ad_creation_time` dentro de cada grupo de título idêntico. Segundos ou minutos = duplicação programática de estrutura. Dias = subida manual, sinal fraco.
- `dias_no_ar` = `(agora − min(ad_delivery_start_time)) / 86400`, usando o anúncio **mais antigo ainda ativo** da página. Os timestamps são unix epoch.

**Classificação:**

| Faixa | Critério |
|---|---|
| 🔴 Escalando | `densidade_dup` ≥ 5 **e** `dias_no_ar` ≥ 21 **e** ≥ 2 criativos distintos |
| 🟡 Validando | `densidade_dup` ≥ 3 **ou** `dias_no_ar` ≥ 30, mas não os dois |
| ⚪ Testando | resto — descarte, salvo pedido explícito |

## Passo 3 — Aprofundar os candidatos

Só para os 🔴 e 🟡 (normalmente 5 a 15 páginas). Rechame o tool com `page_ids` da página **sem `search_terms`**, pra puxar o inventário completo — a varredura do Passo 1 só viu o que casou com o termo.

Com o inventário completo, recalcule o score e confirme:
- É infoproduto mesmo? Cheque o destino/checkout contra a lista acima.
- É produtor ou afiliado? Página com nome pessoal + criativo único replicado = geralmente produtor. Muitas páginas diferentes com o mesmo criativo = rede de afiliados sobre uma oferta só — nesse caso o alvo real é a **oferta**, não a página.
- **Lançamento ou perpétuo?** Pico de duplicação em janela curta com termos de escassez ("últimas vagas", "turma fechando") = lançamento. Volume estável por 60+ dias = perpétuo. Isso muda completamente o que é copiável: no lançamento, a mecânica de escassez carrega o resultado, não o hook.

## Passo 4 — Entrega

Ranking no chat, ordenado por classificação e depois por `dias_no_ar`. Uma linha por página:

```
🔴 [Nome da Página] — 23 ads / 3 criativos (7,7x) · 47 dias no ar · Kiwify
   Ângulo dominante: "<ad_creative_link_title mais replicado>"
   Snapshot: https://www.facebook.com/ads/library/?id=<id>
```

Inclua sempre pelo menos um `ad_snapshot_url` por página — sem ele o usuário não consegue inspecionar visualmente. Feche com um parágrafo curto de leitura do leilão: quantos players 🔴, qual ângulo se repete entre eles, qual fatia está descoberta.

## Encaminhamento

Esta skill é o filtro de topo. Depois dela, ofereça o próximo passo (não execute sem confirmação):
- `benchmarking-mercado` — mapa completo do leilão do nicho e fatias livres
- `espiao-de-funil` — reconstruir a operação inteira de UM candidato 🔴
- `dissecacao-de-criativo` — destrinchar os anúncios mais replicados em ângulo, avatar, formato e hook

## Armadilhas — dizer ao usuário, não esconder

- **Nº de anúncios ativos ≠ verba.** 40 ads duplicados a R$ 20/dia é R$ 800/dia, não R$ 50 mil. A assinatura prova *estrutura de escala*, não volume de investimento. Nunca apresente contagem de ads como estimativa de faturamento.
- **A Ad Library só mostra o que está ativo agora.** Criativo campeão já derrubado é invisível aqui. Para histórico, só ferramenta paga com biblioteca própria.
- **Copiar criativo de lançamento sem a mecânica não transfere resultado.** Diga isso quando o candidato for lançamento.
- **O tool exige conta de anúncios ativa.** Se retornar erro de permissão, é isso — não insista com variações da chamada.