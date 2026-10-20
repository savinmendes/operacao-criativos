# -*- coding: utf-8 -*-
"""Abertura v4 com a REPORTERA em PiP (chroma) falando desde 0:00 por cima da briga (substitui a mulher do react).
Base: abertura_v2/briga_limpa.mp4 (take Seedance sem PiP) + punch-in 130 % da versão (A: resize/crop c=(330,400); B: warpAffine c=(360,400)), 0-2,0 s.
PiP: take HeyGen da reportera (fundo verde) -> 304x540 em (0,300), recorte x<284, sai em fade de 5 quadros depois da fala.
Áudio: som nativo do take (-16 LUFS, -5 dB enquanto ela fala, volta em 0,3 s) + voz R00 (-15 LUFS) desde 0,000; loudnorm -14.
Uso: python compor_reporter.py A|B [take_heygen.mp4]  -> final_A/abertura/react_reporter_A.mp4 | final_B/abertura/react_reporter_B.mp4"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; V3T = AQ.parent; AB = V3T / "abertura_v2"; W = AQ / "w"; W.mkdir(exist_ok=True)
VER = sys.argv[1].upper(); HG = Path(sys.argv[2]) if len(sys.argv) > 2 else AQ / "takes" / "hg_reportera.mp4"
OUTD = V3T / ("final_A" if VER == "A" else "final_B") / "abertura"; OUT = OUTD / f"react_reporter_{VER}.mp4"
VOZ = AQ / "audio" / "R00.wav"; TAKE = AB / "takes" / "seedance_violenta.mp4"
FPS, SR, WW, WH = 30, 48000, 720, 840
PIP = dict(x=0, y=300, w=304, h=540, xc=284)
Z, ZATE = 1.30, 60
FALA_FIM = json.loads((AQ / "audio" / "palavras.json").read_text(encoding="utf-8"))[-1]["fim"]
NFADE = 4                               # PiP some em fade nos 4 últimos quadros do take HeyGen (3,84 s; fala termina 3,71; agressor 3,98)
DUCK_ATE = FALA_FIM + 0.05


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


def alfa(f):          # chroma verde + despill (mesmo do compor_abertura.py)
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def zoom(f):
    if VER == "A":
        CX, CY = 330, 400; sw, sh = round(WW * Z), round(WH * Z)
        z = cv2.resize(f, (sw, sh), interpolation=cv2.INTER_LANCZOS4)
        x0 = int(np.clip(CX * Z - WW / 2, 0, sw - WW)); y0 = int(np.clip(CY * Z - WH / 2, 0, sh - WH))
        return z[y0:y0 + WH, x0:x0 + WW]
    cw, ch = WW / Z, WH / Z; x0 = min(max(360 - cw / 2, 0), WW - cw); y0 = min(max(400 - ch / 2, 0), WH - ch)
    M = np.float32([[Z, 0, -x0 * Z], [0, Z, -y0 * Z]])
    return cv2.warpAffine(f, M, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def audio(N):
    D = N / FPS; n = int(round(D * SR)); mix = np.zeros((n, 2), np.float32)
    s = load(TAKE, 0.0, D); s *= 10 ** ((-16 - lufs(s)) / 20)
    t = np.arange(len(s)) / SR
    s *= (10 ** (np.interp(t, [0, DUCK_ATE, DUCK_ATE + 0.3, 1e9], [-5, -5, 0, 0]) / 20)).astype(np.float32)[:, None]
    mix[:len(s)] += s[:n]
    v = load(VOZ); v *= 10 ** ((-15 - lufs(v)) / 20); m = min(len(v), n); mix[:m] += v[:m]
    k = int(0.25 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = W / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.7:level=false,aresample=48000")
    wav = W / f"mix_{VER}.wav"
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{D:.4f}", "-c:a", "pcm_s16le", wav]); raw.unlink()
    return wav


def main():
    base = list(quadros(AB / "briga_limpa.mp4", 0, None, WW, WH)); N = len(base)
    t30 = W / "hg30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", HG, "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)]
    NP = len(tk); Q_SAI = NP - NFADE
    x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; out = []
    for q, o in enumerate(base):
        if q < ZATE: o = zoom(o)
        if q < NP:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            hh = min(h, WH - y0); A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
            if q >= Q_SAI: A *= 1 - (q - Q_SAI + 1) / (NFADE + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    wav = audio(N)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                           *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, "-frames:v", str(N),
                           str(OUT)], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()
    a = next(quadros(AB / "react_briga.mp4", 150, 1, WW, WH)); b = next(quadros(OUT, 150, 1, WW, WH))
    print(OUT.name, N, "quadros; PiP 0 ..", NP, "; luma q150 orig/novo", round(float(a.mean()), 2), round(float(b.mean()), 2))


if __name__ == "__main__":
    main()
