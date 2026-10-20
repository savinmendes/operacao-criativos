---
name: reference-mod-progresso
description: Mod "progresso" do Claude Code (painel de progresso, faixa 5h/modelo, próximos passos via AskUserQuestion, dicas de tokens) instalado em ~/.claude/mods/progresso via CLAUDE_CODE_PLUGIN_DIRS (14/10/2026)
metadata:
  type: reference
---

Fonte: `C:\Users\PICHAU\.claude\mods\progresso\` (hooks/register.tsx, types/index.d.ts, testes em hooks/register.test.ts). Registrado em `~/.claude/settings.json` → `env.CLAUDE_CODE_PLUGIN_DIRS` (com confirmação da pessoa). Validar/testar: `claude plugin validate|test C:\Users\PICHAU\.claude\mods\progresso`.
CLI do terminal atualizado 2.1.283 → 2.1.300 em 14/10/2026 (a 2.1.283 não conhecia o evento prompt.compose). O app desktop roda o seu próprio claude.exe.
A pergunta do engine "Enable hot reloading for this session?" aparece em inglês — explicar à pessoa em português antes.
