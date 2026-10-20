# V30 — LYMPHORIA-ANTES-AHORA
- **Saída:** `ADLIB-VITALY-CL\LYMPHORIA-ES-CL\V30 - LYMPHORIA-ANTES-AHORA.mp4` (20,3 s, 720x1280, ~10,8 MB)
- **Trocas:**
  1. Legenda "…linfático con **Vitaly**" (0–3,27 s, 99 quadros) → "**Lymphoria**": caixa branca opaca redesenhada no mesmo estilo (Poppins SemiBold preto, cantos arredondados), `trocar_caption.py`.
  2. Frasco Nature's Sunshine mostrado à câmera (2,67–5,37 s, 82 quadros): **Kling O1 Edit** (Flora, projeto Lymphoria, nó n254, ref. n59) → frasco Lymphoria "drenaje linfático". `encaixar_edit.py --sem-legenda` + composição própria (`flora/comp.py`): legenda branca e foto do "antes" voltam do original (o Kling as apagara). O `colar_produto.py` do kit foi testado e descartado: a restauração de branco trazia de volta as letras brancas do rótulo antigo.
  3. Transição do flash laranja (5,4–5,63 s): mistura gradual do último quadro Kling com o flash (`suavizar_flash.py`), porque o frasco novo × flash antigo virava corte duro (revisor acusava quadro solto).
  4. Frasco antigo pequeno/de relance depois (flash 5,39–5,66 s, mão à direita 6,37–7,8 s, 8,47–9,1 s): desfoque móvel por quadros-chave (`blur_movel.py` do lote Drenagem, `blur.json`).
- **Custo:** Kling 1 take US$ 0,706 + TTS ≈ US$ 0,007 = **≈ US$ 0,71** (teto 1,50). Sem QA Gemini (conferido por folha + zoom 3x quadro a quadro).
- **Revisão:** RESULTADO OK (proibidos nenhum, sem quadro solto, pts ok, setas ok). Folha 1 q/0,5 s em `rev/`, zoom do rótulo em `flora/comp_zoom.jpg`.
- **Revisão manual:** em ~3 dos 82 quadros (movimento rápido, ~3,3 s, ~4,4 s e 5,37 s) o rótulo Lymphoria do Kling fica embaralhado/espelhado por 1–2 quadros; o nome antigo não aparece. Antes/depois de rosto atribuído ao produto (risco Meta, do estudo).
## Fim Lymphoria (comum a V14/V22/V25/V30)
- `_fim_V14-V22-V25-V30/`: foto prod_1 (0–1,45 s) + card "COMPRE 1, RECIBA 2 · $34.990 · ENVÍO GRATIS" (2 frascos, recorte do kit3) + narração + legenda + selo "ENVÍO GRATIS A DOMICILIO / PAGO CONTRA ENTREGA / ¡PAGAS AL RECIBIR!" (desde "envío") + setas em "Toca", via `montar_ad.py` (720x1280).
- Narração (voz de banco "chilena" `uHo8F3FY11rc2LxCwDSB`; o vídeo original não tem fala, nada a clonar): "Se llama Lymphoria. Compre uno y reciba dos, con envío gratis, y pagas al recibir en tu casa. Y tienes noventa días de garantía. Toca el botón de abajo y pide el tuyo." 167 caracteres = US$ 0,028, dividido entre os 4 vídeos (≈ US$ 0,007 cada).
- Dose: nenhum dos 4 vídeos diz dose; o fim não cita dose.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 9.30 s, parte 1 intacta, e fim novo com takes Lymphoria (ad14/t2_edit, ad19/t3_edit, ad03/t2_edit). Mesma voz do fim anterior (chilena), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 18.5 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
