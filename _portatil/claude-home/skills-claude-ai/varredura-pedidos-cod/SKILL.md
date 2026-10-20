---
name: "varredura-pedidos-cod"
description: "Revisa os pedidos COD de um período para achar o que ficou pelo caminho (não enviados, retidos, erro de sync, atenção da Talkyria) e monta a lista simples para o funcionário passar o pente fino."
---

# Varredura de pedidos COD

Responder em português do Brasil, direto. Só leitura até o Savin mandar agir. Economizar tokens: consultas agregadas, saída curta.

Usar quando o Savin pedir para revisar pedidos "desde tal dia", achar o que "ficou pelo caminho", ou montar a lista para o Igor (ou outro funcionário) conferir.

## Antes de começar

1. Ler na memória as regras vigentes da loja (Chile: `/areas/processamento-pedidos-cod.md`; outros países: arquivo da loja).
2. **Confirmar o último lote processado** (número de corte) antes de afirmar que existe atraso. Se o Savin disser que já processou, acreditar e recontar a partir do corte dele. Nunca chamar de atraso o que já foi processado.
3. Período: o que o Savin disser; sem data, desde a segunda-feira passada.

## O que levantar (Shopify Admin GraphQL, busca com `query=`)

Pedidos abertos no período, separados em grupos:

1. **Não enviados**: sem a tag "Order sent to dropi" e sem tag `CANC…`, nem cancelados.
2. **Erro de envio**: tag `Dropi Sync Error` → ver o motivo (cidade sem COD, produto não vinculado na Dropify, SKU) e dizer a correção de cada um.
3. **Retidos**: `RETIDO DROPI` ou outras tags de retenção ainda sem decisão.
4. **Talkyria**: atenção urgente, sem resposta, máximo de tentativas, chamada cortada — e pedidos que deveriam ter sido ligados e não foram (sem saldo, cancelados que foram ligados por engano).
5. **Pendentes antigos**: qualquer pedido com mais de 3 dias ainda sem destino.

Na Dropi (se o Savin pedir ou houver dúvida), conferir os IDs que estão em PENDIENTE sem confirmar.

Telefone de cliente: buscar pelos últimos 8–9 dígitos para achar o pedido.

## Entregar

- **Resumo em 3–5 linhas**: total do período, processados, e quantos em cada grupo acima.
- **Lista para o funcionário** (simples, para colar no WhatsApp): por grupo, `#pedido – nome – produto – o que fazer` (ligar, cancelar, corrigir cidade, reenviar, confirmar na Dropi). Sem jargão técnico, sem IDs internos.
- **Lista do Savin**: o que só ele pode fazer (vincular produto na Dropify, mudar configuração, recarregar saldo), completa e de uma vez.
- Se pedido em espanhol, entregar a lista em espanhol e como .txt quando ele pedir arquivo.

## Limites

- Não cancelar nem enviar nada sem o Savin mandar; deixar tags e lista prontas.
- Nunca digitar credenciais.
- Não inventar números; tudo vem da Shopify, da Dropi ou do banco.