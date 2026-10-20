---
name: feedback-orcamento-com-tempo
description: Todo orçamento de produção deve trazer também o tempo médio de produção e a opção paga mais rápida
metadata:
  node_type: memory
  type: feedback
  originSessionId: fefd88e1-1970-4576-a429-cf0c1248f170
  modified: 2026-10-04T01:39:52.220Z
---

Ao orçar qualquer produção (lote de ADs, gerações, upscales), mostrar lado a lado: custo em US$ E tempo médio estimado até ficar pronto. Quando existir alternativa paga que acelera (upscale na nuvem, render paralelo, modelo mais rápido), mostrar as duas opções: "grátis/local: X h" vs "pago: +US$Y, Z min".

**Why:** usuário disse (03/10/2026) "às vezes vale mais a pena pagar um pouco mais pra terminar mais rápido" — depois de esperar ~3 h pelo lote 1 processado só no PC.
**How to apply:** referências medidas no PC dele (RTX 4070): upscale Real-ESRGAN ≈ 3× a duração do vídeo; upscale 2× (720p) ≈ 1× a duração (30 s em 32 s); montagem pelo kit com PC livre ≈ 0,1–0,2× a duração (AD 06: 8 s para 71 s em 720p; com outra tarefa em paralelo sobe para ~0,7×) (montar_ad.py usa o caminho rápido de 1 passada desde 03/10/2026; `--classico` = antigo, 1–1,5×); vídeos > ~2,5 min não cabem em 30 MB com qualidade → finalizar.py usa 1.500 kbps e passa do limite com aviso (antes entrava em looping infinito — corrigido 03/10/2026; nunca rodar 2 montagens longas em paralelo); Kling O1 Edit no Flora ≈ 3–7 min por take, em paralelo; narração ElevenLabs ≈ segundos. Relacionado: [[feedback-mostrar-tempo-restante]], [[project-lymphoria-adaptacao-ads]]
