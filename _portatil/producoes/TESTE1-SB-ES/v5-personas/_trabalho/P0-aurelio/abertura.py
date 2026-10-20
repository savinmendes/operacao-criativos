# -*- coding: utf-8 -*-
"""Abertura P0: briga Seedance (take único 3:4, áudio nativo) + REPORTERA em PiP (chroma) falando R00 desde 0:00,
punch-in de 130 % nos primeiros ZATE quadros (impacto). Janela 720x840, 30 fps, cor bt601 fixa (comum3).
Uso: python abertura.py <fim_s> [cx cy]  -> takes/abertura.mp4 (+ w/abertura_mix.wav)"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; T = AQ / "takes"; W = AQ / "w"; W.mkdir(exist_ok=True)
BRIGA = T / "briga.mp4"; HG = T / "hg_R00.mp4"; VOZ = AQ / "voz" / "R00.wav"
FPS, SR, WW, WH = 30, 48000, 720, 840
PIP = dict(x=0, y=300, w=304, h=540, xc=284)
FIM = float(sys.argv[1]); CX = float(sys.argv[2]) if len(sys.argv) > 2 else 360; CY = float(sys.argv[3]) if len(sys.argv) > 3 else 400
Z, ZATE, ZRAMPA = 1.30, 138, 14
SLOW_SRC, SLOW_OUT = 2.25, 4.60          # câmera lenta no arranque do crucifixo (a reportera fala por cima)
FALA = json.loads((AQ / "voz" / "R00.json").read_text(encoding="utf-8"))["palavras"]
DUCK_ATE = FALA[-1]["fim"] + 0.05; NFADE = 4


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=0.0, t=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    raw = W / "_ab.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
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


def base_frames(N):
    o = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", BRIGA]).stdout
    w, h = (int(x) for x in o.strip().split(",")); s = max(WW / w, WH / h); sw, sh = round(w * s) // 2 * 2, round(h * s) // 2 * 2
    tmp = W / "briga_30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", BRIGA, "-vf", f"fps={FPS},scale={sw}:{sh}:flags=lanczos,crop={WW}:{WH}:{(sw - WW) // 2}:0",
         "-frames:v", N, "-an", "-c:v", "libx264", "-crf", "8", "-preset", "fast", tmp])
    return list(quadros(tmp, 0, N, WW, WH))


def lenta(fr):
    from comum3 import reamostrar
    q = int(round(SLOW_SRC * FPS)); n1 = int(round(SLOW_OUT * FPS))
    return reamostrar(fr[:q], n1) + fr[q:]


def audio(N):
    D = N / FPS; n = int(round(D * SR)); mix = np.zeros((n, 2), np.float32)
    f = SLOW_SRC / SLOW_OUT
    a1 = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-t", f"{SLOW_SRC:.3f}", "-i", str(BRIGA), "-af", f"aresample={SR},asetrate={int(SR * f)},aresample={SR}",
                                      "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2).copy()
    a1 = a1[:int(SLOW_OUT * SR)]; a2 = load(BRIGA, SLOW_SRC, D - SLOW_OUT)
    s = np.concatenate([a1, a2]); s *= 10 ** ((-16 - lufs(s)) / 20); t = np.arange(len(s)) / SR
    s *= (10 ** (np.interp(t, [0, DUCK_ATE, DUCK_ATE + 0.3, 1e9], [-6, -6, 0, 0]) / 20)).astype(np.float32)[:, None]
    mix[:len(s)] += s[:n]
    v = load(VOZ); v *= 10 ** ((-15 - lufs(v)) / 20); m = min(len(v), n); mix[:m] += v[:m]
    k = int(0.15 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = W / "abmix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    wav = W / "abertura_mix.wav"
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-c:a", "pcm_s16le", wav]); raw.unlink()
    return wav


def main():
    base = lenta(base_frames(int(round(FIM * FPS)))); N = len(base)
    t30 = W / "hg_R00_30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", HG, "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    nfala = int(np.ceil((FALA[-1]["fim"] + 0.12) * FPS))
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)][:nfala]
    NP = len(tk); Q_SAI = NP - NFADE; x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; out = []
    for q, o in enumerate(base):
        if q < ZATE:
            z = Z if q < ZATE - ZRAMPA else 1 + (Z - 1) * (ZATE - q) / ZRAMPA
            o = zoom(o, z)
        if q < NP:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            hh = min(h, WH - y0); A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
            if q >= Q_SAI: A *= 1 - (q - Q_SAI + 1) / (NFADE + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    wav = audio(N)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:a", "pcm_s16le", *ENC_VF, "-c:v", "libx264", "-crf", "12",
                           "-preset", "medium", *ENC_TAG, "-frames:v", str(N), str(T / "abertura.mov")], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()
    print("abertura", N, "quadros, PiP", NP, "quadros")


if __name__ == "__main__":
    main()
