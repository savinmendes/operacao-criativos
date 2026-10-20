# -*- coding: utf-8 -*-
"""Gera os PNGs de camada (transparentes, 1080 de largura) usados na montagem:

  manchete -> caixa branca arredondada com texto preto (Poppins Bold) e emojis coloridos
  faixa_sb -> faixa de topo do San Benito ("‼️ Un último aviso ‼️ ...")
  selo     -> selo COD (faixa preta + bloco amarelo + faixa vermelha), cobre selo/texto do concorrente
  seta     -> seta vermelha com contorno branco (o vídeo anima com overlay y=...sin(t))

Uso rápido:
  python overlays.py manchete "¡CORTA HASTA ÁRBOLES! 😱" -o m.png
  python overlays.py selo "SIN BENCINA · 100% ELÉCTRICA|PAGO CONTRA|ENTREGA|¡PAGAS AL RECIBIR!" -o selo.png
  python overlays.py seta -o seta.png
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from comum import POPPINS, W, emoji_font  # noqa: E402

EMOJI_RE = re.compile("([\U0001F000-\U0001FAFF☀-➿‼⁉️‍]+)")


def _desenha_linha(img: Image.Image, xy, texto: str, fonte: ImageFont.FreeTypeFont, cor="black"):
    """Desenha texto misturando Poppins e emoji colorido. Retorna a largura."""
    d = ImageDraw.Draw(img)
    ef = emoji_font()
    x, y = xy
    for parte in EMOJI_RE.split(texto):
        if not parte:
            continue
        if EMOJI_RE.fullmatch(parte) and ef:
            limpa = parte.replace("️", "")
            try:
                # fontes de emoji bitmap só aceitam tamanho fixo (109 Noto / 137 Apple); escalamos depois
                f = ImageFont.truetype(str(ef), 109)
                tmp = Image.new("RGBA", (int(f.getlength(limpa)) + 10, 140), (0, 0, 0, 0))
                ImageDraw.Draw(tmp).text((0, 10), limpa, font=f, embedded_color=True)
                bb = tmp.getbbox()
                if bb:
                    tmp = tmp.crop(bb)
                    alvo = int(fonte.size * 0.95)
                    tmp = tmp.resize((max(1, int(tmp.width * alvo / tmp.height)), alvo), Image.LANCZOS)
                    img.alpha_composite(tmp, (int(x), int(y + fonte.size * 0.12)))
                    x += tmp.width + 4
                continue
            except OSError:
                pass
        d.text((x, y), parte, font=fonte, fill=cor)
        x += fonte.getlength(parte)
    return x - xy[0]


def _largura(texto, fonte):
    return sum(fonte.getlength(p) if not EMOJI_RE.fullmatch(p) else fonte.size for p in EMOJI_RE.split(texto) if p)


def _quebra(texto, fonte, maxw):
    linhas, cur = [], ""
    for p in texto.split():
        t = (cur + " " + p).strip()
        if _largura(t, fonte) > maxw and cur:
            linhas.append(cur)
            cur = p
        else:
            cur = t
    return linhas + [cur]


def manchete(texto: str, destino: str, px: int = 64, maxw: int = 920, borda: bool = True) -> str:
    """Caixa branca arredondada centralizada (largura total 1080, use overlay=0:Y)."""
    f = ImageFont.truetype(str(POPPINS), px)
    linhas = [l for parte in texto.split("\n") for l in _quebra(parte, f, maxw)]
    lh = int(px * 1.25)
    bw = int(max(_largura(l, f) for l in linhas)) + 70
    bh = lh * len(linhas) + 40
    img = Image.new("RGBA", (W, bh + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0 = (W - bw) // 2
    d.rounded_rectangle((x0, 0, x0 + bw, bh), 28, fill=(255, 255, 255, 245),
                        outline=(17, 17, 17, 255) if borda else None, width=4 if borda else 0)
    for i, l in enumerate(linhas):
        lw = _largura(l, f)
        _desenha_linha(img, ((W - lw) / 2, 20 + lh * i + (lh - px * 1.2) / 2), l, f, (17, 17, 17))
    img.save(destino)
    return destino


def faixa_sb(destino: str, texto: str = "‼️ Un último aviso ‼️\nQuedate hasta el final y presta mucha atención 🙏🔮✨❤️") -> str:
    """Faixa de topo padrão do San Benito (Poppins Bold 56, caixa branca). Use overlay=0:150."""
    return manchete(texto, destino, px=56, maxw=960, borda=False)


def selo(linhas: list[str], destino: str, largura: int = 760, escala: float = 1.0) -> str:
    """linhas = [faixa preta, linha amarela 1, linha amarela 2, faixa vermelha]; vazias são puladas.
    escala < 1 encolhe o selo inteiro (4:5 / 1:1); 1 = 760x360 como sempre."""
    preta, am1, am2, verm = (linhas + ["", "", "", ""])[:4]
    f1, f2, f3 = (ImageFont.truetype(str(POPPINS), s) for s in (38, 86, 40))
    h = 360
    img = Image.new("RGBA", (largura, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if preta:
        d.rounded_rectangle((0, 0, largura, 70), 14, fill=(17, 17, 17, 255))
        d.text((largura / 2, 36), preta, font=f1, fill="white", anchor="mm")
    d.rectangle((0, 64, largura, 290), fill=(255, 214, 0, 255))
    if am2:
        d.text((largura / 2, 128), am1, font=f2, fill=(17, 17, 17), anchor="mm")
        d.text((largura / 2, 228), am2, font=f2, fill=(17, 17, 17), anchor="mm")
    else:
        d.text((largura / 2, 177), am1, font=f2, fill=(17, 17, 17), anchor="mm")
    if verm:
        d.rounded_rectangle((60, 282, largura - 60, 356), 12, fill=(214, 20, 30, 255))
        d.text((largura / 2, 320), verm, font=f3, fill="white", anchor="mm")
    if escala != 1.0:
        img = img.resize((round(largura * escala), round(h * escala)), Image.LANCZOS)
    img.save(destino)
    return destino


def seta(destino: str, tam: int = 170, escala: float = 1.0) -> str:
    """Triângulo vermelho apontando para baixo com contorno branco (não depende de fonte).
    escala < 1 encolhe a seta (4:5 / 1:1); com escala 1 o PNG tem 194x194."""
    pad = 12
    img = Image.new("RGBA", (tam + 2 * pad, tam + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(pad, pad + tam * 0.15), (pad + tam, pad + tam * 0.15), (pad + tam / 2, pad + tam)]
    d.polygon(pts, fill=(230, 20, 20, 255), outline=(255, 255, 255, 255), width=10)
    if escala != 1.0:
        img = img.resize((round(img.width * escala), round(img.height * escala)), Image.LANCZOS)
    img.save(destino)
    return destino


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tipo", choices=["manchete", "faixa_sb", "selo", "seta"])
    ap.add_argument("texto", nargs="?", default="")
    ap.add_argument("-o", "--saida", required=True)
    ap.add_argument("--px", type=int, default=64)
    a = ap.parse_args()
    if a.tipo == "manchete":
        manchete(a.texto, a.saida, a.px)
    elif a.tipo == "faixa_sb":
        faixa_sb(a.saida) if not a.texto else faixa_sb(a.saida, a.texto.replace("\\n", "\n"))
    elif a.tipo == "selo":
        selo(a.texto.split("|"), a.saida)
    else:
        seta(a.saida)
    print("ok:", a.saida)


if __name__ == "__main__":
    main()
