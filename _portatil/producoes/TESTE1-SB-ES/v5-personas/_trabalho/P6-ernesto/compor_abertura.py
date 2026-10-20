# -*- coding: utf-8 -*-
"""Abertura P6 (modelo: v3/_trabalho/v4_reporter_pip/compor_reporter.py): take Seedance (3:4) -> janela 720x840,
zoom 130 % no impacto (rampa), REPORTERA em PiP (chroma) falando R00 desde 0:00 por cima da ação.
Áudio: som nativo do take (-16 LUFS, -6 dB enquanto ela fala) + voz R00 (-15 LUFS); loudnorm -14.
Uso: python compor_abertura.py  (lê cfg_abertura.json) -> takes/abertura.mp4"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; W = AQ / "w"; W.mkdir(exist_ok=True)
C = json.loads((AQ / "cfg_abertura.json").read_text(encoding="utf-8"))
TAKE = AQ / C["take"]; HG = AQ / "takes" / "hg_R00_pip.mp4"; VOZ = AQ / "voz" / "JR0.wav"; OUT = AQ / "takes" / "abertura.mp4"
FPS, SR, WW, WH = 30, 48000, 720, 840
PIP = C.get("pip", dict(x=0, y=300, w=304, h=540, xc=284))
FALA_FIM = json.loads((AQ / "voz" / "JR0.json").read_text(encoding="utf-8"))["palavras"][-1]["fim"]
NFADE = 4


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


def zoom(f, z, cx, cy):
    if z <= 1.0001: return f
    cw, ch = WW / z, WH / z; x0 = min(max(cx - cw / 2, 0), WW - cw); y0 = min(max(cy - ch / 2, 0), WH - ch)
    M = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]])
    return cv2.warpAffine(f, M, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def zfator(t):
    """rampa: 1.0 até z0, sobe a 1.30 em 0,25 s, segura até z1, volta a 1.0 em 0,4 s"""
    z0, z1 = C["zoom_ini"], C["zoom_fim"]
    if t < z0 or t > z1 + 0.4: return 1.0
    if t < z0 + 0.25: return 1 + 0.30 * (t - z0) / 0.25
    if t <= z1: return 1.30
    return 1.30 - 0.30 * (t - z1) / 0.4


def main():
    ini, fim = C["ini"], C["fim"]; N = int(round((fim - ini) * FPS))
    # take -> 30 fps, escala para 720 de largura, recorte vertical cy (0 = topo, 1 = base)
    t30 = W / "take30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", TAKE, "-t", f"{fim - ini + 0.2:.3f}",
         "-vf", f"fps={FPS},scale={WW}:-2:flags=lanczos,crop={WW}:{WH}:0:'(ih-{WH})*{C['cy']}'", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    base = list(quadros(t30, 0, N, WW, WH))
    hg30 = W / "hg30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", HG, "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", hg30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(hg30)]
    NP = min(len(tk), int((FALA_FIM + 0.15) * FPS) + NFADE); Q_SAI = NP - NFADE
    x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; out = []
    for q, o in enumerate(base):
        o = zoom(o, zfator(q / FPS), C["zx"], C["zy"])
        if q < NP:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            hh = min(h, WH - y0); A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
            if q >= Q_SAI: A *= 1 - (q - Q_SAI + 1) / (NFADE + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    # áudio
    D = N / FPS; n = int(round(D * SR)); mix = np.zeros((n, 2), np.float32)
    s = load(TAKE, ini, D); s *= 10 ** ((-16 - lufs(s)) / 20); t = np.arange(len(s)) / SR
    duck = FALA_FIM + 0.05
    s *= (10 ** (np.interp(t, [0, duck, duck + 0.3, 1e9], [-6, -6, 0, 0]) / 20)).astype(np.float32)[:, None]
    mix[:min(len(s), n)] += s[:n]
    v = load(VOZ); v *= 10 ** ((-15 - lufs(v)) / 20); m = min(len(v), n); mix[:m] += v[:m]
    k = int(0.06 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = W / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    wav = W / "abertura_mix.wav"
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-c:a", "pcm_s16le", wav]); raw.unlink()
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
                           *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-frames:v", str(N),
                           str(OUT.with_suffix(".mov"))], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()
    print(OUT.with_suffix(".mov").name, N, "quadros; PiP", NP)


if __name__ == "__main__":
    main()
