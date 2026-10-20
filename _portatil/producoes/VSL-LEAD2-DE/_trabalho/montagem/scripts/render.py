# -*- coding: utf-8 -*-
"""Renderiza um bloco da VSL DE: python render.py <bloco> [--n 9000]
Quadro global k -> quadro F = round(T0*30)+k da timeline nova (timeline_de). Fonte: cobertura b-roll > comp/<id>.mp4 > base retimed.
Legenda ASS queimada; leitura/gravacao bt601 fixa (etiqueta so no mux final)."""
import sys, json, subprocess, time
import numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import *
P = json.load(open(M / "params.json")); T0, NF = P["T0"], P["NF"]; F0 = int(round(T0 * FPS))
BL = int(sys.argv[1]); NB = 9000
k0 = BL * NB; k1 = min(NF, k0 + NB)
TESTE = len(sys.argv) > 2
if TESTE: k0 = int(sys.argv[2]); k1 = k0 + int(sys.argv[3])
COB = json.load(open(M / "cobertura.json", encoding="utf-8"))
LOT = [t for t in json.load(open(T / "voz" / "lotes.json", encoding="utf-8"))["trechos"] if int(t["id"][1:]) >= 22]
CLIPS = []
for t in LOT:
    jp = M / "comp" / f"{t['id']}.json"
    if not jp.exists():
        if TESTE or round(t["novo_fim"] * FPS) <= F0 + k0 or round(t["novo_ini"] * FPS) >= F0 + k1: continue
        raise SystemExit(f"falta comp {t['id']}")
    info = json.load(open(jp))
    n = info["N"] if t["id"] != "L244" else min(round(c["novo_ini"] * FPS) for c in COB if "L244" in c["trechos"]) - info["q0"]
    CLIPS.append((info["q0"], info["q0"] + n, t["id"]))
CLIPS.sort()

class Leitor:
    def __init__(self, p, ss_q=0):
        self.p = p; self.abrir(ss_q)
    def abrir(self, q):
        if getattr(self, "pr", None): self.pr.kill(); self.pr.wait()
        cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{(q - 0.5) / FPS:.5f}"] if q > 0 else []) + ["-i", str(self.p), "-vf", READ_VF,
               "-fps_mode", "passthrough", "-f", "rawvideo", "-"]
        self.pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=W * H * 3 * 4)
        self.q = q - 1; self.f = None
    def quadro(self, q):
        if q < self.q or q - self.q > 120: self.abrir(q)
        while self.q < q:
            b = self.pr.stdout.read(W * H * 3)
            if len(b) < W * H * 3: break
            self.f = np.frombuffer(b, np.uint8).reshape(H, W, 3); self.q += 1
        return self.f
    def fechar(self):
        self.pr.kill(); self.pr.wait()

import cv2
PILL = np.zeros((H, W), np.float32)
cv2.rectangle(PILL, (570, 14), (687, 50), 1.0, -1); cv2.circle(PILL, (570, 32), 18, 1.0, -1); cv2.circle(PILL, (687, 32), 18, 1.0, -1)
PILL = cv2.GaussianBlur(PILL, (0, 0), 0.7)[..., None]
REF_Q = int(round(2153.3 * FPS)); FADE = (int(round(2153.7 * FPS)), int(round(2156.2 * FPS))); _ref = [None]
def corrige_fade_selo(fr, q):
    """fim do b-roll antes do close: fade p/ preto em que o selo_live nao pegou (EN VIVO). Cola o LIVE do quadro REF escurecido."""
    if not (FADE[0] <= q < FADE[1]): return fr
    if _ref[0] is None: _ref[0] = ler(BASE, (REF_Q - 0.5) / FPS, 1)[0].astype(np.float32)
    r = _ref[0]; k = float(fr[100:600].mean()) / max(1.0, float(r[100:600].mean()))
    o = fr.copy(); o[20:76, 86:254] = np.clip(r[20:76, 86:254] * min(1.0, k), 0, 255).astype(np.uint8); return o
def zoom_sem_selo(fr):
    z = cv2.resize(fr, None, fx=1.12, fy=1.12, interpolation=cv2.INTER_LANCZOS4)
    x0 = (z.shape[1] - W) // 2
    return z[z.shape[0] - H:, x0:x0 + W].copy()
PATCH = {}
for pp in (M / "residuo" / "patches").glob("*.npz") if (M / "residuo" / "patches").exists() else []:
    PATCH[int(pp.stem)] = pp
_pc = {}
def aplica_patch(fr, q, tol=0):
    cand = [q + d for d in sorted(range(-tol, tol + 1), key=abs) if q + d in PATCH]
    if not cand: return fr
    qq = cand[0]
    if qq not in _pc:
        if len(_pc) > 60: _pc.clear()
        z = np.load(PATCH[qq]); _pc[qq] = (int(z["y0"]), z["al"], z["px"])
    y0, al, px = _pc[qq]; o = fr.copy(); h = px.shape[0]
    a = al[..., None].astype(np.float32) / 255.0
    o[y0:y0 + h] = np.clip(px * a + o[y0:y0 + h] * (1 - a), 0, 255).astype(np.uint8); return o

def fonte(F):
    tn = F / FPS
    for c in COB:
        if round(c["novo_ini"] * FPS) <= F < round(c["novo_fim"] * FPS):
            return ("cob", c, int(round((c["src_ini"] + tn - c["novo_ini"]) * FPS)))
    for a, b, i in CLIPS:
        if a <= F < b: return ("lip", i, F - a)
    return ("base", None, int(round(novo2orig(tn) * FPS)))

out = M / "blocos" / (f"teste_{k0}.mp4" if TESTE else f"bl{BL:02d}.mp4"); out.parent.mkdir(exist_ok=True)
vf = (f"setpts=PTS+{k0 / FPS:.5f}/TB,ass=legenda_de.ass:fontsdir=fonts,setpts=PTS-STARTPTS,"
      "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p")
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-g", "60", "-pix_fmt", "yuv420p", "-an", str(out)],
                       stdin=subprocess.PIPE, cwd=str(M))
base = None; lips = {}; cobs = {}; log = []; ultimo_ok = None
GLITCH = set()
for a, b in [(1115.133, 1115.233), (1484.1, 1484.2)]:  # s do video final (blackdetect)
    GLITCH |= set(range(int(round(a * FPS)), int(round(b * FPS))))
t0 = time.time(); ult = None
for k in range(k0, k1):
    F = F0 + k
    tp, ref, q = fonte(F)
    if tp == "base":
        if base is None: base = Leitor(BASE, q)
        fr = aplica_patch(corrige_fade_selo(base.quadro(q), q), q)
    elif tp == "lip":
        if ref not in lips:
            for v in lips.values(): v.fechar()
            lips = {ref: Leitor(M / "comp" / f"{ref}.mp4")}
        fr = lips[ref].quadro(q)
        fr = aplica_patch(fr, int(round(novo2orig(F / FPS) * FPS)), tol=3)
    else:
        key = id(ref)
        if key not in cobs: cobs = {key: Leitor(BASE, q)}
        fr = aplica_patch(cobs[key].quadro(q), q)
        if ref.get("zoom"):
            fr = zoom_sem_selo(fr)
        else:  # contador do momento (o b-roll vem de outro trecho, com outro numero)
            qb = int(round(novo2orig(F / FPS) * FPS))
            if base is None: base = Leitor(BASE, qb)
            und = base.quadro(qb)
            fr = np.clip(und.astype(np.float32) * PILL + fr.astype(np.float32) * (1 - PILL), 0, 255).astype(np.uint8)
    if (tp, ref if tp != "cob" else ref["novo_ini"]) != ult:
        log.append([k, round(k / FPS, 3), tp, ref if tp != "cob" else ref["broll"], q]); ult = (tp, ref if tp != "cob" else ref["novo_ini"])
    if k in GLITCH and ultimo_ok is not None:
        fr = ultimo_ok  # quadros pretos soltos que ja vinham do original
    else:
        ultimo_ok = fr
    if k < 9:
        fr = (fr.astype(np.float32) * (k / 9.0)).astype(np.uint8)
    enc.stdin.write(fr.tobytes())
    if (k - k0) % 900 == 899:
        el = time.time() - t0; done = k - k0 + 1
        print(f"bloco {BL} [{done}/{k1 - k0}] {done / el:.1f} q/s falta ~{(k1 - k0 - done) / (done / el) / 60:.1f} min", flush=True)
enc.stdin.close(); enc.wait()
json.dump(log, open(M / "blocos" / (f"teste_{k0}_fontes.json" if TESTE else f"bl{BL:02d}_fontes.json"), "w"), ensure_ascii=False)
print("ok", BL, k1 - k0, round(time.time() - t0), "s", flush=True)
