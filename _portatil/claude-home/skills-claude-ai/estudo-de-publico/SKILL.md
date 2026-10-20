---
name: estudo-de-publico
description: "Estudo de público completo de um nicho: extrai micro-personas pelo papel ameaçado, colhe linguagem literal em reviews/Reddit/YouTube/comentários de anúncios, mapeia dor, desejo, objeção e crença, e valida contra evidência citável. Use para estudo de público, avatar, persona, ou linguagem do cliente."
---

# Estudo de Público

O criativo não segmenta pelo interesse que você marca no gerenciador, segmenta pelo que ele diz. Por isso público não é dado demográfico, é **um conjunto de recortes com medos diferentes que compram a mesma coisa por razões diferentes**.

Esta skill produz o eixo mais importante do pack: as micro-personas que todas as outras skills consomem no campo `micro_persona_id`. Sem ela, esse campo é chute e o chute contamina tudo em silêncio.

## Autonomia — execute, não pergunte

Roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

- **Não pergunte o que a coleta responde.** Disse o nicho? Abra a biblioteca e olhe. Decida amostra, alvo e prioridade pelos critérios deste arquivo e informe o que decidiu.
- **Só pare quando** faltar login, permissão de pasta, ou quando a escolha mudar o resultado e houver duas leituras igualmente defensáveis.
- **Execute a cadeia inteira sem pedir aprovação no meio.** Narre em uma linha por etapa enquanto faz.
- **Leia os JSONs do banco antes de começar.** Não refaça trabalho que já existe.
- **Entregue arquivo salvo com o caminho informado**, não texto no chat.
- **Ao terminar, diga três coisas:** o tamanho da amostra, o que saiu, e onde está.
- Puxe das cinco fontes sem perguntar quais. Se uma não render, diga qual e siga com as outras.

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

## Persona, micro-persona e avatar

Três coisas que costumam virar uma só e não são:

- **Persona** é o problema. Emagrecer, recuperar memória, sair da dívida.
- **Micro-persona** é **o papel que a pessoa tem medo de perder**. Dentro de "recuperar memória" existe o orgulhoso (medo de virar dependente), o cuidador exausto (medo de não dar conta), o cônjuge protetor (medo de perder o parceiro em vida) e o preventivo (medo de virar o que viu no pai). Mesmo problema, medos distintos, leilões distintos.
- **Avatar** é quem aparece no criativo falando. É variável de produção, não de público. Um avatar pode servir várias micro-personas e vice-versa.

O erro caro é tratar micro-persona como faixa etária. "Mulher 35-50" não é micro-persona, é filtro. "Filha que assumiu sozinha o cuidado da mãe e tem culpa de sentir raiva" é micro-persona: tem medo nomeável, linguagem própria e objeção própria.

## Fontes, e o que cada uma entrega

Cruze pelo menos três. Padrão que aparece numa fonte só costuma ser artefato da fonte.

1. **Reviews da Amazon** de best-sellers do nicho. Leia as **positivas e as negativas**. Positiva de 5 estrelas entrega o desejo declarado; negativa de 1 a 3 entrega a objeção e a decepção, que é onde mora o ângulo. Reviews longas de comprador verificado valem mais.
2. **Reddit e fóruns** do nicho. É onde a pessoa fala sem estar vendendo nada. Crença crua, vilão, vocabulário interno.
3. **Comentários de YouTube e TikTok** em vídeos do tema. Sinaliza reação emocional e revela quem marca quem: "@fulana olha isso" é a prova de que existe um comprador terceiro.
4. **Comentários dos próprios anúncios** na Ad Library e nas páginas. Objeção viva, no ponto de compra. É a fonte mais próxima da decisão e a mais subusada.
5. **Perguntas do Google e do YouTube** ("por que", "como", "e se"). Entrega o nível de consciência real do mercado.

Registre a amostra por fonte. Mínimo 40 itens de linguagem coletados; ideal 150+.

## O que extrair de cada micro-persona

- **Papel ameaçado** — o que ela tem medo de deixar de ser. É o núcleo, e é o que muda o leilão.
- **Quem compra x quem usa** — quando divergem, são duas peças de criativo, não uma. Marque sempre.
- **Voz** — primeira ou terceira pessoa. Define se o criativo fala "eu estava esquecendo" ou "minha mãe não me reconhecia".
- **Dor central e desejo central** — o que dói hoje e o que ela quer amanhã, na linguagem dela.
- **Objeção principal** — o que a impede de comprar. Sai principalmente das reviews negativas e dos comentários de anúncio.
- **Crenças** — o que ela jura que é verdade. O ângulo joga **ao lado** disso, nunca contra.
- **Vilão** — quem ela culpa. Indústria, médico, genética, ela mesma. Vilão errado queima o criativo.
- **Linguagem literal** — as expressões exatas, copiadas como aparecem. Não traduza para termo técnico.
- **Onde vive** — plataformas e comunidades onde esse recorte se concentra.
- **Nível de consciência** dominante do recorte.

## Regra da evidência

Toda micro-persona precisa de **3+ ocorrências independentes** em pelo menos **2 fontes diferentes** para entrar como validada. Abaixo disso é hipótese, e vai marcada `confianca: "baixa"`.

Para cada micro-persona, registre em `fonte_evidencia` de onde veio: quantos itens, de que fontes, com link de pelo menos um exemplo. Micro-persona sem lastro é a falha mais cara do pack inteiro, porque ela vira `micro_persona_id` e se espalha silenciosamente por ângulo, formato, hook e esteira.

Se existir `benchmark.json`, cruze: micro-persona que aparece no seu estudo **e** tem índice de discriminação alto no benchmark é fatia quente. A que aparece no estudo e não aparece em anúncio nenhum é candidata a Fatia Fantasma, e é o achado mais valioso desta skill.

## Linha vermelha

Colete linguagem pública. Não perfile indivíduos: nada de juntar dados de uma pessoa identificável, nomear autor de comentário, ou montar dossê de gente real. O objeto é o recorte, não a pessoa.

Em nicho sensível (saúde, dívida, vício), registre a dor sem transformá-la em alavanca de fraude. Dor real vira ângulo honesto; dor real vira também promessa de cura, e essa segunda cai.

## Passo a passo

1. Determine nicho e país pela tabela de derivação. Leia `benchmark.json` se existir.
2. Colete das 5 fontes. Registre a amostra por fonte.
3. Agrupe a linguagem por medo, não por demografia. O agrupamento é o trabalho.
4. Nomeie cada micro-persona pelo papel ameaçado.
5. Preencha os campos e o lastro de evidência de cada uma.
6. Cruze com o benchmark: quente, atacada ou órfã.
7. Grave `banco/publico.json` e rode o consolidador da planilha.

## Saída — `banco/publico.json`

```json
[
  {
    "id": "MP-001",
    "nome": "nome pelo papel ameaçado, não pela demografia",
    "papel_ameacado": "",
    "quem_compra": "usuario | terceiro",
    "quem_usa": "",
    "voz": "primeira_pessoa | terceira_pessoa",
    "faixa_etaria": "",
    "gatilho_emocional": "",
    "dor_central": "",
    "desejo_central": "",
    "objecao_principal": "",
    "crencas": [""],
    "vilao": "",
    "linguagem_literal": ["expressões exatas, como o público escreve"],
    "onde_vive": [""],
    "nivel_consciencia": "inconsciente | problema | solucao | produto | total",
    "ocorrencias": 0,
    "fontes_distintas": 0,
    "fonte_evidencia": "n itens em Amazon reviews e Reddit; exemplo: url",
    "pct_grupo_a": 0,
    "pct_grupo_b": 0,
    "indice_discriminacao": 0,
    "situacao_no_leilao": "quente | atacada | orfa | desconhecida",
    "confianca": "alta | media | baixa"
  }
]
```

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

- Cada micro-persona é nomeada por papel ameaçado, e não por faixa etária?
- Quem compra e quem usa foram separados onde divergem?
- Toda micro-persona tem 3+ ocorrências em 2+ fontes, ou está marcada baixa confiança?
- Cada uma tem lastro em `fonte_evidencia`, com link de exemplo?
- A linguagem literal foi copiada como o público escreve, sem tradução para termo técnico?
- Dor, desejo, objeção, crença e vilão preenchidos em todas?
- Cruzou com o benchmark pra marcar quente, atacada ou órfã?
- Nenhum indivíduo identificável foi perfilado?
- Gravou no contrato e rodou o consolidador?