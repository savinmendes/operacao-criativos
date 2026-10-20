# -*- coding: utf-8 -*-
"""Abertura P2 Rosa: take Seedance (briga) na janela 720x840 + REPORTERA em PiP (chroma) desde 0:00 + punch-in 130 % no impacto.
Baseado em v3/_trabalho/v4_reporter_pip/compor_reporter.py (mesmo alfa/PiP/ducking), cor bt601 fixa (comum3).
Uso: python abertura.py <fim_s> [zoom_ate_quadro] [cx cy]  -> mont/abertura.mp4 (vídeo+áudio)"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; W = AQ / "mont"; W.mkdir(exist_ok=True)
TAKE = AQ / "takes" / "seedance_slow.mp4"; HG = AQ / "takes" / "hg_R00.mp4"; VOZ = AQ / "audio" / "R00.wav"
FPS, SR, WW, WH = 30, 48000, 720, 840
PIP = dict(x=0, y=300, w=304, h=540, xc=284)
FIM = float(sys.argv[1]); ZATE = int(sys.argv[2]) if len(sys.argv) > 2 else 60
CX, CY = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (400, 400)
Z = 1.30; NFADE = 4
FALA_FIM = json.loads((AQ / "audio" / "itens.json").read_text(encoding="utf-8"))["R00"]["palavras"][-1]["fim"]
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


def alfa(f):
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def zoom(f, z):
    cw, ch = WW / z, WH / z; x0 = min(max(CX - cw / 2, 0), WW - cw); y0 = min(max(CY - ch / 2, 0), WH - ch)
    M = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]])
    return cv2.warpAffine(f, M, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def main():
    N = int(round(FIM * FPS))
    w, h = [int(x) for x in run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", TAKE]).stdout.strip().split(",")]
    s = max(WW / w, WH / h); sw, sh = round(w * s / 2) * 2, round(h * s / 2) * 2
    b30 = W / "briga30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", TAKE, "-vf", f"fps={FPS},scale={sw}:{sh}:flags=lanczos,crop={WW}:{WH}:{(sw - WW) // 2}:{(sh - WH) // 2}",
         "-frames:v", N, "-an", "-c:v", "libx264", "-crf", "8", "-preset", "fast", b30])
    base = list(quadros(b30, 0, N, WW, WH))
    t30 = W / "hg30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", HG, "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)]
    NP = min(len(tk), int(round((FALA_FIM + 0.12) * FPS)) + NFADE); Q_SAI = NP - NFADE
    x0, y0, pw, ph = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; out = []
    for q, o in enumerate(base):
        if q < ZATE:
            zz = Z if q < ZATE - 8 else 1 + (Z - 1) * (ZATE - q) / 8          # volta ao 100 % em 8 quadros
            o = zoom(o, zz)
        if q < NP:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            hh = min(ph, WH - y0); A[y0:y0 + hh, x0:x0 + pw] = a[:hh]; F[y0:y0 + hh, x0:x0 + pw] = fg[:hh]; A[:, PIP["xc"]:] = 0
            if q >= Q_SAI: A *= 1 - (q - Q_SAI + 1) / (NFADE + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    D = N / FPS; n = int(round(D * SR)); mix = np.zeros((n, 2), np.float32)
    sd = AQ / "audio" / "briga_audio.wav"
    s_ = load(sd if sd.exists() else TAKE, 0.0, D); s_ *= 10 ** ((-16 - lufs(s_)) / 20)
    t = np.arange(len(s_)) / SR
    s_ *= (10 ** (np.interp(t, [0, DUCK_ATE, DUCK_ATE + 0.3, 1e9], [-5, -5, 0, 0]) / 20)).astype(np.float32)[:, None]
    mix[:len(s_)] += s_[:n]
    v = load(VOZ); v *= 10 ** ((-15 - lufs(v)) / 20); m = min(len(v), n); mix[:m] += v[:m]
    k = int(0.15 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
    wav = W / "abertura.wav"; raw = W / "ab.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-c:a", "pcm_s16le", wav]); raw.unlink()
    OUT = W / "abertura.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-frames:v", str(N), "-an", str(OUT)], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()
    print(OUT.name, N, "quadros; PiP 0 ..", NP, "fala R00 até", FALA_FIM)


if __name__ == "__main__":
    main()
