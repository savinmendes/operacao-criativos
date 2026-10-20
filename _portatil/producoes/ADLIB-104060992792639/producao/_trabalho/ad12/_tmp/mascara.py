"""Mascara justa da legenda PT (amarela c/ contorno escuro, faixa y 960-1110) e da seta vermelha do original (y 740-950)."""
import cv2, numpy as np
R0, R1 = 720, 1130          # linhas salvas (faixa de trabalho)
def mascara(f):
    M = np.zeros((R1 - R0, 720), np.uint8)
    Y0, Y1 = 955, 1115
    roi = f[Y0:Y1]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    core = ((h >= 20) & (h <= 40) & (s >= 120) & (v >= 170)).astype(np.uint8) & cv2.dilate((v < 80).astype(np.uint8), np.ones((7, 7), np.uint8))
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    keep = np.zeros_like(core)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] >= 6: keep[lab == k] = 1
    if keep.sum() >= 60:                       # tem legenda
        rows = np.where(keep.any(1))[0]; cols = np.where(keep.any(0))[0]
        box = np.zeros_like(keep); box[max(0, rows[0] - 12):rows[-1] + 13, max(0, cols[0] - 14):cols[-1] + 15] = 1
        out = (v < 110).astype(np.uint8) & cv2.dilate(keep, np.ones((9, 9), np.uint8))
        m = cv2.dilate(cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) | out, np.ones((9, 9), np.uint8)) & box
        M[Y0 - R0:Y1 - R0] |= m
    A0, A1 = 730, 1010
    hsv = cv2.cvtColor(f[A0:A1], cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    red = (((h <= 6) | (h >= 172)) & (s >= 170) & (v >= 140)).astype(np.uint8)
    red = cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    if red.sum() >= 400:
        m = cv2.dilate(red, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
        perto = cv2.dilate(red, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (221, 221)))
        wht = ((v >= 232) & (s <= 28)).astype(np.uint8) & perto & (1 - cv2.dilate(red, np.ones((3, 3), np.uint8)))
        m |= cv2.dilate(wht, np.ones((7, 7), np.uint8))
        M[A0 - R0:A1 - R0] |= m
    return M
