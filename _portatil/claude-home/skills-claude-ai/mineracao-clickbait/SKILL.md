---
name: mineracao-clickbait
description: "Minera hooks visuais e clickbait que travam o scroll, capturando imagens e extraindo mecanismo e receita de replicação."
---

# Mineração de Clickbait e Hook Visual

Clickbait bom não é mentira, é engenharia de curiosidade. E a maior parte dessa engenharia é **visual**: o dedo para antes da mente ler. Um relatório de texto sobre hook visual é inútil — você precisa **ver** o gancho, saber **onde ele está** e saber **como refazer**.

Por isso esta skill entrega três coisas, sempre juntas:

1. **A imagem** — capturada e salva em arquivo, embutida num board.
2. **O link** — a fonte, pra você abrir o anúncio vivo e ver contexto e longevidade.
3. **A receita** — como reproduzir aquele gancho com cenário, elenco, props e custo declarados.

Sem os três, a entrega está incompleta.

## Autonomia — execute, não pergunte

Roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

- **Não pergunte o que a coleta responde.** Disse o nicho? Abra a biblioteca e olhe. Decida amostra, alvo e prioridade pelos critérios deste arquivo e informe o que decidiu.
- **Só pare quando** faltar login, permissão de pasta, ou quando a escolha mudar o resultado e houver duas leituras igualmente defensáveis.
- **Execute a cadeia inteira sem pedir aprovação no meio.** Narre em uma linha por etapa enquanto faz.
- **Leia os JSONs do banco antes de começar.** Não refaça trabalho que já existe.
- **Entregue arquivo salvo com o caminho informado**, não texto no chat.
- **Ao terminar, diga três coisas:** o tamanho da amostra, o que saiu, e onde está.
- Capture as imagens e monte o board sem pedir confirmação. Board sem imagem não é entrega.

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

## Linha vermelha (leia antes de capturar)

**Captura é referência, não ativo.** As imagens salvas formam um board de pesquisa interno, do mesmo jeito que um diretor de arte guarda referência numa pasta. O que a skill entrega pra produção é a **receita**, nunca o arquivo do concorrente.

- **Não** reproduza, publique ou suba a arte capturada como criativo seu. Isso é obra de terceiro e gera notificação.
- **Não** use o rosto de pessoa real que aparece na captura. Sua replicação usa seu elenco.
- **Não** catalogue como replicável clickbait que depende de fraude em nicho sensível: cura de doença, garantia financeira, emagrecimento milagroso, prova ou depoimento fabricado. Marque como **linha vermelha**, registre só o mecanismo abstrato e não escreva receita para ele.
- Prefira e destaque a moldura white: gancho de terceira pessoa (sem "você/seu"), narrativa ou jornalística. Agressivo sem tomar ban e sem queimar imagem.

O método é forte sem o veneno. Um gancho que só funciona mentindo não é ativo, é passivo.

## Entrada esperada

Se existir `mineracao/benchmark.json`, leia primeiro e herde o nicho, o corte de longevidade parametrizado pelo ticket, as **micro-personas** (não invente esse campo) e o **grupo de controle**, pra reportar índice de discriminação além do percentual bruto.

Se o usuário mandou um print ou um link de anúncio específico e perguntou "como eu faço um desse", pule a coleta em massa e vá direto para a anatomia e a receita daquele item.

## Capacidade e limite

- **Imagem — é o forte aqui.** Capture thumbnail, criativo estático e o frame dos primeiros segundos e analise composição, contraste, sujeito, texto e tratamento.
- **Vídeo — não assiste.** Não deduza ritmo, corte ou movimento de um arquivo de vídeo. Trabalhe do frame + transcrição + descrição fornecida. Padrão de formato vai para `mineracao-formatos-virais`.
- **Nem toda captura sai.** Se a fonte bloquear a captura, registre o item com o link e a descrição textual e marque `captura_status: "indisponivel"`. Não invente descrição de imagem que você não viu.
- **Texto — puxa direto:** manchetes, primária de anúncio, títulos de YouTube, comentários.
- Amostra mínima 30, ideal 100+. Abaixo disso, baixa confiança.

## Fontes

- **Meta Ad Library** — criativo e primária. Aplique o Radar de Longevidade (21+ dias, ou o corte do benchmark) pra separar gancho que sustenta de gancho que morre.
- **YouTube** — thumbnails dos mais virais do nicho. Thumbnail de viral é o laboratório mais barato de hook visual que existe.
- **TikTok Creative Center** — frames de abertura em tendência.
- **Comentários** — o que o público achou absurdo, odiou ou marcou alguém. Reação alta indica gancho que funcionou.

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

## Anatomia do hook visual — destrinche cada captura

Para cada imagem, registre o que está acontecendo na tela:

- **Composição e enquadramento** — close, plano médio, primeira pessoa (mão segurando), plano aberto.
- **Sujeito** — quem ou o quê ocupa o quadro. Rosto? Objeto? Documento? Comida? Tela de celular?
- **Olhar e direção** — a pessoa olha pra câmera, pra fora, pro objeto? Olhar pra câmera prende; olhar pro objeto direciona a atenção pro objeto.
- **Contraste e cor** — o que salta primeiro. Fundo estourado, cor saturada, alto contraste, flash.
- **Elemento de quebra** — o que não deveria estar ali. Objeto fora de contexto, escala errada, combinação absurda.
- **Texto na tela** — manchete, legenda nativa, caixa de comentário, palavra circulada, seta.
- **Tratamento** — parece anúncio ou parece conteúdo? Foto amadora, print de tela, screenshot de notícia, captura de chamada de vídeo, UGC cru.
- **Anotação** — círculo vermelho, seta, borrão, tarja. Sinaliza "tem algo escondido aqui" e abre loop sozinho.

## Mecanismos de curiosidade a catalogar

- **Open loop / lacuna de informação** — abre uma pergunta que só fecha depois. Quanto mais loops, mais forte.
- **Choque / padrão quebrado** — imagem ou afirmação que não bate com o esperado. Inclui o **Hook Órfão**: visual sem relação com a oferta que mesmo assim para o scroll.
- **Viés da negatividade** — o oposto ou negativo batendo mais que o positivo.
- **Proibido** — enquadre de "o que não querem que você veja". Puxa forte e é o que mais se aproxima da linha vermelha: extraia só o mecanismo.
- **Inimigo comum / autoridade** — vilão externo ou autoridade endossando.
- **Especificidade / ancoragem temporal** — número ou tempo concreto que ancora credibilidade e curiosidade.

## Princípios empilhados

Gancho forte não usa um princípio, empilha vários. "Durante 17 anos, ninguém percebeu que aquilo estava no rótulo" carrega **especificidade + information gap + temporal anchoring + open loop + pattern interrupt** ao mesmo tempo. Liste todos os princípios de cada gancho — é isso que a esteira usa pra montar hook denso.

Trate como **modelo mental, não lei** (priming e psicologia social têm crise de replicação). Não afirme "cientificamente provado".

## Receita de Replicação — a entrega principal

Para cada gancho limpo, escreva uma receita executável. Ela precisa responder o que produzir, com o quê e por quanto:

```
### CB-004 — [nome curto do gancho]

**Mecanismo:** open loop + elemento de quebra
**Por que para o dedo:** [uma linha]

**Como refazer:**
- Cenário: mesa de cozinha, luz de janela, sem produção
- Elenco: 1 pessoa, mãos apenas, sem rosto
- Props: [objeto], [objeto], papel impresso
- Enquadramento: close vertical, objeto ocupando 60% do quadro
- Texto na tela: manchete curta em caixa branca no terço superior
- Tratamento: foto de celular, sem filtro, levemente torta
- Anotação: círculo vermelho no [detalhe]

**Adaptação pro seu nicho:** [como trocar o objeto/tema mantendo o mecanismo]
**Custo:** baixo · **Tempo:** 15 min · **Ferramentas:** celular + Canva
**Variação negativa a testar:** [a versão oposta]
```

A regra da adaptação: **troca o conteúdo, mantém o mecanismo.** Se o gancho original é um documento com um trecho circulado, o seu também é um documento com um trecho circulado — o documento é outro. O que transfere entre nichos é a estrutura visual, não o assunto.

Marque a dificuldade honestamente. Gancho que exige celebridade, locação ou pós-produção pesada é `custo: alto` e a esteira vai despriorizar, mesmo que o mecanismo seja forte.

## Método

- **Amostragem:** só conte o mecanismo que se repete em % alta. Reporte o %.
- **Grupo de controle:** com a amostra dos que morreram cedo, reporte o % nos dois grupos e o índice de discriminação. Mecanismo presente igualmente nos dois é convenção do nicho, não vantagem.
- **Isolamento:** gancho de copy e gancho visual são variáveis independentes e são testadas separadas. Nunca misture na mesma linha.
- **Transferência:** avalie o quão fácil é adaptar cada padrão pra outro nicho.
- **Amarra:** registre a que ângulo e micro-persona o gancho serve e qual estado cognitivo ele mira.

## Passo a passo

1. Leia `benchmark.json` se existir. Confirme o nicho e a micro-persona alvo.
2. Puxe os itens das fontes. **Capture a imagem de cada um** e salve em `mineracao/capturas/` com o id como nome do arquivo. Registre o link da fonte e os dias no ar.
3. Para cada captura, preencha a anatomia visual, isole o mecanismo, liste os princípios empilhados.
4. Marque linha vermelha onde couber. Esses não recebem receita.
5. Escreva a Receita de Replicação de cada gancho limpo, com custo e tempo.
6. Agrupe por mecanismo e conte a repetição nos dois grupos.
7. Ranqueie por %, por transferência e por custo de replicação — barato e forte primeiro.
8. Gere o **board visual** e salve o JSON.

## Saída — três artefatos

### 1. Capturas
`mineracao/capturas/CB-001.png` — uma por gancho, nome do arquivo igual ao id.

### 2. Board visual em `mineracao/board-clickbait.md`

Este é o entregável que a pessoa realmente lê. Abra com um resumo de 5 linhas (quantos ganchos, quantos limpos, quantos linha vermelha, qual mecanismo domina o nicho, qual está subexplorado) e depois uma seção por gancho, na ordem do ranking:

```markdown
## CB-001 · [nome curto] · forte · custo baixo

![CB-001](capturas/CB-001.png)

**Anúncio:** [ver criativo](link_anuncio) · **Biblioteca:** [todos os anúncios do anunciante](link_biblioteca) · **Funil:** [página de vendas](link_funil)
**Anunciante:** [nome] · 47 dias no ar · 23 anúncios ativos · BR
**Mecanismo:** choque + open loop
**Empilha:** especificidade, information_gap, pattern_interrupt
**Micro-persona:** [quem para]
**Anatomia:** close vertical, mão segurando [objeto], fundo estourado,
manchete em caixa branca, círculo vermelho no canto inferior.
**Por que para o dedo:** [uma linha]

**Receita de replicação:** [o bloco completo da seção acima]
```

### 3. JSON em `mineracao/clickbait.json`

```json
[
  {
    "id": "CB-001",
    "tipo": "clickbait",
    "descricao": "o padrão de gancho em uma linha (mecanismo, não a alegação)",
    "mecanismo": "open_loop | choque | negatividade | proibido | inimigo_comum | autoridade | especificidade",
    "principios": ["especificidade", "information_gap", "temporal_anchoring", "open_loop", "pattern_interrupt"],
    "tipo_gancho": "copy | visual | ambos",
    "captura": "capturas/CB-001.png",
    "captura_status": "ok | indisponivel",
    "anatomia_visual": {
      "enquadramento": "",
      "sujeito": "",
      "olhar": "",
      "contraste_cor": "",
      "elemento_quebra": "",
      "texto_na_tela": "",
      "tratamento": "anuncio | conteudo | print | ugc_cru | noticia",
      "anotacao": ""
    },
    "receita_replicacao": {
      "cenario": "",
      "elenco": "",
      "props": [""],
      "enquadramento": "",
      "texto_na_tela": "",
      "tratamento": "",
      "anotacao": "",
      "adaptacao_nicho": "",
      "custo": "baixo | medio | alto",
      "tempo_producao": "",
      "ferramentas": [""]
    },
    "estado_cognitivo": "atencao | curiosidade | desejo | mecanismo | prova | progressao",
    "nivel_consciencia": "inconsciente | problema | solucao | produto | total",
    "micro_persona_id": "MP-001",
    "micro_persona": "nome da micro-persona, exatamente como no benchmark.json",
    "emocao": "gatilho emocional principal",
    "crenca_respeitada": "a crença que o gancho joga ao lado",
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
    "variacao_negativa": "",
    "linha_vermelha": false,
    "status": "validado | a_testar"
  }
]
```

O campo `receita_replicacao` é o que a `esteira-de-hook` consome pra preencher a coluna de visual da tabela de produção. Se ele vier vazio, o editor não consegue produzir a peça.

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
- `link_funil` é a URL final, já resolvida depois do redirect, e não o encurtador?

- Toda entrada tem imagem salva, ou está marcada `captura_status: "indisponivel"` com o motivo?
- Todo item tem link da fonte e dias no ar?
- Todo gancho limpo tem receita executável, com custo e tempo declarados?
- A receita adapta o mecanismo em vez de copiar o assunto do concorrente?
- Gancho de copy e gancho visual foram isolados?
- Cada gancho lista todos os princípios que empilha?
- Itens de linha vermelha foram marcados, reduzidos a mecanismo abstrato e ficaram sem receita?
- Nenhuma arte capturada foi entregue como ativo produzível?
- Amostra ≥ 30 (ideal 100+), com % nos dois grupos e índice de discriminação quando havia controle?
- Nada afirmado como "cientificamente provado"?
- Board gerado com as imagens embutidas, e JSON no contrato exato?