---
name: benchmarking-mercado
description: "Raio-X do leilão de um nicho na Meta Ad Library: mapeia anunciantes, grupo de controle e devolve o Mapa de Fatias com as combinações persona x ângulo x formato ainda livres."
---

# Benchmarking de Mercado — Raio-X do Leilão

As skills de mineração olham a peça. Esta olha o tabuleiro. Ela não responde "que ângulo funciona", responde "quem está no leilão, quanto tempo cada um aguenta, onde a fatia está lotada e onde ainda tem espaço vazio".

O output que importa é o **Mapa de Fatias**: a matriz micro-persona x ângulo x formato do nicho, com a densidade de ocupação de cada célula. Célula cheia é onde todo mundo está e o CPM é caro. Célula vazia com adjacentes validadas é Fatia Fantasma, e é ali que a verba entra.

## Autonomia — execute, não pergunte

Roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

- **Não pergunte o que a coleta responde.** Disse o nicho? Abra a biblioteca e olhe. Decida amostra, alvo e prioridade pelos critérios deste arquivo e informe o que decidiu.
- **Só pare quando** faltar login, permissão de pasta, ou quando a escolha mudar o resultado e houver duas leituras igualmente defensáveis.
- **Execute a cadeia inteira sem pedir aprovação no meio.** Narre em uma linha por etapa enquanto faz.
- **Leia os JSONs do banco antes de começar.** Não refaça trabalho que já existe.
- **Entregue arquivo salvo com o caminho informado**, não texto no chat.
- **Ao terminar, diga três coisas:** o tamanho da amostra, o que saiu, e onde está.
- Colete os dois grupos na mesma passada. Grupo de controle não é opcional e não se pede autorização pra coletar.

## Como você descobre sozinho o que ia perguntar

Nenhum destes vira pergunta. Todos se derivam do mercado — **e só do pedaço dele que está escalando.**

### Passo zero: estabeleça o subconjunto escalado antes de derivar qualquer coisa

Derivar da amostra inteira é derivar do ruído. A maioria dos anúncios de qualquer nicho não está performando, e o que é comum entre eles é convenção, não vantagem.

A ordem é esta, e ela resolve a circularidade de precisar do ticket para definir o corte:

1. **Passada provisória.** Ordene por longevidade aparente com corte provisório de 21 dias e pegue os 10 anunciantes do topo.
2. **Leia o ticket** nas páginas de destino desses 10. A mediana é o ticket do nicho.
3. **Fixe o corte real** pela tabela de longevidade por ticket.
4. **Reordene** com o corte correto. **Este conjunto é o grupo A**, e é a única fonte de derivação.
5. Colete o grupo B (os que morreram cedo) em separado, **só para calcular discriminação**.

### A tabela

| O que falta | De onde tirar — sempre dentro do grupo A | Se não der |
|---|---|---|
| **País** | O país da maioria dos anúncios do grupo A | Assume o do usuário e declara |
| **Ticket** | Mediana das páginas dos 10 de maior longevidade | Assume médio e declara |
| **Nicho exato** | O subnicho com mais anunciantes **sustentando verba**, não com mais anúncios | Roda no amplo e segmenta depois |
| **Micro-personas** | Quem aparece, quem fala e sobre quem fala **nos criativos do grupo A**. 3+ ocorrências valida | Marca baixa confiança e segue |
| **Avatares** | Classifique quem aparece **nos escalados** em autoridade, transformado e espectador | Usa o dominante do grupo A |
| **Formatos** | Repetição por formato macro **dentro do grupo A**. Acima de 30% está validado | Usa os 3 mais frequentes do grupo A |
| **Ângulos** | Os criativos de maior longevidade do grupo A, por repetição | Usa o do anunciante mais antigo |
| **Oferta do usuário** | Se ele não deu, gere para o padrão do grupo A e diga que adaptou ao mercado | — |
| **Quantas peças** | O padrão está escrito neste arquivo | — |
| **Amostra** | O mínimo está escrito neste arquivo. Colete até fechar | — |

### As três regras que não se quebram

**Nunca derive do grupo B.** Os mortos servem para uma coisa só: dizer o que **não** discrimina. Persona, formato, ângulo e avatar tirados de anúncio que morreu são exatamente o que você não quer modelar.

**Nunca derive da amostra somada.** "Aparece em 40% dos anúncios" não significa nada se você não sabe em quantos dos que escalaram. Toda contagem é sobre o grupo A, e o número do grupo B entra só ao lado, para comparação.

**Se o grupo A tiver menos de 8 anunciantes**, o nicho é pequeno demais ou o corte está apertado demais. Afrouxe o corte um degrau, declare que afrouxou, e refaça. Não complete o grupo A com anúncio que não passou.

### E declare o que derivou

Em uma linha, sempre: "grupo A com 14 anunciantes acima de 21 dias, ticket mediano de R$47 lido em 10 páginas, três micro-personas com 3+ ocorrências cada". Assim o usuário corrige se quiser, sem você ter travado esperando.

## Qual criativo entra na extração

Grupo A diz quais **anunciantes** estão escalando. Não diz quais **criativos** prestam. Uma conta com 40 anúncios costuma ter três carregando e o resto testando — e extrair dos 40 é derivar do ruído dela.

### Os três tipos de criativo dentro de uma conta

| Tipo | Como reconhecer | Serve para |
|---|---|---|
| **Controle** | Longevidade acima da mediana da própria conta, e duplicado ou variado | Extrair **ângulo, avatar e micro-persona** |
| **Variação de controle** | Mesma base do controle com uma coisa mudada, no ar há mais de uma semana | Extrair **formato e hook visual** — é o que ele está testando |
| **Teste** | Apareceu nos últimos 7 dias, sem duplicação nem variação | **Não extraia nada.** Ainda não provou |

### Os sinais de que um criativo é controle, em ordem de força

1. **Duplicação.** O mesmo criativo aparece em vários registros de anúncio. Ninguém duplica perdedor — é o sinal mais forte que existe na biblioteca e o mais ignorado.
2. **Variações em volta dele.** Três peças com a mesma base e o gancho trocado significam que ele está investindo naquela direção.
3. **Longevidade acima da mediana da conta.** Compare o criativo com os outros do mesmo anunciante, não com o nicho.
4. **Localização.** Aparece em mais de um país ou idioma. Traduzir custa dinheiro e ninguém traduz perdedor.
5. **Reposição.** Foi ressubido depois de um tempo fora.

Dois sinais bastam para tratar como controle. Um só, trate como variação.

### De onde tirar cada elemento

- **Ângulo, avatar e micro-persona** saem dos **controles**. São as variáveis que a longevidade valida.
- **Formato e hook visual** saem das **variações recentes dos controles**. É onde o anunciante está mexendo agora, e o que ele está testando é onde ele acha que tem ganho.
- **Estrutura e ordem narrativa** saem do controle mais antigo da conta. É o que sobreviveu mais tempo sem mudar.

### Conte por anunciante, nunca por anúncio

Este é o erro que estraga a análise inteira. Se um anunciante tem 200 peças e outro tem 8, contar por anúncio faz o primeiro definir sozinho todos os percentuais — e você acaba modelando a preferência de uma conta, não o padrão do mercado.

**A regra:** um anunciante, um voto por elemento. Se o formato UGC selfie aparece em 60 peças de um anunciante só, ele conta como **um**. O que vale é em quantos **anunciantes distintos** do grupo A aquele elemento aparece nos controles.

`repeticao_pct` é sempre sobre anunciantes distintos. Registre `amostra_n` como número de anunciantes, e o total de peças lidas em campo separado.

### O piso

Elemento que aparece nos controles de **menos de 3 anunciantes distintos** não é padrão, é preferência de conta. Registre como hipótese e marque baixa confiança.

## Princípio que separa isso de espiar concorrente

Contar o que os vencedores fazem não prova nada sozinho. Se 47% dos anúncios que escalam usam UGC selfie e 45% dos que morreram em 3 dias também usam, UGC selfie não explica performance: é só o padrão do nicho. **Sem grupo de controle, frequência é ruído com aparência de dado.**

Por isso esta skill sempre coleta duas amostras e compara:

- **Grupo A (sobreviventes):** anúncios que passam o Radar de Longevidade.
- **Grupo B (controle):** anúncios do mesmo nicho, mesma janela, que ficaram menos de 7 dias no ar ou têm 1-2 criativos e nenhuma renovação.

O que importa é o **Índice de Discriminação**: `% no grupo A menos % no grupo B`.

- Índice alto e positivo → variável que provavelmente explica performance. Trave como variável fixa.
- Índice perto de zero → variável neutra. É convenção do nicho, não vantagem. **Território livre pra testar**, porque mexer nela custa pouco.
- Índice negativo → variável associada a morte. Evite.

Reporte sempre os dois percentuais e o índice. Nunca entregue só o percentual do grupo A.

## Capacidade e limite (leia antes de rodar)

- **A Ad Library não mostra gasto nem resultado** fora de anúncios políticos na maioria dos países. Tudo aqui é inferência a partir de comportamento de verba, não medição. Diga isso no relatório.
- **"Ativo desde" é o proxy central, e ele mente às vezes.** Uma edição pode zerar a data em algumas situações, e anúncio pausado e reativado aparece diferente. Trate longevidade como sinal forte, nunca como prova. Triangule com número de variações e ritmo de reposição.
- **Contagem de anúncios ativos infla.** Dynamic creative, múltiplos posicionamentos e múltiplos idiomas contam como anúncios separados. Um anunciante com 200 "anúncios" pode ter 12 criativos reais. Sempre estime criativos únicos, não linhas.
- **O Claude não assiste vídeo.** Formato de vídeo sai por frame + transcrição + descrição. Para profundidade de formato, mande pra `mineracao-formatos-virais`.
- **Amostra:** mínimo 40 anúncios no grupo A e 40 no grupo B. Ideal 150+ em cada. Abaixo do mínimo, entregue mesmo assim mas carimbe **baixa confiança** em cada conclusão e diga quantos itens faltaram.

## Corte de longevidade por ticket (não use 21 fixo)

O tempo que prova lucro muda com o modelo. Parametrize antes de coletar:

| Modelo | Corte grupo A | Corte grupo B |
|---|---|---|
| Low ticket R$9-47, leva grande | 10+ dias | menos de 3 dias |
| Ticket médio R$47-297 | 21+ dias | menos de 7 dias |
| High ticket / VSL longa | 30+ dias | menos de 10 dias |
| Recorrência / assinatura | 45+ dias | menos de 14 dias |

Se o usuário não disse o ticket, **descubra**: abra três páginas de destino dos anunciantes do topo e leia o preço. A mediana define o corte. Declare o que assumiu e siga — não pergunte.

## Fontes e protocolo de coleta

1. **Meta Ad Library** (`facebook.com/ads/library`) — fonte primária. Busque por palavra-chave do nicho E por anunciante, nos dois sentidos: keyword revela quem você não conhecia, anunciante revela o portfólio de quem você já conhece.
2. **Página de destino de cada anunciante** — leia até o checkout. É de onde sai ticket, escada de preços, order bump e mecanismo. Sem isso o benchmark fica só de criativo.
3. **Ad Library de outros países** — o mesmo nicho em US/PT/ES/MX. Ângulo saturado aqui pode estar virgem lá, e o contrário também. Registre sempre o país.
4. **Comentários dos anúncios ativos** — volume e teor de comentário indicam entrega real e revelam objeção viva.

Registre a amostra por fonte e por grupo. O relatório abre com a contagem.

## Classificação de anunciante

Para cada anunciante do grupo A, classifique:

- **Dominante** — muitos criativos únicos, longevidade alta, reposição contínua. É o CPM que você vai pagar se entrar na mesma fatia.
- **Desafiante** — entrou recentemente e está subindo volume rápido. Sinal de que achou fatia nova. Vale dissecar primeiro: é o mais informativo do mapa.
- **Testador** — muitos criativos, longevidade baixa em cada um, alta rotatividade. Está minerando ângulo. Bom pra copiar a agenda de testes, ruim pra copiar o criativo.
- **Zumbi** — poucos criativos, longevidade alta, zero reposição. Provavelmente esquecido no ar. Não conte como validação.
- **Morto** — sumiu na janela analisada. Registre, porque quem saiu diz tanto quanto quem ficou.

## Sinais de mercado a extrair

- **Temperatura do leilão** — quantos anunciantes ativos, quantos entraram nos últimos 30 dias, quantos morreram. Nicho lotado e crescendo = CPM subindo, entre por fatia lateral. Nicho esvaziando = ou morreu a demanda, ou ficou uma janela livre. Diga qual das duas você acha e por quê.
- **Concentração** — se 3 anunciantes concentram a maior parte dos criativos, o nicho tem donos e você entra por micro-persona órfã, não de frente.
- **Idade dos ângulos dominantes** — ângulo velho e ainda escalando é mina. Ângulo que apareceu há 3 semanas em todo mundo é onda, e onda satura junto.
- **Ritmo de reposição** — de quantos em quantos dias o dominante troca criativo. Isso te dá a cadência de produção necessária pra competir naquele nicho. É um número que muda decisão de operação.
- **Faixa de ticket praticada** — colhida das páginas. Define se dá pra entrar por baixo no leilão.
- **Nível de consciência dominante** — se todo mundo ataca solution aware, product aware e problem aware costumam estar livres.

## Extração de micro-persona (faça antes de montar a matriz)

O eixo mais importante da matriz é a micro-persona, e ela não existe em lugar nenhum pronta. Extraia do mesmo corpus que você já coletou, sem passada extra.

A persona é o problema (emagrecer, recuperar memória, ganhar dinheiro). A micro-persona é **o papel que a pessoa tem medo de perder** ou o papel que ela ocupa na compra. É por isso que o orgulhoso, o cuidador exausto, o cônjuge protetor e o preventivo são micro-personas diferentes dentro do mesmo nicho: mesmo problema, medo diferente, e portanto leilão diferente.

Para cada micro-persona candidata, extraia do corpus:

- **Quem aparece no criativo** — idade, gênero, papel (paciente, filha, cônjuge, profissional). O avatar escolhido revela quem o anunciante está mirando.
- **Quem fala e sobre quem** — primeira pessoa ("eu estava esquecendo tudo") mira quem vive o problema; terceira ("minha mãe não me reconhecia") mira o cuidador. São públicos distintos com dor distinta.
- **Quem compra x quem usa** — quando divergem, são duas micro-personas e você precisa de criativo para cada.
- **O papel ameaçado** — dirigir, cozinhar, trabalhar, decidir, ser respeitado. É o gatilho emocional que muda tudo.
- **A linguagem literal** — termos que só aquele recorte usa. Puxe dos comentários dos anúncios, não invente.

Conte a incidência de cada micro-persona nos dois grupos e rode o índice de discriminação nelas também: micro-persona que aparece muito no grupo A e pouco no B é fatia quente; a que aparece igual nos dois é convenção.

Uma micro-persona só entra no mapa com **3+ ocorrências independentes** no corpus. Abaixo disso, registre como hipótese e marque baixa confiança. Micro-persona inventada contamina todas as skills seguintes, porque todas herdam esse campo.

## Banco de Fatias — leia antes, escreva depois

Se existir `banco-de-fatias.json`, **leia antes de coletar**. Ele guarda o que já foi testado e o resultado real de cada teste. Duas consequências:

- Fatia marcada como já testada e queimada não deve voltar como recomendação. Se voltar, diga que já foi testada e com que resultado.
- Variável já validada para uma micro-persona no banco entra no relatório com peso maior que qualquer inferência de biblioteca, porque é dado de gerenciador e não proxy.

Ao terminar, acrescente as fatias fantasma priorizadas ao banco com `status: "a_testar"` e a data. É assim que o banco vira ativo: o Raio-X propõe, o Diagnóstico confirma ou mata, e o próximo Raio-X já começa mais inteligente que o anterior.

## Mapa de Fatias — o output principal

Monte a matriz cruzando as três variáveis: **micro-persona x ângulo x formato**.

Para cada célula, registre a densidade:

- `lotada` — 5+ anunciantes ali. Não entre, a menos que você tenha vantagem estrutural de ticket ou de criativo.
- `disputada` — 2 a 4.
- `rala` — 1.
- `fantasma` — nenhum anunciante, **mas com as três variáveis individualmente validadas em outras células**. Este é o achado. Você combina peças provadas de um jeito que ninguém combinou.
- `deserto` — vazia porque as variáveis não se sustentam (persona não existe, ângulo briga com a crença, formato não cabe). Não confunda com fantasma: célula vazia não é oportunidade automática.

A diferença entre fantasma e deserto é o julgamento mais importante desta skill. Antes de marcar fantasma, verifique: a micro-persona aparece em alguma célula ocupada? O ângulo aparece? O formato aparece? Se as três aparecem separadamente e a combinação não, é fantasma. Se alguma delas não aparece em lugar nenhum, é deserto até prova em contrário e você marca como hipótese de baixa confiança.

Ranqueie as fantasmas por: força individual das três variáveis (média do índice de discriminação), custo de produção do formato, e distância da crença do público.

## Passo a passo

1. Determine nicho, país, ticket e janela pela tabela de derivação. Defina o corte de longevidade e declare o que assumiu.
2. Leia `banco-de-fatias.json` se existir. Anote o que já foi testado.
3. Colete o grupo A na Ad Library. Registre por anunciante: data ativo desde, criativos únicos estimados, país, link da página, ticket, ângulo aparente, formato aparente, avatar e quem fala.
4. Colete o grupo B com os mesmos campos. Este passo é obrigatório, não é opcional. Sem ele o relatório sai sem índice de discriminação e você avisa que a confiança caiu.
5. Extraia as micro-personas do corpus pela seção acima. Só entram as com 3+ ocorrências.
6. Classifique cada anunciante. Estime criativos únicos, não linhas.
7. Calcule as frequências nos dois grupos e o índice de discriminação de cada variável, micro-persona incluída.
8. Monte o Mapa de Fatias e classifique a densidade de cada célula.
9. Separe fantasma de deserto com o teste das três variáveis. Descarte o que o banco já queimou.
10. Puxe as páginas de destino e complete ticket, escada e mecanismo.
11. Salve o JSON, escreva as fatias prioritárias no banco e escreva o relatório.
12. Rode a checklist.

## Saída — contrato compartilhado da esteira

Salve em `mineracao/benchmark.json`. O array `fatias` usa os mesmos nomes de campo das outras skills, pra esteira consumir sem tradução.

```json
{
  "nicho": "",
  "pais": "",
  "janela": "AAAA-MM-DD a AAAA-MM-DD",
  "ticket_alvo": "",
  "corte_longevidade_dias": 0,
  "amostra": { "grupo_a_n": 0, "grupo_b_n": 0, "confianca": "alta | media | baixa" },
  "temperatura_leilao": {
    "anunciantes_ativos": 0,
    "entraram_30d": 0,
    "morreram_30d": 0,
    "concentracao_top3_pct": 0,
    "leitura": "lotado_crescendo | lotado_estavel | esvaziando | virgem",
    "ritmo_reposicao_dias": 0
  },
  "anunciantes": [
    {
      "nome": "",
      "classificacao": "dominante | desafiante | testador | zumbi | morto",
      "dias_no_ar_max": 0,
      "criativos_unicos_estimados": 0,
      "linhas_na_biblioteca": 0,
      "pais": [""],
      "page_id": "",
      "link_biblioteca": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&view_all_page_id=PAGE_ID",
      "link_funil": "url da página de vendas, resolvida depois do redirect",
      "link_anuncio_referencia": "https://www.facebook.com/ads/library/?id=AD_ID",
      "ticket": "",
      "escada_precos": "",
      "mecanismo": "",
      "angulos_usados": [""],
      "formatos_usados": [""],
      "micro_personas_atacadas": [""],
      "nivel_consciencia": "inconsciente | problema | solucao | produto | total",
      "observacao": ""
    }
  ],
  "micro_personas": [
    {
      "id": "MP-001",
      "nome": "",
      "papel_ameacado": "",
      "quem_compra": "usuario | terceiro",
      "voz": "primeira_pessoa | terceira_pessoa",
      "faixa_etaria": "",
      "gatilho_emocional": "",
      "linguagem_literal": [""],
      "crencas": [""],
      "ocorrencias": 0,
      "pct_grupo_a": 0,
      "pct_grupo_b": 0,
      "indice_discriminacao": 0,
      "confianca": "alta | media | baixa"
    }
  ],
  "discriminacao": [
    {
      "variavel": "",
      "dimensao": "angulo | formato | micro_persona | nivel_consciencia | ticket | comprimento",
      "pct_grupo_a": 0,
      "pct_grupo_b": 0,
      "indice_discriminacao": 0,
      "leitura": "fixar | neutra_livre_pra_testar | evitar"
    }
  ],
  "fatias": [
    {
      "id": "FAT-001",
      "tipo": "fatia",
      "micro_persona": "",
      "angulo": "",
      "formato": "",
      "densidade": "lotada | disputada | rala | fantasma | deserto",
      "anunciantes_na_fatia": 0,
      "descricao": "a combinação em uma linha",
      "mecanismo": "por que essa combinação faria sentido",
      "estado_cognitivo": "atencao | curiosidade | desejo | mecanismo | prova | progressao",
      "nivel_consciencia": "inconsciente | problema | solucao | produto | total",
      "crenca_respeitada": "",
      "emocao": "",
      "forca_media_variaveis": 0,
      "custo_producao": "baixo | medio | alto",
      "prioridade": 0,
      "amostra_n": 0,
    "amostra_anunciantes": 0,
    "pecas_lidas": 0,
    "tipo_de_origem": "controle | variacao_de_controle",
      "status": "validado | a_testar"
    }
  ],
  "arbitragem_geografica": [
    { "angulo": "", "saturado_em": "", "virgem_em": "", "confianca": "alta | media | baixa" }
  ]
}
```

## Relatório — use este template

```
# Raio-X do Leilão — [nicho] · [país] · [janela]

## Amostra
Grupo A: N anúncios / N anunciantes. Grupo B: N. Confiança: X.
Limites conhecidos desta leitura.

## Temperatura
Leitura do leilão em 3 linhas. Está lotado? Crescendo? Quem entrou, quem saiu.

## Quem está no leilão
Tabela: anunciante · classificação · dias no ar · criativos únicos · ticket · fatia que ocupa · **biblioteca** · **funil**.
Os dois links vão clicáveis em toda linha: sem eles a tabela não é auditável.
Comece pelos desafiantes — é onde está a informação nova.

## Micro-personas do nicho
Tabela: nome · papel ameaçado · quem compra · % A · % B · índice · confiança.
Marque quais estão sendo atacadas e quais estão órfãs.

## O que discrimina
Tabela: variável · % A · % B · índice · leitura.
Diga em uma frase o que travar e o que está livre pra testar.

## Mapa de Fatias
A matriz, com as lotadas primeiro (pra mostrar onde não entrar) e as fantasmas depois.

## As 3 Fatias Fantasma prioritárias
Para cada uma: qual a combinação, por que as três variáveis se sustentam separadamente,
qual estado cognitivo ela mira, e qual seria o primeiro teste.

## Arbitragem geográfica
O que está saturado num país e virgem noutro.

## Recomendação de entrada
Onde entrar, com que ticket, com que cadência de reposição de criativo.
```

## Linha vermelha

Vale a mesma regra da `mineracao-clickbait`. Extraia mecanismo e estrutura de mercado, nunca a alegação enganosa. Se um dominante escala com fraude em nicho sensível (cura, garantia financeira, prova fabricada), registre o **mecanismo abstrato e o fato de que aquela fatia é radioativa**, e marque `observacao: "linha vermelha"`. Fatia que só existe com veneno não é oportunidade, é passivo: ela leva BM, gateway e imagem junto quando cai. O método é forte sem isso.

Não reproduza copy literal, imagem, PDF ou nome de produto de concorrente no output. Estrutura, ângulo, escada de preços e mecanismo são ideia e se modelam. Texto e arte são obra de terceiro e se copiam em cima de risco jurídico.

## Checklist de qualidade
- Tudo que era derivável foi derivado do mercado, em vez de perguntado?
- A derivação saiu SÓ do grupo A, e nada foi tirado do grupo B nem da amostra somada?
- Dentro do grupo A, a extração saiu dos controles e das variações — e não dos testes recentes?
- A contagem foi por anunciante distinto, e não por anúncio?
- Elemento com menos de 3 anunciantes distintos foi marcado como hipótese?
- O grupo A fechou com 8+ anunciantes, ou o afrouxamento do corte está declarado?
- O que foi assumido está declarado em uma linha?
- A cadeia rodou inteira, sem parar pedindo aprovação no meio?
- A saída é arquivo salvo com caminho informado?

- Ticket confirmado e corte de longevidade escolhido pela tabela, não fixado em 21?
- Grupo B coletado de verdade? Se não, a queda de confiança está declarada no relatório?
- Amostra ≥ 40 por grupo (ideal 150+), com o N reportado?
- Criativos únicos estimados, e não a contagem crua de linhas da biblioteca?
- Todo anunciante tem link da biblioteca dele e link do funil, ambos conferidos?
- Toda variável tem % nos dois grupos e índice de discriminação?
- Micro-personas extraídas do corpus, com 3+ ocorrências cada, e não inventadas?
- Banco de Fatias lido antes e atualizado depois, sem repropor fatia já queimada?
- Cada anunciante foi classificado e os desafiantes vieram primeiro?
- Fantasma foi separada de deserto pelo teste das três variáveis?
- As páginas de destino foram lidas (ticket, escada, mecanismo preenchidos)?
- Nada afirmado como medição quando é inferência de comportamento de verba?
- JSON no contrato exato, pronto pra esteira e pro Banco de Fatias?