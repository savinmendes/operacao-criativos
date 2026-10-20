---
name: feedback-mostrar-tempo-restante
description: "Em tarefas demoradas (renders, varreduras, lotes, gerações IA), mostrar progresso e tempo restante estimado"
metadata:
  node_type: memory
  type: feedback
  originSessionId: fefd88e1-1970-4576-a429-cf0c1248f170
  modified: 2026-10-03T21:02:03.745Z
---

Usuário quer ver quanto falta para terminar processos longos (03/10/2026).

**Why:** pediu "alguma coisa que mostre o tempo faltante para terminar".
**How to apply:** scripts longos devem imprimir `[k/N] item | % | decorrido | falta ~X` (ver `kit-edicao-criativos/ferramentas/folhas_contato.py` como modelo). Ao rodar algo em background ou esperar Flora/HeyGen/upscale, informar na mensagem o tempo estimado restante (ex.: "upscale 2.700/3.228 quadros, falta ~3 min"). Relacionado: [[feedback-abrir-video-ao-terminar]]
