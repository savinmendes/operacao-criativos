# Unit economics do COD

> Modelo real de margem, CPA e efetividade do dropshipping com pagamento na entrega: onde estão a planilha, as calculadoras e o código, e como fazer a conta sem os erros que já custaram 10 pontos percentuais. Abra para qualquer pergunta de preço, margem, CPA máximo ou efetividade do COD.

## Contexto de uso

### Onde estão as ferramentas
- **Planilha fonte:** "Precificação Padrão CONTRA" (Google Sheets, id `18mNPqnRFDd3Kzc6V8_cjAaeciNmVqiTowSKchVC_Ya4`). Tem células quebradas (`#N/A`, `#DIV/0!`) e um "Custos Administrativos 3%" que rende R$ 0,01 sem base identificável. A cotação nela ficou defasada (set/2026: 165 CLP por real, mercado ~186).
- **Calculadora web** (20/09/2026): https://claude.ai/artifact/8yBHU2JigWBRPEut9V3y2Q (presets reais do Chile por produto e ranking de todos os produtos com o CPA da tela).
- **Dashboard de ranking de produtos Chile** (20/09/2026): https://claude.ai/artifact/8mSgJQt4ppVvfrXhEasqzW · cópia em `03-dashboards/2026-09_cod_dashboard_ranking-produtos-chile.html`.
- **Chegou Operações (09/10/2026):** páginas livres `calculadora-margem-cod` (v6, presets fixos até meados de set) e `calculadora-margem-cod-ao-vivo` (lê o banco: consultas `presets_dropi`, `presets_ecomhub`, `cambio`, `sincronizacao`, `frete_cadastro`, `canceladas_shopify`; período editável, padrão 45 dias). URL: https://operacoes.chegouhub.com.br/drop/paginas/calculadora-margem-cod-ao-vivo. Página irmã de efetividade: `efetividade-drop-latam-ao-vivo`.
- **Código:** `Produtividade com ia/ferramentas/calculadora-cod/` (`lib/modelo.py` = a conta; `adaptadores/helpship_csv.py` = modelo de adaptador; 27 testes).

### Fatos medidos
- Não processado (09/10/2026, funil Shopify): **CL 14,3%, CO 9,5%, GT 17,4%, MX 30,9%**. Romênia (EcomHub) não tem link com a Shopify → usa a regra de cancelados da plataforma.
- Prova do adaptador Helpship (Romênia) contra a versão 46 publicada: Smartwatch Y68 156 pedidos, 67,3% entrega, teto CPA R$ 63,59; Caixa de som 89, 39,5%, R$ 51,16; Perfumes 239 72, 43,5%, R$ 28,59.
- Análise Chile (20/09/2026): descartar pedidos em trânsito dava 65% de efetividade; projetar deu 54,4%, que bate com a coorte madura. Curva de desfecho medida: pedido aberto no 7º dia entrega em 6,1%, no 9º em 2,7%, no 13º em 0,6%.
- Um erro de encoding zerou a curva numa rodada e a Colômbia apareceu com 69,4% em vez de 60,5%.
- O banco do Chegou Operações **não tem frete** de CL/CO/GT/MX (estimado por tabela medida nos exports de set); RO tem frete real (EcomHub). Quantidade por pedido vem do join com a Shopify. Câmbio do cadastro está velho (11/09 e 01/01) → a página usa campo manual.
- Amostra pequena (v9): produto com < 20 pedidos ou < 15 fechados vai para o grupo "Amostra pequena" com aviso (antes sumiam os kits de perfume feminino). Fica fora só quem não tem entrega ou tem < 10 pedidos não cancelados.

### Diferenças por país
- **Chile:** devolução custa só o frete de ida.
- **Guatemala (DropLatam, export "ordenes"):** devolução = frete de ida **mais** `COSTO DEVOLUCION FLETE` (~20,7 GTQ capital, ~28,3 interior). Identidade que valida o mapeamento: `VALOR DE COMPRA EN PRODUCTOS − TOTAL EN PRECIOS DE PROVEEDOR − PRECIO FLETE = GANANCIA`.
- **Romênia (Helpship):** só o preço original vem em RON; custo e fretes já em euro.

## Lógica de uso

### O modelo (não "corrigir" estas três decisões)
1. **Tudo se dilui sobre ENTREGAS CONCRETIZADAS**, não sobre pedidos enviados. No COD o dinheiro só entra quando o produto chega e é pago.
2. **Devolução custa frete, não produto** (o produto volta ao estoque). Perde-se o frete de ida + taxa de retorno onde existir (`frete_devolucao`), rateado sobre as entregas.
3. **CPA é valor absoluto** (custo por compra do gerenciador, Meta/Kwai/TikTok), não % do preço.

### Fórmulas
- Funil: `vendas totais → − % não processados → pedidos enviados → − % devolução → entregas concretizadas`.
- `Margem = preço de venda − custo`.
- Despesa real de anúncio por entrega = `CPA × vendas_totais ÷ entregas`.
- `Lucro por entrega = margem − despesa de anúncio por entrega` (descontando o custo de devolução rateado).
- `CPA máximo = margem × entregas ÷ vendas`.
- **Cotação** = quantas unidades da moeda local valem R$ 1. Converta dividindo: `valor_R$ = valor_local / cotação`. O rótulo "Cotação Peso Colômbia Hoje" é genérico: cole o numeral do país que está calculando.

### Efetividade (fórmula da pessoa, 09/10/2026, a que vale)
- `efetividade = entregues ÷ (entregues + precários + devolvidos)`, **sem cancelados**.
- `efetividade projetada = (entregues + r × em trânsito) ÷ (entregues + precários + devolvidos + em trânsito)`, com `r` = efetividade das semanas anteriores (maduras).
- Exemplo: 40 entregues, 10 novedad, 30 devolvidos, 20 em trânsito, r = 50% → 50%.
- **Precários** (já entraram em novedades/incidência) contam como **devolução**, não como abertos.
- Só o trânsito normal entra na projeção. A efetividade usada em cálculo é sempre a **projetada** (mesma conta da página `efetividade-drop-latam-ao-vivo`). Não use curva por idade nem taxa fixa de 50% nessa conta.
- **Não processado** = `1 − enviadas ÷ vendas Shopify` (canceladas na Shopify + nunca enviadas + canceladas na plataforma), ligando por `shop_order_id` (`vendas_shopify_vendashopify`).
- **Cancelado não é venda**: sai da base como taxa de não processado.

### Medir efetividade num export da Dropi sem se enganar
1. O **custo do export já vem multiplicado pela quantidade**; `Lucro bruto entregue = valor − custo − frete` exato. Não multiplique de novo em pedidos de 2–3 unidades.
2. **Não olhe só a semana recente**: entrega resolve em ~3 dias e devolução em ~10; a última semana chegou a marcar 100% de entrega com 73% dos pedidos em aberto.
3. **Não descarte os pedidos em trânsito**: são majoritariamente perda encalhada. Projete.

### Calculadora em código (`ferramentas/calculadora-cod/`)
- Testes: `python -m unittest discover -s tests` (um só: `python -m unittest tests.test_modelo.<Classe>.<metodo>`). Python nesta máquina pelo caminho completo se precisar: `C:\Users\PICHAU\AppData\Local\Programs\Python\Python312\python.exe`.
- Contrato de entrada (lista de dicts): `classe` (`entregue`/`devolvido`/`cancelado`/`aberto`), `data`, `movimento`, `idade`, `preco` (moeda local), `custo` (**já × quantidade**), `frete`, `frete_devolucao`, `quantidade`, `produto`.
- Projeção: `medir(..., curva=None)` (padrão, taxa dos fechados do próprio grupo; correto com cobertura alta) ou `medir(..., curva=curva_desfecho(...))` (coorte madura, quando há muito em trânsito). A saída registra `metodo_projecao`. Curva global num produto que entrega pior que a média infla o resultado em silêncio.
- **Adaptador novo:** copie `adaptadores/helpship_csv.py`; só traduz campos e status, sem regra de negócio. Confira: moeda por coluna; encoding `utf-8-sig` (BOM quebra a 1ª coluna em silêncio); custo unitário × multiplicado. Antes de virar fonte de presets, rode contra dados com saída conhecida e bata os números.

### Cotações
- Puxe **todas da mesma fonte**: taxa média de mercado do **Wise**, buscando a página direto (WebFetch), não resumo de busca. Releia todas as moedas de uma vez.
- Em 21/09/2026, misturar Wise, XE e Investing gerou erro de 6% (o quetzal "corrigido" de 1,497 para 1,406 estava certo; Wise mostrava 1,495). No mesmo dia: COP 589,64 no Investing × 625,9 no Wise.
- Confira a cotação do dia: a planilha fica defasada.

### Checklist de uma conta de COD
- [ ] País e fonte (Dropi, DropLatam, EcomHub/Helpship, Chegou Operações) identificados; regra de devolução do país aplicada.
- [ ] Moeda por coluna conferida; cotação do Wise do dia, todas da mesma fonte.
- [ ] Custo × quantidade conferido (não multiplicar duas vezes).
- [ ] Cancelados fora; precários como devolução; trânsito projetado com `r` maduro.
- [ ] Não processado do funil Shopify do país.
- [ ] Tudo diluído sobre entregas; CPA absoluto do gerenciador.
- [ ] Amostra pequena sinalizada.
- [ ] Método de projeção dito na saída.

### Lacunas
- Adaptador do MCP `chegou-operacoes` (`https://operacoes-api.chegouhub.com.br/mcp`) para substituir o export manual: bloqueado na autorização OAuth (exige navegador). Falta confirmar se o conector expõe por pedido status, custo de fornecedor, frete e custo de devolução. **Precisa de revisão manual.**
- Frete real de CL/CO/GT/MX no banco: inexistente (estimado). **Precisa de revisão manual.**
- Origem do "Custos Administrativos 3%" da planilha: **precisa de revisão manual**.

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [15-lojas-e-paginas.md](15-lojas-e-paginas.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [projetos/](projetos/)
