# Helpers de redesenho local de texto (PIL/OpenCV).
import os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(D, "fonts")
KITF = r"C:/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos/fonts"
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"


def font(name, size, wght=None):
    p = os.path.join(F, name)
    if not os.path.exists(p):
        p = os.path.join(KITF, name)
    f = ImageFont.truetype(p, size)
    if wght is not None:
        try:
            axes = f.get_variation_axes()
            vals = []
            for a in axes:
                nm = a.get("name", b"")
                nm = nm.decode() if isinstance(nm, bytes) else nm
                if "eight" in str(nm) or str(nm).lower().startswith("wght"):
                    vals.append(wght)
                elif "pt" in str(nm).lower() or "opsz" in str(nm).lower():
                    vals.append(min(max(size, a["minimum"]), a["maximum"]))
                else:
                    vals.append(a["default"])
            f.set_variation_by_axes(vals)
        except Exception as e:
            print("var fail", name, e)
    return f


def fill(im, box, color):
    ImageDraw.Draw(im).rectangle(box, fill=color)


def rrect(im, box, r, color):
    ImageDraw.Draw(im).rounded_rectangle(box, r, fill=color)


def interp_v(im, box):
    """Preenche a caixa interpolando, coluna a coluna, entre a linha acima e a linha abaixo (gradientes verticais)."""
    a = np.asarray(im).astype(float).copy()
    x0, y0, x1, y1 = box
    top = a[y0 - 2:y0, x0:x1].mean(0)
    bot = a[y1:y1 + 2, x0:x1].mean(0)
    t = np.linspace(0, 1, y1 - y0)[:, None, None]
    a[y0:y1, x0:x1] = top[None] * (1 - t) + bot[None] * t
    im.paste(Image.fromarray(a.astype(np.uint8)))


def interp_h(im, box):
    a = np.asarray(im).astype(float).copy()
    x0, y0, x1, y1 = box
    l = a[y0:y1, x0 - 2:x0].mean(1)
    r = a[y0:y1, x1:x1 + 2].mean(1)
    t = np.linspace(0, 1, x1 - x0)[None, :, None]
    a[y0:y1, x0:x1] = l[:, None] * (1 - t) + r[:, None] * t
    im.paste(Image.fromarray(a.astype(np.uint8)))


def inpaint(im, box=None, mask=None, r=7):
    a = np.asarray(im)
    m = np.zeros(a.shape[:2], np.uint8) if mask is None else mask
    if box is not None:
        x0, y0, x1, y1 = box
        m[y0:y1, x0:x1] = 255
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, r, cv2.INPAINT_TELEA)
    im.paste(Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)))


def textmask(im, box, dark=True, thr=None):
    """Mascara dos pixels de texto dentro da caixa (texto escuro sobre claro ou o contrario)."""
    a = np.asarray(im.convert("L")).astype(int)
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1]
    if thr is None:
        thr = (sub.max() + sub.min()) / 2
    m = np.zeros(a.shape, np.uint8)
    m[y0:y1, x0:x1] = ((sub < thr) if dark else (sub > thr)).astype(np.uint8) * 255
    return cv2.dilate(m, np.ones((5, 5), np.uint8))


def size(t, f, tracking=0):
    b = f.getbbox(t)
    return b[2] - b[0] + tracking * max(len(t) - 1, 0), b[3] - b[1]


def fit(t, name, size0, maxw, wght=None, tracking=0):
    s = size0
    while s > 6:
        f = font(name, s, wght)
        if size(t, f, tracking)[0] <= maxw:
            return f
        s -= 1
    return font(name, s, wght)


def text(im, xy, t, f, color, anchor="la", tracking=0, stroke=0, stroke_fill=None):
    d = ImageDraw.Draw(im)
    if tracking == 0:
        d.text(xy, t, font=f, fill=color, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)
        return
    w, _ = size(t, f, tracking)
    x, y = xy
    if anchor[0] == "m":
        x -= w / 2
    elif anchor[0] == "r":
        x -= w
    a2 = "l" + anchor[1]
    for ch in t:
        d.text((x, y), ch, font=f, fill=color, anchor=a2)
        x += f.getlength(ch) + tracking


def emoji(im, xy, ch, px):
    """Desenha emoji colorido (Segoe UI Emoji) com altura ~px, canto sup. esq. em xy."""
    f = ImageFont.truetype(EMOJI, 109)
    tmp = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((10, 10), ch, font=f, embedded_color=True)
    bb = tmp.getbbox()
    tmp = tmp.crop(bb)
    s = px / tmp.size[1]
    tmp = tmp.resize((max(1, int(tmp.size[0] * s)), px), Image.LANCZOS)
    im.paste(tmp, xy, tmp)
    return tmp.size[0]


_LOGO = None


def logo(im, xy, height, color, anchor="l", text_font="Montserrat.ttf", wght=600):
    """Logo Lymphoria: icone de folha (do rotulo n59) + 'LYMPHORIA'. xy = (x, y_centro)."""
    global _LOGO
    if _LOGO is None:
        _LOGO = Image.open(os.path.join(D, "ref", "logo_mask.png")).convert("L")
    m = _LOGO
    # icone = primeira coluna de componentes (ate o primeiro vao vertical apos x>20)
    a = np.asarray(m) > 60
    cols = a.any(0)
    xs = np.where(cols)[0]
    gap = None
    for i in range(xs[0] + 20, len(cols)):
        if not cols[i]:
            gap = i
            break
    icon = m.crop((0, 0, gap, m.size[1]))
    ib = icon.getbbox()
    icon = icon.crop(ib)
    ih = int(height * 1.15)
    icon = icon.resize((max(1, int(icon.size[0] * ih / icon.size[1])), ih), Image.LANCZOS)
    f = font(text_font, int(height * 1.38), wght)
    t = "LYMPHORIA"
    tw, th = size(t, f)
    gapx = int(height * 0.3)
    W = icon.size[0] + gapx + tw
    x, yc = xy
    if anchor == "m":
        x -= W / 2
    elif anchor == "r":
        x -= W
    x = int(x)
    col = Image.new("RGB", icon.size, color)
    im.paste(col, (x, int(yc - ih / 2)), icon)
    text(im, (x + icon.size[0] + gapx, yc), t, f, color, anchor="lm")
    return W


def smooth_fill(im, mask, scale=4, blur=3, noise=0):
    """Preenche a mascara com fundo suave (inpaint em escala reduzida + blur), bom p/ gradientes e areas grandes."""
    a = np.asarray(im).copy()
    H, W = mask.shape
    sm = cv2.resize(a, (W // scale, H // scale), interpolation=cv2.INTER_AREA)
    mm = cv2.resize(mask, (W // scale, H // scale), interpolation=cv2.INTER_NEAREST)
    mm = cv2.dilate(mm, np.ones((3, 3), np.uint8))
    sm = cv2.inpaint(sm, mm, 9, cv2.INPAINT_TELEA)
    up = cv2.resize(sm, (W, H), interpolation=cv2.INTER_CUBIC)
    if blur:
        up = cv2.GaussianBlur(up, (0, 0), blur)
    if noise:
        rng = np.random.default_rng(3)
        up = np.clip(up.astype(float) + rng.normal(0, noise, up.shape[:2])[..., None], 0, 255).astype(np.uint8)
    m = (mask > 0)[..., None]
    a = np.where(m, up, a)
    im.paste(Image.fromarray(a))


def boxmask(shape, boxes):
    m = np.zeros(shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes:
        m[y0:y1, x0:x1] = 255
    return m


def colmask(im, box, fn, dil=3):
    """Mascara dos pixels dentro da caixa onde fn(R,G,B) e verdadeiro."""
    a = np.asarray(im).astype(int)
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1]
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = fn(sub[..., 0], sub[..., 1], sub[..., 2]).astype(np.uint8) * 255
    if dil:
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dil + 1, 2 * dil + 1)))
    return m


def sample(im, xy):
    return tuple(int(v) for v in np.asarray(im)[xy[1], xy[0]][:3])


def rot_text(im, center, t, f, color, angle):
    """Texto girado (graus, anti-horario) centrado em center."""
    w, h = size(t, f)
    pad = 20
    lay = Image.new("RGBA", (w + 2 * pad, int(h * 1.6) + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((lay.size[0] / 2, lay.size[1] / 2), t, font=f, fill=color, anchor="mm")
    lay = lay.rotate(angle, resample=Image.BICUBIC, expand=True)
    im.paste(lay, (int(center[0] - lay.size[0] / 2), int(center[1] - lay.size[1] / 2)), lay)


def italic_text(im, xy, t, f, color, shear=0.18, anchor="ls"):
    w, h = size(t, f)
    pad = 40
    W, Hh = int(w + 2 * pad + h * shear), int(f.size * 1.5) + 2 * pad
    lay = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    base = pad + f.size
    ImageDraw.Draw(lay).text((pad, base), t, font=f, fill=color, anchor="ls")
    lay = lay.transform(lay.size, Image.AFFINE, (1, shear, -shear * base, 0, 1, 0), resample=Image.BICUBIC)
    x, y = xy
    if anchor[0] == "m":
        x -= w / 2
    im.paste(lay, (int(x - pad), int(y - base)), lay)


def poly_fill(im, mask, fitbox, bgtest, deg=3, noise=0):
    """Preenche a mascara com um polinomio 2D ajustado aos pixels de fundo (bgtest) dentro de fitbox."""
    a = np.asarray(im).astype(float).copy()
    x0, y0, x1, y1 = fitbox
    sub = a[y0:y1, x0:x1]
    ok = bgtest(sub[..., 0], sub[..., 1], sub[..., 2]) & (mask[y0:y1, x0:x1] == 0)
    yy, xx = np.nonzero(ok)
    step = max(1, len(yy) // 40000)
    yy, xx = yy[::step], xx[::step]
    def feats(x, y):
        x = x / (x1 - x0); y = y / (y1 - y0)
        return np.stack([x ** i * y ** j for i in range(deg + 1) for j in range(deg + 1 - i)], 1)
    A = feats(xx.astype(float), yy.astype(float))
    my, mx = np.nonzero(mask[y0:y1, x0:x1])
    B = feats(mx.astype(float), my.astype(float))
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, sub[yy, xx, c], rcond=None)
        v = B @ coef
        if noise:
            v = v + np.random.default_rng(c).normal(0, noise, v.shape)
        a[y0 + my, x0 + mx, c] = np.clip(v, 0, 255)
    im.paste(Image.fromarray(a.astype(np.uint8)))


def like(im, old, box, new, fname, color, wght=None, align="l", maxw=None, scale=1.0, dy=0, dx=0):
    """Escreve `new` no mesmo tamanho/linha de base que `old` ocupava em box (bbox da tinta, do OCR)."""
    x0, y0, x1, y1 = box
    s = 200
    f = font(fname, s, wght)
    b = f.getbbox(old, anchor="ls")
    s = max(6, int(s * (x1 - x0) / (b[2] - b[0]) * scale))
    f = font(fname, s, wght)
    b = f.getbbox(old, anchor="ls")
    base = y0 - b[1] + dy
    if maxw:
        while f.getbbox(new, anchor="ls")[2] - f.getbbox(new, anchor="ls")[0] > maxw and s > 6:
            s -= 1
            f = font(fname, s, wght)
    nb = f.getbbox(new, anchor="ls")
    if align == "l":
        x = x0 - nb[0]
    elif align == "m":
        x = (x0 + x1) / 2 - (nb[0] + nb[2]) / 2
    else:
        x = x1 - nb[2]
    ImageDraw.Draw(im).text((x + dx, base), new, font=f, fill=color, anchor="ls")
    return f, (x + dx + nb[0], base + nb[1], x + dx + nb[2], base + nb[3])


def maskfill(im, mask, color):
    a = np.asarray(im).copy()
    a[mask > 0] = color
    im.paste(Image.fromarray(a))
