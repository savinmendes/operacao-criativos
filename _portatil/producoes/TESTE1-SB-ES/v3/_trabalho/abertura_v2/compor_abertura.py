# -*- coding: utf-8 -*-
"""Abertura v3: react_briga.mp4 (take contínuo Seedance + mulher HeyGen em PiP nos primeiros ~2,8 s, áudio mixado)
e b04/b05/b06 (Kling, sem áudio). Janela 720x840, 30 fps, cor bt601 fixa (comum3).
Config: cfg.json.  Uso: python compor_abertura.py [briga|virada|tudo]"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; T = AQ / "takes"; W = AQ / "w"; W.mkdir(exist_ok=True)
V2R = AQ.parents[2] / "v2" / "_trabalho" / "react"; V1 = AQ.parents[2] / "_trabalho"
HG = V2R / "w" / "hg_low.mp4"; VOZ = V1 / "voz" / "c" / "L01.wav"
assert HG.exists() and VOZ.exists(), (HG, VOZ)
C = json.loads((AQ / "cfg.json").read_text(encoding="utf-8"))
FPS, SR, WW, WH = 30, 48000, 720, 840
PIP = C.get("pip", dict(x=0, y=120, w=405, h=720, xc=378))


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    return r


def dims(p):
    o = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", p]).stdout
    return tuple(int(x) for x in o.strip().split(","))


def janela(src, ini, n, cy=0.5, cx=0.5):
    """quadros do take a partir de ini (s), 30 fps, cover em 720x840 (recorte centrado em cx/cy)."""
    w, h = dims(src); s = max(WW / w, WH / h); sw, sh = round(w * s), round(h * s)
    tmp = W / (Path(src).stem + "_30.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", src, "-vf",
         f"fps={FPS},scale={sw}:{sh}:flags=lanczos,crop={WW}:{WH}:{round((sw - WW) * cx)}:{round((sh - WH) * cy)}",
         "-frames:v", n, "-an", "-c:v", "libx264", "-crf", "8", "-preset", "fast", tmp])
    return list(quadros(tmp, 0, n, WW, WH))


def enc(frames, out, audio=None):
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           *(["-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"] if audio else ["-an"]),
                           *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, "-frames:v", str(len(frames)),
                           "-shortest" if audio else "-y", str(out)], stdin=subprocess.PIPE)
    for f in frames: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()


def alfa(f):
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def load(p, ss=0.0, t=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    raw = W / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    raw.unlink(); return float([x for x in r.stderr.splitlines() if x.strip().startswith("I:")][-1].split()[1])


def env(n, pts):
    """envelope em dB por pontos [(t, dB)] -> ganho linear por amostra."""
    t = np.arange(n) / SR; xs, ys = zip(*pts); return (10 ** (np.interp(t, xs, ys) / 20)).astype(np.float32)[:, None]


def briga():
    b = C["briga"]; src = T / b["arquivo"]; ini, fim = b["ini"], b["fim"]; NS = round((fim - ini) * FPS)
    fr = janela(src, ini, NS, b.get("cy", 0.5), b.get("cx", 0.5))
    pr = C.get("pre"); P = 0
    if pr:   # pré-roll sem fala (Kling first->last frame que TERMINA no quadro 0 do Seedance): últimos P quadros
        P = pr["quadros"]; pf = janela(T / pr["arquivo"], pr["ini"], P + 2, b.get("cy", 0.5), b.get("cx", 0.5))[:P]
        J = pr.get("fundir", 4)   # funde os últimos J quadros do pré-roll no 1º quadro do take (mesmo quadro-alvo)
        for k in range(J):
            a = (k + 1) / (J + 1); i = P - J + k
            pf[i] = cv2.addWeighted(pf[i], 1 - a, fr[0], a, 0)
        fr = pf + fr
    N = len(fr)
    enc(fr, AQ / "briga_limpa.mp4")
    # PiP da mulher
    t30 = W / "hg30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", HG, "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)]
    NR = C["react"]["quadros"]; tk += [tk[-1]] * max(0, NR - len(tk))
    x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; out = []
    for q, o in enumerate(fr):
        if q < NR:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            hh = min(h, WH - y0); A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    # áudio: voz L01 + som do take (abaixado enquanto ela fala)
    D = N / FPS; n = int(round(D * SR)); mix = np.zeros((n, 2), np.float32); off = int(round(P / FPS * SR))
    s = load(src, ini, NS / FPS); g = 10 ** ((b.get("lufs", -16) - lufs(s)) / 20); s *= g
    if b.get("duck_db"):   # take mais baixo enquanto a mulher fala (volta em 0,3 s)
        t = np.arange(len(s)) / SR; da = b.get("duck_ate", 2.6)
        s *= (10 ** (np.interp(t, [0, da, da + 0.3, 1e9], [b["duck_db"], b["duck_db"], 0, 0]) / 20)).astype(np.float32)[:, None]
    mix[off:off + len(s)] += s[:n - off]
    if P:   # ambiente do pré-roll = cauda silenciosa do próprio take (rua/murmúrio), com o mesmo ganho
        amb = load(src, pr["amb_ss"], P / FPS + 0.3) * g; m = min(len(amb), off + int(0.3 * SR)); amb = amb[:m]
        k = int(0.3 * SR); amb[-k:] *= np.linspace(1, 0, k)[:, None]; amb[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
        mix[:m] += amb
    v = load(VOZ); v *= 10 ** ((-15 - lufs(v)) / 20); m = min(len(v), n); mix[:m] += v[:m]
    k = int(0.25 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = W / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.7:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{D:.4f}", "-c:a", "pcm_s16le", W / "mix.wav"])
    raw.unlink()
    enc(out, AQ / "react_briga.mp4", W / "mix.wav")
    print("react_briga", N, f"{D:.3f}s")


def virada():
    for k, it in C["virada"].items():
        N = round(it["dur"] * FPS); fr = janela(T / it["arquivo"], it.get("ini", 0.0), N, it.get("cy", 0.5), it.get("cx", 0.5))
        enc(fr, AQ / f"{k}.mp4"); print(k, N)


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    if q in ("briga", "tudo"): briga()
    if q in ("virada", "tudo"): virada()
