---
name: mineracao-angulo
description: "Minera ângulos de resposta direta que estão escalando na Ad Library e ângulos antigos adaptáveis, destrincha os princípios de persuasão e devolve JSON pronto pra esteira de hook. Use para minerar, achar ou extrair ângulo, ou dissecar anúncios/VSL/swipe."
---

# Mineração de Ângulo

O ângulo é a variável que decide qual fatia do leilão você ganha. Criativo satura; ângulo validado vira mina que se explora por meses. Esta skill acha o ângulo — não o criativo pronto. O princípio-mestre: **ângulo antigo, formato atual.** Ângulo novo praticamente não existe; você adapta ângulo que já foi testado em milhões e veste com o formato de hoje.

## Autonomia — execute, não pergunte

Roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

- **Não pergunte o que a coleta responde.** Disse o nicho? Abra a biblioteca e olhe. Decida amostra, alvo e prioridade pelos critérios deste arquivo e informe o que decidiu.
- **Só pare quando** faltar login, permissão de pasta, ou quando a escolha mudar o resultado e houver duas leituras igualmente defensáveis.
- **Execute a cadeia inteira sem pedir aprovação no meio.** Narre em uma linha por etapa enquanto faz.
- **Leia os JSONs do banco antes de começar.** Não refaça trabalho que já existe.
- **Entregue arquivo salvo com o caminho informado**, não texto no chat.
- **Ao terminar, diga três coisas:** o tamanho da amostra, o que saiu, e onde está.
- Puxe das quatro fontes por conta própria. Amostra pequena se declara, não se pergunta.

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

## O que ela faz
Recebe um nicho (ou um material bruto) e devolve um conjunto de ângulos validados, ranqueados por força (% de repetição na amostra) e adaptabilidade, cada um destrinchado nos princípios de persuasão e etiquetado no contrato que a esteira de hook consome.

## Entrada esperada (rode depois do Raio-X quando possível)
Se existir `mineracao/benchmark.json`, leia primeiro. Dele você herda, sem precisar refazer:
- o nicho, o país e o corte de longevidade já parametrizado pelo ticket;
- as **micro-personas** do mercado (é de lá que vem o campo `micro_persona`, que esta skill não deve inventar);
- o **grupo de controle** e o índice de discriminação já calculados;
- a **fatia prioritária** que o Mapa de Fatias apontou.

Divisão de trabalho: o Raio-X **rotula** ângulo grosso pra contar densidade de célula. Esta skill **destrincha** a fatia que ele apontou. Se o benchmark não existir, rode normalmente, mas avise que a amostra não tem grupo de controle e que as micro-personas são inferência sua.

## Capacidade e limite (leia antes de rodar)
- **Texto — puxa e analisa direto:** copy de anúncio (Meta Ad Library), data "ativo desde" (o filtro de longevidade), reviews da Amazon, comentários de Reddit/YouTube, swipe em texto. É aqui que ângulo mora, então a skill é forte nisso.
- **Visual — por screenshot:** quando o ângulo depende de uma imagem, capture o frame e analise a imagem.
- **Vídeo — não assiste:** não interprete movimento/edição. Se o ângulo veio de um vídeo, trabalhe da transcrição + frames + descrição fornecida. Para formato de vídeo, use a skill `mineracao-formatos-virais`.
- Nunca conclua um padrão de menos de 30 itens. Ideal 100+. Se a amostra é pequena, diga isso e marque os achados como baixa confiança.

## Fontes e como puxar
Use as ferramentas de web/navegador disponíveis. Puxe de várias fontes e cruze — o padrão só é real quando aparece em fontes diferentes.

1. **Meta Ad Library** (`facebook.com/ads/library`) — busque o nicho/concorrente. Aplique o **Radar de Longevidade**: só considere anúncio ativo há 21+ dias contínuos (a data "ativo desde" prova lucro; beleza é irrelevante). Extraia a copy primária e a estrutura lógica. Se o benchmark definiu outro corte pelo ticket, use o dele.
2. **Amazon best-sellers do nicho** — leia os reviews (positivos e negativos). Deles saem desejos, dores e a linguagem exata do público.
3. **Reddit + comentários de YouTube/TikTok** do nicho — minere crença e linguagem: o que o público jura ser verdade, o que odeia, os termos que só eles usam.
4. **Swipe antigo / cartas de venda / headlines de jornal** — a mina de ângulo antigo. Se o usuário fornecer, use; se não, busque swipe files públicos do nicho ou adjacentes.

## Método (o que separa isso de prompt genérico)
- **Amostragem:** conte só o que se repete em % alta sobre a amostra. Reporte o % de cada achado — o % é a força do ângulo.
- **Grupo de controle:** quando o benchmark tiver fornecido a amostra dos que morreram cedo, reporte também o % nesse grupo e o índice de discriminação. Ângulo comum nos dois grupos é convenção do nicho, não vantagem.
- **Isolamento de variável:** separe ângulo de formato de avatar. Você está minerando ÂNGULO (a promessa/narrativa central), não o formato nem a estética.
- **Alinhamento de crença:** todo ângulo tem que jogar AO LADO da crença do público, nunca contra. Marque, pra cada ângulo, a crença que ele respeita.
- **Viés da negatividade:** para todo ângulo forte, gere também a versão negativa/oposta. Sinalize como variação a testar.
- **Clickbait transferível (lente de adaptação):** ângulos de choque+curiosidade de QUALQUER nicho costumam ser transferíveis. Avalie a adaptabilidade de cada um.

## Links obrigatórios (nenhum item sai sem eles)

Achado sem link é achado inútil: você não consegue conferir, não consegue reabrir depois e não consegue mostrar pra ninguém. Todo item do JSON carrega **três links**, e cada um responde uma pergunta diferente:

1. **`link_anuncio`** — o anúncio específico, pra ver o criativo exato que você catalogou.
   Formato: `https://www.facebook.com/ads/library/?id=<AD_ID>`
2. **`link_biblioteca`** — a biblioteca inteira daquele anunciante, filtrada. É aqui que você vê o volume real que ele sustenta e volta daqui a 15 dias pra saber se ainda está no ar.
   Formato: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=<PAIS>&view_all_page_id=<PAGE_ID>`
3. **`link_funil`** — o destino do anúncio, a página de vendas. É o funil. Registre a URL final depois do redirect, não o encurtador.

Regras:
- **Nunca invente URL.** Só entra link que veio da coleta e que você conferiu que abre. Se um dos três não existir (anúncio sem destino, página fora do ar), grave `null` e escreva o motivo em `fonte.observacao`. Campo vazio inventado é pior que campo ausente.
- Registre também `anunciante`, `page_id`, `pais`, `dias_no_ar` e `anuncios_ativos`, porque é o que permite reabrir a busca quando o link direto quebrar.
- Se o item veio de YouTube ou TikTok em vez da Ad Library, `link_biblioteca` vira o canal ou perfil e `link_anuncio` vira o vídeo. Marque a origem em `fonte.plataforma`.
- No board e no relatório, os links vão **clicáveis**, não como texto solto.

## A Ciência do Ângulo — destrinche cada peça nos princípios
Para cada ângulo, identifique quais princípios de persuasão ele empilha (é isso que o torna forte e reutilizável). Trate como **modelo mental, não lei** (priming/psicologia social têm crise de replicação; information gap, curiosidade e mere exposure são sólidos, social priming é o escorregadio). Não afirme "cientificamente provado"; use "é o que explica o que escala".

Princípios a marcar: **information gap · open loop · novel mechanism · reason-why · enemy construction · mechanism of failure · mechanism of success · belief sequencing · contrast · specificity · desire channeling · pattern interrupt · temporal anchoring · social proof transfer.**

E rode o **schema de engenharia reversa** em cada peça (é o banco de princípios reutilizável):
`HOOK → TENSÃO → DESEJO → CRENÇA → MECANISMO → PROVA → OBJEÇÃO → OFERTA → CTA`

Também marque, pra cada ângulo, qual **estado cognitivo** ele mira (atenção, curiosidade, desejo, mecanismo, prova, progressão).

## Passo a passo
1. Leia `benchmark.json` se existir. Confirme o nicho, o mercado e (se houver) a oferta/mecanismo do usuário. Se ele deu material bruto, pule pra análise.
2. Puxe das 4 fontes acima. Registre a amostra (quantos itens de cada fonte).
3. Extraia candidatos a ângulo. Destrinche cada um no schema e nos princípios. Preencha o contrato de saída.
4. Ranqueie por % de repetição (e por índice de discriminação, quando houver controle), depois por adaptabilidade.
5. Rode a checklist de qualidade.
6. Salve o JSON na pasta que a esteira lê e avise o usuário quantos ângulos validados saíram.

## Saída — contrato compartilhado da esteira
Salve um array JSON em `mineracao/angulos.json` (crie a pasta se não existir). MESMO contrato das skills de formato e clickbait.

```json
[
  {
    "id": "ANG-001",
    "tipo": "angulo",
    "descricao": "resumo do ângulo em uma linha",
    "mecanismo": "mecanismo do problema/solução, inimigo comum, nova causa",
    "principios": ["information_gap", "novel_mechanism", "enemy_construction"],
    "estado_cognitivo": "atencao | curiosidade | desejo | mecanismo | prova | progressao",
    "engenharia_reversa": {
      "hook": "", "tensao": "", "desejo": "", "crenca": "",
      "mecanismo": "", "prova": "", "objecao": "", "oferta": "", "cta": ""
    },
    "nivel_consciencia": "inconsciente | problema | solucao | produto | total",
    "micro_persona_id": "MP-001",
    "micro_persona": "nome da micro-persona, exatamente como no benchmark.json",
    "emocao": "gatilho emocional principal",
    "crenca_respeitada": "a crença do público que o ângulo joga ao lado",
    "repeticao_pct": 0,
    "repeticao_pct_controle": 0,
    "indice_discriminacao": 0,
    "amostra_n": 0,
    "amostra_anunciantes": 0,
    "pecas_lidas": 0,
    "tipo_de_origem": "controle | variacao_de_controle",
    "fonte": {
      "plataforma": "meta_ad_library | youtube | tiktok | outro",
      "anunciante": "",
      "page_id": "",
      "pais": "",
      "link_anuncio": "https://www.facebook.com/ads/library/?id=AD_ID",
      "link_biblioteca": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&view_all_page_id=PAGE_ID",
      "link_funil": "url da página de vendas, já resolvida depois do redirect",
      "dias_no_ar": 0,
      "anuncios_ativos": 0,
      "observacao": "motivo de qualquer link null"
    },
    "adaptabilidade": "alta | media | baixa",
    "variacao_negativa": "a versão oposta/negativa do ângulo, a testar",
    "linha_vermelha": false,
    "status": "validado | a_testar"
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
- Todo item tem os TRÊS links (anúncio, biblioteca do anunciante, funil), ou `null` com motivo?
- Nenhum link foi inventado — todos vieram da coleta e abrem?
- `link_funil` é a URL final, já resolvida depois do redirect, e não o encurtador? (rode antes de entregar)
- Amostra >= 30 (ideal 100+)? Se não, marcado como baixa confiança.
- Todo achado tem % de repetição real, não achismo?
- Quando havia grupo de controle, o índice de discriminação foi calculado?
- Ângulo, formato e avatar foram isolados?
- Cada ângulo foi destrinchado no schema e tem os princípios que empilha?
- Cada ângulo tem a crença que respeita e a micro-persona alvo (herdada do benchmark, não inventada)?
- Ângulos vindos de anúncio vivo passaram pelo Radar de Longevidade?
- Nada afirmado como "cientificamente provado" — princípios tratados como modelo mental?
- O JSON está no contrato exato acima, pronto pra esteira?