# Análise de Meta Ads e escolha de vencedores

> Contas de anúncio conhecidas, o critério de vencedor usado na análise San Benito (11/10/2026), como ler resultado por frente no Meta, estrutura de teste/escala e como cruzar gasto × venda real. Abra antes de qualquer leitura de campanha ou ranking de criativos.

## Contexto de uso

### Contas e fontes de venda conhecidas
| Conta / fonte | ID | Moeda | Situação |
|---|---|---|---|
| Meta: **CONTA 01 SAN BENITO** | act 1929332567965953 | USD | Onde rodam as campanhas San Benito (SB ES, SB US, SB RESTO, SB FR) |
| Meta: **INFO 01** | 2116263812662576 | USD | Acessível; sem campanhas San Benito com gasto em 11/10/2026 |
| Meta: contas em BRL | precisa de revisão manual (IDs) | BRL | Sem forma de pagamento (informado na orquestração de 13/10/2026) |
| **Stripe** (SMA DIGITAL BUSINESS LLC) | — | — | Fonte de vendas de infoproduto para cruzar com o gasto |

- Na análise de 11/10/2026 havia 4 contas acessíveis pelo conector; só a CONTA 01 tinha campanhas San Benito com gasto.
- Os checkouts aparecem nos nomes dos anúncios como sufixos (`| HOT`, `| HOT 2`, `| WHOP`), e houve teste A/B de gateway "HOT x WHOP" (21/09/2026). O que cada sigla significa exatamente (Hotmart? Whop?): **precisa de revisão manual**.
- Conector usado: Meta Ads (somente leitura na análise; nada criado, editado, pausado ou ativado).

### Análise San Benito ES, 11/10/2026 (fatos)
- Escopo: vida útil inteira (`date_preset maximum`), 50 campanhas `SB ES` de vendas (datas no nome de 12/07 a 04/10/2026), 543 anúncios → **220 criativos** após juntar variações. Fora: SB US, SB RESTO, SB FR e 2 campanhas de engajamento.
- Totais SB ES: **US$ 14.292,29 de gasto, 452 compras, CPA médio US$ 31,62, ROAS médio 1,22** (pixel, `website_purchase_roas`).
- Vencedores (ordem de ROAS):

| # | Criativo | Gasto | Compras | CPA | ROAS | CTR link | Obs. |
|---|---|---|---|---|---|---|---|
| 01 | SHAKIRA 1 + PAPA 1 | 221,31 | 21 | 10,54 | 3,82 | 5,37% | Reprovado (DISAPPROVED), sem arquivo |
| 02 | ADS 6 | 1.047,85 | 71 | 14,76 | 2,64 | 5,88% | 1080p, 136,9 s |
| 03 | SHAKIRA 3 + PAPA 2 | 446,83 | 27 | 16,55 | 2,32 | 5,55% | Reprovado, sem arquivo |
| 04 | ADS 20 | 1.001,50 | 46 | 21,77 | 1,91 | 6,66% | 720p, 141,3 s |
| 05 | ADS 12.12 | 341,52 | 13 | 26,27 | 1,63 | 10,17% | 31,6 s |
| 06 | JESU V07 | 296,20 | 11 | 26,93 | 1,48 | 10,14% | 33,1 s |
| 07 | ADS 1 | 1.202,40 | 43 | 27,96 | 1,43 | 6,28% | Só 360×480 no Meta |
| 08 | ADS 12 | 1.239,25 | 48 | 25,82 | 1,41 | 4,57% | 31,5 s |
| 09 | AD 81 (provisório) | 71,21 | 3 | 23,74 | 2,08 | 6,32% | 109,9 s |
| 10 | ADS 12.1 GD (provisório) | 90,47 | 3 | 30,16 | 1,30 | 5,72% | 31,6 s |

- Padrões observados: título "🔴 EN VIVO: La oración a San Benito que casi nadie conoce 🙏" em 6 de 10; texto principal quase igual em todos (ângulo "mala suerte"/bloqueio espiritual); vídeos longos (~2 min) = volume (US$ 1.000–1.200, 43–71 compras); curtos (31–33 s) = CTR ~10%. Família ADS 12: 12, 12.12 e 12.1 GD venceram, mas 12.1, 12.7 e 12.18 gastaram bem e perderam (o corpo funciona, depende da abertura). Celebridade (Shakira) = os 2 melhores ROAS, mas reprovados: reaproveitar exige decisão de compliance.
- Pasta: `Downloads/SAN-BENITO-ES-VENCEDORES/` (8 vídeos + `.txt` de origem de cada um + `00-RELATORIO.md` com o ranking completo dos 220 criativos e a lista das 50 campanhas).
- 13/10/2026: a pessoa apontou **OP2 ASCENSAO** (~US$ 2,1 mil de gasto na vida, ativo ES/US/EURO) e **JESU V07** como vencedores para versão FR. Note que na análise de 11/10 (só SB ES) o OP2 ASCENSAO teve ROAS 0,46 e não entrou no critério; o julgamento da pessoa usa outros mercados/dados. Ver `projetos/`.
- Limitações registradas: compras/ROAS do pixel com janela padrão, sem reembolso, chargeback nem upsell fora do pixel; sem dado de margem; a API não liberou `download_hd_url` (vídeos baixados com yt-dlp ou achados localmente pela duração); ADS 1, 6 e 12 rodaram parte do gasto em posts sem `video_id`.

### Nomes de campanha observados (SB ES)
Padrão `SB ES - DD/MM - <estrutura> [rótulo]`, ex.: `CBO 1-1-6 - BID 53 [ESPANHA]`, `ABO - lead 2 [TESTE DE CRIATIVOS]`, `CBO BIDCAP 37 - PUBLICAÇÕES [HOT]`, `1-5-10 JESU [ABO]`, `CBO 1-1-7 CAMPEOES`. Mostra uso de ABO para teste, CBO com bid cap para escala e campanhas de "campeões".

## Lógica de uso

### 1. Antes de ler: frente e KPI
| | COD | Infoproduto | X1 After-Pay |
|---|---|---|---|
| Unidade de campanha | País × produto | Oferta × mercado | Oferta (Brasil) |
| KPI de decisão | CPA por **pedido entregue/pago** + margem (o gerenciador só vê o pedido) | CAC do front + upsell, ticket | Custo por **venda paga**; fechamento por closer |
| Fonte da venda real | Dropi / Chegou Operações | Stripe / Hotmart / Digistore / Whop | Atendimento/closers |
| Atribuição | 7d clique / 1d view | Padrão | Evitar 1d view (compra demora dias) |

Nunca decida COD ou X1 pelo CPA do gerenciador. Nunca invente métrica; sem dado, diga a limitação.

### 2. Critério de vencedor (método San Benito 11/10/2026, reaproveitável)
1. **Escopo:** defina conta, mercado (prefixo do nome da campanha), objetivo (só vendas) e período. Exclua engajamento/aquecimento.
2. **Agrupe variações** do mesmo criativo: some anúncios com sufixos de checkout/nova veiculação (`| HOT`, `| WHOP`, `— NV`, `B`). Confirme pelo `video_id` quando houver.
3. **Gasto relevante:** gasto ≥ **2× o CPA médio** do escopo (no SB ES: ≥ US$ 63,24, perto do percentil 90).
4. **Eficiência:** CPA ≤ média **ou** ROAS > média.
5. **Ordene por ROAS** (média dos ROAS dos anúncios ponderada pelo gasto). Vencedores com < 5 compras ficam no fim como **provisórios**.
6. Marque status (reprovado, pausado, ativo) e resolução do arquivo disponível. Reprovado por compliance (ex.: celebridade) vai para decisão da pessoa.
7. Baixe os vencedores na maior qualidade (≥720p; ver [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)) para uma pasta `<OFERTA>-<MERCADO>-VENCEDORES/` com `.txt` de origem e `00-RELATORIO.md`.
8. Relatório: contexto, totais, critério, tabela de vencedores, "o que têm em comum" (só o que os dados e arquivos mostram), limitações, ranking completo, campanhas analisadas.

### 3. Cruzamento gasto × venda real
- **Infoproduto:** gasto do Meta por criativo/campanha × vendas no Stripe (e demais plataformas), no mesmo período e moeda. Ligue pela UTM/nome do anúncio. Inclua upsell para chegar ao CAC real. Desconte reembolso/chargeback quando a fonte trouxer.
- **COD:** gasto × pedidos × **entregas** (Dropi/Chegou Operações), com efetividade projetada (ver [14-unit-economics-cod.md](14-unit-economics-cod.md)). CPA real por entrega = CPA × vendas ÷ entregas.
- **X1:** gasto × conversas × vendas pagas por closer (fonte: **precisa de revisão manual**).
- Sempre: mesma janela, mesma moeda (cotação de uma fonte só), e diga qual fonte foi usada.

### 4. Ler o resultado (Andromeda modo 3)
1. Julgue o **conjunto** antes do anúncio. Anúncio de CPA ruim em conjunto que bate meta pode ser topo de funil.
2. Classifique cada anúncio pela assinatura (frequência **diária**, não do período):
   - Topo: gasto alto, CPM baixo, frequência 1,00–1,10, CPA atribuído alto.
   - Meio: médio, 1,15–1,20.
   - Fundo: gasto baixo, CPM alto, 1,25–1,5+, CPA baixo.
   Não corte o topo por CPA atribuído (seca o funil). Diagnostique o elo mais fraco: topo fraco → mais criativos de topo; sem fundo → estáticos de oferta.
3. Leia **por eixo** (persona, ângulo, consciência, formato): o nome do anúncio precisa carregar isso.
4. Sinais de agrupamento por similaridade: quase todo o gasto em 1–2 anúncios com as variações sem impressão; frequência > 2 em público frio. Saída é conceito novo (criador, cenário, formato), não variação.
5. Saída: escalar / manter / cortar / substituir, com evidência e confiança, e o conceito que falta no próximo lote.
6. Dado da conta que contradiz heurística vai para `contexto/estrategias-criativos.md`.

### 5. Teste e escala (pontos de partida de praticantes; calibrar)
- Verba de teste por conjunto ≥ 3× CPA-alvo; julgamento em blocos de 7 dias.
- Corte: gasto de 2× CPA-alvo sem conversão, ou 7 dias sem conversão.
- Escala: +10% 1–3×/semana (−15% se passar do CPA) ou +20% a cada ~4 dias; pré-requisito ≥ 4 vencedores diferentes entre si.
- Volume: gasto < US$ 10 mil/mês → ~8–12 conceitos distintos/mês; acerto típico 4–6% ⇒ ~1 vencedor a cada 16–25 criativos. Orce o lote.
- Lançamento por frente: COD 4–6 ângulos × 2–3 execuções (8–12 ativos), ângulo com > 60% do gasto ganha campanha própria; Infoproduto 3 ângulos por perfil × 5–6 tipos; X1 8–15 anúncios (estático, carrossel, vídeo) por consciência, início agendado ≥ 12 h após criar.
- Não fazer: anúncio novo contra vencedor com histórico; pausar os antigos ao subir novos; adicionar anúncio em conjunto que bate meta.
- Desligue as melhorias automáticas do Advantage+ Creative em saúde/estética (a IA pode reescrever promessa).
- COD e conversa: cost cap e "não matar" só funcionam se o evento otimizado for dinheiro real. CPA por pedido aceitável = CPA por entrega paga aceitável × efetividade.

### 6. Armadilhas
- ROAS do pixel não desconta reembolso, chargeback nem upsell fora do pixel.
- Vencedor com < 5 compras é estatisticamente fraco.
- Vídeo baixado pode não ser a mesma edição que rodou em post sem `video_id`: confira visualmente.
- `download_hd_url` pode vir `null` na API: use yt-dlp `-f "bv*+ba/b"` ou o arquivo local com a mesma duração.

### Lacunas
- IDs das contas BRL e o uso de cada conta além de SB: **precisa de revisão manual**.
- Integração Stripe × Meta (como ligar venda a anúncio: UTM, metadata): **precisa de revisão manual**.
- Contas Kwai e TikTok Ads: nenhum dado nas fontes lidas. **Precisa de revisão manual.**

## Relacionados
- [01-perfil-e-operacao.md](01-perfil-e-operacao.md)
- [03-preferencias-de-trabalho.md](03-preferencias-de-trabalho.md)
- [09-lipsync-e-avatar-heygen.md](09-lipsync-e-avatar-heygen.md)
- [12-estrategia-criativa-e-copy.md](12-estrategia-criativa-e-copy.md)
- [14-unit-economics-cod.md](14-unit-economics-cod.md)
- [16-ferramentas-e-servicos.md](16-ferramentas-e-servicos.md)
- [projetos/](projetos/)
