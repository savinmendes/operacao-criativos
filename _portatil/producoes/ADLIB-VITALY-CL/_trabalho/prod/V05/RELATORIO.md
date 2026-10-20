# V05 → LYMPHORIA-POV-10MIL-PASOS (09/10/2026)
- **Saída:** `LYMPHORIA-ES-CL\V05 - LYMPHORIA-POV-10MIL-PASOS.mp4` · 27,3 s · 720x1280 · 15,5 MB
- **Trocas:**
  - Rótulo Vitaly → "LYMPHORIA" na faixa marrom do frasco (10,20–11,27 s e 11,30–12,57 s), sem IA: `trocar_rotulo_faixa.py --caixa` com caixas por quadro geradas por template matching (`track.py`, `track2.py`). Zoom 3x conferido quadro a quadro (`zoomA.jpg`, `zoomB.jpg`, `q339z.png`): nenhum resto de "VITALY".
  - Vídeo original mantido inteiro (0–12,6 s, trend sem fala, textos na tela sem marca).
  - Fim novo (12,6–27,3 s): takes Lymphoria já produzidos (Drenagem UGC `V1_gotero_hierbas`, `V3_frasco_mesa`) + card de oferta (Compre 1, Reciba 2 $34.990 / 2→4 $59.990 / 3→6 $79.990, envío gratis, pagas al recibir, 90 días) + selo "Pago contra entrega" + setas no "Toca".
  - "Oferta 2x1" era só o título do anúncio: no texto novo virou "Compre 1, Reciba 2".
- **Voz:** narração do fim com voz de banco ElevenLabs "Carolina" (`cIBxLwfshLYhRB9lCXEg`, feminina latina), 216 caracteres. A mesma narração serve ao V01. O vídeo original não tem fala, então não houve clone.
- **Custo:** US$ 0,018 (metade dos US$ 0,036 da narração compartilhada com o V01). Kling não foi usado.
- **Revisão:** `revisar_ad.py` → RESULTADO OK (proibidos: nenhum; pts sem salto; sem quadro solto; setas no último quadro). Whisper: "Se llama Linforia…" (pronúncia certa da marca).
- **Para olhar:** antes/depois de corpo implícito (moletom → top vermelho), herdado do original.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 12.50 s, parte 1 intacta, e fim novo com takes Lymphoria (ad19/t1_edit, V3_frasco_mesa, ad11/t3_edit). Mesma voz do fim anterior (carolina), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 22.0 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
