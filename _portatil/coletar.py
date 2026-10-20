# -*- coding: utf-8 -*-
"""Junta em _portatil/ o que mora FORA da pasta do projeto e precisa ir para o GitHub:
- claude-home/: CLAUDE.md global, hooks, mods (sem tipos gerados), memória do projeto e settings.json (sem chaves);
- producoes/: só os scripts e documentos (.py .md .json .txt .sh .ps1 .ass) das pastas de lote em Downloads.
Rode de novo sempre que quiser atualizar o repositório:  python _portatil/coletar.py
"""
import json, os, re, shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CASA = Path.home() / ".claude"
DOWN = Path.home() / "Downloads"
PROJ = RAIZ.parent
EXT = {".py", ".md", ".json", ".txt", ".sh", ".ps1", ".ass", ".csv", ".jsonl"}
MAX = 400_000  # bytes por arquivo de texto
SENSIVEL = re.compile(r"X-Amz-|Signature=|signature=|amazonaws\.com|access_token|Bearer [A-Za-z0-9]|xi-api-key\"?\s*:\s*\"[A-Za-z0-9]|x-api-key\"?\s*:\s*\"[A-Za-z0-9]|sk_[A-Za-z0-9]{24,}|gh[pousr]_[A-Za-z0-9]{30,}|EAA[A-Za-z0-9]{40,}|AKIA[0-9A-Z]{16}")
PULAR = {"_vg", "site-packages", "__pycache__", "node_modules", "htdemucs", "sep", "venv", ".venv", "frames", "folhas", "lama", "tmp"}

def copiar_arvore(src: Path, dst: Path, so_texto=True):
    n = 0
    for raiz, pastas, arqs in os.walk(src):
        pastas[:] = [p for p in pastas if p not in PULAR and not p.startswith(".git")]
        for a in arqs:
            f = Path(raiz) / a
            if so_texto and (f.suffix.lower() not in EXT or f.stat().st_size > MAX): continue
            if a.startswith(".env") or "secret" in a.lower() or "credential" in a.lower(): continue
            if so_texto:
                try:
                    txt = f.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if SENSIVEL.search(txt): continue   # URL assinada, token ou chave: nunca vai para o GitHub
            alvo = dst / f.relative_to(src); alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, alvo); n += 1
    return n

def main():
    home = RAIZ / "claude-home"
    if home.exists(): shutil.rmtree(home)
    home.mkdir(parents=True)
    if (CASA / "CLAUDE.md").exists(): shutil.copy2(CASA / "CLAUDE.md", home / "CLAUDE.md")
    copiar_arvore(CASA / "hooks", home / "hooks")
    mods = CASA / "mods"
    for m in (mods.iterdir() if mods.exists() else []):
        if m.is_dir():
            for raiz, pastas, arqs in os.walk(m):
                pastas[:] = [p for p in pastas if p != "types" or Path(raiz).name != ".claude-plugin"]
                for a in arqs:
                    if a.endswith(".bak-20261019") or a.startswith(".env"): continue
                    f = Path(raiz) / a; alvo = home / "mods" / f.relative_to(mods); alvo.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, alvo)
    mem = CASA / "projects" / "c--Users-PICHAU-Downloads-Produtividade-com-ia" / "memory"
    copiar_arvore(mem, home / "memory")
    s = json.loads((CASA / "settings.json").read_text(encoding="utf-8"))
    s.pop("env", None)  # caminhos desta máquina; o guia explica como recriar
    (home / "settings.exemplo.json").write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")

    prod = RAIZ / "producoes"
    if prod.exists(): shutil.rmtree(prod)
    total = 0
    for d in sorted(DOWN.iterdir()):
        if not d.is_dir() or d.resolve() == PROJ.resolve() or d.name.startswith((".", "001-", "1-", "2-", "3-", "4-", "6-")): continue
        n = copiar_arvore(d, prod / re.sub(r"[^\w.-]+", "_", d.name))
        total += n
    print("claude-home ok · producoes:", total, "arquivos")

if __name__ == "__main__":
    main()
