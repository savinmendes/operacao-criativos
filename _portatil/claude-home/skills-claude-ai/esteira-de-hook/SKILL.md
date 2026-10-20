---
name: esteira-de-hook
description: "Transforma ângulo, clickbait e formato minerados numa leva de hooks pronta pra produção: cruza micro-persona x ângulo x formato e devolve N hooks etiquetados com variável isolada, regra 70/30 e nomenclatura pro gerenciador. Use para gerar hooks, ganchos, leva de criativos ou brief pro editor."
---

# A Esteira de Hook

A mineração descobre o que funciona. A esteira transforma isso em volume produzível. O gargalo de uma operação nunca é ideia, é produção: um editor faz um criativo por hora, e a esteira precisa entregar a ele um documento onde não sobra nenhuma decisão criativa a tomar.

Regra que governa tudo aqui: **cada hook muda uma variável só.** Se você troca ângulo, formato e avatar ao mesmo tempo e o anúncio performa, você não aprendeu nada e não consegue repetir. A esteira existe pra produzir volume sem destruir a capacidade de aprender com ele.

## Autonomia — execute, não pergunte

Roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

- **Não pergunte o que a coleta responde.** Disse o nicho? Abra a biblioteca e olhe. Decida amostra, alvo e prioridade pelos critérios deste arquivo e informe o que decidiu.
- **Só pare quando** faltar login, permissão de pasta, ou quando a escolha mudar o resultado e houver duas leituras igualmente defensáveis.
- **Execute a cadeia inteira sem pedir aprovação no meio.** Narre em uma linha por etapa enquanto faz.
- **Leia os JSONs do banco antes de começar.** Não refaça trabalho que já existe.
- **Entregue arquivo salvo com o caminho informado**, não texto no chat.
- **Ao terminar, diga três coisas:** o tamanho da amostra, o que saiu, e onde está.
- Leia os bancos e gere a leva inteira. Não pergunte quantas peças: o padrão é 30, três por micro-persona.

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

## Entrada esperada

Bloco 1, em `mineracao/` e `banco/`:
- `angulos.json` — de `mineracao-angulo`
- `clickbait.json` — de `mineracao-clickbait`
- `formatos.json` — de `mineracao-formatos-virais`
- `benchmark.json` — de `benchmarking-mercado` (micro-personas e Mapa de Fatias)
- `banco/criativos.json` — de `dissecacao-de-criativo` (a combinação real que estava junta em cada ad)

Bloco 2, em `banco/`:
- `publico.json` — de `estudo-de-publico`
- `virais.json` — de `mineracao-formatos-virais` (frente orgânica)

E o ativo:
- `banco-de-fatias.json` — histórico do que já foi testado

Mínimo pra rodar: **um ângulo validado e uma micro-persona.** Sem isso a skill não inventa, ela pede.

Se faltar formato, ela roda mas avisa que a distribuição de formato saiu por convenção e não por dado. Se faltar `benchmark.json`, avisa que as micro-personas não passaram por grupo de controle.

Antes de gerar, **leia o Banco de Fatias**: combinação já testada e queimada não volta como novidade. Se voltar, é como reteste declarado, com o motivo.

## O cruzamento — bloco 1 x bloco 2

A esteira é o ponto onde os dois bancos se encontram, e é daí que sai criativo que ninguém tem.

**Bloco 1 (o que já vende)** — `criativos.json`, `angulos.json`, `clickbait.json`, `benchmark.json`. É pago, validado por verba, e diz o que converte neste nicho.

**Bloco 2 (o que já prende)** — `publico.json` e `virais.json`. É público e orgânico, valida atenção antes de intenção, e chega mais cedo no ciclo.

O cruzamento produz três tipos de peça, e você deve gerar das três:

**Transplante de formato** — ângulo validado no pago, vestido com formato que está viralizando no orgânico e que ninguém do nicho usa em anúncio ainda. É a peça de maior retorno esperado, porque combina promessa provada com embalagem nova. Só entra se o viral estiver marcado `transferivel_para_ads`.

**Troca de avatar** — mesma combinação de ângulo e formato que já escala, com o avatar trocado pra atender uma micro-persona que o `publico.json` mapeou e o `benchmark.json` mostrou órfã. Leilão novo com ativos provados.

**Linguagem do público** — pega o hook que já performa e reescreve na linguagem literal do `publico.json`, mantendo estrutura e mecanismo. Variável isolada: só o vocabulário. É o teste mais barato do pack e um dos que mais move CTR.

Para cada peça, registre em `cruzamento` de onde veio cada metade. Sem isso você não consegue saber depois se o ganho veio do formato novo, do avatar ou da linguagem.

Se um dos dois blocos estiver faltando, a esteira roda só com o que tem e **avisa qual tipo de peça não foi gerada e por quê**. Nunca invente viral nem micro-persona pra completar o cruzamento.

## Regra 70/30

Toda leva se divide assim:

- **70% contenção** — tudo validado. Ângulo, formato, avatar e estrutura que já provaram. Aqui você não inova, você colhe. É o que paga a operação.
- **30% exploração** — uma variável nova por peça, sempre montada em cima de uma base validada. É o que impede a saturação e é onde nasce a próxima mina.

Nunca gere uma peça de exploração que muda duas coisas. Exploração é uma variável nova sobre três validadas, não um criativo do zero.

Distribua a exploração priorizando as variáveis com **índice de discriminação neutro** no benchmark: elas são convenção do nicho, não vantagem, então mexer nelas custa pouco e pode revelar fatia. Variável com índice alto positivo você trava, não explora.

## Anatomia de um hook

Todo hook tem duas variáveis independentes que precisam ser escritas separadas, porque são testadas separadas:

- **Hook visual (0-3s)** — o que aparece. Plano, cenário, quem está em cena, elemento de quebra, texto na tela.
- **Hook de copy** — a primeira fala ou a primeira linha.

O hook visual **não é escrito do zero**: ele sai da `receita_replicacao` do `clickbait.json`. Copie cenário, elenco, props, enquadramento, tratamento e anotação da receita e aplique a `adaptacao_nicho` ao seu produto. Se a receita estiver vazia ou o item estiver marcado como linha vermelha, aquele gancho não entra na leva — peça a captura à `mineracao-clickbait` em vez de inventar um visual.

Ao montar a leva, ranqueie os visuais também por `custo` da receita. Peça de contenção pode custar caro se o retorno já está provado; peça de exploração deve ser barata, porque a maioria vai morrer.

Um hook forte **empilha princípios**. Puxe do `clickbait.json` os princípios que cada padrão carrega e monte peças densas: especificidade + lacuna de informação + ancoragem temporal numa frase só é mais forte que um princípio isolado. Liste no output quais princípios cada hook empilha.

Todo hook mira o estado cognitivo **atenção**. Ele não vende, não explica e não convence: ele para o dedo e abre loop. Se o hook estiver tentando entregar mecanismo ou prova, ele virou body e você errou a peça.

## Como escrever (o que separa isso de prompt genérico)

- **Linguagem literal do público.** Use os termos que saíram dos comentários e reviews na mineração. Não escreva "declínio cognitivo" se o público fala "minha memória não é mais a mesma".
- **Ao lado da crença, nunca contra.** Hook que contraria o que o público jura ser verdade perde antes de começar.
- **Concreto vence abstrato.** Objeto, número, cena. "17 anos no rótulo" para mais que "descoberta surpreendente".
- **Terceira pessoa quando o nicho é sensível.** Narrativa em vez de "você/seu": agressivo sem convite a bloqueio.
- **Sem travessão. Sem "não é X, é Y". Sem "imagine só". Sem emoji decorativo.** São marcas de texto de IA e queimam o criativo na hora.
- **Versão negativa.** Para os hooks mais fortes, gere também o oposto. Viés da negatividade costuma bater mais e é teste barato.
- **Nada de alegação de linha vermelha.** Cura, garantia financeira, prova fabricada. Se o padrão minerado for radioativo, use o mecanismo abstrato e não a promessa.

## Nomenclatura — o que faz o Banco de Fatias funcionar

Cada hook sai com um código que carrega tudo que você precisa saber depois, quando o resultado voltar do gerenciador:

`[PRODUTO]-[MP##]-[ANG##]-[FMT##]-[VAR]-[###]`

- `MP##` micro-persona
- `ANG##` ângulo
- `FMT##` formato
- `VAR` a variável isolada nesta peça (`base` quando é contenção)
- `###` sequencial

Sem isso, o resultado volta do gerenciador e ninguém sabe o que validou. A nomenclatura não é organização, é o mecanismo de aprendizado da operação inteira.

## Passo a passo

1. Leia os JSONs disponíveis e o Banco de Fatias. Diga ao usuário o que encontrou e o que faltou.
2. Use o padrão: 30 peças, três por micro-persona, priorizando as de maior índice de discriminação. Só mude se o usuário pediu outra coisa.
3. Monte a matriz de peças: micro-persona x ângulo x formato, aplicando 70/30 e uma variável isolada por peça.
4. Descarte combinações queimadas no banco.
5. Escreva cada hook: visual e copy separados, princípios empilhados listados, hipótese do teste explícita.
6. Gere as versões negativas dos mais fortes.
7. Rode a checklist anti-IA em cada peça.
8. Salve o JSON, escreva as peças no Banco com `status: "a_testar"`, e gere a tabela de produção.

## Saída — duas peças

### 1. JSON em `esteira/leva-[data].json`

```json
[
  {
    "id": "NB-MP03-ANG07-FMT02-base-001",
    "tipo": "hook",
    "papel": "contencao | exploracao",
    "micro_persona_id": "MP-001",
    "micro_persona": "",
    "angulo_id": "ANG-007",
    "formato_id": "FMT-002",
    "clickbait_id": "CB-004",
    "variavel_isolada": "base | formato | avatar | comprimento | gancho_visual | mecanismo | ingrediente",
    "hipotese": "o que este teste responde se performar",
    "hook_visual": "o que acontece nos 3 primeiros segundos",
    "receita_visual": {
      "cenario": "", "elenco": "", "props": [""], "enquadramento": "",
      "texto_na_tela": "", "tratamento": "", "anotacao": "",
      "custo": "baixo | medio | alto", "referencia": "capturas/CB-004.png"
    },
    "origem": {
      "link_anuncio": "", "link_biblioteca": "", "link_funil": "", "anunciante": ""
    },
    "cruzamento": {
      "tipo": "transplante_formato | troca_avatar | linguagem_publico | contencao_pura",
      "veio_do_pago": "ANG-007, CB-004",
      "veio_do_organico": "VIR-012",
      "veio_do_publico": "MP-003"
    },
    "avatar": {
      "descricao": "", "papel": "", "voz": "primeira_pessoa | terceira_pessoa"
    },
    "hook_copy": "a primeira fala ou linha",
    "principios": ["especificidade", "information_gap", "temporal_anchoring"],
    "estado_cognitivo": "atencao",
    "nivel_consciencia": "inconsciente | problema | solucao | produto | total",
    "crenca_respeitada": "",
    "emocao": "",
    "linguagem_publico": [""],
    "versao_negativa": "",
    "linha_vermelha": false,
    "status": "a_testar"
  }
]
```

### 2. Tabela de produção (o que vai pro editor)

Uma linha por peça, sem nada além do necessário pra produzir:

| Código | Formato | Cenário | Elenco | Props | Enquadramento | Visual 0-3s | Fala de abertura | Texto na tela | Tratamento | Ref. |
|---|---|---|---|---|---|---|---|---|---|---|

A coluna `Ref.` aponta a captura de referência (`capturas/CB-004.png`) pra o editor ver o que está sendo replicado. Deixe claro no cabeçalho da tabela que a referência é para consulta, não para uso: o editor produz do zero seguindo a receita.

O editor não deve precisar abrir o JSON nem perguntar nada. Se a linha não é produzível sozinha, ela está incompleta.

## Demonstração de contraste (para aula ou apresentação)

Quando o usuário estiver mostrando a esteira pra uma plateia, rode duas vezes e mostre lado a lado:

1. **Genérico:** "me dê 10 hooks para um produto de memória". Sai o previsível, sem persona, sem variável isolada, sem nomenclatura, e com as marcas de IA.
2. **Com a esteira:** os mesmos 10 hooks saindo dos JSONs, cada um etiquetado, com hipótese e código.

O contraste é o argumento: a ferramenta é a mesma, o que muda é o método e os dados que alimentam ela.

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

- Cada peça muda uma variável só, e a variável está declarada?
- A leva respeita 70/30?
- A exploração ataca variáveis de índice neutro, não as travadas?
- Hook visual e hook de copy estão separados em toda peça?
- Todo hook visual veio de uma receita de replicação real, e não foi inventado?
- Toda peça carrega os links de origem, pro editor e pro gestor conferirem a referência?
- A leva tem peças dos três tipos de cruzamento, ou o motivo da ausência está declarado?
- Todo transplante de formato usa viral marcado `transferivel_para_ads`?
- Nenhum viral ou micro-persona foi inventado pra completar o cruzamento?
- Nenhuma peça usa gancho marcado como linha vermelha?
- Cada hook lista os princípios que empilha?
- Todo hook mira atenção, e nenhum virou body?
- A linguagem saiu dos termos reais do público?
- Nenhum travessão, nenhum "não é X, é Y", nenhuma marca de IA?
- Todos os hooks fortes têm versão negativa?
- Nomenclatura completa em toda peça?
- Combinações queimadas no Banco foram descartadas ou declaradas como reteste?
- A tabela de produção é executável sem nenhuma pergunta ao editor?