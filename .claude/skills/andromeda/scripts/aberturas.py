"""Compara as aberturas (primeiros segundos) dos vídeos de um lote e aponta os pares visualmente parecidos.

A Meta não publica como agrupa criativos parecidos; este script é só um sinal prático: se as aberturas de dois
anúncios são quase iguais numa grade, há boa chance de serem tratados como o mesmo criativo.

Uso:  python aberturas.py <pasta-ou-videos...> [--saida pasta] [--limiar 0.85] [--tempos 0.2,1,2]
Saída: aberturas.json (matriz e pares parecidos) + aberturas_grade.jpg. Código 1 quando acha par parecido.
"""
import argparse
import functools
import itertools
import json
import os
import subprocess
import sys
from io import BytesIO

from PIL import Image, ImageDraw

EXT = (".mp4", ".mov", ".m4v", ".webm", ".mkv")
TEMPOS = (0.2, 1.0, 2.0)


@functools.lru_cache(maxsize=None)
def _duracao(video):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", video],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def _quadro(video, t, largura=180):
    """Quadro no tempo t (limitado à duração), como imagem PIL RGB. Cada quadro é extraído uma vez só."""
    return _quadro_cache(video, t, largura).copy()


@functools.lru_cache(maxsize=None)
def _quadro_cache(video, t, largura):
    dur = _duracao(video)
    if dur:
        t = min(t, max(dur - 0.05, 0))
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
         "-vf", f"scale={largura}:-2", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True,
    )
    if not r.stdout:
        raise RuntimeError(f"não consegui ler o quadro {t}s de {video}: {r.stderr.decode(errors='ignore')[:200]}")
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def _dhash(img):
    g = img.convert("L").resize((9, 8), Image.LANCZOS)
    px = list(g.tobytes())
    return "".join("1" if px[l * 9 + c] > px[l * 9 + c + 1] else "0" for l in range(8) for c in range(8))


def assinatura(video, tempos=TEMPOS):
    """Lista de hashes de 64 bits, um por tempo da abertura."""
    return [_dhash(_quadro(video, t)) for t in tempos]


def similaridade(sig_a, sig_b):
    """0 a 1: média, quadro a quadro, da fração de bits iguais."""
    vals = [sum(x == y for x, y in zip(a, b)) / len(a) for a, b in zip(sig_a, sig_b)]
    return sum(vals) / len(vals)


def _listar(entradas):
    vids = []
    for e in entradas:
        if os.path.isdir(e):
            vids += sorted(os.path.join(e, f) for f in os.listdir(e) if f.lower().endswith(EXT))
        elif e.lower().endswith(EXT):
            vids.append(e)
    return vids


def comparar(videos, limiar=0.85, tempos=TEMPOS):
    sigs = {v: assinatura(v, tempos) for v in videos}
    nomes = [os.path.basename(v) for v in videos]
    matriz = [[round(similaridade(sigs[a], sigs[b]), 3) for b in videos] for a in videos]
    parecidos = []
    for i, j in itertools.combinations(range(len(videos)), 2):
        if matriz[i][j] >= limiar:
            parecidos.append({"a": nomes[i], "b": nomes[j], "similaridade": matriz[i][j]})
    parecidos.sort(key=lambda p: -p["similaridade"])
    return {"limiar": limiar, "tempos": list(tempos), "videos": nomes, "matriz": matriz, "parecidos": parecidos}


def grade(videos, caminho, tempos=TEMPOS, largura=180):
    linhas = []
    for v in videos:
        quadros = [_quadro(v, t, largura) for t in tempos]
        h = max(q.height for q in quadros)
        linha = Image.new("RGB", (largura * len(quadros), h + 22), "white")
        for k, q in enumerate(quadros):
            linha.paste(q, (k * largura, 22))
        ImageDraw.Draw(linha).text((4, 4), os.path.basename(v)[:60], fill="black")
        linhas.append(linha)
    img = Image.new("RGB", (max(l.width for l in linhas), sum(l.height for l in linhas)), "white")
    y = 0
    for l in linhas:
        img.paste(l, (0, y))
        y += l.height
    img.save(caminho, quality=85)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entradas", nargs="+")
    ap.add_argument("--saida", default=".")
    ap.add_argument("--limiar", type=float, default=0.85)
    ap.add_argument("--tempos", default=",".join(str(t) for t in TEMPOS))
    a = ap.parse_args()
    tempos = tuple(float(t) for t in a.tempos.split(","))
    videos = _listar(a.entradas)
    if len(videos) < 2:
        print("Preciso de pelo menos 2 vídeos.")
        return 2
    os.makedirs(a.saida, exist_ok=True)
    res = comparar(videos, a.limiar, tempos)
    with open(os.path.join(a.saida, "aberturas.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    grade(videos, os.path.join(a.saida, "aberturas_grade.jpg"), tempos)
    print(f"{len(videos)} vídeos, {len(res['parecidos'])} pares com abertura parecida (limiar {a.limiar}):")
    for p in res["parecidos"]:
        print(f"  {p['similaridade']:.2f}  {p['a']}  x  {p['b']}")
    return 1 if res["parecidos"] else 0


if __name__ == "__main__":
    sys.exit(main())
