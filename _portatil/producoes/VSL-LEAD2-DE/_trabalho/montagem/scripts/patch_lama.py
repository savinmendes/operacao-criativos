# -*- coding: utf-8 -*-
"""(venv _vg) Limpa residuos de legenda ES nos quadros da base listados em residuo/achados_ok.json com LaMa
(mesmo metodo do limpar.py da base). Grava residuo/patches/<q>.npz (faixa 600-910: px + alfa)."""
import sys, json, subprocess, warnings; warnings.filterwarnings("ignore")
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\base\scripts")
from limpar import preparar, inpaint
from simple_lama_inpainting import SimpleLama
from pathlib import Path
M = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem"); BASE = M.parent / "base" / "base_limpa_live.mp4"
W, H = 720, 960; Y0, Y1 = 600, 910
A = {int(k): v for k, v in json.load(open(M / "residuo" / "achados_ok.json", encoding="utf-8")).items()}
EXTRA = {int(k): v for k, v in json.load(open(M / "residuo" / "extra.json", encoding="utf-8")).items()} if (M / "residuo" / "extra.json").exists() else {}
out = M / "residuo" / "patches"; out.mkdir(exist_ok=True)
lama = SimpleLama()
qs = sorted(set(A) | set(EXTRA))
def ler(q):
    pr = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{(q - 0.5) / 30:.5f}", "-i", str(BASE), "-frames:v", "1", "-vf",
        "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24", "-f", "rawvideo", "-"], capture_output=True)
    return np.frombuffer(pr.stdout, np.uint8).reshape(H, W, 3).copy()
prev = None; pm = None; pq = None
for n, q in enumerate(qs):
    f = ler(q)
    bx = [b[:4] for b in A.get(q, [])]
    if bx:
        u, mk, modos = preparar(f, bx)
    else:
        u, mk = f, np.zeros((H, W), np.uint8)
    for x0, y0, x1, y1 in EXTRA.get(q, []):   # caixas marcadas a mao (residuo pequeno que o OCR nao le)
        mk[y0:y1, x0:x1] = 1
    o = inpaint(lama, u, mk)
    if prev is not None and pq == q - 1:
        both = (mk > 0) & (pm > 0); o = o.copy(); o[both] = np.clip(0.7 * o[both] + 0.3 * prev[both], 0, 255).astype(np.uint8)
    prev, pm, pq = o, mk, q
    diff = (np.abs(o.astype(int) - f.astype(int)).sum(2) > 3).astype(np.uint8)
    al = cv2.GaussianBlur(cv2.dilate(diff, np.ones((5, 5), np.uint8)).astype(np.float32), (0, 0), 1.5)
    al = (np.clip(al * 1.5, 0, 1) * 255).astype(np.uint8)
    np.savez_compressed(out / f"{q}.npz", y0=Y0, al=al[Y0:Y1], px=o[Y0:Y1])
    if n % 50 == 0: print(f"[{n}/{len(qs)}]", flush=True)
print("ok", len(qs))
