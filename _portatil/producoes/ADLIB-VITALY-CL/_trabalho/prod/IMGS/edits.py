# Redesenho local dos textos (marca, oferta, suavizacoes) sobre comp/NN.png -> final/NN.png
import os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("final", exist_ok=True)
DKGREEN = (24, 66, 52)


def load(n):
    return Image.open("comp/%s.png" % n).convert("RGB")


# ---------------------------------------------------------------- 02
def e02():
    im = load("02")
    W, H = im.size
    # logo topo
    m = colmask(im, (630, 110, 850, 185), lambda r, g, b: (r + g + b) < 300, 4)
    smooth_fill(im, m, scale=2, blur=2)
    logo(im, (737, 147), 36, (20, 22, 22), anchor="m")
    # caixa vermelha HOY: casco convexo dos pixels vermelhos
    a = np.asarray(im).astype(int)
    red = colmask(im, (480, 250, 1000, 490), lambda r, g, b: (r > 170) & (g < 140) & (b < 120), 0)
    pts = cv2.findNonZero(red)
    hull = cv2.convexHull(pts)
    rect = cv2.minAreaRect(pts)
    hm = np.zeros(red.shape, np.uint8)
    cv2.fillConvexPoly(hm, hull, 255)
    hm = cv2.dilate(hm, np.ones((19, 19), np.uint8))
    hm[255:485, 490:530] = 255
    # "2x1" verde escuro (sem pegar frasco preto/ambar)
    g2 = colmask(im, (440, 440, 1010, 775), lambda r, g, b: (g - r > 10) & (b >= r) & (r + g + b < 520), 5)
    cap = colmask(im, (430, 440, 520, 775), lambda r, g, b: (np.abs(g - r) < 9) & (r + g + b < 330) | (r > g + 8), 1)
    g2 = cv2.bitwise_and(g2, cv2.bitwise_not(cap))
    poly_fill(im, cv2.bitwise_or(hm, g2), (430, 240, 1080, 800),
              lambda r, g, b: (r + g + b > 600) & (g >= r), deg=3, noise=1.2)
    # nova caixa vermelha (mesmo quadrilatero e gradiente)
    box = cv2.boxPoints(rect).astype(np.int32)
    lay = Image.new("RGB", (W, H))
    xs = np.linspace(0, 1, W)[None, :, None]
    c1, c2 = np.array([255, 105, 80]), np.array([255, 40, 5])
    grad = (c1 * (1 - xs) + c2 * xs) * np.ones((H, 1, 1))
    lay = Image.fromarray(grad.astype(np.uint8))
    big = Image.new("L", (W * 4, H * 4), 0)
    ImageDraw.Draw(big).polygon([(p[0] * 4, p[1] * 4) for p in box.tolist()], fill=255)
    im.paste(lay, (0, 0), big.resize((W, H), Image.LANCZOS))
    (cx, cy), (bw, bh), ang = rect
    if bw < bh:
        bw, bh = bh, bw
        ang = ang - 90
    f = fit("COMPRE 1", "Poppins-Black.ttf", 140, int(bw * 0.86))
    rot_text(im, (cx, cy + 4), "COMPRE 1", f, (255, 255, 255), -ang if abs(ang) < 45 else 0)
    # RECIBA 2 no lugar do 2x1
    f = fit("RECIBA 2", "Poppins-Black.ttf", 220, 540)
    text(im, (757, 625), "RECIBA 2", f, (27, 66, 56), anchor="mm")
    # pilula "en GOTAS VITALY"
    pill = sample(im, (560, 830))
    fill(im, (470, 845, 1005, 930), pill)
    f = fit("en GOTAS LYMPHORIA", "Poppins-Bold.ttf", 66, 560)
    text(im, (738, 888), "en GOTAS LYMPHORIA", f, (255, 255, 255), anchor="mm")
    im.save("final/02.png")


# ---------------------------------------------------------------- 04
def e04():
    im = load("04")
    bg = sample(im, (60, 1110))
    blk = (17, 17, 17)
    fB = font("Inter.ttf", 66, 700)
    fR = font("Inter.ttf", 66, 400)
    # DESAPARECEN -> DISMINUYEN
    fill(im, (160, 725, 650, 792), bg)
    text(im, (166, 782), "DISMINUYEN", fB, blk, anchor="ls")
    # Por eso Gotas Vitaly tiene su / PROMOCION de MARZO.
    fill(im, (100, 1120, 1040, 1280), bg)
    x = 108
    t1 = "Por eso Gotas Lymphoria "
    text(im, (x, 1190), t1, fR, blk, anchor="ls")
    w = fR.getlength(t1)
    emoji(im, (int(x + w), 1132), "\U0001F49A", 62)
    text(im, (x, 1268), "tiene su PROMOCIÓN.", fR, blk, anchor="ls")
    # COMPRA 1, RECIBE 2 -> COMPRE 1, RECIBA 2 (faixa amarela)
    yel = sample(im, (100, 1500))
    fill(im, (92, 1494, 920, 1592), yel)
    f = fit("COMPRE 1, RECIBA 2", "Inter.ttf", 92, 800, 800)
    text(im, (110, 1575), "COMPRE 1, RECIBA 2", f, blk, anchor="ls")
    im.save("final/04.png")


# ---------------------------------------------------------------- 06
def e06():
    im = load("06")
    m = colmask(im, (865, 1153, 1325, 1228), lambda r, g, b: (r + g + b) < 400, 3)
    a = np.asarray(im).copy(); a[m > 0] = (255, 255, 255); im.paste(Image.fromarray(a))
    f = fit("Gotas LYMPHORIA®", "Inter.ttf", 78, 440, 560)
    text(im, (873, 1212), "Gotas LYMPHORIA®", f, (10, 10, 10), anchor="ls")
    im.save("final/06.png")


# ---------------------------------------------------------------- 07
def e07():
    im = load("07")
    # limpa sombras do rotulo antigo que o NB2 deixou no creme do frasco menor
    a = np.asarray(im).copy()
    x0, y0, x1, y1 = 975, 1440, 1300, 1610
    sub = a[y0:y1, x0:x1]
    med = cv2.medianBlur(cv2.GaussianBlur(sub, (0, 0), 3), 21)
    hsv = cv2.cvtColor(sub, cv2.COLOR_RGB2HSV)
    cream = ((hsv[..., 0] > 10) & (hsv[..., 0] < 35) & (hsv[..., 1] < 110) & (hsv[..., 2] > 170)).astype(np.float32)
    cream = cv2.GaussianBlur(cv2.erode(cream, np.ones((9, 9), np.uint8)), (0, 0), 3)[..., None]
    a[y0:y1, x0:x1] = (med * cream + sub * (1 - cream)).astype(np.uint8)
    im = Image.fromarray(a)
    m = colmask(im, (620, 55, 880, 130), lambda r, g, b: (r + g + b) > 450, 4)
    smooth_fill(im, m, scale=2, blur=2, noise=6)
    logo(im, (751, 94), 37, (255, 255, 255), anchor="m")
    im.save("final/07.png")


# ---------------------------------------------------------------- 08 / 18 bloco de oferta
def oferta(im, box):
    """lines: dict com y das linhas (baseline) e x esquerdo, larguras alvo."""
    x0, y0, x1, y1 = box
    m = colmask(im, box, lambda r, g, b: ((r + g + b) < 420) | ((r > 150) & (g < 90)), 4)
    smooth_fill(im, m, scale=4, blur=3)


def e08():
    im = load("08")
    # logo cybervitaly
    m = boxmask(np.asarray(im).shape, [(350, 100, 790, 215)])
    smooth_fill(im, m, scale=4, blur=3)
    logo(im, (576, 166), 44, (37, 104, 74), anchor="m")
    # bloco de oferta
    oferta(im, (80, 1255, 650, 1820))
    _bloco(im, x=104, w_cyber=486, y_cy=1359, y_l2=1541, w_l2=508, y_p1=1741, w_p1=521, y_se=1805, w_se=490,
           green=(52, 120, 84))
    im.save("final/08.png")


def _bloco(im, x, w_cyber, y_cy, y_l2, w_l2, y_p1, w_p1, y_se, w_se, green):
    blk = (12, 12, 12)
    red = (198, 40, 40)
    # ENVIO GRATIS (no lugar de SOLO POR CYBER)
    h_cy = 0.85
    f = fit("ENVÍO GRATIS", "Anton-Regular.ttf", 160, w_cyber)
    w1 = f.getlength("ENVÍO ")
    text(im, (x, y_cy), "ENVÍO ", f, blk, anchor="ls")
    text(im, (x + w1, y_cy), "GRATIS", f, red, anchor="ls")
    # COMPRE 1 (italico preto)
    f = fit("COMPRE 1", "Anton-Regular.ttf", 300, int(w_l2 * 0.95))
    italic_text(im, (x, y_l2), "COMPRE 1", f, blk, shear=0.2)
    # RECIBA 2 (verde)
    f = fit("RECIBA 2", "Anton-Regular.ttf", 320, w_p1)
    text(im, (x - 4, y_p1), "RECIBA 2", f, green, anchor="ls")
    # SOLO ESTA SEMANA (mantido)
    f = fit("¡SÓLO ESTA SEMANA!", "Anton-Regular.ttf", 140, w_se)
    text(im, (x, y_se), "¡SÓLO ESTA SEMANA!", f, blk, anchor="ls")


# ---------------------------------------------------------------- 13 (so rotulo)
def e13():
    load("13").save("final/13.png")


# ---------------------------------------------------------------- 15
def e15():
    im = load("15")
    brown = sample(im, (172, 512))
    ycol = sample_text(im, (194, 524, 656, 578), lambda r, g, b: (r > 180) & (g > 130) & (b < 140))
    m = colmask(im, (185, 515, 668, 578), lambda r, g, b: (r > 150) & (g > 110) & (b < 150) & (r - b > 60), 3)
    maskfill(im, m, brown)
    like(im, "¿Tengo hipotiroidismo,", (194, 524, 656, 581), "¿Tomo otras vitaminas,", "RobotoCondensed.ttf", ycol, wght=500)
    im.save("final/15.png")


def sample_text(im, box, fn):
    a = np.asarray(im).astype(int)
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    k = fn(sub[:, 0], sub[:, 1], sub[:, 2])
    return tuple(int(v) for v in np.median(sub[k], 0)) if k.any() else (0, 0, 0)


# ---------------------------------------------------------------- 16
def e16():
    im = load("16")
    g = sample(im, (630, 1064))
    m = colmask(im, (640, 1028, 1000, 1100), lambda r, g_, b: (r + g_ + b) > 560, 3)
    maskfill(im, m, g)
    logo(im, (811, 1064), 38, (255, 255, 255), anchor="m")
    im.save("final/16.png")


# ---------------------------------------------------------------- 18
def e18():
    im = load("18")
    interp_v(im, (560, 80, 1050, 205))
    logo(im, (819, 150), 46, (37, 104, 74), anchor="m")
    m = colmask(im, (425, 362, 1195, 500), lambda r, g, b: (r < 110) & (g < 110) & (b < 110) & (np.abs(g - r) < 22), 3)
    smooth_fill(im, m, scale=2, blur=2)
    like(im, "Prueba Vitaly®", (435, 368, 1186, 495), "Prueba Lymphoria®", "Poppins-SemiBold.ttf", (12, 12, 12), align="m", maxw=1450, scale=0.9, dy=10)
    green = sample_text(im, (121, 1487, 824, 1783), lambda r, g, b: (g - r > 40))
    oferta(im, (110, 1160, 870, 1890))
    _bloco(im, x=150, w_cyber=637, y_cy=1283, y_l2=1532, w_l2=695, y_p1=1780, w_p1=703, y_se=1872, w_se=649, green=green)
    im.save("final/18.png")


# ---------------------------------------------------------------- 21
def e21():
    im = load("21")
    teal = sample_text(im, (169, 132, 927, 344), lambda r, g, b: (g - r > 60))
    m = colmask(im, (150, 125, 955, 438), lambda r, g, b: (g - r > 25) & (g > 70), 4)
    smooth_fill(im, m, scale=2, blur=2)
    f = fit("QUE PAGAS", "ArchivoBlack-Regular.ttf", 260, 780)
    text(im, (552, 290), "QUE PAGAS", f, teal, anchor="ms")
    f = fit("AL RECIBIR", "ArchivoBlack-Regular.ttf", 260, 780)
    text(im, (552, 425), "AL RECIBIR", f, teal, anchor="ms")
    # selo
    wh = sample(im, (720, 660))
    gray = sample_text(im, (709, 698, 910, 731), lambda r, g, b: (r + g + b) < 250)
    m = colmask(im, (680, 690, 935, 865), lambda r, g, b: (r + g + b) < 600, 3)
    maskfill(im, m, wh)
    like(im, "COMPRA 2", (709, 698, 910, 731), "COMPRE 2,", "ArchivoBlack-Regular.ttf", gray, align="m", maxw=240)
    like(im, "LLEVA4", (681, 742, 934, 793), "RECIBA 4", "ArchivoBlack-Regular.ttf", teal, align="m", maxw=250)
    like(im, "GRATIS", (694, 806, 929, 856), "ENVÍO GRATIS", "ArchivoBlack-Regular.ttf", teal, align="m", maxw=235)
    # botao
    wb = sample(im, (150, 1225))
    fill(im, (185, 1198, 925, 1252), wb)
    f, bb = like(im, "APROVECHAR HASTA 61% OFF", (195, 1206, 862, 1243), "APROVECHAR LA OFERTA", "ArchivoBlack-Regular.ttf", (20, 20, 20), align="l", dx=60)
    fa = font("Inter.ttf", f.size, 800)
    text(im, (bb[2] + 14, bb[3]), "→", fa, (20, 20, 20), anchor="ls")
    im.save("final/21.png")


# ---------------------------------------------------------------- 27
def e27():
    im = load("27")
    W, H = im.size
    a = np.asarray(im).astype(float)
    dk = colmask(im, (715, 1220, 1060, 1620), lambda r, g_, b: ((r + g_ + b) < 260) & (g_ >= r), 0)
    dk = cv2.morphologyEx(dk, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
    nlab, lab, st, cen_ = cv2.connectedComponentsWithStats(dk)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    cx, cy = cen_[k]
    x_, y_, w_, h_ = st[k, :4]
    cx, cy = x_ + w_ / 2, y_ + h_ / 2
    R = max(w_, h_) / 2 + 2
    Rx, Ry = w_ / 2 + 1.5, h_ / 2 + 1.5
    print("circ", cx, cy, R)
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.sqrt(((xx - cx) / Rx) ** 2 + ((yy - cy) / Ry) ** 2)
    sub = a[(rr < 0.97) & (a.sum(2) < 260)]
    ring = a[(rr > 0.80) & (rr < 0.93) & (a.sum(2) < 260)]
    cen = a[(rr < 0.45) & (a.sum(2) < 240)]
    c_in, c_out = np.median(cen, 0), np.median(ring, 0)
    t = np.clip(rr, 0, 1)[..., None] ** 2
    grad = c_in * (1 - t) + c_out * t
    rng = np.random.default_rng(5)
    grad = grad + rng.normal(0, 1.5, grad.shape[:2])[..., None]
    big = Image.new("L", (W * 2, H * 2), 0)
    ImageDraw.Draw(big).ellipse(((cx - Rx) * 2, (cy - Ry) * 2, (cx + Rx) * 2, (cy + Ry) * 2), fill=255)
    im.paste(Image.fromarray(np.clip(grad, 0, 255).astype(np.uint8)), (0, 0), big.resize((W, H), Image.LANCZOS))
    cream = (246, 240, 222)
    like(im, "LLEVA 2,", (767, 1313, 982, 1373), "COMPRE 1,", "Montserrat.ttf", cream, wght=700, align="m", maxw=235, dx=int(cx - 874))
    like(im, "PAGA1", (769, 1374, 983, 1438), "RECIBA 2", "Montserrat.ttf", cream, wght=700, align="m", maxw=235, dx=int(cx - 876))
    like(im, "SÓLO ESTA", (778, 1441, 968, 1488), "SÓLO ESTA", "Montserrat.ttf", cream, wght=500, align="m")
    like(im, "SEMANA", (800, 1487, 947, 1525), "SEMANA", "Montserrat.ttf", cream, wght=500, align="m")
    im.save("final/27.png")


# ---------------------------------------------------------------- 28
def e28():
    im = load("28")
    bg = sample(im, (60, 300))
    dg = sample_text(im, (128, 420, 1445, 489), lambda r, g, b: (r + g + b) < 250)
    fill(im, (110, 110, 480, 215), bg)
    logo(im, (122, 166), 52, dg, anchor="l")
    m = colmask(im, (110, 678, 1400, 760), lambda r, g, b: (r + g + b) < 640, 3)
    maskfill(im, m, bg)
    like(im, "incluso Ozempic durante 8 meses.", (121, 679, 1361, 755), "incluso ayunos durante 8 meses.", "Poppins-Medium.ttf", dg)
    m = colmask(im, (110, 849, 1420, 932), lambda r, g, b: (r + g + b) < 640, 3)
    maskfill(im, m, bg)
    like(im, "Vitaly, mis jeans cierran sin luchar", (125, 850, 1352, 930), "Lymphoria, mis jeans cierran sin luchar", "Poppins-Medium.ttf", dg, maxw=1340)
    band = sample(im, (600, 1815))
    a = np.asarray(im).copy()
    row = a[1800, :1258].copy()
    row[:175] = a[1800, 175]
    a[1798:1916, :1258] = row[None]
    im.paste(Image.fromarray(a))
    like(im, "• GOTAS LÍQUIDAS • 4 HIERBAS • LIBRE DE GMO •", (180, 1834, 1235, 1885),
         "• GOTAS LÍQUIDAS • 4 HIERBAS • SIN ALCOHOL •", "Poppins-Regular.ttf", dg, dx=0)
    leaf(im, (108, 1857), 80, dg)
    im.save("final/28.png")


def leaf(im, center, h, color):
    import tx
    tx.logo(Image.new("RGB", (10, 10)), (0, 5), 5, color)  # carrega mascara
    m = tx._LOGO
    a = np.asarray(m) > 60
    cols = a.any(0)
    xs = np.where(cols)[0]
    gap = next(i for i in range(xs[0] + 20, len(cols)) if not cols[i])
    icon = m.crop((0, 0, gap, m.size[1]))
    icon = icon.crop(icon.getbbox())
    icon = icon.resize((int(icon.size[0] * h / icon.size[1]), h), Image.LANCZOS)
    im.paste(Image.new("RGB", icon.size, color), (int(center[0] - icon.size[0] / 2), int(center[1] - h / 2)), icon)


if __name__ == "__main__":
    for n in sys.argv[1:]:
        globals()["e" + n]()
        print(n, "ok")
