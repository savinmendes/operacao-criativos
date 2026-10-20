# -*- coding: utf-8 -*-
"""Compositor do agente C (vídeos sem narração do lote H2O X5).
Mantém o formato do original (720x720 / 720x900 / 720x1280), cobre o texto em inglês com rótulos opacos
(alpha 255) com o texto em espanhol, põe o selo "Pago contra entrega" e o CTA "Haz clic en Más información"
com setas vermelhas (overlays.seta do kit) e mantém o áudio original (ou outro, ou silêncio).

  python compor.py spec.json

spec = {
 "video": "...mp4", "saida": "...mp4", "W": 720, "H": 900,
 "audio": "orig" | "silencio" | "<arquivo>",
 "camadas": [
   {"tipo": "rotulo", "rect": [x0,y0,x1,y1], "linhas": ["..", ".."], "cores": ["#fff", "#ff0"], "fundo": "#3dae49",
    "raio": 16, "px": 40, "fonte": "bold|semi|medium", "alinhar": "centro|esq|dir", "de": 0, "ate": 9999, "pad": 14},
   {"tipo": "coracao", "rect": [...], "linhas": [...], "px": 40, "angulo": 30, "de": .., "ate": ..},
   {"tipo": "selo", "x": 20, "y": 20, "larg": 300, "linhas": ["PAGO CONTRA", "ENTREGA"], "fita": "¡PAGAS AL RECIBIR!", "de":..,"ate":..},
   {"tipo": "cta", "cx": 360, "y": 600, "px": 34, "de": 6.0, "setas_de": 6.3, "setas_x": [180, 420], "setas_y": 680,
    "seta_tam": 110, "fundo": "#ffffff"},
   {"tipo": "png", "arquivo": "x.png", "de": .., "ate": ..}
 ]
}
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import overlays as OV  # noqa: E402
from comum import COR  # noqa: E402

FONTES = {"bold": KIT / "fonts" / "Poppins-Bold.ttf", "semi": KIT / "fonts" / "Poppins-SemiBold.ttf",
          "medium": KIT / "fonts" / "Poppins-Medium.ttf"}
AMARELO = (255, 214, 0, 255)
VERMELHO = (214, 20, 30, 255)


def cor(c, a=255):
    if isinstance(c, (list, tuple)):
        return tuple(c[:3]) + (a,)
    c = c.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), a)


def fonte(nome, px):
    return ImageFont.truetype(str(FONTES.get(nome, FONTES["bold"])), px)


def bloco_texto(d, linhas, cores, f, box, alinhar="centro", entre=1.12):
    x0, y0, x1, y1 = box
    hs = [f.getbbox(l)[3] - f.getbbox("H")[1] for l in linhas]
    lh = int(f.size * entre)
    tot = lh * (len(linhas) - 1) + (f.getbbox("Hg")[3] - f.getbbox("H")[1])
    y = (y0 + y1) / 2 - tot / 2 - f.getbbox("H")[1]
    for k, l in enumerate(linhas):
        w = d.textlength(l, font=f)
        x = {"esq": x0, "dir": x1 - w}.get(alinhar, (x0 + x1) / 2 - w / 2)
        d.text((x, y), l, font=f, fill=cor(cores[k % len(cores)]))
        y += lh


def ajustar_px(d, linhas, nome, px, larg, alt, entre=1.12):
    while px > 10:
        f = fonte(nome, px)
        w = max(d.textlength(l, font=f) for l in linhas)
        h = int(px * entre) * (len(linhas) - 1) + px
        if w <= larg and h <= alt:
            return f
        px -= 1
    return fonte(nome, px)


def png_rotulo(c, W, H, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = c["rect"]
    d.rounded_rectangle([x0, y0, x1, y1], radius=c.get("raio", 16), fill=cor(c.get("fundo", "#ffffff")))
    pad = c.get("pad", 14)
    f = ajustar_px(d, c["linhas"], c.get("fonte", "bold"), c.get("px", 40), x1 - x0 - 2 * pad, y1 - y0 - 2 * pad,
                   c.get("entre", 1.12))
    bloco_texto(d, c["linhas"], c.get("cores", ["#000000"]), f, (x0 + pad, y0 + pad, x1 - pad, y1 - pad),
                c.get("alinhar", "centro"), c.get("entre", 1.12))
    img.save(destino)
    return destino


def heart_pts(cx, cy, s, ang):
    pts = []
    for k in range(240):
        t = 2 * math.pi * k / 240
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        a = math.radians(ang)
        xr, yr = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
        pts.append((cx + s * xr, cy + s * yr))
    return pts


def png_coracao(c, W, H, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy, s = c["cx"], c["cy"], c["escala"]
    if c.get("forma") == "circulo":
        r = c["raio_px"]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cor(c.get("fundo", "#5cb547")),
                  outline=(255, 255, 255, 255), width=c.get("contorno", 0))
    else:
        d.polygon(heart_pts(cx, cy, s, c.get("angulo", 0)), fill=cor(c.get("fundo", "#5cb547")))
    # texto num quadro à parte, girado
    tw, th = int(s * 24), int(s * 16)
    t = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    dt = ImageDraw.Draw(t)
    f = ajustar_px(dt, c["linhas"], "bold", c.get("px", 60), tw, th, 1.0)
    linhas, fs = c["linhas"], []
    if c.get("pxs"):   # tamanho por linha
        y = 0
        for l, p in zip(linhas, c["pxs"]):
            fl = fonte("bold", p)
            hb = fl.getbbox("H")
            dt.text(((tw - dt.textlength(l, font=fl)) / 2, y - hb[1]), l, font=fl, fill=(255, 255, 255, 255))
            y += int(p * 1.0)
        linhas = []
    # 1ª linha grande, demais menores
    f1 = ajustar_px(dt, [linhas[0] if linhas else "x"], "bold", c.get("px", 60), tw, th * 0.55, 1.0)
    f2 = ajustar_px(dt, linhas[1:] or ["x"], "bold", int(f1.size * 0.42), tw, th * 0.45, 1.05)
    if not linhas:
        t = t.crop((0, 0, tw, min(th, y + 4)))
        t = t.rotate(-c.get("angulo", 0) + c.get("angulo_texto", 0), expand=True, resample=Image.BICUBIC)
        ox, oy = c.get("texto_off", (0, 0))
        img.alpha_composite(t, (int(cx - t.width / 2 + ox), int(cy - t.height / 2 + oy)))
        img.save(destino)
        return destino
    y = 0
    hh1 = f1.getbbox("H")
    dt.text(((tw - dt.textlength(linhas[0], font=f1)) / 2, y - hh1[1]), linhas[0], font=f1, fill=(255, 255, 255, 255))
    y += hh1[3] - hh1[1] + int(f1.size * 0.12)
    for l in linhas[1:]:
        hb = f2.getbbox("H")
        dt.text(((tw - dt.textlength(l, font=f2)) / 2, y - hb[1]), l, font=f2, fill=(255, 255, 255, 255))
        y += int(f2.size * 1.08)
    t = t.crop((0, 0, tw, min(th, y + 4)))
    t = t.rotate(-c.get("angulo", 0) + c.get("angulo_texto", 0), expand=True, resample=Image.BICUBIC)
    ox, oy = c.get("texto_off", (0, 0))
    img.alpha_composite(t, (int(cx - t.width / 2 + ox), int(cy - t.height / 2 + oy)))
    img.save(destino)
    return destino


def png_selo(c, W, H, destino):
    """Selo compacto no padrão de cores do kit (amarelo + texto preto + fita vermelha)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x, y, w = c["x"], c["y"], c["larg"]
    linhas = c.get("linhas", ["PAGO CONTRA", "ENTREGA"])
    f = ajustar_px(d, linhas, "bold", c.get("px", 60), w - 28, 999, 1.0)
    lh = int(f.size * 1.02)
    h_am = lh * len(linhas) + 18
    d.rounded_rectangle([x, y, x + w, y + h_am], radius=12, fill=AMARELO, outline=(17, 17, 17, 255), width=3)
    bloco_texto(d, linhas, ["#111111"], f, (x + 14, y + 6, x + w - 14, y + h_am - 4), "centro", 1.02)
    if c.get("fita"):
        ff = ajustar_px(d, [c["fita"]], "bold", int(f.size * 0.6), w - 50, 999)
        fh = int(ff.size * 1.55)
        fy = y + h_am - 6
        d.rounded_rectangle([x + 18, fy, x + w - 18, fy + fh], radius=9, fill=VERMELHO, outline=(255, 255, 255, 255), width=2)
        bloco_texto(d, [c["fita"]], ["#ffffff"], ff, (x + 18, fy, x + w - 18, fy + fh))
    img.save(destino)
    return destino


def png_cta(c, W, H, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    px = c.get("px", 34)
    f1, f2 = fonte("semi", int(px * 0.8)), fonte("bold", px)
    l1, l2 = c.get("linhas", ["Haz clic en", "Más información"])
    w = max(d.textlength(l1, font=f1), d.textlength(l2, font=f2)) + 2 * c.get("pad", 26)
    h = int(px * 0.8 * 1.25) + int(px * 1.3) + 22
    cx, y = c["cx"], c["y"]
    d.rounded_rectangle([cx - w / 2, y, cx + w / 2, y + h], radius=18, fill=cor(c.get("fundo", "#ffffff")),
                        outline=cor(c.get("borda", "#d6141e")), width=c.get("borda_px", 4))
    d.text((cx - d.textlength(l1, font=f1) / 2, y + 10), l1, font=f1, fill=(17, 17, 17, 255))
    d.text((cx - d.textlength(l2, font=f2) / 2, y + 10 + int(px * 0.8 * 1.25)), l2, font=f2,
           fill=cor(c.get("cor2", "#d6141e")))
    img.save(destino)
    return destino


def seta_pequena(destino, tam):
    """Mesma seta do kit (triângulo vermelho, contorno branco), com contorno proporcional para tamanhos pequenos."""
    pad = max(3, tam // 14)
    img = Image.new("RGBA", (tam + 2 * pad, tam + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(pad, pad + tam * 0.15), (pad + tam, pad + tam * 0.15), (pad + tam / 2, pad + tam)]
    d.polygon(pts, fill=(230, 20, 20, 255), outline=(255, 255, 255, 255), width=max(2, tam // 17))
    img.save(destino)
    return destino


def compor(spec_path):
    sp = Path(spec_path).resolve()
    S = json.loads(sp.read_text(encoding="utf-8"))
    base = sp.parent
    P = lambda p: str((base / p).resolve()) if not Path(p).is_absolute() else p  # noqa: E731
    W, H = S["W"], S["H"]
    tmp = base / "_camadas"
    tmp.mkdir(exist_ok=True)
    ins = ["-i", P(S["video"])]
    fc = [f"[0:v]scale={W}:{H}:flags=lanczos,fps=30,setsar=1,format=yuv420p[v0]"]
    ult, n = "[v0]", 1
    fin = S.get("fps_in")

    def T(t):
        # tempo do original -> tempo da saída (30 fps): com 29,97 fps o quadro k cai em k/30, não em k/29,97
        if not fin or t <= 0 or t >= 90:
            return t
        return round(t * fin) / 30 - 0.005

    for k, c in enumerate(S["camadas"]):
        de, ate = T(c.get("de", 0)), T(c.get("ate", 9999))
        en = f":enable='between(t,{de},{ate})'"
        t = c["tipo"]
        if t in ("rotulo", "coracao", "selo", "cta", "png"):
            png = {"rotulo": png_rotulo, "coracao": png_coracao, "selo": png_selo, "cta": png_cta}.get(t)
            arq = png(c, W, H, str(tmp / f"c{k:02d}_{t}.png")) if png else P(c["arquivo"])
            ins += ["-loop", "1", "-i", arq]
            fc.append(f"{ult}[{n}:v]overlay=0:0:shortest=0:eof_action=pass{en}[o{n}]")
            ult, n = f"[o{n}]", n + 1
        if t == "cta":
            tam = c.get("seta_tam", 110)
            seta = OV.seta(str(tmp / f"seta_{tam}.png"), tam) if tam >= 80 else seta_pequena(str(tmp / f"seta_{tam}.png"), tam)
            sd = T(c.get("setas_de", c.get("de", 0)))
            amp = c.get("seta_amp", 12)
            for x in c["setas_x"]:
                ins += ["-loop", "1", "-i", seta]
                fc.append(f"{ult}[{n}:v]overlay={x}:'{c['setas_y']}+{amp}*sin(3*PI*t)':shortest=0"
                          f":enable='between(t,{sd},{ate})'[o{n}]")
                ult, n = f"[o{n}]", n + 1
    # duração = do vídeo original
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                P(S["video"])], capture_output=True, text=True).stdout.strip())
    vdur = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                 "stream=duration", "-of", "csv=p=0", P(S["video"])], capture_output=True,
                                text=True).stdout.strip() or dur)
    total = S.get("duracao", vdur)
    fc.append(f"{ult}trim=0:{total:.3f},setpts=PTS-STARTPTS[vout]")
    au = S.get("audio", "orig")
    if au == "silencio":
        ins += ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        fc.append(f"[{n}:a]atrim=0:{total:.3f}[aout]")
    else:
        ia = 0
        if au != "orig":
            ins += ["-i", P(au)]
            ia = n
        fc.append(f"[{ia}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{total:.3f},"
                  f"afade=t=out:st={max(0, total - 0.25):.3f}:d=0.25[aout]")
    saida = P(S["saida"])
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y", "-threads", "4", *ins, "-filter_complex", ";".join(fc),
           "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}",
           "-c:v", "libx264", "-profile:v", "high", "-crf", str(S.get("crf", 18)), "-preset", "medium",
           "-pix_fmt", "yuv420p", "-r", "30", *COR,
           "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-3000:])
        raise SystemExit(1)
    print("ok", saida, f"{total:.2f}s")


if __name__ == "__main__":
    compor(sys.argv[1])
