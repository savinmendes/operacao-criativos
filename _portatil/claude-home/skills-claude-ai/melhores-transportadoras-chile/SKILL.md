---
name: "melhores-transportadoras-chile"
description: "Ranqueia as transportadoras da loja Chile (Dropi) pela efetividade recente por região e comuna e entrega a lista de preferências para configurar na Dropi."
---

# Melhores transportadoras — Loja Chile

Responder em português do Brasil, direto, sem pedir permissão para leituras ("apenas faça"). Economizar tokens: só consultas agregadas, saída curta.

Fonte: banco Chegou Operações (MCP Dropi), operação `drop`, tabela `metricas_dropi_dropipedido`, `pais='chile'`, lojas `dados->'shop'->>'name' IN ('Tienda Tuya','Nicochat - Shopify')`. Chamar `mapa_dos_dados('drop')` uma vez antes da primeira consulta da sessão.

## Definições (não mudar sem o Savin pedir)

- **Janela:** pedidos criados entre **60 e 7 dias atrás** (os dos últimos 7 dias ainda estão em trânsito). Mostrar sempre duas colunas lado a lado: **60 dias** (volume) e **últimos 30 dias** (tendência, de 30 a 7 dias atrás).
- **Classe do pedido:**
  - cancelado = `CANCELADO`, `CERRADO CON PROBLEMA CONTACTAR CON EJECUTIVO` → fora da conta;
  - devolvido = status de devolução (`DEVOLUCION`, `DEVOLUCION A REMITENTE`, `DEVOLUCION EN BODEGA`, `EN DEVOLUCION`, `PARA DEVOLUCION`, `RECHAZADO`, `REHUZA PRODUCTO`) **ou qualquer pedido que já teve NOVEDAD** (`status LIKE 'NOVEDAD%'` ou `dados->>'novedad_servientrega'` não nulo);
  - entregue = `ENTREGADO` sem novedad;
  - resto = em trânsito.
- **Efetividade** = entregues ÷ (entregues + devolvidos). Dizer sempre que é efetividade de finalizados com novedad contando como devolvido.
- **Amostra mínima:** 15 finalizados por transportadora no recorte. Entre 15 e 30, marcar como "amostra fraca".
- **Atual** de uma região ou comuna = transportadora com mais pedidos nos últimos 7 dias nela.

## Qual coluna decide

- Padrão: decidir pela de **60 dias**.
- Usar a de **30 dias** quando:
  - uma das transportadoras quase não rodou na primeira metade da janela (mais de 80% dos finalizados dela estão nos últimos 30 dias) — senão a comparação é de períodos diferentes;
  - ou a efetividade de 30 dias de uma transportadora difere 10 pontos ou mais da de 60 (piorou ou melhorou recentemente).
- Dizer na tabela qual coluna decidiu cada linha.

## Passos

1. **Visão geral do país:** por transportadora → finalizados, efetividade 60d e 30d, em trânsito.
2. **Por região** (`state`): consulta-base abaixo.
3. **Região Metropolitana por comuna** (`city` onde `state` = `METROPOLITANA DE SANTIAGO`): mesma consulta agrupando por `city`. Também por comuna em Valparaíso e Biobío se tiver amostra.
4. **Travados:** por transportadora, % de pedidos com 7–60 dias ainda em `PENDIENTE`, `PREPARADO PARA TRANSPORTADORA`, `GUIA_GENERADA` ou `NOVEDAD SOLUCIONADA`. Acima de 10% é sinal de problema operacional: avisar mesmo que a efetividade pareça boa.
5. **Atual:** transportadora dominante dos últimos 7 dias por região/comuna.
6. **Decisão** por região ou comuna (na coluna que decide):
   - trocar só se a melhor tiver amostra mínima e ganhar da atual por **5 pontos ou mais**;
   - diferença menor que 5 pontos ou amostra insuficiente → manter a atual;
   - comuna sem amostra herda a decisão da região;
   - transportadora com efetividade abaixo de 30% e amostra mínima → recomendar tirar da região;
   - empate técnico → preferir a com menos travados.
7. **Entregar:**
   - tabela curta: região/comuna | atual | recomendada | efet. 60d e 30d de cada | amostra | coluna que decidiu | ação (TROCAR / MANTER / TIRAR);
   - **lista completa e exata das mudanças** para o Savin aplicar em Dropi → Transportadora → Preferencias (região, comuna, transportadora), tudo de uma vez;
   - 1–2 linhas sobre o que mudou desde a última análise, se houver uma na conversa ou na memória.

## Consulta-base (PostgreSQL)

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
 WHERE pais='chile' AND dados->'shop'->>'name' IN ('Tienda Tuya','Nicochat - Shopify')
   AND created_at_dropi >= now() - interval '60 days'
   AND created_at_dropi <  now() - interval '7 days')
SELECT reg, tr,
 SUM((cl IN ('e','d'))::int) fin60,
 ROUND(100.0*SUM((cl='e')::int)/NULLIF(SUM((cl IN ('e','d'))::int),0),1) efet60,
 SUM((cl IN ('e','d') AND rec)::int) fin30,
 ROUND(100.0*SUM((cl='e' AND rec)::int)/NULLIF(SUM((cl IN ('e','d') AND rec)::int),0),1) efet30
FROM b WHERE cl<>'c'
GROUP BY 1,2 HAVING SUM((cl IN ('e','d'))::int) >= 15
ORDER BY 1, efet60 DESC
```

Para comuna: trocar `reg` por `cid` no SELECT/GROUP BY e filtrar a região. Para recorte por produto: adicionar `product_name` (só quando o Savin pedir ou quando um produto destoar muito).

## Limites

- Mudar a preferência na Dropi é com o Savin: entregar a lista pronta, não alterar a configuração.
- Nunca digitar credenciais.
- Status fora da lista conhecida → contar à parte e avisar, sem encaixar por semelhança.
- Não inventar números: tudo vem da consulta. O banco não tem os pedidos de hoje.
- Se o Savin pedir para salvar a decisão, registrar na memória `/areas/processamento-pedidos-cod.md` (preferências vigentes por região e data).