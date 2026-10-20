# -*- coding: utf-8 -*-
"""Varre os quadros da BASE realmente usados (a cada 5 quadros do video final) com OCR na faixa da legenda (y 600-910)
e depois quadro a quadro em volta dos achados. Saida: residuo/achados.json {orig_q: [[x0,y0,x1,y1,txt,conf],...]}"""
import sys, json, subprocess, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import *
from rapidocr_onnxruntime import RapidOCR
P = json.load(open(M / "params.json")); F0 = int(round(P["T0"] * FPS)); NF = P["NF"]
COB = json.load(open(M / "cobertura.json", encoding="utf-8"))
def q_base(k):
    F = F0 + k
    for c in COB:
        if round(c["novo_ini"] * FPS) <= F < round(c["novo_fim"] * FPS):
            return int(round((c["src_ini"] + F / FPS - c["novo_ini"]) * FPS))
    return int(round(novo2orig(F / FPS) * FPS))
qs = sorted(set(q_base(k) for k in range(0, NF, 5)))
Y0, Y1 = 600, 910
ocr = RapidOCR()
def ler_q(qlist):
    """le quadros (faixa) da base por indice, em ordem, com leitor sequencial que pula buracos grandes por seek"""
    out = {}; i = 0
    while i < len(qlist):
        a = qlist[i]; j = i
        while j + 1 < len(qlist) and qlist[j + 1] - qlist[j] <= 30: j += 1
        b = qlist[j]
        pr = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{(a - 0.5) / FPS:.5f}", "-i", str(BASE), "-frames:v", str(b - a + 1), "-vf",
                               READ_VF, "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        want = set(qlist[i:j + 1]); q = a
        while q <= b:
            buf = pr.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            if q in want: yield q, np.frombuffer(buf, np.uint8).reshape(H, W, 3)[Y0:Y1].copy()
            q += 1
        pr.stdout.close(); pr.wait(); i = j + 1
def boxes(f):
    r, _ = ocr(f, use_cls=False)
    res = []
    for bx, txt, c in (r or []):
        if c > 0.6 and len(txt.strip()) >= 2:
            x = [p[0] for p in bx]; y = [p[1] + Y0 for p in bx]
            res.append([int(min(x)), int(min(y)), int(max(x)), int(max(y)), txt, round(float(c), 2)])
    return res
achados = {}
n = 0
for q, f in ler_q(qs):
    b = boxes(f); n += 1
    if b: achados[q] = b
    if n % 1000 == 0: print(f"[{n}/{len(qs)}] achados {len(achados)}", flush=True)
print("amostragem:", len(achados), flush=True)
viz = sorted(set(q2 for q in achados for q2 in range(q - 6, q + 7)) - set(achados))
for q, f in ler_q(viz):
    b = boxes(f)
    if b: achados[q] = b
(M / "residuo").mkdir(exist_ok=True)
json.dump({str(k): v for k, v in sorted(achados.items())}, open(M / "residuo" / "achados.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("total quadros com texto:", len(achados))
for q in sorted(achados)[:400]: print(q, round(q / 30, 2), [x[4] for x in achados[q]])
