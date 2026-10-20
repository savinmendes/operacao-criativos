# Bid Cap no Meta Ads — achados e prompt para o agente de anúncios
**03/10/2026 · base: 27 vídeos transcritos, 69.905 palavras**

---

## Como esta base foi montada

Busquei no YouTube por sete consultas em português e inglês, achei **51 candidatos**
com mais de 3 minutos e data identificável, e transcrevi **27** antes de parar. Os
24 restantes não tinham legenda e cada um exigia vários minutos de GPU — o custo
por vídeo adicional deixou de pagar, porque os achados pararam de se mover.

**Duas coisas que você pediu e eu não consegui entregar:**

**"Bem avaliados / comentários positivos"** não é medível. O YouTube removeu a
contagem pública de dislikes em 2021 e oculta likes em boa parte dos vídeos. Usei
**visualizações e recência** como critério, o que é outra coisa.

**"Pontos irrefutáveis que viram certeza"** não existem nessa base. Encontrei um
ponto estrutural com forte convergência e uma contradição numérica grave. Chamar
isso de certeza seria mentir sobre a qualidade da evidência.

---

## Achado 1 — a contradição que invalida copiar número de vídeo

Todos ancoram o lance no **ticket**. Nenhum usa valor absoluto. Mas o multiplicador
varia 4×:

| Prescrição | Lance ÷ ticket |
|---|---|
| "50% do ticket para validar cada criativo" | **0,50×** |
| "limite de lance de 61% do seu ticket" | **0,61×** |
| ticket R$ 30 → bidcap R$ 25 | **0,83×** |
| ticket R$ 80 → bid R$ 88 | **1,10×** |
| "recebe R$ 100 por venda, coloca lance R$ 200" | **2,00×** |
| "coloquei duas vezes o ticket do meu produto" | **2,00×** |

Seguir o vídeo errado erra o lance em 4×. **Não há denominador comum numérico.**

O denominador comum é de **método**: ancore na sua própria economia. É isso que
todos fazem — cada um com o número da conta dele.

---

## Achado 2 — um terço do conteúdo é sobre outra coisa

Contei menções dentro da transcrição, não no título:

**7 dos 27 vídeos ensinam cost cap, não bid cap.** Um deles diz "cost cap" 32 vezes
e "bid cap" uma. Outro, 26 contra zero.

São mecânicas diferentes:

| | Bid cap | Cost cap |
|---|---|---|
| O que limita | O lance máximo em **cada leilão** | O custo **médio** por resultado |
| Pode estourar o alvo num leilão? | Não | Sim |
| Entrega | Mais restrita | Mais livre |

Quem aplica um achando que é o outro tem resultado inexplicável. Isso sozinho
explica parte de "não funciona comigo".

---

## Achado 3 — o que o campo cobre e o que ignora

| Conceito | Em quantos vídeos |
|---|---|
| CPA alvo | 24/27 · **89%** |
| Ticket | 17/27 · 63% |
| Leilão | 15/27 · 56% |
| Estabilizar resultado | 13/27 · 48% |
| Duplicar conjunto | 10/27 · 37% |
| Baixa entrega / não gasta | 9/27 · 33% |
| Margem | 8/27 · 30% |
| Subir orçamento | 6/27 · 22% |
| Criativo vencedor | 5/27 · 19% |
| **Fase de aprendizagem** | **3/27 · 11%** |

A fase de aprendizagem é o ponto onde lance limitado mais interfere no algoritmo,
e **89% do conteúdo não toca no assunto**. Esse número eu refiz depois de corrigir
uma falha no meu próprio filtro de busca — na primeira passada ele deu 1/21 por erro
meu, não por ausência do tema.

**Ressalva de medição:** meu filtro para "subir o lance" retornou zero, mas eu
encontrei pelo menos uma prescrição desse tipo por outro caminho. O filtro falhou.
Não trate "ninguém fala de X" como achado onde eu não confirmei manualmente.

---

## Achado 4 — as três regras de condução que apareceram

São as únicas prescrições sobre o que fazer **depois** de ligar a campanha. Cada
uma apareceu **uma vez**. São hipóteses, não consenso:

- Campanha não gasta, com 15+ criativos no ar → subir o lance 10% por dia
- Escalar orçamento → aumentar de 30% em 30%
- Custo acima do alvo → baixar 20 a 30%

---

# PROMPT PARA O AGENTE DE ANÚNCIOS

Copie daqui para baixo.

---

Você vai configurar e conduzir campanhas de **bid cap** (limite de lance) no Meta Ads
para infoproduto. Siga este documento como regra operacional.

## 1. Antes de qualquer coisa: bid cap não é cost cap

- **Bid cap / limite de lance** limita quanto a conta paga em **cada leilão**.
  Nunca ultrapassa o valor. Entrega mais restrita.
- **Cost cap / meta de custo por resultado** mira um custo **médio**. Pode pagar
  mais num leilão e compensar em outro. Entrega mais livre.

Se o objetivo é **previsibilidade de custo por venda**, é bid cap. Se é **volume com
custo médio controlado**, é cost cap. Nunca descreva um usando a lógica do outro, e
se a instrução recebida misturar os dois, pare e peça esclarecimento.

## 2. O lance sai da economia da oferta, nunca de um número copiado

**Não use multiplicador padrão.** A referência de mercado varia de 0,5× a 2× o
ticket — uma dispersão de 4× que torna qualquer valor emprestado inútil.

Derive assim, nesta ordem:

1. **Estabeleça o CPA máximo** — o custo por venda acima do qual a oferta dá
   prejuízo. Para infoproduto: ticket do front menos taxa de plataforma, menos
   custo de entrega/suporte, menos reembolso esperado. Se houver upsell com taxa
   de aceite medida, inclua a contribuição dele.
2. **Estabeleça o CPA alvo** — o CPA máximo menos a margem que você quer reservar.
3. **O lance inicial é o CPA alvo.** Não o máximo: o alvo. O máximo é onde o
   resultado zera, não onde ele serve.

Se o CPA máximo não estiver disponível, **pare e peça**. Não arbitre lance sem ele —
é o único número que separa configuração de aposta.

## 3. Diagnóstico por sintoma

**Campanha não gasta ou entrega muito pouco.** O lance está abaixo do que o leilão
cobra por aquele público. Três causas possíveis, nesta ordem de verificação:
público pequeno demais, criativo sem tração, lance realmente baixo. Só mexa no
lance depois de descartar as duas primeiras — subir lance para compensar criativo
ruim é comprar o problema mais caro.

Se for mesmo o lance: suba em passos de 10% ao dia, não de uma vez. *(Prescrição
observada em 1 fonte apenas — trate como hipótese e meça.)*

**Custo acima do alvo com entrega normal.** Baixe o lance em 20 a 30% e observe
antes de mexer de novo. *(1 fonte.)*

**Resultado instável dia a dia.** Comportamento esperado com volume baixo por
conjunto. Não reaja a um dia ruim: avalie em janela que acumule pelo menos algumas
dezenas de conversões.

## 4. Escala

Suba orçamento em incrementos de cerca de 30%, não dobrando. *(1 fonte.)*

Ao escalar, mexa em **uma variável por vez** — orçamento ou lance, nunca os dois
juntos. Com os dois ao mesmo tempo é impossível saber qual causou a mudança.

## 5. Dois pontos onde não existe referência confiável

Avise o operador quando a decisão cair aqui:

**Fase de aprendizagem.** Lance limitado interage diretamente com ela, e 89% do
material consultado não aborda o tema. Não há prática validada para copiar.
Qualquer regra sobre reiniciar aprendizado com bid cap é suposição.

**Condução pós-estabilização.** O material cobre bem como ligar a campanha e quase
nada sobre conduzi-la depois. Decisões nessa etapa são do operador, com os dados
da conta dele.

## 6. Como relatar

Ao propor qualquer alteração, informe:
- qual variável muda e em quanto
- qual número da conta justifica (CPA atual contra CPA alvo)
- o que você espera que aconteça e em quanto tempo
- qual resultado faria você reverter

Nunca apresente como regra estabelecida algo que veio de uma fonte só. Diga
"prescrição isolada, não validada" quando for o caso.

---

## Limitações desta base

- **27 de 51 vídeos.** Os 24 restantes ficaram de fora por custo de transcrição,
  não por irrelevância.
- **Nenhum criador mostra teste controlado.** Todos apresentam resultado de conta
  própria, sem grupo de comparação. Convergência entre eles é evidência fraca:
  esses criadores se assistem e vendem curso.
- **Contexto misto.** Parte do material é de e-commerce/dropshipping, com ticket e
  recompra diferentes de infoproduto. Onde a origem não estava clara, não atribuí.
- **As transcrições vieram de legenda automática e Whisper.** Número falado pode
  sair errado. Os valores da tabela de multiplicadores eu conferi na frase de
  origem; os demais, não.

Transcrições em `01-arquivos-organizados/transcricoes-bidcap/`.
