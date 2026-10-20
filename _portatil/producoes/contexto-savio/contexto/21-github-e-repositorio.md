# GitHub: como manter este repositório

> Onde fica o repositório `contexto-savio`, quem tem acesso, o fluxo pull → editar → commit → push e o que nunca pode subir. Abra antes de atualizar qualquer arquivo daqui.

## Contexto de uso
- **Repositório:** `https://github.com/Grupo-Chegou-Geral/contexto-savio` (privado), branch `main`. Criado em 13/10/2026.
- **Clone local:** `C:\Users\PICHAU\Downloads\contexto-savio`.
- **GitHub CLI:** instalado em `C:\Program Files\GitHub CLI\gh.exe` (no Git Bash ele pode não estar no PATH: use o caminho completo ou o PowerShell). Logado como **savinmendes**, com acesso de administrador ao repositório. `gh auth setup-git` já foi feito, então `git push`/`git pull` usam a credencial do gh.
- **Conteúdo:** só `.md` (README como índice, `contexto/NN-*.md` por tema e `contexto/projetos/<slug>.md` por lote).
  - Scripts e código **não** foram copiados: a cópia em massa foi bloqueada por risco de levar chave junto, e a decisão ficou pendente com a pessoa.
  - Mídia e `.env` nunca entram.
- **Fonte das informações:** memórias do Claude Code desta máquina, `CLAUDE.md` do projeto e do kit, relatórios das pastas de lote em `Downloads\`. O repositório existe para quem clonar só ele conseguir trabalhar sem essa máquina.

## Lógica de uso

### Fluxo de atualização
```bash
cd /c/Users/PICHAU/Downloads/contexto-savio
git pull
# editar / criar .md
git status && git diff --stat
git add contexto/ README.md
git commit -m "<o que mudou, em português>

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push
```

### Regras de escrita
1. Todo arquivo segue `contexto/_MODELO.md`: título, linha `>`, **## Contexto de uso** (fatos, datas absolutas, onde estão os arquivos), **## Lógica de uso** (passo a passo, regras, comandos, armadilhas, checklist) e **## Relacionados**.
2. Português do Brasil, "a pessoa" (neutro). Lacuna = "precisa de revisão manual". Número de terceiro = "declarado".
3. Não reescreva arquivo inteiro: acrescente uma seção ou crie um arquivo novo. Edição pontual só para corrigir o que está errado ou desatualizado, e diga no commit o que mudou.
4. Lote novo → `contexto/projetos/<slug>.md` + uma linha em `projetos/00-indice-projetos.md`. Tema novo → `contexto/NN-<tema>.md` + uma linha no índice do `README.md`.
5. Não duplique: antes de escrever, procure (`grep -rni "<termo>" contexto`) e linke o arquivo que já cobre o tema.

### O que nunca sobe
- `.env`, `settings.local.json`, chaves de API, tokens, senhas, cookies.
- CPF/documentos, endereços, telefones, dados bancários, dados pessoais ou financeiros pessoais, dados de clientes.
- Nada de `001- INBOX` nem das pastas `pessoal`, `financeiro` e `recibos-e-comprovantes`.
- Mídia (vídeo, imagem, áudio), `.zip` e transcrições inteiras de terceiros. Só resumo e caminho.
- Pode subir: IDs de conta de anúncio, voice_id, ID de projeto Flora e ID de avatar (não são segredo), sempre sem a chave.

### Antes de cada commit: varredura de segredos
```bash
cd /c/Users/PICHAU/Downloads/contexto-savio
git diff --cached -U0 | grep -nEi "(sk-[A-Za-z0-9]{20,}|xi-api-key|api[_-]?key\s*[:=]|secret\s*[:=]|token\s*[:=]|password|senha\s*[:=]|Bearer [A-Za-z0-9]|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|EAA[A-Za-z0-9]{20,}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2})"
```
Saída vazia = ok. Qualquer acerto: revise e tire antes do commit.

### Armadilhas
- `gh: command not found` no Git Bash: use `"/c/Program Files/GitHub CLI/gh.exe"` ou o PowerShell.
- Conflito no `git pull`: outra máquina ou pessoa editou. Resolva preservando as duas versões; nunca use `push --force`.

## Relacionados
- [02-regras-gerais-e-seguranca.md](02-regras-gerais-e-seguranca.md)
- [17-orquestracao-agentes-e-painel.md](17-orquestracao-agentes-e-painel.md)
- [projetos/00-indice-projetos.md](projetos/00-indice-projetos.md)
