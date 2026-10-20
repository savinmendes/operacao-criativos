# -*- coding: utf-8 -*-
"""Busca nas transcrições e fichas da base de cases.

Camada de verificação: a ficha diz onde procurar, isto traz o trecho literal com
timestamp para conferir antes de afirmar qualquer coisa.

A legenda automática não tem pontuação e escreve termo técnico de qualquer jeito
("ROAS" vira ruas/rost/RAS/Ross), então busca por termo único erra muito. Por
isso aceita vários termos e mostra quantos casaram em cada trecho.

Uso:
    python buscar.py <pasta> "upsell" "opcel" "opcial"
    python buscar.py <pasta> "connect rate" --contexto 2
    python buscar.py <pasta> "webinário" --so-fichas
"""
import argparse
import io
import os
import re
import sys
import unicodedata


def normalizar(s):
    """Minúscula e sem acento — a legenda automática erra acentuação o tempo todo."""
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


_RE_BLOCO = re.compile(r"^\*\*\[([0-9:]+)\]\*\*\s*(.*)$")


def blocos_do_arquivo(caminho):
    saida = []
    with io.open(caminho, encoding="utf-8") as f:
        for i, linha in enumerate(f, 1):
            m = _RE_BLOCO.match(linha.strip())
            if m:
                saida.append({"linha": i, "tempo": m.group(1), "texto": m.group(2).strip()})
            elif linha.strip():
                saida.append({"linha": i, "tempo": None, "texto": linha.strip()})
    return saida


def buscar(pasta, termos, contexto=0, so_fichas=False, limite=60):
    termos_n = [normalizar(t) for t in termos if t.strip()]
    if not termos_n:
        return []

    alvos = []
    for raiz, _, arquivos in os.walk(pasta):
        if so_fichas and "_fichas" not in raiz:
            continue
        for n in sorted(arquivos):
            if n.lower().endswith(".md"):
                alvos.append(os.path.join(raiz, n))

    achados = []
    for caminho in alvos:
        bs = blocos_do_arquivo(caminho)
        for i, b in enumerate(bs):
            alvo = normalizar(b["texto"])
            casaram = [t for t in termos_n if t in alvo]
            if not casaram:
                continue
            ini, fim = max(0, i - contexto), min(len(bs), i + contexto + 1)
            achados.append({
                "arquivo": os.path.basename(caminho),
                "tempo": b["tempo"], "linha": b["linha"],
                "casaram": len(casaram),
                "trecho": " ".join(x["texto"] for x in bs[ini:fim]),
            })
    # mais termos casados primeiro: trecho que junta vários é o mais relevante
    achados.sort(key=lambda a: (-a["casaram"], a["arquivo"], a["linha"]))
    return achados[:limite]


def main():
    p = argparse.ArgumentParser(description="Busca na base de cases.")
    p.add_argument("pasta", help="pasta com as transcrições (e _fichas dentro)")
    p.add_argument("termos", nargs="+", help="um ou mais termos; variações ajudam")
    p.add_argument("--contexto", type=int, default=0, help="blocos vizinhos a incluir")
    p.add_argument("--so-fichas", action="store_true", help="busca só nas fichas")
    p.add_argument("--limite", type=int, default=60)
    a = p.parse_args()

    r = buscar(a.pasta, a.termos, a.contexto, a.so_fichas, a.limite)
    if not r:
        print("Nada encontrado para: %s" % ", ".join(a.termos))
        print("A legenda automática troca muito termo técnico — tente variações.")
        return 1

    print("%d trecho(s):\n" % len(r))
    for x in r:
        marca = " [%d termos]" % x["casaram"] if x["casaram"] > 1 else ""
        print("--- %s · %s · linha %d%s" %
              (x["arquivo"][:60], x["tempo"] or "-", x["linha"], marca))
        print(x["trecho"][:700])
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
