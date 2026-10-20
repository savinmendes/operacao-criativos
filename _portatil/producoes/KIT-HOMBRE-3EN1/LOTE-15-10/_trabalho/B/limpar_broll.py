# -*- coding: utf-8 -*-
"""Tira a legenda queimada (branca/amarela com contorno preto) da faixa central dos takes de unboxing do vencedor,
com LaMa na GPU. Topo (selo) e rodapé (sticker) ficam: são cobertos pelos overlays novos na montagem.

Uso (venv _vg):  python limpar_broll.py fonte.mp4 inicio dur saida.mp4 [--faixa 760,975] [--prev q.png]
Saída: 720x1280 30 fps, sem áudio, bt709/tv, crf 14.
"""
import argparse
import subprocess
import warnings

import cv2
import numpy as np

warnings.filterwarnings("ignore")
COR = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]


def mascara(f, y0, y1):
    roi = f[y0:y1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    branco = (v >= 215) & (s <= 45)
    amarelo = (h >= 18) & (h <= 40) & (s >= 110) & (v >= 170)
    escuro = cv2.dilate((v < 70).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    core = ((branco | amarelo) & escuro).astype(np.uint8)
    # glifo inteiro: fecha e remove ruído
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    keep = np.zeros_like(core)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] >= 20:
            keep[lab == k] = 1
    if keep.sum() < 150:
        return None
    # linha de texto: caixa horizontal das componentes por linha -> retângulo justo, +margem
    ys, xs = np.nonzero(keep)
    m = np.zeros(f.shape[:2], np.uint8)
    # agrupa por faixas de 70 px (até 2 linhas de legenda)
    for a in range(0, y1 - y0, 35):
        sel = (ys >= a) & (ys < a + 70)
        if sel.sum() < 60:
            continue
    d = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
    m[y0:y1] = d
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fonte"); ap.add_argument("ini", type=float); ap.add_argument("dur", type=float); ap.add_argument("saida")
    ap.add_argument("--faixa", default="760,975"); ap.add_argument("--prev")
    a = ap.parse_args()
    y0, y1 = map(int, a.faixa.split(","))
    from simple_lama_inpainting import SimpleLama
    from PIL import Image
    lama = SimpleLama()
    cap = cv2.VideoCapture(a.fonte)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(a.ini * fps)))
    n = int(round(a.dur * fps))
    ff = None
    if not a.prev:
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280",
                               "-r", f"{fps}", "-i", "-", "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                               "-pix_fmt", "yuv420p", *COR, a.saida], stdin=subprocess.PIPE)
    for i in range(n):
        ok, f = cap.read()
        if not ok:
            break
        m = mascara(f, y0, y1)
        if m is not None:
            # LaMa só num recorte em volta da faixa (mais rápido e com contexto)
            c0, c1 = max(0, y0 - 140), min(1280, y1 + 140)
            crop = f[c0:c1]
            mk = m[c0:c1] * 255
            out = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk))
            out = cv2.cvtColor(np.array(out)[: crop.shape[0], : crop.shape[1]], cv2.COLOR_RGB2BGR)
            g = cv2.GaussianBlur(m[c0:c1].astype(np.float32), (9, 9), 0)[..., None]
            f[c0:c1] = (out * g + crop * (1 - g)).astype(np.uint8)
        if a.prev:
            if i == n // 2:
                vis = f.copy()
                if m is not None:
                    vis[m > 0] = (vis[m > 0] * 0.5 + np.array([0, 0, 255]) * 0.5).astype(np.uint8)
                cv2.imwrite(a.prev, np.hstack([f, vis]))
                break
            continue
        ff.stdin.write(np.ascontiguousarray(f).tobytes())
    if ff:
        ff.stdin.close(); ff.wait()
    print("ok", a.saida or a.prev)


if __name__ == "__main__":
    main()
