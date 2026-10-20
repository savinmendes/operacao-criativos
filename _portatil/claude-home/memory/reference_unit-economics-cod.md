---
name: reference-unit-economics-cod
description: "Onde vive o cálculo de margem/CPA do COD: planilha 'Precificação Padrão CONTRA' no Google Drive e a calculadora publicada como artifact. Inclui o modelo de cálculo real, que não é óbvio."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 68966334-b2d9-4891-bbd6-2776cdfc0763
  modified: 2026-10-09T22:49:19.147Z
---

**Planilha fonte:** "Precificação Padrão CONTRA" — Google Sheets, dono saviomendesalvess@gmail.com, id `18mNPqnRFDd3Kzc6V8_cjAaeciNmVqiTowSKchVC_Ya4`. É onde o usuário calcula preço, margem e CPA por produto/país do COD.

**Calculadora web** (feita em 20/09/2026 a partir dela): https://claude.ai/artifact/8yBHU2JigWBRPEut9V3y2Q — tem presets reais do Chile por produto (mix de ofertas e só 1 unidade) e um ranking que roda todos os produtos com o CPA que estiver na tela.

**Dashboard de ranking de produtos** (Chile, 20/09/2026): https://claude.ai/artifact/8mSgJQt4ppVvfrXhEasqzW · cópia em `03-dashboards/2026-09_cod_dashboard_ranking-produtos-chile.html`

**Como medir efetividade num export da Dropi sem se enganar** (aprendido analisando o Chile em 20/09/2026 — os três erros custam 10 pontos percentuais cada):
- **O custo do export já vem multiplicado pela quantidade**, e `Lucro bruto entregue = valor − custo − frete` exato. Não multiplicar de novo em pedidos de 2 ou 3 unidades.
- **Não olhe a semana recente.** Entrega resolve em ~3 dias e devolução em ~10, então entre os pedidos recentes que já fecharam quase só há entrega. A última semana marcava 100% de entrega com 73% dos pedidos ainda em aberto.
- **Não descarte os pedidos em trânsito** — eles são majoritariamente perda encalhada. Projete pela curva de desfecho medida numa coorte antiga: um pedido ainda aberto no 7º dia entrega em 6,1% dos casos, no 9º em 2,7%, no 13º em 0,6%. Descartar dava 65% de efetividade; projetar dá 54,4%, que bate com o que a coorte madura mostra de verdade.
- Scripts dessa análise ficaram em `scratchpad/dropi_*.py` (sessão 68966334); Python nessa máquina só roda pelo caminho completo `C:\Users\PICHAU\AppData\Local\Programs\Python\Python312\python.exe`.

**Modelo de cálculo do COD** — vale registrar porque não é dedutível olhando a planilha (ela tem células quebradas: `#N/A`, `#DIV/0!`, e um "Custos Administrativos 3%" que rende R$0,01 sem base identificável):

- **Cotação = quantas unidades da moeda local valem R$ 1** (taxa inversa). Converte-se dividindo: `valor_R$ = valor_local / cotação`. O rótulo "Cotação Peso Colômbia Hoje" é fixo/genérico — o usuário cola ali o numeral do país que está calculando, seja Chile, Colômbia ou México.
- **Tudo é diluído sobre as ENTREGAS CONCRETIZADAS**, não sobre pedidos enviados. Esse é o erro fácil de cometer.
- **Devolução custa o frete de ida, não o produto** (o produto volta pro estoque). Esse custo é rateado sobre as entregas que deram certo.
- **CPA é o valor por compra do gerenciador de anúncios** (Meta/Kwai/TikTok), em moeda local ou R$ — não uma % do preço. A despesa real de anúncio por entrega é `CPA × vendas_totais ÷ entregas`, o que infla bastante o CPA nominal.
- Funil: `vendas totais → −% não processados → pedidos enviados → −% devolução → entregas concretizadas`.
- `Margem = preço de venda − valor de custo` · `Lucro por entrega = margem − despesa de anúncio` · `CPA máximo = margem × entregas ÷ vendas`.

**Como aplicar:** se o assunto for precificação, margem, CPA ou efetividade do COD, usar esse modelo em vez de unit economics genérico de e-commerce — e sempre conferir a cotação do dia, porque a planilha fica defasada (em set/2026 ela ainda usava 165 CLP por real, quando o mercado estava em ~186).

**Cotações: puxar todas da MESMA fonte, sempre.** Em 21/09/2026 eu misturei Wise, XE e Investing e produzi erro de 6% — "corrigi" o quetzal de 1,497 para 1,406 com base num inverso do XE lido via resumo de busca, e o Wise mostrava 1,495, ou seja o valor original estava certo. Fontes divergem muito entre si (no mesmo dia: COP 589,64 no Investing contra 625,9 no Wise). Usar a taxa média de mercado do Wise, buscando a página direto com WebFetch em vez de confiar em resumo de busca, e reler todas as moedas de uma vez para o conjunto ficar coerente.

**Guatemala (DropLatam, export "ordenes") é um modelo diferente do Chile:** a devolução custa o frete de ida **mais** uma taxa de volta na coluna `COSTO DEVOLUCION FLETE` (~20,7 GTQ na capital, ~28,3 no interior). No Chile só se perde o frete de ida. A identidade que valida o mapeamento de colunas é `VALOR DE COMPRA EN PRODUCTOS − TOTAL EN PRECIOS DE PROVEEDOR − PRECIO FLETE = GANANCIA`.

**Calculadora no Chegou Operações (09/10/2026):** página livre `calculadora-margem-cod` (v6, presets fixos até meados de set) e a nova `calculadora-margem-cod-ao-vivo` (lê o banco: consultas `presets_dropi`, `presets_ecomhub`, `cambio`, `sincronizacao`, `frete_cadastro`, `canceladas_shopify`; período editável, padrão 45 dias). URL: https://operacoes.chegouhub.com.br/drop/paginas/calculadora-margem-cod-ao-vivo. O banco NÃO tem frete de CL/CO/GT/MX (frete estimado por tabela medida nos exports de set); RO tem frete real (EcomHub). Quantidade por pedido vem do join com a Shopify. Câmbio do cadastro está velho (11/09 e 01/01) → a página usa o campo manual. Scripts/SQL em scratchpad da sessão fefd88e1 `calc\`.

**Regra da pessoa (09/10/2026): pedidos "precários" (já entraram em novedades/incidência) contam como DEVOLUÇÃO**, não como em aberto/projetados — senão a efetividade fica superestimada. Efetividade usada em cálculo é sempre a **projetada** (mesma conta da página `efetividade-drop-latam-ao-vivo`). Só o que está em trânsito normal entra na projeção pela curva.

**Fórmula da pessoa (09/10/2026), a que vale:** efetividade = entregues ÷ (entregues + precários + devolvidos), sem cancelados. Efetividade projetada = (entregues + r × em trânsito) ÷ (entregues + precários + devolvidos + em trânsito), com r = efetividade das semanas anteriores (maduras). Ex.: 40 E, 10 novedad, 30 D, 20 trânsito, r=50% → 50%. Não usar curva por idade nem taxa fixa de 50%.

**Não processado (regra da pessoa, 09/10/2026):** vem do funil da Shopify — 1 − enviadas ÷ vendas Shopify (canceladas na Shopify + nunca enviadas + canceladas na plataforma). Link via `shop_order_id` (`vendas_shopify_vendashopify`). Medido: CL 14,3%, CO 9,5%, GT 17,4%, MX 30,9%. Romênia (EcomHub) não tem link com a Shopify → fica na regra de cancelados da plataforma. Calculadora ao vivo v8 já usa isso.

**Amostra pequena (v9, 09/10/2026):** produto com <20 pedidos ou <15 fechados não some mais — vai pro grupo "Amostra pequena" do seletor, com aviso. Só fica fora quem não tem nenhuma entrega, ou tem <10 pedidos não cancelados (HAVING das consultas SQL). Motivo: os kits de perfume feminino (Yara/Pink White Candy CL, combos femininos RO) sumiam.
