# Revisão independente: lote A (ADs 01, 02, 03, 05, 12, 13 e 14), 08/10/2026

Sou o revisor independente: não editei nenhum vídeo nem arquivo de trabalho. Tudo o que gerei está em `_trabalho\revisao\loteA\`. O "AD 01 AVATAR" ficou de fora, como pedido.

## Resumo

| Vídeo | Veredito | Motivo principal |
|---|---|---|
| AD 01 - ORACION-TRES-BENDICIONES | **APROVADO** | Todos os trechos ≤ 0,47; conjunto 0,19. A boca refeita fecha nas pausas do ES. |
| AD 02 - ORACION-TRES-BENDICIONES-SHOPPING | **REPROVADO** | Usa as versões **antigas** de s03, s10 e s13, sem o `fechar.py` que o AD 01 recebeu. O s13 dá 0,67 e a boca abre nas pausas do ES. Correção sem crédito. |
| AD 03 - ORACION-PADRE-ROMERO | **APROVADO** (com observações) | Conjunto 0,07; nenhum trecho acima de 0,6. |
| AD 05 - ORACION-FAMILIA | **APROVADO** (com observações) | Conjunto 0,22. O c1 está no limite (0,57 no kit, 0,66 na minha conta) e a boca fechada por script fica parada ~1,3 s em duas pausas. |
| AD 12 - ORACION-SERPIENTES-CAMPO | **APROVADO** | Todos os trechos ≤ 0,55; conjunto 0,27. |
| AD 13 - ORACION-PAZ | **REPROVADO** | O lipsync ainda é o de `precision` da v1. Três trechos passam de 0,75 (w04 0,90; w05 0,98; w11 0,83) e cinco ficam entre 0,6 e 0,75. Há **boca articulando o português** nas pausas do ES (34,5–35,4 s e 36,9–37,4 s). |
| AD 14 - ORACION-SERPIENTES-CASA | **APROVADO** | Gancho 0,10; corpo igual ao do 12; conjunto 0,28. O "quadro solto" em 9,53 s é falso positivo (conferido contra o original). |

## Método (o mesmo das revisões anteriores, refeito no vídeo FINAL)

1. **Voz ES isolada do próprio final:** separei a voz com demucs (`audio\sep\htdemucs\fin_NN\vocals.wav`), para não depender das narrações de trabalho. A voz PT veio do demucs do original (no AD 05, com o mesmo corte 1286–1356 q a 24 fps).
2. **Varredura quadro a quadro** (`varrer.py` → `faces_NN.jsonl`): mede a abertura de cada rosto no final e no original, no mesmo tempo.
3. **Rosto de quem fala, trecho a trecho** (`analisar.py` → `met_NN.txt`): em cada trecho escolhi a trilha de rosto que o lipsync mudou. Conferi a escolha nas folhas. No gancho do AD 02, o script pegou a enfermeira calada; recalculei na mulher que fala.
4. **Índice de pausa:** a mesma conta do kit (pico do trecho − 30 dB; pausas ≥ 8 q, sem 2 q de cada borda). Nos trechos sem pausa longa, uso também um índice com pausas ≥ 4 q.
5. **Folhas de boca** (`folha.py`), de 2 em 2 ou de 3 em 3 quadros: final em cima, original embaixo, barra verde = voz ES, barra vermelha = voz PT.
   - **Folhas de emenda** (`emendas.py`), de 1 em 1 quadro, nos cortes.
6. **`revisar_ad.py`** pelo PowerShell, com a lista de proibidos do briefing: saídas em `loteA\revisar\`. Rodei também `ebur128` e a medida do silêncio final.
7. **Limitação:** a medida "mudou" (pixels da boca × testa) não serve neste lote. A colagem só da boca e a diferença de compressão entre fonte e final dão valores baixos mesmo com a boca claramente diferente. Por isso conferi "boca diferente do original" **nas folhas**, não por esse número.

---

## AD 01: APROVADO

**Lipsync** (`met_01.txt`; rosto da mulher; o Jesus fica calado com a boca fechada, conferido em `f01_jesus_*.jpg`):

| Trecho | Tempo | Índice | Corr. ES / PT |
|---|---|---|---|
| s01 | 0,00–8,40 | 0,23 | 0,37 / 0,11 |
| s02 | 8,40–15,90 | 0,43 | 0,28 / 0,18 |
| s03 | 15,90–19,47 | 0,04 | 0,58 / 0,40 |
| s04 | 19,47–20,97 | sem pausa (1,5 s) | 0,51 / 0,52 |
| s05 | 20,97–32,63 | 0,22 | 0,18 / 0,03 |
| s06 | 32,63–42,00 | 0,20 | 0,48 / −0,04 |
| s07 | 42,00–49,00 | 0,18 | 0,64 / 0,31 |
| s08 | 49,00–60,27 | sem pausa ≥ 8 q; com pausas ≥ 4 q: 0,53 | 0,24 / 0,17 |
| s09 | 60,27–72,47 | 0,09 | 0,47 / 0,31 |
| s10 | 72,47–83,30 | 0,03 | 0,61 / 0,15 |
| s11 | 83,30–93,73 | 0,47 | 0,32 / −0,02 |
| s12 | 93,73–104,77 | 0,38 | 0,37 / 0,04 |
| s13 | 104,77–115,50 | 0,05 | 0,58 / 0,08 |
| **Conjunto** | | **0,19** | |

- **Folhas:**
  - `f01_s05_fim.jpg`: a boca do final é outra e fecha na pausa de 30,8–31,0 s;
  - `f01_s08.jpg`: articula diferente do original durante todo o trecho.
- **Pausas do ES com a boca aberta:** nenhuma.
- **Rosto falando fora do lipsync:** nenhum, porque os 13 trechos cobrem o vídeo inteiro.
- **Boca coberta:** nenhuma.
- **Emendas** (`e01_a.jpg`, `e01_b.jpg`):
  - 19,47 s, 20,97 s e 49,00 s são cortes reais de câmera;
  - as emendas contínuas (8,40, 42,0, 60,27, 72,47, 83,30, 93,73 e 104,77 s) estão suaves, sem pulo de boca. O defeito nº 3 da revisão anterior foi resolvido.
- **Fala:**
  - `revisar_ad`: OK, es (1,00), nenhum proibido, sem PT residual;
  - o texto bate com o roteiro. O whisper só junta o "Toca" de 105 s à frase anterior, como antes.
- **Áudio:** −15,0 LUFS, LRA 1,9, fim 0,8 s depois da fala, nenhum silêncio > 0,7 s.
- **Imagem e CTA:** sem mudança desde a revisão anterior (aprovados). As setas vão de 104,97 s ao fim.
- **Defeitos:** nenhum que impeça.
  - **Baixa:** o s04 (1,5 s) não tem pausa, e a correlação é a mesma com o ES e com o PT. Na folha, a boca articula e é diferente da original. Aceito.

## AD 02: REPROVADO

**Lipsync** (`met_02.txt`):

| Trecho | Tempo | Índice | Observação |
|---|---|---|---|
| h1 (mulher do shopping) | 0–9,53 | **0,22** | Medido no rosto dela (a enfermeira chora calada). `f02_h1_mulher.jpg`: a boca fecha nas pausas do ES (6,4–7,6 s e 9,0–9,5 s) enquanto o original segue falando. OK. |
| s01 (resto) | 9,53–9,87 | — | De 9,53 a 9,66 s a Desatadora ainda fecha o "ti" sem voz (já anotado no relatório). Baixa. |
| s02, s05, s06, s07, s09, s11, s12 | | 0,37 / 0,23 / 0,18 / 0,18 / 0,11 / 0,50 / 0,38 | OK, iguais aos do AD 01 |
| s03 | 17,37–20,93 | sem pausa ≥ 8 q (≥ 4 q: 0,53) | É a versão antiga, não a do AD 01 com `fechar.py` (0,04) |
| s08 | 50,47–61,73 | sem pausa | É a mesma saída do s08 do AD 01 (`f02_s08.jpg`). Aceito, como no 01. |
| s10 | 73,93–84,77 | 0,52 | Versão antiga. A boca **abre e articula** em 73,97–74,23 s, sem voz ES (`f02_s10.jpg`), e fica aberta em 78,23–78,53 s. No AD 01 esse trecho dá 0,03. |
| **s13** | 106,23–116,97 | **0,67** | **Acima de 0,6.** Versão antiga: a boca fica aberta, sorrindo com os dentes, nas pausas do ES em 106,2–106,4, 108,0–108,4 e 110,9–111,1 s, igual ao original (`f02_s13.jpg`). No AD 01 esse trecho dá 0,05. |
| **Conjunto** | | **0,43** | O AD 01, com o mesmo corpo, dá 0,19. |

- **Fala:**
  - `revisar_ad`: OK, es (1,00), nenhum proibido;
  - o texto do gancho bate com o roteiro, e o corpo é o do AD 01.
- **Áudio:** −15,0 LUFS, LRA 2,3, fim 0,8 s depois da fala, nenhum silêncio > 0,7 s.
- **Imagem:**
  - sem legenda PT;
  - o corte do gancho (9,53 s) está limpo;
  - a enfermeira chora calada (boca original, mas sem fala).
- **CTA:** as setas vão de 106,4 s ao fim, abaixo da legenda e longe da boca.

**Defeitos:**

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 106,23–116,97 (s13) | Índice 0,67 (> 0,6): boca aberta nas pausas do ES, como no original. | **Alta** (regra do lote) | Trocar s03, s10 e s13 pelas versões do AD 01 já tratadas com `fechar.py` (`ad01\lipsync2`, deslocadas +44 q) e remontar (`montar_corpo.py` + `montar_ad.py`). **Sem crédito.** O relatório do AD 02 diz que usou a cópia de 22:03 da `base_lipsync` do 01, anterior ao `fechar.py` nesses trechos. |
| 2 | 73,97–74,23 e 78,23–78,53 (s10) | A boca articula e fica aberta sem voz ES. | Média | Sai junto com o item 1. |
| 3 | 9,53–9,66 | A boca termina o "ti" sem voz por cerca de 4 q. | Baixa | Fechar a boca nesses 4 quadros (`fechar.py`) ou aceitar. |

## AD 03: APROVADO (com observações)

**Lipsync** (`met_03.txt`; um só rosto, o padre):

| Trecho | Tempo | Índice |
|---|---|---|
| p01 | 0,00–2,43 | sem pausa (corr. ES 0,42 × PT 0,18) |
| p02 | 2,43–3,57 | sem pausa |
| p03 | 3,57–9,13 | sem pausa |
| p04 | 9,43–16,63 | 0,60 (só 6 q de pausa) |
| p05 | | 0,09 |
| p06 | | 0,03 |
| p07 (tela dividida, padre em cima) | 39,93–47,90 | sem pausa ≥ 8 q (≥ 4 q: 0,19) |
| p08 | | sem pausa |
| p09 | | 0,05 |
| p10 | | 0,05 |
| p11 | | 0,13 |
| p12 | | sem pausa |
| p13 | | 0,03 |
| p14 | 83,10–92,30 | sem pausa ≥ 8 q (≥ 4 q: 0,40) |
| p15 | | 0,02 |
| **Conjunto** | | **0,07** |

- **Folhas:**
  - `f03_p03.jpg` e `f03_p07.jpg`: a boca do final é diferente da original, articula e fecha na pausa de 43,0–43,1 s;
  - nenhuma pausa do ES com a boca aberta.
- **Fora do lipsync:** 9,13–9,43 s (clarão de transição do próprio original, `e03_clarao.jpg`).
  - O rosto fica lavado de luz e sorrindo, sem articular.
  - No quadro 9,40 s (q282, 1 quadro antes do p04) a boca original aparece aberta.
  - Gravidade baixa.
- **Falsos positivos do `revisar_ad`, conferidos a olho:**
  - "quadro solto" em 9,13/9,27/9,37 s: é o clarão do original;
  - "setas sobre a faixa escura": é a madeira do púlpito, sem texto embaixo.
- **Fala:**
  - es (0,96), nenhum proibido, o texto bate com o roteiro;
  - "Una mujer… la rezó con fe, y sintió una paz y una esperanza" está dentro do que o briefing permite ("pode virar 'sintió paz y esperanza'");
  - "acceso totalmente gratis" está OK.
- **Áudio:**
  - −15,1 LUFS, LRA 3,5, fim 0,7 s depois da fala;
  - **4 silêncios absolutos** de 1,1–1,4 s (22,93–24,08, 37,41–38,85, 59,22–60,13 e 66,39–67,53 s), a −61 dB, sem nenhum fundo;
  - o original não tem silêncio > 0,7 s.
- **Imagem:**
  - o PIX/R$ saiu (a cruz dourada está na metade de baixo, 40–48 s);
  - sem legenda PT e sem a mãozinha.
- **CTA:** as setas entram com o 1º "toca" (60,46 s) e ficam no púlpito, abaixo da legenda.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 37,41–38,85 (e os outros 3) | Silêncio digital de 1,1–1,4 s com o padre parado: soa como "buraco" de áudio. | Baixa/média | Pôr um ambiente de sala (room tone) baixo por baixo da narração, ou encurtar as pausas para ~0,6 s. |
| 2 | 9,40 (1 quadro) | Boca original aberta logo antes do p04. | Baixa | Começar o p04 1 quadro antes ou fechar a boca nesse quadro. |

## AD 05: APROVADO (com observações)

**Lipsync** (`met_05.txt`; trechos pelas tomadas do final):

| Trecho | Tempo | Quem | Índice |
|---|---|---|---|
| c1 | 0,00–3,13 | Clara (rosto pequeno, no alto à direita) | **0,66** na minha conta / **0,57** no `checar_lipsync.py --rosto` do kit |
| c2 | 11,93–17,93 | Clara | 0,07 |
| c3 | 17,93–27,20 | Clara | 0,12 |
| m3 | 27,20–37,20 | marido | 0,14 |
| m4 | 37,20–47,03 | marido | 0,23 |
| m5 | 47,03–52,97 | marido | 0,07 |
| d1 | 54,27–61,43 | Desatadora | 0,16 |
| d2 | 61,43–71,33 | Desatadora | 0,17 |
| d3 | 71,33–83,00 | Desatadora | 0,43 |
| d4 | 83,00–89,60 | Desatadora | 0,41 |
| d5 | 89,60–95,50 | Desatadora | 0,03 |
| **Conjunto** | | | **0,22** |

- **c1** (`f05_c1.jpg`):
  - durante a fala ES (0,13–1,87 s), a boca articula diferente do original;
  - na pausa de 1,87–2,67 s (o PT ainda falava), ela fica sorrindo com os dentes, parecida com a original, mas sem articulação visível.
  - Fica no limite. Não reprovo só por isso, porque o kit dá 0,57 e não se vê fala PT, mas anoto.
- **Bocas fechadas por script** (`f05_m3fim.jpg`, `f05_m5.jpg`, `f05_d1.jpg`):
  - nas pausas a boca fica fechada, sem rastro de PT;
  - em **35,9–37,2 s** (fim do m3) e **51,6–52,9 s** (fim do m5), porém, os lábios ficam **idênticos quadro a quadro por ~1,3 s**, enquanto o original sorri e fala;
  - nas folhas o encaixe parece limpo, sem borda nem desalinhamento, mas parado. Em quadros parados não dá para garantir que não pareça "colado" em movimento: **conferir assistindo**;
  - as pausas curtas do d1 (55,9–56,0 s e 60,9–61,5 s) parecem naturais.
- **Pausas do ES com a boca aberta:**
  - d3 74,97–75,33 s e d4 84,53–84,90 s: é um sorriso parado (`f05_d3p.jpg`, `f05_d4p.jpg`), não articulação;
  - aceitável.
- **Trechos de rosto falando fora do lipsync:**
  - **nenhum com fala visível** (`f05_cobertos.jpg`);
  - 3,13–6,7 s: detalhes (prato, mãos), boca coberta (m1 "Gracias, mi reina" e a fala da Clara);
  - 6,7–8,2 s: close do pai, calado; a Clara fala fora de quadro;
  - 8,2–11,9 s: enquadramento na Clara escutando e no pai; o marido fala fora de quadro;
  - 52,97–54,25 s: plano aberto da família, com o clarão, sem a Desatadora.
- **Bocas cobertas:** 3,62–4,96 s (m1), 4,96–6,71 s (Clara) e 8,17–11,92 s (marido).
- **Fala:**
  - es (0,97), nenhum proibido, o texto novo do marido bate com o relatório v3;
  - "Recé… y mi corazón encontró descanso. Por eso volvió la paz a nuestra casa" é depoimento de paz, permitido pelo briefing;
  - não há relação entre comida/dinheiro e oração.
- **Áudio:** −15,0 LUFS, LRA 3,5, fim 0,8 s depois da fala, nenhum silêncio.
- **Imagem:** sem legenda PT, e as manchas toleráveis.
- **CTA:** as setas entram com "Toca el botón" (73,4 s), abaixo da legenda, sobre o vestido e o cordão. Legível.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 1,87–2,67 (c1) | Na pausa do ES, a Clara mantém o sorriso aberto parecido com o original. Índice no limite (0,57–0,66). | Baixa/média | Aplicar o `fechar.py` na pausa de 1,87–3,13 s (sem crédito) e medir de novo. |
| 2 | 35,9–37,2 e 51,6–52,9 | Boca fechada idêntica por ~1,3 s (pode parecer parada). | Baixa | Conferir assistindo. Se incomodar, alternar 2–3 quadros fechados do próprio trecho, ou pôr um leve movimento de lábio. |

## AD 12: APROVADO

**Lipsync** (`met_12.txt`; a Desatadora; o Jesus fica calado atrás):

| Trecho | Índice |
|---|---|
| h | 0,08 |
| s01 | 0,25 |
| s02 | 0,32 |
| s03 | 0,46 |
| s04 | 0,06 |
| s05a | 0,45 |
| s05b | 0,03 |
| s06 | 0,27 |
| s07 | **0,55** (o mais alto) |
| s08 | 0,03 |
| s09 | sem pausa ≥ 8 q (≥ 4 q: 0,08) |
| s10 | 0,22 |
| s11 | 0,08 |
| s12 | 0,12 |
| s13 | 0,28 |
| **Conjunto** | **0,27** |

- **Folhas** `f12_s01.jpg` e `f12_s07.jpg`: a boca é claramente outra e fecha nas pausas (11,4–11,7, 14,5–14,7, 65,6–66,0 e 68,2–68,5 s) enquanto o original segue falando ou sorrindo.
- **Duas pausas com a boca entreaberta** (19,60–19,93 e 34,50–34,73 s): sem articulação. Baixa.
- **Fora do lipsync:** só o clarão de 9,54–9,60 s.
- **Emendas:** de 1 em 1 quadro nos 12 cortes (`e12_a.jpg`, `e12_b.jpg`). São cortes reais, sem quadro solto.
  - A emenda contínua s05a/s05b (48,03 s) está suave.
- **Fala:**
  - es (0,99), nenhum proibido, o texto bate com o roteiro;
  - "Hay quien no quiere que este secreto llegue hasta ti" é ameaça leve e sem alvo, no nível do AD 11;
  - sem contagem regressiva.
- **Áudio:** −15,1 LUFS, LRA 2,2, fim 0,8 s, nenhum silêncio.
- **Imagem:** sem legenda PT, e a seta vermelha do original saiu.
- **CTA:** as setas vão de 75,9 s ao fim, sobre as cordas, abaixo da legenda.
- **Defeitos:** nenhum que impeça.
  - **Baixa:** a voz é o clone do AD 13, não o do AD 01, apesar de ser a mesma personagem (já anotado).

## AD 13: REPROVADO

**Lipsync** (`met_13.txt`). O w10 foi refeito na v2, mas **os demais trechos continuam na versão `precision` da v1.** É exatamente o modo que o `LICOES-LIPSYNC.md` mostra que devolve a boca do PT onde o ES se cala.

| Trecho | Tempo | Índice | Veredito |
|---|---|---|---|
| j1 (Jesus) | 0,00–6,60 | 0,62 (8 q de pausa) | aviso |
| w01 | 7,03–15,17 | 0,36 | OK |
| w02 | 15,17–23,07 | 0,16 | OK |
| w03 | 23,07–29,10 | **0,69** | > 0,6 |
| w04 | 33,43–43,57 | **0,90** | **reprovado** |
| w05 | 47,13–53,00 | **0,98** | **reprovado** |
| w06 | 53,00–59,80 | **0,71** | > 0,6 |
| w07 | 63,63–67,10 | **0,65** | > 0,6 |
| w08 | 67,10–76,17 | 0,35 | OK |
| w09 | 76,17–83,90 | **0,67** | > 0,6 |
| w10 | 88,90–98,30 | sem pausa | atravessa o corte de câmera em 94,87 s |
| w11 | 98,30–106,40 | **0,83** | **reprovado** |
| w12 | 106,40–116,00 | 0,24 | OK |
| w13 | 116,00–119,80 | 0,56 | OK |
| **Conjunto** | | **0,57** | Passa no conjunto, mas reprova por trecho. |

**Boca articulando o português (o que as folhas mostram):**
- **34,5–35,4 s** (w04, `f13_w04.jpg`): o ES está calado e o PT fala. A boca do final abre e fecha acompanhando o original.
- **36,9–37,4 s** (w04): pausa do ES; a boca fica bem aberta, mostrando os dentes, igual ao original.
- **48,3–48,9 s** (w05, `f13_w05.jpg`, perfil): pausa do ES; a boca segue entreaberta como no original.
- **50,47–51,0 s** (w05, início do close): pausa do ES; a boca está aberta.
- **105,8–106,0 s** (w11, `f13_w11.jpg`, perfil): pausa com a boca aberta.

**Outros pontos:**
- **Rostos fora do lipsync:**
  - b-roll da mesa (43,57–47,13 s): a mulher não fala, aceitável, como na revisão anterior;
  - o glitch de 6,6–7,0 s ficou resolvido na v2: a fala começa em 6,98 s.
- **v2 conferida:**
  - o quadro solto de 88,90 s saiu (`e13_a.jpg`);
  - a frase nova de 90,9–98,3 s está no áudio e na transcrição ("Pero presta mucha atención hasta el final, porque este momento es para ti…");
  - "segundos" e "aire" saíram.
- **Emendas** (`e13_a.jpg`, `e13_b.jpg`): sem quadro solto. Os cortes em 58,37, 94,87 e 111,87 s caem dentro de trechos de lipsync, mas não mostram defeito.
- **Fala:**
  - `revisar_ad`: OK, es (0,99), nenhum proibido;
  - **ainda tem "Pero sé rápido" (107,8 s)**, que é pressão de tempo. Não é contagem regressiva, mas destoa do resto do lote, que tirou isso.
  - O depoimento "en ese mismo mes, sintió una paz y una esperanza" está permitido.
- **Áudio:** −15,1 LUFS, LRA 3,2, fim 0,3 s depois da fala, nenhum silêncio.
- **Imagem:** sem legenda PT nem a mãozinha; a cena do quarto é sem pessoa.
- **CTA:** as setas vão de 99,4 s ao fim. Nos closes de 116 s ficam sobre o brilho do peito, abaixo da legenda. Legível.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 23,07–29,10; 33,43–43,57; 47,13–59,80; 63,63–67,10; 76,17–83,90; 98,30–106,40 (w03, w04, w05, w06, w07, w09, w11) | Lipsync `precision`: a boca segue o PT nas pausas do ES. Índices de 0,65 a 0,98. | **Alta** | Refazer esses 7 trechos como no `LICOES-LIPSYNC.md`: recorte só na mulher, PT na entrada e **`mode: speed`**. São cerca de 52 s, ou ~52 créditos. Antes, dá para testar o `fechar.py` (sem crédito) nas pausas, mas o 34,5–35,4 s articula PT por quase 1 s e provavelmente precisa ser refeito. Medir de novo cada trecho no final (meta ≤ 0,6). |
| 2 | 34,5–35,4 e 36,9–37,4 | Boca falando PT visível (sem voz ES). | **Alta** | Sai com o item 1. Se não refizer, fechar a boca nesses intervalos. |
| 3 | 0,00–6,60 (j1) | Índice 0,62, com poucas pausas (8 q); barba. | Baixa | Conferir assistindo; `fechar.py` na pausa final, se precisar. |
| 4 | 107,8 | "Pero sé rápido": pressão de tempo. | Baixa/média | Trocar por "Pero presta atención" ou tirar (refaz o w12, ou só cortar o áudio, se couber). |

## AD 14: APROVADO

- **Gancho h** (0–9,53 s, `f14_h.jpg`):
  - índice 0,10, corr. ES 0,44 × PT 0,01;
  - a boca fecha nas pausas (6,2–6,5 s e 8,5–8,9 s) enquanto o original fala.
- **Corpo:** o mesmo do AD 12. Na minha medida no final do 14: s01–s13 de 0,03 a 0,58 (s07 0,58); s09 sem pausa ≥ 8 q (≥ 4 q: 0,06).
- **Conjunto: 0,28.**
- **"Quadro solto" em 9,53/9,60 s (`revisar_ad`): falso positivo.** O 1 em 1 quadro do final (`e14_trans.jpg`) contra o original (`e14_trans_orig.jpg`) mostra a mesma dissolução com clarão (escuro → amarelo → rosa → olival), sem quadro de outra tomada.
- **Fala:** es (0,99), nenhum proibido, o mesmo roteiro do 12.
- **Áudio:** −15,1 LUFS, LRA 2,2, fim 0,8 s.
- **Imagem:** sem legenda PT no gancho nem no corpo.
- **CTA:** igual ao 12.
- **Defeitos:** nenhum que impeça. Só o s07 perto do limite (0,58), igual no 12.

---

## Arquivos desta revisão (`_trabalho\revisao\loteA\`)
- **Scripts:** `varrer.py`, `analisar.py`, `folha.py` e `emendas.py`.
- **Dados:** `faces_NN.jsonl`, `escolha_NN.json`, `met_NN.txt`, `audio\sep\htdemucs\` (vozes) e `segs_05.json`.
- **Folhas de boca:**
  - AD 01: `f01_*.jpg`;
  - AD 02: `f02_h1_mulher.jpg`, `f02_s08.jpg`, `f02_s10.jpg`, `f02_s13.jpg`;
  - AD 03: `f03_*.jpg`;
  - AD 05: `f05_*.jpg`;
  - AD 12: `f12_*.jpg`;
  - AD 13: `f13_w04.jpg`, `f13_w05.jpg`, `f13_w11.jpg`, `f13_jesus_33-38.jpg`;
  - AD 14: `f14_h.jpg`.
- **Emendas:** `e01_a/b.jpg`, `e03_clarao.jpg`, `e12_a/b.jpg`, `e13_a/b.jpg`, `e14_trans.jpg`, `e14_trans_orig.jpg`.
- **`revisar_ad.py`:** `revisar\AD NN - …_revisao.txt/.jpg` e `revisar\log_NN.txt`.
- **Kit no c1 do AD 05:** `kit\`.
