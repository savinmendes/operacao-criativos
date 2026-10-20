---
name: feedback-baixar-videos-maior-qualidade
description: "Sempre baixar vídeos na maior qualidade disponível (≥720p); na Biblioteca de Anúncios do Meta pegar o video_hd_url, nunca o src do player (360p)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: fefd88e1-1970-4576-a429-cf0c1248f170
  modified: 2026-10-07T19:39:43.310Z
---

Ao baixar vídeos (Biblioteca de Anúncios do Meta, TikTok, Drive, qualquer fonte), sempre pegar a **maior qualidade disponível, acima de 720p**. Se a fonte só tiver abaixo de 720p, avisar a pessoa antes de produzir.

**Why:** pedido da pessoa em 07/10/2026, depois que o 1º download da Biblioteca veio em 360x640 (o `<video src>` do player é a versão SD) e a versão HD 720x1280 existia nos dados da página.
**How to apply:** na Biblioteca do Meta, capturar `video_hd_url` nas respostas da página (script `Downloads/ADLIB-104060992792639/buscar_hd.py`, Playwright + Chrome headless) em vez do `src` do player; conferir com `ffprobe` que saiu ≥720p; deduplicar por md5 (a mesma página sobe o mesmo vídeo em vários anúncios). Em yt-dlp, usar `-f "bv*+ba/b"`. Relacionado: [[feedback-720p-padrao-origem-baixa]]
