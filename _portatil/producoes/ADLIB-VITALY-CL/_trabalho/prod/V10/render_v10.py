# -*- coding: utf-8 -*-
"""V10: imagem inteira (77,07 s) com trocas Vitaly -> Lymphoria, oferta nova e textos suavizados.
  python render_v10.py [--prev k1,k2]  -> corpo_video.mp4 (sem áudio)"""
import sys, subprocess
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, str(Path(__file__).parent.parent / "comum"))
import texto as T
import patch_rotulo as PR

D = Path(__file__).parent
PROD = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod")
LYM = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho\ad04")
W, H, FPS = 720, 1280, 30
PREV = [int(x) for x in sys.argv[sys.argv.index("--prev") + 1].split(",")] if "--prev" in sys.argv else None

orig = T.ler_quadros(str(D / "orig.mp4"))
NQ = len(orig)
v2 = T.ler_quadros(str(PROD / "V2_frasco_cocina.mp4"))                                # 66 q
v3 = T.ler_quadros(str(PROD / "V3_frasco_mesa.mp4"), vf="setpts=PTS*101/80,fps=30")    # ~101 q
p1 = T.ler_quadros(str(PROD / "P1_kit3.mp4"))                                         # 90 q
p2 = T.ler_quadros(str(PROD / "P2_frasco_miel.mp4"))                                  # 90 q
FL = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
VF = "scale=720:1280:flags=lanczos,fps=30"
tk_card = [T.ler_quadros(str(FL / t), vf=VF, ss=0.2, t=3.0)[:89] for t in
           ("ad10/flora/t1_edit.mp4", "ad11/flora/t3_edit.mp4", "ad11/flora/t4_edit.mp4")]  # 3 x 89 q, sem texto
print("quadros", NQ, len(v2), len(v3), len(p1), len(p2))


def take(arr, i):
    return arr[max(0, min(i, len(arr) - 1))].copy()


def q(t):
    return int(round(t * FPS))


# ---------- camadas fixas ----------
def camada_checklist():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle((18, 39, 702, 143), fill=(0, 0, 0, 105))
    linhas = [([("💧 ", 1), ("20 gotas — mañana (con desayuno)", 1)], 41),
              ([("💧 ", 1), ("20 gotas — noche (con cena)", 1)], 75),
              ([("💡 ", 1), ("Junto a una comida = mejor absorción", 1)], 107)]
    for segs, y in linhas:
        T.desenhar_linha(im, segs, 360, y - 4, 29, cor=(255, 255, 255, 255), emoji_cor=True)
    return im


CHECK = camada_checklist()


def camada_cartao():
    """cartão da oferta Lymphoria (substitui o card do guia em PDF de brinde)"""
    bg = Image.open(LYM / "kit3_quadrado.jpg").convert("RGB")
    f = bg.resize((H, H)).crop(((H - W) // 2, 0, (H - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(30))
    f = Image.blend(f, Image.new("RGB", f.size, (10, 25, 15)), 0.55).convert("RGBA")
    d = ImageDraw.Draw(f)
    T.desenhar_linha(f, [("PROMOCIÓN ", 1), ("LYMPHORIA", 1)], 360, 70, 46, cor=(255, 255, 255, 255))
    kit = bg.resize((560, 560), Image.LANCZOS)
    m = Image.new("L", (560, 560), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 559, 559), radius=28, fill=255)
    f.paste(kit, (80, 150), m)
    return f


CARD = camada_cartao()
OFERTAS = [("Compre 1, Reciba 2", "$34.990"), ("Compre 2, Reciba 4", "$59.990"), ("Compre 3, Reciba 6", "$79.990")]


def cartao(k, k0):
    im = CARD.copy()
    for i, (a, b) in enumerate(OFERTAS):
        ki = k0 + 6 + i * 5
        if k < ki:
            continue
        u = min(1.0, (k - ki) / 5)
        y = 745 + i * 102 + (1 - u) * 30
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        dd.rounded_rectangle((60, y, 660, y + 86), radius=22, fill=(255, 255, 255, int(250 * u)))
        T.desenhar_linha(lay, [(a, 1)], 360, y + 17, 40, cor=(30, 30, 30, int(255 * u)))  # sem preço (pedido do dono)
        im = Image.alpha_composite(im, lay)
    ki = k0 + 24
    if k >= ki:
        u = min(1.0, (k - ki) / 5)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        dd.rounded_rectangle((40, 1062, 680, 1150), radius=44, fill=(28, 120, 66, int(252 * u)))
        T.desenhar_linha(lay, [("ENVÍO GRATIS · PAGAS AL RECIBIR", 1)], 360, 1086, 33, cor=(255, 255, 255, int(255 * u)))
        im = Image.alpha_composite(im, lay)
    return im


# selo de garantia: "45" -> "90" (remendo feito no quadro de referência e somado como diferença)
KREF = q(68.0)
ref = orig[KREF].copy()
SX0, SY0, SX1, SY1 = 172, 482, 314, 598
reg = ref[SY0:SY1, SX0:SX1]
mask = ((reg.min(2) > 150) & (reg.astype(int)[..., 1] > reg.astype(int)[..., 2] + 10) |
        (reg.min(2) > 185)).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((11, 11), np.uint8))
fill = cv2.inpaint(cv2.cvtColor(reg, cv2.COLOR_RGB2BGR), mask, 7, cv2.INPAINT_TELEA)
fill = cv2.cvtColor(fill, cv2.COLOR_BGR2RGB)
pim = Image.fromarray(fill).convert("RGBA")
cor_txt = tuple(int(c) for c in np.median(reg[mask > 0].reshape(-1, 3), axis=0))
y0_, y1_, _, _ = T.tinta_bbox([("90", 1)], 104)
sh = Image.new("RGBA", pim.size, (0, 0, 0, 0))
T.desenhar_linha(sh, [("90", 1)], (SX1 - SX0) / 2 + 2, 51 - (y0_ + y1_) / 2 + 3, 104, cor=(0, 0, 0, 150))
sh = sh.filter(ImageFilter.GaussianBlur(2.5))
pim = Image.alpha_composite(pim, sh)
T.desenhar_linha(pim, [("90", 1)], (SX1 - SX0) / 2, 51 - (y0_ + y1_) / 2, 104, cor=(246, 240, 214, 255))
SELO_DELTA = np.asarray(pim.convert("RGB")).astype(np.float32) - reg.astype(np.float32)
_antes = orig[1974].astype(np.float32)   # último quadro sem selo
_m = (np.abs(ref.astype(np.float32) - _antes).mean(2) > 28).astype(np.uint8) * 255
_m = cv2.morphologyEx(_m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
_n, _lab, _st, _ = cv2.connectedComponentsWithStats(_m)
_big = 1 + int(np.argmax(_st[1:, cv2.CC_STAT_AREA]))
_m = ((_lab == _big) * 255).astype(np.uint8)
_m = cv2.GaussianBlur(cv2.dilate(_m, np.ones((5, 5), np.uint8)), (0, 0), 1.5)
SELO_MASK = (_m.astype(np.float32) / 255.0)[..., None]


def faixa_cinza(im, box, y_a, y_b):
    """apaga uma linha dentro de caixa cinza semitransparente: cada linha recebe a interpolação
    entre a cor da borda esquerda e a da direita da própria caixa (sem texto ali)."""
    a = np.asarray(im).astype(np.float32).copy()
    x0, x1 = box
    for y in range(y_a, y_b):
        l = a[y, x0:x0 + 4, :3].mean(0)
        r = a[y, x1 - 4:x1, :3].mean(0)
        t = np.linspace(0, 1, x1 - x0)[:, None]
        a[y, x0:x1, :3] = l * (1 - t) + r * t
    return Image.fromarray(a.astype(np.uint8))


def fade_k(k, ka, kb, sobe=True):
    u = min(1.0, max(0.0, (k - ka) / max(1, kb - ka)))
    return u if sobe else 1 - u


K_DESP0, K_DESP1 = q(17.933), q(24.833)
K_TK0, K_TK1 = q(30.8), q(36.333)
K_IT2 = q(42.2)
K_BR0, K_BR1 = q(50.067), q(55.133)
K_CARD1 = q(63.833)
K_SELO0, K_SELO_POP, K_SELO1 = 1976, q(66.3), q(70.6)
K_ROD = q(70.967)

if not PREV:
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                           "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                           "-colorspace", "bt709", str(D / "corpo_video.mp4")], stdin=subprocess.PIPE)
for k in (PREV or range(NQ)):
    fr = orig[k]
    if k < 232:                                            # rótulo VITALY na mão -> LYMPHORIA (rastreado)
        im = Image.fromarray(PR.aplicar(fr, k))
    elif K_DESP0 <= k < K_DESP1:                           # "con Vitaly ✓" -> "con Lymphoria ✓"
        im = faixa_cinza(Image.fromarray(fr), (86, 630), 108, 170).convert("RGBA")
        T.desenhar_linha(im, [("con Lymphoria ✓", 1)], 358, 106, 50, cor=(255, 255, 255, 255))
    elif K_TK0 <= k < K_TK1:                               # copo + frasco Vitaly -> takes do frasco Lymphoria
        i = k - K_TK0
        a = take(v2, i) if i < 66 else take(v3, i - 66)
        fa = 1.0 - fade_k(k, q(35.467), K_TK1)
        im = Image.fromarray((a.astype(np.float32) * fa).astype(np.uint8)).convert("RGBA")
        ch = CHECK.copy()
        if fa < 1:
            al = np.asarray(ch).copy(); al[..., 3] = (al[..., 3] * fa).astype(np.uint8); ch = Image.fromarray(al)
        im = Image.alpha_composite(im, ch)
    elif q(42.0) <= k < K_BR0:                           # item "No interfiere con medicamentos" -> "Sabor a miel"
        im = Image.fromarray(fr).convert("RGBA")
        ImageDraw.Draw(im).rectangle((0, 400, 719, 600), fill=(0, 0, 0, 255))
        if k >= K_IT2:
            u = fade_k(k, K_IT2, q(42.9))
            if k >= q(49.5):                               # o original some em fade p/ preto
                u *= 1 - fade_k(k, q(49.5), q(50.033))
            v = int(255 * u)
            T.desenhar_linha(im, [("✓ Sabor a miel", 1)], 360, 412, 60, cor=(v, v, v, 255))
    elif K_BR0 <= k < K_BR1:                               # 2 frascos Vitaly -> kit e frasco Lymphoria
        i = k - K_BR0
        a = take(p1, i) if i < 90 else take(p2, i - 90)
        fa = fade_k(k, K_BR0, q(50.567))
        im = Image.fromarray((a.astype(np.float32) * fa).astype(np.uint8))
    elif K_BR1 <= k < K_CARD1 + 6:                         # card do guia (Vitaly) -> takes limpos do frasco Lymphoria (sem cartão)
        i = k - K_BR1
        im = Image.fromarray(take(tk_card[min(2, i // 89)], i % 89 if i < 267 else 88))
    elif K_SELO0 <= k < K_SELO_POP:                        # entrada animada do selo -> selo "90" já pronto
        a = _antes
        r = ref.astype(np.float32).copy()
        r[SY0:SY1, SX0:SX1] += SELO_DELTA
        im = Image.fromarray((a * (1 - SELO_MASK) + r * SELO_MASK).clip(0, 255).astype(np.uint8))
    elif K_SELO1 <= k < K_ROD:                             # saída animada do selo (mostrava "45"): congela o selo "90"
        a = ref.astype(np.float32).copy()
        a[SY0:SY1, SX0:SX1] += SELO_DELTA
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    elif K_SELO_POP <= k < K_SELO1:                        # "45 DÍAS" -> "90 DÍAS"
        a = fr.astype(np.float32).copy()
        a[SY0:SY1, SX0:SX1] += SELO_DELTA
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    elif k >= K_ROD:                                       # rodapé "vitaly-chile.com / Comprar ahora" -> CTA
        im = Image.fromarray(fr).convert("RGBA")
        ImageDraw.Draw(im).rounded_rectangle((44, 1070, 676, 1220), radius=6, fill=(62, 62, 62, 252))
        T.desenhar_linha(im, [("Toca el botón de abajo", 1)], 360, 1080, 44, cor=(255, 255, 255, 255))
        T.desenhar_linha(im, [("Comprar ahora 👇", 1)], 360, 1146, 38, cor=(255, 255, 255, 255))
    else:
        im = Image.fromarray(fr)
    if PREV:
        im.convert("RGB").save(D / "fr" / f"prev_{k}.png")
        continue
    ff.stdin.write(np.asarray(im.convert("RGB")).tobytes())
if not PREV:
    ff.stdin.close()
    ff.wait()
print("ok")
