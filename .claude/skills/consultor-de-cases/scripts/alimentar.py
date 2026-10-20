# -*- coding: utf-8 -*-
"""Fluxo 0: leva transcrições novas para a base de cases e mantém o índice.

Pega as transcrições `.md` geradas por qualquer transcritor que escreva o cabeçalho
padrão (título + tabela com Canal, Duração, Publicado e URL), copia para
`<base>/transcricoes/<canal>/`, gera o esqueleto de ficha das que ainda não têm
(via fichar.py) e reescreve `<base>/INDICE.md`.

Nunca apaga nem sobrescreve nada que já está na base.

Uso:
    python alimentar.py <pasta-de-transcricoes> <pasta-da-base> [--canal "nome"]
    python alimentar.py <pasta-da-base> --so-indice
"""
import argparse
import io
import os
import re
import shutil
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fichar import ler_metadados  # noqa: E402


def slug(s):
    s = unicodedata.normalize("NFD", (s or "sem-canal").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "sem-canal"


def _ler(caminho):
    with io.open(caminho, encoding="utf-8") as f:
        return f.read()


def alimentar(origem, base, canal=None):
    """Copia as transcrições novas (opcionalmente só de um canal) e gera fichas e índice."""
    copiados, ja, ignorados, pastas = 0, 0, 0, set()
    for nome in sorted(os.listdir(origem)):
        if not nome.endswith(".md"):
            continue
        meta = ler_metadados(_ler(os.path.join(origem, nome)))
        if canal and slug(meta.get("canal")) != slug(canal):
            ignorados += 1
            continue
        pasta = os.path.join(base, "transcricoes", slug(meta.get("canal")))
        destino = os.path.join(pasta, nome)
        if os.path.exists(destino):
            ja += 1
            continue
        os.makedirs(pasta, exist_ok=True)
        shutil.copy2(os.path.join(origem, nome), destino)
        copiados += 1
        pastas.add(pasta)
    for pasta in sorted(pastas):  # esqueleto de ficha só das pastas que receberam material
        subprocess_fichar(pasta)
    montar_indice(base, escrever=True)
    return {"copiados": copiados, "ja_estavam": ja, "ignorados": ignorados}


def subprocess_fichar(pasta):
    import subprocess
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fichar.py")
    subprocess.run([sys.executable, script, pasta, "--lote"], check=True,
                   stdout=subprocess.DEVNULL, env={**os.environ, "PYTHONIOENCODING": "utf-8"})


def montar_indice(base, escrever=True):
    """Tabela com todos os casos da base e o estado da ficha (esqueleto ou preenchida)."""
    raiz = os.path.join(base, "transcricoes")
    linhas = []
    if os.path.isdir(raiz):
        for canal_dir in sorted(os.listdir(raiz)):
            pasta = os.path.join(raiz, canal_dir)
            if not os.path.isdir(pasta):
                continue
            for nome in sorted(os.listdir(pasta)):
                if not nome.endswith(".md"):
                    continue
                meta = ler_metadados(_ler(os.path.join(pasta, nome)))
                ficha = os.path.join(pasta, "_fichas", nome[:-3] + ".ficha.md")
                if not os.path.exists(ficha):
                    estado = "sem ficha"
                elif re.search(r"^\[PREENCHER", _ler(ficha), re.M):
                    estado = "esqueleto"
                else:
                    estado = "preenchida"
                linhas.append((meta.get("canal") or canal_dir, meta.get("publicado") or "",
                               meta.get("duracao") or "", (meta.get("titulo") or nome[:-3]).replace("|", "/"),
                               f"transcricoes/{canal_dir}/{nome}", estado))
    total = len(linhas)
    feitas = sum(1 for l in linhas if l[5] == "preenchida")
    L = ["# Índice da base de cases", "",
         f"{total} casos · {feitas} fichas preenchidas · {total - feitas} faltando", "",
         "| Canal | Publicado | Duração | Título | Arquivo | Ficha |", "|---|---|---|---|---|---|"]
    L += [f"| {c} | {p} | {d} | {t} | `{a}` | {e} |" for c, p, d, t, a, e in linhas]
    texto = "\n".join(L) + "\n"
    if escrever:
        os.makedirs(base, exist_ok=True)
        with io.open(os.path.join(base, "INDICE.md"), "w", encoding="utf-8") as f:
            f.write(texto)
    return texto


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("caminhos", nargs="+", help="<origem> <base>, ou só <base> com --so-indice")
    p.add_argument("--canal", help="leva só as transcrições deste canal")
    p.add_argument("--so-indice", action="store_true", help="só reescreve o INDICE.md")
    a = p.parse_args()
    if a.so_indice:
        montar_indice(a.caminhos[0]); print("índice atualizado"); return 0
    if len(a.caminhos) != 2:
        p.error("informe <pasta-de-transcricoes> <pasta-da-base>")
    r = alimentar(a.caminhos[0], a.caminhos[1], a.canal)
    print(f"copiados {r['copiados']} · já estavam {r['ja_estavam']} · de outros canais {r['ignorados']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
