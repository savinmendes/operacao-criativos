# -*- coding: utf-8 -*-
"""Máscaras do TESTE1 (720x1280, quadros BGR): legenda PT, textos da moldura da live, título e círculos do quadro das 12 palavras."""
import numpy as np, cv2
PILL = np.load(__file__.replace("mascaras.py", "pill.npy"))
BOARD = (1893, 2215)   # quadros do quadro das 12 palavras
REF_RED = None
def red_mask(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    return (((hsv[..., 0] < 7) | (hsv[..., 0] > 172)) & (hsv[..., 1] > 140) & (hsv[..., 2] > 110)).astype(np.uint8)


def live(q):
    r = PILL[q]; return 396 <= r[1] <= 404 and 56 <= r[2] <= 64 and 512 <= r[3] <= 521

def leg(f, Y0=850, Y1=1030):
    roi = f[Y0:Y1]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    branco = (v > 185) & (s < 70)
    amarelo = (h >= 18) & (h <= 40) & (s > 90) & (v > 150)
    escuro = cv2.dilate((v < 55).astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
    core = ((branco | amarelo) & escuro).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] < 20 or st[k, cv2.CC_STAT_HEIGHT] > 70: core[lab == k] = 0
    # exige alinhamento horizontal típico de texto: linhas com muito núcleo
    if core.sum() < 150: return np.zeros(f.shape[:2], np.uint8)
    d = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    dn = np.zeros_like(d); dn[6:] = d[:-6]
    m = cv2.dilate(d | dn, np.ones((7, 7), np.uint8))
    full = np.zeros(f.shape[:2], np.uint8); full[Y0:Y1] = m
    return full

def caixa_clara(f, x0, y0, x1, y1, vmin=160, smax=80, dil=7):
    roi = f[y0:y1, x0:x1]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    c = ((hsv[..., 2] > vmin) & (hsv[..., 1] < smax)).astype(np.uint8)
    full = np.zeros(f.shape[:2], np.uint8); full[y0:y1, x0:x1] = cv2.dilate(c, np.ones((dil, dil), np.uint8))
    return full

def ui_live(f):
    m = caixa_clara(f, 118, 64, 392, 106, 150, 90, 7)            # "Pe. Rafael Martins ⌄"
    m |= caixa_clara(f, 56, 1170, 336, 1214, 140, 90, 7)         # "Comentários desativados"
    return m

def board(f):
    full = np.zeros(f.shape[:2], np.uint8)
    roi = f[150:310, 120:560]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    ouro = ((hsv[..., 2] > 120) & (hsv[..., 1] > 40) & (hsv[..., 0] >= 10) & (hsv[..., 0] <= 35)) | (hsv[..., 2] > 200)
    full[150:310, 120:560] = cv2.dilate(ouro.astype(np.uint8), np.ones((5, 5), np.uint8))
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    red = (((hsv[..., 0] < 7) | (hsv[..., 0] > 172)) & (hsv[..., 1] > 140) & (hsv[..., 2] > 110)).astype(np.uint8)
    if REF_RED is not None:
        red = red & (1 - REF_RED)          # só o vermelho que não existe no quadro sem círculo
        n, lab, st, _ = cv2.connectedComponentsWithStats(red)
        for k in range(1, n):
            if st[k, cv2.CC_STAT_AREA] < 15: red[lab == k] = 0
    full |= cv2.dilate(red, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    return full

def mascara(f, q):
    m = leg(f) if not (BOARD[0] <= q <= BOARD[1]) else np.zeros(f.shape[:2], np.uint8)
    if live(q): m |= ui_live(f)
    if 2395 <= q <= 2475:   # marca vermelha solta perto do crucifixo (artefato do vídeo IA)
        hsv = cv2.cvtColor(f[200:330, 300:480], cv2.COLOR_BGR2HSV)
        red = (((hsv[..., 0] < 8) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 120) & (hsv[..., 2] > 100)).astype(np.uint8)
        m[200:330, 300:480] |= cv2.dilate(red, np.ones((9, 9), np.uint8))
    if BOARD[0] <= q <= BOARD[1]: m |= board(f)
    return m
