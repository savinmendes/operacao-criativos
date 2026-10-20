---
name: gerar-midia-ia
description: Gera imagens base, takes de vídeo IA, avatar falando e narração para criativos via MCPs Flora, HeyGen e ElevenLabs, com custo informado antes, QA por outra IA e organização do canvas. Use quando o Savin pedir imagens, takes, hooks com avatar ou áudio narrado.
---

# Gerar mídia com IA

**Antes de qualquer geração:** diga quantas peças × preço = total em US$. Nunca repita geração paga sem avisar.

## Imagens base (Flora)
- `flora_list_workspaces` → projeto do produto (crie um se não existir: "<Produto> — Criativos").
- Suba a foto ORIGINAL do produto/avatar (`flora_create_asset` com URL https, ou `source="signed-url"` + upload do arquivo local).
- Gere i2i com `i2i-gpt-image-2-5-flare`, 9:16, quality high (~US$0,073). Prompt: descrição EXATA do produto
  (cores, peças, acessórios), cena da dor/função, espaço livre 15% topo e 25% base para textos, fotorrealista, sem texto/logo.
- Faça 1, mostre, aprove; depois o lote. Arrume o canvas: grupo por lote, 5 colunas, sem sobrepor (`flora_arrange_canvas`).
- Salve prompt + node id em `imagens/<codigo>.txt` na pasta do produto.

## Takes de vídeo (Flora)
- `i2v-kling-2.5`, 5 s (~US$0,294) — 10 s só se pedido (~US$0,588). Prompt de movimento curto e físico.
- Kling não faz física de corte/destruição: para "máquina cortando", gere o ANTES (planta inteira) e use filmagem real
  ou só o 1º trecho limpo.
- **QA obrigatório:** cada take passa por `v2t-gemini-3.1-pro` (~US$0,025) com perguntas objetivas
  (produto igual à referência? física correta? deformação de mãos/rosto? texto/logo?). Responda APROVADO/REPROVADO + trecho limpo (s).
  Reprovado não entra no criativo; informe quantos passaram.
- Baixe os aprovados para `takes/` com o código (ex.: `DSM-CLIP-X04 ARVORES-10s.mp4`).

## Avatar falando (HeyGen)
- Imagem base aprovada → `create_video_from_image`: 9:16, 1080p, expressiveness high, fit cover, motionPrompt pequeno
  (manter dedo apontado, fundo com movimento sutil). Voz "JESU ESPANHOL" `485d82fb75ab42d397affd962ca338c4` ou a do produto.
- Polling a cada 30 s com `get_video` (5–8 min). Baixe para `takes/` ou `hooks/`.
- Corte o hook 0,35 s após a última palavra (`audio.py pausas` ou ffmpeg -t).

## Narração (ElevenLabs)
- Preferir `python ferramentas/tts_elevenlabs.py --arquivo roteiro.txt -o audio/narr.mp3 --voz divina|chilena` (gera o JSON de alinhamento para a legenda).
- Pelo MCP: 1 geração (não 4 variações), voz pela lista, modelo `eleven_multilingual_v2`.
- Roteiro no idioma do mercado, sem hora do dia, sem promessa de resultado.
