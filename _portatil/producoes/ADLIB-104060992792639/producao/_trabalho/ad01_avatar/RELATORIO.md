# AD 01 AVATAR (teste HeyGen photo avatar), 07/10/2026

- **Saída:** `producao\AD 01 AVATAR - ORACION-TRES-BENDICIONES-ES-LATAM.mp4`: 115,50 s, 720x1280, 30 fps, 26,9 MB, sem selo. Setas de CTA a partir de 104,97 s (o primeiro "Toca").
- **Imagem base:** quadro 60 (2,0 s) de `UNICOS_HD\01.mp4`, escolhido por varredura MediaPipe: boca fechada, olhos abertos, de frente, foco bom.
  - A legenda foi tirada com LaMa na GPU (`lama_base.py`).
  - O Jesus aparece atrás em todos os quadros, com a mão no ombro dela, e não sai com recorte. Por isso foi usado o Flora (1 geração, US$ 0,072, `i2i-gemini-3.1-flash-image`) com o prompt-base e mais "remove the man behind her and his hand". O rosto ficou preservado (`cand\cmp_rosto.jpg`).
  - Arquivo: `base.jpg` (768x1376).
- **Avatar HeyGen:** "ORACION Desatadora 01", look/grupo `59a82887f9adaae29270031871f4b757`.
- **Vídeos gerados** (Avatar IV, 9:16, 720p, áudio = `ad01\narracao_es.wav` cortado em 115,5 s):
  - **v1** `44701f76897eb4585a387bce822e8b8a`: expressividade medium. Sorri com os dentes nas pausas. Índice 0,99.
  - **v2** `f15c20a98af49091a7b4543bfee7d397`: expressividade low, prompt "solemn, no smiling". Índice 0,95. **É a usada.**
- **Créditos HeyGen:** de 8.912 para 8.874 (avatar + v1 = 38) e para 8.842 (v2 = 32). Total: 70, dentro do teto de 80.
  - Outro agente trabalhava no AD 01 ao mesmo tempo, então parte da diferença pode ser dele.
- **Montagem:** `montar_corpo.py` junta a imagem do avatar, `narracao_es` e `fundo.wav` (música do original), cortados 0,7 s depois da última fala. Depois roda `montar_ad.py receita_avatar.json`.
  - Não há b-roll: no original, de 0 a 115,8 s ela está sempre falando na tela.
- **Revisão:** `revisar_ad.py` OK em decodificação, pts, silêncio, cortes, idioma (es 1,00) e proibidos (nenhum). Só reprovou no lipsync.
  - **Índice de pausa:** 0,95. Meta ≤ 0,6.
  - Nas pausas curtas (0,3–0,6 s) a boca fica entreaberta com os dentes. Na pausa longa (78,7–79,9 s) ela fecha, mas abre cerca de 0,3 s antes da fala.
  - As duas versões têm a boca quase idêntica (correlação 0,95), então o comportamento vem do motor e não da expressividade.
  - Folhas: `folha_boca_v1.jpg`, `folha_boca_v2.jpg`, `tira_78.jpg`, `tira_37_10.jpg` e `zoom_boca_final.jpg`.
