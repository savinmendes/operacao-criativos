# -*- coding: utf-8 -*-
"""Importa fichas preenchidas (vindas de outro chat/download) para a base.

Casa pelo ID do vídeo, que vem depois de `__` no nome
(ex.: `...Escala 171__iHl26ShFJJ4.ficha.md`). Downloads costumam perder `#` e
acentos, então o nome inteiro não serve. O esqueleto antigo fica guardado em
`_fichas/_esqueletos/`. Só importa ficha sem `[PREENCHER]`.

Uso:
    python importar_fichas.py <pasta-com-fichas-baixadas> <pasta-da-base>
"""
import io
import os
import re
import shutil
import sys

_RE_ID = re.compile(r"__([A-Za-z0-9_-]{11})\.ficha\.md$")


def video_id(nome):
    m = _RE_ID.search(nome)
    return m.group(1) if m else None


def importar(origem, base):
    destinos = {}
    for raiz, _, arquivos in os.walk(os.path.join(base, "transcricoes")):
        if os.path.basename(raiz) != "_fichas":
            continue
        for a in arquivos:
            if video_id(a):
                destinos[video_id(a)] = os.path.join(raiz, a)
    feitos, pulados = [], []
    for a in sorted(os.listdir(origem)):
        vid = video_id(a)
        if not vid or vid not in destinos:
            continue
        src = os.path.join(origem, a)
        if os.path.abspath(src) == os.path.abspath(destinos[vid]):
            continue
        texto = io.open(src, encoding="utf-8").read()
        if re.search(r"^\[PREENCHER", texto, re.M):  # a nota "> `[PREENCHER]` exigem..." do topo não conta
            pulados.append(a)
            continue
        dst = destinos[vid]
        bak = os.path.join(os.path.dirname(dst), "_esqueletos")
        os.makedirs(bak, exist_ok=True)
        if not os.path.exists(os.path.join(bak, os.path.basename(dst))):
            shutil.copy2(dst, os.path.join(bak, os.path.basename(dst)))
        io.open(dst, "w", encoding="utf-8").write(texto)
        feitos.append(os.path.basename(dst))
    return feitos, pulados


if __name__ == "__main__":
    f, p = importar(sys.argv[1], sys.argv[2])
    print(f"importadas {len(f)}" + (f" · ignoradas (ainda com [PREENCHER]) {len(p)}" if p else ""))
    for x in f:
        print("  ✓", x)
