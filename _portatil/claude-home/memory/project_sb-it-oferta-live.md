---
name: project-sb-it-oferta-live
description: "San Benito em ITALIANO (16/10/2026): os 9 vencedores do lote EN → IT, destino preghiera in diretta, base = lote EN, 9 agentes em paralelo"
metadata:
  type: project
---

16/10/2026: a pessoa vai subir campanha na Itália e confirmou ("confirmo") produzir os 9 vencedores SB em italiano. São os mesmos do lote EN: ADS 9, ADS 7, JESU V07, ADS 12.18, ADS 12.1 GD, ADS 6, ADS 20, ADS 12 e OP2 ASCENSAO B.
- **Destino:** oração ao vivo em italiano. CTA: "Tocca «Scopri di più» qui sotto e unisciti alla preghiera in diretta". "San Benedetto", sem preço.
- **Método B** sobre o `_trabalho` do lote EN, com as mesmas vozes (Jesus The Chosen e Brian, multilíngues).
- **Pasta:** `Downloads/SB-IT-OFERTA-LIVE/` (`BRIEFING_LOTE_IT.md`), um agente por vídeo.
- **Saldo HeyGen antes do lote:** 4.941 créditos.
- **Entrega planejada:** uma pasta `PARA-SUBIR` com `00_TITOLI-E-TESTI.txt`, como no EN.

Relacionado: [[project-sb-en-oferta-live]], [[project-san-benito-fr]]

**16/10/2026, entregue:** os 9 vídeos estão em `Downloads/SB-IT-OFERTA-LIVE/PARA-SUBIR/`, junto com `00_TITOLI-E-TESTI.txt`. Todos passaram no `revisar_ad.py` (it) e num revisor independente. ElevenLabs custou ~US$ 1. O saldo HeyGen marcava 4.938 logo depois do lote, mas a cobrança do modo speed pode demorar até ~1 h para aparecer. Foram ~33 jobs de lipsync.
- **Defeitos achados no lote EN, ainda não corrigidos:**
  - OP2: Jesus fica em quadro congelado entre ~15,0 e 17,3 s. É o offset errado do clipA no `compor_en.py`.
  - ADS 9: aparece 1 quadro com o selo FR "EN DIRECT" em 97,77 s. A correção no `compor.py` é `t >= LIVE - 0.02`.
