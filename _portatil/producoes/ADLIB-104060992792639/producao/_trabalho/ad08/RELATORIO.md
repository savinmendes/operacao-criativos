# AD 08 — relatório (PT → espanhol neutro LATAM), 08/10/2026

## Correção de cor (08/10/2026, depois da REVISAO-LOTE-C)

A versão anterior está em `_trabalho\ad08\_antes_cor\`: vídeo, folhas, `base_lipsync`, `base_sem_legenda`, corpo, receita e relatório.

**Causa:** cada passada de leitura (cv2) e gravação (encoder padrão) escurecia ~2,3 níveis e puxava a cor para o frio. O 08 tinha 4 passadas antes do lipsync:
- LaMa da legenda;
- LaMa dos brilhos;
- colagem do lote A;
- reaplicação do lote B.

Por isso o rosto ficava −16.

**O que foi feito (sem crédito HeyGen, nenhum job novo):** `lipsync\recolocar_cor.py` refaz a `base_sem_legenda` (2935 q) e a `base_lipsync` (2921 q) **numa geração só**.
- **Base:**
  - Parte do original `UNICOS_HD\08.mp4`.
  - Só as áreas editadas pelo LaMa (legenda, seta e brilhos) vêm da base antiga, com a cor reajustada quadro a quadro: ajuste afim por canal, da base antiga para o original, medido fora da máscara.
  - A máscara é a `base_sem_legenda_mask.npy` mais os brilhos (q ≥ 2250).
  - Nenhum LaMa novo.
- **Montagem:** igual ao `lipsync\recolocar.py` + `_lote\rastreado.py aplicar`.
  - Cobertura do s01 (0–285) e clarão refeito (286–292).
  - s02–s16 colados com as trilhas e a regra dos quadros "ruins", que deu os mesmos 20 quadros.
  - Lote B por cima: f02, f14 e f15.
  - Mesmas emendas: crossfade em 1326, 1549, 494 (boca) e 2712 (boca); as outras são cortes.
- **Leitura e gravação:** iguais às do `ad13\lipsync3\comum3.py`.
- **Cor de cada trecho do HeyGen:**
  - desvio no anel de pele em volta da elipse (≈ +4,8/+8,3/+14 BGR, o maior do lote, por causa das passadas extras da entrada);
  - mais o ajuste interno pelo peso da elipse.
- **Depois:** `montar_corpo.py` e `montar_ad.py` com a mesma receita. Duração de 97,40 s, CTA em 76,84 s.

**Medidas** (`cor.py`/`brilho.py`, `loteC\escolha_08.json`; saídas em `revisao\loteC\cor_08_depois.txt`, `br_08_depois.txt` e `br_08_antes.txt`):

| | Antes | Depois |
|---|---|---|
| Degrau área colada − rosto (geral) | −7,2 | **+0,9** |
| Pior trecho | s16 −9,0 | s09 +2,5 / s16 −1,9 |
| Rosto × original | **−16,0** (U +3,9 / V −5,0: frio) | **−0,7** (U +0,1 / V +0,2) |
| Fundo × original | −9,1 | **+0,2** |

**Revisão (`revisar_ad.py --lipsync`, PowerShell, `_lote\proibidos.txt`; trechos de `chk_trechos.json` recortados do final, em `_cor_rev\`):**
- es (0,99), nenhum proibido, nenhum silêncio, nenhum salto de pts, 13 cortes, setas no último quadro.
- **Índice de pausa do conjunto:** 0,19 antes e **0,19** depois.
- Por trecho:
  - s09: 0,26 → 0,22;
  - s06: 0,42 → 0,52;
  - **s14: 0,57 → 0,69**, aviso, com só 7 quadros de pausa.
- **s14 conferido:**
  - Medido isolado, com a mesma colagem, dá 0,49. Sem correção de cor nenhuma dá 0,63. A diferença é ruído da medida com poucos quadros de pausa, não da cor.
  - Na folha de 87,9–88,7 s (antes × depois), a boca fica fechada na pausa do mesmo jeito.
- **"PROBLEMA" do s08:**
  - Antes: "a boca não mudou (10 %)", o falso positivo já registrado.
  - Agora o controle de cor bate com o original, então o "mudou" subiu para 86 %. Com isso o kit passou a acusar pela outra regra: "boca acompanha mais o original (0,37) do que o novo (0,22)".
  - As correlações são as mesmas de antes (0,38/0,21). O trecho não foi mexido além da cor e já tinha sido aceito pelo revisor (o close articula diferente do original).
- **Folha visual** (original × antes × depois): o dourado da pele voltou e não aparece elipse. O vídeo não foi aberto.

---

## Correção do lote B (08/10/2026, depois da REVISAO-LOTE-B)

A versão anterior está em `_trabalho\ad08\_antes_loteB\` (vídeo, folhas, narração, alinhamento, base_lipsync, corpo, receita, relatório).

**O que mudou**
1. **Boca PT na pausa de 18,13–18,53 s (s02).**
   - Causa: na entrada antiga o recorte rastreado pulava para o Jesus nos quadros 542–553, e o HeyGen devolveu a boca de entrada (PT).
   - Refiz 16,47–19,47 s (quadros 494–583, 90 q, sem padding) no HeyGen `speed`, com um recorte novo **rastreado e estável** (354x630, fixo, ~2,4x o rosto; detecção que pula mais de 0,5 rosto é descartada e interpolada).
   - Colado só na boca e no queixo, com crossfade de 2 quadros na emenda contínua de 494; em 584 há corte de câmera.
   - A boca fica fechada em 546–557, diferente do original. O `fechar.py` não foi usado.
2. **"hoy" (88,07–88,36 s) removido sem mexer no tempo.**
   - Usei um TTS novo, só "el que más aprieta tu vida." (27 caracteres, voz "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5`), no mesmo ponto (86,52 s), com o ganho casado (`_audio\tirar_hoy.py`). O resto da narração ficou idêntico.
   - A frase termina em 88,02 s e o b13 segue em 88,78 s, como antes.
   - Lipsync refeito em `speed`, com o mesmo recorte rastreado: s14 (2515–2621, 107 q) e o começo do s15 (2622–2711, 90 q). Há crossfade na emenda contínua de 2712; 2515 e 2622 são cortes de câmera.
3. **Remontagem:**
   - `lipsync_b\` + `_lote\rastreado.py aplicar` → `base_lipsync.mp4`, depois `montar_corpo.py` → `corpo_ad08.mp4`, depois `montar_ad.py`;
   - nenhum quadro congelado: as saídas voltaram com o número exato de quadros;
   - duração igual (97,40 s), setas desde 76,84 s até o fim.

**Roteiro:** o b12 termina agora em "…comenzando por el primero: el que más aprieta tu vida." (sem "hoy").

**Custos do lote B**
- TTS: 27 caracteres.
- HeyGen `speed`: 3 jobs, 3,0 + 3,57 + 3,0 = **9,6 s ≈ 10 créditos**.
- Com o AD 16, o total fica em ~21,5 s ≈ 21 créditos (teto 25).
- O saldo ainda mostrava 8.814 logo depois, porque a cobrança atrasa até ~1 h.

**Revisão (`revisar_ad.py --lipsync`, PowerShell, proibidos em `_lote\proibidos.txt` UTF-8 com "rápido", "hoy", "segundos")**
- es (0,99) e nenhum termo proibido: o "hoy" foi achado como ausente, e a transcrição diz "el que más aprieta tu vida.".
- Nenhum silêncio acima de 0,7 s, 13 cortes, setas no último quadro.
- **Índice de pausa do conjunto: 0,19** (15 trechos, medido no vídeo final).
- s02: **0,06** (era 0,60/0,61), corr. ES 0,50; s14: 0,57; s15: 0,06 (corr. 0,68). Os outros ficaram como antes.
- **Único "PROBLEMA" do kit: s08 "a boca não mudou (10 %)".** É falso positivo da medida de pixels (o lote B inteiro dá ~0–20 % nessa medida, como a REVISAO-LOTE-B já registrou). O s08 não foi mexido. Na folha de 6 em 6 quadros, final × original, a boca é outra e articula: quadros 12, 48, 60, 66 e 78.
- Os avisos "pixels da boca quase iguais" nos outros trechos têm a mesma causa.
- Folhas: `revisao\loteB_1em1.jpg` (1 em 1 quadro em 490–499, 542–561 e 2707–2716). Sem quadro solto, com a boca fechada na pausa.
- Log: `revisao\revisar_loteB.log`; clipes em `revisao\chk_loteB\`.

---

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 08 - ORACION-BENDICION-DETENIDA-ES-LATAM.mp4`
- 97,40 s · 720x1280 · 30 fps · 26,1 MB · sem selo · setas a partir do 1º "Toca" (76,84 s) até o fim.
- Original: 393,5 s. Fala PT até 105,7 s; depois, tela fixa com cruz e seta vermelha, sem fala, até o fim (saiu). O espanhol foi montado em fluxo contínuo (pausas de 0,42 s) e o vídeo termina 0,7 s depois da última fala, com fade de 0,3 s. As tomadas finais do original (97,7–106 s) ficaram de fora porque a fala acabou antes; são todas iguais (Desatadora com Jesus atrás).

## Roteiro em espanhol (tempos no vídeo final; voz a 1,0x)
| Tempo | Fala (DESATADORA) |
|---|---|
| 0,70–7,75 | En este momento estoy quitando de tu camino las serpientes que se enrollaron en tu vida y no dejan llegar tu bendición. |
| 8,17–12,42 | Yo soy la Desatadora de Nudos, y no fue por casualidad que vine a hablar contigo, |
| 12,84–18,22 | porque fuiste tú a quien elegí entre tanta gente, para recibir lo que estaba preparado para ti. |
| 18,64–23,42 | Hay una bendición grande separada con tu nombre, y ya está en camino hacia ti. |
| 23,84–27,71 | Pero hay un nudo apretado en medio del camino, que la detiene afuera. |
| 28,13–31,37 | Y ese nudo no lo ataste tú. No es que tu fe sea débil. |
| 31,79–38,59 | Rezaste, encendiste velas, hiciste promesas, y aun así sentías que todo se te escapaba de las manos. |
| 39,01–43,97 | La culpa nunca fue tuya. Siempre fue ese nudo. Y no se trata de rezar más. |
| 44,39–51,43 | Lo que desata el nudo de la tristeza y del cansancio es rezar de la manera correcta, exactamente como te voy a enseñar. |
| 51,85–60,22 | Y cuando ese nudo se desate, esa bendición que estaba detenida va a empezar a llegar, y tu vida entra en un tiempo de paz y de alegría. |
| 60,64–69,35 | Esa preocupación que te quita la paz se alivia, y por primera vez en mucho tiempo, sientes descanso en el corazón, sin ese peso en el pecho. |
| 69,77–75,58 | Pero presta mucha atención hasta el final, porque esta oración sagrada fue preparada con amor para ti. |
| 76,00–88,36 | Entonces, toca el botón de abajo ahora, porque te dejé un video corto y gratuito con el orden correcto de las oraciones. Una para cada nudo, comenzando por el primero: el que más aprieta tu vida. *(lote B: sem "hoy")* |
| 88,78–92,93 | No lo dejes para después. Hay quien no quiere que este secreto llegue hasta ti. |
| 93,35–96,65 | Toca el botón de abajo, y recibe lo que Dios preparó para ti. |

## Voz
- **Reaproveitada:** "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5` (Desatadora). Semelhança (Resemblyzer) da voz original do 08 com a voz original do 01, de onde vem esse clone: **0,97–0,985** (é a mesma voz). Contra "ORACAO-13 mulher": 0,93–0,96. Nenhuma voz nova, nenhuma apagada.

## Custos
- **TTS ElevenLabs:** 1.505 caracteres (15 blocos, `eleven_multilingual_v2`, 1 rodada), ≈ US$ 0,25.
- **HeyGen:** 15 jobs `speed` numa rodada só, sem refação: ~88 s de rosto (s05 completado até 3 s) ≈ **~90 créditos** pela taxa de ~1 crédito/s (teto 170). O saldo da conta ia de 8.816 para 8.814 ao terminar, mas a cobrança do `speed` chega com até ~1 h de atraso e a conta é compartilhada; conferir mais tarde.

## Lipsync (HeyGen, `mode speed`, como no LICOES-LIPSYNC.md)
- **Entrada:** recorte 9:16 que segue o rosto da Desatadora quadro a quadro (a câmera anda entre 44 e 55 s, chegando a um close). O recorte tem cerca de 2x a largura do rosto e é escalado para 720x1280. O rosto do Jesus, quando entra no recorte, foi apagado por inpaint. O vídeo leva o **áudio PT original** e o espanhol vai como `audio`. `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água. Todos voltaram com o número exato de quadros.
- **Colagem:** só uma elipse suave na boca e no queixo dela, quadro a quadro. Há crossfade de 2 quadros nas 2 emendas da mesma tomada (44,20 e 51,63 s). As outras 12 emendas caem em cortes reais. Cor bt709/tv.
- **Detecção trocada:** em 20 quadros (9 no s02, 4 no s09, 4 no s15, 2 no s13 e 1 no s07), o detector pegou o Jesus no lugar dela. Nesses quadros o rosto dela tinha saído borrado na entrada do HeyGen. Na colagem, a caixa do rosto foi interpolada e a boca veio do quadro bom vizinho (no máximo 3 quadros seguidos). Conferido na folha: não há borrão.

| Trecho | Tempo | Índice de pausa (final) | Corr. boca × ES | Kit (`checar_lipsync`) |
|---|---|---|---|---|
| s01 | 0–9,53 | — (coberto, ver abaixo) | — | — |
| s02 | 9,77–19,47 | 0,57–0,61 | 0,25 | AVISO (0,61 no kit; mudou 94%) |
| s03 | 19,47–29,27 | 0,22 | 0,34 | APROVADO |
| s04 | 29,27–38,93 | 0,24 | 0,52 | APROVADO |
| s05 | 38,93–40,97 | 0,27 | 0,33 | APROVADO (0,10 no kit) |
| s06 | 40,97–44,20 | 0,49 | 0,50 | APROVADO |
| s07 | 44,20–51,63 | 0,07 | 0,32 | AVISO (sem pausa suficiente; mudou 100%) |
| s08 | 51,63–55,13 (close) | 0,22 | 0,34 | AVISO (idem) |
| s09 | 55,13–62,47 | 0,24 | 0,38 | APROVADO |
| s10 | 62,47–72,47 | 0,39 | 0,35 | APROVADO |
| s11 | 72,47–77,33 | 0,05 | 0,48 | APROVADO |
| s12 | 77,33–80,43 | 0,09 | 0,63 | APROVADO |
| s13 | 80,43–83,83 | 0,08 | 0,54 | APROVADO |
| s14 | 83,83–87,40 | 0,44 | 0,35 | APROVADO |
| s15 | 87,40–92,30 | 0,11 | 0,59 | APROVADO |
| s16 | 92,30–97,37 | 0,11 | 0,60 | APROVADO |
| **Conjunto** | | **0,22 (revisar_ad) / 0,19 (medida própria no vídeo montado)** | | **APROVADO** (meta ≤ 0,6) |

- **s02 (aviso):** na pausa de 18,2–18,6 s ela fica com um sorriso leve, mostrando os dentes. Testei o plano B (`fechar.py`, que cola uma boca fechada) e o queixo ficou com fantasma e borrão, então foi descartado. Ficou a saída do HeyGen.

## O que saiu ou foi trocado
- **Dinheiro:**
  - "bênção financeira grande" virou "una bendición grande";
  - "o dinheiro entrava numa mão e sumia na outra" virou "sentías que todo se te escapaba de las manos";
  - "nó da escassez e da pobreza" virou "nudo de la tristeza y del cansancio";
  - "tempo de fartura e de multiplicação" virou "tiempo de paz y de alegría";
  - "aquela conta que tira o seu sono, você paga" virou "esa preocupación que te quita la paz se alivia";
  - "o que já era seu faz tempo / seu por direito" virou "lo que estaba preparado para ti / lo que Dios preparó para ti".
- **Saúde e sono:** "dorme a noite inteira sem aquele aperto no peito" virou "sientes descanso en el corazón, sin ese peso en el pecho".
- **Contagem regressiva e ameaça:**
  - "essa revelação vai ser removida / você tem poucos segundos" virou "presta mucha atención hasta el final, porque esta oración… fue preparada con amor para ti";
  - "seja rápido, não fica muito tempo no ar" virou "No lo dejes para después";
  - "hoje" saiu do "vim falar com você hoje".
- **Mantido:**
  - as serpientes no gancho, a Desatadora de Nudos, "fuiste tú a quien elegí", o nó que segura a bênção;
  - "no es que tu fe sea débil / rezaste, encendiste velas…" e "no se trata de rezar más / de la manera correcta";
  - "hay quien no quiere que este secreto llegue hasta ti" (no nível do "el enemigo no quiere…" aprovado no AD 13), o vídeo grátis com a ordem das orações e o CTA "Toca el botón de abajo".
- **Imagem:**
  - **Legenda PT** amarela (y 980–1060): removida com LaMa na GPU (`_lote\lama_base.py`, máscara justa). A boca fica em y≈480 e não foi tocada.
  - **Seta vermelha** (a partir de 77 s): removida, assim como os "brilhos" brancos em triângulo ao lado dela (2ª passada LaMa, `_tmp\tirar_brilhos.py`). As setas do CTA são as do kit.
  - **Cena das serpentes (0–9,53 s):** a Desatadora aparece de perfil, com o rosto pequeno e a boca falando PT. O HeyGen não pega perfil, então essa parte foi **coberta** com um enquadramento do próprio quadro: mãos, serpentes caindo e a luz (recorte 380x676, 1,8x). Nenhum rosto aparece nesse trecho.
  - **Clarão de transição (9,53–9,77 s):** no original, ele tinha a legenda PT lavada (o LaMa não pegava) e a boca dela já falando PT. Foi refeito como fusão do último quadro coberto para o 1º quadro com lipsync, com o mesmo clarão branco.
  - Nenhuma moeda, marca ou famoso na imagem.
- **Áudio:** narração a −16 LUFS por bloco + trilha do original (demucs `no_vocals`, −27,7 LUFS) no nível original.

## Revisão própria
- **`revisar_ad.py`** (PowerShell), com `--idioma es --idioma-residual pt`, `--proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada"` e `--lipsync` com os 15 trechos: **OK: nenhum problema**.
  - es (0,99), nenhum termo proibido, nenhum silêncio > 0,7 s, nenhum salto de pts;
  - 13 cortes, sem pares a menos de 0,3 s;
  - setas no último quadro;
  - índice de pausa do conjunto 0,22, APROVADO;
  - avisos: s02 (0,61) e s07/s08 (sem pausa suficiente);
  - a transcrição bate com o roteiro, e a passada em PT só "traduz" o espanhol.
- **Folhas de 1 em 1 quadro** em volta de todos os cortes e emendas: `revisao\cortes_1em1_a.jpg`, `_b.jpg` e `_c.jpg`. Não há quadro solto nem pulo de boca nas emendas, e o clarão refeito não tem resto de legenda.
- **Folhas do kit:** `producao\AD 08 - …_frames.jpg` e `_revisao.jpg/.txt`. O vídeo não foi aberto.

## Pontos para a pessoa olhar
1. **Gancho (0–9,5 s):** é um zoom 1,8x nas mãos e nas serpentes, sem rostos, e por isso fica mais suave que o resto. A voz diz "estoy quitando de tu camino las serpientes" sobre as serpientes caindo. Se preferir o plano aberto original, a boca de perfil dela (pequena) volta a falar PT.
2. **Clarão refeito em 9,53–9,77 s:** fica mais rosado que o original, porque parte do último quadro coberto.
3. **s02, 18,2–18,6 s:** sorriso com os dentes numa pausa curta. É o único trecho com aviso de índice.
4. **Manchas na corda:** a legenda antiga ficava em cima da corda com nós, e o inpaint deixa a corda borrada em alguns quadros. Isso fica quase todo debaixo da legenda nova.
5. **"Hay quien no quiere que este secreto llegue hasta ti":** é pressão leve, sem ameaça a quem assiste. Dá para tirar, se preferir.

## Arquivos (`_trabalho\ad08\`)
- **`_audio\`:** `orig.wav`, `demucs\`, `blocos.json`, `gerar_tts.py`, `tts\`, `montar_narracao.py`, `tempos_reais.json`.
- **Narração:** `narracao_es.wav` + `.alinhamento.json`.
- **Base sem legenda:**
  - `base_sem_legenda.mp4`: legenda + seta + brilhos removidos;
  - `base_sem_legenda_v1.mp4`: só legenda + seta;
  - `_tmp\lama_cfg.json` e `_tmp\tirar_brilhos.py`.
- **`lipsync\`:**
  - preparo e envio: `segs.py`, `rostos.py`, `preparar.py` (rastreamento), `trilhas\sNN.json`, `in\`, `put.sh`, `up.tsv`, `ids.txt`, `baixar.sh`, `out\`;
  - colagem e medida: `colar.py`, `medir.py`, `medir_out.py`, `medidas.json`, `fechar.py` (testado, não usado), `recolocar.py`.
- **Montagem e revisão:** `segmentos.json`, `base_lipsync.mp4`, `montar_corpo.py`, `corpo_ad08.mp4`, `receita_ad08.json`, `revisao\`.
