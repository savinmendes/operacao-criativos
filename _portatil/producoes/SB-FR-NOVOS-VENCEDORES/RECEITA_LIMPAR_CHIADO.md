# Receita: limpar chiado (hiss) de voz TTS + trilha demucs

Validada em 17/10/2026 nos ADs FR `02_ADS-20` e `03_ADS-13.13F-REZA-MUJER`. Use no `01_AVATAR-REST` e nos lotes IT/PL.
O código está em `SB-FR-NOVOS-VENCEDORES\_chiado\chiado.py`. Exemplos de uso: `02_ADS-20\_trabalho\chiado\remix.py`
(várias fontes de voz + linha do tempo) e `03_ADS-13.13F-REZA-MUJER\_trabalho\chiado\remix.py` (voz já na linha do tempo).

## Onde estava o chiado (diagnóstico)
- **Voz ElevenLabs.** Nas pausas longas o TTS é quase silêncio digital (-95 a -130 dBFS). O chiado audível é um **tapete
  de ruído de 5 a 15,5 kHz que acompanha a fala**: ele aparece entre as palavras e por baixo das vogais. É forte na voz
  "Jesus The Chosen" (clone de fonte ruidosa) e bem mais fraco no Brian.
- **Trilha demucs (`no_vocals`).** Tem tapete de chiado em banda larga até 20 kHz e resto das sibilantes da voz
  removida (riscos verticais de 4 a 15 kHz). Também tem linhas tonais em 5,5/8,5/11/14 kHz. Nas pausas da voz só sobra
  a trilha, e é ali que o chiado aparece.
- **`afftdn` do ffmpeg não serve aqui.** Com perfil branco (nr 12 a 30, nf -40 a -70, com e sem +30 dB de pré-ganho) a
  diferença medida foi de 0,0 dB. Com perfil amostrado (`asendcmd ... afftdn sn start/stop`) o chiado caiu, mas as
  sibilantes caíram 3,8 dB e o "s" ficou abafado. Ficou o gate espectral em Python descrito abaixo.

## Cadeia da VOZ: `limpar_voz(x, palavras)`
Aplique em cada fonte de voz separadamente (gancho e corpo). Cada voz tem o próprio perfil.
Faça isso antes de montar a linha do tempo. O comprimento fica idêntico, então os cortes e o alinhamento valem como estão.

1. **Gate espectral acima de 5 kHz** (STFT 2048, hop 512):
   - perfil de ruído por bin = percentil 35 da potência nos quadros com voz (150 a 4000 Hz > -55 dBFS);
   - ganho = sqrt(1 - (2,0·N/|X|)²), atenuação máxima de -18 dB;
   - ganho suavizado em 5 bins × 3 quadros (evita "musical noise");
   - abaixo de 4 kHz não mexe (rampa de 4 a 5 kHz).
   - Parâmetros: `q=35, k=2.0, piso_db=-18, fmin=5000`. Testados: leve q25/k1,2/-10, médio q30/k1,5/-14 e forte
     q35/k2,0/-18. O forte tira mais chiado e as sibilantes (p97 de 7 a 14 kHz) caem só 0,2 dB.
2. **Silêncio real fora da fala**:
   - a máscara de fala é a união de duas coisas: as palavras do alinhamento do ElevenLabs (de 50 ms antes do início a
     80 ms depois do fim) e os quadros de 10 ms com energia acima de max(-50 dBFS, mediana da fala - 35 dB);
   - a máscara é dilatada em 20 ms, e buracos menores que 60 ms continuam contando como fala;
   - fora da máscara a voz cai -60 dB, com rampas de 15 ms. Nada é deslocado no tempo.
3. **EQ suave**: `highshelf=f=10000:g=-3,lowpass=f=14000:p=2`.

Não usei de-esser: depois da cadeia o "s" ficou 1,5 a 3 dB mais baixo, sem ficar estridente.

## Cadeia da TRILHA: `limpar_trilha(no_vocals)`
1. **Gate espectral acima de 1,5 kHz**: perfil = percentil 30 de todos os quadros ativos (o chiado é estacionário),
   com `k=2.0` e atenuação máxima de -20 dB.
2. **EQ**: `lowpass=f=11500:p=2,lowpass=f=11500:p=2,highshelf=f=5000:g=-4` (passa-baixa de 24 dB/oitava em 11,5 kHz e
   shelf para o resto de sibilantes).
3. **Nível**: -32 LUFS integrados (pyloudnorm, ganho estático), montada com os mesmos cortes e fades do mix original.
4. **Dip nas pausas**: `dip_pausas(trilha, máscara_da_voz, 3)` baixa a trilha mais 3 dB (≈ -35) em pausas da voz de pelo
   menos 0,25 s, com rampas de 150 ms. Pausas mais curtas ficam sem dip.

## Mix final: `finalizar_mix(voz + trilha)`
- A voz entra com ganho estático (-16 a -16,5 LUFS). **Não use `loudnorm` dinâmico na voz**: ele mexe no ganho das pausas.
- O mix leva ganho estático até -16 LUFS. Se o true peak (4× oversampling) passar de -1,5 dBTP, entra
  `alimiter=limit=…:attack=2:release=60:level=false:latency=1` (o `latency=1` evita atraso) e o ganho é reajustado.
- Remonte só o áudio:
  `ffmpeg -i video_v1.mp4 -i mix_v2.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -t <dur_v1> -movflags +faststart saida.mp4`
- **Sincronia**: compare por correlação o áudio da v1 com o da v2 em 3 pontos; o atraso tem que dar 0 amostra.
  O `alimiter` antigo, sem `latency=1`, atrasava o mix em 238 amostras (5 ms). No ADS-20 a v2 foi deslocada para ficar
  igual à v1.

## Medição (antes × depois, nos mp4 finais)
Bandas em dBFS RMS (STFT 2048, soma dos bins).
- **Pausas**: intervalos ≥ 0,25 s entre palavras, com 80 ms de margem.
- **Tapete na fala**: percentil 25 da banda de 7 a 14 kHz nos quadros com voz.

| AD | 7–14 kHz nas pausas | (pausas) agudo − graves 100–1000 Hz | tapete 7–14 kHz na fala (p25) | sibilantes (p97) | LUFS / pico |
|---|---|---|---|---|---|
| ADS-20 v1 | -61,2 dB | -29,7 dB | -78,2 dB | -50,8 dB | -17,6 / — |
| ADS-20 v2 | **-71,7 dB** (−10,5) | -38,9 dB | **-89,3 dB** (−11,1) | -50,7 dB | -16,0 / -1,5 dBFS |
| 13.13F v1 | -58,7 dB | -25,8 dB | -71,9 dB | -46,5 dB | -16,0 / — |
| 13.13F v2 | **-66,0 dB** (−7,3) | -33,2 dB | **-81,0 dB** (−9,1) | -47,8 dB | -16,0 / -2,4 dBFS |

Conferências:
- `_chiado\conferir_palavras.py` (whisper fr medium, roteiro × transcrição): ADS-20 deu 461/466 palavras na v1 e na
  v2, com as mesmas 4 diferenças de grafia (fini/finis...); 13.13F deu 102/102 nas duas. Nenhuma palavra foi comida.
- `revisar_ad.py --idioma fr`: OK nos dois, sem salto de pts e sem silêncio.
- Vídeo idêntico: o md5 do stream de vídeo da v1 é igual ao da v2.

## Como aplicar num AD novo
```python
import sys; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
voz = load("voz.mp3"); vz, mk = limpar_voz(voz, palavras("voz.alinhamento.json"))
bed = limpar_trilha(load("demucs/htdemucs/x/no_vocals.wav"))          # depois aplique os mesmos cortes do mix original
vz = ganho_lufs(vz, -16.5); bed = dip_pausas(ganho_lufs(bed, -32), mk, 3)
mix = finalizar_mix(vz + bed)
```
Se o AD tiver várias vozes (gancho com uma voz e corpo com outra), limpe cada uma com o próprio alinhamento antes de
montar a linha do tempo.
