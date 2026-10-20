---
name: reference_repo-operacao-criativos
description: Repo privado github.com/savinmendes/operacao-criativos = a pasta do projeto inteira (sem chaves/mídia) p/ usar em outro PC; sincronizar com coletar.py + push / pull + restaurar.ps1
metadata:
  type: reference
---

Criado em 20/10/2026. A própria pasta "Produtividade com ia" é o repositório (branch main). O `.gitignore` funciona como lista branca: só entram código, skills, contexto e relatórios. Mídia, `.env`, `00-inbox`, `01-arquivos-organizados` e `08-entregas` ficam de fora.

`_portatil/` guarda:
- `claude-home/`: CLAUDE.md global, hooks, mods e memória;
- `producoes/`: os scripts dos lotes de Downloads;
- `coletar.py`, que atualiza essas cópias e pula qualquer arquivo com URL assinada ou chave;
- `restaurar.ps1`, que aplica tudo no ~/.claude do outro PC;
- `INSTALAR-NO-OUTRO-PC.md`.

**Why:** a pessoa quer os dois PCs (ambos dela) com tudo igual.
**How to apply:** depois de mudanças relevantes, rode `coletar.py`, faça commit e push. Antes de dar push, varra chaves de novo. Os scripts antigos dos lotes tinham URLs assinadas do HeyGen e ficaram de fora.
