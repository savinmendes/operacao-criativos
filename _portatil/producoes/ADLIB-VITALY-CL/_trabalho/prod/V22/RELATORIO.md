# V22 — LYMPHORIA-POV-DRENAR
- **Saída:** `ADLIB-VITALY-CL\LYMPHORIA-ES-CL\V22 - LYMPHORIA-POV-DRENAR.mp4` (26,4 s, 720x1280, 17,2 MB)
- **Trocas:** nenhuma no corpo (sem marca, frasco, oferta ou fala). Vídeo original inteiro (0–15,37 s) + fim Lymphoria. Música com fade de 0,25 s na emenda.
- **Custo:** ≈ US$ 0,007 (parte do TTS do fim). Teto US$ 1,50.
- **Revisão:** `revisar_ad.py` RESULTADO OK (whisper es só com a narração do fim, proibidos nenhum, sem quadro solto, sem salto de pts, setas no último quadro). Folha: `rev/`.
- **Revisão manual:** antes/depois de corpo com duas moças diferentes e abdome à mostra (risco Meta, já apontado no estudo).
## Fim Lymphoria (comum a V14/V22/V25/V30)
- `_fim_V14-V22-V25-V30/`: foto prod_1 (0–1,45 s) + card "COMPRE 1, RECIBA 2 · $34.990 · ENVÍO GRATIS" (2 frascos, recorte do kit3) + narração + legenda + selo "ENVÍO GRATIS A DOMICILIO / PAGO CONTRA ENTREGA / ¡PAGAS AL RECIBIR!" (desde "envío") + setas em "Toca", via `montar_ad.py` (720x1280).
- Narração (voz de banco "chilena" `uHo8F3FY11rc2LxCwDSB`; o vídeo original não tem fala, nada a clonar): "Se llama Lymphoria. Compre uno y reciba dos, con envío gratis, y pagas al recibir en tu casa. Y tienes noventa días de garantía. Toca el botón de abajo y pide el tuyo." 167 caracteres = US$ 0,028, dividido entre os 4 vídeos (≈ US$ 0,007 cada).
- Dose: nenhum dos 4 vídeos diz dose; o fim não cita dose.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 15.37 s, parte 1 intacta, e fim novo com takes Lymphoria (ad03/t2_edit, ad19/t1_edit, ad22/t1_edit). Mesma voz do fim anterior (chilena), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 24.6 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
