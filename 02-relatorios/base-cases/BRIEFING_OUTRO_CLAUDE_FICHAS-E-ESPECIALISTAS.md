# Briefing: fichas de cases + dossiês dos 8 especialistas

Você vai fazer a **leitura pesada** de uma base de transcrições de podcasts de marketing digital: o «Scaling Secrets», do canal VTurb, com entrevistas de operações de resposta direta, VSL, tráfego pago, infoproduto e e-commerce.

Do que você produzir sai um **consultor com 8 especialistas**. A pessoa vai consultá-lo para tirar dúvidas de estratégia, mercado, campanha e modelo de negócio. Outro Claude vai usar os seus arquivos para responder. Por isso, **a qualidade aqui é a do consultor depois**.

Trabalhe em português do Brasil. Os episódios estão em português ou em inglês, conforme o episódio.

---

## 0. Onde está o material

- **Transcrições:** `C:\Users\PICHAU\Downloads\Produtividade com ia\02-relatorios\base-cases\transcricoes\vturb\*.md`
  - Uma por episódio, em blocos `**[mm:ss]** texto…`.
  - Cabeçalho com título, canal, duração, data e URL.
- **Esqueleto das fichas, já gerado:** `…\transcricoes\vturb\_fichas\<mesmo nome>.ficha.md`
  - A parte mecânica já vem preenchida: metadados, resumo de abertura do host, números declarados com o minuto, menções e o **mapa de leitura** (a transcrição fatiada em partes).
  - Você só preenche os campos `[PREENCHER]` e as seções novas descritas abaixo.
- **Índice:** `…\base-cases\INDICE.md`, com a lista dos episódios e o estado de cada ficha.

**Se você não tiver acesso a essas pastas** (por exemplo, rodando no claude.ai), a pessoa vai anexar os `.md`. Nesse caso, devolva as fichas e os dossiês como arquivos `.md` com os **mesmos nomes**, para ela colar nas pastas.

---

## 1. Etapa 1: fichar cada episódio

**Ordem:** do episódio mais recente para o mais antigo.

**Como ler:**
1. Leia primeiro o «Resumo de abertura» da ficha. É o resumo que o próprio host faz antes da conversa e já mostra se o episódio vale a leitura completa.
2. Leia a transcrição inteira, parte por parte, seguindo o «Mapa de leitura».

### 1.1 Preencha cada seção do esqueleto

| Seção | O que entra |
|---|---|
| **Quem é / contexto** | Quem é o convidado, o nicho, o tamanho declarado e o momento da operação |
| **Modelo de negócio** | Como entra dinheiro: infoproduto, COD, e-commerce pré-pago, assinatura, low ticket, high ticket, mentoria, SaaS. Onde está a margem. Ticket. Onde fica a recompra, se houver |
| **Frentes a que se aplica** | Marque só as que de fato transferem, **com o motivo**: «infoproduto VSL», «COD/pagamento na entrega», «venda 1-a-1 por WhatsApp (pós-pago)», «e-commerce pré-pago» |
| **Táticas replicáveis** | Tabela `tática | quando usar / condição | timestamp`. Só o que é **acionável**: nada de frase motivacional |
| **Erros, fracassos e contra-exemplos** ⚠️ obrigatório | O que deu errado, o que o convidado admite ter feito mal, onde ele contradiz outro convidado ou o senso comum. **Nunca deixe vazio.** Todo case tem erro: se não achou, leia de novo |
| **Limites: onde NÃO se aplica** ⚠️ obrigatório | Pressupostos do case que podem não valer para outra operação: ticket, recompra, custo de produto, frete, país, time, verba, momento do mercado |
| **Citações-chave** | 3 a 6 frases curtas, literais, **sempre com timestamp** |

### 1.2 Acrescente ao final da ficha esta seção nova

```
## Especialistas (tags)
| Especialista | Trechos (timestamps) | O que este episódio contribui (1–2 linhas) |
|---|---|---|
| E1 Mercados/países/ofertas | 12:30, 47:10 | … |
| E3 Campanha/tráfego | 1:05:20 | … |
```

Use só os especialistas que o episódio realmente alimenta (veja a lista na seção 2). Um episódio costuma cair em 2 a 4 deles.

### 1.3 Regras da ficha (não negociáveis)

1. **Não invente nada.** O que a transcrição não diz, a ficha também não diz. Lacuna vira o texto «não dito no episódio».
2. **Todo número citado é declarado:** faturamento, ROAS, CPA, conversão, verba. Escreva «declarado» e o timestamp. Nunca apresente como benchmark.
3. **A legenda automática erra termos técnicos** («ROAS» vira «ruas», «upsell» vira «opcel», nomes próprios aparecem errados). Corrija o termo quando o contexto deixar óbvio e marque `(termo corrigido)`. Na dúvida, mantenha o original e escreva `(?)`.
4. **Timestamp em toda afirmação relevante,** no formato `mm:ss` ou `h:mm:ss`.
5. **Seja conciso:** a ficha tem 1 a 2 páginas. Ninguém vai reler uma ficha de 10 páginas.
6. Ao terminar cada ficha, salve o arquivo por cima do esqueleto. Não mude o nome.

---

## 2. Os 8 especialistas

| Código | Especialista | O que ele cobre |
|---|---|---|
| **E1** | **Mercados, países e ofertas** | Quais mercados e nichos estão abertos ou saturados, países e idiomas, ticket, sazonalidade, tipo de oferta (front, bump, upsell, kit), o que foi lançado e escalou |
| **E2** | **Modelo de negócio** | Infoproduto, COD, e-commerce, assinatura, recorrência, low e high ticket, margem, LTV, unit economics, sócio e estrutura societária, reinvestimento |
| **E3** | **Estrutura de campanha e tráfego** | Meta e as outras fontes (TikTok, Google/YouTube, Native/Taboola/NewsBreak, Pinterest); CBO/ABO; bid e cost cap; teste e escala; volume de verba; atribuição e tracking; públicos; Andromeda e Advantage+ |
| **E4** | **Criativo e copy** | Ganchos, VSL (estrutura, duração, lead), formatos, ângulos, volume de criativos por semana, UGC, roteiros, edição, o que satura |
| **E5** | **Funil e conversão** | Página, advertorial, quiz, checkout, order bump, upsell/downsell, back-end, e-mail, SMS, call center e WhatsApp, taxa de conversão, recuperação, reembolso |
| **E6** | **Operação e time** | Contratação, funções, processos, ferramentas e softwares, gestão, rotina, terceirização, escala de equipe |
| **E7** | **Riscos operacionais** | Bloqueio e queda de conta, BM e contingência, gateway e processamento, chargeback e reembolso como risco, compliance de anúncio e de oferta, dependência de uma fonte só. (Erros gerais de cada tema ficam na seção de contra-casos do dossiê daquele tema.) |
| **E8** | **IA e automação na produção** | Ferramentas de IA citadas (texto, imagem, vídeo, voz, avatar, edição), em que etapa entram (pesquisa, copy, criativo, VSL, atendimento, análise), automações de subida e relatório, ganho de volume e custo declarados, onde a IA piorou o resultado |

---

## 3. Etapa 2: montar os dossiês dos especialistas

Comece **depois de fichar todos os episódios** ou, se o crédito acabar no meio, com o que estiver pronto.

Para cada especialista, crie `…\base-cases\especialistas\E<n>_<nome>.md` com esta estrutura:

```
# E<n> · <Nome do especialista>
Base: <N> episódios (lista de códigos #NNN) · atualizado em <data>

## Em 10 linhas (o que a base diz)
- …

## Teses e práticas (agrupadas por subtema)
### <Subtema, ex.: "Bid cap vs cost cap">
- **O que dizem:** … — #172 (12:30), #168 (45:10)
- **Condição em que vale:** ticket / nicho / verba / país
- **Força da evidência:** declarado (1 caso) | convergente (3+ casos independentes)

## Onde os convidados DISCORDAM
| Tema | Posição A (quem, #ep, ts) | Posição B (quem, #ep, ts) | Por que divergem (contexto diferente?) |

## Números declarados (NÃO são benchmark)
| Métrica | Valor | Contexto (nicho, país, ticket) | #ep · ts |

## O que deu errado / riscos (contra-casos)
- …

## Lacunas: o que a base NÃO cobre
- …

## Transferência para outros modelos de negócio
- **Infoproduto VSL:** o que transfere e o que não
- **COD / pagamento na entrega:** o que transfere e o que não (lembre que o dinheiro só entra se o pedido é entregue e pago, e que há produto, frete e devolução)
- **Venda 1-a-1 pós-paga por WhatsApp:** idem
```

### 3.1 Regras do dossiê

- **Toda frase do dossiê aponta para episódio e timestamp.** Sem isso, ela vira boato.
- **A seção «Onde discordam» é a mais valiosa.** Busque ativamente os conflitos. Dez convidados concordando valem menos do que dois em lados opostos.
- **Use as categorias de evidência certas:**
  - **convergente:** vários casos independentes, em contextos diferentes;
  - **declarado:** um só caso;
  - nunca escreva «comprovado».
- **Viés de sobrevivente:** a base só tem quem deu certo e topou falar, e o canal (VTurb) vende ferramenta para esse mercado. Diga isso no topo de cada dossiê, em 1 linha.
- **Tamanho:** 3 a 8 páginas por especialista. Prefira listas e tabelas.

---

## 4. Também atualize

- **`…\base-cases\INDICE.md`:** na coluna «Ficha», troque «esqueleto» por «preenchida» nos episódios que você terminou. Se tiver Python, rode `python ".claude/skills/consultor-de-cases/scripts/alimentar.py" "02-relatorios/base-cases" --so-indice` a partir da pasta do projeto.
- **`…\base-cases\especialistas\_README.md`:** a lista dos 8 dossiês, com quantos episódios cada um cobre e a data.

---

## 5. Ao terminar (ou se o crédito acabar)

Responda em português, curto:

1. Quantas fichas foram preenchidas e quais ficaram faltando (nº dos episódios).
2. Quais dossiês ficaram prontos e quais ficaram parciais.
3. Os 5 achados mais interessantes da base, com episódio e timestamp.
4. Os pontos em que a transcrição estava ruim demais e algo precisa ser conferido no vídeo.

**Se o crédito acabar no meio:** salve o que já estiver pronto. Uma ficha completa vale mais do que três pela metade. Termine a ficha atual antes de começar outra.
