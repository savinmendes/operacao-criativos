# Revisão independente: lote C (08/10/2026, 00:14–01:20)

Sou o revisor independente: não editei nenhum vídeo nem arquivo de trabalho. Tudo o que gerei está em `_trabalho\revisao\loteC\`.

- **1ª rodada:** AD 06 (revisão completa) e confirmação da "Correção lote A" dos ADs 02, 03 e 05.
- **2ª rodada:** AD 13 v3, AD 08 e 16 (correção lote B) e AD 09, 10 e 17 (correção lote B).
- **Pedido extra do coordenador:** brilho e cor da área colada da boca × resto do rosto nos ADs 12, 14, 17 e 18. Estendi a medida aos outros ADs para ter referência.

## Resumo do lote C

| Vídeo | Veredito | Motivo principal |
|---|---|---|
| AD 02 | **APROVADO** | s03 0,03 (pausas ≥ 4 q), s10 0,04, s13 0,06. Conjunto 0,20. As bocas abertas de 74,0, 78,3, 106,2 e 108,0 s agora fecham. O s08 em speed articula diferente do original. |
| AD 03 | **APROVADO** | Não há mais silêncio absoluto: o ambiente de sala fica a −45/−47 dB, com espectro de sala (centroide ~2,1 kHz) e sem repetição audível do loop. O quadro de 9,40 s está com a boca quase fechada. Conjunto 0,07. |
| AD 05 | **APROVADO** | O c1 cai de 0,66 para **0,19** (na minha conta). Na pausa de 1,9–3,1 s a Clara mantém o sorriso de boca fechada. Conjunto 0,19. |
| AD 06 | **APROVADO** (com observações) | Conjunto 0,11. Os closes da corda são limpos e entram e saem nos cortes do original. O zoom de 51–54 s não tem borda. O clarão não deixa legenda PT. |
| AD 13 v3 | **APROVADO** (com observações) | Conjunto 0,24, sem trecho acima de 0,6. As 5 bocas PT do lote A estão fechadas e o "sé rápido" saiu. **Defeito novo:** xadrez de pixels sob o lábio, no perfil, em 35,27–35,40 e 35,63–35,87 s. Correção barata recomendada. |
| AD 08 | **APROVADO** (com observações) | s02 0,07: a boca fecha em 18,13–18,53 s. O "hoy" saiu. Conjunto 0,19. A cor do vídeo inteiro está mais escura e fria que o original (ver "Brilho e cor"). |
| AD 09 | **APROVADO** | Em 46,93–47,07 s a boca fica num "o" fechado, sem dentes. Conjunto 0,14. |
| AD 10 | **APROVADO** (com observações) | A abertura foi reenquadrada só na personagem: sem leito, idoso ou monitor. h0 0,08, conjunto 0,14. |
| AD 16 | **APROVADO** | O "sé rápido" e o buraco de 3,3 s saíram. j1 0,30, k1 0,35, conjunto 0,21. |
| AD 17 | **REPROVADO** | Compliance e lipsync OK: frascos apagados, "paz" no lugar de "alivio", conjunto 0,10. Reprovado pela **cor do gancho (s00, 0–9,3 s)**: a área colada fica 10,5 níveis mais escura que o resto do rosto, e o rosto inteiro fica 17 níveis mais escuro e magenta que o original. |
| AD 18 | **REPROVADO** (era APROVADO no lote B) | Pedido extra. A área colada fica 8 níveis mais escura que o rosto em todos os trechos e **16 no gancho (s00)**, com tom roxo na metade de baixo do rosto. Dá para ver no recorte. |
| AD 12 / AD 14 | **APROVADO** (mantido, com anotação) | Pedido extra. O degrau da área colada é de −4,8 níveis, constante. É imperceptível sem comparar com o original. |

---

## Método

Uso o mesmo método dos lotes A e B, refeito no vídeo FINAL. Os scripts dos dois lotes foram copiados para `loteC\` e adaptados.

1. **Voz ES isolada do próprio final** com demucs (`audio\sep\htdemucs\fin_NN`). A voz PT vem do demucs do original:
   - copiada de `loteA` e `loteB` (o AD 05 já com o corte de 70 q);
   - a do AD 06 foi feita agora (`ori_06`).
2. **Tempo do final = tempo do original** (AD 06: `alinh.py`, melhor deslocamento 0). No AD 05 uso o mapa do lote A (+70/24 s depois do q24 1286).
3. **Varredura quadro a quadro** (`varrer.py` → `faces_NN.jsonl`) e **rosto de quem fala por trecho** (`analisar.py` → `met_NN.txt`).
   - Trechos: `segs_C.json`, tirados dos relatórios e dos `segmentos.json`. No AD 16 entram o j1 e o k1 novos, e o l1 saiu.
   - Escolha do rosto: o mais à direita, como no lote B. No AD 13 a mulher fica à esquerda e a medida "mudou" funciona (65–100 %), então escolho a trilha refeita com mais presença.
   - Conferi a escolha nas folhas.
4. **Índice de pausa** pela conta do kit (pico − 30 dB; pausas ≥ 8 q, sem 2 q de cada borda). Nos trechos sem pausa longa, uso também pausas ≥ 4 q.
5. **Folhas de boca** (`folha.py`, final em cima e original embaixo; barra verde = ES, vermelha = PT), **emendas** (`emendas.py`, 1 em 1 quadro) e **transições** (`trans.py`, final × original).
6. **`revisar_ad.py`** pelo PowerShell (`rodar_revisar.ps1`), com os proibidos em **`proibidos.txt` UTF-8**: briefing + "rápido, rápida, pocos, minuto, salud, dolor, sanar, sanación, milagro, enfermo, hospital, hoy, noche". Com o .txt os acentos chegam certos ao Python. Saídas em `loteC\revisar\`.
7. **Áudio:**
   - `ebur128`: todos os ADs do lote C ficam entre −15,0 e −15,1 LUFS;
   - `silencedetect` a −55 dB / 0,5 s: nenhum silêncio absoluto em nenhum vídeo;
   - buracos de fala medidos na voz ES isolada (−40 dB / 1,2 s).
8. **Novos nesta rodada:**
   - `brilho.py` e `cor.py`: Y/U/V do final − original no lábio superior + queixo (dentro da elipse colada) e nas bochechas altas (fora dela);
   - `mapa_dif.py`: mapa médio de final − original no rosto, que mostra a elipse;
   - `xadrez.py`: procura padrão de pixels alternados perto da boca. Foi o que achou o defeito do AD 13.

---

## AD 06: APROVADO (com observações)

**Lipsync** (`met_06.txt`; rosto da Desatadora; o Jesus fica calado):

| Trecho | Tempo | Índice | Corr. ES / PT |
|---|---|---|---|
| v1 (varal) | 0,00–8,70 | 0,10 | 0,54 / 0,39 |
| w1 | 8,70–18,43 | 0,11 | 0,36 / 0,10 |
| w2 | 18,43–28,20 | 0,15 | 0,38 / 0,13 |
| w3 | 28,20–37,87 | 0,30 | 0,31 / 0,32 |
| w4 | 37,87–39,93 | coberto (close da corda) | — |
| w5 | 39,93–47,30 | sem pausa ≥ 8 q (≥ 4 q: 0,60) | 0,23 / 0,02 |
| w6 (zoom) | 47,30–54,07 | 0,06 | 0,48 / 0,15 |
| w7 / w8 / w9 / w10 | | 0,08 / 0,10 / 0,03 / 0,03 | |
| w11 | 79,37–82,80 | coberto (close da corda) | — |
| w12 / w13 / w14 / w15 | | 0,10 / 0,05 / 0,04 / 0,09 | |
| w16 | 99,20–100,53 | sem pausa (1,3 s) | 0,34 / 0,21 |
| w17 | 100,53–102,70 | 0,25 | |
| **Conjunto** | | **0,11** | |

- **Closes da corda** (`t06_corda1.jpg`, `t06_corda2.jpg`, `z06_cortes_corda.jpg`; 1 em 1 quadro, final × original):
  - **37,87–39,90 s:** entra e sai exatamente nos cortes de câmera do original (37,87 e 39,90 s). Não há rosto, só o colo, as mãos e a corda. A nitidez é aceitável, um pouco mais suave que o plano aberto.
  - **79,37–82,77 s:** também entra e sai nos cortes do original (79,37 e 82,80 s). As mãos se mexem (não é quadro parado). As setas novas ficam por cima, sem resto da seta antiga.
  - Os dois closes são parecidos entre si (mesmo enquadramento), mas cumprem a função. Nenhum quadro de boca PT.
- **Zoom de 51–54 s** (`f06_w6.jpg`, `z06_zoom_rosto.jpg`):
  - a boca é outra, articula e fecha na pausa de 50,3–51,2 s, enquanto o original fala;
  - no close em tamanho real não há borda nem mancha na colagem que segue o rosto;
  - a emenda w5→w6 (47,30 s) está suave (`e06_a.jpg`).
- **Clarão de 8,6 s** (`t06_clarao.jpg`, `z06_clarao_legenda.jpg`, `z06_ponto.jpg`):
  - a legenda PT, inclusive a tingida de rosa e amarelo, sumiu em todos os quadros de 8,30 a 8,80 s;
  - há um pontinho escuro de ~5 px em 8,43–8,63 s, onde a corda pende. É, provavelmente, a ponta da corda vista através do clarão. Desprezível.
- **Pausas com a boca aberta:** w3 35,27–35,63 s (`f06_w3_pausa.jpg`). Os lábios ficam entreabertos e depois fecham (35,40–35,57 s), enquanto o original articula. Não é PT. Baixa.
- **w5** (`f06_w5.jpg`):
  - articula diferente do original e fecha nas pausas de 41,4 e 45,4–45,5 s;
  - nos 2 primeiros quadros (40,00–40,07 s), logo depois do close da corda, aparece um sorriso com dentes sem voz. Baixa.
- **Emendas** (`e06_a.jpg`, `e06_b.jpg`, 17 cortes de 1 em 1 quadro): sem quadro solto e sem pulo de boca.
- **Fala** (`revisar\log_06.txt`):
  - es (0,96), nenhum proibido;
  - o texto bate com o roteiro (o whisper escreve "Resaste" e "correto");
  - "El enemigo no quiere que esta oración llegue hasta ti" fica no nível do AD 11/13/17;
  - sem dinheiro, cura, prazo ou "hoy".
- **Áudio:**
  - −15,1 LUFS, LRA 2,7, nenhum silêncio absoluto;
  - duas pausas de fala de ~2,1 s (58,9–60,9 e 88,5–90,6 s), com o fundo musical por baixo. São do roteiro. Baixa.
- **Imagem e CTA:**
  - sem legenda PT nem seta antiga; sobra só uma leve mancha na corda sob as setas novas (`z06_mancha_setas.jpg`), quase invisível;
  - as setas vão de 76,67 s ao fim, abaixo da legenda.
- **Cor:** degrau da área colada de −2,5 níveis. Fica entre os melhores do lote, junto com o AD 13 v3 e o 03.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 35,27–35,63 | Boca entreaberta numa pausa (sem PT). | Baixa | Aceitar. |
| 2 | 40,00–40,07 | 2 q de sorriso com dentes sem voz, depois do close. | Baixa | Aceitar, ou `fechar.py` em 2 q. |
| 3 | 37,9–39,9 / 79,4–82,8 | Closes da corda um pouco mais suaves e parecidos entre si. | Baixa | Assistir. |
| 4 | 58,9–60,9 / 88,5–90,6 | Pausas de fala de ~2 s. | Baixa | Opcional: encurtar para ~0,7 s. |

## AD 02 (correção lote A): APROVADO

| Trecho | Lote A | Agora (`met_02.txt`) |
|---|---|---|
| h1 (mulher do shopping) | 0,22 | 0,25 |
| s03 | sem pausa (≥ 4 q: 0,53) | sem pausa ≥ 8 q (**≥ 4 q: 0,03**) |
| s08 | antigo (precision) | o speed do AD 01: articula diferente do original (`f02_s08.jpg`) |
| s10 | 0,52 | **0,04** |
| s13 | **0,67** | **0,06** |
| **Conjunto** | 0,43 | **0,20** |

- **Folhas:**
  - `f02_s10.jpg`: em 73,97–74,23 s a boca fica fechada (antes articulava); em 78,23–78,53 s, também fechada;
  - `f02_s13.jpg`: 106,2–106,47 s com os lábios fechados (antes, o sorriso com dentes do original); 108,0–108,4 s, fechada;
  - `f02_s03.jpg`: fecha nas micropausas.
- **Emendas** (`e02.jpg`; 9,53, 17,37, 20,93, 50,47, 61,73, 73,93, 84,77 e 106,23 s): sem quadro solto e sem pulo de boca.
- **`revisar_ad`:** OK, es (1,00), nenhum proibido, sem silêncio, setas no último quadro. **Áudio:** −15,0 LUFS.
- **Pendente (baixa, aceito):** 9,53–9,66 s, ~4 q terminando o "ti" sem voz.
- **Nada novo apareceu.**

## AD 03 (correção lote A): APROVADO

- **Ambiente de sala:**
  - nenhum silêncio < −55 dB em todo o vídeo;
  - nas 4 pausas apontadas, o nível fica em −45,5 dB (37,6 s) e semelhante nas outras;
  - espectro: centroide de 2,06–2,17 kHz e só 22 % da energia acima de 4 kHz. Soa como sala, não como chiado agudo;
  - autocorrelação máxima de 0,13: o loop de 0,4 s não se repete de forma audível.
- **Quadro de 9,40 s** (`f03_q282.jpg`): a boca está quase fechada, bem diferente da boca aberta do original. Emenda com o p04.
  - Durante o clarão (9,13–9,37 s) o rosto lavado de luz ainda é o do original, com a voz ES por cima, igual no lote A. Baixa.
- **Lipsync** (`met_03.txt`): igual ao lote A, conjunto 0,07 (p04 0,51, com só 6 q de pausa).
- **`revisar_ad`:** es (0,96), nenhum proibido. Os 3 "PROBLEMA" são os falsos positivos já conferidos (clarão e madeira do púlpito).
- **Nada novo apareceu.** A cor também está boa: degrau de +0,7.

## AD 05 (correção lote A): APROVADO

- **c1** (`f05_c1.jpg`, `z05_c1.jpg`): de 2,1 a 3,1 s a Clara mantém um sorriso de boca fechada, enquanto o original mostra os dentes e articula. Não há borda nem salto no corte de 3,13 s.
  - c1: **0,19** (era 0,66 na minha conta do lote A).
- **Conjunto 0,19.** As pausas com a boca "aberta" do d3 (74,97 e 79,07 s) e do d4 (84,53 s) são o sorriso parado já aceito no lote A.
- **`revisar_ad`:** es (0,97). Acusa "hoy" em 47,0 s ("…volvió la paz a nuestra casa y **hoy** vivimos con más fe y unión").
  - É narrativo (depoimento de paz já aceito no lote A), não é prazo nem hora do dia. **Não é defeito.** Anoto só porque o "hoy" foi tirado dos ADs 08/09/18 por outro motivo.
- **Pendente (baixa):** a boca fechada parada em 35,9–37,2 e 51,6–52,9 s. Conferir assistindo.
- **Nada novo apareceu.**

## AD 13 v3: APROVADO (com observações)

**Lipsync** (`met_13.txt`):

| Trecho | Lote A | v3 |
|---|---|---|
| j1 (Jesus) | 0,62 | 0,57 (8 q de pausa; barba) |
| w01 / w02 | 0,36 / 0,16 | 0,35 / 0,22 |
| w03 | **0,69** | 0,08 |
| w04 | **0,90** | 0,30 |
| w05 | **0,98** | 0,12 |
| w06 | **0,71** | 0,31 |
| w07 | **0,65** | 0,17 |
| w08 | 0,35 | 0,35 |
| w09 | **0,67** | 0,12 |
| w10 | sem pausa | 0,03 |
| w11 | **0,83** | 0,30 |
| w12 (frase nova) | 0,24 | 0,04–0,06 |
| w13 | 0,56 | 0,03 |
| **Conjunto** | 0,57 | **0,24** |

- **Bocas PT do lote A, todas fechadas agora:**
  - 34,5–35,4 s e 36,9–37,4 s (`f13_w04.jpg`);
  - 48,3–48,9 s e 50,47–51,0 s (`f13_w05.jpg`);
  - 105,8–106,0 s (`f13_w11.jpg`).
- **Frase nova** (`f13_w12.jpg`): "No lo dejes para después." em 107,66–109,56 s. A boca articula e fecha na pausa anterior. O "sé rápido" saiu.
- **w08** (não refeito), 67,13–67,43 s (`f13_w08p.jpg`): logo depois do corte, a boca fica num sorriso aberto parado, sem voz ES, enquanto o PT fala. A forma é diferente da do original, que articula. Baixa (já estava assim no lote A).
- **Defeito novo, xadrez de pixels** (`z13_w04_art.jpg`, `z13_art_scan.jpg`, `xadrez.py`):
  - no perfil da mulher, logo abaixo do lábio inferior, na borda do rosto contra o fundo, aparece um padrão quadriculado de pixels (~15 px) em **35,27–35,40 s** e **35,63–35,87 s** (cerca de 8 quadros);
  - parece resto da borda da saída do HeyGen ou da elipse colada que passou do contorno do perfil;
  - em tamanho real dá para ver como um "chiado" no lábio. No celular é discreto;
  - o detector não achou nada parecido no resto do 13, nem no 06 (as outras detecções eram letras da legenda).
- **Cor:** degrau da área colada de −0,9 no geral (−1,1 a −2,8 nos trechos refeitos). Entre trechos refeitos e não refeitos o rosto varia só ~2 níveis. **A correção de cor da v3 funcionou.**
- **`revisar_ad`:** OK, es (0,99), nenhum proibido ("rápido" procurado de fato), 18 cortes, setas no último quadro.
- **Urgência:** "No lo dejes para después" (107,7 s) e "No dejes pasar este momento" (112,7 s) ficam próximas. Ambas são suaves e sem prazo. Aceito.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 35,27–35,40 e 35,63–35,87 | Xadrez de pixels sob o lábio, no perfil (w04). | Média/baixa | Sem crédito: recortar a elipse colada para dentro do contorno do perfil nesses quadros (ou desfocar levemente a borda) e remontar. Conferir com `xadrez.py`. |
| 2 | 67,13–67,43 | Sorriso aberto parado na pausa (w08, v1). | Baixa | Aceitar. |
| 3 | 0–6,6 (j1) | 0,57 com 8 q de pausa (barba). | Baixa | Assistir. |

## AD 08 (correção lote B): APROVADO (com observações)

- **s02** (`f08_s02.jpg`): em 18,13–18,53 s a boca fica **fechada** enquanto o original abre o sorriso e fala PT. O defeito do lote B saiu. s02: **0,07**.
- **"hoy":** saiu. A transcrição diz "comenzando por el primero, / el que más aprieta tu vida."
  - s14 (`f08_s14.jpg`): articula, e a pausa de 88,0–88,7 s fica fechada. s14 0,46, s15 0,07.
- **Emendas** (`e08.jpg`): 16,47 (crossfade), 19,47, 83,83, 87,40 e 90,40 s (crossfade). Sem quadro solto e sem pulo.
- **Conjunto 0,19.** As pausas de lábios entreabertos no s03 (21,47 s) e no s10 (71,80 s) são as já aceitas no lote B.
- **`revisar_ad`:** OK, es (0,99), nenhum proibido.
- **Cor (observação, `cor_08.txt`, `z_seam_lado2.jpg`):**
  - o vídeo inteiro está 16 níveis mais escuro que o original no rosto e mais frio (perde o dourado);
  - a área colada fica 7 níveis abaixo do resto do rosto, em todos os trechos;
  - lado a lado com o original salta aos olhos; sozinho, parece um vídeo mais acinzentado, sem elipse evidente;
  - não reprovo, porque o degrau fica abaixo do que se vê no 17 e no 18. Recomendo a mesma correção de cor (abaixo).

## AD 09 (correção lote B): APROVADO

- **E1** (`f09_E1.jpg`):
  - em 46,93–47,07 s a boca fica num "o" fechado e sem dentes, enquanto o original mostra os dentes. Não é mais a boca PT;
  - o "abertura 104 %" que o script acusa é esse "o" parado.
  - O q de 47,10 s (peso 0,6) mostra um leve fantasma de lábio por 1 quadro. Baixa.
- **E1 0,50, conjunto 0,14.** O O continua sem pausa (aceito no lote B).
- **`revisar_ad`:** OK, es (0,98), nenhum proibido.

## AD 10 (correção lote B): APROVADO (com observações)

- **Abertura reenquadrada** (`z10_abertura.jpg`, `z10_topo.jpg`):
  - de 0 a 9,3 s aparece só a personagem, do véu ao rosário, contra a cortina escura;
  - sem leito, idoso, tubo nem monitor;
  - "Vine a traer paz a tu corazón…" com essa imagem lê como bênção. **Risco Meta: baixo.**
- **h0** (`f10_h0.jpg`): articula, e a boca fecha de 7,9 a 9,2 s. h0 0,08. A comparação com o original não vale aqui, porque ele não está reenquadrado.
- **Conjunto 0,14.** O "quadro solto" de 9,63/9,67 s é a transição com brilho do original (falso positivo já conferido).
- **`revisar_ad`:** es (0,98), nenhum proibido.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 0–9,3 | Ampliado 2,25x: mais suave que o resto. No canto superior esquerdo aparece uma forma escura (a bolsa de soro) contra a cortina, borrada e não reconhecível. | Baixa | Aceitar, ou escurecer o canto. |

## AD 16 (correção lote B): APROVADO

- **"Pero sé rápido":** saiu. A transcrição diz "…una para cada nudo. / No dejes pasar este momento. / Hay quien no quiere… / toca el botón de abajo y recibe lo que Dios preparó para ti."
- **Buraco de 3,3 s:** saiu. Na voz ES isolada não há mais pausa de fala acima de 1,2 s depois de 69 s. Fica só a de 4,6–6,8 s, do roteiro, já anotada no lote B.
- **j1** (`f16_j1k1.jpg`):
  - articula, e a pausa de 77,70–78,30 s fica fechada;
  - em 76,20–76,47 s a boca fica num "o" fechando, diferente do original. Baixa.
  - j1 0,30.
- **k1** (78,8–87,77 s, `z16_k1.jpg`, `t16_k1.jpg`): o zoom acompanha o rosto, e o Jesus continua no quadro sem defeito (o inpaint foi só na entrada do HeyGen). k1 0,35.
- **Fim:** corte de câmera em 87,77 s, 0,6 s depois da última fala, com fade. Duração de 87,80 s.
- **Conjunto 0,21.** **`revisar_ad`:** OK, es (0,98), nenhum proibido.
- **Cor:** degrau de −2,4 no geral. O j1 (−6,8) e o k1 (−5,3) ficam um pouco mais avermelhados no nariz e nas bochechas. Numa cena de choro isso passa por natural. Anotado.

## AD 17 (correção lote B): REPROVADO (cor do gancho)

- **Compliance OK:**
  - frascos apagados sem resto (`z17_mesa.jpg`; o copo, o relógio e o celular ficam);
  - "Vine a traer **paz** a tu corazón…" confirmado na transcrição;
  - o homem sentado chorando, sem remédios nem leito, lê como aflição. Aceito.
- **Lipsync OK:**
  - s00 0,14 (`f17_s00.jpg`): articula, e a boca fica fechada de 7,8 a 9,2 s enquanto o PT fala;
  - conjunto **0,10**.
- **`revisar_ad`:** OK, es (0,99), nenhum proibido.
- **Defeito, cor do s00** (`cor_17.txt`, `f17_s00.jpg`, `z_seam_lado2.jpg`, `z_seam_17_18.jpg`):
  - no gancho, a área colada (do nariz ao queixo) fica **10,5 níveis mais escura** que as bochechas altas;
  - o rosto inteiro fica **16,6 níveis mais escuro** e puxado para o magenta (U +4,9 / +9,4 na boca);
  - na folha, o rosto do final fica rosado e o do original, pêssego;
  - os outros trechos ficam com degrau de −0,7 a −4,5, aceitável.
  - O s00 foi refeito no lote B, ainda com o pipeline antigo de leitura e gravação.

| # | Tempo | Defeito | Gravidade | Correção |
|---|---|---|---|---|
| 1 | 0–9,33 (s00) | Elipse colada mais escura e rosto magenta no gancho. | **Média** (visível) | Sem crédito: refazer só a recolocação do s00 (`ls_s00_loteB.mp4` já existe) com a leitura/gravação corrigida do AD 13 v3 (ffmpeg bt601 + `accurate_rnd`, conversão inversa exata, compensação do desvio da entrada do HeyGen) e remontar. Meta: degrau ≤ 3 no `cor.py`. |

## Brilho e cor da área colada (pedido do coordenador)

**Medida** (`cor.py` e `brilho.py`): luma Y, de 0 a 255, final − original.
- **"boca":** lábio superior + queixo, dentro da elipse.
- **"face":** bochechas altas, fora da elipse.
- **Degrau** = boca − face. Num rosto bem colado o degrau é ~0.
- O mapa `mapa_dif.py` (`z_mapa2.jpg`) confirma o formato: em todos os ADs com o pipeline antigo aparece uma elipse escura do nariz ao queixo, com borda suave.

| AD | Degrau geral | Pior trecho | Rosto vs. original | Leitura |
|---|---|---|---|---|
| 03 | +0,7 | — | −8,5 | ok |
| 13 v3 | −0,9 | w03 −2,8 | −1,7 a −4 | ok (pipeline corrigido) |
| 06 | −2,5 | w15 −7,0 / w6 −5,9 | −7,8 | ok (picos no close e no fim do zoom) |
| 16 | −2,4 | j1 −6,8 | −12,9 | anotado |
| 04 / 07 | −2,2 / −2,8 | — | −8,6 / −10,7 | ok |
| 17 (s02–s12) | −0,7 a −4,5 | | −12 a −14 | anotado |
| 05 | −3,4 | d1 −7,1 | −9,9 | anotado |
| 01 / 02 | −4,2 / −5,0 | s07 −6,0 / s09 −6,7 | −6,6 / −10,7 | anotado (imperceptível sozinho) |
| **12 / 14** | **−4,8 / −4,7** | h −6,8 / h −5,6 | −7,7 | **anotado: imperceptível** (`z_seam_lado.jpg`: sem elipse visível sem o original ao lado) |
| 10 (A–L, versão anterior) | −5,7 | | −10,5 | anotado |
| 08 | −7,2 | s16 −9,0 | **−16** | observação: vídeo mais escuro e frio no todo |
| **18** | **−8,4** | **s00 −16,3 / s15 −10,8** | **−15,9** | **visível → REPROVADO** |
| **17 (s00)** | **−10,5** | | **−16,6** | **visível → REPROVADO** |

**Critério:**
- degrau ≤ 3: imperceptível;
- 4–7: só se vê lado a lado com o original (anoto);
- ≥ ~10, ou com tom de pele visivelmente diferente na metade de baixo do rosto: visível (reprovo).

### AD 18: REPROVADO (cor)
- **s00 (gancho, 0–9,5 s):** a boca e o queixo ficam 31 níveis abaixo do original e 16 abaixo das bochechas. Em `z_seam_17_18.jpg` (2,0 e 6,5 s), sem o original ao lado, a metade de baixo do rosto aparece arroxeada e mais escura que a testa.
- **Resto do vídeo:** degrau de −6 a −11 e o rosto todo 16 níveis mais escuro que o original. Lado a lado com o original fica claro (`z_seam_lado.jpg`, 35 s).
- **Lipsync, fala e CTA:** continuam aprovados como no lote B.
- **Correção (sem crédito):** refazer a recolocação de todos os trechos a partir das saídas do HeyGen já baixadas, com a leitura e a gravação do AD 13 v3, e remontar. Se não der tempo, fazer pelo menos o s00 e o s15. Meta: degrau ≤ 3 e rosto até ~−5 do original.

### AD 12 e AD 14: mantidos APROVADOS (anotado)
- O degrau de −4,7/−4,8 é constante em todos os trechos e a borda é suave.
- No recorte de 5 s, sem comparar, não se vê elipse.
- **Recomendação** (não bloqueia): se o AD 18 for refeito com o pipeline corrigido, vale passar o 12 e o 14 pelo mesmo processo, porque usam os mesmos scripts.

### Observação geral (todos os ADs exceto o 13 v3)
- **O vídeo final fica mais escuro que o original** em 3–9 níveis no fundo e 7–16 no rosto.
- A causa é a que o agente do AD 13 achou: matriz de cor diferente na leitura (cv2, bt601) e na gravação, que escurece 2–3 níveis por passada.
- Nos ADs com mais passadas (08, 17, 18) chega a −16 e tira o tom dourado da pele.
- Não reprovo os outros por isso: sozinhos, eles parecem só um pouco mais contrastados. Mas é o ponto mais fácil de melhorar o lote inteiro sem gastar crédito.

---

## Tabela-resumo dos 18 ADs (veredito mais recente: lotes A, B e C)

| AD | Tema | Veredito | Lote | Pendências |
|---|---|---|---|---|
| 01 | TRES-BENDICIONES | **APROVADO** | A | Degrau de cor −4,2 (anotado) |
| 02 | TRES-BENDICIONES-SHOPPING | **APROVADO** | C | 4 q do "ti" sem voz em 9,53 s (baixa) |
| 03 | PADRE-ROMERO | **APROVADO** | C | — |
| 04 | ENVIDIA | **APROVADO** (obs.) | B | w12 0,66 sem PT; gancho de perfil: assistir |
| 05 | FAMILIA | **APROVADO** | C | Boca fechada parada em 35,9 e 51,6 s: assistir |
| 06 | NUDO | **APROVADO** (obs.) | C | Closes da corda e pausas de ~2 s (baixa) |
| 07 | CINTA-BLANCA | **APROVADO** (obs.) | B | Boca parada no fim (88,7–89,5 s) |
| 08 | BENDICION-DETENIDA | **APROVADO** (obs.) | C | Vídeo 16 níveis mais escuro e frio; degrau −7 |
| 09 | SERPIENTES | **APROVADO** | C | — |
| 10 | NUDO (hospital → reenquadrado) | **APROVADO** (obs.) | C | Abertura ampliada 2,25x (suave) |
| 11 | DESATADORA | **APROVADO** | piloto (aprovado pela pessoa; fora dos lotes A/B/C) | — |
| 12 | SERPIENTES-CAMPO | **APROVADO** | A (+ cor no C) | Degrau −4,8 imperceptível (anotado) |
| 13 | PAZ | **APROVADO** (obs.) | C (v3) | Xadrez sob o lábio em 35,3 e 35,7 s: corrigir de preferência |
| 14 | SERPIENTES-CASA | **APROVADO** | A (+ cor no C) | Degrau −4,7 imperceptível (anotado) |
| 15 | REGALO | **APROVADO** | B | — |
| 16 | NUDO | **APROVADO** | C | j1/k1 levemente avermelhados (anotado) |
| 17 | NUDO (quarto) | **REPROVADO** | C | Cor do gancho s00: elipse −10,5 e rosto magenta. Refazer a recolocação do s00 com o pipeline do AD 13 v3 (sem crédito) |
| 18 | SERPIENTES | **REPROVADO** | C (era APROVADO no B) | Cor: elipse −8 em tudo e −16 no gancho, metade de baixo do rosto roxa. Refazer a recolocação com o pipeline do AD 13 v3 (sem crédito) |

**Placar:** 16 aprovados (7 com observações) e 2 reprovados (17 e 18). Os dois reprovados são só de cor, corrigíveis sem crédito do HeyGen.

## Arquivos desta revisão (`_trabalho\revisao\loteC\`)
- **Scripts:**
  - `varrer.py`, `analisar.py`, `folha.py`, `emendas.py`, `trans.py` e `alinh.py` (adaptados);
  - novos: `brilho.py`, `cor.py`, `mapa_dif.py` e `xadrez.py`;
  - `rodar_revisar.ps1` e `proibidos.txt` (UTF-8).
- **Dados:** `segs_C.json`, `faces_NN.jsonl`, `escolha_NN.json`, `met_NN.txt`, `br_NN.txt`, `cor_NN.txt` e `audio\sep\htdemucs\`.
- **Folhas:**
  - AD 06: `f06_*.jpg`, `e06_a/b.jpg`, `t06_*.jpg`, `z06_*.jpg`;
  - AD 02: `f02_*.jpg`, `e02.jpg`;
  - AD 03: `f03_q282.jpg`, `t03_q282.jpg`;
  - AD 05: `f05_c1.jpg`, `z05_c1.jpg`;
  - AD 13: `f13_*.jpg`, `z13_*.jpg`;
  - AD 08: `f08_*.jpg`, `e08.jpg`;
  - AD 09: `f09_E1.jpg`;
  - AD 10: `f10_h0.jpg`, `z10_*.jpg`;
  - AD 16: `f16_j1k1.jpg`, `z16_k1.jpg`, `t16_k1.jpg`;
  - AD 17: `f17_s00.jpg`, `z17_*.jpg`;
  - cor: `z_brilho_seam.jpg`, `z_mapa1/2.jpg`, `z_seam_lado.jpg`, `z_seam_lado2.jpg`, `z_seam_17_18.jpg`.
- **`revisar_ad.py`:** `revisar\log_NN.txt` (UTF-16) e `revisar\AD NN - …_revisao.txt/.jpg`.
