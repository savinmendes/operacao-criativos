---
name: feedback-painel-ao-vivo
description: "Pessoa quer ver execuções em tempo real — registrar etapas no painel local (painel/painel.py, http://127.0.0.1:8765) e avisar por voz ao terminar"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 319d1003-9d4d-47ea-860c-6c7c0212f92e
  modified: 2026-10-10T11:14:45.253Z
---

A pessoa quer acompanhar visualmente o que acontece (Flora, Shopify, agentes) numa aba acoplada ao chat do VS Code. Painel local criado em 09/10/2026: `Produtividade com ia/painel/` (index.html lê status.json a cada 3 s; servidor `painel/iniciar.ps1`, porta 8765).

**Why:** pediu "uma janela acoplada aqui no chat para ver as execuções em tempo real".
**How to apply:** em toda tarefa longa, eu e cada agente chamamos `painel.py etapa/img/custo/link/fim` (instrução no CLAUDE.md do projeto). Antes de começar, rode `iniciar.ps1` se o servidor não responder. Também há hook de voz ("Sávio, terminei" / "Sávio, preciso de você") em `~/.claude/hooks/falar.ps1`.

**Título da aba = pedido mais recente (10/10/2026):** a cada pedido novo da pessoa, rode logo no início `python painel/painel.py pedido "<resumo curto do pedido>"`. Isso troca o título da aba do painel no VS Code e o topo da página, e ela usa isso para se achar entre as abas.

Feed automático (09/10/2026): hook global ~/.claude/hooks/atividade.py (PreToolUse/PostToolUse/UserPromptSubmit/Stop...) grava cada ação em painel/atividade.jsonl; o index.html mostra no quadro "O que o Claude está fazendo agora". Backup do settings: ~/.claude/settings.json.bak-atividade.
