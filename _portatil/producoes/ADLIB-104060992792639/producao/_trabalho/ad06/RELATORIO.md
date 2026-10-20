# AD 06: relatório (lote PT → espanhol neutro LATAM, 08/10/2026)

## Correção de cor (08/10/2026, depois da REVISAO-LOTE-C)

A versão anterior está em `_trabalho\ad06\_antes_cor\`: vídeo, folhas, `base_lipsync`, `base_sem_legenda`, corpo, receita e relatório.

**Causa:** a `base_sem_legenda` tinha uma passada só, mas o `recolocar.py` a lia pelo cv2 com a matriz bt709 (arquivo etiquetado bt709, gravado em bt601) e regravava pelo encoder padrão. Por isso o fundo ficava −4,5 e o rosto −7,8. Já as saídas do HeyGen (sem etiqueta) eram lidas em bt601, e isso gerava o degrau da elipse (−2,5; w15 −7,0, w6 −5,9).

**O que foi feito (sem crédito HeyGen, nenhum job novo, nenhum LaMa novo):** `lipsync
ecolocar_cor.py` refaz a `base_sem_legenda` e a `base_lipsync` (2465 q cada, 24 fps) **numa geração só**.
- **Base (= `_tmp\montar_base.py`):**
  - Parte do original `UNICOS_HD\06.mp4`.
  - Na faixa y 740–1090 entram os PNGs do LaMa já calculados (`_tmp\lama`, `_tmp\mask`), só na máscara: legenda PT, setas e brilhos, e o clarão 205–212 do `lama_flash.py`.
  - A mesma borda suave e a mesma EMA (0,65/0,35) zerada nos cortes.
  - Cada PNG passa por um ajuste afim por canal, do LaMa para o original, medido fora da máscara. Na média, o ganho é 1,00 e o offset é +1,1/+1,5/+0,9 BGR (2459 quadros).
- **Montagem (= `lipsync
ecolocar.py`):**
  - As mesmas saídas `out\ls_<n>.mp4`, com os mesmos quadros (os 17 trechos voltaram com o mesmo número de quadros de antes).
  - A mesma elipse do nariz ao queixo, detectada por MediaPipe na saída lida pelo cv2, como antes.
  - O w6 usa as mesmas caixas (`boxes_w6.json`).
  - Os mesmos closes da corda do `plano.json`: w4 no próprio quadro e w11 nos quadros 1720+ da base nova, em memória.
  - O mesmo crossfade linear w5/w6 (q1125–1134).
- **Leitura e gravação:** iguais às do `ad13\lipsync3\comum3.py`.
- **Cor de cada trecho do HeyGen:**
  - desvio no anel de pele em volta da elipse (≈ +1/+3,2/+4,8 BGR; no w6 +3,1/+5,7/+8,8, porque a entrada rastreada tinha mais uma passada);
  - mais o ajuste interno pela **mediana no miolo da elipse**, aplicado com o peso da elipse.
  - Na 1ª tentativa usei os 2 pontos fixos do AD 08 (filtro e queixo). No v1 e no w17 eles caíam na sombra do lábio PT e deixavam a boca −3. A versão final usa a mediana (log da 1ª em `lipsync
ecolocar_cor_v1pontos.log`).
- **Conferência da montagem** (`_cor_rev\verif_geo.py`): na base nova × antiga, com a cor tirada, a diferença na boca é de 3,2–5,5 contra 2,4–3,4 fora dela. A diferença vem só da correção de cor, e não há quadro trocado nem elipse deslocada.
- **Depois:** `montar_corpo.py` e `montar_ad.py` (kit) com a mesma receita. 102,70 s, 26,6 MB, CTA em 76,67 s.

**Medidas** (`cor.py`/`brilho.py`, `loteC\escolha_06.json`; em `revisao\loteC\cor_06_antes/depois.txt`, `br_06_antes/depois.txt`, `med_06_antes/depois.txt`):

| | Antes | Depois |
|---|---|---|
| Degrau área colada − rosto (geral, cor.py / brilho.py) | −2,5 / −2,4 | **−0,6 / −0,6** |
| Pior trecho (cor.py) | w15 −7,0 / w6 −5,9 | w15 −5,6 (brilho −3,4) / w8 −1,4 |
| Mediana elipse − anel (base_lipsync, `_cor_rev\degrau_mediana06.py`) | −2,0 (w6 −4,0) | **−1,0** (nenhum trecho abaixo de −1) |
| Rosto × original | −7,8 (U +2,2 / V −2,5) | **−0,1** (U +0,2 / V +0,1) |
| Fundo × original | −4,5 | **+0,3** |

- **w15:** o resto vem só da caixa do queixo do `cor.py`: −4,0 na média e −3,5 na mediana. O lábio superior fica em −2,2 e a bochecha baixa, dentro da elipse, em 0,0. A mediana da elipse inteira dá −1,0. É a forma da boca do HeyGen (lábio de baixo e sombra em outro lugar), não um degrau de cor. Na folha não aparece elipse.

**Revisão (`revisar_ad.py --lipsync`, PowerShell, `_lote\proibidos.txt`; 16 trechos de `_cor_rev\trechos.json` recortados do final com `_lote\chk_final.py`, em `_cor_rev\`):**
- es (0,96), nenhum proibido, nenhum silêncio > 0,7 s, sem salto de pts, 15 cortes sem pares a < 0,3 s, setas no último quadro: **OK, nenhum problema**.
- **Índice de pausa do conjunto:** 0,11 antes e **0,12** depois. Avisos em w5 e w16 (sem pausa), iguais aos de antes.
- O "mudou" subiu de 34–86 % para 68–100 %, porque o controle de cor agora bate com o original.

**Folhas** (`_cor_rev\folha_cor_1.jpg`, `folha_cor_2.jpg`, `folha_cor_bocas.jpg`; original × antes × depois):
- a pele voltou ao tom dourado do original e não aparece elipse;
- os closes da corda (38,8 e 81,0 s), o clarão (8,6 s, sem legenda PT) e as setas (90 s, sem seta antiga) estão iguais aos de antes.

O vídeo não foi aberto.

---

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 06 - ORACION-NUDO-ES-LATAM.mp4`
- 102,70 s, 720x1280, 30 fps (fonte de 24 fps), AAC, 26,6 MB, sem selo. Setas a partir do 1º "Toca" (76,67 s) até o fim. Legenda ES pelo alinhamento em y 1535 (escala 1080), na altura da legenda PT antiga.
- O original tem 392 s: depois da última fala (~104,4 s) vem uma tela parada da cruz com setas até o fim. Saiu tudo isso; o vídeo fecha 0,7 s depois da última fala ES (102,00 s), com fade de 0,3 s.
- Tema escolhido: NUDO (o nó que segura a bênção).

## Roteiro em espanhol (tempos no vídeo final)
| Tempo | Fala (Desatadora) |
|---|---|
| 0,44–7,70 | En este momento, estoy quitando de tu camino las serpientes que se enredaron en tu vida, y que no dejan que tu bendición llegue hasta ti. |
| 8,73–18,42 | Yo soy la Desatadora de Nudos, y no fue por casualidad que vine a hablar contigo. Fuiste tú a quien elegí entre tanta gente para recibir lo que fue preparado para ti. |
| 18,50–22,66 | Hay una bendición grande preparada con tu nombre, y ya está en camino hacia ti. |
| 24,06–29,47 | Pero hay un nudo apretado en medio del camino que la detiene afuera, y ese nudo no lo ataste tú. |
| 30,45–38,33 | No es que tu fe sea débil. Rezaste, encendiste velas, hiciste promesas, y aun así tu corazón no encontraba descanso. |
| 38,46–45,44 | La culpa nunca fue tuya. Siempre fue ese nudo. Y se desata con la oración en el orden correcto, como te voy a enseñar. |
| 45,58–50,32 | No se trata de rezar más. Lo que desata ese nudo es rezar de la manera correcta. |
| 51,23–58,89 | Y cuando ese nudo se desate, la bendición que estaba detenida empezará a llegar, y tu vida entrará en un tiempo de paz y de alegría. |
| 60,93–68,18 | Esa preocupación que te quita el sueño se alivia, y por primera vez en mucho tiempo, descansas sin ese peso en el pecho. |
| 68,46–75,53 | Pero presta mucha atención hasta el final, porque este momento es para ti, y esta oración sagrada fue preparada con amor para ti. |
| 76,05–83,02 | Entonces toca el botón de abajo ahora, porque te dejé un video corto y gratuito con el orden correcto de las oraciones, |
| 84,03–88,56 | una para cada nudo, comenzando por el primero: el que más aprieta tu vida. |
| 90,65–97,75 | No dejes pasar este momento. El enemigo no quiere que esta oración llegue hasta ti, pero yo vine hasta aquí solo por ti. |
| 99,06–102,00 | Toca el botón de abajo y recibe lo que fue preparado para ti. |

Velocidade 1,0x em todos os blocos. As frases de urgência seguem a correção já aprovada no AD 13 v2.

## Voz (ElevenLabs, nenhuma nova, nenhuma apagada)
- **"ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc`.** Resemblyzer, voz do 06 (demucs) contra a fonte do clone do 13: **0,95** (9–105 s) e 0,93 (cena do varal); contra "ORACAO-11 mulher": 0,86. É a mesma voz do AD 13.
- O Jesus atrás não fala neste AD.

## Custos
- **TTS:** 1.749 caracteres (14 blocos + 2 blocos refeitos para preencher a cena: b0 e b12), cerca de US$ 0,29. No roteiro final: 1.492.
- **HeyGen (lipsync `speed`):** 20 jobs somando ~116 s de entrada (18 trechos + 2 refações de w4 e w11). Pela regra de ~1 crédito/s, **~116 créditos** (teto 170).
  - Saldo medido: 8.829 antes do AD 04 → 8.814 ao fechar AD 04 + AD 06. A cobrança do speed chega com até 1 h de atraso e a conta é compartilhada, então o delta ainda não mostra o gasto real.

## Lipsync (HeyGen `speed`, entrada recortada só no rosto da Desatadora, sem os olhos do Jesus; áudio PT no vídeo, ES como `audio`; sem duração dinâmica, mesmo formato, cfr, sem marca d'água)
- Recortes 9:16: plano aberto A 234x416 em (318,250); plano B 252x448 em (316,220); varal 252x448 em (310,380); **w6 (zoom de câmera 51–54 s) com recorte que segue o rosto quadro a quadro** (`lipsync\rastrear.py`, caixas em `boxes_w6.json`), desfeito na colagem.
- Colagem só do nariz ao queixo (elipse suave que segue a boca). Todos voltaram com o número exato de quadros (trechos < 3,2 s completados e só os quadros reais usados).
- Medidos com `checar_lipsync.py --rosto` no trecho colado:

| Trecho | Tempo | Mudou | Índice de pausa | Corr. ES (PT) | Veredito |
|---|---|---|---|---|---|
| v1 (varal) | 0,00–8,71 | 97 % | 0,07 | 0,51 (0,26) | APROVADO |
| w1 | 8,71–18,42 | 85 % | 0,06 | 0,34 (0,04) | APROVADO |
| w2 | 18,42–28,21 | 95 % | 0,15 | 0,39 | APROVADO |
| w3 | 28,21–37,88 | 91 % | 0,27 | 0,37 | APROVADO |
| w4 | 37,88–39,92 | 98–100 % | — | 0,19–0,21 (0,37) | **REPROVADO 2x** (o 2º com recorte mais justo) → **boca coberta**: close nas mãos com a corda de nós do próprio quadro (recorte 225,560,320,569), áudio intacto |
| w5 | 39,92–47,29 | 95 % | — | 0,19 (0,12) | AVISO (sem pausa); na folha `lipsync\out\folha_w5.jpg` fecha nas pausas de 0,2 / 1,5 / 5,6 / 7,3 s |
| w6 (zoom) | 46,88–54,08 | 100 % | 0,06 | 0,50 | APROVADO |
| w7 | 54,08–61,42 | 97 % | 0,07 | 0,62 | APROVADO |
| w8 | 61,42–71,42 | 94 % | — (4 q) | 0,23 (0,26) | AVISO; na folha `folha_w8.jpg` fecha nas pausas de 2,3 / 3,5 / 6,3–6,9 / 9,2 s |
| w9 | 71,42–76,29 | 99 % | 0,03 | 0,56 | APROVADO |
| w10 | 76,29–79,38 | 100 % | 0,04 | 0,69 | APROVADO |
| w11 | 79,38–82,79 | 85–89 % | — | 0,05–0,07 (0,00) | **REPROVADO 2x** → **boca coberta**: close na corda de nós tirado de quadros da mesma cena antes das setas originais (1720–1801), para não ampliar a mancha da seta removida |
| w12 | 82,79–86,33 | 92 % | 0,10 | 0,57 | APROVADO |
| w13 | 86,33–91,25 | 94 % | 0,06 | 0,73 | APROVADO |
| w14 | 91,25–96,63 | 95 % | 0,05 | 0,46 | APROVADO |
| w15 | 96,63–99,21 | 81 % | 0,09 | 0,66 | APROVADO |
| w16 | 99,21–100,54 | 84 % | — | 0,33 (0,05) | AVISO (1,3 s, sem pausa) |
| w17 | 100,54–102,70 | 90 % | 0,14 | 0,53 | APROVADO |

- **Índice de pausa do conjunto (16 trechos medidos): 0,10** (meta ≤ 0,6).
- w5 e w6 se sobrepõem 10 quadros (46,88–47,29 s) na mesma tomada: crossfade linear. As outras emendas caem em cortes de câmera.
- Nenhum quadro final tem boca falando português: todos os rostos falando estão em lipsync ou cobertos (w4, w11).

## O que saiu ou foi trocado
- **Dinheiro:**
  - "uma bênção financeira grande separada com o seu nome, já saiu" virou "una bendición grande preparada con tu nombre, y ya está en camino";
  - "o dinheiro entrava numa mão e sumia na outra" virou "tu corazón no encontraba descanso";
  - "o nó da escassez e da pobreza" virou "ese nudo";
  - "tempo de fartura e de multiplicação" virou "tiempo de paz y de alegría";
  - "aquela conta que tira o seu sono você paga" virou "esa preocupación que te quita el sueño se alivia".
- **Contagem regressiva e ameaça:**
  - "essa revelação vai ser removida e você tem poucos segundos" virou "presta mucha atención hasta el final, porque este momento es para ti…";
  - "seja rápido, uma revelação dessas não fica muito tempo no ar" virou "No dejes pasar este momento";
  - "tem quem não queira que esse segredo chegue até você" virou "El enemigo no quiere que esta oración llegue hasta ti, pero yo vine hasta aquí solo por ti" (mesmo nível do AD 13 aprovado).
- **"Direito" e "hoje":** "receber o que já era seu faz tempo" / "o que já é seu por direito" viraram "lo que fue preparado para ti"; "vim falar com você hoje" e "a sua vida hoje" perderam o "hoje".
- **Saúde:** "dorme a noite inteira sem aquele aperto no peito" virou "descansas sin ese peso en el pecho".
- **Mantidos:** a cena das serpentes no varal, a Desatadora com o Jesus atrás, o nó apretado, "no es que tu fe sea débil… rezaste, encendiste velas", "no se trata de rezar más / de la manera correcta", o vídeo "corto y gratuito con el orden correcto de las oraciones, una para cada nudo" e o CTA "Toca el botón de abajo".
- **Imagem:** não há moeda, marca nem famoso do Brasil; nenhuma cena trocada.
- **Tela:** legenda PT amarela (y 982–1064) e setas vermelhas do original com os brilhos (a partir de 76,4 s, em cima da corda branca) removidas com LaMa na GPU, máscara justa; os brilhos foram detectados pelo que pisca contra a mediana de ±6 quadros, para não apagar a corda. No clarão da transição (8,5–8,9 s) a legenda tingida foi refeita com máscara de caixa. A tela final da cruz saiu no corte.
- **Áudio:** narração a −16 LUFS por bloco + fundo do demucs (`no_vocals`, −27 LUFS, sem fala residual) no nível original.

## Revisão própria
- `revisar_ad.py --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada" --lipsync <16 trechos>` (PowerShell): **OK: nenhum problema encontrado.**
  - idioma es (0,96); nenhum termo proibido; a transcrição bate com o roteiro ("Resaste" é o whisper para "Rezaste"); a passada em pt só traduz o espanhol;
  - nenhum silêncio > 0,7 s, sem salto de pts, 15 cortes sem pares a menos de 0,3 s, setas no último quadro;
  - índice de pausa do conjunto **0,10 → APROVADO**; avisos (sem pausa suficiente para o índice) em w5, w8 e w16, conferidos na folha.
- **Emendas de 1 em 1 quadro em volta dos 17 cortes:** `_tmp\emendas_1.jpg` a `emendas_3.jpg`. Nenhum quadro solto; os closes da corda entram e saem nos cortes do original.
- Folhas: `producao\AD 06 - ORACION-NUDO-ES-LATAM_frames.jpg`, `_revisao.jpg`, `_revisao.txt`; bocas em `lipsync\out\folha_w4.jpg`, `folha_w5.jpg`, `folha_w8.jpg`, `folha_w11.jpg`.
- O vídeo não foi aberto (fica para o revisor independente).

## Pontos para a pessoa olhar
1. **Closes da corda (37,9–39,9 s e 79,4–82,8 s):** substituem o rosto onde o lipsync não passou. São zoom de ~2,3x no próprio vídeo, um pouco mais suaves que o resto. O segundo usa a corda de alguns segundos antes (as mãos não continuam o movimento exato do plano anterior).
2. **Zoom de câmera 51–54 s:** lipsync com recorte que acompanha o rosto; vale olhar a boca no close.
3. **Corda na região das setas antigas (76–102 s):** onde a seta original cobria a corda sobra uma leve mancha do LaMa, quase toda embaixo das setas novas.
4. **"El enemigo no quiere…"**: mantido no nível do AD 13 aprovado; avaliar contra a política do Meta.

## Arquivos de trabalho (`producao\_trabalho\ad06\`)
- Áudio: `_audio\blocos.json`, `gerar_tts.py`, `tts\`, `montar_narracao.py`, `palavras_pt.json`, `demucs\`.
- Base: `_tmp\lama06.py`, `_tmp\lama_flash.py`, `_tmp\montar_base.py` → `base_sem_legenda.mp4` (já cortado em 102,7 s).
- Lipsync: `lipsync\segs.json`, `preparar.py`, `rastrear.py`, `boxes_w6.json`, `recolocar.py`, `plano.json`, `medir.sh`, `folha.py`, `ids.txt`, `ids2.txt`, `in\`, `out\`.
- Montagem: `base_lipsync.mp4`, `montar_corpo.py`, `corpo_ad06.mp4`, `receita_ad06.json`.
