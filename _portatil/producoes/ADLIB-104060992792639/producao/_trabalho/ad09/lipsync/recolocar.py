# -*- coding: utf-8 -*-
"""Cola as saídas do HeyGen (entrada recortada no rosto, boxes/<nome>.json) de volta na base limpa, SÓ numa elipse
boca/queixo do rosto de quem fala, com borda suave. Reamostra no tempo (sem congelar) se vier com quadros a menos.
Emendas na mesma tomada: fusão de 3 quadros na região da boca.
Uso: python recolocar.py segs.json plano.json   (plano: {"A": "out/ls_A.mp4", "B": "out/ls_B.mp4@1", "C": "cobrir"...})
Saída: ../base_lipsync.mp4 (24 fps, sem áudio, bt709 tv)."""
import sys, json, subprocess, numpy as np, cv2
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
CFG = json.load(open(AQ / sys.argv[1], encoding="utf-8")); PL = json.load(open(AQ / sys.argv[2], encoding="utf-8")); FPS = CFG["fps"]
def ler(p, pula=0):
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr[pula:]
def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / (n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[min(j, m - 1)] if (a < 1e-3 or j >= m - 1) else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0))
    return out
def elipse(face, cy=0.70, rx=0.38, ry=0.32):
    x0, y0, x1, y1 = face; fw, fh = x1 - x0, y1 - y0
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int((x0 + x1) / 2), int(y0 + cy * fh)), (int(rx * fw), int(ry * fh)), 0, 0, 360, 1.0, -1)
    s = max(3.0, 0.07 * fw); m = cv2.GaussianBlur(m, (0, 0), s)
    return m[..., None]
def colar(base, g, bx, par):
    X0, Y0, Wi, Hi = bx["crop"]
    c = cv2.resize(g, (Wi, Hi), interpolation=cv2.INTER_AREA)
    full = base.copy()
    xa, ya, xb, yb = max(0, X0), max(0, Y0), min(720, X0 + Wi), min(1280, Y0 + Hi)
    full[ya:yb, xa:xb] = c[ya - Y0:yb - Y0, xa - X0:xb - X0]
    M = elipse(bx["face"], **par)
    return np.clip(full * M + base * (1 - M), 0, 255).astype(np.uint8), M
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
    "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
capb = cv2.VideoCapture(str(AD / CFG["base"])); pos = 0; log = []
pend = []   # [(quadro, img, mask, base)] ainda não escritos (fim do segmento anterior)
def flush(): 
    global pend
    for _, f, _, _ in pend: ff.stdin.write(f.tobytes())
    pend = []
def ler_base(k):
    global pos
    fr = []
    while pos < k:
        ok, f = capb.read()
        if not ok: break
        fr.append(f); pos += 1
    return fr
segs = CFG["segs"]; prev = None
for sg in segs:
    nome = sg["nome"]; a, b = sg["q"]
    if nome not in PL:
        log.append(f"{nome}: sem lipsync (base)"); continue
    flush_needed = True
    antes = ler_base(a)
    if antes: flush(); [ff.stdin.write(f.tobytes()) for f in antes]
    bases = ler_base(b + 1)
    arq, _, pula = PL[nome].partition("@")
    bx = json.load(open(AQ / "boxes" / f"{nome}.json")); n, pad = bx["n"], bx["pad"]; assert n == len(bases), (nome, n, len(bases))
    g = ler(AQ / arq, int(pula or 0)); m = len(g)
    g = reamostrar(g, n + pad)[:n]
    par = sg.get("elipse", {}); cur = []
    for i in range(n):
        f, M = colar(bases[i], g[i], bx["boxes"][i], par); cur.append((a + i, f, M, bases[i]))
    log.append(f"{nome}: {m} quadros -> {n + pad} (usa {n}){' pula ' + pula if pula else ''}")
    if pend and pend[-1][0] == a - 1:
        bA, bB = pend[-1][3], cur[0][3]
        if np.abs(cv2.resize(bA, (90, 160)).astype(float) - cv2.resize(bB, (90, 160))).mean() <= 10:
            A_, B_ = pend[-1][1].astype(np.float32), cur[0][1].astype(np.float32); alvo = (A_ + B_) / 2
            M = np.maximum(pend[-1][2], cur[0][2])
            seq = pend[-2:] + cur[:2]; ws = [0.25, 0.5, 0.5, 0.25][-len(seq):] if len(pend) >= 2 else [0.5, 0.5, 0.25]
            for (q, f, mm, bb), w in zip(seq, ws):
                f[:] = np.clip(f.astype(np.float32) * (1 - w * M) + alvo * (w * M), 0, 255).astype(np.uint8)
            log.append(f"emenda q{a}: fusão na boca")
    flush()
    for q, f, M, bb in cur[:-2]: ff.stdin.write(f.tobytes())
    pend = cur[-2:]
flush()
for f in ler_base(10**9): ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait()
print(chr(10).join(log)); print("ok", pos, "quadros")
