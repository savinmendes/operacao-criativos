---
name: feedback-720p-padrao-origem-baixa
description: Criativo cuja origem é baixa resolução (ex. 360p) sai SEMPRE em 720x1280 (upscale 2x); 1080x1920 só para vencedores ou origem já em alta
metadata:
  node_type: memory
  type: feedback
  originSessionId: fefd88e1-1970-4576-a429-cf0c1248f170
  modified: 2026-10-04T01:38:32.607Z
---

Quando o vídeo original é de baixa resolução (360p/480p) e precisa de upscale, o padrão é entregar em **720×1280** (Real-ESRGAN `realesr-animevideov3` escala 2, receita com `"resolucao": "720"`). 1080×1920 só quando: origem já é ≥720p, ou o AD virou vencedor e vale refazer.

**Why:** teste lado a lado (03/10/2026, AD 03): diferença "imperceptível" (palavra do usuário), metade do tempo (32 s vs 64 s para 30 s de vídeo) e metade do tamanho (vídeos curtos voltam a caber em 30 MB). Usuário mandou "colocar na base para sempre fazer em 720p quando for assim".
**How to apply:** upscale com `--escala 2`; montagem com `"resolucao": "720"` (montar_ad_rapido escala o final e usa piso de 900 kbps). Orçar tempo com upscale ≈1,5× a duração. Relacionado: [[feedback-orcamento-com-tempo]], [[project-lymphoria-adaptacao-ads]]
