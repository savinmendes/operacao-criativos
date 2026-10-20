"""Monta localmente o bloco 3 (qué incluye + garantía) e o rótulo extra do bloco 1 da Yara."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts"
BOLD = F + r"\Poppins-Bold.ttf"
SEMI = F + r"\Poppins-SemiBold.ttf"
MED = F + r"\Poppins-Medium.ttf"
W, H = 1536, 2752
BASE = r"C:\Users\PICHAU\Downloads\KITS-PERFUMES"


def font(p, s):
    return ImageFont.truetype(p, s)


def centered(d, y, txt, f, fill):
    w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill)


def check(d, x, y, s, col):
    d.line([(x, y + s * 0.55), (x + s * 0.38, y + s * 0.9), (x + s, y + s * 0.1)], fill=col, width=max(6, s // 7), joint="curve")


def bloco3(pid, nome, hero, crop, bg_top, bg_bot, accent, dark):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        c = tuple(int(bg_top[i] * (1 - t) + bg_bot[i] * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    # rótulo superior
    f = font(SEMI, 46)
    lab = "Q U É   I N C L U Y E   T U   P E D I D O"
    centered(d, 90, lab, f, accent)
    lw = d.textlength(lab, font=f)
    d.line([((W - lw) / 2, 160), ((W + lw) / 2, 160)], fill=accent, width=3)

    # card de itens
    cx0, cy0, cx1, cy1 = 140, 220, W - 140, 760
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rounded_rectangle((cx0, cy0 + 14, cx1, cy1 + 14), 48, fill=70)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    im.paste((0, 0, 0), (0, 0), sh)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((cx0, cy0, cx1, cy1), 48, fill=(255, 255, 255))
    itens = [f"1 perfume Lattafa {nome}", "Eau de Parfum (EDP)", "Frasco de 100 ml", "Originales Lattafa"]
    fi = font(MED, 62)
    for i, t in enumerate(itens):
        y = cy0 + 70 + i * 115
        check(d, cx0 + 80, y + 14, 50, accent)
        d.text((cx0 + 170, y), t, font=fi, fill=dark)

    # manchete
    fh = font(BOLD, 112)
    centered(d, 840, "EL TOQUE FINAL", fh, dark)
    centered(d, 970, "DE TU ESTILO.", fh, accent)

    # foto do frasco (recorte do hero)
    ph = Image.open(hero).convert("RGB").crop(crop)
    pw = W - 280
    ph = ph.resize((pw, int(ph.height * pw / ph.width)))
    ph_h = min(ph.height, 1160)
    ph = ph.crop((0, 0, pw, ph_h))
    m = Image.new("L", ph.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, ph.width, ph.height), 56, fill=255)
    py = 1150
    im.paste(ph, (140, py), m)
    d = ImageDraw.Draw(im)

    # selos
    sy = py + ph_h + 70
    fs = font(SEMI, 54)
    selos = ["Pagas al recibir en tu casa", "Garantía de 90 días"]
    for i, t in enumerate(selos):
        y = sy + i * 150
        d.rounded_rectangle((140, y, W - 140, y + 120), 60, fill=dark)
        tw = d.textlength(t, font=fs)
        x = (W - tw) / 2 + 40
        check(d, x - 90, y + 36, 46, (255, 255, 255))
        d.text((x, y + 26), t, font=fs, fill=(255, 255, 255))
    out = rf"{BASE}\{pid}\06_descricao_bloco3_que-incluye.jpg"
    im.save(out, quality=92)
    print(out, sy + 2 * 150)


def rotulo_yara():
    p = rf"{BASE}\uni-yara\04_descricao_bloco1_notas.png"
    im = Image.open(p).convert("RGB")
    t = "+ Vainilla y almizcle"
    f = font(SEMI, 64)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    w = ds.textlength(t, font=f)
    x, y = (W - w) / 2, 2395
    ds.text((x + 3, y + 4), t, font=f, fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(4))
    im = Image.alpha_composite(im.convert("RGBA"), sh)
    ImageDraw.Draw(im).text((x, y), t, font=f, fill=(255, 255, 255, 255))
    im.convert("RGB").save(p)


if __name__ == "__main__":
    import sys
    if "rotulo" in sys.argv:
        rotulo_yara()
    bloco3("uni-yara", "Yara", rf"{BASE}\uni-yara\01_galeria_hero-yara.png", (330, 500, 1718, 1760),
           (248, 228, 230), (255, 248, 248), (176, 104, 122), (58, 34, 40))
    bloco3("uni-yara-moi", "Yara Moi", rf"{BASE}\uni-yara-moi\01_galeria_hero-yara-moi.png", (330, 500, 1718, 1760),
           (247, 240, 230), (255, 252, 246), (160, 122, 58), (52, 40, 30))
