# V14 — LYMPHORIA-DEJAR-AZUCAR
- **Saída:** `ADLIB-VITALY-CL\LYMPHORIA-ES-CL\V14 - LYMPHORIA-DEJAR-AZUCAR.mp4` (20,8 s, 720x1280)
- **Trocas:** frascos de outra marca (Nature's Sunshine "Lymphatic Drainage") parados no balcão nos 3 takes de 7,4–10,37 s: mosaico + desfoque forte no frasco inteiro abaixo da tampa (quadros 222–245, 246–268, 269–311), rótulo ilegível. Duração original mantida (311 quadros). Texto da tela mantido (sem marca).
- **Custo:** ≈ US$ 0,007 (parte do TTS do fim). Sem Kling (desfoque, conforme briefing: mais barato e o frasco é fundo).
- **Revisão:** RESULTADO OK (proibidos nenhum; whisper só pega a letra da música e o fim).
- **Revisão manual:** antes/depois de rosto com mulheres diferentes; música com letra (direito autoral, do estudo).
## Fim Lymphoria (comum a V14/V22/V25/V30)
- `_fim_V14-V22-V25-V30/`: foto prod_1 (0–1,45 s) + card "COMPRE 1, RECIBA 2 · $34.990 · ENVÍO GRATIS" (2 frascos, recorte do kit3) + narração + legenda + selo "ENVÍO GRATIS A DOMICILIO / PAGO CONTRA ENTREGA / ¡PAGAS AL RECIBIR!" (desde "envío") + setas em "Toca", via `montar_ad.py` (720x1280).
- Narração (voz de banco "chilena" `uHo8F3FY11rc2LxCwDSB`; o vídeo original não tem fala, nada a clonar): "Se llama Lymphoria. Compre uno y reciba dos, con envío gratis, y pagas al recibir en tu casa. Y tienes noventa días de garantía. Toca el botón de abajo y pide el tuyo." 167 caracteres = US$ 0,028, dividido entre os 4 vídeos (≈ US$ 0,007 cada).
- Dose: nenhum dos 4 vídeos diz dose; o fim não cita dose.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 10.37 s, parte 1 intacta, e fim novo com takes Lymphoria (ad22/t1_edit, V2_frasco_cocina, P1_kit3). Mesma voz do fim anterior (chilena), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 19.6 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
