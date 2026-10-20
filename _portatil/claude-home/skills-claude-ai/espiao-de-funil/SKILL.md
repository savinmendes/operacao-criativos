---
name: espiao-de-funil
description: "Reconstrói a operação inteira de UM concorrente: anúncio, página, escada de preços, checkout, e-mail/SMS, remarketing, cadência e estimativa de faturamento, terminando nas lacunas da operação. Use para espionar ou fazer engenharia reversa de um concorrente."
---

# Espão de Funil

O Raio-X do Leilão te diz quem está no jogo. Esta skill escolhe um alvo e reconstrói a máquina dele inteira, incluindo as partes que não aparecem na biblioteca de anúncios: o que acontece depois do clique, depois do checkout e depois do e-mail.

O output não é um JSON pra alimentar esteira. É um **dossê**: a operação de um concorrente real, camada por camada, com as lacunas dele marcadas no fim. As lacunas são o produto final, porque é onde a sua entrada existe.

## Autonomia — execute, não pergunte

Roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

- **Não pergunte o que a coleta responde.** Disse o nicho? Abra a biblioteca e olhe. Decida amostra, alvo e prioridade pelos critérios deste arquivo e informe o que decidiu.
- **Só pare quando** faltar login, permissão de pasta, ou quando a escolha mudar o resultado e houver duas leituras igualmente defensáveis.
- **Execute a cadeia inteira sem pedir aprovação no meio.** Narre em uma linha por etapa enquanto faz.
- **Leia os JSONs do banco antes de começar.** Não refaça trabalho que já existe.
- **Entregue arquivo salvo com o caminho informado**, não texto no chat.
- **Ao terminar, diga três coisas:** o tamanho da amostra, o que saiu, e onde está.
- Percorra as sete camadas até onde der. Camada que travou se declara com o motivo, não vira pergunta.

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

- **Obrigatório:** o alvo. Nome do anunciante, link de anúncio ou URL da página de vendas.
- **Útil:** o `benchmark.json` do nicho, se já rodou o Raio-X. Ele te dá a classificação do alvo (dominante, desafiante, testador) e as micro-personas do mercado, e você já sabe quais delas o alvo ataca e quais deixou órfãs.
- Se o usuário não disse quem é o alvo mas descreveu o nicho, rode ou peça o Raio-X primeiro. Espionar sem saber a posição do alvo no leilão gera dossê bonito e inútil.

## Linha vermelha (leia antes de coletar)

A diferença entre pesquisa de concorrência e problema jurídico é nítida, e a skill fica do lado certo:

**Pode:**
- Ler, catalogar e destrinchar qualquer coisa que o concorrente serve publicamente: anúncios, páginas, checkout, preços, e-mails que ele manda para quem entra na lista, anúncios de remarketing que ele exibe.
- Entrar na lista com um e-mail secundário. Isso é ser um visitante como qualquer outro, e a sequência que chega é exatamente a que qualquer lead recebe.
- Comprar o produto como pesquisa. É compra legítima e você vira cliente com os mesmos direitos.
- Extrair estrutura, mecanismo, ângulo, escada de preços, sequência lógica. **Ideia não tem dono.**

**Não pode, e a skill não faz:**
- Copiar copy literal, arte, criativo, PDF ou nome de produto. Isso tem dono e gera notificação.
- Redistribuir, revender ou entregar como seu o produto comprado.
- Acessar qualquer coisa atrás de login que não seja seu, tentar credencial, explorar falha, ou usar ferramenta que burle proteção.
- Criar identidade falsa além de um e-mail secundário: nada de documento, CNPJ inventado ou fraude de cadastro.
- Reproduzir depoimento, número ou prova do concorrente como se fosse seu.

Se o alvo escala com fraude em nicho sensível (cura, garantia financeira, prova fabricada), registre o mecanismo e **marque a operação como radioativa**: aquilo cai, e quem modelou cai junto. Documente como aviso, não como playbook.

No dossê, sempre separe **o que é dele** (citado como referência, resumido, nunca reproduzido) de **o que você pode modelar** (estrutura e lógica).

## Capacidade e limite

- **Não existe número real de faturamento acessível.** Tudo é estimativa por faixa. Ver a seção de estimativa e nunca entregar número seco.
- **A Ad Library não mostra gasto** fora de anúncios políticos na maioria dos países.
- **"Ativo desde" pode resetar** com edição. Trate longevidade como sinal, não prova.
- **Contagem de anúncios infla** com dynamic creative, posicionamento e idioma. Estime criativos únicos.
- **O Claude não assiste vídeo.** VSL sai da transcrição + frames. Se o alvo roda VSL longa, peça a transcrição ou capture frames em intervalos.
- **A sequência de e-mail leva dias pra completar.** Registre o que chegou e diga que a captura está aberta, com data de reabertura do dossê.

## As 7 camadas

Colete nesta ordem. Cada camada explica a seguinte.

### 1. Camada de aquisição
Todos os anúncios ativos do alvo na Ad Library. Por criativo: data ativo desde, formato, ângulo, avatar, micro-persona alvo, gancho dos primeiros 3 segundos, país e idioma. Estime criativos únicos.
Depois, o padrão: quantos criativos simultâneos ele sustenta, qual o mais antigo (é o controle dele), quantos ele trocou nos últimos 30 dias.

### 2. Camada de página
A página de destino destrinchada no schema: `HOOK → TENSÃO → DESEJO → CRENÇA → MECANISMO → PROVA → OBJEÇÃO → OFERTA → CTA`.
Registre também: TSL ou VSL, comprimento, nível de consciência que ela assume, tipo de prova (depoimento, autoridade, demonstração, número), garantia, e o que ela **não** tem.

## Mapeamento de domínio — como achar as páginas que ele não linka

A camada de página não é só a de vendas. Um funil de resposta direta tem upsell, downsell, order bump, obrigado, backredirect e às vezes uma página de oferta paralela. Boa parte disso é descobrível sem comprar.

### O que dá para achar sem comprar

Rode nesta ordem. Cada passo costuma revelar o próximo.

**1. Sitemap.** `dominio.com/sitemap.xml` e `dominio.com/sitemap_index.xml`. Construtor de página gera isso por padrão e quase ninguém lembra de remover. Costuma listar o funil inteiro.

**2. Robots.txt.** `dominio.com/robots.txt`. Ironia útil: o que ele mandou o buscador não indexar é justamente o que ele não queria que fosse visto — upsell, obrigado, área de membros. O `Disallow` entrega o caminho.

**3. Busca indexada.** `site:dominio.com` no buscador. Revela o que foi indexado apesar do robots, e às vezes subdomínios que você não sabia que existiam.

**4. Arquivo histórico.** Consulte versões antigas do domínio. Página que existiu e saiu do ar aparece ali, e mostra como a escada era antes — o que diz muito sobre o que funcionou e o que ele matou.

**5. Código-fonte da página de vendas.** É a fonte mais rica e a menos usada. Procure por: URL de checkout, plataforma de pagamento, IDs de pixel, links para próximas etapas hardcoded em JavaScript, e comentários esquecidos. O checkout revela a plataforma, e a plataforma revela como o resto da escada está montado.

**6. Checkout.** O order bump aparece na própria página de checkout, sem pagar. Preço, oferta e como ele apresenta o bump: tudo visível.

**7. Backredirect.** Abra a página de vendas e acione o voltar do navegador. Se ele redireciona em vez de sair, existe backredirect — e o destino é quase sempre uma oferta de desconto ou um downsell. Registre a URL de destino.

**8. Exit pop.** Mova o cursor para o topo da viewport como quem vai fechar a aba. Capture o que aparece: costuma ser cupom, downsell ou captura de e-mail.

**9. Caminhos previsíveis.** Construtores de funil usam slugs padrão. Vale testar uma dezena: `/up1`, `/upsell`, `/oto`, `/oto1`, `/ds1`, `/downsell`, `/obrigado`, `/thank-you`, `/checkout`, `/especial`, `/back`, `/oferta-especial`.

**Limite de uso:** uma dezena de tentativas, não um varredor. Isso é pesquisa, não escaneamento. Não rode ferramenta de força bruta contra o domínio de ninguém — além de ser abusivo, gera log e pode configurar acesso não autorizado.

### O que NÃO dá sem comprar

Seja honesto no dossê sobre isso:

- **Upsell pós-compra.** A maioria só existe depois do pagamento, protegida por token de sessão. Não se acessa sem transação.
- **Downsell de recusa.** Só aparece para quem recusou o upsell.
- **Área de membros e entregável.** Precisa de conta.
- **Sequência pós-compra.** O e-mail depois da compra é diferente do e-mail de opt-in.

Quando o alvo importa de verdade, **comprar o produto é pesquisa de concorrência legítima** e resolve tudo isso. Registre o custo como investimento de mineração. O que não se faz é redistribuir o que comprou.

### Como reportar

Nunca diga "a escada é essa". Diga o que viu, por onde viu, e o que ficou fora:

> Mapeadas 7 páginas: vendas, checkout com order bump de R$27, obrigado, backredirect para downsell de R$47, e três páginas indexadas fora do funil principal. Upsell pós-compra não acessível sem transação — a escada acima de R$47 é desconhecida.

Escada incompleta declarada vale mais que escada completa inventada, porque quem lê vai usar isso pra decidir preço.

### 3. Camada de oferta
Nome, promessa central, mecanismo único, entregáveis prometidos, bônus, formato de entrega (PDF, área de membros, comunidade, físico).

### 4. Camada de monetização
A escada inteira: preço de entrada, ancoragem usada, order bump (o que é, por quanto, como é apresentado no card), upsell, downsell, recorrência. Registre também gateway e plataforma de checkout, porque isso revela porte da operação e restrição de nicho.
Calcule o **ticket médio implícito** se todos os degraus converterem numa taxa plausível, e diga a taxa que você assumiu.

### 5. Camada de retenção
Entre na lista com e-mail secundário. Por mensagem: tempo depois do opt-in, assunto, ângulo, objetivo (educar, quebrar objeção, escassez, oferta), e o que ela vende. Mesma coisa para SMS ou WhatsApp se houver.
Isso é o que quase ninguém olha, e é onde está o faturamento invisível do concorrente.

### 6. Camada de remarketing
Depois de visitar a página e abandonar, catalogue os anúncios que ele passa a te servir. Ângulo de remarketing costuma ser diferente do de aquisição, e revela a objeção principal que ele descobriu no mercado.

### 7. Camada de cadência
Junte tudo: de quantos em quantos dias ele repõe criativo, quantas variações por ângulo, quanto tempo um ângulo dura antes de sumir, se ele testa formato ou só troca gancho.
**Esta é a camada que muda a decisão de operação do usuário**, porque define a produção mínima necessária pra competir com ele.

## Estimativa de faturamento — como fazer sem mentir

Nunca entregue número seco. Entregue faixa, com o método visível e a incerteza declarada.

Triangule por três caminhos e veja se convergem:

1. **Por volume de criativo** — criativos únicos sustentados x longevidade média. Quem sustenta 40 criativos por 60 dias está gastando de forma consistente, e ninguém sustenta gasto sem retorno.
2. **Por ticket e escada** — ticket de entrada x ticket médio implícito. Define o piso de volume necessário pra bancar aquele CPM.
3. **Por sinal social** — volume e ritmo de comentários nos anúncios, avaliações na plataforma, número de alunos declarado (com desconto pela prova ser autodeclarada).

Entregue assim: faixa larga, os três caminhos, o que faria a estimativa desabar. Exemplo de formulação correta: "faixa provável de X a Y por mês, sustentada por três sinais convergentes; a estimativa cai se boa parte dos criativos for variação de posicionamento em vez de criativo único".

Se os três caminhos não convergirem, diga isso e não force um número.

## Lacunas — o produto final do dossê

Termine sempre por aqui. Para cada camada, responda: **o que ele não está fazendo?**

- Micro-personas do nicho que ele não ataca (cruze com o `benchmark.json`).
- Formatos que ele não usa.
- Degraus de escada ausentes (sem order bump? sem recorrência?).
- Objeções que a página não trata.
- Prova fraca ou ausente.
- Países e idiomas não explorados.
- Nível de consciência não coberto.

Ranqueie as lacunas por: tamanho da fatia, custo de execução e distância do que o usuário já sabe fazer. As três primeiras são a recomendação de entrada.

## Fechando o loop — as lacunas viram fatias

Um dossê que termina em PDF morre no PDF. Ao fim, converta as **três lacunas prioritárias** em entradas de fatia e grave em `banco-de-fatias.json` com `status: "a_testar"`, no mesmo contrato que o Raio-X usa:

```json
{
  "id": "FAT-###",
  "tipo": "fatia",
  "origem": "espionagem:<alvo>",
  "micro_persona_id": "MP-00X",
  "micro_persona": "",
  "angulo": "",
  "formato": "",
  "densidade": "fantasma",
  "descricao": "a lacuna virada em combinação atacável",
  "custo_producao": "baixo | medio | alto",
  "prioridade": 0,
  "status": "a_testar"
}
```

Se a lacuna for de camada que não vira criativo (escada de preços sem order bump, sequência de e-mail ausente), registre como recomendação de operação no dossê e **não** force em fatia. Fatia é combinação de persona, ângulo e formato; o resto é decisão de oferta e vai no relatório, não no banco.

Com isso, o próximo Raio-X e a próxima leva da esteira já nascem sabendo o que a espionagem descobriu.

## Saída

Salve o dossê em `espionagem/<alvo>.md` e o resumo estruturado em `espionagem/<alvo>.json`.

```json
{
  "alvo": "",
  "data_dossie": "AAAA-MM-DD",
  "classificacao": "dominante | desafiante | testador | zumbi | morto",
  "pais": [""],
  "aquisicao": {
    "criativos_unicos": 0,
    "linhas_na_biblioteca": 0,
    "criativo_mais_antigo_dias": 0,
    "trocas_ultimos_30d": 0,
    "angulos": [""],
    "formatos": [""],
    "micro_personas_atacadas": [""]
  },
  "mapa_de_paginas": [
    { "url": "", "tipo": "vendas | checkout | upsell | downsell | obrigado | backredirect | exit_pop | outra",
      "como_foi_achada": "sitemap | robots | busca_indexada | arquivo | codigo_fonte | backredirect | exit_pop | caminho_testado",
      "preco": "", "acessivel_sem_compra": true }
  ],
  "paginas_nao_acessiveis": ["upsell pós-compra", "área de membros"],
  "pagina": {
    "tipo": "tsl | vsl | hibrida",
    "nivel_consciencia": "inconsciente | problema | solucao | produto | total",
    "engenharia_reversa": {
      "hook": "", "tensao": "", "desejo": "", "crenca": "",
      "mecanismo": "", "prova": "", "objecao": "", "oferta": "", "cta": ""
    },
    "tipo_prova": [""],
    "garantia": "",
    "ausencias": [""]
  },
  "oferta": {
    "nome": "", "promessa": "", "mecanismo_unico": "",
    "entregaveis": [""], "formato_entrega": ""
  },
  "monetizacao": {
    "ticket_entrada": "", "ancoragem": "", "order_bump": "",
    "upsell": "", "downsell": "", "recorrencia": "",
    "checkout": "", "gateway": "",
    "ticket_medio_implicito": "", "premissa_conversao_assumida": ""
  },
  "retencao": [
    { "canal": "email | sms | whatsapp", "ordem": 0, "tempo_apos_optin": "", "angulo": "", "objetivo": "", "vende": "" }
  ],
  "remarketing": [
    { "angulo": "", "objecao_atacada": "", "formato": "" }
  ],
  "cadencia": {
    "reposicao_dias": 0,
    "variacoes_por_angulo": 0,
    "vida_media_angulo_dias": 0,
    "testa_formato": true
  },
  "estimativa_faturamento": {
    "faixa": "", "confianca": "alta | media | baixa",
    "caminhos": [""], "o_que_derruba": ""
  },
  "lacunas": [
    { "camada": "", "descricao": "", "tamanho_fatia": "grande | media | pequena", "custo_execucao": "baixo | medio | alto", "prioridade": 0 }
  ],
  "radioativo": false,
  "captura_aberta": { "email_em_andamento": true, "reabrir_em": "AAAA-MM-DD" }
}
```

## Relatório — template do dossê

```
# Dossê — [alvo] · [data]

## Veredito em 5 linhas
Quem é, que posição ocupa no leilão, o que sustenta a operação, onde ele é forte,
onde ele é vulnerável.

## 1. Aquisição
## 2. Página
## 3. Oferta
## 4. Monetização (a escada desenhada em degraus)
## 5. Retenção (a sequência em linha do tempo)
## 6. Remarketing
## 7. Cadência — o que você precisa produzir por semana pra competir

## Estimativa de faturamento
Faixa, três caminhos, o que derruba.

## As 3 lacunas prioritárias
Para cada: o que falta na operação dele, por que é fatia real, qual o primeiro teste seu.

## O que dá pra modelar e o que não dá
Duas colunas explícitas. Estrutura e lógica de um lado; copy, arte e ativo do outro.
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

- As 7 camadas foram cobertas, ou as ausentes foram declaradas com o motivo?
- O mapeamento de domínio rodou os 9 passos, e cada página achada registra COMO foi achada?
- O que não é acessível sem compra está declarado, em vez de a escada ser apresentada como completa?
- O teste de caminhos ficou numa dezena, sem varredura automatizada?
- Criativos únicos estimados, e não a contagem crua da biblioteca?
- A escada tem todos os degraus, ou está registrado que não achou?
- A sequência de e-mail foi capturada, com data de reabertura se ainda estiver chegando?
- O faturamento saiu como faixa, com três caminhos e o que derruba a estimativa?
- As lacunas foram ranqueadas e viraram recomendação de entrada?
- Nenhuma copy, arte ou entregável do alvo foi reproduzido no dossê?
- Se a operação depende de fraude, foi marcada como radioativa?
- Cruzou com `benchmark.json` pra saber quais micro-personas ele deixou órfãs?
- As três lacunas prioritárias viraram fatias no `banco-de-fatias.json` com `status: "a_testar"`?