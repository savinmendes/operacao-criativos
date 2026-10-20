# Perfil e operação (as 3 frentes do Grupo Chegou)

> Quem é a pessoa, o que ela opera, em quais mercados, com quais ferramentas e quais métricas valem em cada frente. Abra antes de qualquer tarefa para saber de qual frente o pedido é.

## Contexto de uso

### Quem é
- Gestora de tráfego pago e produtora de criativos do **Grupo Chegou**.
- O dia a dia (segundo o HANDOFF-CONTEXTO de 06/10/2026) é **produzir criativos de vídeo em lote** (adaptar, traduzir, variar), com agentes em paralelo, e subir/ler campanhas.
- Público interno dos materiais: a própria pessoa, a equipe de closers, produção e mentorados. Público final dos anúncios: leads COD, compradores de infoproduto e clientes X1 (50+).

### As 3 frentes

| Frente | O que é | Mercados | Ofertas / produtos |
|---|---|---|---|
| **Dropshipping COD** | Pagamento na entrega, sem estoque na maioria dos produtos. Catálogo com dezenas de produtos por país, cada um com fornecedor e custo próprios | Chile, Colômbia, México, Guatemala, Romênia (o HANDOFF-CONTEXTO cita também Equador) | Suplementos, eletrônicos, beleza, casa. Exemplos de lotes recentes: Lymphoria (drenagem), Podadora, Wyze Solar Cam, perfumes árabes Lattafa (kits Yara), DeWalt DCD7781 |
| **Infoprodutos** | VSL + quiz + funil de upsell, via Hotmart / Digistore / Stripe | Latam, Espanha, Worldwide (em out/2026 também FR para San Benito) | **Onda Tesla 2.0** (saúde auditiva), **Protocolo Glúteos Brasileños** (estética), **Oração de San Benito** (espiritualidade) |
| **X1 After-Pay** | Venda 1-a-1 por WhatsApp no Brasil, com entrega antes do pagamento | Brasil, público 50+/aposentados | **CartiCuri/CarteCure** (fitoterápico articular) |

Também existe operação de e-commerce com marca própria fora dessas três (ex.: relógios **Pellorini**, envio mundial, devolução de 90 dias, out/2026). Ver [15-lojas-e-paginas.md](15-lojas-e-paginas.md) e `projetos/`.

### Métricas que importam em cada frente
- **COD:** CPA, taxa de efetividade de entrega/pagamento, margem por produto/país/fornecedor. O CPA de decisão é por **entrega concretizada**, não por pedido (ver [14-unit-economics-cod.md](14-unit-economics-cod.md)).
- **Infoprodutos:** VSL, quiz, funil de upsell, ticket, CAC e LTV por oferta/mercado. Decisão pelo **CAC do front + upsell**, não só pelo CPA do front.
- **X1 After-Pay:** atendimento via WhatsApp, fechamento por closer, inadimplência/efetividade de pagamento pós-entrega. O custo por conversa do gerenciador é o pior indicador de decisão; vale o **custo por venda paga**.

### Ferramentas de mídia e operação
- Mídia: **Meta Ads**, **Kwai Ads**, **TikTok Ads**.
- Fonte de verdade de ofertas e preços: **Notion**. Arquivos: **Google Drive** (a pessoa prefere pastas locais por enquanto; o MCP do Drive não sobe vídeo de 20+ MB).
- Venda/atendimento: **WhatsApp**. Planilhas e VS Code.
- Operação COD: **Dropi** e o sistema **Chegou Operações** (MCP `chegou-operacoes`, somente leitura de dados + páginas livres).
- Lojas: **Shopify** (app Releasit para pagamento na entrega).
- Produção: kit de edição em Python, Flora, HeyGen, ElevenLabs (ver [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)).
- Pesquisa de anúncios: winninghunter, dropkiller, Biblioteca de Anúncios do Meta.

### Entregáveis típicos
Criativos de vídeo e imagem, roteiros e hooks, VSLs, páginas de vendas/advertoriais/quiz, relatórios de performance (por oferta e país), dashboards (CPA, efetividade de pagamento, margem de contribuição), apresentações internas, planilhas de preço/fornecedor, SOPs.

### Principais atividades
Criar e gerir campanhas (Meta/Kwai/TikTok); produzir criativos do roteiro à edição; analisar performance, CPA e margem por país/oferta; organizar funis (advertorial/quiz/VSL → checkout ou WhatsApp); acompanhar fechamento dos closers (X1); documentar SOPs e controlar catálogo de fornecedores/custos por país.

## Lógica de uso

### Regra central: nunca misturar frentes
1. Antes de começar, identifique a frente do pedido (COD, Infoproduto ou X1). Se não der para inferir, pergunte em uma linha.
2. Use **só** as métricas, a linguagem e as regras daquela frente. Exemplos do que não fazer:
   - julgar COD pelo CPA do gerenciador (o gerenciador vê pedido, não entrega paga);
   - aplicar fórmula de margem de e-commerce pré-pago no COD;
   - julgar X1 pelo custo por conversa;
   - trazer linguagem de "paga ao receber" para um funil de checkout.
3. Um lote de criativos = uma frente e um país/mercado. Não misture.
4. Em relatórios e nomes de arquivo, use a frente no nome (`cod`, `infoproduto`, `x1`), conforme [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md).

### Como identificar a frente rápido
- Fala em país LATAM/Romênia, Dropi, fornecedor, efetividade, "pago contra entrega" → **COD**.
- Fala em VSL, quiz, upsell, Hotmart/Digistore/Stripe, San Benito, Onda Tesla, Glúteos → **Infoproduto**.
- Fala em WhatsApp, closer, 50+, CartiCuri/CarteCure, pagamento depois da entrega no Brasil → **X1**.
- Loja Shopify de marca própria com pagamento antecipado (ex.: Pellorini) → e-commerce; trate como modelo pré-pago, separado do COD.

### KPI de decisão por frente (resumo)
| | COD | Infoproduto | X1 |
|---|---|---|---|
| Evento que o Meta otimiza | Pedido (Compra) | Compra no checkout | Conversa |
| KPI de decisão | CPA por **pedido entregue/pago** + margem | CAC front + upsell, ticket | Custo por **venda paga**, fechamento por closer |
| Fonte do dado real | Dropi / Chegou Operações | Plataforma de pagamento (Stripe, Hotmart, Digistore) | Atendimento/closers (fonte precisa de revisão manual) |

### Lacunas
- Dados de operação do X1 (onde ficam fechamento por closer e inadimplência): **precisa de revisão manual**.
- Onda Tesla 2.0 e Glúteos Brasileños: não há histórico de lotes nas fontes lidas. **Precisa de revisão manual.**

## Relacionados
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [04-fluxo-producao-criativos.md](04-fluxo-producao-criativos.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [13-analise-meta-ads-e-vencedores.md](13-analise-meta-ads-e-vencedores.md)
- [14-unit-economics-cod.md](14-unit-economics-cod.md)
- [15-lojas-e-paginas.md](15-lojas-e-paginas.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/](projetos/)
