# Meta Andromeda — o que a Meta publicou oficialmente (2024–2026) e implicações para criativo

Legenda: **[OFICIAL]** = texto/número publicado pela própria Meta (engineering.fb.com, facebook.com/business, transcrições de earnings). **[PRÁTICA]** = interpretação de agências/praticantes, sem fonte Meta localizada. Pesquisa feita em 09/10/2026.

## 1. O que a engenharia da Meta publicou sobre Andromeda, GEM, Lattice, sequence learning e modelos seguintes

### Takeaway
Andromeda é oficialmente o **motor de recuperação (retrieval)** de anúncios: filtra dezenas de milhões de candidatos para alguns milhares que seguem para o ranking (GEM/Lattice). A Meta publicou ganhos modestos e segmentados por modelo (+6% recall, +8% qualidade, +14% qualidade em Q3/2025, ~4% conversões), e em Q2/2026 anunciou o **Meta Generative Recommender**, com LLMs dentro do retrieval que "raciocinam sobre o conteúdo do anúncio".

### Cited Findings
**Andromeda (anúncio original, 02/12/2024)** — [engineering.fb.com](https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/)
- [OFICIAL] "Meta Andromeda is a personalized ads retrieval engine". Seleciona os anúncios relevantes entre dezenas de milhões de candidatos e passa alguns milhares para a etapa de ranking.
- [OFICIAL] Roda em NVIDIA Grace Hopper Superchip; a integração com o MTIA estava planejada.
- [OFICIAL] Números: "+6% recall improvement to the retrieval system"; "+8% ads quality improvement on selected segments"; aumento de "10,000x" na complexidade do modelo; mais de 100x na latência de extração de features; mais de 3x no QPS de inferência ponta a ponta. A Meta projeta "another 1,000x increase in model complexity".
- [OFICIAL] O mesmo post liga Andromeda ao Advantage+ e à IA generativa: "22% increase in ROAS" para quem ativa o Advantage+ creative, "7% increase in conversions" com geração de imagem e "more than a million advertisers … more than 15 million ads in a month". O motivo apresentado: a IA generativa aumenta o volume de criativos e o retrieval precisa escalar para isso.

**Post-resumo para anunciantes (27/03/2025)** — [facebook.com/business/news](https://www.facebook.com/business/news/ai-innovation-in-metas-ads-ranking-driving-advertiser-performance)
- [OFICIAL] Andromeda: "enabled a 10,000x increase in the complexity of models used for ads retrieval"; "allows Meta to pick the right creative to deliver more personalized ads"; "8% increase in ads quality".
- [OFICIAL] GEM: "increased ad conversions by up to 5%".
- [OFICIAL] Lattice: generaliza "across campaign objectives and surfaces in place of numerous, smaller ads models"; "increased ad quality by almost 12% and increased ad conversions by up to 6%".
- [OFICIAL] Sequence learning: considera "the sequence of actions a person takes before and after seeing an ad"; "+3% conversions" em segmentos testados.
- [OFICIAL, a ligação mais direta com criativo] "as businesses upload more and more creatives to support a diversification strategy, Meta Andromeda works behind the scenes" para escolher o criativo certo para cada pessoa.

**GEM (10/11/2025)** — [engineering.fb.com](https://engineering.fb.com/2025/11/10/ml-applications/metas-generative-ads-model-gem-the-central-brain-accelerating-ads-recommendation-ai-innovation/)
- [OFICIAL] É "the largest foundation model for recommendation systems (RecSys) in the industry, trained at the scale of large language models". Fica na etapa de **ranking**, não na de retrieval, e repassa o que aprende para os outros modelos por transferência de conhecimento.
- [OFICIAL] Resultados: "+5% ad conversions on Instagram" e "+3% on Facebook Feed" (Q2/2025); "4x more efficient at driving ad performance gains" que os modelos de ranking anteriores; transferência de conhecimento "2x" mais eficaz que a destilação padrão; "23x increase in effective training FLOPs". Processa sequências de "up to thousands of events".
- [OFICIAL] Posts seguintes: "Training GEM at LLM scale" ([03/08/2026](https://engineering.fb.com/2026/08/03/ml-applications/training-gem-at-llm-scale-meta-ads-recommendation-foundation-model/), não li o texto completo) e a arquitetura multi-estágio de sequências ([05/08/2026](https://engineering.fb.com/2026/08/05/ml-applications/from-user-sequences-to-scaling-laws-a-multi-stage-architecture-for-metas-ads-ranking/)), que traz "+6% conversões no Instagram, +3% no Facebook, +3,5% cliques no Facebook" e leis de escala log-lineares, como em LLMs.

**Earnings calls (falas da CFO Susan Li e de Zuckerberg; transcrições em PDF no site de RI da Meta)**
- [OFICIAL] **Q2/2025 (jul/2025):** "The Andromeda model architecture we began introducing in the second half of 2024 powers the ads retrieval stage … where we select the few thousand most relevant ads from tens of millions of potential candidates." No Q2, as melhorias no Andromeda e a expansão para o Facebook Reels levaram a "nearly 4% higher conversions on Facebook mobile Feed and Reels". GEM: "~5% Instagram e 3% Facebook Feed e Reels". Lattice: "nearly 4% increase in ad conversions across Facebook Feed and Reels"; usado desde 2023. Também em Q2/2025 terminou o rollout do fluxo de criação simplificado das campanhas Advantage+ de vendas e de app. — [Transcrição Q2 2025](https://s21.q4cdn.com/399680738/files/doc_financials/2025/q2/META-Q2-2025-Earnings-Call-Transcript.pdf)
- [OFICIAL] **Q3/2025 (out/2025):** "significantly improved performance of Andromeda in Q3 by combining models across retrieval and early stage ranking into a single model, driving a 14% increase in ads quality on Facebook surfaces." O Lattice cortou cerca de 100 modelos de ranking. O run-rate das soluções end-to-end automatizadas chegou a US$ 60 bi. — [Transcrição Q3 2025](https://s21.q4cdn.com/399680738/files/doc_financials/2025/q3/META-Q3-2025-Earnings-Call-Transcript.pdf)
- [OFICIAL] **Q4/2025 (jan/2026):** "we extended our Andromeda ads retrieval engine so it can now run on Nvidia, AMD, and MTIA … nearly triple Andromeda's compute efficiency." GEM e a nova arquitetura de sequence learning deram "3.5% lift in ad clicks on Facebook and a more than 1% gain in conversions on Instagram". O GEM passou a cobrir o Facebook Reels, e o treino do GEM vai escalar em 2026. — [Transcrição Q4 2025](https://s21.q4cdn.com/399680738/files/doc_financials/2025/q4/META-Q4-2025-Earnings-Call-Transcript.pdf)
- [OFICIAL] **Q1/2026 (abr/2026):** Lattice e GEM deram "more than 6% increase in conversion rate for landing page view ads". O "Adaptive Ranking Model", um recomendador em escala de LLM usado na inferência, deu "+1.6% conversion rates" com conversões offsite. "more than 8 million advertisers using at least one of our gen AI ad creative tools". Quem usa geração de vídeo teve "more than 3% higher conversion rates in tests". — [Transcrição Q1 2026](https://s21.q4cdn.com/399680738/files/doc_financials/2026/q1/META-Q1-2026-Earnings-Call-Transcript.pdf)
- [OFICIAL] **Q2/2026 (jul/2026):** "we introduced Meta Generative Recommender, a paradigm shift … Rather than scoring every possible ad individually, we are now using LLMs to reason about ad content and user preferences together, and predict the best ad for each person … We deployed the first generative model into our ads retrieval system." Pilotos com LLM deram "+1% app event conversions on Instagram". Somados ao GEM e ao sequence learning: "8.3% increase in ad clicks and a 15.7% uplift in conversions on Facebook". Advantage+ end-to-end com mais de US$ 75 bi de run-rate anual. "over 9 million small businesses using at least one AI creative tool". A adoção de geração de imagem (incluindo imagem a partir de vídeo) "more than double[d]". Há uma nova "end-to-end creative solution … translate real performance signals into their next creative decision". O Muse Image (Meta Superintelligence Labs) "can analyze images, improve its own work, and produce better ad variations". — [Transcrição Q2 2026](https://s21.q4cdn.com/399680738/files/doc_financials/2026/q2/META-Q2-2026-Earnings-Call-Transcript.pdf)

### Inferences
- Os ganhos oficiais são de **um dígito por modelo e por trimestre**. Os "+15,7% conversões no Facebook" de Q2/2026 juntam vários modelos. Promessas de "Andromeda dobrou meu ROAS" não vêm da Meta.
- A frase do Generative Recommender ("reason about ad content") é a primeira declaração oficial de que o próprio conteúdo do anúncio é interpretado semanticamente na etapa de retrieval. Isso sustenta a tese de que ângulo e mensagem, e não só o visual, influenciam quem recebe cada criativo. A Meta não detalhou o mecanismo.
- Ordem do pipeline: retrieval (Andromeda, e agora também o Generative Recommender) → ranking inicial e final (Lattice/GEM, Adaptive Ranking na inferência).

### Gaps
- Não achei data oficial de "rollout global concluído" do Andromeda. "Outubro de 2025" aparece só em agências ([ex.](https://themtmagency.com/blog/meta-andromeda-october-2025-update-why-creative-diversity-now-defines-ad-performance)). Oficialmente, a introdução começou no "second half of 2024" (Q2/2025 call).
- Não consegui ler a transcrição de Q1/2025 (o link deu erro). O post do GEM de 03/08/2026 foi visto só pelo título.

## 2. Diversificação de criativo, "creative similarity" e "Entity ID": o que é oficial

### Takeaway
A Meta recomenda oficialmente **diversificar criativos** (é um dos pilares do Performance 5) e, em 2026, colocou no Ads Manager uma métrica de **similaridade criativa** ("em desenvolvimento"). **"Entity ID", "1 Entity ID = 1 ticket no leilão" e limites como 60%/40% de similaridade não aparecem em nenhuma fonte Meta que eu tenha achado.** São jargão de praticantes.

### Cited Findings
- [OFICIAL] O Performance 5 tem 5 pilares: simplificação da conta, automação, **diversificação do criativo**, qualidade dos dados e validação dos resultados. Texto do pilar: "Desenvolva uma variedade de criativos do anúncio e permita que a IA entregue a mensagem certa às pessoas com maior probabilidade de se interessarem por ela." A página não diz quantos criativos usar nem quais tipos de diversidade. — [facebook.com/business/ads/performance-marketing](https://www.facebook.com/business/ads/performance-marketing)
- [OFICIAL, via imprensa] Estudo da Meta com AppsFlyer e Dentsu sobre 1,1 milhão de variações de criativo (Social Media Today, 04/06/2025):
  - Combinação 9:16 com áudio + gancho emocional nos primeiros segundos + pessoa na tela + texto sobreposto: "16% lower CPA on average, a 29% higher conversion rate, and 11% greater reach".
  - Vídeos com pessoas e áudio expressivo: "8% more conversions per dollar".
  - Campanhas com diversidade de formato e de mensagem: "up to a 32% improvement in CPA, and a 9% increase in incremental reach".
  - Imagens geradas por IA: "+11% CTR" e "+7.6% conversion rate".
  - Mais de 4 milhões de anunciantes por mês usam as ferramentas de IA generativa.
  — [Social Media Today](https://www.socialmediatoday.com/news/meta-shares-tips-on-best-performing-ad-approaches-ai/749897/)
- [OFICIAL, via imprensa e busca] Mix de formatos: ad sets com imagem + vídeo + vídeo 9:16 com áudio tiveram "9.1% lower CPA" que os que não tinham algum desses formatos; com 20% ou mais dos assets em 9:16 com áudio, "7% lower CPA". A fonte é atribuída ao handbook/guia de criativo da Meta (amostra de 100 mil ou mais ad sets). — [busca: Social Media Today / Optimixed](https://www.optimixed.com/meta-shares-ad-tips-based-on-1-million-ad-creatives/). Não consegui abrir a página oficial do Help Center para conferir o texto exato.
- [OFICIAL, via busca no Help Center] Limites de volume: até 50 imagens/vídeos (campanhas de app) e até 150 combinações de criativo nas antigas Advantage+ shopping. A recomendação é variar "visuals, messages and storytelling approaches". — [Best Practices for Automated App Ads](https://www.facebook.com/business/help/711378409718185); [Advantage+ shopping](https://www.facebook.com/business/ads/meta-advantage/advantage-plus-shopping-ads)
- [OFICIAL, citado por terceiro] **Creative Similarity no Ads Manager:** "a metric that estimates how visually diverse your images and videos are, designed to detect when assets are becoming too similar early on". Aparece em Colunas → Personalizar colunas, marcada como "em desenvolvimento", e foi liberada no fim de agosto de 2026. O autor alerta que a Meta não divulgou o critério nem os limites entre os níveis Baixo/Médio, e recomenda não otimizar para essa métrica. — [note.com/sheeema_meta, 07/09/2026](https://note.com/sheeema_meta/n/ne771abb2a8b6?hl=en). Existe também a página oficial "Creative fatigue recommendations in Meta Ads Manager" ([Help 1346816142327858](https://www.facebook.com/business/help/1346816142327858)), mas o corpo dela não carregou para leitura.
- [OFICIAL] A métrica, segundo o que foi descrito, é **visual** ("how visually diverse your images and videos are"). Não há texto oficial dizendo que copy, ângulo ou persona entram no cálculo.
- [PRÁTICA] "Entity ID": anúncios parecidos seriam agrupados em um único ID, com "one ticket to the retrieval auction", usando visão computacional + NLP + áudio. — [adsuploader](https://adsuploader.com/blog/meta-andromeda); [dataally](https://www.dataally.ai/blog/metas-creative-entity-id-why-creative-diversification-is-essential). A Precis reconhece que apresenta isso como algo a que "Meta refers to", mas sem citar fonte Meta. — [Precis](https://www.precis.com/resources/meta-andromeda-and-creative-strategy-what-actually-changed-and-what-didnt)
- [PRÁTICA, sem base oficial] "Acima de 60% de similaridade o sistema colapsa em um Entity ID; mantenha abaixo de 40%; 8–12 conceitos por campanha com 2–3 variações cada" ([novoads/dataally/303 London via busca](https://www.dataally.ai/blog/metas-new-metrics-and-why-the-creative-similarity-score-matters)). Também sem base oficial: "20+ ads/mês = 65% mais ROAS" e "1 ad set com 25 criativos = +17% conversões" ([chatterbuzz](https://www.chatterbuzzmedia.com/blog/meta-andromeda-creative-targeting/)).

### Inferences
- A base oficial para "criativos parecidos competem entre si / são agrupados" se resume a: (a) a frase do Andromeda de que ele "pick[s] the right creative", (b) a recomendação de diversidade com ganho de até 32% no CPA, (c) a métrica de similaridade visual de 2026. O mecanismo "ticket de leilão por Entity ID" é hipótese de mercado plausível, **não confirmada**.
- Para um briefing: chame de "orientação oficial" a diversidade de formato (imagem + vídeo + 9:16 com áudio), de mensagem e de storytelling. Chame de "prática de mercado" o diversificar por persona/ângulo/conceito e os números de 8–12 conceitos.

### Gaps
- Não achei texto oficial da Meta que use os termos "Entity ID", "persona" ou "concept" como eixos de diversidade, nem que diga quantos criativos por ad set no Advantage+ Sales (a página em pt-BR de Advantage+ Sales não dá número; ela cita só "reduzindo em 20% o custo por resultado, em média", sem metodologia — [página](https://www.facebook.com/business/ads/meta-advantage-plus/sales-campaigns)).
- Não consegui verificar no X o post de out/2025 de "jasonyimco" ("rolling out a new reporting feature…"): deu 402 e não sei se ele é funcionário da Meta.

## 3. Estrutura de campanha na era Andromeda e a visão de criativo gerado por IA

### Takeaway
A Meta empurra oficialmente para **consolidação + automação**: Advantage+ Sales com público, orçamento e posicionamentos Advantage+, e pacotes de criativo gerados por IA. Zuckerberg já falou em um modelo em que o anunciante informa objetivo e orçamento e a Meta faz o resto.

### Cited Findings
- [OFICIAL] O Advantage+ Sales exige o público Advantage+ para acessar "nossas otimizações de IA mais avançadas", junto com orçamento, posicionamentos e destino Advantage+. — [facebook.com/business Advantage+ Sales](https://www.facebook.com/business/ads/meta-advantage-plus/sales-campaigns)
- [OFICIAL] Simplificação da conta e automação são pilares do Performance 5. — [Performance marketing](https://www.facebook.com/business/ads/performance-marketing)
- [OFICIAL] Caso citado em Q2/2026: Advantage+ Sales com público, posicionamentos e orçamento Advantage+ deu "13% incremental lift in purchases and a 16% increase in add-to-cart". — [Q2 2026](https://s21.q4cdn.com/399680738/files/doc_financials/2026/q2/META-Q2-2026-Earnings-Call-Transcript.pdf)
- [OFICIAL] O Advantage+ creative "allows you to diversify and strengthen your ads' videos, text, images and audio". — [Advantage+ creative](https://www.facebook.com/business/ads/meta-advantage-plus/creative); [About Creative Enhancements](https://www.facebook.com/business/help/297506218282224)
- [OFICIAL, fala de Zuckerberg citada pela imprensa] "any business will be able to just tell us what objective they're trying to achieve … how much they're willing to pay for each result, and connect their bank account and then we just do the rest for them." — [Campaign Asia](https://www.campaignasia.com/article/zuckerberg-says-ai-could-redefine-metas-ad-business/502291). Atribuída a entrevista de maio/2025; não conferi o local exato.
- [NÃO OFICIAL] "Automação total de anúncios até o fim de 2026" vem de reportagem (WSJ, repercutida por [eWeek](https://www.eweek.com/de/news/meta-ads-ai-automation/)), não de comunicado da Meta.

### Inferences
- A direção oficial (Generative Recommender lendo o conteúdo do anúncio + Muse Image gerando variações + "creative solution" guiada por dados) indica que a Meta quer que o anunciante forneça **matéria-prima diversa** e deixe a IA gerar variantes. A diversidade feita por humanos (ângulos e mensagens diferentes) passa a ser o que a IA não replica sozinha.

### Gaps
- Não achei guia oficial de 2025–2026 com regra de "1 campanha / X ad sets / N criativos" para o Advantage+ Sales. Também não achei material do Blueprint sobre Andromeda especificamente.
