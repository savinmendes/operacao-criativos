# -*- coding: utf-8 -*-
"""Abertura v4-B: briga_limpa (Seedance, sem PiP) com punch-in 130 % centrado no impacto (0 - ZATE s) e a mulher (PiP HeyGen)
+ voz L01 entrando só DEPOIS do impacto (OFF s). Janela 720x840, cor bt601 fixa (comum3). Não escreve fora de final_B/abertura.
Saída: react_briga_B.mp4 (com áudio)."""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; W = AQ / "w"; W.mkdir(exist_ok=True)
AB = AQ.parents[1] / "abertura_v2"; RAIZ = AQ.parents[3]
SRC = AB / "briga_limpa.mp4"; TAKE = AB / "takes" / "seedance_violenta.mp4"
HG = RAIZ / "v2" / "_trabalho" / "react" / "w" / "hg_low.mp4"; VOZ = RAIZ / "_trabalho" / "voz" / "c" / "L01.wav"
FPS, SR, WW, WH = 30, 48000, 720, 840
PIP = dict(x=0, y=300, w=304, h=540, xc=284); NR = 83
Z, ZC, ZATE = 1.30, (360, 400), 2.0       # punch-in: zoom, centro (impacto do murro no carrinho), até (s)
OFF = 0.90                                # mulher (voz + PiP) entra depois do impacto


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=0.0, t=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    raw = W / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    raw.unlink(); return float([x for x in r.stderr.splitlines() if x.strip().startswith("I:")][-1].split()[1])


def alfa(f):
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def zoom(f):
    cw, ch = WW / Z, WH / Z; x0 = min(max(ZC[0] - cw / 2, 0), WW - cw); y0 = min(max(ZC[1] - ch / 2, 0), WH - ch)
    M = np.float32([[Z, 0, -x0 * Z], [0, Z, -y0 * Z]])
    return cv2.warpAffine(f, M, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def main():
    fr = list(quadros(SRC, 0, None, WW, WH)); N = len(fr)
    t30 = W / "hg30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", HG, "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)]
    tk += [tk[-1]] * max(0, NR - len(tk)); q0 = round(OFF * FPS); out = []
    for q, o in enumerate(fr):
        if q < round(ZATE * FPS): o = zoom(o)
        k = q - q0
        if 0 <= k < NR:
            fg, a = alfa(tk[k]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; hh = min(h, WH - y0)
            A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    D = N / FPS; n = int(round(D * SR)); mix = np.zeros((n, 2), np.float32)
    s = load(TAKE, 0.0, D); s *= 10 ** ((-16 - lufs(s)) / 20)
    t = np.arange(len(s)) / SR; da0, da1 = OFF, OFF + 2.6
    s *= (10 ** (np.interp(t, [0, da0 - 0.15, da0, da1, da1 + 0.3, 1e9], [0, 0, -5, -5, 0, 0]) / 20)).astype(np.float32)[:, None]
    mix[:min(len(s), n)] += s[:n]
    v = load(VOZ); v *= 10 ** ((-15 - lufs(v)) / 20); o = int(OFF * SR); m = min(len(v), n - o); mix[o:o + m] += v[:m]
    k = int(0.25 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = W / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.7:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{D:.4f}", "-c:a", "pcm_s16le", W / "mix.wav"]); raw.unlink()
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           "-i", str(W / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                           *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, "-frames:v", str(N), str(AQ / "react_briga_B.mp4")], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait(); print("react_briga_B", N, f"{D:.3f}s")


if __name__ == "__main__":
    main()
