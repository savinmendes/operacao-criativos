# -*- coding: utf-8 -*-
"""Tira a interface do TikTok das capturas de tela sobrepostas (overlay estatico):
 - "fundo": retangulos onde a captura vira o fundo do proprio video (quadro fundo_q, sem overlay) = recorte da captura;
 - "lama": retangulos apagados com LaMa (CPU) quadro a quadro.
So mexe num retangulo quando o overlay esta la (diferenca para o quadro de referencia 'still' < LIM).
Saida: ov_patches.npz (quadro -> recorte limpo da regiao de trabalho) + ov_antes_depois.jpg.
Uso: _vg\\Scripts\\python ov_limpar.py ov.json"""
import sys, json, warnings, subprocess; warnings.filterwarnings("ignore")
import numpy as np, cv2
from PIL import Image
from simple_lama_inpainting import SimpleLama
from pathlib import Path
AQ = Path(__file__).parent
cfg = json.load(open(sys.argv[1]))
LIM = cfg.get("lim", 15)
def quadros(p, pula=0, n=None, w=720, h=1280):
    pr = subprocess.Popen(["ffmpeg","-v","error","-i",str(p),"-vf",f"select=gte(n\\,{pula}),scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
        "-fps_mode","passthrough","-f","rawvideo","-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    k = 0; t = w * h * 3
    while n is None or k < n:
        b = pr.stdout.read(t)
        if len(b) < t: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3).copy(); k += 1
    pr.stdout.close(); pr.kill(); pr.wait()
V = cfg["video"]
S = next(quadros(V, cfg["still"], 1)).astype(np.float32)
BG = next(quadros(V, cfg["fundo_q"], 1))
R = cfg["lama"] + cfg["fundo"]
X0 = min(r[0] for r in R) - 24; Y0 = min(r[1] for r in R) - 24; X1 = max(r[2] for r in R) + 24; Y1 = max(r[3] for r in R) + 24
X0, Y0 = max(0, X0), max(0, Y0); X1, Y1 = min(720, X1), min(1280, Y1)
lama = SimpleLama()
q0, q1 = cfg["janela"]; P = {}; amostra = None
for k, f in enumerate(quadros(V, q0, q1 - q0)):
    q = q0 + k; ff = f.astype(np.float32); out = f.copy(); mexeu = False
    for x0, y0, x1, y1 in cfg["fundo"]:
        if np.abs(ff[y0:y1, x0:x1] - S[y0:y1, x0:x1]).mean() < LIM:
            out[y0:y1, x0:x1] = BG[y0:y1, x0:x1]; mexeu = True
    m = np.zeros((1280, 720), np.uint8)
    for x0, y0, x1, y1 in cfg["lama"]:
        if np.abs(ff[y0:y1, x0:x1] - S[y0:y1, x0:x1]).mean() < LIM:
            m[y0:y1, x0:x1] = 255
    if m.any():
        crop = out[Y0:Y1, X0:X1].copy(); mk = m[Y0:Y1, X0:X1]
        r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk))
        r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
        a = (cv2.GaussianBlur(mk.astype(np.float32) / 255, (5, 5), 0))
        a = np.maximum(a, mk / 255.0)[..., None]
        out[Y0:Y1, X0:X1] = np.clip(r * a + crop * (1 - a), 0, 255).astype(np.uint8); mexeu = True
    if mexeu:
        P[q] = out[Y0:Y1, X0:X1]
        if q == cfg["still"]: amostra = (f[Y0:Y1, X0:X1], out[Y0:Y1, X0:X1])
    if k % 20 == 0: print(q, mexeu, flush=True)
np.savez_compressed(AQ / "ov_patches.npz", caixa=np.array([X0, Y0, X1, Y1]), qs=np.array(sorted(P)), ps=np.stack([P[q] for q in sorted(P)]))
if amostra: cv2.imwrite(str(AQ / "ov_antes_depois.jpg"), cv2.resize(np.hstack(amostra), None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))
print("ok", len(P), "quadros", (X0, Y0, X1, Y1))
