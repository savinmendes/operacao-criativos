---
name: diagnostico-criativo
description: "Lê o resultado do gerenciador e aponta qual pedaço do criativo (hook, corpo, CTA ou página) está quebrado, escreve no Banco de Fatias e chama a esteira pelos substitutos."
---

# Diagnóstico de Criativo

Criativo não morre inteiro, morre por pedaço. Quem mata a peça toda joga fora o ângulo, o avatar e o formato junto com o gancho ruim, e no dia seguinte recomeça do zero. Esta skill lê o número, isola o pedaço quebrado e devolve só ele para a esteira.

É também a única skill do pack que **fecha o loop**: sem ela o Banco de Fatias só acumula hipótese e nunca recebe resultado. Com ela, cada rodada de teste ensina alguma coisa ao próximo Raio-X.

## Autonomia — execute, não pergunte

Roda no Cowork, com navegador, terminal e pasta local. **Você tem as mãos. Use.**

- **Não pergunte o que a coleta responde.** Disse o nicho? Abra a biblioteca e olhe. Decida amostra, alvo e prioridade pelos critérios deste arquivo e informe o que decidiu.
- **Só pare quando** faltar login, permissão de pasta, ou quando a escolha mudar o resultado e houver duas leituras igualmente defensáveis.
- **Execute a cadeia inteira sem pedir aprovação no meio.** Narre em uma linha por etapa enquanto faz.
- **Leia os JSONs do banco antes de começar.** Não refaça trabalho que já existe.
- **Entregue arquivo salvo com o caminho informado**, não texto no chat.
- **Ao terminar, diga três coisas:** o tamanho da amostra, o que saiu, e onde está.
- Calcule as quatro métricas por anúncio e já gere os substitutos na mesma rodada. Diagnóstico sem substituto é meio trabalho.

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

- **Ideal:** export do gerenciador em CSV, com as colunas de retenção. Sem elas o diagnóstico fica cego no hook e no corpo.
- **Aceitável:** planilha colada, ou print. De print você lê o que dá e **declara o que não conseguiu ler**.
- **Também leia, se existirem:** `banco-de-fatias.json`, `esteira/leva-*.json` (pra saber qual variável estava isolada em cada peça) e `benchmark.json` (pras micro-personas).

Colunas que importam, e o nome que costumam ter no gerenciador: reproduções de 3s, reproduções até 25/50/75/100%, cliques no link, CTR (all e link), CPM, CPC, CPA, gasto, resultados, e o tempo médio de reprodução.

Se faltar coluna, diga qual falta e o que ela impedia de concluir. Não invente métrica derivada de dado que não veio.

## A matriz — o número aponta o pedaço

Calcule e compare, nesta ordem. **A ordem importa:** um número ruim mais abaixo pode ser consequência do de cima, e trocar o CTA quando o hook está quebrado é desperdício.

| Métrica | Como calcula | Corte | O pedaço quebrado |
|---|---|---|---|
| **Thumb Stop** | reproduções 3s ÷ impressões | < 30% | O **hook**. Ele não interrompe |
| **Hold** | reproduções 100% ÷ reproduções 3s | < 12% | O **corpo**. Parou, mas não sustentou |
| **CTR (link)** | cliques no link ÷ impressões | < 1,5% | O **CTA**. Reteve e não pediu direito |
| **Conversão da página** | vendas ÷ cliques | < 75% do teu padrão | A **página**. O criativo entregou e a página perdeu |

Os cortes acima são ponto de partida. Se o Banco de Fatias tiver histórico do nicho, **use a mediana do próprio histórico como corte** e diga que fez isso: um Thumb Stop de 28% pode ser ruim num nicho e ótimo noutro.

### Os três portões, no número

O diagnóstico fica mais afiado quando você liga a métrica à função que falhou:

- Thumb Stop baixo → falhou o portão de **interromper**. Troca gancho visual, primeiros 500ms, contraste.
- Thumb Stop alto e Hold baixo → o gancho parou **as pessoas erradas**. Falhou o portão de identificar. Não é o corpo: é o gancho atraindo quem não é do público. Sintoma clássico do Hook Órfão.
- Hold alto e CTR baixo → reteve e não pediu. É CTA, e quase sempre é preguiça de chamada.
- CTR alto e CPA alto → o criativo fez o trabalho. O problema é página, oferta ou preço.

Essa segunda linha é a mais valiosa e a que quase ninguém lê certo. Hold baixo é reflexo de gancho errado com muito mais frequência do que de corpo ruim.

## Regras de decisão

- **Meio ticket sem venda, mata.** Gastou metade do ticket sem conversão, não espera.
- **Amostra mínima antes de concluir qualquer coisa:** sem impressões suficientes, o número é ruído. Diga o N e marque baixa confiança em vez de opinar.
- **Não diagnostique variável que não foi isolada.** Se a peça mudou três coisas de uma vez, o número não te diz qual delas causou. Registre isso como falha de processo e aponte pra esteira.
- **Um pedaço por rodada.** Trocar hook e CTA juntos te devolve ao mesmo lugar: resultado sem causa.
- **Padrão antes de peça.** Antes de diagnosticar um anúncio, veja se o mesmo sintoma aparece em várias peças da mesma micro-persona. Se aparece, o problema não é a peça, é a fatia.

## Escrita de volta no Banco de Fatias — obrigatório

Cada peça diagnosticada atualiza o banco. É isso que transforma o pack num sistema que aprende:

```json
{
  "id": "NB-MP03-ANG07-FMT02-base-001",
  "micro_persona_id": "MP-003",
  "angulo_id": "ANG-007",
  "formato_id": "FMT-002",
  "variavel_isolada": "gancho_visual",
  "metricas": {
    "impressoes": 0, "thumb_stop": 0, "hold": 0,
    "ctr_link": 0, "cpm": 0, "cpa": 0, "gasto": 0, "resultados": 0
  },
  "portao_que_falhou": "interromper | identificar | pedir | n/a",
  "pedaco_quebrado": "hook | corpo | cta | pagina | nenhum",
  "veredito": "validado | morto | inconclusivo",
  "confianca": "alta | media | baixa",
  "motivo": "uma linha",
  "data": "AAAA-MM-DD"
}
```

Peça que validou vira variável fixa para aquela micro-persona no próximo Raio-X. Peça que morreu impede a esteira de repropor a mesma combinação como novidade. Peça inconclusiva volta pra fila com o N declarado.

## Chamar a esteira — a mesma rodada

Depois do diagnóstico, **não pare no veredito**. Gere os substitutos:

1. Trave tudo que o número não acusou. Se o hook falhou, ângulo, formato, avatar e corpo continuam iguais.
2. Chame a `esteira-de-hook` pedindo N peças variando **só o pedaço quebrado**, na mesma micro-persona e no mesmo ângulo.
3. Puxe a receita de replicação do `clickbait.json` quando o pedaço for gancho visual, pra o substituto sair produzível.
4. Entregue a tabela de produção junto com o diagnóstico.

O usuário deve terminar a conversa com o que trocar **e** com as peças novas prontas, não com um relatório.

## Passo a passo

1. Leia o export. Diga quais colunas vieram e quais faltaram.
2. Leia `banco-de-fatias.json` e a leva correspondente, se existirem.
3. Calcule as quatro métricas por anúncio. Use mediana do histórico como corte quando houver.
4. Rode a matriz na ordem: hook, corpo, CTA, página. Pare no primeiro que quebrou.
5. Verifique se o sintoma se repete na micro-persona — peça ou fatia?
6. Aplique as regras de decisão. Marque baixa confiança onde a amostra não dá.
7. Escreva no Banco de Fatias.
8. Chame a esteira e entregue os substitutos.

## Saída — relatório

```
# Diagnóstico — [conta/campanha] · [período]

## Leitura em 3 linhas
O que está quebrado, em qual camada, e o que fazer primeiro.

## Tabela
anúncio · gasto · Thumb Stop · Hold · CTR · CPA · portão que falhou · pedaço · veredito

## Padrão por micro-persona
Onde o mesmo sintoma se repete — peça ou fatia?

## O que matar, o que deixar, o que trocar
Listas separadas. Sem meio-termo.

## Substitutos gerados
A tabela de produção das peças novas, variando só o pedaço quebrado.

## O que eu não consegui ler
Colunas ausentes e o que elas impediam de concluir.
```

## Limites — diga sempre

- Métrica de plataforma tem atribuição própria e janela própria; não é verdade absoluta.
- Amostra pequena não vira conclusão, vira hipótese.
- Correlação entre variável e resultado não é causa quando a variável não foi isolada.
- Esta skill lê o que aconteceu. Ela não prevê o que vai acontecer.

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

- As colunas ausentes foram declaradas?
- As quatro métricas foram calculadas por anúncio, e não só no agregado?
- A matriz rodou na ordem, parando no primeiro pedaço quebrado?
- Thumb Stop alto com Hold baixo foi lido como gancho errado, e não como corpo ruim?
- O sintoma foi checado na micro-persona antes de ser atribuído à peça?
- Peça com mais de uma variável alterada foi marcada como não diagnosticável?
- Todo veredito foi escrito no Banco de Fatias com data e confiança?
- Os substitutos foram gerados variando só o pedaço quebrado?