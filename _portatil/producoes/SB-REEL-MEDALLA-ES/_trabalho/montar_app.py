# -*- coding: utf-8 -*-
"""SB Medalla MOTORISTA DE APP (copia do montar_v2.py; narracao em taxi/). Base: v2 (narração nova, sem moldura, sem quadro segurado).
Linha do tempo: narração v2 (voz/v2/narracao_completa) em tempo t; saída T = S(t):
  + G=2,7 s de salão cheio em t=11,75; - pausas cortadas (jump cuts na selfie; pausa longa sob b-roll).
O rosto do sacerdote só aparece em trechos de fala (as pausas caem em b-roll), sem retoque de boca.
Rodar em _trabalho:  python montar_v2.py [--so-audio] [--so-final]  ->  mont2/master.mp4
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

AQ = Path(__file__).resolve().parent
M = AQ / "mont_app"; M.mkdir(exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS")
GR = AQ / "graficos"; AV = AQ / "avatar2"; TK = AQ / "takes"; VZ = AQ / "app"
SAIDA = M / "master.mp4"
FPS = 30
C, G = 11.80, 2.70
TL = json.loads((VZ / "timeline.json").read_text())
D = TL["desl"]                              # deslocamento da narração depois de "taxi."
SAC_OFF = TL["sacerdote_offset"]
NARR_FIM = TL["total"] + 0.15
REMOV = [(15.80, 16.03), (18.72, 19.12), (26.89 + D, 27.15 + D), (55.95 + D, 56.55 + D)]
SAC_A_FIM = 21.25
SELFIE = VZ / "selfie_app.mp4"
SAC_A, SAC_B = AV / "sacA_high.mp4", AV / "sacB_high.mp4"
ROSTO_SELF = (540, 790)
ROSTO_SAC = (558, 650)
NOITE, DIA = VZ / "app_noite.mp4", VZ / "app_dia.mp4"


def S(t):
    """tempo da narração -> tempo de saída (quantizado em quadros)."""
    x = t + (G if t >= C - 1e-9 else 0.0)
    for a, b in REMOV:
        if t >= b - 1e-9:
            x -= (b - a)
        elif t > a:
            x -= (t - a)
    return int(x * FPS + 0.5) / FPS


def brv(n):
    return next(p for p in BR.glob(f"SB-BRV-{n} *KLING25.mp4") if "REPROV" not in p.name)


# (t_ini, t_fim) em tempo de NARRAÇÃO; "gap" usa T direto
EDL = [
    ("take", 0.0, 6.30, dict(src=NOITE, ss=0.0, interp=True)),
    ("take", 6.30, C, dict(src=NOITE, ss=0.0, zoom=1.15, centro=(480, 860), interp=True)),
    ("gap", None, None, dict(src=DIA, ss=0.0)),
    ("selfie", C, 15.80, dict(zoom=1.0)),
    ("selfie", 16.03, 18.72, dict(zoom=1.13)),
    ("selfie", 19.12, 20.38 + D, dict(zoom=1.0)),
    ("take", 20.38 + D, 22.35 + D, dict(src=brv(19), ss=1.0)),
    ("selfie", 22.35 + D, 26.89 + D, dict(zoom=1.13)),
    ("selfie", 27.15 + D, 31.61, dict(zoom=1.0)),
    ("take", 31.61, SAC_OFF, dict(src=DIA, ss=1.3)),
    ("sac", SAC_OFF, 38.66 + D, dict(zoom=1.0)),
    ("take", 38.66 + D, 40.66 + D, dict(src=brv(22), ss=1.0)),
    ("take", 40.66 + D, 43.88 + D, dict(src=brv("01"), ss=0.6)),
    ("sac", 43.88 + D, 47.06 + D, dict(zoom=1.12)),
    ("take", 47.06 + D, 50.53 + D, dict(src=brv("03"), ss=0.8)),
    ("sac", 50.53 + D, 52.72 + D, dict(zoom=1.0)),
    ("take", 52.72 + D, 58.38 + D, dict(src=brv(29), ss=0.0)),
    ("take", 58.38 + D, 60.40 + D, dict(src=brv("02"), ss=1.5)),
    ("sac", 60.40 + D, 63.10 + D, dict(zoom=1.12)),
    ("take", 63.10 + D, 64.90 + D, dict(src=brv(15), ss=1.5)),
    ("sac", 64.90 + D, 67.70 + D, dict(zoom=1.0)),
    ("take", 67.70 + D, NARR_FIM, dict(src=brv(50), ss=1.0)),
]
TOTAL = S(NARR_FIM)
CTA1 = S(53.29 + D)     # "Toca Más Información"
CTA2 = S(64.93 + D)     # "Toca el botón Ver más"


def janelas():
    out = []
    for tipo, a, b, kw in EDL:
        if tipo == "gap":
            out.append((tipo, S(C) - G, S(C), a, b, kw))
        else:
            out.append((tipo, S(a) if a > 0 else 0.0, C if abs(b - C) < 1e-9 else S(b), a, b, kw))
    return out


def run(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
    if r.returncode:
        print(" ".join(map(str, cmd))[:3000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def crop_zoom(z, centro, W=1080, H=1920):
    if z <= 1.0:
        return ""
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    x = int(min(max(centro[0] - cw / 2, 0), W - cw)); y = int(min(max(centro[1] - ch / 2, 0), H - ch))
    return f"crop={cw}:{ch}:{x}:{y},"


TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]


def render(i, tipo, T0, T1, a, kw):
    out = M / f"seg_{i:02d}.mp4"
    n = round(T1 * FPS) - round(T0 * FPS)
    base = "scale=1080:1920:flags=lanczos,setsar=1"
    if tipo in ("take", "gap"):
        dur_src = 5.0 - kw.get("ss", 0.0)
        vel = min(1.0, max(0.5, dur_src / (n / FPS)))      # desacelera só se o take não cobrir
        fr = "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if (kw.get("interp") or vel < 0.97) else "fps=30,"
        vf = f"setpts=(PTS-STARTPTS)/{vel:.4f}," + fr + crop_zoom(kw.get("zoom", 1.0), kw.get("centro", (540, 960))) + base
        inp = ["-ss", f"{kw['ss']:.3f}", "-i", str(kw["src"])]
    elif tipo == "selfie":
        loc = a - 11.75   # a selfie do HeyGen começa em 11,75 s da narração
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SELF) + base
        inp = ["-ss", f"{loc:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(SELFIE)]
    else:
        loc = a - SAC_OFF
        src, l0 = (SAC_A, loc) if loc < SAC_A_FIM else (SAC_B, loc - SAC_A_FIM)
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SAC) + base
        inp = ["-ss", f"{l0:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(src)]
    vf += ",tpad=stop_mode=clone:stop_duration=1,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", *inp, "-vf", vf, "-frames:v", str(n), "-an", "-r", "30", "-c:v", "libx264",
         "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", "-x264-params", "keyint=60", *TAGS, str(out)])
    return out, n, vel if tipo in ("take", "gap") else 1.0


def audio():
    SR = 48000

    def load(p, af=None):
        cmd = ["ffmpeg", "-v", "error", "-i", str(p)] + (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
        return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()

    voz = load(VZ / "narracao_completa.mp3")
    voz = np.pad(voz, ((0, int(NARR_FIM * SR) - len(voz) + 10), (0, 0)))
    reza = load(VZ / "narracao_completa.mp3", f"atrim=0:{C},aecho=0.8:0.5:45|95:0.22|0.12")[:int(C * SR)]
    partes = [reza, np.zeros((int(round(G * FPS)) * SR // FPS, 2), np.float32)]
    cortes = [C] + [x for ab in REMOV for x in ab] + [NARR_FIM]
    f = int(0.008 * SR)
    for k in range(0, len(cortes), 2):
        a, b = cortes[k], cortes[k + 1]
        seg = voz[int(a * SR):int(b * SR)].copy()
        seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]
        partes.append(seg)
    out_v = np.concatenate(partes)
    n = int(round(TOTAL * SR))
    out_v = np.pad(out_v, ((0, max(0, n - len(out_v))), (0, 0)))[:n]
    # confere sincronia: cada palavra deve cair no mesmo T que a legenda usa
    tr = load(AQ / "audio" / "trilha_v2.wav")
    tr = np.pad(tr, ((0, max(0, n - len(tr))), (0, 0)))[:n]
    t = np.arange(n) / SR
    g0, g1 = S(C) - G, S(C)
    db = np.zeros(n)
    x = np.clip(np.minimum((t - (g0 - 0.6)) / 0.9, (g1 + 0.8 - t) / 1.2), 0, 1)
    db += 9 * x
    db += 3 * np.clip((t - CTA1) / 1.5, 0, 1)
    mix = out_v + tr * (10 ** (db / 20))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af",
             "loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-2.5:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']},"
          f"alimiter=limit=0.68:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", af,
         "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", str(M / "mix.wav")])
    raw.unlink()
    print("audio ok", js["input_i"])


def final():
    run([sys.executable, str(AQ / "legenda_app.py")])
    fonts = M / "fonts"
    if not fonts.exists():
        fonts.mkdir()
        for fz in (AQ / "fonts").glob("*.ttf"):
            (fonts / fz.name).write_bytes(fz.read_bytes())
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    pngs = [("titulo_gancho.png", 0, 6.30), ("cta_setas.png", CTA1, TOTAL), ("cta_txt_masinfo.png", CTA1, CTA2),
            ("cta_txt_vermas.png", CTA2, TOTAL), ("selo_ficticio.png", 0, TOTAL)]
    fc = []
    for k, (p, a, b) in enumerate(pngs):
        ins += ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL + 1:.3f}", "-i", str(GR / p)]
        fc.append(f"[{k + 2}:v]format=rgba[p{k}]")
    fc.append("[0:v]ass=leg_v2.ass:fontsdir=fonts[l]"); ult = "[l]"
    for k, (p, a, b) in enumerate(pngs):
        en = "" if (a <= 0 and b >= TOTAL) else f":enable='between(t,{a:.3f},{b - 0.001:.3f})'"
        fc.append(f"{ult}[p{k}]overlay=0:0:format=auto{en}[o{k}]"); ult = f"[o{k}]"
    fc.append(f"{ult}format=yuv420p[v]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "1:a", "-af", "apad",
         "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAGS,
         "-r", "30", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
         "-t", f"{TOTAL:.3f}", str(SAIDA)], cwd=M)
    print("final ok", SAIDA, TOTAL)


if __name__ == "__main__":
    J = janelas()
    for (_, a0, b0, *_), (_, a1, *_) in zip(J, J[1:]):
        assert abs(b0 - a1) < 1e-6, (b0, a1)
    mapa = [dict(i=i, tipo=t, T_ini=round(A, 3), T_fim=round(B, 3), narr_ini=a, narr_fim=b,
                 fonte=Path(str(kw.get("src", SELFIE if t == "selfie" else "sacerdote"))).name)
            for i, (t, A, B, a, b, kw) in enumerate(J)]
    (M / "mapa_cenas.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1), encoding="utf-8")
    (M / "tempos.json").write_text(json.dumps({"total": TOTAL, "cta1": CTA1, "cta2": CTA2, "C": C, "G": G,
                                               "remov": REMOV}, indent=1), encoding="utf-8")
    if "--so-audio" not in sys.argv and "--so-final" not in sys.argv:
        lista, tot = [], 0
        for i, (t, A, B, a, b, kw) in enumerate(J):
            out, n, vel = render(i, t, A, B, a, kw); lista.append(out); tot += n
            print(f"[{i + 1}/{len(J)}] {t:6s} {A:6.2f}-{B:6.2f} vel {vel:.2f}", flush=True)
        assert tot == round(TOTAL * FPS), (tot, TOTAL * FPS)
        (M / "lista.txt").write_text("".join(f"file '{p.name}'\n" for p in lista), encoding="utf-8")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(M / "lista.txt"), "-c", "copy", str(M / "corpo.mp4")])
    if "--so-final" not in sys.argv:
        audio()
    if "--so-audio" not in sys.argv:
        final()
