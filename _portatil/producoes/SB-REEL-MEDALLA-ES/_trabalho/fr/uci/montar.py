# -*- coding: utf-8 -*-
"""SB COMPLETA por persona (copia de _trabalho/montar_completa2.py, 14/10/2026).
Le cfg.json desta pasta. Padre, b-rolls, CTA unico, selo mini e trilhas = IDENTICOS ao Medalla COMPLETA.
Narracao (t) = hook firme (hook.mp3) + reza cortada da reza antiga (reverb) + virada sem fala
  + selfie (selfie.mp3: 1a frase sobre o take frustrado, resto no HeyGen) + padre (completa/padre/padre.mp3).
Saida T = S(t): t menos as pausas cortadas (jump cuts na selfie/padre).
Rodar:  python montar.py [--plano] [--so-audio] [--so-final]  ->  mont/master.mp4
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

AQ = Path(__file__).resolve().parent                       # _trabalho/fr/<slug>  (versao FR)
TR = AQ.parents[1]                                        # _trabalho
PP = TR / "personas" / AQ.name                            # takes da persona (iguais ao ES)
CFG = json.loads((AQ / "cfg.json").read_text(encoding="utf-8"))
M = AQ / "mont"; M.mkdir(exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS")
GR = TR / "fr" / "_comum" / "graficos"; TK = TR / "takes"
PA = TR / "fr" / "_comum" / "padre"
SAIDA = M / "master.mp4"
FPS, SR = 30, 48000
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
ROSTO_SELF = tuple(CFG["rosto_selfie"])
ROSTO_SAC = (558, 650)
PERS = CFG["slug"]

sys.path.insert(0, str(TR / "voz")); import montar_vozes as mv  # noqa

# ---------------------------------------------------------------- linha do tempo da narracao (t)
HOOK_FIM = CFG["hook_fim"]
REZA_SRC = AQ / CFG["reza_src"]
REZA = [tuple(x) for x in CFG["reza_cortes"]]            # trechos da reza antiga
T_REZA = round(max(5.80, HOOK_FIM + 0.30), 3)
_REZA_FIM = T_REZA + CFG.get("reza_atraso", 0.15) + sum(b - a for a, b in REZA) + 0.25 * (len(REZA) - 1)
T_VIRA = round(max(10.40, _REZA_FIM + 0.90), 3)
T_SELF = round(T_VIRA + 2.45, 3)
PAD_GAP = 0.40
SELF_HG0 = CFG["selfie_heygen_ini"]                       # inicio do audio enviado ao HeyGen (local selfie)


def _ws_selfie():
    ws = mv.palavras(AQ / "selfie.alinhamento.json")
    return [dict(w, ini=round(w["ini"], 3), fim=round(w["fim"], 3), personagem=PERS, parte="selfie") for w in ws]


W_SELF = _ws_selfie()
W_PAD = json.loads((PA / "palavras.json").read_text(encoding="utf-8"))
SELF_DUR = CFG["self_dur"]
PAD_GAP = max(0.0, min(PAD_GAP, CFG["selfie_mp3_dur"] - SELF_DUR - 0.04))  # sem quadro segurado no fim da selfie
T_PAD = round(T_SELF + SELF_DUR + PAD_GAP, 3)
PAD_FIM = W_PAD[-1]["fim"] + 0.30
NARR_FIM = T_PAD + PAD_FIM

R_SELF = [tuple(x) for x in CFG["r_self"]]
R_PAD = [(2.40, 2.55), (6.58, 6.70), (8.10, 8.34), (11.66, 11.92), (16.56, 16.78), (18.74, 18.98), (21.98, 22.22), (30.90, 31.10), (34.50, 34.60)]  # padre FR
REMOV = [(T_SELF + a, T_SELF + b) for a, b in R_SELF] + [(T_PAD + a, T_PAD + b) for a, b in R_PAD]


def S(t):
    x = t
    for a, b in REMOV:
        if t >= b - 1e-9:
            x -= (b - a)
        elif t > a:
            x -= (t - a)
    return int(x * FPS + 0.5) / FPS


def brv(n):
    return next(p for p in BR.glob(f"SB-BRV-{n} *KLING25.mp4") if "REPROV" not in p.name)


def s(x): return T_SELF + x
def p(x): return T_PAD + x


def _cena(d):
    d = dict(d); d["src"] = PP / d["src"]
    if "centro" in d: d["centro"] = tuple(d["centro"])
    return d


r0 = R_SELF[0]
EDL = [
    ("take", 0.0, T_REZA, _cena(CFG["cena_gancho"])),
    ("take", T_REZA, T_VIRA, _cena(CFG["cena_reza"])),
    ("take", T_VIRA, T_SELF, _cena(CFG["cena_virada"])),
    ("take", s(0.0), s(r0[0]), _cena(CFG["cena_frustrado"])),
]
# selfie: entre os cortes, zoom alternado 1,13 / 1,0 (+ trocas extras sem corte)
bord = [r0[1]] + [x for ab in R_SELF[1:] for x in ab] + [None]
segs = [(bord[i], bord[i + 1]) for i in range(0, len(bord) - 1, 2)]
extra = CFG.get("self_trocas", [])
z = 1.13
for a, b in segs:
    pts = [a] + [e for e in extra if a < e < (b if b is not None else 1e9)] + [b]
    for a1, b1 in zip(pts, pts[1:]):
        EDL.append(("selfie", s(a1), s(b1) if b1 is not None else T_PAD, dict(zoom=z)))
        z = 1.0 if z > 1.0 else 1.13
EDL += [
    ("pad", p(0.0), p(2.40), dict(zoom=1.0)),
    ("take", p(2.40), p(6.70), dict(src=TK / "medalla.mp4", ss=0.2)),
    ("pad", p(6.70), p(8.10), dict(zoom=1.0)),
    ("pad", p(8.34), p(11.66), dict(zoom=1.12)),
    ("take", p(11.66), p(14.00), dict(src=brv(35), ss=0.3)),
    ("take", p(14.00), p(16.78), dict(src=brv("03"), ss=0.6)),
    ("pad", p(16.78), p(18.74), dict(zoom=1.0)),
    ("take", p(18.74), p(22.22), dict(src=brv(47), ss=0.3)),
    ("pad", p(22.22), p(24.95), dict(zoom=1.12)),
    ("take", p(24.95), p(26.55), dict(src=brv(14), ss=1.0)),
    ("take", p(26.55), p(31.10), dict(src=brv(50), ss=0.5)),
    ("pad", p(31.10), p(34.50), dict(zoom=1.0)),
    ("pad", p(34.60), NARR_FIM, dict(zoom=1.12)),
]
TOTAL = S(NARR_FIM)
TOCA = next(w for w in W_PAD if w["w"].lower().startswith("appuie"))["ini"]
CTA = S(p(TOCA))


def janelas():
    return [(tipo, 0.0 if a <= 0 else S(a), S(b), a, b, kw) for tipo, a, b, kw in EDL]


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


def padre_full():
    out = M / "padre_full.mp4"
    if out.exists():
        return out
    partes = sorted(PA.glob("padre_parte*.mp4"))
    lst = M / "padre_lista.txt"
    lst.write_text("".join(f"file '{q.as_posix()}'\n" for q in partes), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-vf", "fps=30,format=yuv420p",
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-an", str(out)])
    return out


def render(i, tipo, T0, T1, a, kw, PADRE):
    out = M / f"seg_{i:02d}.mp4"
    n = round(T1 * FPS) - round(T0 * FPS)
    base = "scale=1080:1920:flags=lanczos,setsar=1"
    vel = 1.0
    if tipo == "take":
        dur_src = 5.0 - kw.get("ss", 0.0)
        vel = min(1.0, max(0.5, dur_src / (n / FPS)))
        fr = "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if (kw.get("interp") or vel < 0.97) else "fps=30,"
        vf = f"setpts=(PTS-STARTPTS)/{vel:.4f}," + fr + crop_zoom(kw.get("zoom", 1.0), kw.get("centro", (540, 960))) + base
        inp = ["-ss", f"{kw['ss']:.3f}", "-i", str(kw["src"])]
    elif tipo == "selfie":
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SELF) + base
        inp = ["-ss", f"{a - T_SELF - SELF_HG0:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(AQ / "selfie_heygen.mp4")]
    else:
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SAC) + base
        inp = ["-ss", f"{a - T_PAD:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(PADRE)]
    vf += ",tpad=stop_mode=clone:stop_duration=1,format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", *inp, "-vf", vf, "-frames:v", str(n), "-an", "-r", "30", "-c:v", "libx264",
         "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", "-x264-params", "keyint=60", *TAGS, str(out)])
    return out, n, vel


def load(path, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)] + (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs_norm(x, alvo):
    import pyloudnorm as pyln
    l = pyln.Meter(SR).integrated_loudness(x.astype(np.float64))
    return (x * 10 ** ((alvo - l) / 20)).astype(np.float32)


def load_af(x, af):
    raw = M / "_tmp.f32"; raw.write_bytes(x.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", af,
                        "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    raw.unlink()
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()


def narracao():
    n = int(NARR_FIM * SR) + SR
    out = np.zeros((n, 2), np.float32)
    ws = []
    f = int(0.01 * SR)

    def put(x, t0):
        x = x.copy(); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
        i = int(t0 * SR); out[i:i + len(x)] += x[:n - i]

    hook = lufs_norm(load(AQ / "hook.mp3"), -18.0)
    put(hook[:int(HOOK_FIM * SR)], 0.0)
    wh = mv.palavras(AQ / "hook.alinhamento.json")
    ws += [dict(w, personagem=PERS, parte="hook") for w in wh if w["fim"] <= HOOK_FIM]
    rz = load_af(lufs_norm(load(REZA_SRC), -20.0), "aecho=0.8:0.5:45|95:0.22|0.12")
    t = T_REZA + CFG.get("reza_atraso", 0.15)
    for a, b in REZA:
        put(rz[int(a * SR):int(b * SR)], t)
        ws += [dict(w, ini=round(w["ini"] - a + t, 3), fim=round(min(w["fim"], b) - a + t, 3), personagem=PERS, parte="reza")
               for w in mv.palavras(AQ / "reza.alinhamento.json") if a <= w["ini"] < b - 0.1]
        t += (b - a) + 0.25
    assert t < T_VIRA + 0.2, t
    sel = lufs_norm(load(AQ / "selfie.mp3"), -18.0)
    put(sel, T_SELF)
    ws += [dict(w, ini=round(w["ini"] + T_SELF, 3), fim=round(w["fim"] + T_SELF, 3)) for w in W_SELF]
    pad = load(PA / "padre.mp3")
    put(pad, T_PAD)
    ws += [dict(w, ini=round(w["ini"] + T_PAD, 3), fim=round(w["fim"] + T_PAD, 3), personagem="sacerdote") for w in W_PAD]
    return out[:int(NARR_FIM * SR)], ws


def audio():
    voz, ws = narracao()
    keep, s0 = [], 0.0
    for a, b in sorted(REMOV):
        keep.append((s0, a)); s0 = b
    keep.append((s0, NARR_FIM))
    f = int(0.008 * SR); partes = []
    for a, b in keep:
        seg = voz[int(a * SR):int(b * SR)].copy()
        seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]
        partes.append(seg)
    out_v = np.concatenate(partes)
    n = int(round(TOTAL * SR))
    out_v = np.pad(out_v, ((0, max(0, n - len(out_v))), (0, 0)))[:n]
    tt = np.arange(n) / SR
    g0, g1 = S(T_VIRA), S(T_SELF)
    xf = 0.30
    ten = load(TR / "audio" / "trilha_tensao.wav")
    esp = load(TR / "audio" / "trilha_esperanca.wav")
    tr = np.zeros((n, 2), np.float32)
    k0 = int((g0 - xf / 2) * SR); k1 = int((g0 + xf / 2) * SR)
    a = ten[:k1].copy(); a = np.pad(a, ((0, max(0, k1 - len(a))), (0, 0)))
    a[k0:k1] *= np.linspace(1, 0, k1 - k0)[:, None]
    tr[:k1] += a
    b = esp[:n - k0].copy()
    b[:k1 - k0] *= np.linspace(0, 1, k1 - k0)[:, None]
    tr[k0:k0 + len(b)] += b
    x = np.clip(np.minimum((tt - g0) / 0.6, (g1 + 1.0 - tt) / 1.2), 0, 1)
    db = 6 * x + 3 * np.clip((tt - CTA) / 1.5, 0, 1)
    mix = out_v + tr * (10 ** (db / 20))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af",
             "loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-2.5:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']},"
          f"alimiter=limit=0.74:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", af,
         "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", str(M / "mix.wav")])
    raw.unlink()
    wT = [dict(w, ini=S(w["ini"]), fim=S(w["fim"])) for w in ws]
    (M / "palavras_T.json").write_text(json.dumps(wT, ensure_ascii=False, indent=1), encoding="utf-8")
    print("audio ok", js["input_i"])


def final():
    run([sys.executable, str(AQ / "legenda.py")])
    fonts = M / "fonts"
    if not fonts.exists():
        fonts.mkdir()
        for fz in (TR / "fonts").glob("*.ttf"):
            (fonts / fz.name).write_bytes(fz.read_bytes())
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    pngs = [("titulo_gancho_fr.png", 0, T_REZA), ("cta_ensavoirplus_unico_fr.png", CTA, TOTAL), ("selo_ficticio_mini_fr.png", 0, TOTAL)]
    fc = []
    for k, (pg, a, b) in enumerate(pngs):
        ins += ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL + 1:.3f}", "-i", str(GR / pg)]
        fc.append(f"[{k + 2}:v]format=rgba[p{k}]")
    fc.append("[0:v]ass=leg_comp2.ass:fontsdir=fonts[l]"); ult = "[l]"
    for k, (pg, a, b) in enumerate(pngs):
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
    (M / "mapa_cenas.json").write_text(json.dumps(
        [dict(i=i, tipo=t, T_ini=round(A, 3), T_fim=round(B, 3), narr_ini=round(a, 3), narr_fim=round(b, 3),
              fonte=Path(str(kw.get("src", t))).name) for i, (t, A, B, a, b, kw) in enumerate(J)],
        ensure_ascii=False, indent=1), encoding="utf-8")
    (M / "tempos.json").write_text(json.dumps({"total": TOTAL, "cta": CTA, "T_SELF": T_SELF, "T_PAD": T_PAD,
                                               "remov": REMOV}, indent=1), encoding="utf-8")
    if "--plano" in sys.argv:
        for j in J: print(j[0], round(j[1], 2), round(j[2], 2), round(j[2] - j[1], 2), Path(str(j[5].get("src", ""))).name, j[5].get("zoom", ""))
        print("TOTAL", TOTAL, "CTA", CTA); sys.exit()
    if "--so-audio" not in sys.argv and "--so-final" not in sys.argv:
        PADRE = padre_full()
        lista, tot = [], 0
        for i, (t, A, B, a, b, kw) in enumerate(J):
            out, nq, vel = render(i, t, A, B, a, kw, PADRE); lista.append(out); tot += nq
            print(f"[{i + 1}/{len(J)}] {t:6s} {A:6.2f}-{B:6.2f} vel {vel:.2f}", flush=True)
        assert tot == round(TOTAL * FPS), (tot, TOTAL * FPS)
        (M / "lista.txt").write_text("".join(f"file '{q.name}'\n" for q in lista), encoding="utf-8")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(M / "lista.txt"), "-c", "copy", str(M / "corpo.mp4")])
    if "--so-final" not in sys.argv:
        audio()
    if "--so-audio" not in sys.argv:
        final()
