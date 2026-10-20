# V09 → LYMPHORIA-TE-PASO-EL-DATO (09/10/2026)
- **Saída:** `LYMPHORIA-ES-CL\V09 - LYMPHORIA-TE-PASO-EL-DATO.mp4` · 31,0 s · 720x1280 · 17,9 MB
- **Autorização:** a criadora autorizou o uso de imagem e voz (briefing de produção de 09/10). Por isso foi feito o clone da voz.
- **Trocas:**
  - Gancho 0–13,35 s ("Si tú sufres mucho de retención de líquido… eso es para esto."), cortado antes de "Lo agarré porque tiene muy buenas reseñas…". Assim saem a menção a "el otro video de mi página principal" e o "te dejo el enlace".
  - Frasco Nature's Sunshine (outra marca) desfocado no gancho inteiro: desfoque que acompanha o frasco (tracker CSRT do OpenCV, `trk.py` e `blur.py`, com margem de 22%). O frasco fica fora de quadro em 9–11 s. O rosto não foi coberto.
  - Ponte e fim (13,35–31,0 s) na voz clonada da criadora: "Se llama Lymphoria, son gotitas de drenaje linfático con hierbas naturales. Ahora está en compre uno y reciba dos, con envío gratis, y pagas al recibir en tu casa. Y tienes noventa días de garantía. Toca el botón de abajo y pide el tuyo." Por baixo, takes Lymphoria já produzidos e o card de oferta. A voz clonada fala em off (sem rosto), então não precisa de lipsync.
  - Legenda grande no vídeo inteiro, com o texto corrigido ("drenaje linfático" no lugar do "drena gel infático" que o whisper ouviu) e tempos por palavra.
- **Voz:** clone `wSs8c9kFDWX0X0ApjEga` ("Vitaly V09 creadora", amostra de 0–37 s; o clone instantâneo não tem custo). Registrado em `VOZES-CLONADAS.md`. TTS de 237 caracteres.
- **Custo:** US$ 0,039.
- **Revisão:** `revisar_ad.py` → RESULTADO OK (proibidos: nenhum; pts sem salto; sem quadro solto; setas no último quadro). O whisper confere a fala: gancho original + "Se llama linforia…" na voz clonada.
- **Para olhar:** o claim de detox "eliminar las toxinas" é do original e foi mantido (o V09 não está na lista de suavização). O sotaque da criadora não é chileno.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 13.37 s, parte 1 intacta, e fim novo com takes Lymphoria (ad16/t2_edit, ad14/t6_edit, ad11/t2_edit). Mesma voz do fim anterior (v09), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 22.6 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
