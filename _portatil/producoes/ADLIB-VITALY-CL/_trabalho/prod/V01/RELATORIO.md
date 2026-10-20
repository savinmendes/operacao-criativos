# V01 → LYMPHORIA-TE-TRANSFORMA (09/10/2026)
- **Saída:** `LYMPHORIA-ES-CL\V01 - LYMPHORIA-TE-TRANSFORMA.mp4` · 22,6 s · 720x1280 · 12,6 MB
- **Trocas:**
  - Corte de 6,33–8,00 s (as duas cenas com a camiseta "ABOLISH ICE"; nessas cenas também aparecia de perto o frasco de outra marca). Ficou 0–6,33 s (gancho + "te levantas sin hinchazón") + 8,00–9,63 s ("2 gotas en agua por las mañanas": dose mantida como o vídeo diz).
  - Frasco de outra marca na cena final (8,0–9,6 s, canto inferior): desfocado (`desfocar_regioes.py`, força 60). Ilegível no zoom.
  - Upscale Real-ESRGAN 2x (576x1024 → 1152x2048) e saída em 720x1280.
  - Fim novo igual ao V05: takes Lymphoria já produzidos + card com a oferta + selo + setas.
- **Voz:** narração Carolina (`cIBxLwfshLYhRB9lCXEg`), a mesma do V05. O original não tem fala.
- **Custo:** US$ 0,018 (metade da narração compartilhada).
- **Revisão:** `revisar_ad.py` → RESULTADO OK (proibidos: nenhum; pts sem salto; sem quadro solto).
- **Para olhar:** o texto queimado "transhorma" é erro de digitação do original e foi mantido. Há um salto de música no corte de 6,33 s, que soa como um corte de montagem normal.

## CTA v2 (10/10/2026)
- Fim refeito (sem card/preço, sem selo grande): corte em 7.90 s, parte 1 intacta, e fim novo com takes Lymphoria (V1_gotero_hierbas, ad14/t3_edit, P1_kit3). Mesma voz do fim anterior (carolina), encurtada e sem preço. Legenda palavra a palavra, selo amarelo pequeno "PAGO CONTRA ENTREGA" e setas vermelhas no CTA. Música contínua a -32 LUFS por baixo (exceto no V09, cujo original não tem música). Duração nova: 17.3 s. revisar_ad.py: RESULTADO OK. Antigo em `LYMPHORIA-ES-CL\_versao-cta-antigo\`. Scripts em `_cta_v2\`.
