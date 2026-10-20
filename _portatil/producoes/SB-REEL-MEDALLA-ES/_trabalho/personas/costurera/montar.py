# -*- coding: utf-8 -*-
"""Montagem de uma persona da série Medalla (adaptado de _trabalho/montar_app.py; sacerdote idêntico à v2).
Copiado para <slug>/montar.py. Rodar:  python <slug>/montar.py [--mapa] [--so-audio] [--so-final]
Linha do tempo: narração da persona (timeline.json) em tempo t; saída T = S(t): + G s de "depois" em t=C; - pausas (jump cuts)."""
import json, re, shutil, subprocess, sys
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent            # _trabalho/personas/<slug>
TR = P.parent.parent                           # _trabalho
M = P / "mont"; M.mkdir(exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS")
GR = TR / "graficos"; AV = TR / "avatar2"
CFG = json.loads((P / "config.json").read_text(encoding="utf-8"))
SAIDA = M / "master.mp4"
FINAL = TR.parent / CFG["saida"]
FPS = 30
TL = json.loads((P / "timeline.json").read_text())
W = json.loads((P / "narracao_completa.palavras.json").read_text(encoding="utf-8"))
C, G = round(TL["C"] * 30) / 30, 2.70     # C alinhado a quadro
D = TL["desl"]
SAC_OFF = TL["sacerdote_offset"]
SELF0 = TL["selfie_ini"]
NARR_FIM = TL["total"] + 0.15
SAC_A_FIM = 21.25
SELFIE = P / "selfie.mp4"
SAC_A, SAC_B = AV / "sacA_high.mp4", AV / "sacB_high.mp4"
ROSTO_SELF = tuple(CFG["rosto_selfie"])
ROSTO_SAC = (558, 650)
NOITE, DIA = P / CFG.get("antes", "antes.mp4"), P / CFG.get("depois", "depois.mp4")


def brv(n):
    return next(p for p in BR.glob(f"SB-BRV-{n} *KLING25.mp4") if "REPROV" not in p.name)


def limpa(w):
    return re.sub(r"[^\wáéíóúñü]", "", w.lower())


fr = {k: [w for w in W if w.get("fala") == k] for k in ("f1", "f2", "f3", "f4", "f5")}
sel = fr["f3"] + fr["f4"] + fr["f5"]
# frases da selfie e pausas removidas entre elas (jump cut)
frases, cur = [], []
for w in sel:
    cur.append(w)
    if re.search(r"(\.|!|\?|…)$", w["w"]):
        frases.append(cur); cur = []
if cur:
    frases.append(cur)
REMOV, cortes = [], []
for a, b in zip(frases, frases[1:]):
    x0, x1 = a[-1]["fim"] + 0.08, b[0]["ini"] - 0.06
    if x1 - x0 > 0.12:
        REMOV.append((round(x0, 3), round(x1, 3))); cortes.append((round(x0, 3), round(x1, 3)))
    else:
        m = round((a[-1]["fim"] + b[0]["ini"]) / 2, 3); cortes.append((m, m))
REMOV.append((round(55.95 + D, 3), round(56.55 + D, 3)))   # pausa do sacerdote (igual à v2)


def S(t):
    """tempo da narração -> tempo de saída (quantizado em quadros)."""
    x = t + (G if t >= C - 1e-9 else 0.0)
    for a, b in REMOV:
        if t >= b - 1e-9:
            x -= (b - a)
        elif t > a:
            x -= (t - a)
    return int(x * FPS + 0.5) / FPS


# --- EDL (tempo de NARRAÇÃO) ---
t_f2 = fr["f2"][0]["ini"]
T_WIDE = round(t_f2 - 0.5, 3)
EDL = [("take", 0.0, T_WIDE, dict(src=NOITE, ss=0.0, interp=True)),
       ("take", T_WIDE, C, dict(src=NOITE, ss=0.0, zoom=1.15, centro=tuple(CFG.get("centro_antes", (540, 760))), interp=True)),
       ("gap", None, None, dict(src=DIA, ss=0.0))]
ini_p = [C] + [b for a, b in cortes]
fim_p = [a for a, b in cortes]
f4_trans = round(next(w for w in fr["f4"] if limpa(w["w"]).startswith("transmisi"))["ini"] - 0.03, 3)
f4_un = round(next(w for w in fr["f4"] if limpa(w["w"]) == "un")["ini"] - 0.03, 3)
_ip = [i for i, w in enumerate(fr["f5"]) if limpa(w["w"]) == "poco"][-1]
F5_ULT = round(min(fr["f5"][_ip + 1]["ini"] - 0.03, fr["f5"][_ip]["fim"] + 0.12), 3)   # corta p/ o "depois" logo após "poco a poco,"
pecas = []
for k, fra in enumerate(frases):
    a = ini_p[k]; b = fim_p[k] if k < len(fim_p) else F5_ULT
    if fra[0] in fr["f4"] and a < f4_trans < b:
        pecas += [("selfie", a, f4_trans), ("broll", f4_trans, f4_un), ("selfie", f4_un, b)]
    else:
        pecas.append(("selfie", a, b))
z = 0
for tipo, a, b in pecas:
    if tipo == "selfie":
        EDL.append(("selfie", a, b, dict(zoom=(1.0, 1.13)[z % 2]))); z += 1
    else:
        EDL.append(("take", a, b, dict(src=brv(19), ss=1.0)))
EDL.append(("take", F5_ULT, SAC_OFF, dict(src=DIA, ss=1.3)))
EDL += [
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
T_TITULO = S(T_WIDE)


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
        fr_ = "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if (kw.get("interp") or vel < 0.97) else "fps=30,"
        vf = f"setpts=(PTS-STARTPTS)/{vel:.4f}," + fr_ + crop_zoom(kw.get("zoom", 1.0), kw.get("centro", (540, 960))) + base
        inp = ["-ss", f"{kw['ss']:.3f}", "-i", str(kw["src"])]
    elif tipo == "selfie":
        loc = a - SELF0
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

    voz = load(P / "narracao_completa.mp3")
    voz = np.pad(voz, ((0, int(NARR_FIM * SR) - len(voz) + 10), (0, 0)))
    reza = load(P / "narracao_completa.mp3", f"atrim=0:{C},aecho=0.8:0.5:45|95:0.22|0.12")[:int(C * SR)]
    partes = [reza, np.zeros((int(round(G * FPS)) * SR // FPS, 2), np.float32)]
    cortes_a = [C] + [x for ab in REMOV for x in ab] + [NARR_FIM]
    f = int(0.008 * SR)
    for k in range(0, len(cortes_a), 2):
        a, b = cortes_a[k], cortes_a[k + 1]
        seg = voz[int(a * SR):int(b * SR)].copy()
        seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]
        partes.append(seg)
    out_v = np.concatenate(partes)
    n = int(round(TOTAL * SR))
    out_v = np.pad(out_v, ((0, max(0, n - len(out_v))), (0, 0)))[:n]
    tr = load(TR / "audio" / "trilha_v2.wav")
    if len(tr) < n + SR // 2:            # trilha mais curta que o vídeo: desacelera de leve para cobrir
        fator = len(tr) / (n + SR // 2)
        tr = load(TR / "audio" / "trilha_v2.wav", f"atempo={max(0.5, fator):.4f}")
        print("trilha atempo", round(fator, 4))
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
    run([sys.executable, str(P / "legenda.py")])
    fonts = M / "fonts"
    if not fonts.exists():
        fonts.mkdir()
        for fz in (TR / "fonts").glob("*.ttf"):
            (fonts / fz.name).write_bytes(fz.read_bytes())
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    pngs = [("titulo_gancho.png", 0, T_TITULO), ("cta_setas.png", CTA1, TOTAL), ("cta_txt_masinfo.png", CTA1, CTA2),
            ("cta_txt_vermas.png", CTA2, TOTAL), ("selo_ficticio.png", 0, TOTAL)]
    fc = []
    for k, (p, a, b) in enumerate(pngs):
        ins += ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL + 1:.3f}", "-i", str(GR / p)]
        fc.append(f"[{k + 2}:v]format=rgba[p{k}]")
    fc.append("[0:v]ass=leg.ass:fontsdir=fonts[l]"); ult = "[l]"
    for k, (p, a, b) in enumerate(pngs):
        en = "" if (a <= 0 and b >= TOTAL) else f":enable='between(t,{a:.3f},{b - 0.001:.3f})'"
        fc.append(f"{ult}[p{k}]overlay=0:0:format=auto{en}[o{k}]"); ult = f"[o{k}]"
    fc.append(f"{ult}format=yuv420p[v]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "1:a", "-af", "apad",
         "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAGS,
         "-r", "30", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
         "-t", f"{TOTAL:.3f}", str(SAIDA)], cwd=M)
    shutil.copyfile(SAIDA, FINAL)
    print("final ok", FINAL, TOTAL)


if __name__ == "__main__":
    J = janelas()
    for (_, a0, b0, *_), (_, a1, *_) in zip(J, J[1:]):
        assert abs(b0 - a1) < 1e-6, (b0, a1)
    mapa = [dict(i=i, tipo=t, T_ini=round(A, 3), T_fim=round(B, 3), narr_ini=a, narr_fim=b,
                 fonte=Path(str(kw.get("src", SELFIE if t == "selfie" else "sacerdote"))).name, zoom=kw.get("zoom", 1.0))
            for i, (t, A, B, a, b, kw) in enumerate(J)]
    (M / "mapa_cenas.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1), encoding="utf-8")
    (M / "tempos.json").write_text(json.dumps({"total": TOTAL, "cta1": CTA1, "cta2": CTA2, "C": C, "G": G,
                                               "remov": REMOV}, indent=1), encoding="utf-8")
    if "--mapa" in sys.argv:
        for m in mapa:
            print(m)
        print("TOTAL", TOTAL, "REMOV", REMOV)
        sys.exit()
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
