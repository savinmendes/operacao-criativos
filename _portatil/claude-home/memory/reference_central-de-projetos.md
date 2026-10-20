---
name: reference_central-de-projetos
description: Central de Projetos (mod do Grupo Chegou) instalada em OneDrive/Documentos/Central de Projetos; raiz de projetos C:/Users/PICHAU/Projetos-Central (junções)
metadata:
  type: reference
---

Instalada em 19/10/2026 a partir de github.com/Grupo-Chegou-Geral/central-de-projetos, em `C:/Users/PICHAU/OneDrive/Documentos/Central de Projetos`.

- `central.json` aponta `raiz` para `C:/Users/PICHAU/Projetos-Central`. Os projetos são junções nessa pasta; hoje só existe `produtividade-com-ia` → Downloads/Produtividade com ia. Projeto novo = junção nova ali.
- Regras locais estão em `CLAUDE.local.md`, excluído do git: gasto pago só com «confirmo» na central, debater criativo, nada destrutivo, cuidado com a voz online (edge-tts).
- O mod dispara agentes `claude -p --permission-mode auto` em cada projeto. Ele duplica a barra de uso e os próximos passos do mod [[reference_mod-progresso]].
- Atualizar: `git pull` na pasta e reiniciar o Claude Code.
