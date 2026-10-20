# -*- coding: utf-8 -*-
"""Passo 2 da limpeza: LaMa (GPU) nas caixas do OCR + retangulos fixos. Cor bt601/tv fixa na leitura e na gravacao.
Uso: _vg python lama_limpar.py config.json
config: video, saida, caixas_json, passo, tipo ("branco"|"amarelo"), pad, sublinhado (bool),
        fixos: [[x0,y0,x1,y1,q_de,q_ate], ...] (mascara retangular cheia), apagar: [[q_de,q_ate,x0,y0,x1,y1]] (caixa extra), ate"""
import sys, json, time, warnings, subprocess; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
CX = {int(k): v for k, v in json.load(open(cfg["caixas_json"], encoding="utf-8")).items()} if cfg.get("caixas_json") else {}
P = cfg.get("passo", 2); PAD = cfg.get("pad", 8); tipo = cfg.get("tipo", "branco"); ate = cfg.get("ate")
fixos = cfg.get("fixos", []); extras = cfg.get("apagar", [])
ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", cfg["video"], "-vf",
                       "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
                       "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", "30", "-i", "-",
                       "-an", *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, cfg["saida"]], stdin=subprocess.PIPE)
lama = SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
K3 = np.ones((3, 3), np.uint8)

import re
EXC = re.compile(cfg["excluir"]) if cfg.get("excluir") else None
def caixas(i):
    out = []
    for j in range(i - P, i + P + 1):
        out += [b for b in CX.get(j, []) if not (EXC and EXC.search(b[4]))]
    out += [[x0, y0, x1, y1, "extra"] for a, b, x0, y0, x1, y1 in cfg.get("caixas_extra", []) if a <= i <= b]
    return out

def mascara(f, i):
    m = np.zeros((1280, 720), np.uint8)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV); H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    for x0, y0, x1, y1, *_ in caixas(i):
        X0, Y0, X1, Y1 = max(0, x0 - PAD), max(0, y0 - PAD), min(720, x1 + PAD), min(1280, y1 + PAD)
        tp = tipo
        if any(q0 <= i <= q1 for q0, q1 in cfg.get("retangulo_em", [])):
            tp = "retangulo"; X0 = max(0, X0 - cfg.get("ret_esq", 0))
        if tp == "branco":
            core = ((V[Y0:Y1, X0:X1] >= 150) & (S[Y0:Y1, X0:X1] <= 90)).astype(np.uint8)
            d = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
            dn = np.zeros_like(d); dn[3:] = d[:-3]; m[Y0:Y1, X0:X1] |= d | dn
        elif tp == "amarelo":
            h, s, v = H[Y0:Y1, X0:X1], S[Y0:Y1, X0:X1], V[Y0:Y1, X0:X1]
            core = ((h >= 15) & (h <= 42) & (s >= 80) & (v >= 140)).astype(np.uint8) & cv2.dilate((v < 90).astype(np.uint8), np.ones((7, 7), np.uint8))
            d = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
            dn = np.zeros_like(d); dn[5:] = d[:-5]; m[Y0:Y1, X0:X1] |= cv2.dilate(d | dn, np.ones((7, 7), np.uint8))
        else:  # retangulo
            m[Y0:Y1, X0:X1] = 1
        if cfg.get("sublinhado"):  # linha amarela logo abaixo do titulo (AD 37)
            h = y1 - y0; s0, s1 = min(1280, y1), min(1280, y1 + int(1.0 * h) + 6)
            yel = ((H[s0:s1, X0:X1] >= 15) & (H[s0:s1, X0:X1] <= 40) & (S[s0:s1, X0:X1] >= 110) & (V[s0:s1, X0:X1] >= 130))
            rows = np.where(yel.mean(1) > 0.55)[0]
            for r in rows: m[max(0, s0 + r - 3):s0 + r + 4, X0:X1] = 1
    for x0, y0, x1, y1, a, b in fixos:
        if a <= i <= b: m[y0:y1, x0:x1] = 1
    for a, b, x0, y0, x1, y1 in extras:
        if a <= i <= b: m[y0:y1, x0:x1] = 1
    return m

T = 720 * 1280 * 3; ema = None; prev = None; t0 = time.time(); i = 0
while True:
    buf = pr.stdout.read(T)
    if len(buf) < T or (ate and i >= ate): break
    f = np.frombuffer(buf, np.uint8).reshape(1280, 720, 3).copy()
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g - prev).mean() > 20: ema = None
    prev = g
    m = mascara(f, i)
    if m.sum() == 0:
        ema = None; ff.stdin.write(f.tobytes()); i += 1; continue
    ys = np.where(m.any(1))[0]; a0 = max(0, ys.min() - 80); a1 = min(1280, ys.max() + 80)
    crop = f[a0:a1]; mk = m[a0:a1]
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
    l = f.astype(np.float32).copy(); l[a0:a1] = r
    ema = l if (ema is None or ema.shape != l.shape) else 0.65 * l + 0.35 * ema
    al = np.maximum(cv2.GaussianBlur(m.astype(np.float32), (11, 11), 0), m)[..., None]
    f = np.clip(ema * al + f * (1 - al), 0, 255).astype(np.uint8)
    ff.stdin.write(np.ascontiguousarray(f).tobytes()); i += 1
    if i % 150 == 0: print(f"[{i}] {time.time()-t0:.0f}s", flush=True)
pr.kill(); ff.stdin.close(); ff.wait()
print("ok", i, "quadros", round(time.time() - t0), "s")
