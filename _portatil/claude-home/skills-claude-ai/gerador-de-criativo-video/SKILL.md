---
name: gerador-de-criativo-video
description: "Analisa criativos de VÍDEO escalados, decompõe plano a plano e devolve o par de prompts (imagem base + imagem para vídeo) para cada plano, com fala e room tone. Cobre também animação leve, tipografia cinética e slideshow. Use para gerar criativo em vídeo ou prompt para Seedance/Kling/Veo/Sora."
---

# Gerador de Criativo — Vídeo

Gerador de vídeo puxado só por texto devolve a média da distribuição, e média parece banco de imagem. O caminho que funciona é outro: **você gera uma imagem base primeiro, e depois anima aquela imagem.**

A imagem base trava de uma vez o que texto nenhum consegue descrever — posição de câmera, enquadramento, luz, textura, imperfeição. O prompt de vídeo passa a descrever só o que **muda** a partir dali, que é uma tarefa muito menor e muito mais confiável.

Por isso a saída desta skill é sempre um **par por plano**: prompt de imagem base mais prompt de animação. Se o vídeo tem quatro planos, saem quatro pares.

## Autonomia — execute, não pergunte

Esta skill roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

### Não pergunte o que você consegue descobrir

O usuário disse o nicho? Abra a biblioteca e olhe. Não pergunte quantos anúncios coletar, qual anunciante analisar, que formato priorizar ou quantas peças gerar — decida pelos critérios que estão neste arquivo e siga. Pergunta que a coleta responde é pergunta que atrasa o trabalho.

**Só pare para perguntar quando:**
- Falta login, permissão de pasta ou acesso que só o usuário resolve
- A oferta dele não foi informada e ela muda o alvo da geração
- Duas leituras do mercado são igualmente defensáveis e a escolha muda o resultado

Fora disso, **decida e informe o que decidiu**, em vez de perguntar.

### Execute a cadeia inteira de uma vez

Coleta → organização em pastas → análise → matriz → prompts → arquivo salvo. **Sem parar entre etapas pedindo aprovação.** O usuário quer o entregável, não o acompanhamento passo a passo.

Narre o que está fazendo enquanto faz, em uma linha por etapa. Não peça "posso seguir?".

### As primeiras ações, nesta ordem

1. Crie a pasta de trabalho e as subpastas de referência
2. Leia os JSONs do banco que existirem — não refaça trabalho já feito
3. Abra a Ad Library no navegador, com o filtro do nicho e o de tipo de mídia
4. Colete até fechar as cotas, salvando os arquivos direto nas pastas certas
5. Analise, monte a matriz e escreva os prompts
6. Salve o arquivo de saída e o JSON, e só então volte a falar com o usuário

### Entregue arquivo, não texto no chat

O resultado é arquivo salvo na pasta, com caminho informado. Prompt colado no chat some na primeira rolagem. Prompt em arquivo a pessoa abre, copia e usa por semanas.

### O que você não faz sozinho

Você não gera a imagem nem o vídeo — isso acontece no gerador externo. O que você entrega é o prompt pronto para colar, organizado na ordem de uso, com o que fazer com cada saída.

Se o usuário tiver o gerador aberto e pedir, você pode abrir no navegador e colar o prompt. Mas o padrão é entregar o arquivo e deixar ele rodar no ritmo dele.

### Ao terminar, diga três coisas

Quantas referências entraram e como ficou a amostra, quantas peças saíram e qual variável cada uma testa, e onde estão os arquivos. Nada além disso.

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

## Que oferta vale modelar — os 4 filtros

Criativo escalando não significa oferta modelável. Rode os quatro filtros **antes** de gastar captura e frame. Os filtros 1 e 2 são eliminatórios: falhou, próxima oferta.

### Filtro 1 — Ela está escalando de verdade? (eliminatório)

Tudo verificável na biblioteca:

| Sinal | Corte |
|---|---|
| Longevidade | acima do corte do ticket (10, 21, 30 ou 45 dias) |
| Criativos únicos simultâneos | 8 ou mais — únicos, não linhas infladas por posicionamento |
| Reposição nos últimos 30 dias | tem criativo antigo **e** criativo novo no ar |
| Ângulos distintos rodando | 2 ou mais |

Um ângulo só, parado há meses, sem reposição, é zumbi esquecido no ar. Cinco ângulos com reposição contínua é sistema. Falhou dois dos quatro, não é oferta escalada.

### Filtro 2 — Você consegue executar? (eliminatório)

- **Entregável.** Digital pronto (PDF, área de membros, planilha) você replica na semana. Físico traz estoque, logística, importação e reembolso. Serviço traz equipe.
- **Autoridade.** A oferta funciona sem aquele rosto específico? Se ela só existe porque o expert é conhecido, você não replica — você compete com a reputação dele.
- **Elenco.** Você consegue produzir o avatar que ela usa? Idioma, faixa etária, cultura, disponibilidade.
- **Caixa.** Low ticket exige volume de criativo e verba de mineração. High ticket exige página, prova e às vezes atendimento.

Se um desses é não, a oferta é boa e não é sua. Isso não é derrota, é economia.

### Filtro 3 — Ainda tem espaço? (pontua)

- Cola a headline entre aspas na busca da biblioteca e conta anunciantes distintos rodando o mesmo ângulo: **1 a 2** é fatia rala e dá pra entrar; **3 a 4** é disputada e exige diferencial; **5 ou mais** é lotada e só se entra por micro-persona órfã ou país novo.
- Cruza com o Mapa de Fatias: sobrou micro-persona que ninguém ataca?
- Existe país ou idioma onde a oferta ainda não roda?

### Filtro 4 — A operação sustenta? (pontua)

- Página abre, checkout ativo, gateway reconhecível.
- **Existe escada de preços?** Order bump e upsell significam LTV maior, e LTV maior significa que ela aguenta CPA mais caro que o seu. É sinal bom sobre o mercado e alerta sobre o seu bolso: você vai disputar leilão com quem pode pagar mais.
- Comentários com volume e com teor de quem comprou indicam entrega real, não só impressão.
- Reclamação em volume moderado é sinal de escala. Enxurrada de pedido de reembolso é sinal de que ela cai em breve, e você chegaria junto com a queda.

### A pergunta que fecha

**Se essa oferta é tão boa e tão fácil, por que só ele está rodando?**

Três respostas possíveis: existe uma barreira que você ainda não viu (produto, autoridade, logística, fornecedor), ela é nova demais para ter sido copiada, ou ela não está funcionando e você leu ruído em amostra pequena. Descubra qual antes de gastar a primeira hora.

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

## O fluxo, do começo ao fim

1. Coleta e extração de frames dos vídeos escalados do nicho
2. Decomposição plano a plano: formato, ordem, duração, corte, fala, texto
3. Mapa de planos da peça nova, com a base validada e uma variável trocada
4. Para cada plano: prompt de imagem base → o usuário gera no gerador de imagem
5. Para cada plano: prompt de imagem para vídeo → o usuário sobe a imagem no gerador de vídeo junto com esse prompt
6. Montagem na ordem, com o texto de tela entrando em edição

## O que dá e o que não dá

**O Claude não assiste vídeo.** A decomposição sai de frames extraídos, legenda queimada e transcrição.

O que **sai** dos frames: quantos planos, o que acontece em cada um, sujeito, figurino, cenário, enquadramento, texto na tela, mudança de ambiente, e a ordem narrativa.

O que **não sai**: movimento de câmera, velocidade da ação, tom de voz, trilha, energia da atuação. Marque como `inferido` e **nunca escreva no prompt uma direção de câmera que você não observou** — o gerador obedece e a peça sai diferente do que funcionava.

Com menos de 6 frames por vídeo, não decomponha: diga que a amostra não permite e peça mais captura.

## Extração — o passo que decide tudo

Duas passadas por vídeo. A primeira dá a ordem, a segunda dá o detalhe.

**Passada 1 — cortes.** Extrai um frame por mudança de plano. O número de arquivos gerados **é** a contagem de cortes, e é o único dado de ritmo que você obtém sem assistir:

```bash
mkdir -p referencias/frames
ffmpeg -i criativo.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr \
  referencias/frames/corte_%03d.png 2>&1 | grep showinfo | grep -o 'pts_time:[0-9.]*'
```

O `pts_time` de cada linha é o segundo em que aquele corte acontece. Anote: é a linha do tempo da peça.

**Passada 2 — detalhe do início.** Os três primeiros segundos decidem o Thumb Stop e merecem densidade maior:

```bash
for t in 0 0.3 0.6 1 1.5 2 3; do
  ffmpeg -y -ss $t -i criativo.mp4 -frames:v 1 -q:v 2 \
    "referencias/frames/inicio_${t}s.png" 2>/dev/null
done
```

Registre sempre: quantos vídeos, quantos cortes cada um, quantos frames lidos.

## Fase 1 — Decomposição do vídeo escalado

### A camada macro

- **Formato:** UGC selfie, react de podcast, entrevista de rua, GC, notícia, tutorial, demonstração, depoimento, editadão.
- **Estrutura narrativa e onde cada bloco começa:** gancho, problema, mecanismo, prova, oferta, chamada. Anote o segundo de cada virada.
- **Ritmo:** número de cortes dividido pela duração. Um corte a cada 1 a 1,5 segundo é editadão; um corte a cada 5 segundos é conversa.
- **Quem fala e para quem:** primeira ou terceira pessoa, olhando para a câmera ou para o lado.

### A camada de plano

Para cada corte identificado:

| Campo | O que registrar |
|---|---|
| Tempo | início e fim em segundos |
| Função | gancho, problema, mecanismo, prova, oferta, chamada |
| Sujeito | quem aparece, faixa etária aparente, papel |
| Figurino | roupa, cor, formalidade |
| Cenário | cômodo, o que aparece ao fundo |
| Enquadramento | close, médio, aberto, mãos, produto |
| Ação | o que acontece no plano, uma frase |
| Props | objetos em cena |
| Texto na tela | conteúdo, posição, estilo de legenda |
| Fala | a linha exata, da legenda queimada |
| Luz | fonte e direção |

### A ordem é o ativo

O que se modela de um vídeo escalado não é o assunto — é a **sequência**. Registre a ordem como padrão reutilizável:

`close no rosto (gancho) → mãos com o objeto (mecanismo) → plano médio falando (prova) → tela do produto (oferta) → rosto olhando pra câmera (chamada)`

Essa sequência é o que você reaproveita com outro ângulo, outro avatar e outro nicho. É o equivalente de formato, mas no eixo do tempo.

## Como se monta um criativo de 60 segundos

Antes de qualquer prompt, entenda as três unidades. Confundir elas é o que faz a pessoa achar que precisa gerar 40 clipes.

### As três unidades

**Bloco narrativo** — a função dentro do argumento: gancho, problema, mecanismo, prova, oferta, chamada. Uma peça tem de 4 a 8 blocos, e é isso que você copia da base validada.

**Geração** — um clipe que o gerador produz de uma vez, tipicamente 5 a 8 segundos. **Cada geração precisa de uma imagem base.** É a unidade de custo.

**Corte** — decisão de edição, tomada depois, em cima do material gerado. **Corte não é geração.** Você gera 8 segundos e usa 3.

### A conta, por duração alvo

| Peça | Blocos | Gerações | Imagens base | Cortes no final |
|---|---|---|---|---|
| 15s | 3 | 3 a 4 | 2 a 3 | 6 a 10 |
| 30s | 4 a 5 | 5 a 7 | 4 a 5 | 15 a 25 |
| 60s | 6 a 8 | 8 a 12 | 6 a 9 | 30 a 45 |

Imagens base são menos que gerações porque **o mesmo setup se reaproveita**: a mesma imagem do falante serve para vários trechos de fala.

### De onde vem o ritmo de corte

Não das gerações. Vem da edição.

Você gera 8 segundos de alguém falando e usa 3. Gera outro trecho no mesmo cenário e usa 2. Intercala um clipe de b-roll de 1,5 segundo. O editadão de um corte por segundo nasce aí, cortando o gerado — não gerando um clipe por corte.

### O b-roll é o que carrega o ritmo, e é o mais barato

Gere de 3 a 5 clipes curtos **sem fala e sem rosto**: mãos manipulando o objeto, close no produto, tela do celular, detalhe do cenário, o ingrediente caindo.

Eles são baratos, não precisam de consistência de personagem, e são o que você intercala para criar corte sem gerar mais falante. Numa peça de 60 segundos, metade do tempo de tela costuma ser b-roll.

### Falante contínuo — o padrão do UGC

Para talking head, não gere um clipe por frase. Faça assim:

1. Uma imagem base do falante, no cenário definitivo
2. **Várias gerações a partir da mesma imagem**, cada uma com um trecho da fala no prompt de animação
3. Jump cut entre elas na edição

O jump cut com pequena variação de enquadramento é exatamente o que dá cara de gravação real. E o custo é uma imagem base para o bloco inteiro.

### Como fica um exemplo de 60 segundos

| Bloco | Função | Gerações | Imagem base | Tempo final |
|---|---|---|---|---|
| 1 | Gancho | 1 | BASE-A (falante) | 0 a 4s |
| 2 | Problema | 2 | BASE-A reaproveitada | 4 a 16s |
| 3 | Mecanismo | 2 | BASE-B (mãos/objeto) | 16 a 30s |
| 4 | Prova | 2 | BASE-A + BASE-C (tela) | 30 a 42s |
| 5 | Oferta | 1 | BASE-D (produto) | 42 a 52s |
| 6 | Chamada | 1 | BASE-A reaproveitada | 52 a 60s |
| — | B-roll de recheio | 3 | BASE-E, F, G | intercalado |

Total: **12 gerações, 7 imagens base**, e o ritmo de corte se cria na edição.

### A regra de decisão

Antes de escrever prompt, monte esta tabela para a peça. Ela define quantas imagens base você precisa e quais gerações reaproveitam qual. **Sem ela você gera demais e ainda fica com material que não monta.**

## Fase 2 — O mapa de planos da peça nova

1. **Escolha a base validada:** o vídeo com maior longevidade dentro da fatia alvo.
2. **Copie a ordem, não o conteúdo.** Mesma sequência de funções e durações parecidas.
3. **Troque uma variável.** Avatar, cenário, formato macro, ângulo, ritmo ou hook visual do plano 1. Uma só.
4. **Monte a tabela de blocos** da seção acima: quantos blocos, quantas gerações por bloco, qual imagem base cada geração usa. Uma imagem base atende várias gerações quando o cenário e o enquadramento são os mesmos — é assim que 12 gerações cabem em 7 bases.
5. **Trave o personagem.** Se a mesma pessoa aparece em mais de um plano, a imagem base dela é gerada uma vez e reaproveitada como referência nos demais. Personagem trocando de rosto entre cortes é o erro mais visível de vídeo gerado.

## Fase 3A — Prompt da imagem base (um por plano)

A imagem base é o **primeiro frame daquele plano**, no estado inicial. Ela não mostra a ação acontecendo, mostra o instante antes.

```
[RECURSO DE INTERRUPÇÃO, se for o plano 1] ·
[TIPO: still de vídeo de celular, sem produção] ·
[SUJEITO: idade aparente, expressão no estado INICIAL, papel] ·
[FIGURINO com cor e caimento] · [POSIÇÃO das mãos e do corpo] ·
[PROPS: o que está em cena e ONDE, descrito com precisão] ·
[O QUE NÃO ESTÁ em cena] ·
[CENÁRIO com detalhe de fundo] ·
[ENQUADRAMENTO e altura de câmera] ·
[LUZ: fonte, dureza, direção] · [PALETA] ·
[PROPORÇÃO 9:16]

Negative: texto, letras, marca d'água, mãos deformadas,
estética de banco de imagem, pessoa famosa, estúdio, pose de revista
```

**A linha do que não está em cena é obrigatória.** Se você não descrever o vazio, o gerador preenche, e o que ele inventa vira artefato que reaparece no vídeo.

## Fase 3B — Prompt de imagem para vídeo (um por plano)

Este vai para o gerador de vídeo **junto com a imagem gerada no passo anterior**. Ele descreve só o que muda.

```
Imagem base: [arquivo do plano n]
Duração: [n] segundos. 9:16. Plano contínuo. Estilo UGC, celular na mão.

[0-2s] [O que muda a partir da imagem: movimento do sujeito, das mãos,
do objeto. Expressão que se transforma. 2 a 3 frases específicas.]

[2-5s] [Continuação. O que entra em quadro, o que sai. Mesma luz,
mesmo cenário, mesma pessoa.]

Câmera: [estática, ou tremor leve de mão. Movimento só se observado
na referência.]

Áudio: [Voz: idade, gênero, tom, energia.] [Room tone do ambiente.]
Fala natural com pausas. "[a fala exata, com contração e palavra
de preenchimento]"
```

### Regras de escrita do prompt de animação

- **Descreva a mudança, não a cena.** A cena já está na imagem. Repetir a descrição confunde o modelo e ele redesenha em vez de animar.
- **Um arco de ação por plano.** Duas mudanças de cena no mesmo prompt viram borrão.
- **A luz e o cenário permanecem**, ditos explicitamente, senão derivam entre segundos.
- **Densidade por bloco:** 2 a 3 frases por bloco de tempo, cobrindo o que cada mão faz, a expressão e o que entra ou sai de quadro. O que você não descreve, o gerador inventa.

## O vocabulário anti-IA

Esta é a diferença entre um vídeo que parece anúncio e um que parece que alguém filmou ontem. Palavra de cinema puxa o modelo para o cluster de produção profissional, e uma palavra só arrasta a geração inteira.

**Use sempre:** celular na mão, luz natural, luz de janela, estilo UGC, tremor leve, casual, sem produção, 9:16, gravado em casa.

**Nunca use:** cinematográfico, marca de câmera (ARRI, RED, Blackmagic), anamórfico, granulado de filme, luz dramática, flare, chicote de câmera, grua, dolly, steadicam, gimbal, ângulo holandês, correção de cor, LUT, bokeh, épico, deslumbrante, câmera lenta (a não ser "câmera lenta de celular"), profundidade de campo sozinha (diga "profundidade de campo de celular").

Peça a imperfeição de propósito: enquadramento levemente torto, luz irregular, foco que hesita, fundo bagunçado.

## Áudio — não é acessório

Geradores atuais produzem fala com sincronia labial junto do vídeo. Prompt sem direção de áudio devolve voz de narrador, e voz de narrador mata UGC.

**Personagem de voz:** idade, gênero, tom, energia. "Voz masculina calorosa, uns 40 anos, genína, energia de pai, sem locação."

**Room tone casado ao cenário:** banheiro tem reverb de azulejo; quarto é abafado e sem eco; cozinha é aberta com ruído ambiente; carro é fechado e abafado; rua tem ambiência e vento; sala é quente e mobiliada.

**Fala escrita para não parecer roteiro:** contração, palavra de preenchimento, frase quebrada.
Bom: "então tipo, faz duas semanas que eu uso e sinceramente? funciona mesmo."
Ruim: "este produto revolucionário transformou minha rotina."

## Os formatos com movimento parcial

Nem toda peça precisa de vídeo completo, e estes custam uma fração:

**Animação leve** — parte de uma imagem base e move um elemento só:
```
Imagem base: [arquivo]
Elemento que se move: [vapor subindo, líquido girando, folha balançando]
O que fica parado: [tudo o mais, explicitamente]
Loop: 2 a 4 segundos. Movimento sutil, não rouba a leitura do texto.
```

**Tipografia cinética** — não usa gerador, é editor: linhas na ordem, tempo de entrada de cada uma, palavra que ganha destaque e quando, fundo, trilha licenciada.

**Slideshow** — vários prompts de imagem base mais ordem e tempo por quadro, com corte seco entre eles. É o mais barato de todos e quase ninguém no BR usa.

## Consistência de personagem

O erro mais visível de vídeo gerado é o rosto mudando entre cortes.

- Gere a imagem base do personagem **uma vez** e reutilize como referência em todos os planos onde ele aparece.
- Descreva o personagem com os **mesmos termos exatos** em todos os prompts. Mudar "mulher de uns 40" para "senhora" já muda o rosto.
- Figurino e cabelo repetidos literalmente em cada plano.
- Confira antes de montar: se o rosto derivou, regenere aquele plano com a mesma referência em vez de aceitar.

## Linha vermelha (não negociável)

- **Nunca gere semelhança de pessoa real.** Nem celebridade, nem o apresentador do concorrente, nem foto de pessoa achada em rede social usada como referência de rosto. Referência serve para travar luz, enquadramento e textura — o rosto se gera ou se filma com elenco próprio.
- **Nunca reproduza o vídeo do concorrente.** A captura é referência interna. O que você entrega é uma peça nova que usa a mesma sequência.
- **Pessoa gerada por IA não pode ser apresentada como cliente ou profissional real.** Depoimento sintético e especialista inventado com credencial são publicidade enganosa. Se a peça precisa de depoimento, vira briefing de gravação com pessoa real.
- **Referência limpa:** nunca use como referência imagem com emoji, marca d'água, texto sobreposto ou interface de app. O gerador recria tudo que vê como objeto físico.
- **Trilha licenciada sempre.** Áudio em alta é livre no orgânico e é licenciamento em anúncio pago.
- **O prompt herda a alegação.** Ângulo marcado `linha_vermelha` não vira peça.

## Briefing de gravação

Quando a peça pede pessoa real, que costuma vencer o gerado em resposta direta:

```
Elenco: [perfil, nunca pessoa específica]
Local: [cômodo e o que precisa aparecer ao fundo]
Props: [lista]
Figurino: [descrição]
Câmera: celular, [orientação], [altura]
Luz: [o arranjo mais simples que resolve]
Roteiro por plano: [as falas, na ordem]
Texto na tela: [o que entra em edição]
Tempo estimado: [minutos]
```

## Formato exato da saída — siga isto sempre

O entregável é **um arquivo markdown** em `geracao/video-[nicho]-[data].md`.

A unidade é o **criativo**. Cada criativo tem três partes, nesta ordem: **todas as imagens dele**, depois **todos os vídeos dele**, depois a **montagem**. Nunca intercale imagem e vídeo — a pessoa abre o gerador de imagem uma vez, gera tudo, e só então vai para o de vídeo.

````
# Leva de vídeo — [nicho] — [data]

## O que você recebeu
- **[N] criativos** · [X] contenção · [Y] exploração
- **Base validada:** [código] — [formato macro], [N]s
- **Amostra:** [N] anunciantes, [N] controles, [N] cortes detectados
- **Assumido:** [derivações, em uma linha]

## Como usar
Para cada criativo, na ordem: gere todas as imagens → transforme todas em vídeo → monte.

═══════════════════════════════════════════════

# CRIATIVO 01 · [CÓDIGO]

**Testa:** [variável] | **Hipótese:** [o que responde]
**Formato:** [macro] | **Duração:** [N]s | **Blocos:** [N]
**Produção:** [N] imagens → [N] vídeos

### Mapa do criativo 01

| Bloco | Função | Tempo | Usa a imagem | Gera os vídeos |
|---|---|---|---|---|
| 1 | Gancho | 0-4s | IMG-A | VID-01 |
| 2 | Problema | 4-16s | IMG-A | VID-02, VID-03 |
| 3 | Mecanismo | 16-30s | IMG-B | VID-04, VID-05 |
| 4 | Prova | 30-42s | IMG-A, IMG-C | VID-06, VID-07 |
| 5 | Oferta | 42-52s | IMG-D | VID-08 |
| 6 | Chamada | 52-60s | IMG-A | VID-09 |
| — | B-roll | intercalado | IMG-E, F, G | VID-10, 11, 12 |

---

## CRIATIVO 01 · PARTE 1 — Gere estas [N] imagens

Abra o gerador de imagem. Gere **todas** antes de ir para a parte 2.

### IMG-A — [o que é] · usada nos blocos 1, 2, 4, 6

```
[prompt da imagem base]
```
**Negative:** `[lista]` · **Proporção:** 9:16
**Salve como:** `C01-IMG-A.png`

### IMG-B — [o que é] · usada no bloco 3

```
[prompt]
```
**Negative:** `[lista]` · **Proporção:** 9:16
**Salve como:** `C01-IMG-B.png`

[continue até a última]

**Antes de seguir, confira:** o rosto é o mesmo onde precisa ser? nenhuma imagem veio com texto? proporção certa em todas?

---

## CRIATIVO 01 · PARTE 2 — Transforme em vídeo

Abra o gerador de vídeo. Para cada item: suba a imagem indicada e cole o prompt.

### VID-01 · bloco 1 · gancho · 4s

**Suba:** `C01-IMG-A.png`
```
[prompt de animação]
```
**Duração:** 4s · **Câmera:** [estática | tremor leve]
**Salve como:** `C01-VID-01.mp4`

### VID-02 · bloco 2 · problema · 6s

**Suba:** `C01-IMG-A.png` *(a mesma da VID-01)*
```
[prompt de animação, outro trecho da fala]
```
**Duração:** 6s · **Câmera:** [x]
**Salve como:** `C01-VID-02.mp4`

[continue até a última]

---

## CRIATIVO 01 · Ad text

**Micro-persona:** [MP-0X] · **Estrutura do hook:** [fórmula] · **[N] caracteres**

```
[hook — nomeia a micro-persona nas primeiras linhas]

[body — mecanismo, prova, transição]

[a linha que pede o clique]
```

*(Vai no campo de texto do anúncio, não no vídeo. Mesma régua da `gerador-de-criativo-imagem`: comprimento na mediana do grupo A.)*

---

## CRIATIVO 01 · PARTE 3 — Monte

| Ordem | Clipe | Entra | Como cortar | Texto na tela |
|---|---|---|---|---|
| 1 | `C01-VID-01.mp4` | 0s | inteiro | [texto] |
| 2 | `C01-VID-02.mp4` | 4s | usar 0-5s | [texto] |
| 3 | `C01-VID-10.mp4` | 9s | 1,5s de inserção | — |

**Trilha:** [licenciada, ou sem trilha]
**Exporte como:** `C01-final.mp4`

═══════════════════════════════════════════════

# CRIATIVO 02 · [CÓDIGO]

[mesma estrutura: mapa, parte 1, parte 2, parte 3]

═══════════════════════════════════════════════

## Checagem antes de subir
- [ ] O rosto é o mesmo onde precisa ser
- [ ] Nenhum termo de cinema entrou nos prompts
- [ ] Todo vídeo tem voz e room tone
- [ ] Os 3 primeiros segundos param o dedo sem som
- [ ] Todo criativo tem ad text com hook que nomeia a micro-persona

## Referências usadas
| Criativo | Anunciante | Link do anúncio | Biblioteca | Funil |
|---|---|---|---|---|
````

### As regras do documento

- **A unidade é o criativo, não o bloco.** Tudo do criativo 01 fica junto, do mapa à montagem.
- **Imagem e vídeo nunca se intercalam.** Parte 1 esgota o gerador de imagem, parte 2 esgota o de vídeo.
- **O mapa abre o criativo.** Ele diz quantas imagens gerar e qual vídeo usa qual — é o que impede gerar demais.
- **Nomenclatura fixa:** `C[nn]-IMG-[letra].png` e `C[nn]-VID-[nn].mp4`. Vídeo que reaproveita imagem diz isso em itálico.
- **Nada de prompt no chat.** No chat vão só três linhas: amostra, o que saiu, onde está.

### O índice estruturado

Além do markdown, salve `geracao/leva-video.json`:

```json
[
  {
    "id": "VID-001",
    "base_validada": "CRI-004",
    "variavel_isolada": "avatar | cenario | formato | angulo | ritmo | hook_visual",
    "hipotese": "o que este teste responde se performar",
    "papel": "contencao | exploracao",
    "micro_persona_id": "MP-003",
    "angulo_id": "ANG-007",
    "formato_macro": "ugc_selfie | react | entrevista_rua | gc | noticia | tutorial | demonstracao | depoimento | editadao",
    "duracao_total_s": 0,
    "cortes": 0,
    "ordem_funcional": ["gancho", "problema", "mecanismo", "prova", "chamada"],
    "personagem_travado": "PERS-01",
    "planos": [
      {
        "n": 1,
        "funcao": "gancho",
        "inicio_s": 0,
        "fim_s": 3,
        "prompt_imagem_base": "",
        "negative": "",
        "prompt_animacao": "",
        "camera": "estatica | tremor_leve",
        "audio_voz": "",
        "audio_room_tone": "",
        "fala": "",
        "texto_na_tela": "",
        "reaproveita_base_do_plano": null
      }
    ],
    "campos_inferidos": ["o que NÃO foi observado nos frames"],
    "amostragem": { "videos_lidos": 0, "cortes_detectados": 0, "frames_lidos": 0 },
    "linha_vermelha": false,
    "origem": { "link_anuncio": "", "link_biblioteca": "", "link_funil": "" },
    "status": "a_testar"
  }
]
```

Escreva as peças no `banco-de-fatias.json` com `status: "a_testar"`.

## Checklist de qualidade
- Tudo que era derivável foi derivado do mercado, em vez de perguntado?
- A derivação saiu SÓ do grupo A, e nada foi tirado do grupo B nem da amostra somada?
- Dentro do grupo A, a extração saiu dos controles e das variações — e não dos testes recentes?
- A contagem foi por anunciante distinto, e não por anúncio?
- Elemento com menos de 3 anunciantes distintos foi marcado como hipótese?
- O grupo A fechou com 8+ anunciantes, ou o afrouxamento do corte está declarado?
- O que foi assumido está declarado em uma linha?

- A cadeia rodou inteira sem parar pedindo aprovação no meio?
- A saída é arquivo salvo com caminho informado, e não prompt colado no chat?
- O markdown segue o formato exato: um plano, dois passos, na ordem?
- A tabela de produção da peça foi montada antes dos prompts, com a contagem de gerações e imagens base?
- Existe b-roll suficiente para criar o ritmo de corte sem gerar mais falante?
- Todo arquivo segue C[nn]-IMG-[letra] e C[nn]-VID-[nn], e o mapa abre cada criativo?
- As partes 1 e 2 estão separadas, sem intercalar imagem e vídeo?, e a tabela de montagem fecha cada peça?
- A oferta passou pelos filtros 1 e 2 antes de qualquer captura?
- A extração rodou nas duas passadas, e a contagem de cortes está registrada?
- Menos de 6 frames por vídeo foi tratado como amostra insuficiente, e não decomposto assim mesmo?
- Cada plano tem o par completo: prompt de imagem base e prompt de animação?
- A imagem base descreve o estado INICIAL, e não a ação acontecendo?
- O prompt de animação descreve só o que muda, sem repetir a cena?
- Todo prompt de imagem base declara o que NÃO está em cena?
- Nenhum termo da lista de cinema entrou em prompt nenhum?
- Todo plano tem direção de áudio com personagem de voz e room tone do ambiente?
- A fala tem contração e palavra de preenchimento, e não soa a roteiro?
- O personagem foi travado por referência e descrito com os mesmos termos em todos os planos?
- Nenhuma direção de câmera foi escrita sem ter sido observada na referência?
- Nenhuma semelhança de pessoa real, nenhuma credencial inventada, nenhum depoimento sintético?
- A ordem funcional foi copiada da base validada, com uma variável trocada?
- Links de origem em toda peça e escrita no Banco de Fatias?