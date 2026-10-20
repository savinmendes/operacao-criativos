# AD 12: relatório (PT → espanhol neutro LATAM), 08/10/2026

## Correção de cor (08/10/2026, depois da REVISAO-LOTE-C)

A versão anterior está em `_trabalho\ad12\_antes_cor\`: vídeo, folhas, `base_lipsync`, `base_sem_legenda`, corpo, receita e relatório.

**Causa:** a leitura dos quadros pelo cv2 e a gravação pelo encoder padrão escureciam ~2,3 níveis por passada. Eram 2 passadas no corpo (LaMa e colagem) e mais 1 no recorte enviado ao HeyGen, que foi o que deixou a boca mais escura.

**O que foi feito (sem crédito HeyGen, nenhum job novo):**
- `lipsync\recolocar_cor.py 12` refaz a `base_sem_legenda` e a `base_lipsync` **numa geração só**, a partir de:
  - o original `UNICOS_HD\12.mp4`;
  - as faixas LaMa já calculadas (`_tmp\lama`), corrigidas pelo desvio medido fora da máscara;
  - as saídas do HeyGen já baixadas (`lipsync\out\ls_*.mp4`), com a mesma geometria (`geo_*.npz`), a mesma elipse e as mesmas emendas.
- Leitura e gravação são as do `ad13\lipsync3\comum3.py`: ffmpeg bt601 com `accurate_rnd`, conversão inversa exata e etiqueta bt709/tv só no bitstream.
- Cada trecho do HeyGen leva antes da colagem:
  - o desvio de cor medido num anel de pele em volta da elipse (≈ +3/+6/+9 BGR);
  - um ajuste interno (pele do filtro e do meio do queixo), aplicado com o peso da elipse: zero na borda, inteiro no centro.
- Depois: `montar_corpo.py` e `montar_ad.py` com a mesma receita. Duração (97,60 s), CTA (75,89 s) e legenda iguais.
- O corpo refeito é o mesmo que entra no AD 14.

**Medidas** (`revisao\loteC\cor.py` e `brilho.py` com `loteA\escolha_12.json`; luma final − original; saídas em `cor_12_depois.txt` e `br_12_depois.txt`):

| | Antes | Depois |
|---|---|---|
| Degrau área colada − rosto (geral) | −4,8 | **−0,2** |
| Pior trecho | h −6,8 | s02 −1,6 |
| Rosto × original | −7,7 (U +2,2 / V −2,4) | **+0,1** (U +0,2 / V +0,2) |
| Fundo × original | −4,7 | **+0,2** |

**Revisão (`revisar_ad.py --lipsync`, PowerShell, proibidos `_lote\proibidos.txt`; trechos recortados do final pelo `_lote\chk_final.py`, em `_cor_rev\`):**
- Resultado: **OK, nenhum problema**. es (0,99), nenhum proibido, nenhum silêncio, nenhum salto de pts, setas no último quadro.
- Único aviso: o s09, que não tem pausa (já era assim).
- **Índice de pausa do conjunto:** 0,27 antes e **0,28** depois, medido igual nos dois finais. Na prática não mudou. Por trecho a variação fica entre −0,04 e +0,07 (s07 de 0,52 para 0,59, ainda aprovado).
- Logs: `_cor_rev\revisar_antes.log` (anterior, sem whisper) e `revisar_depois.log`.
- Folha visual (original × antes × depois): o tom da pele voltou ao do original e não aparece elipse. O vídeo não foi aberto.

---

## Arquivo final
- `C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 12 - ORACION-SERPIENTES-CAMPO-ES-LATAM.mp4`
- 97,60 s, 720x1280, 30 fps (a base é 24 fps, como o original), AAC, 26,3 MB, sem selo.
- Setas de CTA a partir do 1º "Toca" (75,89 s) até o último quadro. Legenda em espanhol pelo alinhamento, na altura da legenda antiga (y 1493 na escala 1080), longe da boca.
- O original tem 393 s: a fala acaba em ~106 s, e depois vem a cruz com setas, parada. Como o espanhol ficou mais curto, o corte é 0,7 s depois da última fala (97,59 s), com fade de 0,3 s.

## Descoberta: o 12 e o 14 são o mesmo vídeo com gancho diferente
- Do quadro 231 (9,63 s) em diante, imagem e áudio são idênticos (diferença de ~1,5/255, só compressão). Só os primeiros ~9,5 s mudam:
  - 12: a Desatadora no olival, com a serpente;
  - 14: a Desatadora num interior escuro.
- Por isso o corpo (base sem legenda, 14 trechos de lipsync, narração) foi feito uma vez no AD 12 e reaproveitado no AD 14. O roteiro é o mesmo nos dois.

## Roteiro em espanhol (tempos no vídeo final; voz a 1,0x)
| Tempo | Fala |
|---|---|
| 0,15–6,15 | En este momento estoy quitando de tu camino las serpientes que se enredaron en tu vida, y que no dejan llegar tu bendición. |
| 6,61–17,15 | Yo soy la Desatadora de Nudos, y no fue por casualidad que vine a hablarte, porque fuiste tú a quien elegí entre tanta gente, para recibir lo que estaba preparado para ti. |
| 17,61–26,36 | Hay una bendición separada con tu nombre, y ya está en camino hacia ti. Pero hay un nudo apretado en medio del camino, que la detiene afuera. |
| 26,82–37,61 | Y ese nudo no lo ataste tú. No es que tu fe sea débil. Rezaste, encendiste velas, hiciste promesas, y aun así tu corazón no encontraba descanso. |
| 38,07–45,24 | La culpa nunca fue tuya. Siempre fue ese nudo, que se desata con la oración en el orden correcto, como te voy a enseñar. |
| 45,70–50,35 | No se trata de rezar más. Lo que desata ese nudo es rezar de la manera correcta. |
| 50,81–58,68 | Y cuando ese nudo se desate, la bendición que estaba detenida empezará a llegar, y tu vida entrará en un tiempo de paz y alegría. |
| 59,14–65,62 | Las preocupaciones que te quitan la paz se alivian, y por primera vez en mucho tiempo, tu corazón encuentra descanso. |
| 66,08–74,91 | Pero presta mucha atención hasta el final, porque este momento es para ti, y esta oración sagrada fue escogida con amor para ti. |
| 75,36–87,76 | Entonces toca el botón de abajo ahora, porque te dejé un video corto y gratuito, con el orden correcto de las oraciones. Una para cada nudo, comenzando por el primero: el que más aprieta tu vida. |
| 88,22–92,94 | Pero no dejes pasar este momento. Hay quien no quiere que este secreto llegue hasta ti. |
| 93,40–96,89 | Toca el botón de abajo, y recibe lo que Dios ya preparó para ti. |

Os blocos foram encadeados com 0,46 s entre eles, sem prender cada um ao tempo do PT. Assim o espanhol sai a 1,0x sem estourar, e o lipsync speed segue o áudio novo.

## Voz
- **Reaproveitada: "ORACAO-13 mulher" `ZsipxX9wNYg2lJhEScWc`.** Nenhuma voz nova, nenhuma apagada.
- Semelhança medida com o Resemblyzer, contra a voz do 12 limpa pelo demucs:
  - voz original do AD 01: 0,986. É a mesma Desatadora do AD 01;
  - voz original do AD 13: 0,950;
  - fonte do clone do AD 11: 0,862;
  - **TTS do clone "ORACAO-13 mulher": 0,892**;
  - TTS do clone "ORACAO-11 mulher" (o usado no AD 01): 0,837.
- Ficou o clone mais próximo, o do 13. Ponto de atenção: o AD 01, com a mesma personagem, usa o clone do 11.
- Script: `_audio\semelhanca.py`.

## Custos
- **TTS ElevenLabs:** 1.499 caracteres numa rodada só (12 blocos, `eleven_multilingual_v2`), cerca de US$ 0,25. O AD 14 reaproveita tudo e não gastou nenhum caractere a mais.
- **HeyGen:** 15 jobs `speed` (o gancho e 14 trechos do corpo), somando 97,6 s de vídeo.
  - **Saldo:** 8.825 antes do lote e 8.818 na última leitura, cerca de 25 min depois.
  - **A cobrança do speed atrasa até ~1 h, e a conta é compartilhada com outros agentes.** Por isso o valor real ainda não apareceu.
  - **Estimativa:** pela taxa medida no AD 01 (~1 crédito/s), **cerca de 95–100 créditos**, abaixo do teto de 170. Esse valor cobre também o corpo do AD 14.

## Lipsync
- **Parâmetros:** `mode speed`, `enableDynamicDuration=false`, `keepTheSameFormat=true`, `fpsMode cfr`, sem marca d'água.
- **Entrada:** recorte só no rosto da Desatadora, com o áudio PT original no vídeo. O espanhol vai separado, como `audio`.
- **Recorte e colagem:**
  - o recorte 9:16 **acompanha o rosto** quadro a quadro (landmarks do MediaPipe, suavizados) e é escalado para 720x1280;
  - o rosto do Jesus fica fora, conferido em `lipsync\crops.jpg`;
  - a saída volta só na boca e no queixo, com uma elipse suave desenhada pelos landmarks da base;
  - scripts: `lipsync\rosto.py`, `preparar.py`, `medir.py` e `recolocar.py`.
- **Número de quadros:** todos os trechos voltaram com o número exato (24 fps), menos o s05a, que voltou com 169 em vez de 170 e foi reamostrado no tempo. Nenhum quadro ficou congelado.
- **Emendas:** os trechos foram cortados nos cortes de câmera. A única emenda contínua (s05a/s05b, em 48,04 s) leva um crossfade de 2 quadros.
- Nenhum trecho precisou ser refeito.

| Trecho | Tempo | Boca mudou | Índice de pausa | Corr. ES | Veredito (checar_lipsync com --rosto) |
|---|---|---|---|---|---|
| h | 0,00–9,54 | 100 % | 0,10 | 0,40 | aprovado |
| s01 | 9,63–19,46 | 96 % | 0,18 | 0,35 | aprovado |
| s02 | 19,46–29,25 | 100 % | 0,30 | 0,43 | aprovado |
| s03 | 29,25–38,92 | 100 % | 0,32 | 0,23 | aprovado |
| s04 | 38,92–40,96 | 100 % | 0,06 | 0,54 | aprovado |
| s05a | 40,96–48,04 | 100 % | 0,37 | 0,51 | aprovado |
| s05b | 48,04–55,13 | 100 % | 0,03 | 0,35 | aprovado |
| s06 | 55,13–62,46 | 98 % | 0,26 | 0,35 | aprovado |
| s07 | 62,46–72,46 | 100 % | 0,58 | 0,32 | aprovado (o mais perto do limite) |
| s08 | 72,46–77,33 | 100 % | 0,02 | 0,45 | aprovado |
| s09 | 77,33–80,42 | 100 % | — (sem pausa no ES) | 0,58 | aviso do kit só por não ter pausa; a correlação é boa |
| s10 | 80,42–83,83 | 91 % | 0,10 | 0,55 | aprovado |
| s11 | 83,83–87,38 | 100 % | 0,05 | 0,49 | aprovado |
| s12 | 87,38–92,29 | 95 % | 0,09 | 0,58 | aprovado |
| s13 | 92,29–97,59 | 100 % | 0,16 | 0,54 | aprovado |
| **Conjunto** | | | **0,23** | | **aprovado** (meta ≤ 0,6; AD 11 aprovado = 0,38) |

- **Fora do lipsync:** só os 2 quadros do clarão da transição (9,54–9,60 s), em que os rostos ficam lavados de luz.

## O que saiu ou foi trocado
- **Dinheiro:**
  - "bênção financeira grande" virou "una bendición separada con tu nombre";
  - "o dinheiro entrava numa mão e sumia na outra" virou "tu corazón no encontraba descanso";
  - "nó da escassez e da pobreza" virou "ese nudo";
  - "tempo de fartura e de multiplicação" virou "un tiempo de paz y alegría";
  - "aquela conta que tira o seu sono, você paga" virou "las preocupaciones que te quitan la paz se alivian".
- **Saúde e sono:** "dorme a noite inteira sem aquele aperto no peito" virou "tu corazón encuentra descanso".
- **Ameaça e contagem regressiva:**
  - "essa revelação vai ser removida", "você tem poucos segundos" e "não fica muito tempo no ar" viraram "presta mucha atención hasta el final, porque este momento es para ti…" e "no dejes pasar este momento";
  - "tem quem não queira que esse segredo chegue até você" virou "Hay quien no quiere que este secreto llegue hasta ti", sem ameaça a quem assiste.
- **"Hoje" e "o que já é seu por direito":** saíram. Entraram "lo que estaba preparado para ti" e "lo que Dios ya preparó para ti".
- **Mantidos:**
  - o gancho das serpentes, a Desatadora de Nudos e o nó;
  - "no se trata de rezar más / de la manera correcta";
  - o vídeo curto e gratuito com o orden de las oraciones;
  - o CTA "Toca el botón de abajo".
  - O original não cita a "oración de nueve palabras", então ela não foi inserida.
- **Imagem:**
  - a legenda PT amarela (y ~1000–1080) saiu com o LaMa na GPU, com máscara justa (glifo e contorno, dilatados 9 px), longe da boca;
  - a **seta vermelha do original** (78–106 s), com os riscos brancos de brilho, também saiu, com a máscara cobrindo a seta e a borda;
  - não há moeda, marca nem famoso do Brasil na imagem.
- **Áudio:** narração a −16 LUFS por bloco, mais a trilha do original (demucs `no_vocals`, −27,8 LUFS) no nível original.

## Revisão própria
- **Comando:** `revisar_ad.py --idioma es --idioma-residual pt --proibidos "real,reales,dinero,depósito,cantidad,riqueza,cura,curada,enfermedad,cáncer,horas,segundos,aire,borrada" --lipsync <15 trechos com rosto>`, rodado pelo PowerShell.
- **Resultado: OK, nenhum problema.**
  - idioma es (0,99) e nenhum termo proibido;
  - nenhum silêncio acima de 0,7 s e nenhum salto de pts;
  - 12 cortes, nenhum par a menos de 0,3 s;
  - setas no último quadro.
- **Transcrição em espanhol:** bate com o roteiro.
- **Português residual:** a passada em pt só "traduz" o espanhol. Não sobrou fala em português.
- **Lipsync:** índice de pausa do conjunto 0,23. O único aviso é o s09, que não tem pausa (correlação 0,58).
- **Cortes:** folhas de 1 em 1 quadro em volta de todos os cortes (`_tmp\cortes_a.jpg` e `_tmp\cortes_b.jpg`). Nenhum quadro solto, nenhum salto de boca.
- **Folhas do kit:** `producao\AD 12 - …_revisao.jpg/.txt` e `_frames.jpg`.
- O vídeo não foi aberto.

## Pontos para a pessoa olhar
1. **Voz:** é o clone do AD 13 (0,89 de semelhança), não o do AD 01, apesar de ser a mesma Desatadora. Para ter a mesma voz do AD 01, dá para regerar o TTS com `UNDKAyEJ2rTv99l7gCy5`, mas o lipsync teria de ser refeito.
2. **Créditos HeyGen:** o valor final só aparece cerca de 1 h depois. Vale conferir o saldo.
3. **s07 (62,5–72,5 s):** índice de pausa 0,58, perto do limite. Vale conferir assistindo.
4. **Fim antecipado:** o AD termina em 97,6 s. Os planos finais do original (97,7–106 s) e a tela da cruz saíram.
5. **Transição com clarão (9,5–9,7 s):** é do original e foi mantida.

## Arquivos (`producao\_trabalho\ad12\`)
- `_audio\`: `blocos.json`, `gerar_tts.py`, `tts\`, `montar_narracao.py`, `montar_corpo_audio.py`, `semelhanca.py`, `demucs\`.
- `_tmp\`: `mascara.py`, `lama_run.py`, `montar_base.py`, `lama\` e as folhas.
- `lipsync\`: `rosto.py`, `preparar.py`, `medir.py`, `recolocar.py`, `arg.py`, `put.sh`, `baixar.sh`, `ids.txt`, `in\`, `out\`.
- Na raiz:
  - `segmentos.json`, `narracao_es.wav` com o alinhamento e `tempos_reais.json`;
  - `audio_corpo.wav`, `base_sem_legenda.mp4`, `base_lipsync.mp4` e `corpo_ad12.mp4`;
  - `montar_corpo.py` e `receita_ad12.json`.
