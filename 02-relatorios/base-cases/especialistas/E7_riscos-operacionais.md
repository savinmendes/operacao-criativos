# E7 · Riscos operacionais
Base: 37 episódios citados (#127 #128 #130 #132 #133 #134 #135 #136 #137 #138 #139 #140 #141 #144 #145 #146 #147 #148 #149 #150 #152 #153 #154 #155 #157 #158 #159 #160 #162 #164 #168 #170 #171 #173 #174 #175 #177), de 49 · atualizado em 2026-10-17

> **Viés de sobrevivente:** a base só tem quem deu certo e topou falar, e o canal (VTurb) vende ferramenta para esse mercado: anfitriões e convidados também vendem contas de anúncio (#149 2:34:51), cloaker (#160 2:18:36), ofertas a afiliados (#136 6:49) e mentoria. Quem quebrou por bloqueio ou reembolso quase não está aqui; os fracassos aparecem só quando contados por quem se recuperou (#137 17:07, #177 1:53:10).
>
> **Como ler:** tags «E7» das fichas antigas misturam «erros gerais». Este dossiê foi montado por busca direta nas transcrições (bloqueio, contingência, gateway, chargeback, reembolso, cloaker, compliance, dependência, sócio/caixa). Número = «declarado», nunca benchmark. Termos de legenda automática corrigidos pelo contexto quando óbvio.

## Em 10 linhas (o que a base diz)
- Queda de conta de anúncio é custo de operar, não acidente: «bloqueio você sempre vai sofrer, black ou white; a questão é em quanto tempo e como lida» — #136 1:09:38. Em escala alta, o limite é a conta que aguenta verba — #168 2:49:20.
- A defesa que mais aparece é **isolar estruturas** (BM, conta, domínio, página, perfil, proxy/IP próprios) para que uma queda não leve o resto — #160 2:16:33, #168 1:42:31, #136 52:50, #145 46:20, #159 4:15:27.
- **Histórico de conta importa**: contas com tempo e gasto caem menos (agência, comprada com gasto, ou aquecida) — #168 1:44:05, #145 45:49, #149 2:40:35, #140 3:17:26. Mas quem vende conta (#149) e quem usa farm (#145, #160) discordam de qual vale a pena (ver Discordâncias).
- **Reembolso + chargeback** é o risco de caixa central do produtor de infoproduto/nutra: 22–23% num mês, com milhões de prejuízo, é declarado por dois operadores — #136 48:09, #132 50:32. Chega a vir por até 6 meses — #136 48:40.
- A resposta é **operacional**: time de atendimento tratado como vendedor, com meta de reversão (30% → 62% declarado) — #132 1:46:39; e-mails/SMS/entregáveis melhores — #133 1:22:23, #160 2:27:28, #153 1:06:15. Atrito no pedido de reembolso também (#132 1:59:06).
- O gateway/plataforma é parte do risco: chargeback alto «pune» o produtor também no Stripe — #159 40:56; plataformas diferem em reverter reembolso (Cartpanda sim, Digistore/ByGoods quase não) — #132 1:49:46; gateway com taxa de chargeback entra na conta do ROAS — #134 2:20:39.
- **Cloaker, anti-spy, catálogo para «aprovar criativo agressivo», cloaker de áudio** são rotina em parte da base (#149 2:02:47, #160 2:19:07, #145 1:44:13) e tratados como hack de sustentação duvidosa por outra parte (#147 2:16:21).
- Quem opera com marca/produto de verdade diz ter atendimento humano de plataforma (Google em 24 h, #147 1:33:04) e menos bloqueio depois de gastar (#140 3:17:26); o contra-exemplo é conta nova rejeitando tudo no início (#140 3:17:26).
- Dependência de uma só fonte, uma só oferta, um só expert ou um só sócio aparece como causa de quebra em casos contados na primeira pessoa — #137 17:07, #177 1:53:10, #164 17:14, #157 16:28.
- Compliance de promessa/saúde quase não é discutido; aparece de lado: «sem promessa absurda e sem pessoas sem autorização» dura mais (#136 1:09:38); regras de plataforma exigem checar a página (#162 2:14:55); UE exige reformular produto e VAT (#144 1:05:12).

## Teses e práticas (agrupadas por subtema)

### 1. Estrutura anti-queda: isolar e lateralizar
- **O que dizem:** «cada conta tem um domínio, uma página, um perfil; separa todas as informações» para o Facebook não ligar as contas (#160 2:16:33). Ter «vários prédios» (domínio + conta + páginas + VSL próprios) para recriar a mesma oferta se uma cair (#160 55:02). Uma BM com contas, outra BM com outras contas e domínios diferentes: «quando caía uma, a outra ficava de pé» (#168 1:42:31). Afiliados top gastaram US$ 300–400 mil só em contenção de ativos (declarado) e testam a oferta em 10 contas (#136 52:50). Princípios são universais entre fontes: cartão, domínio, proxy, e-mail são os pontos de cruzamento (#145 46:20).
- **Condição em que vale:** escala alta de verba por dia em nutra/infoproduto agressivo, Meta/TikTok/Google, operador brasileiro. Em fonte «gerenciada» (native), todas as contas são iguais e aquecimento não existe (#170 32:49).
- **Força da evidência:** **convergente** (#160, #168, #145, #136, #159 4:15:27).

### 2. Conta de agência × comprada × farm × aquecida (origem das contas)
- **O que dizem:** ver tabela em «Onde discordam». Fatos que convergem: conta nova ligada a cartão/pixel no mesmo dia tende a cair (#145 1:36:21); aquecer e tracionar aos poucos reduz queda (#168 1:43:34, #160 2:17:04); mentalidade é «parecer usuário comum, não o cara com milhares de contas» (#145 53:38); o TikTok marca padrão repetido de criativo/página/avatar (#145 54:09); Wi-Fi compartilhado entre perfis pode gerar banimento (#160 2:16:00).
- **Condição:** operação já validada, que perde venda quando a conta cai (#160 2:17:04). Dropshipping «não precisa de contingência tão forte» quanto o nível de escala de nutra, segundo quem passou pelos dois (#160 21:38).
- **Força da evidência:** **convergente** para «histórico reduz queda» (#168, #145, #149, #140, #160); **declarado** nas diferenças de custo/benefício.

### 3. Diagnóstico e redução da taxa de queda
- **O que dizem:** derrubar conta de propósito para descobrir o motivo e testar a correção: a metade das contas caindo passou para 10% — #168 1:51:24. Teoria de dois robôs do Google (varredura ampla, depois minuciosa), com troca de anúncio antes de horários de queda — #168 2:05:21. Regra automática de 3 rejeições: criativo reprovado 3 vezes não sobe mais — #155 1:33:53. Reeditar criativo reprovado (blur no início, espelhar, tirar legenda, limpar metadados) — #145 1:44:13. Apelação com carta de arrependimento redigida pelo ChatGPT: «30–40% de sucesso na maioria das vezes» (declarado) — #145 42:41. Spark Ads: subir o criativo no perfil antes de vincular a conta mostra se reprova — #145 2:21:09.
- **Condição:** ajuda só a quem já tem criativo vencedor; o método expira com atualização da plataforma (#158 2:35:55 relata método que estourou e foi absorvido pelo mercado).
- **Força da evidência:** **declarado** (cada tática vem de um caso).

### 4. Cloaker, anti-spy, catálogo e outros ocultadores
- **O que dizem:**
  - Anti-spy: distribuir poucos anúncios por muitas páginas (200 páginas, ~6 anúncios cada) e esconder criativo na biblioteca com mídias aleatórias do catálogo; oferta de ~R$ 30 mi/ano sem aparecer em swipe — #149 2:00:44–2:03:17.
  - Catálogo aprova mais criativo agressivo e esconde o criativo na biblioteca — #149 2:05:24.
  - Cloaker de página (The White Rabbit citado) e «cloaker de locução» (áudio white para a revisão da Meta, copy real para o lead); declarado sem reprovação por 3 meses — #160 2:18:05, #160 2:19:07, #160 2:37:52.
  - Cloaker interno entre Facebook e tracker — #155 2:12:48; proxy VPN para «parecer nativo» e cortar o cloaker alheio — #150 1:16:28.
  - Filtro de tráfego da própria VTurb serve contra plágio, mas já é usado para mostrar VSL falsa à revisão do Google — #147 2:15:20–2:16:21 (o host admite que é «um pouco black hat» e que não sabe se é sustentável).
  - Spy ficou mais difícil porque cloakers evoluíram — #128 1:32:48.
- **Condição:** nicho sensível/promessa agressiva (nutra, renda extra) e fonte com revisão automática dura.
- **Força da evidência:** **convergente** como prática (#149, #160, #155, #150, #145, #128); a sustentabilidade é **declarada só pelos que vendem/usam a ferramenta** e contestada em #147.

### 5. Reembolso e chargeback como risco de caixa
- **O que dizem:**
  - Declarado: média de reembolso do mercado ~15%; chargeback real ~1%, mas a plataforma devolve integral quando há alerta, então chargeback vira reembolso «caso perdido» — #132 1:52:22.
  - Mês com 22% de reembolso+chargeback = mais de R$ 6 mi de prejuízo (declarado) — #136 48:09. Mês com 23% de reembolso por problema de logística/estoque — #132 50:32. Checkout retém o dinheiro 60–90 dias — #136 49:12. «Allowance» preso por ~12 semanas pode deixar a operação lucrativa no papel e sem caixa — #155 2:52:18.
  - Margem real depois de reembolso: ROAS 1,7 virou «margem ridícula» antes de arrumar tudo — #132 1:51:20. ROAS mínimo de 1,5–1,6 (ou 1,4 em nicho de reembolso baixo como ED) para dar lucro com reembolso e imposto — #174 2:22:04, #153 2:06:54.
  - Nichos diferem em cancelamento/reembolso (rejuvenescimento alto, ED baixo) — #127 3:33:17, #153 2:06:54.
  - Quem fez promessa forte e entregou ebook fraco teve onda de reembolso e passou a entregar videoaula, suporte e bônus — #153 1:06:15.
  - Prática: tratar atendimento como vendedor, com meta e variável sobre reversão; 62% de recuperação declarada (de 28–32% no início) — #132 1:46:39, 1:47:11; projetar margem com 5/10/15/20% de reembolso — #136 1:20:27; terceirizar recuperação por e-mail/SMS/call center — #162 2:15:26; e-mail de acesso e carrinho reduz reembolso — #160 2:27:28; link de metas/fotos de início aumenta satisfação — #133 1:22:23; mensagem diária que dá motivo para não pedir — #132 2:34:58; mostrar rastreio e foto do pedido embalado — #136 47:08.
  - Copywriter responsável por reembolso/chargeback para não «agressivar até o talo»; comissão sobre margem, não faturamento — #134 2:16:58, #127 3:25:25.
- **Condição:** produtor com checkout de cartão (infoproduto/nutra), tráfego interno, promessa agressiva. Em afiliado por CPA o risco passa para o produtor — #162 2:14:23, #138 1:12:00.
- **Força da evidência:** **convergente** (#132, #136, #162, #134, #138, #155, #153, #127; atenção: #132 e #136 citam a mesma taxa de 62%, e os dois falam de sócio/operação chamados Gabriel, então podem ser a mesma empresa, não dois casos independentes: #132 1:47:11 e #136 13:03).

### 6. Gateway, plataforma de pagamento e conta do produtor
- **O que dizem:** chargeback alto «pune» o produtor também no Stripe, e o host retirou uma funcionalidade sua porque cobrança pós-trial gerou chargeback — #159 40:56. Cartão cobrado por descrição que o cliente não reconhece vira chargeback («que porra de VTurb é essa») — #150 1:32:04. Plataformas variam: Cartpanda trata reembolso ativamente (~30% de reversão da plataforma contra 62% do time); Digistore/ByGoods quase não — #132 1:49:16. Parte dos pedidos o cliente liga para o call center da plataforma antes do seu — 60–72% dos casos vão para a plataforma — #132 1:48:13. Gateway com taxa de chargeback entra no ROAS mínimo — #134 2:20:39. Hotmart derrubava contas de quem rodava PLR; quem manteve produto limpo manteve a conta — #153 1:07:49. Checkout de plataforma cai de vez em quando; Facebook também bane site que viola regra — #147 2:17:24. Briga constante com «fontes de tráfego, com gateway» — #134 2:09:02.
- **Condição:** produtor com checkout na plataforma de terceiro. Não há caso de gateway próprio ou adquirente local.
- **Força da evidência:** **declarado** por caso; lacuna grande (ver abaixo).

### 7. Compliance de anúncio e de oferta
- **O que dizem:** sem muita discussão direta. Fala-se de: reprovação mais dura no Google, sobretudo saúde/fitness (#147 1:32:34, 2:09:31); promessa agressiva reprova e quebra o ritmo (#160 acima, #168 1:39:55); quem não faz promessa absurda nem usa pessoas sem autorização roda meses sem cair (#136 1:09:38); produtor tem de falar com plataformas e checar que a página não mente (#162 2:14:55); em suplemento a Meta cobrava CPC maior de uma conta de risco do que de outra de programa digital, e a empresa separou conta física e digital (#147 2:17:24); TikTok derruba Spark Ads com comentários negativos e baniria vídeo copiado da internet (#145 2:20:37, #139 43:14); copy que usa Anvisa/«remédio» gera objeção, por isso se evita (#137 2:23:58); na UE foi preciso reformular produto por ingrediente proibido e cumprir VAT (#144 1:05:12–1:06:13).
- **Condição:** nicho de saúde/estética/renda extra, promessa forte.
- **Força da evidência:** **declarado** (casos soltos); **a base não traz regra de política da Meta/Google/FTC**. Sobre FTC, claim de saúde e política nada específico foi encontrado nas transcrições (busca por FTC, compliance, claim, política).

### 8. Dependência de fonte única / oferta única / expert único / sócio
- **O que dizem:** só YouTube + só uma oferta (PLR) quebrou quando o leilão encareceu (CPC de R$ 1 para R$ 3) na eleição de 2022 — #137 17:07–17:39. Nutra no Facebook cheia de tentativas, mas o Google «fez uma limpa» e derrubou o planejamento de março; resposta: «me adaptar, entregar lucro» em outras fontes — #134 2:06:57. «Contingência de fontes de tráfego»: quando uma deixa de escalar, outra escala — #134 2:11:44. Oferta de R$ 1 mi/dia dura cerca de 3 meses; queda em set/2025 por insistir em ofertas que já não davam retorno (falha própria declarada) — #177 2:37:47. Lançamento depende de decisão do expert ao vivo: um pitch mudado derrubou a meta apesar de todos os indicadores — #164 17:14; especialista que não sabia fazer pitch — #157 16:28. Hoje «preparado para qualquer onda» (diversificar produto/funil/canal) — #172 2:23:55. Refém de lançamento: 90% do faturamento em 2024 vinha de lançamento; construiu perpétuo — #140 5:14.
- **Sócio/caixa:** sócio de tráfego saiu levando ~30% e deixou o caixa desfalcado — #177 1:53:10. Separação de sócios após quebra e dívida pessoal — #137 18:11. Afiliado precisa de caixa alto: «no mínimo R$ 100 mil» para aguentar o tranco, não R$ 5 mil — #168 3:01:44. Operação lucrativa no papel com 10–12% de margem pode ficar sem caixa por allowance — #155 2:52:18.
- **Condição:** operador brasileiro de VSL/info, 2022–2026.
- **Força da evidência:** **convergente** para fonte/oferta única (#137, #134, #177, #153 45:18 «oferta morreu rápido» ao ser plagiada sem cloaker); **declarado** para sócio.

### 9. Imposto e custo da conta (risco de caixa específico do Brasil)
- **O que dizem:** a partir de 2026 há 12% de imposto sobre o valor gasto em anúncio em reais; a saída citada é conta em dólar e estrutura americana (LLC) — #149 2:36:25. No Facebook, taxa de ~11–12% mencionada; contas de agência de TikTok não pagam; contas alemãs pagam VAT 19% (declarado) — #145 52:05, 50:29. «Reembolso do Facebook nunca vi acontecer» — #145 51:30. «Imposto Meta» entra no cálculo de ROAS mínimo — #174 38:29.
- **Força da evidência:** **declarado** (verificar a lei e as taxas por fora; aqui são falas).

## Onde os convidados DISCORDAM

| Tema | Posição A (quem, #ep, ts) | Posição B (quem, #ep, ts) | Por que divergem |
|---|---|---|---|
| Origem das contas: agência × farm/compra × time interno | «As melhores contas são de agência, não tem jeito»; conta própria «tem que aquecer, demora e você pode perder a qualquer momento» — convidado de #149 (2:40:35) | Para operar de verdade a contingência interna fica **mais barata** que conta de agência «a tua margem diminui» (#158 21:00); farm bem feito (multilogin, proxy residencial, Gmail) deu «30–40 mil de lucro por dia» com conta farmada que gastou US$ 400 mil (#145 44:15, 45:16); comprar BM com mais de R$ 10 mil de gasto já basta (#168 3:01:12) | A é dono de uma empresa que aluga conta de agência (Orion Ads, #149 2:34:51): há conflito de interesse. B opera em escalas e margens diferentes e em fontes diferentes (TikTok farm × Meta). Híbrido é uma terceira posição (#145 53:06) |
| Produtor × afiliado: onde fica o risco de chargeback | Afiliado «é o único que tem 100% de lucro, não tem chargeback, não tem reembolso» (#136 6:49); produtor sofre com chargeback, suporte, compliance e produto queimado (#162 2:14:55); produtor faz mais dinheiro mas mina o fluxo de caixa (#155 2:51:48); nutra: «mais gente se ferrou do que ganhou» (#134 2:36:21) | Virar produtor deu +US$ 40 por venda, suficientes para pagar suporte (#130 43:35–44:37); «o jogo do produtor é melhor para a gente» (#177 2:45:24); manter tráfego interno é 80% da empresa e funcionou (#155 2:50:45) | A é quem vende oferta a afiliado (#136) ou admite que errou ao ser produtor (#162 2:15:26). B tem estrutura de recuperação/time, ticket alto e margem. O mesmo convidado se contradiz em #132: «teria lucrado mais com afiliado» (50:00) e hoje paga CPA a afiliado e opera produtor |
| Como reduzir reembolso | **Atrito e retenção parcial**: exigir que o produto chegue, que o cliente prove uso, oferecer 30% para ficar com o produto — #132 1:59:06; garantia que não é fácil como a do ByGoods | **Experiência e entrega**: onboarding com metas e fotos, e-mails de acesso, vídeo-aula, suporte, bônus — #133 1:22:23, #160 2:27:28, #153 1:06:15; garantia longa «aumenta conversão e reembolso, mas o negócio se paga» — #157 2:17:47 | A parte de produto físico (suplemento por correio) com promessa forte e cliente impulsivo. B parte de produto digital/consumo de conteúdo. Podem se somar |
| Cloaker/anti-spy: proteção legítima de oferta × hack de vida curta | Anti-spy e cloaker protegeram oferta de ~R$ 30 mi sem clone — #149 2:03:17; cloaker de página + áudio garantiu «zero reprovação» por 3 meses — #160 2:37:52; sem cloaker a oferta foi plagiada 5–6 vezes por dia e morreu — #153 45:18 | «Não sei até onde esses hackzinhos são sustentáveis; é melhor criar uma marca de longo prazo» — #147 2:16:21; empresas white operam «dentro das regras» e não têm bloqueio diário — #140 3:16:55; spy está ficando mais difícil, o jogo é «guerra» — #128 1:34:52 | Nicho e promessa: A vende com promessa agressiva (renda extra, nutra); B vende marca/expert. B (#147) também tem interesse: o host (VTurb) tem de convencer que a ferramenta não é black hat (#147 2:16:52) |
| Quantas contas/BMs e como escalar | Poucas campanhas com muita verba e «contas de pé»; analisar 200 contas que caíram é «pensar defensivo» (#168 1:40:57, 1:44:36) | Meta hoje exige 30–40 contas/BMs e comprar 20 BMs (US$ 40–50 mil) para achar uma que escala (#170 18:49); top afiliados testam em 10 contas (#136 53:21) | A trabalha com conta forte/agência. B descreve o custo mínimo de entrada em 2026 para quem não tem conta boa. Escala diária difere (milhões/dia × testes) |
| Black × white: bloqueio some ou nunca some | «Bloqueio você sempre vai sofrer, black ou white» (#136 1:09:38) | Em white «nunca mais» tomou bloqueio depois que a conta gastou o suficiente; o problema é só o início (#140 3:17:26) | Ambos veem o início da conta como o momento frágil; discordam sobre o regime permanente. #136 vende oferta agressiva com queda de 1–2 semanas (1:10:08) |
| Google: risco baixo ou alto | Google é «fonte de contingência»: o prejuízo é controlado (aquecer, proxy, domínio) e quando acerta paga muito (#134 1:41:46) | O Google «fez uma limpa» e derrubou o planejamento de março (#134 2:06:57); «caiu a conta do Google recentemente» (#159 4:17:31); em uma atualização «derrubou todas as contas» (#168 58:46); aprovação rápida só para quem tem relacionamento (#147 1:33:04) | O mesmo convidado (#134) enuncia a tese e depois a contradiz; o efeito depende da época e de relacionamento |

## Números declarados (NÃO são benchmark)

| Métrica | Valor | Contexto (nicho, país, ticket) | #ep · ts |
|---|---|---|---|
| Reembolso + chargeback num mês | 22%; mais de R$ 6 mi de prejuízo | Produtor/afiliados, nutra EUA, ofertas agressivas | #136 · 48:09 |
| Reembolso num mês | 23% (~US$ 3 mi faturados) | Nutra EUA, falta de estoque/logística | #132 · 50:32 |
| Média de reembolso do mercado | ~15% | Nutra/infoproduto, comentário do convidado | #132 · 1:52:22 |
| Chargeback «real» | ~1% (plataforma devolve o total e conta como reembolso) | Idem | #132 · 1:52:22 |
| Taxa de recuperação de reembolso | 62% (de 28–32% no início); 60–72% dos casos vão para a plataforma | Nutra EUA, Cartpanda | #132 · 1:47:11, 1:48:44 |
| Reversão do time da plataforma | ~30% (reembolso parcial) | Cartpanda | #132 · 1:49:16 |
| Prazo de vinda do chargeback/reembolso | até 6 meses | Produtor | #136 · 48:40 |
| Retenção do checkout | 60–90 dias; allowance ~12 semanas | Produtor | #136 · 49:12; #155 · 2:52:18 |
| Queda de contas | metade → 10% após correção | Meta, nutra/infoproduto black | #168 · 1:51:56 |
| Tempo para estruturar contingência | 15 dias, de 45 dias totais até escalar | Projeto de infoproduto agressivo, 2021 | #168 · 1:40:57 |
| Conta aguenta sem cair | 4 meses sem queda; 800 mil/dia | Afiliado top | #136 · 1:10:08 |
| Capital mínimo de afiliado | R$ 100 mil «no mínimo» | Afiliado BR | #168 · 3:01:44 |
| Custo de BM comprada | R$ 5–20 mil, sem garantia | Brasil | #149 · 2:39:02 |
| Apelação de conta TikTok | 30–40% de sucesso | Carta algorítmica | #145 · 42:41 |
| Gasto em contenção de ativos | US$ 300–400 mil | Afiliados top | #136 · 52:50 |
| Imposto sobre gasto em anúncio | 12% (2026) | Brasil, conta em reais | #149 · 2:36:25 |
| VAT em conta alemã | 19% | TikTok | #145 · 50:29 |
| ROAS mínimo declarado | 1,4 (ED) a 1,7; com reembolso/imposto | Nutra/infoproduto | #153 · 2:06:54; #174 · 2:22:04; #134 · 2:20:08 |
| Aprovação de anúncio no Google | nenhum anúncio ficava reprovado mais de 24 h | Relacionamento com Google, fitness | #147 · 1:33:04 |
| Regra de rejeições | 3 reprovações = nunca mais sobe | Operação grande | #155 · 1:33:53 |
| Envios por dia na Europa | 6 mil/dia (nutra emagrecimento França) | Convidado de logística, inglês | #144 · 1:07:21 |

## O que deu errado / riscos (contra-casos)
- PLR com YouTube como única fonte: eleição de 2022 triplicou o CPC, o funil parou de converter, sócios se separaram e um ficou devendo R$ 3 mil ao pai — #137 17:07–19:43.
- Oferta que escala sem cloaker foi plagiada («derrubava 5, 6 plágios por dia») e morreu rápido — #153 45:18. Mesma época: Hotmart bloqueava contas de quem rodava PLR — #153 1:07:49.
- Mês de 23% de reembolso por problema de logística e estoque depois de escalar — #132 50:32; ROAS «bonito» de 1,7 sem contar reembolso era margem ridícula — #132 1:51:20.
- Mês de 22% de reembolso + chargeback e prejuízo de R$ 6 mi — #136 48:09.
- Cobrança pós-trial gerou chargeback na própria VTurb; funcionalidade removida — #159 40:56. Cobrança com nome não reconhecido virou chargeback — #150 1:32:04.
- Sócio saiu com 30% do caixa; depois, queda em set/2025 por insistir em ofertas fracas (falha própria) — #177 1:53:10, 2:37:47.
- Lançamento fracassou porque o expert mudou o pitch ao vivo mesmo com todos os KPIs verdes — #164 17:14.
- Reprovação de anúncio no Google «quebra completamente o ritmo» — #147 1:32:34; queda de conta TikTok e farm exigem «cuidar da conta como filho» — #145 1:35:50–1:36:21.
- Alemanha/VAT: contas alemãs resolveram reprovação nos EUA, mas 19% de VAT inviabilizou — #145 50:29.
- Produtor «sem entender» allowance, refund e chargeback quebra: «muita gente quebrou» — #155 2:52:50, #134 2:36:21.
- Equívocos de método: anunciar vídeo copiado do TikTok, subir comentário negativo, 3 rejeições seguidas — #139 43:14, #145 2:20:37, #155 1:33:53.
- Upsell caro que anula o que a pessoa já tem pode gerar pedido de reembolso de tudo — #146 1:17:00; garantia grande aumenta reembolso — #157 2:17:47.

## Lacunas: o que a base NÃO cobre
- **Nenhuma regra concreta de política** da Meta, do Google ou do TikTok (texto de claim de saúde, antes/depois, antes e depois de estética, linguagem de dor) nem **FTC**: as palavras aparecem, o conteúdo não. Compliance de promessa só aparece como «não faça promessa absurda» (#136 1:09:38).
- **COD**: 0 episódios. Nada sobre recusa na entrega, devolução, courier, estoque de fornecedor, nem sobre risco de conta de anúncio para produto físico por país. O mais próximo: #147 2:17:24 (suplemento × programa digital, contas separadas) e #160 21:38 (dropshipping «não precisa de contingência tão forte»), ambos sem país.
- **Latam / Espanha**: só #153 1:06:15 (emagrecimento Latam com ebook e onda de reembolso). Nada sobre bloqueio por mercado, gateway local ou MCC por idioma.
- **WhatsApp / 1-a-1 / público 50+ / pós-pago**: não há caso; não há risco de número banido nem de inadimplência.
- **Processadora/adquirente em detalhe** (MID, retenção, reserva, descritor): só fragmentos (#159 40:56, #132 1:52:22, #150 1:32:04).
- **Reembolso por país e por nicho** além de EUA/Brasil, e como mudar o descritor ou política de reembolso para reduzir chargeback.
- **Recuperação de BM/conta e perfis pessoais**: só a «carta de apelação» do TikTok (#145 42:41) e a tese de que o Facebook não dá informação do motivo (#168 2:04:49).
- **Risco de sócio/caixa** como tema próprio: só relatos soltos (#177 1:53:10, #137 18:11).
- **Dano da própria exposição** (processo, órgão de defesa do consumidor): não discutido.

## Transferência para outros modelos de negócio
Pressuposto geral que quebra: quase todos os casos são **brasileiros que vendem para EUA/Brasil com pagamento antecipado no cartão** (nutra com checkout de plataforma, infoproduto). O dinheiro entra no momento da compra e o risco é «devolver depois» (reembolso/chargeback). Isso não vale para pagamento na entrega.

- **COD / pagamento na entrega (Chile, Colômbia, México, Guatemala, Romênia):**
  - **Não transfere:** chargeback de cartão não existe em COD; as taxas de reembolso, a retenção de 60–90 dias, o allowance e a recuperação via plataforma (#132, #136, #155) não se aplicam. O risco equivalente é **recusa/ausência na entrega e devolução**, que a base não mede. O número de 62% de recuperação não é aplicável.
  - **Transfere com ressalva:** a lógica de **contingência de conta** (isolar domínio/conta/página; histórico reduz queda; diagnosticar a causa da queda — #160, #168, #145). Um relato diz que dropshipping exige menos contingência (#160 21:38); a base não diz para quais países. A conta separada por tipo de produto (suplemento × digital) de #147 2:17:24 é diretamente útil para COD de suplementos.
  - **Pressuposto que quebra:** produto físico com fornecedor, frete e devolução. #144 1:04:40 mostra que entrega internacional gera risco de reembolso e que a UE exige reformular produto e cumprir VAT (relevante para Romênia, mas o caso é envio dos EUA, não COD local). Os 19% de VAT citados (#145 50:29) são de conta alemã; **conferir a alíquota romena por fora**. Fretes e estoque: #132 50:32 mostra que falta de estoque virou 23% de reembolso (equivalente a pedidos cancelados em COD).
  - **Cuidado:** a prática de «time de atendimento como vendedor com meta» (#132 1:46:05) pode ser adaptada para reduzir recusa na entrega, mas nenhum episódio testou isso em COD.

- **Infoproduto VSL + quiz + upsell (Latam, Espanha, worldwide; espiritualidade/saúde/estética):**
  - **Transfere bem:** reembolso como risco de caixa (#132, #136, #153, #160); onboarding, e-mail de acesso e suporte para reduzir (#133, #160, #153); calcular ROAS com reembolso e imposto (#174, #134); plataformas variam em reverter reembolso (#132 1:49:46); chargeback alto penaliza no Stripe (#159 40:56); upsell que anula o front gera pedido de reembolso total (#146 1:17:00); isolar estrutura (#160, #168).
  - **Não transfere / quebra:** as taxas de 15–23% são de **nutra EUA** (promessa agressiva, impulso); estética/espiritualidade têm outro perfil e a base não tem número. Impostos citados (12% em reais, VAT) são do Brasil e da Alemanha, não de Latam/Espanha. A base não cobre as políticas de saúde/espiritualidade da Meta; nada autoriza supor que o que «passou» em nutra EUA passa em espiritualidade ou em outro idioma. Cloaker de áudio, catálogo para aprovar, reedição e VSL falsa (#160, #149, #145, #147) são **contornos de política com risco de banimento** e foram relatados por quem os vende ou os usa; não replicar sem decisão consciente.

- **Venda 1-a-1 pós-paga por WhatsApp (Brasil, público 50+, closers):**
  - **Não transfere:** nenhum caso de WhatsApp, número banido, ou inadimplência pós-entrega. O risco é «cliente que recebe e não paga», inverso do reembolso do cartão.
  - **Transfere por analogia:** tratar atendimento como time de venda com meta e variável sobre reversão (#132 1:46:05); atrito/qualificação antes de entregar (#132 1:59:06, pedido «espera o produto chegar»); a comissão por margem de contribuição em vez de faturamento, para o closer assumir risco de perda (#127 3:25:25, #134 2:20:08). Risco de sócio/caixa quando a operação depende de poucas pessoas e do closer principal (#177 1:53:10, #164 17:14). Imposto de 12% sobre anúncio em reais (#149 2:36:25) afeta quem compra tráfego no Brasil.
  - **Pressuposto que quebra:** público 50+ e fitoterápico com promessa de saúde: a base não discute compliance de saúde nem a Anvisa, só que dizer «remédio» gera objeção (#137 2:23:58).
