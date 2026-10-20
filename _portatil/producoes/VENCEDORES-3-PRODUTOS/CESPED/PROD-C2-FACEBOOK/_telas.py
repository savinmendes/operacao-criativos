# -*- coding: utf-8 -*-
"""Telas de Facebook por código (720x1280): post que expõe o pátio (gancho) e o antes/depois (virada)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from pathlib import Path
import subprocess

P = Path(__file__).parent
F = "C:/Windows/Fonts/"
def fnt(sz, bold=False): return ImageFont.truetype(F + ("segoeuib.ttf" if bold else "segoeui.ttf"), sz)
EMO = ImageFont.truetype(F + "seguiemj.ttf", 109)  # bitmap emoji: só 109
AZUL, CINZA, TXT, SUB = (24, 119, 242), (240, 242, 245), (5, 5, 5), (101, 103, 107)
W, H = 720, 1280


def is_emo(ch): return ord(ch) > 0x2500


def texto(d, im, xy, s, sz, cor=TXT, bold=False):
    x, y = xy; f = fnt(sz, bold)
    for ch in s:
        if is_emo(ch):
            if ord(ch) in (0xFE0F, 0x200D): continue
            e = Image.new("RGBA", (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(e).text((0, 0), ch, font=EMO, embedded_color=True)
            e = e.crop(e.getbbox() or (0, 0, 1, 1)).resize((int(sz * 1.1), int(sz * 1.1)), Image.LANCZOS)
            im.paste(e, (int(x), int(y + sz * 0.12)), e); x += sz * 1.2
        else:
            d.text((x, y), ch, font=f, fill=cor); x += d.textlength(ch, font=f)
    return x


def avatar(im, xy, r, cor, letra):
    a = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0)); da = ImageDraw.Draw(a)
    da.ellipse((0, 0, r * 2 - 1, r * 2 - 1), fill=cor)
    f = fnt(int(r * 1.0), True); tw = da.textlength(letra, font=f)
    da.text((r - tw / 2, r * 0.38), letra, font=f, fill="white"); im.paste(a, xy, a)


def topo(im, d, grupo):
    d.rectangle((0, 0, W, 60), fill="white")
    d.text((24, 14), "9:41", font=fnt(24, True), fill=TXT)
    d.rectangle((0, 60, W, 150), fill="white")
    d.text((24, 78), "←", font=fnt(40, True), fill=TXT)
    d.text((80, 72), grupo, font=fnt(30, True), fill=TXT)
    d.text((80, 112), "Grupo público · 3,2 mil miembros", font=fnt(20), fill=SUB)
    d.line((0, 150, W, 150), fill=(218, 221, 225), width=2)


def foto(path, box):
    x0, y0, x1, y1 = box
    return ImageOps.fit(Image.open(path).convert("RGB"), (x1 - x0, y1 - y0), Image.LANCZOS)


def tela_gancho(foto_patio, out):
    im = Image.new("RGB", (W, H), CINZA); d = ImageDraw.Draw(im)
    topo(im, d, "Villa Los Jardines - Maipú")
    d.rectangle((0, 166, W, 1150), fill="white")
    avatar(im, (24, 186), 30, (140, 140, 150), "?")
    d.text((96, 186), "Participante anónimo", font=fnt(25, True), fill=TXT)
    d.text((96, 220), "Hace 2 h", font=fnt(20), fill=SUB)
    texto(d, im, (24, 270), "El patio más feo de la villa 🤣🤣", 34)
    im.paste(foto(foto_patio, (0, 340, W, 880)), (0, 340))
    # reações
    texto(d, im, (24, 900), "😂", 30); d.text((70, 902), "47", font=fnt(26), fill=SUB)
    d.text((470, 902), "23 comentarios", font=fnt(24), fill=SUB)
    d.line((24, 950, W - 24, 950), fill=(218, 221, 225), width=2)
    for i, s in enumerate(["Me gusta", "Comentar", "Compartir"]):
        d.text((60 + i * 230, 966), s, font=fnt(24, True), fill=SUB)
    d.line((24, 1016, W - 24, 1016), fill=(218, 221, 225), width=2)
    im.save(out)


def tela_virada(antes, depois, out):
    im = Image.new("RGB", (W, H), CINZA); d = ImageDraw.Draw(im)
    topo(im, d, "Villa Los Jardines - Maipú")
    d.rectangle((0, 166, W, 1250), fill="white")
    avatar(im, (24, 186), 30, (60, 90, 160), "R")
    d.text((96, 186), "Rodrigo M.", font=fnt(25, True), fill=TXT)
    d.text((96, 220), "Ahora", font=fnt(20), fill=SUB)
    texto(d, im, (24, 266), "Antes y después 😎", 34)
    im.paste(foto(antes, (0, 330, 358, 820)), (0, 330)); im.paste(foto(depois, (362, 330, W, 820)), (362, 330))
    for x, s in ((14, "ANTES"), (376, "DESPUÉS")):
        f = fnt(26, True); tw = d.textlength(s, font=f)
        d.rounded_rectangle((x, 344, x + tw + 24, 386), 10, fill=(0, 0, 0)); d.text((x + 12, 346), s, font=f, fill="white")
    texto(d, im, (24, 836), "👍❤️", 28); d.text((100, 838), "128", font=fnt(26), fill=SUB)
    d.text((470, 838), "41 comentarios", font=fnt(24), fill=SUB)
    d.line((24, 884, W - 24, 884), fill=(218, 221, 225), width=2)
    y = 906
    for cor, ini, nome, txt in (((196, 120, 60), "C", "Carola V.", "¿Qué jardinero contrataste?"),
                                ((60, 150, 90), "J", "Jorge P.", "Pasa el dato 🔥")):
        avatar(im, (24, y + 6), 24, cor, ini)
        f = fnt(22); tw = max(d.textlength(txt, font=f) + 40, 200)
        d.rounded_rectangle((84, y, 84 + tw + 20, y + 84), 26, fill=CINZA)
        d.text((104, y + 8), nome, font=fnt(21, True), fill=TXT); texto(d, im, (104, y + 38), txt, 22)
        d.text((104, y + 92), "Me gusta   Responder", font=fnt(19, True), fill=SUB)
        y += 140
    im.save(out)


if __name__ == "__main__":
    B = P.parent / "BANCO" / "V1_720.mp4"
    for t, n in ((0.3, "antes"), (5.3, "depois")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(B), "-frames:v", "1", str(P / "cenas" / f"v1_{n}.png")], check=True)
    tela_gancho(P / "cenas" / "S1b_foto_patio.png", P / "cenas" / "T1_post_gancho.png")
    tela_virada(P / "cenas" / "v1_antes.png", P / "cenas" / "v1_depois.png", P / "cenas" / "T2_post_virada.png")
    print("ok")
