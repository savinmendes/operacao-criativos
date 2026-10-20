# Venda um produto para cinco públicos

O Meta Andromeda é, oficialmente, só o **motor de recuperação (retrieval) de anúncios**: ele reduz dezenas de milhões de anúncios candidatos a "alguns milhares" que seguem para o ranking (GEM/Lattice). A Meta liga esse motor diretamente à diversificação de criativos: ele "escolhe o criativo certo" para cada pessoa à medida que o anunciante sobe mais criativos diferentes ([Meta for Business](https://www.facebook.com/business/news/ai-innovation-in-metas-ads-ranking-driving-advertiser-performance)). Para a operação, a consequência prática é que **o criativo virou a segmentação**. Um mesmo produto vendido para públicos diferentes precisa de conceitos realmente diferentes (persona + ângulo/desejo + nível de consciência + oferta, executados em formatos e elencos visualmente distintos), não de 30 variações do mesmo vídeo com outra legenda. O que é oficial: diversificar mensagem, visual e formato, com ganho de até **32% no CPA** em campanhas com diversidade de formato e mensagem, num estudo da Meta com AppsFlyer e Dentsu ([Social Media Today](https://www.socialmediatoday.com/news/meta-shares-tips-on-best-performing-ad-approaches-ai/749897/)). O que **não** é oficial: "Entity ID", os limiares de similaridade de 60%/40% e a regra dos "8–15 conceitos por campanha". A própria Meta se recusou, em setembro de 2026, a confirmar qualquer limiar ou número ([Relevant Audience](https://www.relevantaudience.com/meta/meta-ad-creative-diversification-same-hook-same-ad/)). O estudo abaixo separa fato de folclore, mostra onde os especialistas concordam e divergem e entrega matriz, regras de diversidade, estrutura de teste por frente (COD, infoproduto, X1), checklist de lote, compliance e lista de vídeos. Nenhuma fonte trata da efetividade de entrega COD nem de VSL/quiz pós-Andromeda; essas lacunas estão marcadas.

---

## 1. Andromeda é retrieval, e o resto é interpretação de mercado

### O que a Meta publicou de fato

O post de engenharia de **02/12/2024** define o Andromeda como "a personalized ads retrieval engine". Ele seleciona entre dezenas de milhões de candidatos e repassa alguns milhares ao ranking, com **+6% de recall** e **+8% de qualidade de anúncios** em segmentos selecionados. O mesmo texto o justifica pelo volume de criativos gerados por IA: "more than 15 million ads in a month" ([Engineering at Meta](https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/)). O resumo para anunciantes de março de 2025 contém a frase que conecta tudo ao criativo: "as businesses upload more and more creatives to support a diversification strategy, Meta Andromeda works behind the scenes" ([Meta for Business](https://www.facebook.com/business/news/ai-innovation-in-metas-ads-ranking-driving-advertiser-performance)). O white paper oficial "The Creative Advantage" (22/04/2025, com versão pt-BR) afirma que o foco mudou "from niche targeting to creative diversification as the best lever to find the most relevant audiences" ([Meta for Business](https://www.facebook.com/business/news/the-creative-advantage-unlocking-the-power-of-diversification-with-meta-andromeda)).

Os ganhos oficiais são **de um dígito por modelo e por trimestre**. No Q3/2025, a fusão de retrieval com o ranking inicial deu **+14% de qualidade** nos anúncios do Facebook ([transcrição Q3 2025](https://s21.q4cdn.com/399680738/files/doc_financials/2025/q3/META-Q3-2025-Earnings-Call-Transcript.pdf)). No Q2/2026, a Meta anunciou o **Meta Generative Recommender**, com LLMs dentro do retrieval que "reason about ad content and user preferences together" ([transcrição Q2 2026](https://s21.q4cdn.com/399680738/files/doc_financials/2026/q2/META-Q2-2026-Earnings-Call-Transcript.pdf)). É a primeira declaração oficial de que o **conteúdo do anúncio** (e não só o pixel) é interpretado semanticamente na hora de decidir quem o recebe. Isso dá base à tese de que **ângulo e mensagem segmentam**, embora a Meta não detalhe o mecanismo. Promessas do tipo "o Andromeda dobrou meu ROAS" não vêm da Meta.

Pipeline, na versão oficial: **retrieval** (Andromeda e, desde 2026, Generative Recommender) → **ranking** (Lattice, GEM, Adaptive Ranking) → leilão. Uma explicação acessível dessa divisão está em [Dara Denney](https://www.youtube.com/watch?v=x1b4h42HTG8) e [Mark Builds Brands](https://www.youtube.com/watch?v=JMw6SmRdYQY).

### Oficial × mito de agência

| Afirmação que circula | Status | Evidência |
|---|---|---|
| Andromeda = retrieval que filtra dezenas de milhões → milhares | **Oficial** | [Engineering at Meta](https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/) |
| "Diversifique mensagem, visual e posicionamento" | **Oficial** (pilar do Performance 5; módulo 1 do curso Blueprint PT-BR "Boas práticas para criativos") | [Performance marketing](https://www.facebook.com/business/ads/performance-marketing); [Blueprint](https://www.facebookblueprint.com/student/path/264320-placements-formats-course) |
| Diversidade de formato + mensagem → até −32% CPA e +9% alcance incremental | **Oficial** (estudo Meta + AppsFlyer + Dentsu, 1,1 mi de variações, reportado pela imprensa) | [Social Media Today](https://www.socialmediatoday.com/news/meta-shares-tips-on-best-performing-ad-approaches-ai/749897/) |
| Anúncios que "parecem ou soam iguais" são vistos como variações do mesmo criativo | **Oficial qualitativo** (orientação de 16/12/2025, conhecida via terceiros) | [Admetrics](https://www.admetrics.io/post/meta-creative-fatigue-and-similarity-score-complete-guide) |
| Métrica de "Creative Similarity" no Ads Manager | **Recurso real, "em desenvolvimento"**, visual (imagens e miniaturas). Critério e limiares não divulgados | [note.com/sheeema_meta](https://note.com/sheeema_meta/n/ne771abb2a8b6?hl=en); [CTC](https://commonthreadco.com/blogs/coachs-corner/metas-new-creative-diversity-score-is-live-in-ads-manager-what-ecommerce-brands-must-act-on-now) |
| "Entity ID: anúncios parecidos ganham 1 só ticket no leilão" | **Mito/jargão de agência.** Não aparece no Ads Manager nem na API | [adsuploader](https://adsuploader.com/blog/meta-andromeda) (defende); [nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/) (desmente a origem); João Marcus: "não é termo oficial da Meta" ([YouTube](https://www.youtube.com/watch?v=hthAuOOeRRY)) |
| Similaridade >60% colapsa em 1 Entity ID; manter <40% | **Mito.** O número de 40% vem de uma agência (303 London) | [nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/); [dataally](https://www.dataally.ai/blog/metas-new-metrics-and-why-the-creative-similarity-score-matters) |
| "8–15 conceitos por campanha" / "10–20 por conjunto" como "recomendação da Meta" | **Heurística de praticante.** Não foi achado em página oficial. O white paper só cita a Dribbleup indo de "3-4 new creatives a week to almost 50" | [Meta for Business](https://www.facebook.com/business/news/the-creative-advantage-unlocking-the-power-of-diversification-with-meta-andromeda); Sobral atribui à Meta ([YouTube](https://www.youtube.com/watch?v=MBSws43QpeA)); Victor Rocha, a "fóruns americanos" ([YouTube](https://www.youtube.com/watch?v=putN-2I7yEE)) |
| "20+ ads/mês = 65% mais ROAS"; "25 criativos = +17% conversões" | **Dado de agência / sem fonte primária** | [CTC](https://commonthreadco.com/blogs/coachs-corner/meta-andromeda-roas-creative-strategy-2026); [chatterbuzz](https://www.chatterbuzzmedia.com/blog/meta-andromeda-creative-targeting/) |
| "Rollout global concluído em outubro de 2025" | **Não oficial.** A Meta só diz que a introdução começou no "second half of 2024" | [MTM Agency](https://themtmagency.com/blog/meta-andromeda-october-2025-update-why-creative-diversity-now-defines-ad-performance); [transcrição Q2 2025](https://s21.q4cdn.com/399680738/files/doc_financials/2025/q2/META-Q2-2025-Earnings-Call-Transcript.pdf) |

A posição da Meta em setembro de 2026, segundo a porta-voz Alisha Swinteck, é que a orientação é "deliberadamente baseada em resultado (não específica de modelo)": diversifique, teste e deixe o sistema otimizar. A Meta não detalha como representa criativos individuais e **não confirmou** a regra "mesmo visual, mesmo gancho = mesmo anúncio" ([Relevant Audience](https://www.relevantaudience.com/meta/meta-ad-creative-diversification-same-hook-same-ad/)). Conclusão operacional: tratar "Entity ID" como **metáfora útil** para o agrupamento observado, nunca como número a perseguir. O autor que reportou a métrica de similaridade recomenda explicitamente não otimizar para ela ([note.com](https://note.com/sheeema_meta/n/ne771abb2a8b6?hl=en)).

---

## 2. Os especialistas concordam no "o quê" e brigam no "quanto"

Há três consensos sólidos, presentes tanto nos canais internacionais quanto nos BR/LATAM. Primeiro, **público aberto**: interesse e lookalike viraram "sugestão", e a localização segue como controle rígido ([Ben Heath](https://www.youtube.com/watch?v=13s-G9Uj51A); [Jon Loomer](https://www.youtube.com/watch?v=bRjdTB4ajfk); [Sobral](https://www.youtube.com/watch?v=MBSws43QpeA)). Segundo, **estrutura consolidada**: poucas campanhas, poucos conjuntos, vários anúncios por conjunto. Terceiro, **conceito diferente vale mais que variação mínima**: trocar cor, título, camiseta ou música não cria anúncio novo ([Nick Theriot](https://www.youtube.com/watch?v=ZF6qAFc60yU); [Rubén Gallardo](https://www.youtube.com/watch?v=jN6xIJXZhEw); [João Marcus](https://www.youtube.com/watch?v=hthAuOOeRRY)). Um quarto consenso, mais recente, é **não desligar cedo** o anúncio que recebe verba com CPA ruim, porque ele pode estar fazendo o papel de topo de funil. Vergara chama isso de "efecto desglose" ([Vergara](https://www.youtube.com/watch?v=RJaLsOR7IUU); [Heath](https://www.youtube.com/watch?v=13s-G9Uj51A)).

As divergências são de dose e de método, e nenhuma vem com teste controlado auditável. O lado do volume (Heath, Robinson, Blue Sense, Marketero com o caso Yeti de 287 anúncios em 14 dias) enfrenta o lado de "poucos anúncios com papéis diferentes" (Charley Tichenor, Caro Dubi, Javi). O dado mais sólido dessa disputa é o benchmark da Motion (+550 mil anúncios, ~US$ 1,3 bi). A faixa Enterprise testa **6,7× mais** criativos por semana que a Micro, mas a taxa de acerto só sobe de **4,0% para 8,8%**. Volume é alavanca, mas a maioria dos testes perde de qualquer jeito ([Motion Benchmarks 2026](https://motionapp.com/library/research/creative-benchmarks-2026/testing-volume-by-tier)).

| Tema | Lado A | Lado B | Leitura para a operação |
|---|---|---|---|
| Anúncios por conjunto | 3 por conceito ([Theriot](https://www.youtube.com/watch?v=FWB6rAVm4Fk)); 2–5 ([Mark](https://www.youtube.com/watch?v=z4UAXut0kCA)); 3–6 com verba < US$ 50/dia ([Gallardo](https://www.youtube.com/watch?v=jN6xIJXZhEw); [Vergara](https://www.youtube.com/watch?v=RJaLsOR7IUU)) | 15–30 ([Robinson](https://www.youtube.com/watch?v=_-y0NZ30VKE)); 20+ ([Heath](https://www.youtube.com/watch?v=13s-G9Uj51A)); até 50 ([Loomer](https://www.jonloomer.com/meta-andromeda/)) | O número de **conceitos distintos** importa mais que o de anúncios. Com verba de país pequeno, 3–6 por conjunto |
| Separar teste e escala | Separa ([Denney](https://www.youtube.com/watch?v=7knQyPYLmfo); [Cottrell](https://www.youtube.com/watch?v=QoGFOGEqijw); [Willian Moraes](https://www.youtube.com/watch?v=tSb6jRMy6Xk); [Gallardo](https://www.youtube.com/watch?v=jN6xIJXZhEw)) | Tudo numa campanha ([Heath](https://www.youtube.com/watch?v=13s-G9Uj51A); [Tichenor](https://www.youtube.com/watch?v=E_wZJhuSK5U); [Caro Dubi](https://www.youtube.com/watch?v=uM0hTBKFb7c): "ya no se usan más") | Com verba alta, separar protege os vencedores. Com verba baixa, consolidar evita fragmentar sinal |
| ABO × CBO | ABO no teste ([Blue Sense](https://www.youtube.com/watch?v=vUbLw80KTpo): no CBO ~4% dos anúncios levam ~64% da verba; [Willian](https://www.youtube.com/watch?v=tSb6jRMy6Xk); [Andre Luiz](https://www.youtube.com/watch?v=N7-gUkiNGeE)) | CBO ([Theriot](https://www.youtube.com/watch?v=FWB6rAVm4Fk); [Mark](https://www.youtube.com/watch?v=z4UAXut0kCA); [Sobral](https://www.youtube.com/watch?v=MBSws43QpeA): "99% das vezes") | ABO para dar verba garantida a conceito novo; CBO/Advantage+ para escalar |
| Mix conceito novo × iteração | 80% conceitos novos ([Mark](https://www.youtube.com/watch?v=z4UAXut0kCA)); 50% novos/30% refino/20% vencedores ([nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/)) | 80% iteração ([Theriot](https://www.youtube.com/watch?v=FWB6rAVm4Fk)); 50–60% replicar vencedores ([Blue Sense](https://www.youtube.com/watch?v=vUbLw80KTpo)); "no castiga la iteración" ([Marketero](https://www.youtube.com/watch?v=B9-Eop8guhI)) | Iteração vale **se for visualmente distinta e tiver hipótese**. A proporção depende de já existir um vencedor |
| Trocar só o gancho | Funciona: "2 corpos + 15 ganchos" ([Blue Sense](https://www.youtube.com/watch?v=vUbLw80KTpo)); 2×10 ([Heath](https://www.youtube.com/watch?v=onFwSud9C2Y)) | Penalizado se o corpo não conversa com o gancho ([Theriot](https://www.youtube.com/watch?v=FVBOYnHL6SA)); gancho precisa ser **visualmente** diferente ([Motion](https://www.youtube.com/watch?v=aNCUFwQw524)) | Gancho novo só conta com **plano de abertura visual novo** e coerente com o corpo |
| Desligar perdedores | Não desligar por padrão ([Heath](https://www.youtube.com/watch?v=13s-G9Uj51A); [Theriot](https://www.youtube.com/watch?v=FWB6rAVm4Fk); [João Marcus](https://www.youtube.com/watch?v=hthAuOOeRRY)) | Cortar com 2× CPA sem conversão ou 7 dias ([Marketero](https://www.youtube.com/watch?v=Y3TexWZTGwk)); 2 dias sem venda ([Andre Luiz](https://www.youtube.com/watch?v=N7-gUkiNGeE)) | Julgar no nível do **conjunto**. Cortar anúncio só com critério de gasto/CPA |
| Melhorias automáticas Advantage+ Creative | Desligar ([Sobral](https://www.youtube.com/watch?v=MBSws43QpeA); [Mark](https://www.youtube.com/watch?v=z4UAXut0kCA); [Theriot](https://www.youtube.com/watch?v=FWB6rAVm4Fk)) | A Meta divulga +22% de ROAS e +11% de CTR com geração de imagem ([Engineering](https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/); [Creative Advantage](https://www.facebook.com/business/news/the-creative-advantage-unlocking-the-power-of-diversification-with-meta-andromeda)) | Em saúde/estética, deixar desligado: a IA pode reescrever promessa e quebrar compliance |
| "Nada mudou" | Mudou tudo (maioria) | [Andre Luiz](https://www.youtube.com/watch?v=N7-gUkiNGeE); [Marketero](https://www.youtube.com/watch?v=B9-Eop8guhI): "evolución, no revolución"; [El Poder del eCommerce](https://www.youtube.com/watch?v=CPuPN572FnI) | Quem já renovava conceitos com frequência sente pouco. Quem vivia de 3 criativos sente muito |

Os céticos merecem registro. Aazar Ali Shad chama o Andromeda de "snake oil", e Jess Bachman diz que na Black Friday ganha a oferta, não o criativo ([Motion](https://motionapp.com/blog/andromeda-impact-on-bfcm)). Barry Hott resume a postura mais útil: "It's probably not Meta's fault. It's probably your fault" ([YouTube](https://www.youtube.com/watch?v=s4mLWmECoKI)). Ele também tira print diário da página de destino, porque mudanças no site explicam muitas quedas atribuídas ao "algoritmo" ([Ecomm Cowboy](https://www.youtube.com/watch?v=m8dbcF407H8)).

---

## 3. Um produto vira vários conceitos quando persona, ângulo e consciência mudam juntos

### O modelo de conceito que todas as escolas compartilham

Os frameworks divergem no nome e convergem na estrutura. Para a Blue Sense, conceito = **Persona + Ângulo + Oferta**, com Formato como 4º componente, testados nessa ordem (ângulo → oferta → persona → formato). O erro comum é começar pelo formato: "UGC não funciona; o que funciona é o que vai dentro dele" ([YouTube](https://www.youtube.com/watch?v=vUbLw80KTpo)). João Marcus repete a fórmula em português ([YouTube](https://www.youtube.com/watch?v=hthAuOOeRRY)). Theriot usa **Desejo × Persona × Estilo de criativo** e define avatar como estado atual → ponte (mecanismo) → estado desejado. No caso relatado por ele, "só achar um avatar novo" levou uma loja de **US$ 186 mil para US$ 444 mil/mês** ([YouTube](https://www.youtube.com/watch?v=c6sXbfoRPR0)), relato anedótico. Dara Denney organiza a diversidade em uma escada: formato → nível de consciência → desejos → personas e casos de uso → diversidade "verdadeira" com orgânico e celebridades ([YouTube](https://www.youtube.com/watch?v=ZydGeio1DGQ)). Sarah Levinger troca o funil TOFU/MOFU/BOFU por quatro estados mentais (Gatilho → Exploração → Avaliação → Compra) e propõe etiquetar todo anúncio pela fase ([YouTube](https://www.youtube.com/watch?v=po85BKDTG-Y); [Motion Library](https://motionapp.com/library/talk/the-customer-psychology-research-system-that-powers-winning-ads-sarah-levinger/)). A Motion junta tudo num "Creative Strategy Engine": âncora em dor ou desejo → personas ligadas → ângulo em cada interseção → 5 níveis de consciência → ganchos e formatos ([Motion](https://motionapp.com/library/frameworks/creative-strategy-engine)).

A própria Meta tem um exemplo oficial do princípio. A geração de imagem do Advantage+ "crea varias versiones diferentes de un anuncio, cada una diseñada para atraer a un tipo específico de cliente", ilustrado com fones de ouvido para amantes de moda, de música e viajantes ([About Meta LTAM](https://about.fb.com/ltam/news/2025/10/performance-basado-en-ia-para-hoy-y-el-futuro/)). É a versão oficial de "um criativo por persona".

Os casos mais ilustrativos de mesmo produto com outro público vêm de praticantes. Um spray de hálito trocou "homens querendo beijar" por "fumantes de charuto cuja esposa odeia o hálito", e o CPA caiu de **US$ 63 para ~US$ 35** ([Theriot](https://www.youtube.com/watch?v=ZF6qAFc60yU)). As meias de alpaca da Hollow Socks rodam três ângulos: caçadores, durabilidade e "não precisa de uma gaveta cheia de meias" ([Perpetual Traffic](https://www.youtube.com/watch?v=xn8T0sKSFO8)). A Quince usou pilotos de avião para vender malas ([Ecomm Cowboy](https://www.youtube.com/watch?v=m8dbcF407H8)). Mark Builds Brands lembra que **o elenco segmenta**: uma mulher de 55 anos no vídeo puxa a entrega para mulheres mais velhas ([YouTube](https://www.youtube.com/watch?v=JMw6SmRdYQY)). Barry Hott estende essa relevância a sotaque, idade e aparência, e exige que ela continue na página ([YouTube](https://www.youtube.com/watch?v=s4mLWmECoKI)). Para LATAM, Andrey Business insiste em **voz com sotaque local** e coerência entre anúncio, copy e landing ([YouTube](https://www.youtube.com/watch?v=IjF_AyBv1Ik)).

O único caso com métrica antes/depois de uma estratégia "conceito primeiro" é de agência e mede o pacote inteiro (volume + diversidade + estrutura consolidada), sem isolar persona. A Direct Vacuums, com a agência Ayko, rodou 4–6 conceitos novos por semana, 3–5 variações cada e avaliação em 7 dias. Em 4 semanas, teve **CPA −25,1% e ROAS +48,2%** ([Ayko](https://www.ayko.com/blog/reducing-cpa-by-25-through-an-andromeda-first-creative-led-paid-social-strategy)).

### Matriz persona × ângulo × formato (pronta para preencher)

Cada linha é **um conceito** (vai para o próprio conjunto ou, em verba baixa, para o mesmo conjunto com etiqueta própria). Cada conceito tem 2–3 **execuções visualmente distintas**: outro elenco, cenário ou formato. A taxonomia de ângulos é a de Andrey Business ([YouTube](https://www.youtube.com/watch?v=IjF_AyBv1Ik)); os níveis de consciência são de Schwartz, aplicados como em [Victor Rocha](https://www.youtube.com/watch?v=lm9FXO4N99E) e [Segwise](https://segwise.ai/blog/advertising-awareness-levels-2026); os estados mentais são os de [Levinger](https://www.youtube.com/watch?v=po85BKDTG-Y).

| ID | Frente / país | Persona (identidade + micro-momento, não demografia) | Ângulo (dor/alívio, aspiração/status, prova/autoridade, mecanismo, ocasião, oferta, quebra de objeção, comparativo, identidade/tribo, rotina, sensorial) | Desejo central | Nível de consciência (inconsciente → problema → solução → produto → pronto) | Estado mental (Gatilho/Exploração/Avaliação/Compra) | Formato 1 | Formato 2 | Formato 3 | Elenco/voz (idade, sotaque) | Gancho visual de abertura | Oferta / CTA | Risco de compliance | Hipótese em 1 frase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | | | | | | | | | | | | | | |
| C02 | | | | | | | | | | | | | | |
| C03 | | | | | | | | | | | | | | |

**Exemplo genérico** (produto fictício "Produto X", um item de uso doméstico; sem dados reais de produto, preço ou resultado):

| ID | Persona | Ângulo | Consciência | Formato 1 / 2 / 3 | Elenco | Abertura visual | Hipótese |
|---|---|---|---|---|---|---|---|
| C01 | Pessoa que mora sozinha e tem pouco tempo no fim do dia | Rotina (economiza tempo) | Consciente do problema | UGC talking head / tela dividida antes×depois de uso / estático "nota no celular" | Adulto 25–35, sotaque local | Pessoa chegando cansada em casa | Quem sente falta de tempo responde a "menos 20 minutos de tarefa" mais que a especificação técnica |
| C02 | Quem já comprou similar barato e se arrependeu | Comparativo / quebra de objeção | Consciente da solução | Demonstração lado a lado / carrossel "3 erros" / depoimento | Adulto 35–50 | Produto concorrente genérico quebrando | Quem já se frustrou precisa de prova de diferença, não de apresentação |
| C03 | Quem compra presente | Ocasião (presente) | Consciente do produto | Unboxing / estático com selo de oferta / vídeo curto de reação | Casal ou família | Caixa sendo aberta | Na ocasião, a decisão é sobre o outro, e o gatilho é a data |
| C04 | Desconfiado de compra online | Oferta (paga ao receber, se for COD) | Pronto para comprar | Entregador entregando + pagamento / print de conversa / depoimento local | Pessoa comum, sotaque local | Campainha / entrega na porta | O risco percebido trava a compra, e "pago contra entrega" é o ângulo, não o rodapé |

O C04 segue a observação de que, em COD, "pago contra entrega" é um **ângulo de oferta**, não só uma linha da copy ([Andrey Business](https://www.youtube.com/watch?v=IjF_AyBv1Ik); [blog](https://www.andreybusiness.com/blog/dropshipping-contra-entrega-guia-definitiva-2026)). Em X1 After-Pay o equivalente é "recebe antes, paga depois"; em infoproduto, a garantia.

---

## 4. Diferente de verdade é outra cena, outra pessoa ou outra promessa

Como a Meta não publica o critério, a regra prática vem do que agências e praticantes observam e do pouco que a Meta confirmou: anúncios que "parecem ou soam iguais" viram variações do mesmo criativo ([Admetrics](https://www.admetrics.io/post/meta-creative-fatigue-and-similarity-score-complete-guide)). A métrica oficial de similaridade é descrita como **visual** ("how visually diverse your images and videos are") ([note.com](https://note.com/sheeema_meta/n/ne771abb2a8b6?hl=en)). Já o Generative Recommender lê o conteúdo ([Q2 2026](https://s21.q4cdn.com/399680738/files/doc_financials/2026/q2/META-Q2-2026-Earnings-Call-Transcript.pdf)). Por isso, a diferença segura é a que muda **visual e mensagem ao mesmo tempo**. Felipe Vergara mostra um slide atribuído a um representante da Meta com três níveis: mesma imagem com texto parecido = diversidade mínima; mesma imagem com mensagem diferente = diferenciado; imagem e mensagem diferentes = máximo ([YouTube](https://www.youtube.com/watch?v=RJaLsOR7IUU)). O post original não foi localizado.

| Mudança | Conta como criativo diferente? | Fonte |
|---|---|---|
| Trocar cor, fonte, título, uma palavra, música de fundo | **Não** | [Tryatria](https://www.tryatria.com/blog/andromeda-meta-ads); [nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/) |
| Mesma filmagem com legenda/texto na tela novo | **Não** | [nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/); [CTC](https://commonthreadco.com/blogs/coachs-corner/metas-new-creative-diversity-score-is-live-in-ads-manager-what-ecommerce-brands-must-act-on-now) |
| Mesmo talento, cenário e enquadramento com roteiro revisado | **Não** | [nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/) |
| Mesma pessoa trocando só a camiseta e repetindo a fala | **Não** ("mesmo conceito") | [Sobral](https://www.youtube.com/watch?v=MBSws43QpeA); [João Marcus](https://www.youtube.com/watch?v=hthAuOOeRRY) |
| Re-subir, limpar metadados | **Não** | [João Marcus](https://www.youtube.com/watch?v=hthAuOOeRRY) |
| Gancho só em texto sobre a mesma abertura | **Não** | [Motion](https://www.youtube.com/watch?v=aNCUFwQw524); [Theriot](https://www.youtube.com/watch?v=FVBOYnHL6SA) |
| Gancho com **plano de abertura visual novo**, coerente com o corpo | **Provavelmente sim** | [Blue Sense](https://www.youtube.com/watch?v=vUbLw80KTpo); [Heath](https://www.youtube.com/watch?v=onFwSud9C2Y) |
| Outra pessoa (idade, etnia, corpo), outro cenário | **Sim**, com intenção. Trocar para uma mulher de 50 anos na menopausa já é **persona nova** | [Theriot](https://www.youtube.com/watch?v=FVBOYnHL6SA) |
| Outro formato (talking head × demo × carrossel × estático) | **Sim** | [nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/); [Denney](https://www.youtube.com/watch?v=ZydGeio1DGQ) |
| Voz diferente, ou narração × silêncio; estrutura narrativa diferente | **Sim** | [nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/) |
| Outra proposta de valor / desejo / nível de consciência / persona | **Sim** (é conceito novo) | [Theriot](https://www.youtube.com/watch?v=ZF6qAFc60yU); [Blue Sense](https://www.youtube.com/watch?v=vUbLw80KTpo) |

Para o lote, use a regra da CTC: **cada família criativa difere das outras em pelo menos 2 dimensões** (formato, identidade visual, mensagem principal), com no mínimo 4 famílias ([CTC](https://commonthreadco.com/blogs/coachs-corner/metas-new-creative-diversity-score-is-live-in-ads-manager-what-ecommerce-brands-must-act-on-now)). Dois testes rápidos ajudam. O primeiro é a grade de primeiros quadros: se as aberturas são indistinguíveis numa grade, provavelmente são uma entidade ([nikhil.pro](https://nikhil.pro/meta-ads-creative-similarity-explained/)). O segundo é observar a entrega: quando quase todo o gasto vai para 1–2 anúncios e os outros, que são variações deles, quase não recebem impressão, há **indício** (não prova) de agrupamento. Frequência acima de 2 em público frio também sinaliza falta de diversidade ([Blue Sense](https://www.youtube.com/watch?v=vUbLw80KTpo)).

Isso tem impacto direto no kit de edição da operação. A matriz gancho × corpo (`gerar_variacao.py`) continua útil, desde que cada gancho use **cenas de abertura diferentes do banco** e fale do mesmo assunto do corpo. Variações que só trocam a legenda do gancho sobre o mesmo plano tendem a ser agrupadas.

---

## 5. Teste e escala precisam de regras diferentes em COD, infoproduto e X1

Os números abaixo vêm de praticantes e servem de ponto de partida para calibrar com dados próprios. A Meta oficialmente só fornece a ferramenta nativa de **Creative testing** (2 a 5 anúncios, 7 dias por padrão, recomendação de **no máximo 20% do orçamento**) ([Jon Loomer](https://pubcast.jonloomer.com/make-creative-testing-part-of-your-process/); [Heath](https://www.youtube.com/watch?v=onFwSud9C2Y)) e a regra histórica de ~50 conversões por semana para sair do aprendizado, citada por [Javi](https://www.youtube.com/watch?v=RLUe92LCmfk) e não reverificada.

### Base comum a todas as frentes

| Parâmetro | Valor de partida | Fonte |
|---|---|---|
| Verba por conjunto de teste | ≥ 3× o CPA-alvo | [Willian Moraes](https://www.youtube.com/watch?v=tSb6jRMy6Xk) |
| Janela de julgamento | 7 dias (blocos de 7 dias) | [Willian](https://www.youtube.com/watch?v=tSb6jRMy6Xk); [Gallardo](https://www.youtube.com/watch?v=jN6xIJXZhEw); [Ayko](https://www.ayko.com/blog/reducing-cpa-by-25-through-an-andromeda-first-creative-led-paid-social-strategy) |
| Corte de anúncio/conceito | Gasto de 2× o CPA-alvo sem conversão, **ou** 7 dias sem conversão | [Marketero](https://www.youtube.com/watch?v=Y3TexWZTGwk) |
| Escala | +10% de 1 a 3×/semana (−15% se passar do CPA) ou +20% a cada ~4 dias | [Marketero](https://www.youtube.com/watch?v=Y3TexWZTGwk); [Willian](https://www.youtube.com/watch?v=tSb6jRMy6Xk); [El Poder del eCommerce](https://www.youtube.com/watch?v=CPuPN572FnI) |
| Pré-requisito para escalar | ≥ 4 vencedores diferentes entre si | [Marketero](https://www.youtube.com/watch?v=Y3TexWZTGwk) |
| Volume de teste por porte (benchmark) | Gasto < US$ 10 mil/mês: ~2,8 criativos/semana (acerto 4,0%); US$ 10–50 mil: ~4,1/semana (6,4%) | [Motion](https://motionapp.com/library/research/creative-benchmarks-2026/testing-volume-by-tier) |
| Volume mensal recomendado | < US$ 10 mil: 8–12 conceitos distintos/mês; US$ 10–50 mil: 15–25/mês | [CTC](https://commonthreadco.com/blogs/coachs-corner/meta-andromeda-roas-creative-strategy-2026) |
| Teste de detalhe (gancho, cor, texto) | Ferramenta Creative testing, 2–5 versões, métrica CPA/CPL | [Heath](https://www.youtube.com/watch?v=onFwSud9C2Y) |
| Não fazer | Anúncio novo contra vencedor com histórico; adicionar anúncio em conjunto que está batendo meta | [Motion/Prevot](https://motionapp.com/blog/ultimate-guide-creative-testing-2025); [Blue Sense](https://www.youtube.com/watch?v=vUbLw80KTpo) |

Com taxa de acerto de 4–6% nas faixas menores, a conta é de cerca de **1 vencedor a cada 16–25 criativos testados**, inferência a partir de [Motion](https://motionapp.com/library/research/creative-benchmarks-2026/testing-volume-by-tier). Isso justifica produzir em lote e orçar o lote, não o criativo avulso.

### COD (Chile, Colômbia, México, Guatemala, Romênia)

A fonte mais específica é Andrey Business (Dropi, contra entrega LATAM). Por produto, ele usa uma campanha ou conjunto com **8–12 anúncios ativos, 4–6 ângulos distintos × 2–3 variantes**. O ângulo que passar de **60% do gasto** é "graduado" para campanha própria. Entra criativo novo toda semana, a atribuição é 7d clique / 1d view e os posicionamentos são Advantage+ ([YouTube](https://www.youtube.com/watch?v=IjF_AyBv1Ik)). Os guardrails de funil COD que ele dá: **CTR > 0,8%**, thumbstop de 35–45%, retenção > 25%, pedidos iniciados de **10–12%** das visitas e conversão **> 3%** (~2,1–2,2% em produtos caros). O blog dele pede **8–15 criativos novos/mês** para contas de 2.000–3.000 €/mês ([Andrey Business](https://www.andreybusiness.com/blog/dropshipping-contra-entrega-guia-definitiva-2026)). Javi usa uma variação: teste CBO com **um conjunto por ângulo** (≥ 4 ângulos × 3–5 criativos, ≥ 50 €/dia) e vencedores numa campanha "winner" Advantage+ com 3–5 peças ([YouTube](https://www.youtube.com/watch?v=RLUe92LCmfk)).

Estrutura sugerida (síntese, a calibrar): **uma campanha por país** (a localização é o único controle rígido que sobrou, segundo [Heath](https://www.youtube.com/watch?v=13s-G9Uj51A)) e uma campanha ou conjunto por produto. Começar com 4–6 conceitos de ângulos diferentes, 2–3 execuções cada, verba de teste ≥ 3× o CPA-alvo e julgamento em 7 dias.

O ponto crítico, que **nenhuma fonte aborda**: a Meta otimiza para o evento "Compra" (pedido), não para pedido entregue e pago. Um ângulo pode trazer pedido barato e efetividade de entrega ruim (por exemplo, compradores mais impulsivos). Por isso o CPA de decisão em COD deve ser **por pedido entregue/pago**, cruzado por ângulo com os dados de entrega, e não o CPA do gerenciador. A afirmação de que o Advantage+ "descobre compradores impulsivos" em contra entrega, atribuída por Andrey à "documentação da Meta", **não foi localizada** em fonte oficial.

### Infoprodutos (VSL + quiz + upsell; LATAM, Espanha, Worldwide)

Nenhum vídeo encontrado trata de VSL/quiz especificamente pós-Andromeda. Valem as regras gerais, com três adaptações sustentadas pelas fontes. Primeira: o roteiro de VSL fria de Robinson serve de esqueleto de anúncio (gancho emocional de 3–10 s, história de 10–30 s, problema do mecanismo, solução do mecanismo, reversão de risco, depoimentos contra objeções), dentro de uma matriz de **3 ângulos por perfil × 5–6 tipos de criativo** ([YouTube](https://www.youtube.com/watch?v=_-y0NZ30VKE)). Segunda: o quiz pode ser **formato de anúncio**, não só de funil. Levinger cita o advertorial em formato de quiz da HealthMaven funcionando com público mais velho pelo "efeito de familiaridade" ([Motion Library](https://motionapp.com/library/talk/the-customer-psychology-research-system-that-powers-winning-ads-sarah-levinger/)), o que é hipótese para as ofertas de saúde e espiritualidade. Terceira: low ticket com muito volume diário tolera estrutura própria. Andre Luiz mantém ABO 1-1-1 (um criativo por campanha), só feeds, e corta com 2 dias sem venda numa oferta de R$ 9,99 ([YouTube](https://www.youtube.com/watch?v=N7-gUkiNGeE)).

Para ticket maior, use a base comum (7 dias, 3× CPA) e decida pelo **CAC do front + upsell**, não pelo CPA do front sozinho. Essa é uma adaptação da operação, sem fonte específica. Persona aqui pode mudar a **página** também: Theriot testa 1 avatar por semana, cada um com página própria ([YouTube](https://www.youtube.com/watch?v=c6sXbfoRPR0)). Levar isso para quiz/VSL por persona é uma opção a testar.

### X1 After-Pay (nutracêutico articular, WhatsApp, Brasil, 50+)

Para campanha de mensagem, Victor Rocha usa **8–15 anúncios por conjunto**, misturando estático, carrossel e vídeo, em CBO com meta "maximizar conversas" e destino só WhatsApp. Ele agenda o início **≥ 12 h após criar**, para todos os anúncios começarem aprovados juntos, e, em vez de pausar o anúncio ruim, troca a mídia ([YouTube](https://www.youtube.com/watch?v=putN-2I7yEE)). A versão "1-1-9" dele distribui 3 imagens + 3 vídeos + 3 carrosséis pelos níveis de consciência ([YouTube](https://www.youtube.com/watch?v=lm9FXO4N99E)). João Marcus alerta contra a atribuição "1 dia de visualização" em funil de WhatsApp, onde a compra demora dias ([YouTube](https://www.youtube.com/watch?v=hthAuOOeRRY)). Para público 50+, a Blue Sense relata que **estático com copy longa e VSL "arrasam"** no feed do Facebook ([YouTube](https://www.youtube.com/watch?v=vUbLw80KTpo)), e Mark Builds Brands lembra que o elenco de idade puxa a entrega para aquela idade ([YouTube](https://www.youtube.com/watch?v=JMw6SmRdYQY)). A afirmação do Casal Raiz Ads de que a campanha de vendas para WhatsApp passou a otimizar pela profundidade da conversa **não foi verificada** ([YouTube](https://www.youtube.com/watch?v=CTY1rDZTy98)).

No X1, o CPA do gerenciador (custo por conversa) é o pior indicador de decisão. O que importa é **fechamento por closer e efetividade de pagamento pós-entrega** por ângulo. Isso exige etiquetar a origem (ID do anúncio/conceito) em cada conversa, o que é recomendação da operação, sem fonte externa.

| Item | COD | Infoproduto | X1 After-Pay |
|---|---|---|---|
| Unidade de campanha | País × produto | Oferta × mercado | Oferta (Brasil) |
| Conceitos no lançamento | 4–6 ângulos × 2–3 execuções (8–12 ativos) | 3 ângulos por perfil × formatos | 8–15 anúncios (mix estático/carrossel/vídeo) |
| Destino / evento | Página → pedido (Compra) | Quiz/VSL → checkout | WhatsApp (conversas) |
| KPI de decisão | CPA por **pedido entregue/pago** e margem | CAC front + upsell, ticket | Custo por **venda paga**; fechamento por closer |
| Guardrails de topo | CTR > 0,8%; pedidos iniciados 10–12%; conversão > 3% ([Andrey](https://www.youtube.com/watch?v=IjF_AyBv1Ik)) | Sem fonte específica: precisa de baseline próprio | Sem fonte específica: precisa de baseline próprio |
| Formatos-chave | UGC sotaque local, demo, entrega/pagamento na porta | VSL curta, advertorial/quiz, depoimento | Estático copy longa, VSL, depoimento de par etário |
| Atribuição | 7d clique / 1d view ([Andrey](https://www.youtube.com/watch?v=IjF_AyBv1Ik)) | Padrão | Evitar 1d view ([João Marcus](https://www.youtube.com/watch?v=hthAuOOeRRY)) |

---

## 6. Checklist de produção de um lote

| ✓ | Etapa | Critério de pronto |
|---|---|---|
| ☐ | **Pesquisa** | Reddit, avaliações, comentários e pesquisa com clientes lidos antes de definir formato ([Cottrell](https://www.youtube.com/watch?v=QoGFOGEqijw); [Theriot](https://www.youtube.com/watch?v=c6sXbfoRPR0)); micro-momentos anotados ([Levinger](https://motionapp.com/library/talk/the-customer-psychology-research-system-that-powers-winning-ads-sarah-levinger/)) |
| ☐ | **Frente e país definidos** | Uma frente por lote; regras e linguagem não misturadas |
| ☐ | **Personas** | 2–4 personas por identidade/micro-momento, priorizadas por dor e sazonalidade ([Theriot](https://www.youtube.com/watch?v=c6sXbfoRPR0)) |
| ☐ | **Matriz preenchida** | Cada linha com persona, ângulo, consciência, estado mental, hipótese em 1 frase |
| ☐ | **Diversidade** | ≥ 4 famílias, cada uma diferente das outras em ≥ 2 dimensões ([CTC](https://commonthreadco.com/blogs/coachs-corner/metas-new-creative-diversity-score-is-live-in-ads-manager-what-ecommerce-brands-must-act-on-now)) |
| ☐ | **Mix de formatos** | Imagem + vídeo + vídeo 9:16 com áudio; ≥ 20% dos assets em 9:16 com áudio, citado como dado da Meta via imprensa ([Optimixed](https://www.optimixed.com/meta-shares-ad-tips-based-on-1-million-ad-creatives/)) |
| ☐ | **Elenco e voz** | Idade, sotaque e aparência coerentes com a persona e o país |
| ☐ | **Ganchos** | Cada gancho com plano visual de abertura próprio e coerente com o corpo |
| ☐ | **Grade de primeiros quadros** | Nenhum par de aberturas indistinguível |
| ☐ | **Página/destino coerente** | A promessa e a persona do anúncio continuam na página, no quiz ou na saudação do WhatsApp ([Hott](https://www.youtube.com/watch?v=s4mLWmECoKI)) |
| ☐ | **Compliance** | Checagem da seção 8; riscos listados para a pessoa decidir manter × suavizar |
| ☐ | **Revisão técnica** | `revisar_ad.py` e skill `revisar-criativo` (resolução ≥ 720p, áudio, quadros soltos, termos proibidos) |
| ☐ | **Nomenclatura** | Nome do anúncio carrega conceito, persona, ângulo e formato (ex.: `C03_presente_ocasiao_unboxing_v1`), para analisar por eixo |
| ☐ | **Configuração** | Melhorias automáticas Advantage+ Creative desligadas (saúde/estética); início agendado; atribuição conferida por frente |
| ☐ | **Plano de leitura** | Data de julgamento (D+7), KPI de decisão da frente e critério de corte registrados antes de subir |

---

## 7. Os erros que mais custam são variações clonadas e decisões apressadas

O erro número um é subir dezenas de variações quase iguais. Na formulação da Tryatria, 50 variações com mesmo gancho e mesma oferta viram "50 anúncios competindo por 1 vaga" ([Tryatria](https://www.tryatria.com/blog/andromeda-meta-ads)); Cottrell diz que 50 variações do mesmo UGC "destroem a conta" ([YouTube](https://www.youtube.com/watch?v=QoGFOGEqijw)). O segundo é **fragmentar a estrutura**: empilhamento de públicos e remarketing em camadas foram apontados como causa de sobreposição no caso Ayko ([Ayko](https://www.ayko.com/blog/reducing-cpa-by-25-through-an-andromeda-first-creative-led-paid-social-strategy)). A estrutura 1-3-1 de teste "já está sendo punida", segundo [Victor Rocha](https://www.youtube.com/watch?v=lm9FXO4N99E). O terceiro é **confundir filtragem por similaridade com fadiga** e "refrescar" com variações, quando a saída é criador, cenário e formato novos ([Playbook](https://playbooknewsletter.beehiiv.com/p/creative-fatigue-isn-t-the-problem)). O quarto é **comparar novos contra vencedores com histórico**, ou pausar os antigos ao subir novos ([Motion/Prevot](https://motionapp.com/blog/ultimate-guide-creative-testing-2025)). O quinto é **começar pelo formato** em vez do ângulo ([Blue Sense](https://www.youtube.com/watch?v=vUbLw80KTpo)). O sexto é **mirar o nível de consciência errado**, falando de produto com quem ainda não reconhece o problema ([Segwise](https://segwise.ai/blog/advertising-awareness-levels-2026)). O sétimo é **escalar agressivamente**: um caso dobrou verba toda semana e caiu porque "o público é finito… mesmos criativos" ([Leandro Pitelli](https://www.youtube.com/watch?v=W5fXoIeW2G0)). O oitavo é **culpar o algoritmo** sem checar página, oferta e sazonalidade ([Hott](https://www.youtube.com/watch?v=s4mLWmECoKI); [Sobral](https://www.youtube.com/watch?v=MBSws43QpeA): "ocorrência e causalidade não são a mesma coisa").

Há dois erros específicos da operação, inferidos e sem fonte externa. Em COD e X1, **decidir pelo CPA do gerenciador** premia ângulos que geram pedido ou conversa e não geram pagamento. E é preciso evitar o **ângulo de persona "doente" em 2ª pessoa**, que quebra compliance (seção 8) e pode tirar a conta do ar.

---

## 8. Compliance Meta para saúde, suplemento, estética e público 50+

Com a otimização de fundo de funil potencialmente restrita para saúde e a segmentação por interesse sensível bloqueada, **o criativo vira o principal segmentador** nesse nicho, e a forma de falar com a persona precisa respeitar a política. As regras abaixo vêm de fonte secundária; a página oficial da Meta retornou 404 na pesquisa e precisa de **revisão manual** na versão vigente.

| Regra | O que significa na prática | Fonte |
|---|---|---|
| **Atributos pessoais** | Proibido afirmar ou insinuar que o usuário tem uma condição ("sua dor no joelho", "você tem artrose?"). Escrever em 3ª pessoa/narrativa: "muita gente depois dos 50 relata…", ou depoimento de personagem | [Accelerated Digital Media](https://www.accelerateddigitalmedia.com/insights/guide-to-social-media-health-ad-restrictions-2026/) |
| **18+** | Produtos de dieta, saúde, emagrecimento e suplementos direcionados a 18+ | [Meta Transparency (via snippet)](https://transparency.meta.com/policies/ad-standards/objectionable-content/personal-health-and-appearance) |
| **Antes/depois** | Permitido para procedimentos/produtos **cosméticos** (18+); **proibido** em emagrecimento | [Meta Transparency (via snippet)](https://transparency.meta.com/policies/ad-standards/objectionable-content/personal-health-and-appearance) |
| **Promessa de cura** | Não alegar "curar/sanar/eliminar" doença incurável; "tratar ou controlar sintomas" é permitido | [Accelerated Digital Media](https://www.accelerateddigitalmedia.com/insights/guide-to-social-media-health-ad-restrictions-2026/) |
| **Sinais de dados de saúde** | Públicos personalizados com nome que implique condição (ex.: "arthritis_interest_list") e conversões personalizadas com desfecho de saúde no nome foram desativados; otimização para compra pode ser restrita a marcas de saúde | [Accelerated Digital Media](https://www.accelerateddigitalmedia.com/insights/guide-to-social-media-health-ad-restrictions-2026/) |
| **Padrões de publicidade** | Módulo 3 do curso Blueprint PT-BR "Boas práticas para criativos" | [Blueprint](https://www.facebookblueprint.com/student/path/264320-placements-formats-course) |

Aplicação por oferta, como inferência a revisar. No **articular X1 (50+)**, persona por situação ("avô que voltou a brincar no chão com o neto") e não por diagnóstico, sem promessa de cura e sem nomear público ou evento com o nome da condição. Na **saúde auditiva (infoproduto)**, mesma lógica de 3ª pessoa e de "sintoma", não "cura". Na **estética/glúteos**, antes/depois só se for resultado cosmético e com 18+. Na **espiritualidade**, evitar por precaução a 2ª pessoa sobre a fé ou a situação do usuário. As fontes lidas não detalham como a política trata crença religiosa, então isso **precisa de revisão manual**. Pela regra interna, **suavizar promessa é decisão da pessoa**: listar riscos e perguntar manter × suavizar. Para formatos 50+, o "insight geracional" de Levinger (advertorial com cara de matéria, quiz, depoimento de par etário) é a hipótese mais bem fundamentada encontrada ([Motion Library](https://motionapp.com/library/talk/the-customer-psychology-research-system-that-powers-winning-ads-sarah-levinger/)). **Não há dado** de performance 50+ pós-Andromeda.

---

## 9. Os vídeos que valem o tempo

Views e datas coletadas via yt-dlp em 09/10/2026.

### Internacionais (inglês)

| Título | Canal | Data | Views | Por que assistir |
|---|---|---|---|---|
| [Meta Ads Creative Strategy in 2026: The Full System](https://www.youtube.com/watch?v=vUbLw80KTpo) | Blue Sense Digital | 11/05/2026 | ~120,8 mil | Melhor definição de conceito (persona + ângulo + oferta + formato), ordem de teste, "2 corpos + 15 ganchos", dica para 50+ |
| [Copy This Facebook Ads Strategy… (Post-Andromeda)](https://www.youtube.com/watch?v=_-y0NZ30VKE) | Jared Robinson | 28/10/2025 | ~194,7 mil | Matriz 3 ângulos × 5–6 tipos de criativo e roteiro de VSL fria; útil para infoproduto |
| [the entire meta ads algorithm explained in 21 mins](https://www.youtube.com/watch?v=JMw6SmRdYQY) | Mark Builds Brands | 11/05/2026 | ~190,4 mil | Leilão em 4 etapas e "o criativo é a segmentação" (o elenco puxa a idade) |
| [The BEST Facebook Ad Campaign Structure for 2026](https://www.youtube.com/watch?v=13s-G9Uj51A) | Ben Heath | 17/02/2026 | ~124,2 mil | Estrutura consolidada; localização como único controle rígido; não desligar o anúncio "de topo" |
| [The NEW WAY To Test Facebook Ads (Post Andromeda)](https://www.youtube.com/watch?v=onFwSud9C2Y) | Ben Heath | 10/02/2026 | ~92,6 mil | Como usar a ferramenta nativa Creative testing para ganchos e detalhes |
| [The 5 Levels of Creative Diversity](https://www.youtube.com/watch?v=ZydGeio1DGQ) | Dara Denney | 18/12/2025 | ~18,8 mil | Escada de diversidade: formato → consciência → desejo → persona |
| [Meta's Andromeda & GEM: Clearly Explained](https://www.youtube.com/watch?v=x1b4h42HTG8) | Dara Denney | 21/12/2025 | ~25,3 mil | Explicação clara de Andromeda/GEM/Lattice e "velocity, not volume" |
| [How To Test Facebook Ads In 2025 (Post-Andromeda)](https://www.youtube.com/watch?v=ZF6qAFc60yU) | Nick Theriot | 29/10/2025 | ~17,6 mil | Casos de troca de persona/desejo com CPA (spray de hálito) |
| [Creative Iterations To Scale Facebook Ads](https://www.youtube.com/watch?v=FVBOYnHL6SA) | Nick Theriot | 17/11/2025 | ~4,8 mil | Diferença precisa entre iteração, variação e conceito novo |
| [How To Create Avatars That Scale Facebook Ads To $500k Months](https://www.youtube.com/watch?v=c6sXbfoRPR0) | Nick Theriot | 12/06/2026 | ~4,2 mil | Plano de 4 semanas por avatar, com página própria |
| [The NEW Meta Ad Creative Strategy in 2026 (Post Andromeda)](https://www.youtube.com/watch?v=po85BKDTG-Y) | Sarah Levinger | 23/04/2026 | ~14,6 mil | Estados mentais (Gatilho/Exploração/Avaliação/Compra) para auditar lacunas do portfólio |
| [The BEST NEW Way to Test Ads on Meta in 2026](https://www.youtube.com/watch?v=QyF0V_YTwmE) | Charley T | 11/05/2026 | ~15,5 mil | Contraponto ao volume: poucos anúncios com papéis diferentes |
| [Andromeda demands this new ad structure](https://www.youtube.com/watch?v=aNCUFwQw524) | Motion | 15/01/2026 | ~3 mil | Pirâmide persona → ângulo → gancho → conceito; matriz 10 ângulos por persona |
| [Ad Relevance: What Everyone Still Gets Wrong](https://www.youtube.com/watch?v=s4mLWmECoKI) | Barry Hott | 05/05/2026 | ~1,3 mil | Relevância de elenco (idade, sotaque) do anúncio até a página |

### BR/LATAM (português e espanhol)

| Título | Canal | Data | Views | Por que assistir |
|---|---|---|---|---|
| [ALERTA ¡Meta ANDRÓMEDA cambió Facebook Ads para SIEMPRE](https://www.youtube.com/watch?v=RJaLsOR7IUU) | Felipe Vergara (CO) | 24/10/2025 | ~121 mil | Motivadores de compra como ângulo, "efecto desglose", slide de níveis de diferenciação; casos CO/PE/MX |
| [Meta Ads y por qué ANDROMEDA sube el nivel de los ANUNCIOS de DROPSHIPPING](https://www.youtube.com/watch?v=IjF_AyBv1Ik) | Andrey Business | 25/04/2026 | ~710 | **O mais útil para COD LATAM**: 8–12 anúncios, 4–6 ângulos, guardrails de funil contra entrega |
| [Andromeda, Pmax e Advantage+… Live #361](https://www.youtube.com/watch?v=MBSws43QpeA) | Canal Subido (Pedro Sobral) | 25/11/2025 | ~40 mil | Leitura do paper oficial, CBO, "trocar camiseta = mesmo conceito". Live pode sair do ar |
| [Andrômeda: Como Funciona o Algoritmo de Anúncios da Meta em 2026](https://www.youtube.com/watch?v=hthAuOOeRRY) | João Marcus | 12/08/2026 | ~14,6 mil | Conceito = persona + ângulo + oferta; desmonta "Entity ID"; atribuição em WhatsApp |
| [A Melhor Estratégia de Criativos… Pós-Andrômeda](https://www.youtube.com/watch?v=kZPmnVy2ejM) | João Marcus | 24/08/2026 | ~8,8 mil | Banco de formatos nativos; "cópia converte, formato retém" |
| [Meta ADS Andrômeda – Nova Campanha de Mensagem para WhatsApp](https://www.youtube.com/watch?v=putN-2I7yEE) | Victor Rocha | 14/10/2025 | ~11,9 mil | **Referência para X1**: estrutura de campanha de mensagem pós-Andromeda |
| [Meta ADS Andrômeda – Nova Estrutura e Otimização](https://www.youtube.com/watch?v=lm9FXO4N99E) | Victor Rocha | 21/10/2025 | ~4,5 mil | Estrutura 1-1-9 por nível de consciência |
| [TESTE DE CRIATIVOS Andrômeda](https://www.youtube.com/watch?v=tSb6jRMy6Xk) | Willian Moraes | 03/11/2025 | ~7,8 mil | Teste ABO com verba ≥ 3× CPA e 7 dias |
| [como testar criativos depois da atualização do andromeda – low ticket](https://www.youtube.com/watch?v=N7-gUkiNGeE) | Andre Luiz | 03/11/2025 | ~14,9 mil | O dissidente: ABO 1-1-1 em low ticket |
| [Cómo vender con Meta Andrómeda – Estrategia 2026](https://www.youtube.com/watch?v=uM0hTBKFb7c) | Caro Dubi | 07/12/2025 | ~26,9 mil | Leitura de anúncio por gasto, CPM e frequência; reposição por papel |
| [Meta Andromeda está destrozando tus campañas](https://www.youtube.com/watch?v=jN6xIJXZhEw) | Aprendamos Marketing (Rubén Gallardo) | 18/11/2025 | ~16,1 mil | Volumes por verba (< US$ 50/dia: 3–6 anúncios) |
| [EL SISTEMA DEFINITIVO POST-ANDRÓMEDA](https://www.youtube.com/watch?v=Y3TexWZTGwk) | Marketero | 06/05/2026 | ~7,8 mil | Regras numéricas de corte e escala |
| [Como hacer CAMPAÑAS de Facebook Ads DROPSHIPPING con ANDROMEDA](https://www.youtube.com/watch?v=RLUe92LCmfk) | Emprende con Javi (ES) | 26/12/2025 | ~955 | Teste com um conjunto por ângulo e campanha winner |

---

## 10. Lacunas e o que precisa de revisão manual

Faltam dados em sete pontos.

- **COD:** nenhuma fonte liga o Andromeda à **efetividade de entrega/pagamento**, nem discute enviar à Meta o evento de pedido entregue/pago (CAPI) como sinal de otimização.
- **Infoproduto:** nenhum vídeo trata de **VSL + quiz** pós-Andromeda.
- **50+ e saúde:** não há dados de performance pós-Andromeda para **público 50+** nem casos numéricos de saúde/suplemento.
- **Limiares de criativo:** não existem limiares públicos e confiáveis de hook rate/hold rate para matar ou escalar.
- **Conteúdo com login:** **grupos e páginas do Facebook** que exigem login não foram acessados, então o "conteúdo dentro do próprio Facebook" pedido ficou limitado às páginas oficiais públicas (about.fb.com, facebook.com/business, Blueprint).
- **Biblioteca de Anúncios:** não foi consultada para exemplos COD LATAM. Isso pode ser feito com as skills `benchmarking-mercado` e `dissecacao-de-criativo`.
- **Criadores BR conhecidos:** Leandro Ladeira, Tiago Tessmann, Rafael Kiso, Erico Rocha e outros **não têm vídeo dedicado** encontrado. Não atribuir posições a eles.

Precisam de revisão manual na conta antes de virar regra:

- as **políticas de saúde vigentes** da Meta (a página oficial deu 404);
- se as métricas **Creative Similarity / Creative Diversity** aparecem na conta (a Meta disse que os *creative insights* via API estão restritos a poucas agências);
- a página oficial "Recomendações para fadiga do criativo" (não renderizou);
- o slide de "níveis de diferenciação" atribuído a um representante da Meta (post original não achado);
- a regra de 50 conversões por semana;
- a alegação de otimização por "qualidade da conversa" no WhatsApp.

Todos os números de praticantes (3× CPA, 8–12 anúncios, guardrails de CTR, cortes, escala) são **pontos de partida a calibrar** com os dados próprios por país e oferta. Não são benchmarks.

## 11. Adendo: o método do JarBuildsBrands (31 vídeos, ago/2025 → out/2026)

Canal: [youtube.com/@JarBuildsBrands](https://www.youtube.com/@JarBuildsBrands/videos). Jar é dono de marca de roupa nos EUA, depois agência com comunidade paga. Os 31 vídeos foram transcritos (30 por legenda automática, 1 por Whisper) e lidos por completo. As fichas por vídeo estão em `research_notes/Meta Andromeda criativos por ângulo/jar_notas_A.md`, `_B.md` e `_C.md`, e as transcrições em `jar_txt/`. Os números de faturamento são dele ou de clientes, sem auditoria, e vários aparecem de forma inconsistente entre vídeos.

**O que ele acrescenta ao estudo**

- **Leitura do funil por anúncio.** É a contribuição mais útil. Cada anúncio tem uma "assinatura": o de topo gasta muito, tem CPM baixo, frequência diária de 1,00–1,10 e ROAS atribuído ruim. O de fundo gasta pouco, tem CPM alto, frequência de 1,25–1,5+ e o melhor ROAS ([the only ad creatives you need](https://www.youtube.com/watch?v=O7B6NiEReng)). Cortar o topo pelo CPA "seca o funil", e o fundo piora junto ([laziest way](https://www.youtube.com/watch?v=R7kxwvRqEyc); [full advanced breakdown](https://www.youtube.com/watch?v=IWWz-TmE6SM)). O diagnóstico vira "qual elo está fraco": falta topo → criativos de topo; falta fundo → estáticos de oferta.
- **Duas alavancas.** O criativo traz o clique certo e a oferta/página vende. Para caber no CAC do leilão, ele sobe o ticket com kits, "leve 2", brinde e garantia, e testa página e oferta por **lucro por visitante**, não por taxa de conversão ([$30k days](https://www.youtube.com/watch?v=ZDRu_jGT4H8); [small budget](https://www.youtube.com/watch?v=WCwOT0qLpQc)).
- **Mesmo produto, vários "bolsões".** Pelo caso Grüns, o mesmo suplemento é vendido para digestão, foco, usuários de GLP-1 e mães no pós-parto. Pelo caso dele, um moletom streetwear masculino × moletons combinando para casal. Trocar etnia, gênero e idade de quem aparece abre públicos novos ([$30k days](https://www.youtube.com/watch?v=ZDRu_jGT4H8); [small budget](https://www.youtube.com/watch?v=WCwOT0qLpQc)). Ele se critica por ter variado pouco a persona.
- **Ficha de conceito.** Hipótese + persona + ângulo + desejo + nível de consciência + **sofisticação de mercado** (Schwartz), com roteiro descendo a escada de consciência. Mensagem vale mais que estética: "anúncio bonito" é o erro que ele mais vê. Ele começa pelo formato barato (foto/estático) e só faz vídeo do conceito que deu sinal. Grava o mesmo roteiro com vários criadores ([my entire $1M+ ad strategy](https://www.youtube.com/watch?v=rnqKfnElMaM)).
- **Metas pela economia da unidade.** ROAS-alvo ≈ ROAS de equilíbrio × 1,2. Decide por margem de contribuição e MER (receita total ÷ gasto), não pelo ROAS da plataforma. Mantém um piso de gasto que paga o custo fixo.
- **Cadência.** Revisão semanal com 7 dias de dados, 1–2 mudanças por semana, uma variável por vez e 3–7 dias para ler o efeito.
- **Vender a sensação, não a especificação** ([stop selling products, start selling dopamine](https://www.youtube.com/watch?v=XWH-hKCKUAM), 13/03/2026; transcrito com Whisper).
  - O anúncio que emociona ou entretém é o de topo, que "destrava gasto". O anúncio básico não escala.
  - Ele mostra um esquete de humor que carrega todos os argumentos do produto.
  - Persona também pela estética e identidade (estágio 5 de sofisticação).
  - Mede a saúde da marca por busca pelo nome e tráfego direto ao longo de 30, 60 e 180 dias.
  - O humor chulo dele não serve para público 50+ e traz risco de reprovação.

**Como ele mudou (cite com data)**

| Tema | Antes | Depois |
|---|---|---|
| Variações | "pequenas variações dão opções à máquina" (22/10/2025) | "pequena variação = o mesmo anúncio"; exige conceitos visualmente diferentes (19/11/2025) |
| Volume | ~3 conceitos/semana "de sniper" (jan/2026) | 3–7, até 7–10, com IA (fev/2026); "volume **e** variedade", número absoluto de vencedores > taxa de acerto (out/2026) |
| Criativo novo | "se bate a meta, só sobe orçamento, sem criativo novo" (out/2025) | lotes semanais constantes (2026) |
| Escala | média de 3 dias × meta → +20% / +10% / manter / −20%, com média de 7 dias e piso de gasto (mar/2026) | cost cap ou ROAS mínimo no conjunto, orçamento diário inflado como teto, ajustar lance em vez de orçamento (out/2026) |
| Corte | mata e lança toda semana (mar/2026) | "eu não mato anúncios": um anúncio de ROAS 1,68 com US$25 mil de gasto fica no ar (out/2026) |
| Estrutura | várias campanhas por objetivo (evergreen, drop, catálogo) | 1 CBO por objetivo, conjuntos só quando a economia muda, sem campanha de teste, muitos anúncios por conjunto (out/2026) |

**O que transfere e o que não transfere**

- **Transfere para as três frentes:** diversidade por persona e elenco, mapa topo/meio/fundo por anúncio, não cortar o topo pelo CPA, ficha de conceito com sofisticação, oferta para subir ticket (kit e "leve 2" no COD e no X1, order bump/upsell no infoproduto) e cadência estável.
  - O ângulo de **confiança** ("marca de Instagram não entrega") é diretamente o ângulo "paga ao receber" do COD e do after-pay, e pesa mais no público 50+.
- **Não transfere sem adaptação:**
  - "Moda é simples, não precisa de roteiro": saúde, nutracêutico e infoproduto precisam de mecanismo, prova e quebra de objeção.
  - Os limiares dele (US$50–100/dia, MER 3–3,2, CAC US$40–60) são calibrados para ticket de US$58–200, pré-pago, nos EUA.
  - Os casos de out/2026 são de clientes da agência.
- **Cost cap e "não matar" no COD e no X1:** só funcionam se o evento otimizado representar dinheiro de verdade. O lance precisa embutir a efetividade (CPA por pedido aceitável = CPA por entrega paga aceitável × efetividade). Sem devolver ao Meta a conversão confirmada (entrega paga ou venda fechada, via API de conversões), o lance otimiza para pedido ou lead. A média de 3 dias também engana quando a entrega só confirma depois. Esta adaptação é da operação, não do Jar.
- **Lacuna:** ele não mostra como calibrar o lance do cost cap (diz que está na comunidade paga). É o ponto mais arriscado de copiar sem teste próprio.

## Conclusão

A mudança real não é técnica, é de quem segmenta. A Meta tirou do gestor o controle fino de público e o devolveu dentro do criativo: idade e sotaque de quem aparece, a dor que o gancho nomeia, a promessa que o corpo sustenta. Com o Generative Recommender lendo o conteúdo do anúncio desde 2026, essa tendência só se aprofunda. Para uma operação que vende o mesmo produto em cinco países e três modelos de negócio, a unidade de trabalho deixa de ser "o criativo" e passa a ser **o conceito com hipótese escrita**, produzido em lote, nomeado por eixo e julgado pelo resultado que paga a conta (pedido entregue em COD, CAC com upsell em infoproduto, venda paga no X1), não pelo CPA que o gerenciador mostra.

A segunda implicação é defensiva. Como a Meta não publica limiares e as agências preenchem o vácuo com números inventados, a vantagem está em medir a própria conta: etiquetar cada anúncio por persona, ângulo, consciência e formato e ler os resultados por eixo depois de alguns lotes. Esse banco interno vai responder melhor que qualquer "60%/40%" ou "8–15 conceitos" quais personas abrem mercado em cada país. Em saúde, ele também mostra até onde dá para falar com a dor sem pisar na política de atributos pessoais.
