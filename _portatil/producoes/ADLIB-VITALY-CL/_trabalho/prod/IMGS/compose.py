# Cola so a regiao do rotulo (diferenca NB2 x original, dentro das caixas) de volta no original, em resolucao cheia.
import glob, json, os, sys
import numpy as np, cv2
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SRC = r"C:/Users/PICHAU/Downloads/ADLIB-VITALY-CL/IMAGENS/"
C = json.load(open("crops.json"))
CFG = {
    "02": dict(boxes=[(55, 450, 450, 1245)], leaf=True, bghue=(120, 200), thr=14, close=45, hull=False),
    "04": dict(boxes=[(1070, 1180, 1515, 1890)]),
    "06": dict(boxes=[(1080, 1380, 1470, 1822)]),
    "07": dict(boxes=[(135, 1110, 675, 1700), (940, 1115, 1320, 1700)]),
    "08": dict(boxes=[(790, 1440, 1020, 1830)]),
    "13": dict(boxes=[(665, 1070, 925, 1478)], noise=5, blur=0.6),
    "15": dict(boxes=[(665, 985, 970, 1480)], leaf=True),
    "16": dict(boxes=[(720, 680, 910, 1000)], leaf=True, leafmax=135),
    "18": dict(boxes=[(930, 1120, 1180, 1880)]),
    "21": dict(boxes=[(400, 760, 680, 1115), (460, 495, 705, 650)], hull=False),
    "27": dict(boxes=[(340, 1050, 765, 1600)]),
    "28": dict(boxes=[(1290, 1440, 1530, 1840)]),
}


def compose(n, save=True):
    cfg = CFG[n]
    f = glob.glob(SRC + n + " - *.jpg")[0]
    im = np.asarray(Image.open(f).convert("RGB")).copy()
    x0, y0, x1, y1 = C[n]
    nb = np.asarray(Image.open("nb/%s.png" % n).convert("RGB").resize((x1 - x0, y1 - y0), Image.LANCZOS))
    orig = im[y0:y1, x0:x1]
    diff = np.abs(nb.astype(int) - orig.astype(int)).max(2)
    m = (diff > cfg.get("thr", 28)).astype(np.uint8)
    lim = np.zeros_like(m)
    for bx0, by0, bx1, by1 in cfg["boxes"]:
        lim[max(by0 - y0, 0):by1 - y0, max(bx0 - x0, 0):bx1 - x0] = 1
    hsv = cv2.cvtColor(orig, cv2.COLOR_RGB2HSV).astype(int)  # H 0-180
    h, s, v = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
    excl = np.zeros_like(m)
    if cfg.get("leaf"):
        excl |= ((h > 60) & (h < cfg.get("leafmax", 150)) & (s > 0.35) & (v > 0.12)).astype(np.uint8)
    bgx = np.zeros_like(m)
    if cfg.get("bghue"):
        a, b = cfg["bghue"]
        bgx = ((h > a) & (h < b) & (s < 0.3) & (v > 0.7)).astype(np.uint8)
    m = m & lim & (1 - bgx) & (1 - excl)
    kk = cfg.get("close", 15)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kk, kk))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    # preenche buracos
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    big = [c for c in cnts if cv2.contourArea(c) > 400]
    m2 = np.zeros_like(m)
    if cfg.get("hull", True):
        big = [cv2.convexHull(c) for c in big]
    cv2.drawContours(m2, big, -1, 1, -1)
    m2 = cv2.dilate(m2, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) & lim
    if cfg.get("blur"):
        nb = cv2.GaussianBlur(nb, (0, 0), cfg["blur"])
    if cfg.get("noise"):
        rng = np.random.default_rng(1)
        nb = np.clip(nb.astype(float) + rng.normal(0, cfg["noise"], nb.shape[:2])[..., None], 0, 255).astype(np.uint8)
    a = cv2.GaussianBlur(m2.astype(np.float32), (0, 0), 2.0)[..., None]
    out = (nb * a + orig * (1 - a)).astype(np.uint8)
    im[y0:y1, x0:x1] = out
    if save:
        Image.fromarray(im).save("comp/%s.png" % n)
        Image.fromarray((m2 * 255).astype(np.uint8)).save("comp/%s_mask.png" % n)
    return im


if __name__ == "__main__":
    os.makedirs("comp", exist_ok=True)
    for n in (sys.argv[1:] or [k for k in CFG if os.path.exists("nb/%s.png" % k)]):
        compose(n)
        print(n, "ok")
