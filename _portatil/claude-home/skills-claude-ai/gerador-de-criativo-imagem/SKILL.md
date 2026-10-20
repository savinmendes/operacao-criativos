---
name: gerador-de-criativo-imagem
description: "Analisa criativos de IMAGEM escalados na Ad Library e devolve prompt da base visual, especificação da camada de edição e o ad text, sempre variando uma variável sobre base validada. Use para gerar criativo de imagem, prompt de imagem, ou variar um estático que está escalando."
---

# Gerador de Criativo — Imagem

As outras skills catalogam. Esta produz. Ela pega o que está escalando, destrincha até o nível de cena, e devolve **prompts executáveis** — não descrição, não conceito, prompt que a pessoa cola no gerador ou entrega pro editor.

A regra que governa tudo: **nunca gere um criativo do zero.** Todo prompt sai de uma base validada com **uma variável trocada**. Criativo inventado inteiro é aposta; criativo com uma variável nova sobre três validadas é teste.

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

## O que dá e o que não dá (leia antes de prometer)

**Imagem — análise profunda de verdade.** Screenshot de criativo estático ou de frame: dá pra ler sujeito, faixa etária aparente, figurino, cenário, objetos em cena, enquadramento, direção do olhar, fonte de luz, paleta, textura, texto na tela, anotação e o quanto parece anúncio ou conteúdo. É aqui que a skill é forte.

**Vídeo — não é assunto desta skill.** Se a referência é vídeo, ou se a peça precisa de movimento, mande para `gerador-de-criativo-video`. Frame de vídeo aqui só contamina a amostra.

**O que fica invisível mesmo em imagem:** a fonte exata, o software usado na edição e a intenção por trás de uma escolha estética. Marque como `inferido` e siga.

## Entrada esperada

- **Mínimo:** o nicho, ou um link de anúncio, ou prints.
- **Ideal:** `banco/criativos.json` da `dissecacao-de-criativo`, `benchmark.json` do Raio-X e **`mineracao/clickbait.json` da mineração de hook visual**.
- O `clickbait.json` é o mais importante dos três para esta skill: o campo `anatomia_visual` já traz enquadramento, sujeito, olhar, contraste, elemento de quebra e anotação de cada gancho que está parando o dedo no nicho, e o `receita_replicacao` já traz cenário, elenco, props e custo. **Se ele existir, o hook visual não se inventa — se herda.** Com eles você herda micro-personas, ângulos validados e o Mapa de Fatias, e pula direto pra geração.
- Se não houver banco, faça uma passada própria: 10 a 20 criativos do topo por longevidade, com frames extraídos pelo pipeline abaixo.
- **Nunca aceite só um link como entrada.** Link não é imagem. Rode o pipeline ou peça a captura.

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

## De onde vêm os pixels — o pipeline

Esta é a parte que decide se a skill roda ou não. **Você não analisa criativo a partir de link.** A Ad Library bloqueia acesso automatizado; o que funciona é navegador logado mais captura.

### Separe na coleta, não depois

Se as duas referências caem na mesma pasta, um frame vira referência de imagem por acidente e você não percebe. Separe na origem:

**1. Filtre por tipo de mídia na própria biblioteca.** A Ad Library tem filtro de tipo de mídia. Rode duas coletas distintas, uma de imagem e uma de vídeo, e nunca as duas juntas.

**2. Duas pastas, nomes que não se confundem:**

```
referencias/
  estaticos/     ← criativo de IMAGEM, arquivo original ou screenshot do card
  frames/        ← frames extraídos de VÍDEO, nunca usados como referência de imagem
```

**3. A regra que a skill obedece sem exceção:** arquivo que veio de `frames/` alimenta apenas a trilha de vídeo. Ele nunca entra na Fase 1A nem gera prompt de imagem, por mais que a composição pareça boa.

**4. Se estiver em dúvida sobre o tipo, olhe a proporção de texto.** Criativo de imagem reserva um terço ou mais do quadro para bloco de texto e quase sempre tem botão desenhado. Frame de vídeo tem legenda de fala, geralmente centralizada e curta, e nunca tem botão. Na dúvida, trate como frame.

**5. Cotas de coleta — é isso que impede a leva de virar só vídeo com pessoa falando.**

- **Colete apenas referências estáticas.** Vídeo é o mais fácil de achar na biblioteca e domina a amostra sozinho se você deixar. Se o filtro devolver pouco estático, procure mais — não complete com frame.
- **Nenhuma estrutura passa de 30% da amostra.** Se sete de dez são manchete sobre cena, volte e procure outras.
- **Mínimo 3 estilos visuais distintos.** Se tudo veio fotorrealista, você não coletou formato, coletou o padrão do nicho.
- **Pelo menos 1 tentativa em cada nível de movimento**, mesmo que o nicho não use. Nível que não existe no nicho é candidato a fatia vazia, não motivo para pular.
- Se uma cota não fechar, **diga qual não fechou e por quê** em vez de completar com mais do mesmo.

**6. Registre a contagem separada.** "12 estáticos e 8 vídeos" é uma amostra. "20 referências" não diz nada, porque você não sabe qual trilha ficou sem base.

### Criativo estático

1. Abra a Ad Library no navegador com o filtro do nicho **e o filtro de tipo de mídia**. Marque **imagens e memes** — a opção de meme devolve boa parte dos estáticos de resposta direta que o filtro de imagem sozinho não traz.
2. Salve a imagem do criativo, ou tire screenshot do card, em `referencias/estaticos/`.
3. Leia o arquivo. É aqui que a análise profunda acontece de verdade.

### Se aparecer vídeo na coleta

Descarte e registre a contagem. Vídeo é matéria-prima da `gerador-de-criativo-video`, e frame contamina a amostra de imagem. Não extraia frames aqui.

### Ordem de preferência das fontes

1. Arquivo baixado com frames extraídos — melhor qualidade de leitura
2. Screenshots do usuário — funciona, cobre menos
3. Print único do card — só dá pra ler hook visual, não a peça
4. Só o link — **não é fonte.** Peça a captura antes de prometer análise

### O que registrar sempre

Quantas referências de cada trilha (estáticos e vídeos, contados separado), quantos frames por vídeo, em que tempos, e se veio de arquivo ou de screenshot. Análise feita com 3 frames e análise feita com 12 não valem a mesma coisa, e o usuário precisa saber qual ele recebeu.

( O arquivo baixado é referência interna de pesquisa, como um diretor de arte guarda numa pasta. Ele não vira ativo seu, não é republicado e não entra em campanha. )

## A regra das duas trilhas

**Criativo de imagem se modela de criativo de imagem. Criativo de vídeo se modela de criativo de vídeo.** Esta skill cobre só a primeira.

Um frame de vídeo não é um criativo de imagem. O frame é um instante de uma sequência: quem sustenta o argumento é a fala que vem depois. O criativo de imagem entrega o argumento inteiro num quadro só, porque não existe "depois".

Por isso ele tem elementos que frame nenhum tem: bloco de texto dominante, hierarquia de leitura desenhada, botão falso, anotação, comparação lado a lado. Gerar prompt de imagem a partir de frame de vídeo produz foto bonita que não vende.

**Se a referência é vídeo, ou se a peça precisa de movimento** — animação leve, tipografia cinética, slideshow ou vídeo completo — **mande para `gerador-de-criativo-video`.** Aquela skill parte de uma imagem base e transforma em movimento; esta produz a imagem que fica parada.

## Fase 1 — Leitura de criativo de imagem

O criativo de imagem tem duas camadas, e elas são produzidas separado: a **base visual** (que o gerador faz) e a **camada de edição** (texto, botão, anotação — que entra depois, no Canva ou no editor). Leia as duas.

### A aba de formatos — três eixos independentes

Formato não é uma lista. São **três eixos que se combinam**, e é o cruzamento deles que gera variedade. Classifique cada referência nos três, e monte peças novas trocando **um eixo por vez**.

#### Eixo 1 — Estrutura (o layout do quadro)

| Estrutura | Como é |
|---|---|
| Manchete sobre cena | Bloco de texto no terço superior, imagem embaixo |
| UI falsa | Bolha de mensagem, comentário, DM, notificação, card de nota |
| Diagrama anotado | Setas e rótulos apontando partes da imagem |
| Comparação | Dois painéis com rótulo: antes e depois, com e sem, A e B |
| Print de tela | Simula matéria, post, resultado de busca, conversa |
| Objeto isolado | Ingredientes ou produto arrumados sobre superfície |
| Tipografia pura | Só texto, sem imagem nenhuma. Fundo liso ou textura |
| Lista numerada | 3 a 5 itens numerados dentro do quadro |
| Mockup | Produto em contexto de uso, embalagem, tela de app |
| Nativo de plataforma | Imita post, story, enquete, resultado de quiz |
| Elemento estranho em moldura conhecida | Objeto inesperado dentro de um contexto familiar e banal |

#### Eixo 2 — Estilo visual (o tratamento)

| Estilo | Como é | Onde ganha |
|---|---|---|
| Foto de celular crua | Luz irregular, enquadramento torto, sem produção | Fura cegueira de anúncio |
| Foto produzida | Luz montada, composição limpa | Ticket alto, produto físico |
| Ilustração 2D | Desenho, traço, vetor | Nicho onde foto não convence ou não existe |
| Render 3D | Objeto ou cena renderizada | Mecanismo interno, produto, anatomia |
| Cartoon | Traço caricato, mascote | Público jovem, tema leve |
| Arte estilizada | Surreal, místico, fantasia, onírico | Nicho de crença, espiritualidade, transformação |
| Vintage | Gravura, prancha anatômica, jornal antigo, manual | Empresta autoridade de "conhecimento antigo" |
| Colagem | Recorte, sobreposição, textura de papel | Quebra de padrão pura |
| Infográfico | Vetorial, ícone, esquema, seta | Explicar mecanismo sem foto |
| Captura real | Print de tela de verdade, sem simulação | Prova |
| Alto contraste | Neon, saturado, cor chapada | Parar o dedo na força bruta |

#### Eixo 3 — Movimento

| Movimento | O que é | Produz como |
|---|---|---|
| Estático | Imagem parada | Prompt de imagem |
| Animação leve | Um elemento se move, o resto parado. Loop curto | Imagem + prompt de animação |
| Tipografia cinética | Texto entrando, saindo, escalando | Motion, sem gerador de vídeo |
| Slideshow | Sequência de imagens com texto, sem fala | Vários prompts de imagem + ordem |
| Vídeo sem pessoa | B-roll, mãos, objeto, com legenda | Prompt de vídeo plano a plano |
| Vídeo com pessoa | Alguém falando em cena | Prompt de vídeo ou briefing de gravação |

Esta skill produz **apenas o nível estático**. Os cinco níveis com movimento são a `gerador-de-criativo-video`, e todos eles começam por uma imagem base — que é justamente o que esta skill entrega. Gere a imagem aqui, mande para lá para virar movimento.

Os níveis intermediários quase não são explorados no BR e custam uma fração do vídeo com pessoa falando. **Se a sua leva inteira caiu nos dois últimos, você não minerou formato — você minerou o que é mais fácil de achar.**

#### A matriz

`Estrutura × Estilo × Movimento` dá centenas de combinações a partir de poucas referências. Um mesmo ângulo validado vira dez peças diferentes só trocando um eixo.

Exemplo do movimento: manchete sobre cena em foto crua estática é o que todo mundo faz. Manchete sobre cena em **vintage** estático já é leilão diferente. Diagrama anotado em **infográfico** com **animação leve** é outro leilão ainda.

### O que ler na base visual

Sujeito, figurino, cenário, enquadramento, luz, paleta, props, tratamento — a mesma grade de sempre. Mais duas coisas que só existem em imagem:

- **Onde a imagem cede espaço.** Todo criativo de imagem reserva área para o texto. Anote qual terço fica limpo, e se o fundo ali é liso ou escurecido de propósito.
- **O que se lê em miniatura.** Reduza a imagem ao tamanho real no feed. Se o elemento principal some, a base está errada, por mais bonita que seja.

### O que ler no ad text

Puxe o texto primário de cada anúncio do grupo A e registre:

- **Hook:** as primeiras linhas, separadas do resto
- **Estrutura do hook:** a fórmula por trás dele
- **Micro-persona que ele nomeia:** quem o texto está chamando
- **Body:** mecanismo, prova e transição para a página
- **Comprimento em caracteres**
- **Onde ele pede o clique** e com que verbo

A mediana de comprimento e as estruturas de hook mais repetidas são o que você reaproveita.

### O que ler na camada de edição

- **Bloco de texto:** posição, quantas linhas, proporção do quadro que ocupa, caixa alta ou não.
- **Destaque de palavra:** quais palavras ganham cor, fundo colorido ou tarja. É quase sempre o número, o ingrediente ou a promessa.
- **Botão falso:** existe? Cor, formato, texto, seta. Botão desenhado não é botão, é convite visual — e é convenção quase universal em criativo de imagem de resposta direta.
- **Anotação:** setas, rótulos, círculos, linhas ligando texto a parte da imagem.
- **Hierarquia de leitura:** em que ordem o olho passa. Numere: primeiro, segundo, terceiro elemento.

Marque cada campo como `observado` ou `inferido`. O prompt só usa observado.

## A inteligência do criativo de imagem — os 10 princípios

A aba de formatos diz **o que existe**. Estes princípios dizem **por que funciona**, e é com eles que você cria formato novo em vez de copiar os que já viu.

**1. A imagem carrega o MECANISMO, não a promessa.** Teste: tire a imagem e veja se o argumento sobrevive. Se sobreviver, a imagem era decoração e o criativo é fraco. Malha de pontos sobre um rosto mostra a tecnologia funcionando; rótulos anatômicos mostram o processo interno; objetos sobre a mesa mostram a receita. O texto promete, a imagem prova.

**2. A moldura empresta autoridade de uma categoria que não é publicidade.** Prancha anatômica lê como livro didático. Card branco arredondado lê como mensagem encaminhada por alguém. Malha de leitura facial lê como software. Nenhum deles parece anúncio porque nenhum usa a linguagem visual de anúncio.

**3. O botão falso pede informação, não compra.** "Ver a receita", "Começar meu teste", "Ver o resultado". Nunca "comprar" nem "saiba mais". O custo psicológico do clique despenca quando o que se promete é a resposta, não o produto.

**4. A anotação transforma imagem em argumento.** Rótulo com linha de chamada apontando parte da imagem é um micro-gancho cada. Sete rótulos são sete chances de a pessoa se reconhecer. É o jeito mais barato de aumentar densidade de mensagem sem aumentar texto corrido.

**5. Densidade de dor maior que densidade de resultado.** Em comparação, o lado do problema costuma ter mais rótulos que o lado do resultado. A pessoa precisa se reconhecer antes de desejar.

**6. Especificidade concreta em pelo menos um ponto.** Um número, um tempo, uma medida, uma idade. "Uma selfie, dez segundos" vale mais que "rápido e fácil". O número não precisa ser o principal — precisa existir.

**7. Autoridade inesperada vence autoridade credenciada.** Um pescador de 84 anos convence mais que um especialista genérico, porque credencial soa a anúncio e personagem improvável soa a história real. Escolha quem ninguém esperaria saber aquilo.

**8. O objeto em cena é a lista de ingredientes.** Quando o produto é protocolo ou receita, os objetos sobre a superfície entregam o método sem uma linha de texto. A pessoa monta o passo a passo com os olhos.

**9. Nada de cara de anúncio.** Sem logo, sem produto como herói, sem linguagem de promoção, sem selo. O criativo de imagem que funciona parece qualquer coisa menos peça publicitária.

**10. Legibilidade em miniatura antes de qualquer estética.** Se em tamanho de feed a manchete não se lê e o elemento principal some, o resto não importa.

## A camada de interrupção — o hook visual

Os dez princípios acima constroem o argumento. Eles não param o dedo. **Argumento é o que segura depois; hook visual é o que faz parar antes.** São coisas separadas e se testam separadas.

O hook visual age em menos de um segundo, em miniatura, antes de qualquer leitura. Se a peça depende de a pessoa ler para parar, ela já perdeu.

### Os 11 recursos de interrupção

| Recurso | Como se constrói | Por que para o dedo |
|---|---|---|
| **Elemento fora de contexto** | Objeto num lugar onde ele não deveria estar | O cérebro trava no que não bate com o esperado |
| **Olhar direto na câmera** | Sujeito encarando quem vê | Rosto encarando é prioridade de processamento |
| **Olhar como seta** | Sujeito olhando para o texto ou para o objeto | Quem vê segue a direção do olhar sem perceber |
| **Escala impossível** | Objeto muito maior ou menor do que deveria | Incoerência de tamanho é lida antes do conteúdo |
| **Corte parcial** | Elemento cortado pela borda do quadro | Incompletude gera vontade de completar |
| **Ocultação** | Borrão, tarja, mão cobrindo, objeto na frente | O que está escondido é o que se quer ver |
| **Anotação vermelha** | Círculo, seta ou traço marcando um ponto | Marca de correção diz "olha aqui" sem palavra |
| **Padrão quebrado** | Repetição com um elemento diferente | O diferente salta antes de a repetição ser contada |
| **Cor que não existe no feed** | Fundo ou elemento em cor pouco usada no nicho | O feed é previsível; a exceção aparece |
| **Movimento congelado** | Algo no meio da queda, do respingo, da ação | Ação parada implica o que veio antes e depois |
| **Textura errada** | Superfície que não combina com o objeto | Estranhamento sem precisar de explicação |

### Como escolher

Comece pelo mecanismo do gancho, não pelo visual. Se o clickbait minerado usa choque, vá em elemento fora de contexto ou escala impossível. Se usa lacuna de informação, vá em ocultação ou corte parcial. Se usa especificidade, vá em anotação. O visual é a execução de um mecanismo, não uma ideia solta.

### Regras que decidem

- **Um recurso por peça.** Dois competem e a imagem vira poluída.
- **O hook visual não pode depender do texto.** Cubra o texto com a mão: a imagem ainda para o dedo? Se não, você tem uma boa manchete e nenhum hook.
- **Ele é variável independente.** Dez hooks visuais com o mesmo texto, depois dez textos com o hook vencedor. Nunca os dois de uma vez.
- **Teste em miniatura, sempre.** Reduza ao tamanho real do feed. O que não sobrevive ali não existe.
- **O hook órfão é legítimo.** Visual sem relação com a oferta que mesmo assim para o scroll funciona, mas escala mal: ele passa o portão de interromper e falha o de identificar. Use como exploração, nunca como base.

### No prompt

O recurso de interrupção entra na Parte 1, junto da base visual, e é a **primeira** coisa descrita — antes de sujeito, cenário e luz. O gerador dá mais peso ao que vem primeiro.

## Motor 1 — a moldura emprestada (é daqui que sai formato novo)

Escolha uma linguagem visual que o seu público **já confia**, de uma categoria que não é publicidade, e renderize o argumento dentro das convenções dela. Este é o gerador de formato inédito, e ele não se esgota:

**Documento e registro:** prancha anatômica, página de livro antigo, ficha de biblioteca, laudo, prontuário, bula, manual de instruções, diagrama de patente, mapa, planta baixa, telegrama, carta manuscrita, recibo, etiqueta, tabela nutricional, calendário, agenda, quadro de avisos.

**Tela e interface:** resultado de busca, notificação, conversa, resultado de quiz, tela de app, extrato, planilha, painel de métricas, player de vídeo, comentário, avaliação de produto.

**Mídia e cultura:** manchete de jornal, capa de revista, cartaz antigo, quadro de HQ, storyboard, legenda de documentário, ficha técnica, cardápio, embalagem de produto.

**Objeto do cotidiano:** post-it, bilhete de geladeira, caderno de receita da avó, lista de compras, foto de álbum antigo, envelope, ingresso.

**Onde garimpar a moldura visual, fora da biblioteca:** bancos de imagem de interesse (tipo Pinterest) pesquisando pelo objeto ou pela categoria, capas de jornal antigo, manuais e catálogos escaneados. Você não copia a imagem — pega a **linguagem** dela e descreve no prompt.

Como usar: determine qual dessas linguagens o público **reconhece e respeita**, pelo que aparece nos criativos escalados e pela faixa etária dominante, e monte a mensagem dentro dela. Público mais velho responde a documento e registro. Público jovem responde a tela e interface. Nicho de crença responde a objeto simbólico e arte estilizada.

Regra: **a moldura tem que ser respeitada até o detalhe.** Prancha anatômica com fonte moderna quebra a ilusão. Card de mensagem com tipografia de anúncio quebra a ilusão. Se você vai emprestar a linguagem, empresta inteira.

## Motor 2 — como tornar visível um mecanismo invisível

A maioria dos mecanismos de resposta direta não se vê: fluido retido, absorção, hormônio, algoritmo, compatibilidade, envelhecimento. O criativo forte resolve isso. As saídas possíveis:

| Recurso | Como é | Serve para |
|---|---|---|
| Sobreposição gráfica | Malha, grade, marcação sobre foto real | Mostrar tecnologia ou análise agindo |
| Corte transversal | Vista interna desenhada | Órgão, camada, interior de objeto |
| Seta de fluxo | Setas indicando movimento | Circulação, drenagem, processo |
| Comparação de escala | Dois objetos lado a lado | Quantidade, tamanho, dose |
| Sequência de 3 quadros | Antes, durante, depois | Processo que leva tempo |
| Objeto substituto | Algo concreto representando o abstrato | Quando não há como mostrar o real |
| Mapa de calor | Zonas coloridas por intensidade | Onde dói, onde acumula |
| Linha do tempo | Marcos ao longo de um eixo | Progressão, idade, estágio |
| Rótulo com chamada | Texto ligado por linha ao ponto | Nomear o que a pessoa sente |

Antes de escrever o prompt, responda: **qual desses recursos torna o meu mecanismo visível?** Se nenhum servir, o criativo vai depender só de texto — e aí vale mais ir de tipografia pura do que de foto genérica.

## A régua do botão falso

- O verbo promete **informação**, não transação: ver, descobrir, conferir, começar, tocar.
- O objeto do verbo é o **próximo passo**, não o produto: "ver a receita", não "ver o produto".
- Cor sólida e alto contraste contra o fundo. Verde e coral funcionam porque não são cor de anúncio.
- Formato de pílula ou retângulo arredondado, largura de 50% a 80% do quadro, na base.
- Seta ou sinal de continuação logo abaixo aumenta o toque sem custo nenhum.
- Um botão por peça. Dois competem e nenhum vence.

## Por que imagem, agora

Vale saber para escolher o eixo de movimento com intenção, e para explicar a decisão a quem for produzir.

A duração do conteúdo que o público consome vem caindo em escada: vídeo de uma hora, depois dez minutos, depois um minuto, depois dez segundos. Abaixo de dez segundos não é mais vídeo — vira gif. E abaixo do gif, imagem.

Duas consequências práticas:

- **Imagem e gif quebram padrão num feed feito de vídeo curto.** O que interrompe é o que destoa, e hoje o que destoa é o que não se move.
- **Biblioteca com milhares de anúncios em imagem é sinal de onda, não de nicho pobre.** Quando você abrir o Raio-X e vir um anunciante com volume grande de estático, é aí que a fatia está se abrindo.

O gif fica entre os dois: produz-se pela `gerador-de-criativo-video` no nível de animação leve, partindo de uma imagem base gerada aqui.

## O ad text — o texto do anúncio é o que segmenta

Esta é a metade que quase todo mundo trata como legenda. Ela não é legenda. **É o que a plataforma lê para decidir a quem entregar.**

### Por que ele pesa mais em imagem do que em vídeo

Em vídeo, a plataforma precisa transcrever a fala para entender do que se trata. Transcrição erra, e erro de transcrição vira erro de entrega — o criativo vai para o público errado e você culpa a oferta.

Em imagem não existe o que transcrever. **Você entrega o texto pronto.** Sem intermediário e sem ruído entre o que você quis dizer e o que a plataforma entendeu.

É a vantagem estrutural do criativo de imagem, e quase ninguém no BR usa de propósito.

*(Trate como modelo mental do que explica o que se vê escalar, não como documentação oficial. Não afirme como funcionamento declarado da plataforma.)*

### A anatomia: hook e body

O ad text tem as mesmas duas peças de um criativo.

**Hook — as primeiras linhas.** Duas funções ao mesmo tempo: prender quem lê **e dizer pra quem aquilo é**. É o hook que segmenta.

**Body — o resto.** Aquece, entrega o mecanismo e manda para a página.

Ao ler os ad texts do grupo A, separe hook de body e destrinche a estrutura do hook. Elas se repetem. Exemplos de estruturas que aparecem muito:

- `inimigo nomeado + tempo específico + resultado`
- `descoberta + fonte inesperada + o que ela revela`
- `negação do óbvio + o que é de verdade + como funciona`
- `situação cotidiana + o que ninguém percebe nela`

Catalogue as que aparecerem, com a incidência, do mesmo jeito que faz com formato.

### O ad text é onde o micro-público se testa

Este é o uso que muda operação, e ele conecta direto com o Mapa de Fatias.

Mesma oferta. Mesmo entregável. **Mesma imagem.** Só o texto muda — um ad text por micro-persona, escrito com a dor específica do dia a dia dela.

Uma oferta de emagrecimento vira: mulher que engordou depois da gravidez, mulher que emagrece e recupera tudo, mulher que só quer voltar a caber na roupa antiga. Mesma promessa central, três conversas diferentes.

**É o teste de público mais barato que existe**, porque você não produz nada novo. E é por isso que criativo de imagem acha micro-público mais rápido que vídeo: em vídeo você teria que regravar.

### A régua do teste

**Divida o ticket por dez.** Esse é o gasto por ad text antes de matar.

Ticket de R$100 → dez ad texts, R$10 de teste em cada. O corte fica próximo do meio ticket ou da margem líquida do front, que é a mesma régua do resto do pack.

### Depois que um valida

Micro-público que vendeu deixa de ser teste e vira base. Duas consequências:

- Escreva mais ad texts **para aquele mesmo micro-público**, com ângulos diferentes.
- A lead e a página passam a falar com ele. Ad text validado numa micro-persona e página falando com outra é o vazamento que a cascata do CTA já descreve.

### O comprimento

A copy que antes ia dentro do vídeo passa a ir no ad text. Texto longo é a norma entre os escalados de imagem, não a exceção.

Não chute: **conte o comprimento dos ad texts do grupo A e use a mediana.** Registre em caracteres. Se a mediana do nicho é 900 caracteres, um ad text de 200 está fora do padrão do que funciona ali.

### Vale para vídeo também

Criativo em vídeo também tem ad text, e a mesma disciplina se aplica: hook que nomeia a micro-persona, body que aquece, comprimento na mediana do nicho. A diferença é que em vídeo o ad text **reforça** a segmentação que a transcrição já faz; em imagem ele **é** a segmentação.

Se a peça for de vídeo, escreva o ad text pela mesma régua e entregue junto — a `gerador-de-criativo-video` referencia esta seção.

### Onde ele entra

O ad text **não vai para o gerador de imagem**. Ele é campo separado no gerenciador, colado na hora de subir o anúncio. Assim como a camada de edição, é a parte que não se gera.

## Fase 2 — A matriz de geração

Antes de escrever prompt nenhum, monte a matriz:

1. **Escolha a base validada.** O criativo com maior longevidade dentro da fatia alvo. Ele é o controle.
2. **Trave o que não muda.** Ângulo, micro-persona e estrutura de mensagem ficam iguais, salvo se a variável do teste for justamente uma delas.
3. **Escolha a variável por peça.** Uma só: recurso de interrupção, sujeito, figurino, cenário, enquadramento, luz, props, texto na tela, moldura ou estilo.
   O **recurso de interrupção** é a variável de maior impacto e a mais barata de trocar. Comece por ela.
4. **Aplique 70/30.** Setenta por cento das peças variam algo de baixo risco (figurino, cenário, props). Trinta por cento testam algo estrutural (tratamento, sujeito, hook visual).
5. **Priorize variável de índice neutro.** Se o benchmark mostrou que uma variável aparece igual em quem escalou e em quem morreu, ela é convenção do nicho — mexer nela custa pouco e pode revelar fatia.

## Fase 3 — O prompt, em duas partes

Sempre em **duas partes**. Prompt de imagem que tenta resolver tudo num bloco só produz aquela foto genérica que não vende.

### Parte 1 — a base visual (vai pro gerador)

```
[TIPO: fotografia de celular | ilustração | diagrama | print de tela] ·
[SUJEITO com idade aparente, expressão, papel] · [FIGURINO] ·
[AÇÃO ou pose] · [PROPS em cena, descritos com precisão] ·
[CENÁRIO com detalhe de fundo] · [ENQUADRAMENTO e altura de câmera] ·
[LUZ: fonte, dureza, direção] · [PALETA e contraste] ·
[ESPAÇO LIVRE: qual terço fica limpo para o texto entrar depois] ·
[TRATAMENTO desejado] · [PROPORÇÃO]

Negative: texto, letras, marca d'água, mãos deformadas,
estética de banco de imagem, pessoa famosa
```

A linha do **espaço livre** é a que separa prompt de imagem de prompt de foto. Sem ela o gerador enche o quadro e o texto não tem onde entrar.

### Parte 2 — a camada de edição (não vai pro gerador)

```
Sub-formato: [manchete sobre cena | UI falsa | diagrama | comparação | print | objeto]
Bloco de texto: [as linhas exatas, com quebra marcada]
  Posição: [terço superior | inferior | dentro do card]
  Proporção: [% do quadro]
  Estilo: [caixa alta, peso, cor]
Destaque: [quais palavras ganham cor ou fundo, e qual cor]
Botão falso: [texto, cor, formato, seta] ou "não tem"
Anotação: [setas e rótulos, ligando o quê ao quê] ou "não tem"
Hierarquia de leitura: 1º [x] · 2º [y] · 3º [z]
Ferramenta sugerida: [Canva | editor de imagem]
```

**Nunca peça texto ao gerador.** Ele erra letra, e o texto é justamente o elemento que carrega o criativo de imagem. A camada de edição é sempre humana ou de editor de imagem.

## Linha vermelha (não negociável)

- **Nunca gere semelhança de pessoa real.** Nem celebridade, nem o apresentador do concorrente, nem "uma mulher parecida com [nome]". Descreva um perfil, nunca uma pessoa.
- **Nunca reproduza a arte do concorrente.** A captura é referência interna. O que você entrega é uma cena nova que usa o mesmo mecanismo visual.
- **Pessoa gerada por IA não pode ser apresentada como cliente ou como profissional real.** Depoimento com rosto sintético e especialista inventado com credencial são publicidade enganosa, e é o erro que derruba conta e gera notificação. Se a peça precisa de depoimento, o briefing vai para gravação com pessoa real.
- **O prompt herda a alegação.** Se o ângulo de origem estiver marcado `linha_vermelha`, a peça não é gerada. Registre o mecanismo e siga.
- Em nicho sensível, o prompt não pode conter promessa de cura, garantia de resultado financeiro nem antes e depois corporal.

## Formato exato da saída — siga isto sempre

O entregável é **um arquivo markdown** em `geracao/imagem-[nicho]-[data].md`.

A unidade é o **criativo**. E o documento é organizado **por ferramenta**: primeiro todos os prompts para o gerador, depois todas as camadas de edição. A pessoa abre o gerador uma vez, gera tudo, e só então vai para o editor.

````
# Leva de imagem — [nicho] — [data]

## O que você recebeu
- **[N] criativos** · [X] contenção · [Y] exploração
- **Base validada:** [código] — [uma linha]
- **Amostra:** [N] anunciantes distintos, [N] controles lidos
- **Assumido:** [derivações, em uma linha]

## Como usar
Parte 1: gere as [N] imagens no gerador. Parte 2: monte a camada de edição e copie o ad text de cada uma.
O ad text vai no campo de texto do anúncio no gerenciador — não entra na imagem.
⚠️ O texto **não** entra no gerador. Ele entra na parte 2.

### Mapa da leva

| Criativo | Micro-persona | Testa | Estrutura · Estilo | Interrupção |
|---|---|---|---|---|
| C01 | [MP-0X] | [variável] | [x] · [y] | [recurso] |
| C02 | [MP-0Y] | [variável] | [x] · [y] | [recurso] |

**Teste de micro-público:** [N] destes criativos usam a MESMA imagem e mudam só o ad text.
Gasto por ad text antes de matar: **[ticket ÷ 10]**

═══════════════════════════════════════════════

# PARTE 1 — Gere estas [N] imagens

Abra o gerador de imagem. Gere todas antes de ir para a parte 2.

## C01

```
[prompt da base visual]
```
**Negative:** `[lista]` · **Proporção:** [9:16]
**Salve como:** `C01.png`

## C02

```
[prompt]
```
**Negative:** `[lista]` · **Proporção:** [9:16]
**Salve como:** `C02.png`

[continue até a última]

**Antes de seguir, confira:** nenhuma veio com texto? o terço reservado ficou livre? legível em miniatura?

═══════════════════════════════════════════════

# PARTE 2 — Monte a camada de edição

Abra o editor. Para cada imagem, monte conforme a tabela.

## C01 · sobre `C01.png`

**Testa:** [variável] | **Hipótese:** [o que responde]
**Micro-persona:** [MP-0X] — [nome]

| Elemento | O que fazer |
|---|---|
| Bloco de texto | [linhas exatas, com a quebra marcada] |
| Posição | [terço, proporção do quadro] |
| Destaque | [palavras e cor] |
| Botão falso | [texto, cor, formato] ou "não tem" |
| Anotação | [setas e rótulos] ou "não tem" |
| Ordem de leitura | 1º [x] → 2º [y] → 3º [z] |

**Exporte como:** `C01-final.png`

### Ad text do C01

**Micro-persona:** [MP-0X] · **Estrutura do hook:** [fórmula] · **[N] caracteres**

```
[hook — as primeiras linhas]

[body — mecanismo, prova, transição]

[a linha que pede o clique]
```

## C02 · sobre `C02.png`

[mesma estrutura: tabela de edição + ad text]

═══════════════════════════════════════════════

## Checagem antes de subir
- [ ] Legível em miniatura
- [ ] Hook visual sobrevive com o texto coberto
- [ ] Nenhum texto veio do gerador
- [ ] Arquivo nomeado com o código

## Referências usadas
| Criativo | Anunciante | Link do anúncio | Biblioteca | Funil |
|---|---|---|---|---|
````

### As regras do documento

- **Organizado por ferramenta, não por criativo.** Parte 1 esgota o gerador, parte 2 esgota o editor.
- **O mapa da leva abre o documento**, para a pessoa ver o que cada criativo testa antes de gerar.
- **Nomenclatura fixa:** `C[nn].png` na geração, `C[nn]-final.png` na exportação.
- **Nada de prompt no chat.** No chat vão só três linhas: amostra, o que saiu, onde está.

### O índice estruturado

Além do markdown, salve `geracao/leva.json`:

```json
[
  {
    "id": "GEN-001",
    "base_validada": "CRI-004",
    "oferta_aprovada": {
      "escalando": true, "executavel": true,
      "densidade_do_angulo": "rala | disputada | lotada",
      "entregavel": "digital | fisico | servico",
      "depende_de_autoridade": false,
      "tem_escada_de_precos": true,
      "motivo_se_reprovada": ""
    },
    "variavel_isolada": "cenario",
    "hipotese": "o que este teste responde se performar",
    "papel": "contencao | exploracao",
    "micro_persona_id": "MP-003",
    "angulo_id": "ANG-007",
    "familia_angulo": "problema | solucao | crenca | identificacao",
    "tipo": "imagem",
    "estrutura": "manchete_sobre_cena | ui_falsa | diagrama | comparacao | print_de_tela | objeto_isolado | tipografia_pura | lista_numerada | mockup | nativo_plataforma",
    "estilo_visual": "foto_crua | foto_produzida | ilustracao_2d | render_3d | cartoon | arte_estilizada | vintage | colagem | infografico | captura_real | alto_contraste",
    "movimento": "estatico",
    "eixo_trocado": "estrutura | estilo | movimento | nenhum",
    "hook_visual": {
      "recurso_interrupcao": "elemento_fora_de_contexto | olhar_direto | olhar_como_seta | escala_impossivel | corte_parcial | ocultacao | anotacao_vermelha | padrao_quebrado | cor_incomum | movimento_congelado | textura_errada",
      "mecanismo_do_gancho": "choque | open_loop | negatividade | especificidade | inimigo_comum | autoridade",
      "herdado_de": "CB-00X ou null",
      "sobrevive_sem_texto": true,
      "legivel_em_miniatura": true
    },
    "leitura_de_cena": {
      "sujeito": "", "figurino": "", "cenario": "", "enquadramento": "",
      "luz": "", "paleta": "", "props": [""], "texto_na_tela": "",
      "tratamento": "", "anotacao": "",
      "campos_inferidos": ["lista do que NÃO foi observado"]
    },
    "prompt_base_en": "",
    "prompt_base_pt": "",
    "negative": "",
    "proporcao": "9:16 | 4:5 | 1:1",
    "micro_persona_id": "MP-001",
    "ad_text": {
      "hook": "",
      "estrutura_hook": "inimigo+tempo+resultado | descoberta+fonte | negacao+verdade | cotidiano+revelacao | outra",
      "body": "",
      "pedido_de_clique": "",
      "caracteres": 0,
      "mediana_do_nicho": 0,
      "testa_micro_publico": true,
      "compartilha_imagem_com": ["C02", "C03"]
    },
    "camada_edicao": {
      "bloco_texto": "", "posicao": "", "proporcao_do_quadro": "",
      "destaque": "", "botao_falso": "", "anotacao": "",
      "hierarquia_leitura": ["", "", ""]
    },
    "custo_producao": "baixo | medio | alto",
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

- A oferta passou pelos filtros 1 e 2 antes de qualquer captura?
- Está registrado por que ela foi aprovada, e não só que foi?
- A coleta foi feita em duas passadas separadas, com o filtro de tipo de mídia da biblioteca?
- As cotas fecharam: 60% estático ou animado, nenhuma estrutura acima de 30%, 3+ estilos, tentativa em cada nível de movimento?
- Cada referência foi classificada nos TRÊS eixos, e não só num deles?
- A leva troca um eixo por vez, e não caiu inteira em foto crua com pessoa falando?
- Os arquivos estão em `estaticos/` e `frames/`, e nenhum frame foi usado como referência de imagem?
- A contagem da amostra está declarada por trilha, e não somada?
- Nenhum frame de vídeo foi usado como referência?
- Todo prompt de imagem tem as DUAS partes: base visual e camada de edição?
- O prompt de base reserva o espaço livre onde o texto vai entrar?
- Cada peça tem UM recurso de interrupção declarado, e só um?
- O hook visual sobrevive com o texto coberto?
- Quando existia `clickbait.json`, o hook foi herdado em vez de inventado?
- A imagem carrega o mecanismo, e o argumento quebra se ela for removida?
- A peça empresta a linguagem visual de uma categoria que não é publicidade, e respeita ela até o detalhe?
- O botão falso promete informação e não compra?
- Existe pelo menos um dado concreto na peça — número, tempo ou medida?
- Foi escolhido um recurso do Motor 2 para tornar o mecanismo visível?
- A cadeia rodou inteira sem parar pedindo aprovação no meio?
- A saída é arquivo salvo com caminho informado, e não prompt colado no chat?
- O markdown está em duas partes, com a parte 1 esgotando o gerador antes da parte 2?
- O ad text está junto da camada de edição, e fora do prompt do gerador?
- O mapa da leva abre o documento?
- Toda peça tem código, e o código é o nome do arquivo em todas as etapas?
- Cada peça tem uma base validada declarada, e não foi inventada do zero?
- Está registrado quantos frames foram lidos, em que tempos e de que fonte?
- Vídeo foi lido por frames extraídos, e não por screenshot de vídeo rodando?
- Uma variável isolada por peça, com a hipótese escrita?
- A leitura de cena separa observado de inferido, e o prompt só usa observado?
- Os prompts de imagem pedem imperfeição em vez de estética de banco de imagem?
- Nenhum prompt pede texto dentro da imagem?
- Proporção e negative prompt em todas as peças de imagem?
- Nenhuma semelhança de pessoa real, nenhuma credencial inventada, nenhum depoimento sintético?
- Peça vinda de ângulo radioativo foi barrada em vez de gerada?
- 70/30 respeitado, com a exploração indo em variáveis de índice neutro?
- Links de origem em toda peça e escrita no Banco de Fatias?