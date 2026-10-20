# V25 — LYMPHORIA-HINCHAZON-ENERGIA
- **Saída:** `ADLIB-VITALY-CL\LYMPHORIA-ES-CL\V25 - LYMPHORIA-HINCHAZON-ENERGIA.mp4` (21,6 s, 720x1280, 11,9 MB)
- **Trocas:**
  - Camiseta "ABOLISH ICE" (take 9,73–10,57 s): mosaico + desfoque forte na estampa (caixa 160,750–580,1110), ilegível (`blur_forte.py`). O take ficou para o texto "Sí, y te vas a sentir muchísimo mejor" ter ~1,8 s de leitura.
  - Último take (10,57–11,47 s), criadora segurando frasco de outra marca (Nature's Sunshine, rótulo verde legível): **cortado**. Vídeo usa 0–10,567 s + fim Lymphoria.
- **Custo:** ≈ US$ 0,007 (parte do TTS do fim).
- **Revisão:** RESULTADO OK (proibidos nenhum, sem quadro solto, pts ok, setas ok). Whisper ouviu "linforia" (pronúncia da voz; a legenda escreve LYMPHORIA).
- **Revisão manual:** antes/depois de rosto com pessoas diferentes (0–5,9 × 6–8,9 s). Frasco âmbar pequeno sem rótulo legível no take da camiseta: mantido.
## Fim Lymphoria (comum a V14/V22/V25/V30)
- `_fim_V14-V22-V25-V30/`: foto prod_1 (0–1,45 s) + card "COMPRE 1, RECIBA 2 · $34.990 · ENVÍO GRATIS" (2 frascos, recorte do kit3) + narração + legenda + selo "ENVÍO GRATIS A DOMICILIO / PAGO CONTRA ENTREGA / ¡PAGAS AL RECIBIR!" (desde "envío") + setas em "Toca", via `montar_ad.py` (720x1280).
- Narração (voz de banco "chilena" `uHo8F3FY11rc2LxCwDSB`; o vídeo original não tem fala, nada a clonar): "Se llama Lymphoria. Compre uno y reciba dos, con envío gratis, y pagas al recibir en tu casa. Y tienes noventa días de garantía. Toca el botón de abajo y pide el tuyo." 167 caracteres = US$ 0,028, dividido entre os 4 vídeos (≈ US$ 0,007 cada).
- Dose: nenhum dos 4 vídeos diz dose; o fim não cita dose.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 10.57 s, parte 1 intacta, e fim novo com takes Lymphoria (ad13/t4_edit, ad14/t3_edit, P1_kit3). Mesma voz do fim anterior (chilena), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 19.8 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
