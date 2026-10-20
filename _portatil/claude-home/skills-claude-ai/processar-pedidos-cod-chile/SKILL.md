---
name: "processar-pedidos-cod-chile"
description: "Processa os pedidos COD da loja Chile (chileverificada.com): valida, tagueia, confere estoque, envia à Dropi pela Dropify, confirma na Dropi e audita transportadoras. Use para processar/enviar pedidos ou revisar efetividade por transportadora."
---

# Processar pedidos COD — Loja Chile

Responder sempre em português do Brasil, direto, sem pedir permissão para o que é reversível ("apenas faça"). Economizar tokens: consultas agregadas, saídas curtas.

Ferramentas: Shopify Admin GraphQL (MCP), Dropi web (app.dropi.cl via Chrome), banco Chegou Operações (MCP Dropi, operação `drop`, tabela `metricas_dropi_dropipedido`, `pais='chile'`), Talkyria (tags na Shopify).

Antes de começar, ler a memória `/areas/processamento-pedidos-cod.md` (regras vigentes) e `/areas/calculadora-margem.md` (pontos de equilíbrio). Se a memória e esta skill divergirem, vale a memória mais recente.

## Ordem obrigatória

1. **Levantar o ciclo**: pedidos abertos desde o último lote sem "Order sent to dropi" nem tag CANC.
2. **Taguear** cada pedido (regras abaixo).
3. **ESTOQUE (BLOQUEANTE)**: conferir no painel da Dropi o estoque de cada produto/fornecedor do lote. Se não der (sessão expirada), PARAR e pedir para o usuário logar. Nunca enviar sem saber o estoque.
4. **Enviar pela Dropify** (app "Enviar a Dropi" na lista de pedidos da Shopify): só funciona com seleção explícita, até 50 por página; ~10 s por pedido. Usar tag temporária `ENV` para separar o lote e removê-la depois do envio.
5. Tratar `Dropi Sync Error` (ex.: cidade sem COD → ajustar cidade ou taguear `SEM ENTREGA`).
6. **Confirmar na Dropi**: Mis Pedidos → Mostrar 100 → selecionar → Estatus "CONFIRMADO (PASARÁ A PENDIENTE)" → Actualizar. Antes, tirar os que a Talkyria marcou com atenção/cancelamento (tag `RETIDO DROPI`).
7. Relatar: total do ciclo, enviados, confirmados, cancelados, retidos (por motivo, com números dos pedidos).

## Regras de tag e decisão

- Comparar só com pedidos anteriores NÃO cancelados (cancelado na Shopify ou com tag `CANC…`/`CANC DROPI` fica fora). Comparar por telefone (últimos 8–9 dígitos).
- **Oferta = página/título da Shopify**, não o produto da Dropi.
- Mesmo modelo + anterior aberto/em trânsito → `DUPLICADO` → cancelar (`CANC: DUPLICADO`), sem ligar.
- Mesmo modelo + anterior entregue → recompra → `CANC: RECOMPRA`.
- Outro modelo do mesmo tipo (SEMELHANTE):
  - **Câmeras (desde 01/10/2026): igual duplicado → cancelar** (`CANC: SEMELHANTE` / `CANC: SEMELH TRANSITO`), sem ligar.
  - Demais produtos: `SEMELHANTE` / `SEMELH TRANSITO` → ligar (Talkyria) e só enviar com confirmação.
- Histórico do cliente abaixo do corte do produto (~2× ponto de equilíbrio) → `BAIXO RECEBIMENTO`/`ABAIXO PE`. Cliente com até 4 pedidos no histórico envia.
- Endereço sem número/referência → `END INCOMPLETO` (cliente com >60% de entrega e referência não é cancelado).
- Comunas de risco/sem entrega → só taguear (`COMUNA RISCO`, `SEM ENTREGA`).
- Talkyria: enviar `Talkyria_Confirmado` e sem tag que passem nas regras; `SinRespuesta` dentro dos padrões pode ir; `AtencionUrgente`/`ClienteRechaza` → reter.
- Tags curtas (cabem numa tela). Ao cancelar pedido retido: deixar só `CANC: <motivo>`.
- Pedido já processado na Dropi não pode ser cancelado lá — barrar ANTES do envio.

## Auditoria de transportadoras

1. Olhar PRIMEIRO pedidos travados e as últimas ~2 semanas, por produto e por região (RM × regiões); só depois a média histórica.
2. Efetividade = entregues ÷ (entregues + devolvidos), contando **qualquer pedido que já teve NOVEDAD como devolvido** (`status LIKE 'NOVEDAD%'` ou `dados->>'novedad_servientrega'` não nulo).
3. Travado = PENDIENTE / PREPARADO PARA TRANSPORTADORA / GUIA_GENERADA / NOVEDAD SOLUCIONADA sem movimento há dias.
4. Comparar transportadoras na mesma cidade/semana; amostra mínima ~15 por lado.
5. Preferência por cidade fica em Dropi → Transportadora → Preferencias. Mudança de configuração na Dropi é feita pelo usuário (passar a lista exata de região/comuna/transportadora).
6. Pedidos parados → montar CSV (ID Dropi, transportadora, status, data, guia) e texto em espanhol para ticket em CAS → Tickets.

## Limites

- Nunca digitar credenciais nem logar pelo usuário.
- Cancelamentos (Shopify/Dropi) e mudanças de configuração da Dropi podem ser bloqueados para o Claude: deixar tudo pronto (tags, filtro, lista) e passar o passo a passo curto.
- Não inventar números; o banco não tem os pedidos do dia (usar a Shopify para o dia corrente).