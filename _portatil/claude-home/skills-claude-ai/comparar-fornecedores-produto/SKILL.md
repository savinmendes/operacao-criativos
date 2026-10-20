---
name: "comparar-fornecedores-produto"
description: "Compara fornecedores e produtos equivalentes na Dropi (efetividade, devolução, travados, estoque) para decidir de qual fornecedor enviar cada oferta, em qualquer país COD."
---

# Comparar fornecedores de um produto

Responder em português do Brasil, direto, com opinião clara. Economizar tokens: consultas agregadas.

Usar quando o Savin perguntar por que um pedido saiu por certo fornecedor, comparar dois produtos parecidos (ex.: câmera foco × ampolleta) ou escolher de qual fornecedor enviar.

## Passos

1. **Mapear o vínculo atual**: na Shopify, o metafield `dropi._dropi_product` do produto diz para qual produto/fornecedor da Dropi ele vai. Dizer qual é e desde quando (se der).
2. **Efetividade** no banco Chegou Operações (MCP Dropi, operação `drop`, `metricas_dropi_dropipedido`), mesmas regras da skill de transportadoras:
   - janela de 60 a 7 dias atrás, com coluna de 30 dias ao lado;
   - cancelado fora; devolvido inclui qualquer pedido que já teve NOVEDAD;
   - efetividade = entregues ÷ (entregues + devolvidos);
   - mínimo 15 finalizados por lado.
   Agrupar por `product_name` (produto da Dropi). Na primeira vez em um país, descobrir no `dados` o campo do fornecedor/bodega e agrupar por ele também.
3. **Cortar o viés**: comparar na mesma região e com a mesma transportadora quando der; se um lado tem muito mais pedidos na capital, dizer.
4. **Travados e estoque**: % parado em PENDIENTE/GUIA_GENERADA etc.; estoque atual na página `app.dropi.cl/dashboard/product-details/<ID>/<slug>` (ler "Stock N").
5. **Margem**: se o custo for diferente entre fornecedores, usar `/areas/calculadora-margem.md` para ver o lucro por pedido enviado (efetividade × margem), não só a efetividade.

## Entregar

- Tabela: fornecedor/produto | pedidos | efet. 60d | efet. 30d | travados | estoque | custo.
- Veredito em 1–2 linhas: de qual enviar e por quê.
- Se for trocar, lista exata do que o Savin faz (vincular na Dropify, conferir variantes) — vincular na Dropify é na interface dela, não via metafield.

## Limites

- Não mudar vínculo nem configuração sem o Savin mandar.
- Nunca digitar credenciais.
- Não inventar números.