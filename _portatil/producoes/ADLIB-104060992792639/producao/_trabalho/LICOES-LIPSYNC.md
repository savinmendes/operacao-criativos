# Lições de lipsync (HeyGen) — AD 01, 08/10/2026

Fonte: refação do AD 01 (`_trabalho\ad01\lipsync2\`). Atualizado à medida que os resultados se confirmam.

## Resumo (o que funcionou)

**Use `mode: "speed"`, NÃO `precision`.** Entrada recortada só no rosto de quem fala, com o áudio PT original no vídeo e o espanhol como `audio`.

- Com `precision`, o HeyGen só refaz a boca **onde a fala ORIGINAL (PT) existe**. Fora disso, ele devolve a boca do vídeo de entrada.
  - O próprio erro do HeyGen confirma: "Video translation uses the original speech in the video to detect who is speaking and when".
  - Resultado: nas pausas do ES a boca segue falando PT (aberta, sorrindo), e onde o ES fala e o PT estava calado ela fica parada. É exatamente o defeito "segue o português".
- Com `speed`, a boca segue o áudio novo: fecha nas pausas do ES e articula na fala.

## Teste no trecho s06 do AD 01 (32,63–42,00 s, 281 quadros)

Índice de pausa = abertura média da boca nas pausas do ES / abertura na fala do ES. Meta ≤ 0,6. O AD 11 aprovado dá 0,38.

| Variação | Índice de pausa | Corr. boca × ES |
|---|---|---|
| Antes (quadro inteiro, 2 rostos, PT na entrada, precision) | 1,27 | −0,01 |
| (a) recorte só na mulher + PT na entrada, precision | 1,05 | 0,01 |
| (b) = (a) em 2 trechos ≤ 8 s (4,8 s + 4,5 s), precision | 0,97 | 0,04 |
| (c) = (a) sem áudio no vídeo | **falhou**: "audio is missing or corrupted" | — |
| (c) com trilha de silêncio | **falhou**: "audio track is silent… uses the original speech… to detect who is speaking and when" | — |
| (c2) trilha = ES com cada fala invertida (mesma atividade de fala) | **falhou**: "No speaker is detected" | — |
| **(d) = (a) com `mode: speed`** | **0,19** | **0,47** |

- Os dois rostos (Jesus calado atrás) não eram a causa principal: o recorte só ajudou um pouco (1,27 → 1,05). O que resolve é o modo `speed`.
- Trechos curtos não resolvem.
- A trilha do vídeo de entrada **tem que ter fala real**, e a fala PT original é a opção que funciona.

## Aplicado aos 9 trechos reprovados do AD 01 (recorte + PT + speed)

Os trechos foram medidos no próprio trecho, colado de volta na base. A coluna "antes" vem do revisor.

| Trecho | Antes | Depois | Corr. ES depois |
|---|---|---|---|
| s01 | 1,09 | 0,21 | 0,39 |
| s02 | 1,15 | 0,41 | 0,32 |
| s05 | 1,35 | 0,22 | 0,21 |
| s06 | 1,26 | 0,19 | 0,47 |
| s07 | 0,90 | 0,18 | 0,63 |
| s08 | sem pausa (corr. ES 0,14, PT 0,28) | sem pausa ≥ 8 q; índice com pausas ≥ 4 q: 0,95 → 0,59 | 0,24 |

- O 1º job speed do s08 travou mais de 2 h em "processing". O reenvio idêntico voltou em ~25 min.
- **Se um job passar de ~45 min, reenvie.**
| s09 | 0,83 | 0,09 | 0,47 |
| s11 | 1,07 | 0,58 | 0,28 |
| s12 | 0,86 | 0,39 | 0,37 |

- Todos voltaram com o número exato de quadros (30 fps, cfr), sem precisar reamostrar.
- Na folha de contato, a boca fecha nas pausas e articula na fala. A nitidez é igual à do precision nesse recorte 720x1280.

## Custo (atenção: speed é caro)

- **Créditos: de 8.914 para 8.825, ou seja, 89 créditos**, com a cobrança aparecendo até cerca de 1 h depois.
  - Logo após os testes, o saldo tinha caído só 2; meia hora depois, 73.
  - Jobs: precision, 18,7 s somados (a, b1, b2); speed, 88,9 s (o teste d e mais 8 trechos); 4 jobs falharam (c, c-silêncio, c2 ×2).
- **Estimativa: speed ≈ 0,9–1,0 crédito por segundo de vídeo; precision ≈ 0,26 crédito/s** (o AD 01 original: 30 créditos para 115,8 s).
- **Orçamento para o lote: cerca de 1 crédito por segundo de rosto falando.** Um AD de 115 s fica em cerca de 115 créditos.
- Meça `get_current_user` antes, e de novo cerca de 1 h depois do último job, porque a cobrança atrasa.
- Um job speed (o s08, 11,3 s) ficou mais de 1,5 h em "running" sem terminar. Os outros levaram de 20 a 40 min.
  - Se travar, não reenvie sem checar o orçamento.

## Resultado no vídeo final do AD 01 (revisar_ad.py --lipsync + revisao\pausas.py, trecho a trecho)

- **Índice de pausa do conjunto: 0,19** (antes 0,86; o AD 11 aprovado dá 0,38).
- Trechos refeitos: s01 0,20 · s02 0,39 · s05 0,26 · s06 0,16 · s07 0,20 · s09 0,10 · s11 0,51 · s12 0,43.
- s03, s10 e s13 são os trechos antigos com `fechar.py`, sem custo: de 0,66 / 0,49 / 0,64 para 0,03 / 0,03 / 0,04.
- O único reprovado é o **s08**, que ficou na versão antiga (precision) porque o job novo travou. Ele não tem pausa no ES, então só a correlação conta: 0,13.

## Parâmetros

`create_lipsync`:
- `mode: "speed"`
- `enableDynamicDuration: false`
- `keepTheSameFormat: true`
- `fpsMode: "cfr"`
- `enableWatermark: false`
- `video` = recorte com o áudio PT original do trecho
- `audio` = mp3 do ES do mesmo intervalo

## Scripts para reproduzir (em `_trabalho\ad01\lipsync2\`; adapte as coordenadas)

1. **`preparar.py nome qini qfim pt`**: entrada recortada.
   - Faz um recorte 9:16 de 288x512 em (318,196) da `base_sem_legenda.mp4`, só a mulher. O resto de barba do Jesus no canto vai para inpaint.
   - Escala 2,5x para 720x1280 e junta o áudio PT do `UNICOS_HD\NN.mp4`.
   - Gera também o `es_<nome>.mp3`.
   - **Para outro AD:** ache o rosto de quem fala com `rostos.py` (landmarks por trecho, de quem fala e de quem não fala) e escolha um recorte 9:16 que contenha o rosto inteiro de quem fala e deixe os olhos do outro de fora.
2. **Upload:** `create_asset_upload_batch`, depois `put.sh` (curl PUT com `x-amz-server-side-encryption: AES256`), depois `complete_asset_batch`.
3. **`baixar.sh ids.txt`**: baixa `https://resource2.heygen.ai/video_translate/<id>/original.mp4`.
4. **`medir_out.py nome qini out/arquivo_nNNN.mp4`**: cola de volta (`colar.py`: elipse suave na boca e no queixo, reamostrando para N quadros) e mede o índice de pausa, com a mesma conta do revisor (`revisao\pausas.py`).
5. **`recolocar2.py`** + `plano.json`: monta a `base_lipsync.mp4`.
   - Trechos refeitos: colagem só da boca e do queixo.
   - Trechos mantidos: como no `recolocar.py` antigo.
   - Reamostragem no tempo (interpolação) em vez de congelar o último quadro.
   - Crossfade de 2 quadros nas emendas sem corte de câmera (corte = diferença média da base > 10).
6. **Conferência pelo kit:**
   - Comando: `checar_lipsync.py full_sNN.mp4 --audio-novo es_sNN.mp3 --original orig_sNN.mp4 --rosto 330,280,200,260`.
   - No s06, deu 0,20 APROVADO (speed) contra 1,05 REPROVADO (precision), batendo com a medida acima.
7. **Plano B:** se algum trecho ainda abrir a boca numa pausa, use `fechar.py`, que cola uma boca fechada do próprio trecho, alinhada por olhos e nariz, nas pausas ≥ 6 quadros. Não precisa de crédito. Foi testado no s06 em precision (1,05 → 0,02, visual natural), mas com speed não foi necessário.

## Cortes de câmera no AD 01

- As emendas em 19,47 s, 20,97 s e 49,00 s caem em **cortes reais** entre clipes (a base muda inteira, diferença média de 25 a 31). O pulo de boca nelas é o próprio corte.
- As emendas contínuas são as de 8,40 s, 42,00 s, 60,27 s, 72,47 s, 83,30 s, 93,73 s e 104,77 s. Nelas entra o crossfade de 2 quadros.
