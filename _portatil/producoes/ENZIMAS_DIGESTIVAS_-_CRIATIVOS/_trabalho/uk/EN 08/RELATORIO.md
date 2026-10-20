# EN 08 - ENZIMAS-TRUQUE-6-MESES-GRAVIDA-V2 → UK (08/10/2026)

Saída: `UK\EN 08 - ENZIMAS-TRUQUE-6-MESES-GRAVIDA-V2 - UK.mp4` (720x1280, 30 fps, 116,40 s, 3491 quadros, igual ao original).

## Frases trocadas
| Tempo | Original | UK |
|---|---|---|
| 74,00–80,30 s (fala 74,20–80,00) | "Literally hamburgers, whatever the average American eats, you know, our average American diet is" | "Literally hamburgers, whatever most of us eat, you know, our modern diet is" |

- "Literally hamburgers," foi regerado junto para a emenda cair na pausa natural antes (73,75–74,15 s) e depois (80,05–80,45 s, antes de "Disgusting").
- Duração da fala nova 5,66 s contra 5,80 s da original (diferença de 0,14 s, dentro de ±0,3 s). TTS com velocidade 0,8, sem atempo.
- Volume: voz original -27,3 LUFS, nova -27,6 → +0,3 dB. Áudio do trecho = fundo do demucs + voz nova; fora do trecho o original fica intocado (crossfade de 30 ms).
- Varredura completa da transcrição: nenhuma outra menção a EUA, TikTok, dólar, grocery store ou "on here". Nada na tela (sem carrinho, @, marca d'água ou $).

## Voz
- ElevenLabs IVC "ENZIMAS UK EN 08 creator": `QuE2ojjpawaYQH7JLSPO` (vocals do demucs, 0–116 s).
- Caracteres de TTS: 156 (2 gerações de 78; foi usada a tts2, velocidade 0,8).

## HeyGen
- 1 job `create_lipsync` em modo speed, 6,3 s (189 quadros): `8c0fbbc1adeb4a1cb0cefd7e4d3d6d86`. Entrada recortada no rosto (360x640 → 720x1280) com o áudio original.
- Saldo antes: 8.797. Logo depois: 8.797 (a cobrança atrasa e outros agentes usam a mesma conta).
- Estimativa pelo próprio job (≈1 crédito/s em speed): **~6 créditos**.

## Lipsync
- `checar_lipsync.py`: **índice de pausa 0,19 APROVADO**; a boca mudou em 81% dos quadros, corr. com o áudio novo 0,31 (com o original, 0,18).
- Colagem com elipse na boca e no queixo, cor exata (comum3; desvio de cor -0,3 BGR) e crossfade de 2 quadros nas emendas q2220 e q2409.

## Revisão
- `revisar_ad.py --lipsync` (PowerShell, termos proibidos em `proibidos.txt`): **OK, nenhum problema encontrado**.
  - Sem saltos de pts nem silêncio.
  - Whisper en: "...whatever most of us eat, you know, our modern diet is disgusting and horrible...". Nenhuma sobra da frase antiga.
- Folha de 1 em 1 quadro nas emendas (`seams.jpg`): emenda de 80,3 s contínua. Na de 74,0 s a boca passa de aberta (fim de "pizza") a fechada em cerca de 2 quadros; é aceitável e cai na pausa antes de "Literally".
- Folha da boca no trecho: `boca.jpg`.

## Pendências
- Créditos HeyGen: reconfirmar o saldo cerca de 1 h depois (a medida isolada fica confundida por outros agentes).
- Texto do gancho "PROOF DIGESTIVE EMZYMES WORK" tem erro de digitação ("EMZYMES") no original. Não foi alterado por estar fora do escopo; corrigir se a pessoa quiser.
- O vídeo não fala de preço, então nada a confirmar em libras aqui.
