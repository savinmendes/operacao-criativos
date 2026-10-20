# -*- coding: utf-8 -*-
"""Gancho novo do AD 05: cenas do próprio vídeo (full_up720) + narração clonada (hook.mp3) +
remoção da legenda antiga + legenda nova + manchete.  -> hook_final.mp4"""
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
sys.path.insert(0, str(KIT))
import legenda as LEG  # noqa: E402
import overlays as OV  # noqa: E402

P = Path(__file__).parent
SRC = P / "full_up720.mp4"
# (início na fonte, duração) — em ordem, somando a duração do gancho
SEGS = [(170.9, 1.65), (172.6, 0.75), (173.5, 1.8), (13.0, 2.1), (17.5, 1.8), (29.8, 1.6), (33.0, 2.2),
        (35.4, 1.6), (37.6, 1.6)]
tmp = P / "hook_tmp"
tmp.mkdir(exist_ok=True)


def run(*a):
    subprocess.run([str(x) for x in a], check=True)


lst = []
for i, (s, d) in enumerate(SEGS):
    o = tmp / f"s{i}.mp4"
    run("ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC, "-an", "-vf", "fps=30,setpts=PTS-STARTPTS",
        "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", o)
    lst.append(f"file '{o.as_posix()}'")
(tmp / "lista.txt").write_text("\n".join(lst), encoding="utf-8")
cru = tmp / "cru.mp4"
run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", tmp / "lista.txt", "-c:v", "libx264", "-crf", "14",
    "-pix_fmt", "yuv420p", "-r", "30", cru)

# remove a legenda antiga: só traços finos claros (top-hat) na faixa da legenda
limpo = tmp / "limpo.mp4"
cap = cv2.VideoCapture(str(cru))
W, H = int(cap.get(3)), int(cap.get(4))
Y0, Y1, X0, X1 = 880, 1070, 20, W - 20
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                       "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(limpo)], stdin=subprocess.PIPE)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
while True:
    ok, im = cap.read()
    if not ok:
        break
    roi = im[Y0:Y1, X0:X1]
    g = roi.min(2)
    branco = (g > 185).astype(np.uint8)
    fino = branco & (1 - cv2.morphologyEx(branco, cv2.MORPH_OPEN, k))
    m = np.zeros(im.shape[:2], np.uint8)
    m[Y0:Y1, X0:X1] = cv2.dilate(fino, np.ones((7, 7), np.uint8), iterations=1)
    im = cv2.inpaint(im, m, 6, cv2.INPAINT_TELEA)
    ff.stdin.write(im.tobytes())
ff.stdin.close()
ff.wait()

# áudio + legenda nova + manchete
ali = P / "hook.alinhamento.json"
pal = LEG.palavras_por_alinhamento(str(ali), 0)
ass = tmp / "hook.ass"
LEG.gera_ass(pal, str(ass), "drop", {"esposo", "compañera", "miraba", "veintidós", "teléfono", "luz"}, y=1460)
leg = tmp / "leg.mp4"
LEG.queimar(str(limpo), str(ass), str(leg), crf=14)
man = OV.manchete("¿POR QUÉ MI ESPOSO\nYA NO ME MIRABA? 💔", str(tmp / "manchete.png"), 60)
dur = sum(d for _, d in SEGS)
run("ffmpeg", "-v", "error", "-y", "-i", leg, "-i", P / "hook.mp3", "-i", man, "-filter_complex",
    "[2:v]scale=iw*2/3:-1[m];[0:v][m]overlay=(W-w)/2:90:enable='lt(t,4.2)',format=yuv420p[v];"
    f"[1:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{dur:.3f}[a]",
    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "14", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}",
    P / "hook_final.mp4")
print("ok hook", dur)
