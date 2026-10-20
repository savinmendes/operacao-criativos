---
name: "melhores-transportadoras-cod"
description: "Ranqueia as transportadoras de qualquer país COD (Dropi ou Ecomhub) pela efetividade recente por região e cidade e entrega a lista de preferências para configurar."
---

# Melhores transportadoras — qualquer país COD

Responder em português do Brasil, direto, sem pedir permissão para leituras ("apenas faça"). Economizar tokens: só consultas agregadas, saída curta.

## 1. Escolher país e fonte

- Se o país não foi dito, perguntar qual (ou rodar todos e entregar um bloco por país, se ele pedir "todos").
- Fonte: banco Chegou Operações (MCP Dropi), operação `drop`. Chamar `mapa_dos_dados('drop')` uma vez antes da primeira consulta da sessão e seguir as regras de leitura de pedidos dele (classes de status, fuso do país).
- **América Latina (Dropi):** `metricas_dropi_dropipedido`, filtro `pais` = `chile`, `colombia`, `mexico`, `guatemala`. Colunas: `state` (região/departamento), `city`, `shipping_company`, `status`, `created_at_dropi`, `product_name`, loja em `dados->'shop'->>'name'`.
- **Europa (Ecomhub):** `pedidos_ecomhub_pedidoecomhub` + `cadastro_drop_pais` (pelo `pais_id`), colunas `transportadora`, `status`, `data_pedido`, `produto_nome`. Não tem região nem cidade: análise só por país e por produto. Transportadora vazia → contar à parte como "sem transportadora".
- **País que não está no banco** (ex.: Equador, Polônia, Rep. Tcheca, Hungria hoje): dizer que o banco não tem esse país e pedir a exportação de pedidos do painel (CSV/Excel com status, transportadora, região, cidade, data). Aplicar as mesmas regras sobre o arquivo.
- **Lojas:** antes de calcular, listar as lojas do país (`GROUP BY dados->'shop'->>'name'`) e incluir só as do Savin. Loja com poucos pedidos e nome estranho → perguntar se entra.
- Na primeira análise de um país novo, checar se existe status fora da lista do mapa e se há campo de novedad no `dados` desse país.

## 2. Definições (não mudar sem o Savin pedir)

- **Janela:** pedidos criados entre **60 e 7 dias atrás** (os dos últimos 7 dias ainda estão em trânsito). Mostrar sempre duas colunas: **60 dias** (volume) e **últimos 30 dias** (de 30 a 7 dias atrás, tendência). Se o país tem prazo de entrega longo (em trânsito acima de 20% na janela), aumentar o corte de 7 para 14 dias e avisar.
- **Classe do pedido** (usar as listas do `mapa_dos_dados`):
  - cancelado → fora da conta;
  - devolvido = status de devolução **ou, na Dropi, qualquer pedido que já teve NOVEDAD** (`status LIKE 'NOVEDAD%'` ou `dados->>'novedad_servientrega'` não nulo); na Ecomhub, `RETURNED`/`RETURNING`;
  - entregue = entregue sem novedad;
  - resto = em trânsito.
- **Efetividade** = entregues ÷ (entregues + devolvidos). Dizer sempre que é efetividade de finalizados, com novedad contando como devolvido na Dropi.
- **Amostra mínima:** 15 finalizados por transportadora no recorte. Entre 15 e 30, marcar "amostra fraca".
- **Atual** de uma região ou cidade = transportadora com mais pedidos nos últimos 7 dias nela.

## 3. Qual coluna decide

- Padrão: **60 dias**.
- Usar **30 dias** quando:
  - uma das transportadoras quase não rodou na primeira metade da janela (mais de 80% dos finalizados dela nos últimos 30 dias) — senão compara períodos diferentes;
  - ou a efetividade de 30 dias de uma transportadora difere 10 pontos ou mais da de 60.
- Dizer em cada linha qual coluna decidiu.

## 4. Passos

1. **Visão geral do país:** por transportadora → finalizados, efetividade 60d e 30d, % em trânsito.
2. **Por região** (`state`) com a consulta-base.
3. **Por cidade** na região da capital e nas 2–3 regiões de maior volume (Chile: Metropolitana por comuna; Colômbia: Bogotá, Antioquia, Valle; México: CDMX/Estado de México; Guatemala: departamento de Guatemala), só onde houver amostra.
4. **Travados:** por transportadora, % de pedidos da janela ainda em `PENDIENTE`, `PREPARADO PARA TRANSPORTADORA`, `GUIA_GENERADA` ou `NOVEDAD SOLUCIONADA` (Ecomhub: `PROCESSING`, `PREPARING_FOR_SHIPPING`, `READY_TO_SHIP`, `ISSUE`). Acima de 10% → avisar mesmo com efetividade boa.
5. **Atual:** transportadora dominante dos últimos 7 dias por região/cidade.
6. **Decisão** (na coluna que decide):
   - trocar só se a melhor tiver amostra mínima e ganhar da atual por **5 pontos ou mais**;
   - diferença menor que 5 pontos ou amostra insuficiente → manter;
   - cidade sem amostra herda a decisão da região; região sem amostra herda a do país;
   - transportadora abaixo de 30% com amostra mínima → recomendar tirar;
   - empate técnico → a com menos travados.
7. **Entregar** (um bloco por país):
   - tabela curta: região/cidade | atual | recomendada | efet. 60d e 30d de cada | amostra | coluna que decidiu | ação (TROCAR / MANTER / TIRAR);
   - **lista completa e exata das mudanças** para o Savin aplicar de uma vez (Dropi: Transportadora → Preferencias, por região/cidade; Ecomhub ou outro painel: onde a preferência fica nele);
   - 1–2 linhas sobre o que mudou desde a última análise daquele país, se houver.

## 5. Consulta-base Dropi (PostgreSQL)

Trocar `:pais` e `:lojas`.

```sql
WITH b AS (
 SELECT upper(state) reg, upper(city) cid, upper(shipping_company) tr,
  created_at_dropi >= now() - interval '30 days' rec,
  CASE WHEN upper(status) IN ('CANCELADO','CERRADO CON PROBLEMA CONTACTAR CON EJECUTIVO') THEN 'c'
       WHEN upper(status)='ENTREGADO' AND dados->>'novedad_servientrega' IS NULL THEN 'e'
       WHEN upper(status) IN ('DEVOLUCION','DEVOLUCION A REMITENTE','DEVOLUCION EN BODEGA','EN DEVOLUCION','PARA DEVOLUCION','RECHAZADO','REHUZA PRODUCTO')
            OR upper(status) LIKE 'NOVEDAD%' OR dados->>'novedad_servientrega' IS NOT NULL THEN 'd'
       ELSE 't' END cl
 FROM metricas_dropi_dropipedido
 WHERE pais = :pais AND dados->'shop'->>'name' IN (:lojas)
   AND created_at_dropi >= now() - interval '60 days'
   AND created_at_dropi <  now() - interval '7 days')
SELECT reg, tr,
 SUM((cl IN ('e','d'))::int) fin60,
 ROUND(100.0*SUM((cl='e')::int)/NULLIF(SUM((cl IN ('e','d'))::int),0),1) efet60,
 SUM((cl IN ('e','d') AND rec)::int) fin30,
 ROUND(100.0*SUM((cl='e' AND rec)::int)/NULLIF(SUM((cl IN ('e','d') AND rec)::int),0),1) efet30,
 SUM((cl='t')::int) transito
FROM b WHERE cl<>'c'
GROUP BY 1,2 HAVING SUM((cl IN ('e','d'))::int) >= 15
ORDER BY 1, efet60 DESC
```

Por cidade: trocar `reg` por `cid` e filtrar a região. Por produto: adicionar `product_name` (só se o Savin pedir ou um produto destoar muito). Status fora da lista → contar à parte e avisar.

## 6. Consulta-base Ecomhub (PostgreSQL)

```sql
SELECT coalesce(nullif(e.transportadora,''),'(sem)') tr,
 SUM((upper(e.status) IN ('DELIVERED','RETURNED','RETURNING'))::int) fin60,
 ROUND(100.0*SUM((upper(e.status)='DELIVERED')::int)/NULLIF(SUM((upper(e.status) IN ('DELIVERED','RETURNED','RETURNING'))::int),0),1) efet60,
 SUM((upper(e.status) IN ('DELIVERED','RETURNED','RETURNING') AND e.data_pedido >= now() - interval '30 days')::int) fin30,
 ROUND(100.0*SUM((upper(e.status)='DELIVERED' AND e.data_pedido >= now() - interval '30 days')::int)/NULLIF(SUM((upper(e.status) IN ('DELIVERED','RETURNED','RETURNING') AND e.data_pedido >= now() - interval '30 days')::int),0),1) efet30
FROM pedidos_ecomhub_pedidoecomhub e JOIN cadastro_drop_pais p ON p.id = e.pais_id
WHERE p.nome = :pais_nome AND upper(e.status) <> 'CANCELLED'
  AND e.data_pedido >= now() - interval '60 days' AND e.data_pedido < now() - interval '7 days'
GROUP BY 1 ORDER BY efet60 DESC
```

## Limites

- Mudar preferência de transportadora nos painéis é com o Savin: entregar a lista pronta, não alterar configuração.
- Nunca digitar credenciais.
- Não inventar números: tudo vem da consulta ou do arquivo. O banco não tem os pedidos de hoje.
- Se o Savin pedir para salvar a decisão, registrar na memória do país/loja (ex.: `/areas/processamento-pedidos-cod.md` no Chile, `/areas/loja-guatemala-shopify.md` na Guatemala), com preferências vigentes por região e data.