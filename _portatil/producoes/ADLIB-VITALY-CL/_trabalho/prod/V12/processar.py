# -*- coding: utf-8 -*-
"""V12: parte 1 (0 até o fim de 'sobraban', quadro 1933) com títulos/legendas trocados e takes do frasco Lymphoria."""
import subprocess, cv2, numpy as np, caixas as C
V = r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\VIDEOS\12 - Mi Camino al Bienestar - 1313049140654830.mp4"
FIM = 1934                       # quadros 0..1933 (64,467 s)
T_EXT = (464, 866); C_EXT = (470, 551)
T_HIE = (1086, 1277); C_LYM = (1088, 1175)
REP1 = (1086, 1198)              # boticário -> takeA
REP2 = (1277, 1433)              # mulher pingando -> takeC_lento (ad14 t3 a 0,65x)
BOX_CAFE = (98, 43, 620, 147)
def le(p):
    c = cv2.VideoCapture(p); out = []
    while True:
        r, f = c.read()
        if not r: break
        out.append(f)
    return out
A = le("takeA.mp4"); B = le("takeC_lento.mp4"); B += [B[-1]] * (156 - len(B))
assert len(A) >= 112 and len(B) >= 156, (len(A), len(B))
cap = cv2.VideoCapture(V)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", "30", "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-threads", "3", "-pix_fmt", "yuv420p",
                      "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "parte1_video.mp4"], stdin=subprocess.PIPE)
ins = lambda i, r: r[0] <= i < r[1]
for i in range(FIM):
    ok, fo = cap.read(); assert ok, i
    f = fo.copy()
    if ins(i, REP1) or ins(i, REP2):
        f = (A[i - REP1[0]] if ins(i, REP1) else B[i - REP2[0]]).copy()
        bb = C.bbox_verde(fo)
        if bb and not ins(i, C_LYM):
            f = C.copia_arred(f, fo, (bb[0], bb[1], bb[2], bb[3]), 18)
        if ins(i, REP2):
            f = C.copia_arred(f, fo, BOX_CAFE, 14)
    if ins(i, T_EXT):
        f = C.cola_caixa_branca(f, (68, 50, 652, 155), 14, [("4 EXTRACTOS QUE", 27, 66, 547 - 172), ("DISUELVEN LOS BLOQUEOS", 27, 112, 636 - 84)])
    if ins(i, C_EXT):
        f = C.cola_caixa_verde(f, ["cuatro extractos naturales", "entran a tu torrente"], 998, 41, min_box=C.bbox_verde(fo), pad_x=26, alt=124)
    if ins(i, T_HIE):
        f = C.cola_caixa_branca(f, (25, 42, 694, 105), 14, [("4 HIERBAS · 1 FÓRMULA · 20 GOTAS", 24, 66, 677 - 42)])
    if ins(i, C_LYM):
        f = C.cola_caixa_verde(f, ["Lymphoria tiene las cuatro", "hierbas en una sola fórmula"], 998, 41, min_box=C.bbox_verde(fo), pad_x=26, alt=124)
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait(); print("ok parte1_video.mp4", FIM, "quadros")
