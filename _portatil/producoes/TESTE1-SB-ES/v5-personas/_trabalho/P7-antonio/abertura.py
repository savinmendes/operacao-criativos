# -*- coding: utf-8 -*-
"""Abertura P7 (janela do post 720x840, 30 fps): take HeyGen Video 1 da briga (banco) com
- câmera lenta 0,84x em 0-4,3 s do take (ação sem fala: caixa ri, rasga o papel da pensão e joga no balcão) para caber a fala da reportera;
- punch-in 130 % em 0-2,0 s;
- REPORTERA em PiP (chroma, HeyGen R00, acelerada 1,04x junto com o áudio) na caixa (0,300,304,540) com fade de saída;
- áudio: ambiente do take (lento com atempo), voz do caixa nativa, fala do Antonio trocada por STS (Pa Gabriel) + fundo demucs.
Saída: mont/ab.mp4 (sem áudio) + mont/ab.wav + mont/ab.json (palavras no tempo da abertura)."""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; M = AQ / "mont"; M.mkdir(exist_ok=True); W = AQ / "w"
TAKE = AQ / "takes" / "hv_briga_v1.mp4"; HG = AQ / "takes" / "hg_R00.mp4"
FPS, SR, WW, WH = 30, 48000, 720, 840
K, CUT = 0.84, 4.30            # câmera lenta até CUT s do take
SPR = 1.04                     # reportera acelerada
PIP = dict(x=0, y=300, w=304, h=540, xc=284); NFADE = 5
Z, ZC, ZATE = 1.30, (470, 330), 2.0
STS_INI = 7.2                  # Antonio começa a falar depois daqui (fala trocada por STS)
FIM_SRC = 11.54


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=0.0, t=None, extra=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p)] + (["-af", extra] if extra else []) + \
          ["-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
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
    Mx = np.float32([[Z, 0, -x0 * Z], [0, Z, -y0 * Z]])
    return cv2.warpAffine(f, Mx, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def t_out(ts):           # tempo do take -> tempo da abertura
    return ts / K if ts <= CUT else CUT / K + (ts - CUT)


def main():
    D = t_out(FIM_SRC)
    base = W / "ab_base.mp4"          # take reamostrado: lento até CUT, 30 fps, 720x960 -> recorte 840 (y0=40)
    fc = (f"[0:v]split[a][b];[a]trim=0:{CUT},setpts=(PTS-STARTPTS)/{K}[s];[b]trim={CUT}:{FIM_SRC},setpts=PTS-STARTPTS[n];"
          f"[s][n]concat=n=2:v=1,fps={FPS},scale=720:960:flags=lanczos,crop=720:840:0:40[v]")
    run(["ffmpeg", "-v", "error", "-y", "-i", TAKE, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", base])
    fr = list(quadros(base, 0, None, WW, WH)); N = min(len(fr), int(round(D * FPS)))
    t30 = W / "r00_30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", HG, "-vf", f"setpts=PTS/{SPR},fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30, 0, None, 720, 1280)]
    R0 = json.loads((AQ / "voz" / "R00.json").read_text(encoding="utf-8"))
    fala_fim = R0["palavras"][-1]["fim"] / SPR
    NP = min(len(tk), int(round((fala_fim + 0.12) * FPS)) + NFADE); Q_SAI = NP - NFADE
    out = []
    for q in range(N):
        o = fr[q]
        if q < round(ZATE * FPS): o = zoom(o)
        if q < NP:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; hh = min(h, WH - y0)
            A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
            if q >= Q_SAI: A *= 1 - (q - Q_SAI + 1) / (NFADE + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-frames:v", str(N), str(M / "ab.mp4")], stdin=subprocess.PIPE)
    for f in out: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()
    # ---------------- áudio
    Dn = N / FPS; n = int(round(Dn * SR)); amb = np.zeros((n, 2), np.float32)
    a1 = load(TAKE, 0.0, CUT, f"atempo={K}")                           # ação lenta (ambiente)
    a2 = load(TAKE, CUT, STS_INI - CUT)                                # caixa (nativo)
    s0 = int(round(CUT / K * SR)); amb[:min(len(a1), n)] += a1[:n]
    xf = int(0.03 * SR); a2[:xf] *= np.linspace(0, 1, xf)[:, None]
    m2 = min(len(a2), n - s0); amb[s0:s0 + m2] += a2[:m2]
    s1 = int(round(t_out(STS_INI) * SR))
    voz = load(AQ / "voz" / "sts" / "antonio_brig_sts.wav"); fundo = load(AQ / "voz" / "sts" / "antonio_brig_sts_fundo.wav")
    ref = load(TAKE, STS_INI, FIM_SRC - STS_INI)
    voz *= 10 ** ((lufs(ref) + 1.0 - lufs(voz)) / 20)                 # mesma altura da fala original (+1 dB)
    seg = voz[:len(fundo)] + fundo[:len(voz)]; seg[:xf] *= np.linspace(0, 1, xf)[:, None]
    m3 = min(len(seg), n - s1); amb[s1:s1 + m3] += seg[:m3]
    amb *= 10 ** ((-16 - lufs(amb)) / 20)
    t = np.arange(n) / SR; duck = fala_fim + 0.05
    amb *= (10 ** (np.interp(t, [0, duck, duck + 0.3, 1e9], [-6, -6, 0, 0]) / 20)).astype(np.float32)[:, None]
    v = load(AQ / "voz" / "R00.wav", extra=f"atempo={SPR}"); v *= 10 ** ((-15 - lufs(v)) / 20); m = min(len(v), n); amb[:m] += v[:m]
    k = int(0.12 * SR); amb[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = W / "ab.f32"; raw.write_bytes(amb.astype(np.float32).tobytes())
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-c:a", "pcm_s16le", M / "ab.wav"]); raw.unlink()
    # ---------------- palavras (tempo da abertura)
    P = [dict(w=p["w"], ini=p["ini"] / SPR, fim=p["fim"] / SPR, quem="R00") for p in R0["palavras"]]
    Wb = json.loads((AQ / "takes" / "hv_briga_v1_whisper.json").read_text(encoding="utf-8"))
    TXT = "Vuelva mañana… o pídale a su Dios que le pague. Joven, yo trabajé toda mi vida. Por favor, no se burle de mí.".split()
    assert len(TXT) == len(Wb), (len(TXT), len(Wb))
    for w_, x in zip(TXT, Wb):
        P.append(dict(w=w_, ini=t_out(x["ini"]), fim=t_out(x["fim"]), quem="CAJERO" if x["ini"] < STS_INI else "ANTONIO"))
    json.dump(dict(dur=Dn, palavras=P, pip_fim=NP / FPS), open(M / "ab.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("ab", N, "quadros", round(Dn, 3), "s; PiP até", round(NP / FPS, 2), "s; caixa fala em", round(t_out(Wb[0]["ini"]), 2))


if __name__ == "__main__":
    main()
