# -*- coding: utf-8 -*-
"""Remendo do rótulo (0–7,73 s): faixa marrom com "LYMPHORIA" desenhada no quadro 0 e levada a cada quadro
pela matriz do rastreio.json.  aplicar(frame_rgb, k) -> frame_rgb"""
import sys, json
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, str(Path(__file__).parent.parent / "comum"))
import texto as T
D = Path(__file__).parent
RAS = {o["k"]: o for o in json.loads((D / "rastreio.json").read_text(encoding="utf-8"))}
W, H = 720, 1280
BANDS = {0: (186, 649, 276, 674), 136: (144, 686, 234, 709)}


def _patch(ak):
    f0 = T.ler_quadros(str(D / "orig.mp4"), ss=ak / 30, t=0.04)[0]
    BAND = BANDS[ak]
    x0, y0, x1, y1 = BAND
    reg = f0[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    lum = reg.mean(1)
    cor = (29, 71, 52)   # verde da faixa do rótulo Lymphoria (antes: marrom do frasco Vitaly)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle(BAND, fill=cor + (255,))
    txt = "LYMPHORIA"
    px = T.px_para_largura([(txt, 1)], (x1 - x0) * 0.80)
    y_0, y_1, _, _ = T.tinta_bbox([(txt, 1)], px)
    T.desenhar_linha(im, [(txt, 1)], (x0 + x1) / 2 + 1, (y0 + y1) / 2 - (y_0 + y_1) / 2, px, cor=(244, 242, 234, 255))
    a = np.asarray(im).astype(np.float32)
    al = Image.fromarray(a[..., 3].astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    a[..., 3] = np.minimum(a[..., 3], np.asarray(al).astype(np.float32) * 1.0 + 0)  # borda suave
    return a, cor


PATCHES = {ak: _patch(ak) for ak in BANDS}
COR = PATCHES[0][1]


def aplicar(fr, k):
    o = RAS.get(k)
    if not o or o["M"] is None:
        return fr
    M = np.float32(o["M"])
    w = cv2.warpAffine(PATCHES[o["a"]][0], M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    if k >= 218:                      # frasco saindo do quadro com borrão de movimento
        w = cv2.GaussianBlur(w, (0, 0), 1.5 + (k - 218) * 1.2)
    al = w[..., 3:4] / 255.0
    return (fr.astype(np.float32) * (1 - al) + w[..., :3] * al).clip(0, 255).astype(np.uint8)


if __name__ == "__main__":
    fr = T.ler_quadros(str(D / "orig.mp4"), t=7.75)
    ks = list(range(92, 104, 1)) + list(range(214, 228, 2))
    tiles = []
    for k in ks:
        o = RAS[k]
        g = aplicar(fr[k], k)
        c = np.float32([[230, 662]] if o["a"] in (0, None) else [[189, 697]])
        if o["M"] is not None:
            c = cv2.transform(c[None], np.float32(o["M"]))[0]
        cx, cy = int(c[0][0]), int(c[0][1])
        x0, y0 = max(0, cx - 90), max(0, cy - 70)
        im = Image.fromarray(g[y0:y0 + 140, x0:x0 + 180]).resize((270, 210))
        ImageDraw.Draw(im).text((3, 3), str(k), fill="red")
        tiles.append(im)
    cols = 6
    sheet = Image.new("RGB", (270 * cols, 210 * ((len(tiles) + cols - 1) // cols)))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * 270, (i // cols) * 210))
    sheet.save(D / "fr" / "rotulo_chk.jpg")
    print("cor faixa", COR)
