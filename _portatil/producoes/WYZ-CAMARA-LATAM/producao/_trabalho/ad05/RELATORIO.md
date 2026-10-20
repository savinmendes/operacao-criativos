# AD 05 — Wyze Solar Cam Pan (câmera no beiral + app) — EN → ES LATAM

- **Arquivo:** `producao\AD 05 - WYZE-SOLAR-CAM-PAN-INSTALACION-FACIL-ES-LATAM.mp4` — 62,60 s, 720x1280, 26,8 MB, decodifica OK.
- **Voz:** Alberto Rodríguez - Serious, Narrative (catálogo, espanhol latino, masculina) — `l1zE9xgNpUTaQCZzpNJa`, velocidade 1,06 no ElevenLabs. Sem clonagem.
- **TTS:** 1.844 caracteres no total (~US$ 0,30): 1ª versão de 1.036 caracteres descartada (76 s, longa demais) e versão final de 808 caracteres (55,9 s).
- **HeyGen:** não se aplica (Grupo A).

## O que foi cortado ou trocado
- Fala nova (roteiro em `roteiro_es.txt`), com a mesma estrutura do original. A fala foi encaixada **frase a frase no tempo das cenas** (ex.: "eliges un lugar firme…" sobre o app; "audio bidireccional, reflector, sirena…" no trecho das features).
- **Saiu "Zoom":** não está nas especificações oficiais do briefing. "Full-color night video" virou "visión nocturna a color". O resto é a fala original enxugada.
- **Desfoque com rastreamento** (`blur_track.py`, keyframes interpolados) entre 17,8 e 21,97 s: rosto do terceiro na gravação do app e a data/hora "2025-10-27…". A marca d'água WYZE ficou (permitida).
- Legenda roxa em inglês coberta por uma barra preta 100% opaca (y 940–1110). A legenda nova fica dentro da barra (y=1537 na escala 1080x1920), e as setas ficam logo abaixo dela, no "Toca" (59,76 s até o fim).
- Fundo: `no_vocals` do demucs, ~15 dB abaixo da voz. O Whisper en não achou nenhuma fala no fundo.
- Sem selo. A receita com selo está pronta em `receita_com_selo.json` (não renderizada; conferir o y).

## Revisão
- Whisper es: bate com o roteiro (só "no pagas" sai como "no paga"). Sem preço, país, TikTok, "link", Navidad/año nuevo ou alegação proibida.
- Whisper en: só a tradução da fala em espanhol; nada do inglês original.
- Folha 1/s (`rev\folha.jpg`) e conferência quadro a quadro do app (`f\chk_blur*.jpg`): nenhuma legenda em inglês, rosto e data desfocados em todos os quadros, sem quadro solto. Não há silêncio ≥ 0,4 s no fim (a fala termina em 62,3 s e o vídeo em 62,6 s).

## Pendências
- Há pausas de 1–1,5 s entre algumas frases (a fala ficou mais curta que o vídeo). O fundo musical preenche essas pausas.
- Relevo WYZE na câmera mantido (permitido).
- Selo só depois da confirmação.
