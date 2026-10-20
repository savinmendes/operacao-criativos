# Revisão independente: lote B (ADs 04, 07, 08, 09, 10, 15, 16, 17 e 18), 08/10/2026

Sou o revisor independente: não editei nenhum vídeo nem arquivo de trabalho. Tudo o que gerei está em `_trabalho\revisao\loteB\`. O AD 06 ficou de fora porque ainda não tem `ad06\RELATORIO.md` (o .mp4 existe, mas a produção não fechou).

## Resumo

| Vídeo | Veredito | Motivo principal |
|---|---|---|
| AD 04 - ENVIDIA | **APROVADO** (com observações) | Conjunto 0,29. O w12 dá 0,66 na minha conta (0,58 no kit), mas a boca fica fechada nas pausas. Gancho de perfil conferido na folha. |
| AD 07 - CINTA-BLANCA | **APROVADO** (com observações) | Conjunto 0,20. Só a tomada final (88,3–89,5 s) passa de 0,6: boca entreaberta e parada depois do "ahora", sem articular PT. |
| AD 08 - BENDICION-DETENIDA | **REPROVADO** | Em 18,13–18,53 s (12 q) a boca do final é **idêntica à do original**, que está falando PT, enquanto o ES está calado. Correção pequena. "hoy" em 86,4 s. |
| AD 09 - SERPIENTES | **REPROVADO** | Em 46,93–47,07 s (5 q, fim do E1) a boca abre e mostra os dentes **igual ao original**, que fala PT, numa pausa do ES. Correção pequena (sem crédito). |
| AD 10 - NUDO (hospital) | **REPROVADO** | Lipsync aprovado (conjunto 0,13). Reprovado pela **imagem**: idoso entubado no leito de hospital, com monitor e oxigênio, de 0 a 9,3 s, sob "Vine a traer paz a tu corazón". Lê como cura pela fé. Risco alto no Meta. |
| AD 15 - REGALO | **APROVADO** | Conjunto 0,24. O s2 está no limite (0,60), mas a pausa final é um sorriso parado, sem articular. |
| AD 16 - NUDO | **REPROVADO** | Mantém **"Pero sé rápido"** (78,4 s), que o AD 13 está tirando. Para ficar consistente, sai aqui também. Há ainda 3,3 s sem fala logo depois (78,9–82,2 s). Lipsync aprovado (conjunto 0,15). |
| AD 17 - NUDO (quarto) | **REPROVADO** | Lipsync aprovado (conjunto 0,10). Reprovado pela **imagem com a fala**: frascos de remédio na mesa, homem chorando com a mão no rosto, e "Vine a traer **alivio** a tu corazón" (0–9 s). Risco médio no Meta, correção barata. |
| AD 18 - SERPIENTES | **APROVADO** | Conjunto 0,16, todos os trechos ≤ 0,37. O flash branco no lugar do light-leak ficou limpo. |

**Consistência sobre urgência:** marquei como defeito só o "sé rápido", porque é pressão de prazo e o AD 13 está sendo corrigido por isso. "Pocos segundos", "30 segundos" e "segundos" não aparecem em nenhum dos 9. "No dejes pasar este momento" e "No lo dejes para después" são urgência suave sem prazo: aceitei, no nível do lote A. O mesmo vale para "Hay quien no quiere…" e "El enemigo no quiere…", que estão no nível do AD 11/13 aprovados.

## Método (o mesmo do lote A, refeito no vídeo FINAL)

1. **Voz ES isolada do final** com demucs (`audio\sep\htdemucs\fin_NN\vocals.wav`). A voz PT vem do demucs do original, cortado na duração do final mais 2 s.
2. **Tempo do final = tempo do original** em todos os ADs. Conferi com `alinh.py` (MAE de quadros reduzidos, com busca de deslocamento; o melhor deslocamento é 0 em todos). As exceções são as aberturas refeitas do 16 (reenquadrada) e do 08 (coberta).
3. **Varredura quadro a quadro** (`varrer.py` → `faces_NN.jsonl`) e **rosto de quem fala por trecho** (`analisar.py` → `met_NN.txt`). Os trechos vêm dos relatórios (`segs_B.json`).
   - Corrigi a escolha do rosto: a medida "mudou" (pixels) dá 0 % em todos os rostos neste lote, como já se viu no lote A. No AD 18 o script pegou o Jesus em 8 trechos. Passei a preferir o rosto à direita, que é o da mulher, e conferi a escolha nas folhas.
4. **Índice de pausa** pela conta do kit (pico − 30 dB; pausas ≥ 8 q, sem 2 q de cada borda). Nos trechos sem pausa longa, uso também o índice com pausas ≥ 4 q.
5. **Folhas de boca** (`folha.py`): de 3 em 3 quadros nos trechos de aviso e de 1 em 1 nas pausas suspeitas. Final em cima, original embaixo; barra verde = voz ES, vermelha = voz PT.
   - O `folha.py` ganhou uma trilha linear de posição (para o perfil da menina do 04 e o close do 08).
   - **Folhas de transição** (`trans.py`), de 1 em 1 quadro, final × original.
6. **`revisar_ad.py`** pelo PowerShell (`rodar_revisar.ps1`), com os proibidos do briefing e mais "rápido, pocos, minuto, salud, dolor, sanar, milagro, enfermo, hospital, hoy, noche". As saídas estão em `loteB\revisar\`.
   - **Atenção, falha do script:** passados por um `.ps1` sem BOM, os termos **acentuados** ("rápido", "depósito", "cáncer") chegam corrompidos ao Python e **não são achados**. Por isso o "sé rápido" do AD 16 não foi acusado. Conferi esses termos lendo as transcrições.
7. **Áudio:** `ebur128` e `silencedetect` a −55 dB / 0,5 s. Nenhum silêncio absoluto em nenhum vídeo. Todos ficam entre −15,1 e −15,2 LUFS, com LRA de 1,6 a 3,4.

---

## AD 04: APROVADO (com observações)

**Lipsync** (`met_04.txt`):

| Trecho | Tempo | Índice | Obs. |
|---|---|---|---|
| g1 (menina de perfil) | 0–9,67 | não medível (o MediaPipe não acha perfil) | `f04_g1.jpg`: a boca do final difere do original e fecha nas pausas do ES (3,8–4,0, 6,7–6,8 e 7,8 s) enquanto o PT fala. Aceito. |
| w1 | 9,77–17,43 | ≥ 4 q: 0,45 | articula diferente do original |
| w2 (coberto) | 17,43–20,07 | — | zoom na invejosa, **boca fechada e calada** (`f04_w2w3.jpg`). OK. |
| w3 / w4 | 20,07–27,00 | ≥ 4 q: 0,30 / 0,26 | |
| w5 a w11 | 27,00–76,53 | 0,49 / 0,30 / 0,08 / 0,04 / 0,10 / 0,09 / 0,42 | |
| **w12** | 76,53–83,10 | **0,66** (kit 0,58) | `f04_w12.jpg`: nas pausas (76,5–76,8, 78,6–78,8 e 82,4–83,0 s) a boca fica fechada ou entreaberta, sem articular, e o original mostra os dentes. O índice sobe porque a fala ES abre pouco a boca. Mesma situação do c1 do AD 05 no lote A: não reprovo. |
| **Conjunto** | | **0,29** | |

- **Pausa com boca aberta:** w6, 36,43–36,87 s (`f04_w6_pausa.jpg`). Os lábios ficam entreabertos e parados, enquanto o original articula. Não é PT. Baixa.
- **Fala:**
  - es (1,00), nenhum proibido, o texto bate com o roteiro;
  - "La semana pasada, un hombre… sintió una paz y una esperanza" é depoimento só emocional, no nível do AD 13.
- **Áudio:** −15,2 LUFS. O fim fica 0,7 s depois da fala, com fade.
- **Imagem:**
  - sem legenda PT nem moeda;
  - os anjos substituem o carro;
  - o "quadro solto" em 9,67/9,77 s é **falso positivo**: é o clarão do original, igual quadro a quadro (`t_0410.jpg`).
- **CTA:** as setas vão de 70,15 s ao fim, abaixo da legenda e longe da boca.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 76,53–83,10 (w12) | Índice 0,66 na minha conta (> 0,6), mas sem PT visível. | Baixa | Opcional: `fechar.py` nas pausas 76,5–76,8 e 82,4–83,0 s (sem crédito). |
| 2 | 0–9,67 (g1) | Lipsync de perfil, só conferível a olho. | Baixa | Assistir. |

## AD 07: APROVADO (com observações)

**Lipsync** (`met_07.txt`; a Desatadora; o Jesus fica calado):

| Trecho | Índice |
|---|---|
| s01 | 0,03 |
| s02 | 0,11 |
| s03 | 0,03 |
| s04 | ≥ 4 q: 0,12 |
| s05 | 0,13 |
| s06 | 0,03 |
| s07 | ≥ 4 q: 0,23 |
| s08 | 0,41 |
| s09 | 0,14 |
| s10 | 0,26 |
| s11 | 0,32 |
| **s12** (88,29–89,50) | **2,07** |
| **Conjunto** | **0,20** |

- **s12** (`f07_s12.jpg`, `f07_s12_fim.jpg`):
  - durante o "ahora" (88,1–88,6 s) a boca articula;
  - depois da última fala, de 88,67 s ao fim, ela fica **entreaberta e parada**, enquanto o original fala PT ("O" bem aberto). Não segue o PT, mas parece congelada por 0,8 s, sob o fade;
  - o índice alto vem daí.
- **Início** (`f07_ini.jpg`): 0–0,13 s é um quadro parado do s01, com a boca fechada. OK.
- **Fala:**
  - es (0,99), nenhum proibido, o texto bate com o roteiro;
  - "La última mujer… despertó con una paz en el corazón" é depoimento emocional (nível do AD 13);
  - "te quita el sueño" é preocupação, não saúde. Aceito.
- **Áudio:** −15,1 LUFS, nenhum silêncio.
- **Imagem e CTA:** sem legenda PT. As setas vão de 70,4 s ao fim, abaixo da legenda.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 88,67–89,50 | Boca entreaberta parada depois da fala. | Baixa | Opcional: cortar o vídeo em ~89,0 s, com fade mais curto, ou fechar a boca. |

## AD 08: REPROVADO

**Lipsync** (`met_08.txt`):

| Trecho | Índice | Obs. |
|---|---|---|
| s01 (0–9,53) | — | **coberto**: zoom nas mãos e nas serpentes, **nenhum rosto** (as 2 "detecções" em 2,2 e 4,9 s são falsas, em mãos e cobras; conferido). OK. |
| **s02** (9,77–19,47) | **0,60** (limite) | ver defeito 1 |
| s03 | 0,23 | |
| s04 | 0,25 | |
| s05 | ≥ 4 q: 0,33 | |
| s06 | 0,46 | |
| s07 | ≥ 4 q: 0,14 | |
| s08 (close, 51,63–55,13) | ≥ 4 q: 0,35, medido no rosto certo | `f08_s08.jpg`: a boca é diferente da original e articula |
| s09 a s16 | 0,26 / 0,42 / 0,07 / 0,08 / 0,08 / 0,46 / 0,11 / 0,12 | |
| **Conjunto** | **0,27** | |

- **Defeito principal** (`f08_s02_pausa.jpg`, de 1 em 1 quadro):
  - em **18,13–18,53 s** o ES está calado e o PT fala;
  - a boca do final é **quadro a quadro igual à do original**: abre o sorriso com os dentes e vai fechando, acompanhando a fala PT;
  - é a boca original vazando (o "sorriso com dentes" do relatório). Na dúvida sobre o lipsync, reprovo.
- **Outras pausas:**
  - s03 21,47–21,70 s e s10 71,80–72,03 s: lábios entreabertos, sem articular. Baixa;
  - 12,4–12,8 e 15,5–15,8 s: boca fechada. OK.
- **Os 20 quadros com a boca do quadro vizinho:** nas folhas de 3 em 3 quadros do s02 e do s07–s08 não aparece borrão, salto nem boca duplicada. Não dá para garantir os 20 um a um sem a lista de quadros. Na folha, nada visível.
- **Clarão refeito** (`t08_clarao.jpg`): fusão rosada e branca de 9,47 a 9,77 s, sem resto de legenda PT. O rosto dela só aparece lavado de luz, já no 1º quadro com lipsync. OK.
- **Fala:**
  - es (0,99), o texto bate com o roteiro;
  - **"el que más aprieta tu vida hoy" (86,4 s)**: hora do dia, que o lote tirou dos outros ADs (09, 18). Baixa.
  - "sin ese peso en el pecho" é idiomático. Aceito, como no 09 e no 16.
- **Áudio:** sem silêncio. **CTA:** as setas vão de 76,8 s ao fim. Imagem sem legenda PT.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 18,13–18,53 (s02) | Boca original (PT) numa pausa do ES, 12 q. | **Média/alta** (regra "nenhum quadro com boca PT") | O `fechar.py` deixou fantasma. Alternativas: (a) refazer só 17,5–19,47 s no HeyGen speed (~2–3 créditos); (b) encurtar a pausa do ES; (c) repetir quadros de boca fechada do próprio s02 (12,5–12,8 s), alinhados por olhos e nariz. Medir de novo. |
| 2 | 86,4 | "hoy". | Baixa | Tirar o "hoy" (TTS curto + refazer o s14) ou aceitar. |

## AD 09: REPROVADO

**Lipsync** (`met_09.txt`):

| Trecho | Índice |
|---|---|
| m0 (espelho) | 0,15 |
| A | 0,10 |
| B | 0,17 |
| C | 0,10 |
| D | 0,02 |
| **E1** | **0,60** |
| E2 | 0,06 |
| F | 0,33 |
| G | 0,14 |
| H | 0,03 |
| I | ≥ 4 q: 0,09 |
| J | 0,04 |
| K | ≥ 4 q: 0,07 |
| L | 0,06 |
| M | 0,22 |
| N | 0,03 |
| O | sem pausa |
| P | 0,04 |
| **Conjunto** | **0,16** |

- **E1, defeito** (`f09_E1_pausa.jpg`):
  - em **46,93–47,07 s** o ES está calado e o PT fala;
  - a boca abre e mostra os dentes de cima **igual ao original**, por 5 quadros, logo antes da emenda E1|E2 (47,12 s).
  - As outras pausas do E1 (42,0–42,3 e 43,7–44,0 s) estão fechadas (`f09_E1.jpg`).
- **O** (99,33–100,67): a correlação ES é baixa (0,07), mas a folha `f09_NOP.jpg` mostra a boca articulando diferente do original e fechada na pausa de 98,6–99,2 s. OK.
- **Fora do lipsync:** só a transição com brilho de 8,33–8,83 s, sem fala.
- **Fala:**
  - es (0,98), nenhum proibido, o texto bate com o roteiro;
  - "tu corazón descansa sin ese peso en el pecho" é idiomático. Aceito.
- **Áudio:** −15,1 LUFS, sem silêncio.
- **Imagem e CTA:** sem legenda PT. As setas vão de 80,6 s ao fim. A mancha leve das setas antigas fica atrás da legenda (já anotada).

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 46,93–47,07 (fim do E1) | Boca original (PT) abrindo numa pausa do ES, 5 q. | Média (regra "nenhum quadro com boca PT") | Sem crédito: colar nesses 5 quadros a boca fechada de 46,77–46,90 s (`fechar.py`) ou adiantar 4 quadros a fusão E1|E2. Medir o E1 de novo. |

## AD 10: REPROVADO (imagem)

**Lipsync** (`met_10.txt`):

| Trecho | Índice |
|---|---|
| h0 | 0,08 |
| A | 0,28 |
| B | 0,05 |
| C | 0,37 |
| D | 0,08 |
| E | 0,10 |
| F | 0,14 |
| G | ≥ 4 q: 0,03 |
| H | ≥ 4 q: 0,37 |
| I | 0,09 |
| J | ≥ 4 q: 0,05 |
| K | 0,16 |
| L | 0,03 |
| **Conjunto** | **0,13** |

- Nenhuma pausa com a boca aberta. O C (`f10_C.jpg`) fecha nas 4 pausas. Lipsync aprovado.
- **Fala:** es (0,98), nenhum proibido, o texto bate com o roteiro. Nada de cura, dinheiro ou contagem.
- **Áudio:** −15,1 LUFS, sem silêncio.
- **CTA:** as setas vão de 73,6 s ao fim. No close (85–87 s) a legenda fica no pescoço, fora da boca.
- **"Quadro solto" em 9,63/9,80 s:** falso positivo. É a transição com brilho do original, igual quadro a quadro (`t_0410.jpg`).
- **Imagem: cena do hospital, 0–9,33 s.**
  - Mostra: idoso entubado, cânula de oxigênio, monitor cardíaco, a personagem com a mão na cabeça dele e o rosário.
  - Com "Vine a traer paz a tu corazón y a desatar el nudo que detiene tu vida", o gancho comunica **cura pela fé** sem dizer a palavra.
  - **Risco Meta: alto.** A política de saúde e de alegações milagrosas olha a imagem, não só o texto. Doente em UTI no gancho de um produto de oração é o padrão que a revisão do Meta pega.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 0–9,33 | Cena de hospital (idoso entubado, monitor) que sugere cura. | **Alta** (compliance) | Sem crédito: reenquadrar o próprio plano só na personagem, como no AD 16. Um recorte de ~360x640 em torno dela, no alto à direita, ampliado 2x, tira o leito, o monitor e o idoso. O lipsync já feito continua valendo, porque é a mesma boca. Se o recorte ainda mostrar o leito, cobrir com outra tomada da Desatadora (mantendo o áudio) ou gerar uma abertura nova, o que exige lipsync. |

## AD 15: APROVADO

- **Lipsync** (`met_15.txt`):
  - s1 0,04; **s2 0,60** (limite); s3 0,02; conjunto **0,24**;
  - s2 (`f15_s2.jpg`, `f_pausas.jpg`): a pausa de 11,0–11,2 s fecha;
  - na de 13,17–13,43 s ela fica num sorriso parado, igual ao original, mas **o original também não articula** ali. Aceito, como o c1 do AD 05.
- **Fala:** es (1,00), nenhum proibido, o texto bate com o roteiro. É corrida, mas inteligível no whisper.
- **Áudio:**
  - −15,2 LUFS, sem silêncio;
  - o fim fica ~0,4 s depois do "ahora", com fade. Curto, mas não corta a palavra.
- **Imagem:** sem legenda PT, e a seta vermelha antiga saiu.
- **CTA:** as setas vão de 11,25 s ao fim, abaixo da legenda e fora da boca.
  - A detecção do `revisar_ad` (y 761–1183) inclui a túnica vermelha. Na folha, as setas estão em ~y 1110–1180. Falso positivo.
- **Defeitos:** nenhum que impeça.

## AD 16: REPROVADO

**Lipsync** (`met_16.txt`):

| Trecho | Índice |
|---|---|
| a1 | 0,24 |
| b1 | 0,40 |
| c1 | 0,05 |
| c2 | 0,24 |
| d1 | 0,25 |
| e1 | 0,06 |
| f1 | 0,03 |
| g1 | sem pausa |
| h1 | 0,06 |
| i1r | ≥ 4 q: 0,72 |
| **j1** | **0,61** |
| k1 | 0,08 |
| l1 | 0,05 |
| **Conjunto** | **0,15** |

- **j1** (`f16_j1_pausa.jpg`): em 76,20–76,47 s a boca fecha devagar depois do "nudo". É diferente do original, sem articular PT. Baixa.
- **i1r** (`f16_i1j1.jpg`):
  - a correlação é fraca (0,17), mas a boca articula diferente do original;
  - na micropausa de 71,9–72,1 s fica entreaberta, sem PT.
  - Qualidade de lipsync mediana: vale assistir.
- **a1** (abertura reenquadrada, `f16_a1.jpg`): articula na fala. Na pausa de 4,7–6,7 s os lábios ficam entreabertos e parados. Baixa.
- **Fala:**
  - es (0,98), o texto bate com o roteiro;
  - **"Pero sé rápido" em 76,44–78,94 s** (a frase "…una para cada nudo, pero sé rápido"). O `revisar_ad` não acusou por causa do acento (ver Método).
- **Áudio:**
  - −15,1 LUFS, nenhum silêncio absoluto (há o fundo musical);
  - **pausa de fala de 3,3 s em 78,9–82,2 s**, logo depois do "sé rápido", e outra de 2 s em 4,7–6,7 s. Soa como buraco no ritmo.
- **Imagem:**
  - **abertura reenquadrada (0–9,7 s):** a cadeira de rodas saiu. Fica a mulher com a mão na cabeça de um idoso, no meio da multidão, o que lê como bênção ou imposição de mãos;
  - **risco Meta: baixo/médio**, aceitável. Bem menor que o hospital do AD 10 e sem nenhuma palavra de cura;
  - a fusão em 9,73–9,93 s está limpa (sem quadro solto). O tom roxo em 9,40 s é do original.
- **CTA:** as setas vão de 70,45 s ao fim, abaixo da legenda.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | ~78,0–78,9 | "Pero sé rápido": pressão de prazo, mesmo critério do AD 13. | **Média** (consistência do lote) | Tirar a frase do áudio e aproveitar para encurtar a pausa de 78,9–82,2 s (puxar o b14 para ~79,3 s). A boca do j1 ainda articula o "sé rápido", então é preciso refazer o j1 (75,97–78,80 s, ~3 créditos speed) ou fechar a boca nesses quadros (`fechar.py`). Remontar e medir. |
| 2 | 78,9–82,2 | 3,3 s sem fala. | Baixa/média | Sai junto com o item 1. |

## AD 17: REPROVADO (imagem + fala da abertura)

**Lipsync** (`met_17.txt`):

| Trecho | Índice |
|---|---|
| s00 | 0,09 |
| s02 | 0,31 |
| s03 | 0,05 |
| s04 | 0,10 |
| s05 | 0,07 |
| s06 | 0,06 |
| s07 | 0,12 |
| s08 | 0,04 |
| s09 | sem pausa |
| s10 | 0,05 |
| s11 | 0,06 |
| s12 | 0,19 |
| **Conjunto** | **0,10** |

- **Fim do s00** (`f17_s00fim.jpg`): de 9,00 a 9,33 s a boca fica fechada enquanto o original ainda fala. Bom.
- **s09** (`f17_s08s09.jpg`): a boca articula diferente do original, e a pausa de 66,0–67,2 s fica fechada. OK.
- **Glitch de 9,27–9,83 s:** é do original (`t17_glitch.jpg`).
- **Fala:**
  - es (0,98), nenhum proibido, o texto bate com o roteiro;
  - "El enemigo no quiere que este mensaje llegue hasta ti" está no nível do AD 11/13.
- **Áudio:** −15,2 LUFS, sem silêncio. **CTA:** as setas vão de 67,9 s ao fim.
- **Imagem: abertura no quarto, 0–9 s.**
  - Mostra: **frascos de remédio** (laranja, tipo farmácia) e um relógio na mesa, o homem sentado na cama chorando com a mão no rosto e a personagem com a mão no ombro dele.
  - A fala da abertura é "Vine a traer **alivio** a tu corazón": "alivio" com remédios em cena lê como alívio de doença.
  - **Risco Meta: médio.** Não é tão explícito quanto o hospital do 10, mas a combinação remédios + "alivio" é o tipo de sinal de saúde que a revisão do Meta pega.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 0–9,0 | Frascos de remédio em cena. | **Média** (compliance) | Sem crédito: apagar os frascos com LaMa (máscara fixa na mesa, longe dos rostos) ou cobrir a mesa com um enquadramento mais fechado nos dois. |
| 2 | 0,51–2,5 | "alivio" (com a cena acima). | Baixa/média | Ideal: "Vine a traer paz a tu corazón", como no 10 e no 16 (TTS curto + refazer o s00, ~9 créditos). Se tirar os remédios, dá para aceitar o "alivio". |

## AD 18: APROVADO

- **Lipsync** (`met_18.txt`, medido no rosto da mulher):
  - s00 0,03; s02 0,04; s03 0,09; s04 0,25; s05 0,08; s06a 0,12; s06b 0,13; s07 0,37; s08 0,26; s09 0,05; s10 0,02; s11 (≥ 4 q) 0,08; s12 0,19; s13 0,17; s14 0,24; s15 0,05;
  - **conjunto 0,16**, nenhuma pausa com a boca aberta;
  - `f18_s11s13.jpg`: as pausas de 83,5, 86,2–86,5 e 88,2–89,1 s ficam fechadas;
  - `f18_s00fim.jpg`: de 9,00 a 9,47 s a boca fica fechada enquanto o original fala PT. Bom.
- **Flash branco (9,47–9,77 s, `t18_flash.jpg`):**
  - é uma fusão suave para o branco e do branco para a cena do Jesus, sem quadro de outra tomada e sem boca PT;
  - fica mais "limpa" que o light-leak original e não desentoa;
  - o tom roxo de 9,20–9,27 s é do original. Aprovado.
- **Fala:** es (0,98), nenhum proibido, o texto bate com o roteiro (miolo igual ao do 17).
- **Áudio:** −15,1 LUFS, sem silêncio.
- **Imagem:** as cobras do gancho ficam (são a cena). Sem legenda PT nem seta antiga.
- **CTA:** as setas vão de 77,25 s ao fim, abaixo da legenda.
- **Defeitos:** nenhum.

---

## Áudio do lote (todos)

| AD | LUFS | LRA | Silêncio absoluto (< −55 dB, ≥ 0,5 s) | Silêncio no fim |
|---|---|---|---|---|
| 04 | −15,2 | 2,6 | nenhum | 0,7 s (fade) |
| 07 | −15,1 | 2,1 | nenhum | ok |
| 08 | −15,1 | — | nenhum | ok |
| 09 | −15,1 | 2,4 | nenhum | ok |
| 10 | −15,1 | 2,4 | nenhum | ok |
| 15 | −15,2 | 1,6 | nenhum | ok |
| 16 | −15,1 | 3,4 | nenhum (mas 3,3 s sem fala em 78,9 s) | ok |
| 17 | −15,2 | 2,8 | nenhum | ok |
| 18 | −15,1 | 2,6 | nenhum | ok |

## Arquivos desta revisão (`_trabalho\revisao\loteB\`)
- **Scripts:**
  - `varrer.py`, `analisar.py` (com a escolha do rosto corrigida), `folha.py` (com trilha linear) e `emendas.py`;
  - `trans.py` (transições, final × original);
  - `alinh.py` (tempo do final × original);
  - `rodar_revisar.ps1`.
- **Dados:** `segs_B.json`, `faces_NN.jsonl`, `escolha_NN.json`, `met_NN.txt` e `audio\sep\htdemucs\` (vozes ES/PT).
- **Folhas de boca:**
  - AD 04: `f04_g1.jpg`, `f04_w1.jpg`, `f04_w2w3.jpg`, `f04_w6.jpg`, `f04_w6_pausa.jpg`, `f04_w12.jpg`;
  - AD 07: `f07_ini.jpg`, `f07_s12.jpg`, `f07_s12_fim.jpg`;
  - AD 08: `f08_s02.jpg`, `f08_s02_pausa.jpg`, `f08_s07s08.jpg`, `f08_s08.jpg`;
  - AD 09: `f09_m0fim.jpg`, `f09_E1.jpg`, `f09_NOP.jpg`;
  - AD 10: `f10_h0.jpg`, `f10_C.jpg`;
  - AD 15: `f15_s2.jpg`;
  - AD 16: `f16_a1.jpg`, `f16_i1j1.jpg`;
  - AD 17: `f17_s00fim.jpg`, `f17_s08s09.jpg`;
  - AD 18: `f18_s00fim.jpg`, `f18_s11s13.jpg`;
  - pausas de 1 em 1 quadro: `f_pausas.jpg` (09 E1, 16 j1 e 15 s2).
- **Transições:** `t04_clarao.jpg`, `t08_clarao.jpg`, `t10_brilho.jpg`, `t16_fusao.jpg`, `t17_glitch.jpg`, `t18_flash.jpg` e `t_0410.jpg`.
- **`revisar_ad.py`:** `revisar\AD NN - …_revisao.txt/.jpg` e `revisar\log_NN.txt`.
