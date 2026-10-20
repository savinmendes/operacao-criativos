---
name: dissecacao-de-criativo
description: "Pega os anúncios mais escalados de uma oferta/anunciante na Ad Library, reconstrói o roteiro e destrincha cada um em ângulo, avatar, formato e hook de uma vez, gravando em banco/criativos.json e consolidando numa planilha. Use para dissecar oferta, destrinchar anúncios de concorrente, ou montar planilha de criativos."
---

# Dissecacão de Criativo

O Raio-X conta densidade de fatia. As minerações olham uma variável por vez, no nicho inteiro. Esta skill faz o movimento que faltava: pega **os anúncios mais escalados de uma oferta** e destrincha **cada peça nas quatro variáveis de uma vez**, mantendo tudo amarrado ao anúncio de origem.

A diferença importa. Quando ângulo, avatar, formato e hook vêm de listas separadas, você perde a informação de qual combinação estava junta no anúncio que escalou. É essa combinação que a esteira precisa pra lateralizar sem chutar.

Saída: uma linha por anúncio no `criativos.json` e uma planilha com aba por elemento.

## Autonomia — execute, não pergunte

Roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

- **Não pergunte o que a coleta responde.** Disse o nicho? Abra a biblioteca e olhe. Decida amostra, alvo e prioridade pelos critérios deste arquivo e informe o que decidiu.
- **Só pare quando** faltar login, permissão de pasta, ou quando a escolha mudar o resultado e houver duas leituras igualmente defensáveis.
- **Execute a cadeia inteira sem pedir aprovação no meio.** Narre em uma linha por etapa enquanto faz.
- **Leia os JSONs do banco antes de começar.** Não refaça trabalho que já existe.
- **Entregue arquivo salvo com o caminho informado**, não texto no chat.
- **Ao terminar, diga três coisas:** o tamanho da amostra, o que saiu, e onde está.
- Baixe, extraia os frames e monte a planilha de ponta a ponta. Rode o consolidador no fim, sempre.

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

## O limite do vídeo, e como contornar

**O Claude não assiste vídeo.** Não existe versão disso que assista. Ele não percebe movimento, corte nem ritmo a partir de um arquivo. Qualquer skill que prometa "analisar o vídeo" está mentindo sobre o mecanismo.

O que funciona é reconstruir o vídeo por quatro vias, em ordem de preferência:

**1. Legenda queimada lida por frames (a principal).** A maioria esmagadora dos anúncios de resposta direta tem legenda palavra a palavra queimada na tela. Capture frames a cada 1 a 1,5 segundo e leia o texto na imagem: você reconstrói praticamente o roteiro inteiro sem áudio nenhum. É a via mais confiável e é a que resolve o problema na prática. Marque `transcricao.origem: "legenda_queimada"`.

**2. Captions da plataforma.** YouTube e TikTok expõem transcrição automática em boa parte dos vídeos. Puxe quando existir. Marque `"caption_api"`.

**3. Transcrição fornecida.** O usuário cola o roteiro. Marque `"fornecida"`.

**4. Descrição estruturada.** Para o que nenhuma das anteriores cobre (ritmo de corte, trilha, energia da fala), o usuário preenche o template curto. Marque o que veio daí e **não invente o resto**.

Regra dura: se você não conseguiu reconstruir a fala por nenhuma via, grave `transcricao.origem: "indisponivel"` e deixe os campos dependentes vazios. **Nunca escreva um roteiro plausível.** Roteiro inventado contamina ângulo, hook e planilha, e ninguém descobre até o criativo morrer no gerenciador.

## Como escolher "os mais escalados"

Escalado não é o que tem mais curtida. É o que consome verba há mais tempo. Ranqueie os anúncios do alvo por, nesta ordem:

1. **Dias no ar** — passa o corte de longevidade do benchmark (10, 21, 30 ou 45 dias conforme o ticket).
2. **Número de variações do mesmo criativo** — quem varia é porque está investindo em cima daquilo.
3. **Reposição recente** — anúncio antigo E renovado nos últimos 15 dias é o controle vivo do concorrente.

Pegue os **10 a 20 primeiros**, não todos. Vinte anúncios bem dissecados valem mais que duzentos rotulados no atacado. Se o alvo tiver menos de 5 anúncios acima do corte, diga que a operação dele é pequena demais pra extrair padrão e trate os achados como baixa confiança.

Cuidado com a contagem: dynamic creative e múltiplos posicionamentos duplicam linhas. Estime criativos únicos antes de ranquear.

## As quatro variáveis, por anúncio

Destrinche cada peça nas quatro, sempre separadas, porque são testadas separadas:

**Ângulo** — a promessa e a narrativa central. Qual o mecanismo do problema, quem é o vilão, qual a lacuna de informação. Se o ângulo já existe no `angulos.json`, reutilize o id em vez de criar outro.

**Avatar** — quem aparece em cena. Esta é uma das variáveis mais baratas de trocar e classifica em três arquétipos:

- **autoridade** — "eu resolvo esse problema". O especialista, o médico, o profissional indignado com o sistema.
- **transformado** — "eu tive esse problema". Fala a dor por dentro; casa com UGC e primeira pessoa.
- **espectador** — "meu pai teve esse problema". Terceira pessoa; mira o cuidador em vez de quem sofre, e é agressivo sem convidar bloqueio.

Registre também gênero, faixa etária, papel concreto, voz e tratamento (UGC cru, produção, print, notícia).

**Avatar não é micro-persona:** o avatar é quem fala, a micro-persona é quem escuta. Filha cuidadora falando pode mirar a própria cuidadora ou a idosa. Registre os dois, sempre.

**Formato** — o macro (UGC selfie, react de podcast, entrevista de rua, GC, notícia, tutorial, editadão) mais cenário, plano e estilo de legenda.

**Hook** — separado em visual (o que aparece nos 0-3s) e copy (a primeira fala). Liste os princípios que o gancho empilha.

## Passo a passo

1. Determine o alvo pelo mercado: se o usuário não nomeou anunciante, escolha o de maior longevidade no nicho e diga qual escolheu. Leia `benchmark.json` se existir, pra herdar corte de longevidade e micro-personas.
2. Abra a biblioteca do anunciante. Estime criativos únicos e ranqueie pelo critério acima. Registre `link_biblioteca`.
3. Para os 10-20 do topo: capture frames (0s, e depois a cada 1-1,5s até uns 15s), reconstrua a fala pela melhor via disponível, registre a origem da transcrição.
4. Destrinche cada anúncio nas quatro variáveis. Reutilize ids existentes quando o elemento já estiver no banco.
5. Colete os três links de cada peça: `link_anuncio`, `link_biblioteca`, `link_funil` (URL final, depois do redirect). Nada de link inventado; ausente vira `null` com motivo.
6. Marque `linha_vermelha: true` em qualquer peça que dependa de fraude em nicho sensível. Ela entra no banco como aviso e não é replicável.
7. Grave `banco/criativos.json`.
8. Rode o consolidador e entregue a planilha.

## Loop de palavra-chave — expandir a amostra sozinho

Depois de dissecar as primeiras peças, use a transcrição pra achar mais anunciantes em vez de parar no alvo:

1. Da transcrição de cada ad escalado, extraia os termos que sustentam aquela lógica (mecanismo, sintoma, objeto, expressão do público). Peça de 20 a 30, não 3.
2. Busque cada termo na Ad Library. Cada palavra abre um conjunto novo de anunciantes que você não conhecia.
3. Os novos ads escalados que aparecerem voltam pro passo 1.

O ciclo se alimenta: cada oferta achada devolve as palavras que acham a próxima. Registre em `termos_derivados` de onde cada termo saiu, e pare quando os termos novos só devolverem anunciantes já catalogados — é o sinal de que você cobriu o nicho.

## Consolidação — a planilha

```bash
python3 scripts/consolidar_planilha.py [pasta_raiz] [saida.xlsx]
```

Lê tudo que existir (`criativos.json`, `angulos.json`, `clickbait.json`, `formatos.json`, `benchmark.json`, `virais.json`, `publico.json`, `banco-de-fatias.json`) e gera **uma planilha com 10 abas**: Resumo, Criativos, Angulos, Avatares, Formatos, Hooks, Publico, Virais, Anunciantes, Fatias.

Comportamento que importa: **arquivo ausente vira aba vazia com cabeçalho**, nunca erro. A aba Avatares é derivada dos criativos, com dedupliçao e contagem de ocorrências. Os links saem clicáveis. O Resumo usa fórmulas de contagem, então cresce sozinho quando você regerar.

Rode o script sempre que pedirem "junta tudo", "me dá a planilha" ou "consolida o banco". Não monte planilha na mão: o script é determinístico e a montagem manual erra coluna.

Se o ambiente tiver o utilitário de recálculo, rode depois pra as contagens do Resumo aparecerem preenchidas.

## Saída — `banco/criativos.json`

```json
[
  {
    "id": "CRI-001",
    "oferta": "",
    "micro_persona_id": "MP-001",
    "micro_persona": "quem ESCUTA o anúncio",
    "angulo": {
      "id": "ANG-001",
      "descricao": "",
      "mecanismo": "",
      "principios": [""],
      "crenca_respeitada": ""
    },
    "avatar": {
      "id": "AVT-001",
      "arquetipo": "autoridade | transformado | espectador",
      "descricao": "quem APARECE em cena, em uma linha",
      "afirma_credencial": false,
      "genero": "",
      "faixa_etaria": "",
      "papel": "paciente | cuidador | conjuge | especialista | anonimo | so_maos | figura_publica",
      "voz": "primeira_pessoa | terceira_pessoa",
      "tratamento": "ugc_cru | producao | print | noticia | animacao"
    },
    "formato": {
      "macro": "ugc_selfie | react_podcast | entrevista_rua | gc | noticia | tutorial | editadao",
      "cenario": "",
      "plano": "",
      "estilo_legenda": ""
    },
    "hook": {
      "visual": "o que aparece nos 0-3s",
      "copy": "a primeira fala",
      "principios": [""]
    },
    "transcricao": {
      "origem": "legenda_queimada | caption_api | fornecida | descricao_estruturada | indisponivel",
      "texto": "roteiro reconstruído, ou vazio se indisponivel",
      "cobertura_pct": 0
    },
    "nivel_consciencia": "inconsciente | problema | solucao | produto | total",
    "estado_cognitivo": "atencao | curiosidade | desejo | mecanismo | prova | progressao",
    "emocao": "",
    "crenca_respeitada": "",
    "linha_vermelha": false,
    "fonte": {
      "plataforma": "meta_ad_library",
      "anunciante": "",
      "page_id": "",
      "pais": "",
      "link_anuncio": "https://www.facebook.com/ads/library/?id=AD_ID",
      "link_biblioteca": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&view_all_page_id=PAGE_ID",
      "link_funil": "url final da página de vendas",
      "dias_no_ar": 0,
      "anuncios_ativos": 0,
      "observacao": ""
    }
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

- Os anúncios foram ranqueados por longevidade e variação, não por engajamento?
- Criativos únicos estimados, e não linhas cruas da biblioteca?
- Toda peça declara a origem da transcrição, e nenhuma fala foi inventada?
- As quatro variáveis foram extraídas separadas em toda peça?
- Avatar foi distinguido de micro-persona (quem aparece x quem escuta) e classificado no arquétipo?
- Peça que afirma credencial profissional foi marcada em `afirma_credencial`?
- O loop de palavra-chave rodou até saturar, ou o motivo de parar está declarado?
- Ids reutilizados quando o elemento já existia no banco, em vez de duplicar?
- Os três links em toda peça, conferidos, com `null` justificado onde faltar?
- Peças radioativas marcadas `linha_vermelha: true`?
- Planilha gerada pelo script, com o número de linhas conferido contra o JSON?