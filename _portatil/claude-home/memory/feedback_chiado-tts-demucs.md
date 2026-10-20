---
name: feedback-chiado-tts-demucs
description: "Vídeos traduzidos saíam com chiado (TTS ElevenLabs + trilha demucs). Limpar sempre com o gate espectral de _chiado/chiado.py; afftdn não resolve"
metadata:
  type: feedback
---

Em 17/10/2026 a pessoa reclamou de "xiado" nos 3 vídeos SB FR. O problema aparecia nos lotes traduzidos (método B) e passou despercebido no EN/IT/PL.

**De onde vem o chiado:**
- **Voz TTS:** um tapete agudo de 5 a 15 kHz que acompanha a fala. É forte na voz Jesus The Chosen e na Martin, fraco na Brian.
- **Trilha separada pelo demucs:** chiado em banda larga e resto das sibilantes da voz.

**O que não funcionou:** o `afftdn` do ffmpeg não mudou nada com perfil branco e, com perfil amostrado, deixou os "s" abafados.

**O que funcionou:** o gate espectral em Python de `Downloads/SB-FR-NOVOS-VENCEDORES/_chiado/chiado.py`, com as funções `limpar_voz`, `limpar_trilha`, `dip_pausas` e `finalizar_mix`. A receita está em `RECEITA_LIMPAR_CHIADO.md`, na mesma pasta. Reduziu 7 a 11 dB de chiado sem comer palavras.

**Why:** a pessoa ouve os vídeos e percebe o chiado. As métricas do `revisar_ad.py` não pegam esse defeito.

**How to apply:**
- Em todo lote com TTS e trilha demucs, rodar a limpeza antes de entregar.
- Medir o ruído de 7 a 14 kHz nas pausas, antes e depois.
- Os lotes EN/IT/PL de 15–16/10 provavelmente têm o mesmo chiado. Oferecer limpar.

Relacionado: [[feedback-licoes-producao-video]]
