---
name: consultor-de-cases
description: Consulta uma base de transcrições de cases de mercado (podcasts, entrevistas, aulas, mentorias, cursos) para validar uma estratégia, achar precedente, gerar ideia ou entender como outras operações resolveram um problema. Use sempre que a pessoa perguntar se alguém já fez algo, o que o mercado está fazendo sobre um tema, se uma ideia faz sentido, quais padrões aparecem entre operações que escalaram, ou pedir para cruzar o que vários convidados disseram — ex.: "alguém já testou isso?", "o que falaram sobre upsell?", "essa estratégia faz sentido?", "quem discorda disso?", "compara o que os caras falaram sobre criativo". Também use ao processar material novo para dentro da base (transcrição nova que precisa virar ficha). É genérica: funciona com qualquer fonte, qualquer nicho e qualquer projeto, e não pressupõe nada sobre o negócio de quem pergunta.
---

# Consultor de cases

Esta skill transforma uma pilha de transcrições em algo consultável: responde
perguntas de estratégia citando quem disse, quando disse e com que ressalva —
e, principalmente, mostra quem discorda.

## O problema que ela resolve, e o que ela não resolve

Uma base feita de **cases de sucesso é viés de sobrevivência puro**. Só entra
quem deu certo, quem topou dar entrevista e quem tem algo a vender ao contar a
história. Uma base assim confirma praticamente qualquer coisa que se pergunte a
ela.

Por isso esta skill não serve para "provar que minha ideia está certa". Serve
para **mapear o espaço de soluções e achar onde elas quebram**. Se o resultado
de uma consulta for só concordância, a consulta foi mal feita — volte e procure
o contra-caso.

## Quando usar

Use quando a pessoa quiser validar estratégia, achar precedente, gerar ideia,
entender um tema pelo que já foi dito na base, ou processar material novo para
dentro dela. Não é necessária para responder algo que não depende da base.

## Passo 0 — Parâmetros

Infira o que puder. **Só pergunte se algo essencial não der para inferir.**

| Parâmetro | Como resolver |
|---|---|
| Pasta da base | Pasta com as transcrições `.md`. Se o projeto só tem uma, use-a. As fichas ficam em `_fichas/` dentro dela. |
| Contexto de quem pergunta | Leia `contexto/` (ou equivalente) do projeto para saber quais são as frentes de negócio, as métricas que importam e o vocabulário. Sem isso não dá para julgar o que transfere. |
| Profundidade | Pergunta pontual: busca direta basta. Pergunta comparativa ("quais padrões", "quem discorda"): precisa das fichas. |

---

## Fluxo 0 — Alimentar a base pelo YouTube (custo zero de tokens)

Use quando a pessoa mandar links, uma playlist ou um canal («os 50 vídeos mais recentes de @canal»).

1. **Transcreva** com o transcritor do projeto (procure em `ferramentas/`). Se não houver, use `yt-dlp` para a legenda e Whisper local para os vídeos sem legenda. Para os N vídeos mais recentes de um canal, liste antes com `yt-dlp --flat-playlist --playlist-end N`.
   - Esta etapa roda local e não gasta token: pode deixar rodando em segundo plano.
2. **Leve para a base** e gere índice e esqueleto das fichas, também de graça:
   ```bash
   python scripts/alimentar.py <pasta-das-transcricoes> <pasta-da-base> --canal "<nome do canal>"
   ```
   - Copia para `<base>/transcricoes/<canal>/` só o que ainda não está lá. Nunca sobrescreve.
   - Roda o `fichar.py --lote`.
   - Reescreve `<base>/INDICE.md`, com o estado de cada ficha: sem ficha / esqueleto / preenchida.
3. **Preencher as fichas (Fluxo B) gasta token**: é ler a transcrição inteira.
   - Antes, informe o volume (horas × ~12 mil tokens por hora de fala) e **espere a pessoa autorizar**.
   - Ofereça fazer só uma parte: os episódios mais recentes ou um tema específico.
   - Para consultas pontuais, o `buscar.py` funciona direto sobre as transcrições, mesmo sem ficha.

---

## Fluxo A — Responder uma consulta

### 1. Entenda a que frente de negócio a pergunta pertence

Antes de buscar qualquer coisa, determine sobre que tipo de operação se está
falando. Se o projeto tem frentes distintas, identifique qual. Isto não é
formalidade: é o filtro que decide o que da base é aplicável e o que é
armadilha. Se não der para determinar, pergunte — uma linha resolve.

### 2. Procure o contra-caso primeiro

Busque nesta ordem, sempre:

1. **Quem tentou e não deu certo** — fracassos, limitações, "a gente errou"
2. **Quem discorda** — dois convidados com posições opostas valem mais que dez concordando
3. **Sob que condições funcionou** — ticket, nicho, volume, tamanho de time
4. **Só então** quem confirma

Inverter essa ordem produz resposta bajuladora. A pessoa já tem uma hipótese
quando pergunta; o valor está em testá-la, não em vesti-la de evidência.

### 3. Busque

Se a base tiver `especialistas/` (dossiês por tema, com `_README.md`), comece pelo
dossiê do tema: as seções «Onde os convidados DISCORDAM», «Lacunas» e «Transferência»
já fazem metade do trabalho. Use o dossiê como mapa e confirme na ficha ou na
transcrição antes de citar.

Comece pelas fichas (`--so-fichas`) para achar quais casos interessam, depois vá
à transcrição para o trecho literal.

```bash
python scripts/buscar.py <pasta> "termo" "variação" "sinônimo" --contexto 1
```

**Sempre use variações.** Legenda automática não tem pontuação confiável e
destrói termo técnico — "ROAS" aparece como ruas, rost, RAS, Ross; "upsell"
como opcel, opcial, opsal. Buscar um termo só produz falso negativo, e falso
negativo aqui vira "ninguém falou sobre isso", que é uma afirmação errada.

### 4. Responda

Toda afirmação vinda da base carrega **episódio + timestamp**. Sem isso a
pessoa não consegue conferir, e a base vira boato com aparência de pesquisa.

Estrutura que funciona:

- **O que a base mostra** — com citação e timestamp
- **Onde os casos divergem** — se divergem
- **Sob que condições aquilo valeu** — ticket, nicho, volume, estrutura de time
- **O que não se aplica ao caso de quem perguntou** — e por quê
- **O que a base não cobre** — dito explicitamente

### 5. Classifique a força da evidência

Diga qual dos três é, sempre:

| | Significa |
|---|---|
| **Declarado** | Alguém afirmou. Não foi verificado. É o caso da maioria esmagadora. |
| **Convergente** | Vários casos independentes, em contextos diferentes, dizem o mesmo. |
| **Verificado** | Confere com dado próprio de quem pergunta. Raro, e o mais valioso. |

Número de faturamento, margem, ROAS e conversão dito em entrevista é
**declarado**, ponto. Nunca apresente como benchmark. Quem dá entrevista tem
incentivo a arredondar para cima, e canal de podcast costuma pertencer a alguém
que vende no mesmo mercado.

---

## A regra que mais importa: transferência entre contextos

**Uma tática só transfere junto com seus pressupostos.** Antes de recomendar
qualquer coisa vinda da base, verifique se os pressupostos do case valem no
caso de quem pergunta:

| Pressuposto | Pergunta a fazer |
|---|---|
| Recompra | O cliente compra de novo, ou é transação única? |
| Custo marginal | Entregar mais uma unidade custa perto de zero, ou tem produto, frete e devolução? |
| Onde o dinheiro entra | Na venda, ou só depois de entregue e pago? |
| Unidade de diluição | A conta se faz por pedido, por entrega concretizada ou por assinatura? |
| Ticket e ciclo | Compra por impulso ou decisão longa com várias sessões? |
| Estrutura | Precisa de time comercial, closer, suporte? Existe? |

Quando os pressupostos não batem, **diga que não transfere e explique qual
pressuposto quebra.** Não adapte silenciosamente.

Este é o erro mais caro que esta skill pode cometer: pegar lógica de um modelo
de negócio e aplicar em outro porque os dois "vendem pela internet". O resultado
é conclusão errada com aparência de embasada — pior do que não ter resposta.

---

## Fluxo B — Processar material novo

### 1. Gere o esqueleto

```bash
python scripts/fichar.py <transcricao.md>          # uma
python scripts/fichar.py <pasta> --lote            # todas que ainda não têm ficha
```

Sai de graça: metadados, resumo de abertura, números declarados com timestamp,
menções e um mapa de fatias para leitura.

O **resumo de abertura** é o trecho em que o apresentador resume o episódio
antes da conversa começar. É um resumo escrito por quem viu o material inteiro.
Leia antes de qualquer coisa — ele já diz se o case vale o passe completo.

### 2. Leia e preencha

Use o mapa de fatias para ler por partes. Preencha cada `[PREENCHER]`:

| Seção | O que entra |
|---|---|
| Quem é / contexto | Nicho, tamanho, momento da operação |
| Modelo de negócio | Como entra dinheiro, onde está a margem |
| Frentes a que se aplica | Só as que de fato transferem, **com o motivo** |
| Táticas replicáveis | Tática, quando usar, timestamp |
| **Erros e contra-exemplos** | O que deu errado, o que admite ter feito mal, onde contradiz outro case |
| **Limites** | Pressupostos do case que podem não valer em outro contexto |
| Citações-chave | Curtas, sempre com timestamp |

**As duas seções em negrito são obrigatórias e nunca ficam vazias.** Se um case
parece não ter erro nem limite, você não procurou o suficiente — todo case tem,
e são a parte que a base de sucessos esconde por construção. Uma ficha só com
acertos é uma ficha que vai enviesar toda consulta futura.

### 3. Não invente

Se a transcrição não diz, a ficha não diz. Lacuna se registra como lacuna. A
legenda automática erra nome próprio e número com frequência — quando um dado
for decisivo, confira no vídeo pelo timestamp antes de fixá-lo na ficha.

---

## Limitações a declarar quando forem relevantes

- A base só tem quem deu certo e topou contar.
- Quase todo número é declarado, sem verificação.
- Quem dá entrevista costuma ter algo a vender; o canal também.
- Transcrição automática perde pontuação e erra termo técnico.
- O que funcionou num momento de mercado pode não valer hoje — cheque a data.
