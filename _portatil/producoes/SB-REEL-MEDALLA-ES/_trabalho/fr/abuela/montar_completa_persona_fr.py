# -*- coding: utf-8 -*-
"""Série COMPLETA FR por persona. Cópia de personas/<slug>/completa/montar_completa_persona.py (ES) adaptada ao francês.
Muda: vozes FR (voz/hook|reza|selfie.mp3 + .palavras.json), selfie HeyGen FR (selfie_final.mp4, começa em SELF_OFF da
selfie.mp3), padre FR (_comum/padre), gráficos FR (_comum/graficos) e legenda FR (legenda_comp2_fr.py).
Iguais ao ES: takes (gancho_amplo/antes/depois/frustrado), B-roll, trilhas, zooms/centros (config_es.json).
Cortes do gancho/selfie/padre recalculados pelas pausas da fala FR (mesma regra do ES: jump cut deixando ~0,2 s).
Rodar nesta pasta:  python montar_completa_persona_fr.py [--plano] [--so-audio] [--so-final]  ->  mont/master.mp4
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

AQ = Path(__file__).resolve().parent                      # fr/<slug>
SLUG = AQ.name
TR = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho")
PE = TR / "personas" / SLUG                                # antes.mp4 / depois.mp4
ES = PE / "completa"                                       # takes ES + trilha_tensao.wav
CF = json.loads((AQ / "config_es.json").read_text(encoding="utf-8"))
FRC = json.loads((AQ / "config_fr.json").read_text(encoding="utf-8"))
M = AQ / "mont"; M.mkdir(exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS")
GR = TR / "fr" / "_comum" / "graficos"; TK = TR / "takes"; PA = TR / "fr" / "_comum" / "padre"; V = AQ / "voz"
SAIDA = M / "master.mp4"
FPS, SR = 30, 48000
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
ROSTO_SELF = tuple(CF["rosto_selfie"])
ROSTO_SAC = (558, 650)
PERS = CF["slug"]


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def jpal(n):
    return json.loads((V / f"{n}.palavras.json").read_text(encoding="utf-8"))


def cortes_pausa(ws, minimo, deixa=0.20):
    """pausas maiores que `minimo` viram jump cut deixando `deixa` s de respiro."""
    out = []
    for a, b in zip(ws, ws[1:]):
        g = b["ini"] - a["fim"]
        if g > minimo:
            out.append((round(a["fim"] + deixa / 2, 3), round(b["ini"] - deixa / 2, 3)))
    return out


# ---------------------------------------------------------------- linha do tempo da narração (t)
W_HOOK = jpal("hook")
HOOK_FIM = W_HOOK[-1]["fim"] + 0.12
W_REZA = jpal("reza")
T_REZA = round(HOOK_FIM + 0.30, 3)
REZA_DUR = W_REZA[-1]["fim"] + 0.15
G0 = round(T_REZA + REZA_DUR + 0.30, 3)   # corte p/ a virada (trilha muda aqui)
T_SELF = round(G0 + 2.50, 3)
PAD_GAP = 0.40

W_SELF = jpal("selfie")
W_PAD = json.loads((PA / "palavras.json").read_text(encoding="utf-8"))
SELF_DUR = W_SELF[-1]["fim"] + 0.15
T_PAD = round(T_SELF + SELF_DUR + PAD_GAP, 3)
PADRE_VID = dur(PA / "padre_parte1.mp4") + dur(PA / "padre_parte2.mp4")
PAD_FIM = min(W_PAD[-1]["fim"] + 0.30, PADRE_VID - 0.04)  # sem quadro segurado no fim
NARR_FIM = T_PAD + PAD_FIM
SELF_OFF = FRC["selfie_off"]              # tempo local da selfie.mp3 onde começa o vídeo HeyGen FR


def cortes_selfie():
    """(do campesino ES) pausas da selfie viram jump cut (deixa 0,22 s). A 1ª frase sempre fecha num corte
    (frustrado -> selfie HeyGen). Trechos menores que 1,2 s não ganham corte."""
    i1 = next(i for i, w in enumerate(W_SELF) if re.search(r"[.!?]$", w["w"]))
    out, ult = [], 0.0
    for i in range(len(W_SELF) - 1):
        a, b = W_SELF[i]["fim"], W_SELF[i + 1]["ini"]
        if i != i1 and (b - a < 0.35 or a - ult < 1.2 or SELF_DUR - b < 1.2):
            continue
        sobra = min(0.22, b - a)
        ra, rb = round(a + sobra / 2, 3), round(b - sobra / 2, 3)
        if rb - ra < 0.02:
            ra, rb = round((a + b) / 2 - 0.01, 3), round((a + b) / 2 + 0.01, 3)
        out.append((ra, rb)); ult = rb
    return out


def plano_padre():
    """Mesmas cenas do padre ES, ancoradas nas mesmas frases da fala FR."""
    ancoras = ["médaille", "lettres", "foi", "prier", "façon", "va", "issues", "fermées", "complète", "lettre", "24", "dessous"]
    corta = [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1]          # onde o ES tinha jump cut
    limpo = lambda w: re.sub(r"[^\w]", "", w.lower())
    idx, k = [], 0
    for anc in ancoras:
        while not (limpo(W_PAD[k]["w"]) == limpo(anc) and (anc == "issues" or re.search(r"[.,…]$", W_PAD[k]["w"]))):
            k += 1
        idx.append(k); k += 1
    bnd, rp = [], []
    for i, c in zip(idx, corta):
        a, b = W_PAD[i]["fim"], W_PAD[i + 1]["ini"]
        if b - a > 0.30 and c:
            rp.append((round(a + 0.13, 3), round(b - 0.12, 3)))
        bnd.append(round((a + b) / 2, 3))
    return bnd, rp


B_PAD, R_PAD = plano_padre()
R_HOOK = cortes_pausa(W_HOOK, 0.35)
R_SELF = cortes_selfie()
assert R_SELF[0][0] < SELF_OFF < R_SELF[0][1], (R_SELF[0], SELF_OFF)
REMOV = sorted(R_HOOK + [(T_SELF + a, T_SELF + b) for a, b in R_SELF] + [(T_PAD + a, T_PAD + b) for a, b in R_PAD])


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


EDL = [
    ("take", 0.0, T_REZA, dict(src=ES / "takes" / "gancho_amplo.mp4", ss=0.0, zoom=CF["gancho_zoom"],
                               centro=tuple(CF["gancho_centro"]), interp=True)),
    ("take", T_REZA, G0, dict(src=PE / "antes.mp4", ss=0.0, zoom=CF.get("antes_zoom", 1.0),
                              centro=tuple(CF.get("antes_centro", (540, 960))))),
    ("take", G0, T_SELF, dict(src=PE / "depois.mp4", ss=0.3)),
    ("take", s(0.0), s(R_SELF[0][0]), dict(src=ES / "takes" / "frustrado.mp4", ss=0.1)),
]
_z = [1.13, 1.0]
for k, (a0, b0) in enumerate(R_SELF):
    fim = s(R_SELF[k + 1][0]) if k + 1 < len(R_SELF) else T_PAD
    EDL.append(("selfie", s(b0), fim, dict(zoom=_z[k % 2])))
b = [0.0] + B_PAD + [None]
PLANO_PAD = [("pad", dict(zoom=1.0)), ("take", dict(src=TK / "medalla.mp4", ss=0.2)), ("pad", dict(zoom=1.0)),
             ("pad", dict(zoom=1.12)), ("take", dict(src=brv(35), ss=0.3)), ("take", dict(src=brv("03"), ss=0.6)),
             ("pad", dict(zoom=1.0)), ("take", dict(src=brv(47), ss=0.3)), ("pad", dict(zoom=1.12)),
             ("take", dict(src=brv(14), ss=1.0)), ("take", dict(src=brv(50), ss=0.5)), ("pad", dict(zoom=1.0)),
             ("pad", dict(zoom=1.12))]
for k, (tipo, kw) in enumerate(PLANO_PAD):
    EDL.append((tipo, p(b[k]), p(b[k + 1]) if b[k + 1] is not None else NARR_FIM, kw))
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
        vf = f"scale=1080:1920,setpts=(PTS-STARTPTS)/{vel:.4f}," + fr + crop_zoom(kw.get("zoom", 1.0), kw.get("centro", (540, 960))) + base
        inp = ["-ss", f"{kw['ss']:.3f}", "-i", str(kw["src"])]
    elif tipo == "selfie":
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SELF) + base
        inp = ["-ss", f"{a - T_SELF - SELF_OFF:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(AQ / "selfie_final.mp4")]
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


def narracao():
    n = int(NARR_FIM * SR) + SR
    out = np.zeros((n, 2), np.float32)
    ws = []
    f = int(0.01 * SR)

    def put(x, t0):
        x = x.copy(); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
        i = int(t0 * SR); out[i:i + len(x)] += x[:n - i]

    hook = lufs_norm(load(V / "hook.mp3"), -18.0)
    put(hook[:int(HOOK_FIM * SR)], 0.0)
    ws += [dict(w, personagem=PERS, parte="hook") for w in W_HOOK]
    # reza sussurrada: volume baixo + reverb (mesmo filtro do ES)
    x = lufs_norm(load(V / "reza.mp3", "highpass=f=180,aecho=0.8:0.5:45|95:0.22|0.12"), -21.0)
    put(x[:int(REZA_DUR * SR)], T_REZA)
    ws += [dict(w, ini=round(w["ini"] + T_REZA, 3), fim=round(w["fim"] + T_REZA, 3), personagem=PERS, parte="reza")
           for w in W_REZA]
    sel = lufs_norm(load(V / "selfie.mp3"), -18.0)
    put(sel, T_SELF)
    ws += [dict(w, ini=round(w["ini"] + T_SELF, 3), fim=round(w["fim"] + T_SELF, 3)) for w in W_SELF]
    pad = load(PA / "padre.mp3")
    put(pad[:int(PAD_FIM * SR)], T_PAD)
    ws += [dict(w, ini=round(w["ini"] + T_PAD, 3), fim=round(w["fim"] + T_PAD, 3), personagem="sacerdote") for w in W_PAD]
    return out[:int(NARR_FIM * SR)], ws


def audio():
    voz, ws = narracao()
    keep, s0 = [], 0.0
    for a, b in REMOV:
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
    g0, g1 = S(G0), S(T_SELF)
    xf = 0.30
    ten = load(ES / "trilha_tensao.wav")
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
    run([sys.executable, str(AQ / "legenda_comp2_fr.py")])
    fonts = M / "fonts"
    if not fonts.exists():
        fonts.mkdir()
        for fz in (TR / "fonts").glob("*.ttf"):
            (fonts / fz.name).write_bytes(fz.read_bytes())
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    t_tit = S(T_REZA)
    pngs = [("titulo_gancho_fr.png", 0, t_tit), ("cta_ensavoirplus_unico_fr.png", CTA, TOTAL), ("selo_ficticio_mini_fr.png", 0, TOTAL)]
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
    (M / "tempos.json").write_text(json.dumps({"total": TOTAL, "cta": CTA, "T_REZA": T_REZA, "G0": G0, "T_SELF": T_SELF,
                                               "T_PAD": T_PAD, "remov": REMOV}, indent=1), encoding="utf-8")
    if "--plano" in sys.argv:
        for j in J: print(j[0], round(j[1], 2), round(j[2], 2), round(j[2] - j[1], 2), Path(str(j[5].get("src", ""))).name)
        print("R_HOOK", R_HOOK, "R_SELF", R_SELF, "R_PAD", R_PAD)
        print("TOTAL", TOTAL, "CTA", CTA, "S(T_REZA)", S(T_REZA), "S(G0)", S(G0), "S(T_SELF)", S(T_SELF), "S(T_PAD)", S(T_PAD)); sys.exit()
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
