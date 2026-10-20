# AD 07 — relatório (PT → espanhol neutro LATAM), 08/10/2026

## Correção de cor (08/10/2026, depois da REVISAO-LOTE-C)

A versão anterior está em `_trabalho\ad07\_antes_cor\`: vídeo, folhas, `base_lipsync`, `base_sem_legenda`, corpo, receita e relatório.

**Causa:** a leitura dos quadros pelo cv2 e a gravação pelo encoder padrão escureciam ~2–3 níveis por passada. O 07 tinha 2 passadas no corpo (LaMa da legenda e colagem) e mais 1 no recorte enviado ao HeyGen. Como a elipse colada do 07 cobre quase o rosto inteiro (das sobrancelhas ao queixo), o rosto todo ficava −11 e a área colada −13.

**O que foi feito (sem crédito HeyGen, nenhum job novo):** `lipsync\recolocar_cor.py` refaz a `base_sem_legenda` (2170 q) e a `base_lipsync` (2147 q) **numa geração só**.
- **Base:**
  - Parte do original `UNICOS_HD\07.mp4`.
  - Só a área editada pelo LaMa (legenda PT) vem da base antiga, com a cor reajustada quadro a quadro: ajuste afim por canal, da base antiga para o original, medido fora da máscara na faixa y 700–1100. A base antiga estava ~2–3 níveis mais escura que o original fora da legenda.
  - A máscara é a `base_sem_legenda_mask.npy` dilatada 19 px. Nenhum LaMa novo.
- **Montagem:** igual ao `lipsync\recolocar.py`.
  - Mesmas saídas do HeyGen (`out\ls_sNN.mp4`; o s08 é o `ls_s08g`, mesmo arquivo), mesmas caixas (`segmentos.json`), mesma elipse e o mesmo canto do Jesus (`colar.mascara`), mesma reamostragem (`colar.reamostrar`; todos voltaram com o nº exato de quadros, o s12 cortado em 28 q como antes).
  - Quadros 0–3 = 1º quadro colado do s01.
  - Mesmas emendas: cortes em 201, 906 e 2119; crossfade de 2 q em 341, 507, 645, 1083, 1217, 1407, 1686 e 1927.
- **Leitura e gravação:** iguais às do `ad13\lipsync3\comum3.py` (ffmpeg bt601 com `accurate_rnd`, conversão inversa exata, etiqueta bt709/tv só no bitstream). crf 12 na base sem legenda e 14 na base lipsync, como antes.
- **Cor de cada trecho do HeyGen:**
  - desvio (mediana) num anel em volta da elipse, fora dela, dentro da caixa e fora do canto do Jesus: ≈ +4/+4/+7 BGR, igual em todos os trechos;
  - mais o ajuste interno (mediana no miolo da elipse, ≈ −1/+3/+2,5), aplicado com o peso da elipse.
- **Depois:** `montar_corpo.py` e `montar_ad.py` com a mesma receita. Duração 89,50 s, CTA em 70,40 s, legenda igual.

**Medidas** (`revisao\loteC\cor.py`/`brilho.py`, `loteB\escolha_07.json`; saídas em `revisao\loteC\cor_07_antes.txt`, `cor_07_depois.txt`, `br_07_antes.txt` e `br_07_depois.txt`):

| | Antes | Depois |
|---|---|---|
| Degrau área colada − rosto (geral, `brilho.py`) | −2,5 | **−0,7** |
| Pior trecho | s01 −5,6 / s08 −4,0 | s01 −2,8 / s04 +2,3 |
| Rosto × original | **−10,8** (U +2,8 / V −2,6) | **−0,8** (U +0,5 / V +0,1) |
| Área colada × original | −13,2 | −1,4 |
| Fundo × original | −3,5 | **+0,4** (s10–s12 +2,0 por causa das setas) |
| Mediana base_lipsync − original (`lipsync\degrau_mediana.py`): miolo / anel / degrau | −11 / −6 / −5 | **−1 / 0 / −1** |

**Revisão (`revisar_ad.py --lipsync`, PowerShell, `_lote\proibidos.txt`; 12 trechos de `_cor_rev\trechos.json` recortados do final pelo `_lote\chk_final.py`, rosto forçado pelo `rostos.json`):**
- es (0,99), nenhum proibido, nenhum silêncio, nenhum salto de pts, 1 corte, setas no último quadro.
- **Índice de pausa do conjunto:** 0,21 antes e **0,17** depois, medido igual nos dois finais.
- Por trecho, igual ou melhor, exceto s05 0,18 → 0,19 e s10 0,16 → 0,19. s08: 0,58 → 0,38; s09: 0,17 → 0,08; s11: 0,35 → 0,23 (o aviso "pixels quase iguais ao original" sumiu: o "mudou" subiu de 30–48 % para 86–99 % em todos, porque a cor agora bate com o original).
- **"PROBLEMA" do s12** (índice 2,47 antes, 2,58 depois): é o ponto já registrado (boca entreaberta parada de 88,67 s ao fim, sob o fade; revisão do lote B, gravidade baixa). Não vem da cor e já estava no anterior com os mesmos trechos.
- Avisos s04 e s07: trechos sem pausa, como antes.
- Logs: `_cor_rev\revisar_antes.log` (anterior, sem whisper) e `revisar_depois.log`.
- **Folha visual** `_cor_rev\folha_cor.jpg` (original × antes × depois, 8 tempos, quadro inteiro e zoom no rosto): o tom dourado da pele voltou e não aparece elipse. O vídeo não foi aberto.

---

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 07 - ORACION-CINTA-BLANCA-ES-LATAM.mp4`
- 89,50 s · 720x1280 · 30 fps · 26,3 MB · sem selo · setas a partir do 1º "Toca" (70,40 s) até o fim.
- Original: 126,6 s (24 fps). Fala PT até 111,2 s e depois tela final sem fala (saiu). O espanhol é mais curto que o PT e foi montado em fluxo contínuo (pausas de 0,42 s entre frases); o vídeo termina 0,7 s depois da última fala, com fade de 0,3 s. O plano é fixo (porta, Desatadora com Jesus atrás), então encurtar não corta nenhuma cena com sentido próprio.

## Roteiro em espanhol (tempos no vídeo final; voz a 1,0x)
| Tempo | Fala (DESATADORA) |
|---|---|
| 0,20–3,71 | En el nombre del Padre, del Hijo y del Espíritu Santo. |
| 4,40–6,85 | Yo levanto esta cinta blanca de la Desatadora. |
| 7,60–11,41 | Yo corto la envidia, el mal de ojo y el nudo que ató tu camino. |
| 11,83–14,01 | Y declaro paz y bendición sobre tu casa. |
| 14,43–20,90 | Yo soy la Desatadora de Nudos. Quédate conmigo hasta el final, porque este video es la mano que Dios te extiende. |
| 21,32–26,65 | Esta cinta y esta oración guardan una revelación que estuvo escondida de ti toda la vida. |
| 27,07–40,43 | Es una bendición del tamaño de la preocupación que te quita el sueño. Cuando hagas esta oración, vas a sentir que algo empieza a cambiar. Esta cinta blanca es la señal de que Dios te escuchó. |
| 40,85–50,50 | La última mujer que escuchó esta oración vivía cansada y sin esperanza. A la mañana siguiente, despertó con una paz en el corazón que no sentía hace mucho tiempo. |
| 50,92–58,37 | Dios ya firmó tu bendición allá arriba, con tu nombre escrito en ella. Por eso la Desatadora vino a cortar ese nudo ahora. |
| 58,79–64,35 | La envidia de alguien que se sienta a tu mesa quiere apagar tu alegría. Así que escúchame con atención. |
| 64,77–69,99 | Esta oración de nueve palabras te muestra cuál de los nueve nudos está apretando tu vida. |
| 70,41–80,04 | Toca el botón de abajo y recibe gratis las nueve palabras. En el video te muestro el orden correcto para rezar, comenzando por el nudo que más aprieta tu camino. |
| 80,46–88,74 | Presta atención: esta oración fue preparada para ti, y este es tu momento. Toca el botón de abajo ahora. |

## Voz
- **Reaproveitada:** "ORACAO-11 mulher" `UNDKAyEJ2rTv99l7gCy5` (Desatadora). Semelhança (Resemblyzer) da voz original do 07 com a voz original do 01 (fonte do mesmo clone): 0,89–0,90 — mesmo nível do AD 01 (0,887), que reusou o clone. Contra "ORACAO-13 mulher": 0,87–0,89. Nenhuma voz nova, nenhuma apagada.

## Custos
- **TTS ElevenLabs:** 1.337 caracteres (13 blocos, `eleven_multilingual_v2`, 1 rodada só), ≈ US$ 0,22.
- **HeyGen:** saldo da conta 8.839 → 8.816 (−23) ao fechar o vídeo, mas a cobrança do `speed` chega com até ~1 h de atraso e a conta é compartilhada com os outros ADs. **Estimativa pelo uso:** ~118 s de lipsync (12 trechos speed = 93 s, mais 3 refações do s08 de 7,9 s cada: speed igual, precision e speed com recorte maior) ≈ 110–120 créditos (teto 170).

## Lipsync (HeyGen, `mode speed`, conforme LICOES-LIPSYNC.md)
- Entrada recortada só no rosto da Desatadora (270x480 escalado 2,67x; o canto com o rosto do Jesus foi apagado por inpaint), com o **áudio PT original** no vídeo e o ES como `audio`. `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água. Todos os trechos voltaram com o número exato de quadros (24 fps), sem reamostrar.
- 12 trechos de 1,2 a 11,6 s, sem atravessar os cortes de câmera (8,375 s, 37,75 s e 88,29 s, além de uma mini-tomada nos quadros 0–3).
- Colagem: só uma elipse suave na boca/queixo da Desatadora; crossfade de 2 quadros nas emendas da mesma tomada; bt709/tv.

| Trecho | Tempo | Índice de pausa (colado) | Corr. boca × ES | Kit (`checar_lipsync`) |
|---|---|---|---|---|
| s01 | 0,17–8,37 | 0,04 | 0,64 | APROVADO |
| s02 | 8,37–14,21 | 0,05 | 0,69 | APROVADO |
| s03 | 14,21–21,12 | sem pausa | 0,56 | AVISO (sem pausa; boca mudou 100%) |
| s04 | 21,12–26,87 | sem pausa | 0,48 | AVISO (idem) |
| s05 | 26,87–37,75 | 0,15 | 0,49 | APROVADO |
| s06 | 37,75–45,12 | 0,03 | 0,54 | APROVADO |
| s07 | 45,12–50,71 | sem pausa | 0,48 | AVISO (idem) |
| s08 | 50,71–58,62 | 0,45 (4 q de pausa) | 0,37 | AVISO (sem pausa suficiente; boca mudou 100%) |
| s09 | 58,62–70,25 | 0,06 | 0,35 | APROVADO |
| s10 | 70,25–80,29 | sem pausa | 0,32 | AVISO (idem) |
| s11 | 80,29–88,29 | 0,17 | 0,40 | APROVADO |
| s12 | 88,29–89,46 | (ver ponto 2) | 0,61 | AVISO |
| **Conjunto** | | **0,21 (revisar_ad) / 0,20 (medida própria)** | | **APROVADO** (meta ≤ 0,6) |

- **s08 deu trabalho:** com o recorte 270x480, o HeyGen devolveu a boca original 3 vezes (speed, speed de novo e precision — "mudou 0%"). Com um recorte maior (324x576) passou: boca mudou 100%, corr. 0,34. Ficou essa versão (`out/ls_s08g.mp4`).

## O que saiu ou foi trocado
- **Dinheiro:** "o nó que amarrou o teu dinheiro" → "el nudo que ató tu camino"; "profetizo fartura" → "declaro paz y bendición"; "dinheiro farto do tamanho da dívida… cai na tua conta antes do sol nascer" → "una bendición del tamaño de la preocupación que te quita el sueño… vas a sentir que algo empieza a cambiar"; "o nó que trava o teu dinheiro" → "el nudo que más aprieta tu camino"; "roubar o que é teu por direito" → "apagar tu alegría".
- **Depoimento com pessoa e valor:** "dona Marlene, 58 anos, de Sorocaba… rescisão de R$ 3.900" → "La última mujer… vivía cansada y sin esperanza… despertó con una paz en el corazón" (sem nome, cidade nem dinheiro; no nível do AD 13 aprovado).
- **Ameaça / pressão:** "nem penso em pular / pular é empurrar a mão de Deus" → "Quédate conmigo hasta el final, porque este video es la mano que Dios te extiende"; "se não cair, eu queimo essa fita e nunca mais rezo" → "Esta cinta blanca es la señal de que Dios te escuchó"; "é a última vez que rezo de graça" saiu; "se pular, as nove palavras somem para sempre" → "esta oración fue preparada para ti, y este es tu momento"; "nesse minuto / num minuto" saiu.
- **Mantido:** sinal da cruz, a cinta branca da Desatadora, o corte da inveja e do mau-olhado, "Dios ya firmó tu bendición… con tu nombre", a inveja de quem senta à mesa, a "oración de nueve palabras", os nove nós, "gratis" e o CTA "Toca el botón de abajo".
- **Imagem:** legenda PT amarela (y 860–945) removida com LaMa na GPU (`_lote\lama_base.py`, máscara justa); boca em y≈600, não tocada. Nenhuma moeda, marca ou famoso na imagem. A tela final sem fala saiu no corte.
- **Áudio:** narração a −16 LUFS por bloco + trilha do original (demucs `no_vocals`, −30 LUFS) no nível original.

## Revisão própria
- `revisar_ad.py --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada" --lipsync <12 trechos>` (PowerShell): **OK: nenhum problema**. es (0,99), nenhum termo proibido, nenhum silêncio > 0,7 s, nenhum salto de pts, 1 corte de cena sem pares < 0,3 s, setas no último quadro, índice de pausa do conjunto 0,21 APROVADO. Avisos só de "trecho sem pausa" (boca mudou 100% em todos). A passada em PT só "traduz" o espanhol (sem fala PT residual). A transcrição bate com o roteiro.
- Folhas de 1 em 1 quadro: `revisao\cortes_1em1.jpg` (início, 8,375 s, 37,75 s, 88,29 s) e `revisao\emendas_1em1.jpg` (8 emendas da mesma tomada): sem quadro solto, sem pulo de boca nas emendas.
- Folhas do kit: `producao\AD 07 - …_frames.jpg` e `_revisao.jpg/.txt`. O vídeo não foi aberto.

## Pontos para a pessoa olhar
1. **Início (0–0,17 s):** os 4 primeiros quadros do original são uma mini-tomada com a boca em PT; viraram o 1º quadro do s01 parado (0,17 s, antes da fala).
2. **Final (88,29–89,46 s):** é uma tomada curta do original que começa sorrindo, passa por uma transição tipo "morph" (já do original, ~88,5 s) e termina com a boca entreaberta, olhos arregalados. O "ahora" cai no começo dela; depois da fala a boca fica entreaberta, sem articular. O índice desse pedacinho dá alto porque compara com o sorriso fechado de outra tomada.
3. **Testemunho:** "La última mujer… despertó con una paz en el corazón" é depoimento com resultado emocional (paz), como no AD 13. Se quiser zero depoimento, dá para trocar o bloco 40,85–50,50 s (TTS + 2 trechos de lipsync).
4. **Duração:** 89,5 s contra 111 s de fala no original — o espanhol ficou mais enxuto depois de tirar dinheiro, ameaça e o depoimento com valor.
5. **"te quita el sueño":** expressão de preocupação, não promessa de saúde; vale confirmar se está ok para a política.

## Arquivos (`_trabalho\ad07\`)
- `_audio\`: `orig.wav`, `demucs\`, `blocos.json`, `gerar_tts.py`, `tts\`, `montar_narracao.py`, `tempos_reais.json`.
- `narracao_es.wav` + `.alinhamento.json`; `base_sem_legenda.mp4` (+ `_mask.npy`); `_tmp\lama_cfg.json`.
- `lipsync\`: `segs.py`, `rostos.py`, `preparar.py`, `in\` (pt_/es_), `put.sh`, `up*.tsv`, `ids*.txt`, `baixar.sh`, `out\ls_*.mp4`, `colar.py`, `medir.py`, `medir_out.py`, `medidas.json`, `recolocar.py`.
- `segmentos.json`, `base_lipsync.mp4`, `montar_corpo.py`, `corpo_ad07.mp4`, `receita_ad07.json`, `revisao\`.
