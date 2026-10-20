# -*- coding: utf-8 -*-
"""[FR] Cópia de app/completa/montar_completa_persona.py (série COMPLETA ES) para a versão FRANCESA.
Trocas: vozes FR (voz/), selfie HeyGen FR, legenda FR, padre FR e gráficos FR de fr/_comum; R_PAD/EDL do padre
recalculados pelas pausas do padre FR (mesmos b-rolls na mesma ordem, cortes nas mesmas pausas). Takes/trilha iguais.
Série COMPLETA por persona. Cópia adaptada de _trabalho/montar_completa2.py (Medalla COMPLETA v2).
Diferenças: tudo da persona vem de persona.json (na mesma pasta deste script); hook com pausa encurtada;
reza (voz da persona) com reverb; selfie HeyGen começa num offset da selfie.mp3; padre IDÊNTICO ao modelo
(completa/padre/padre_parte*.mp4 + padre.mp3, mesmos b-rolls, mesmo CTA único).
Rodar:  python montar_completa_persona.py [--plano] [--so-audio] [--so-final]  ->  mont/master.mp4
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent                 # pasta completa da persona
TR = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho")
CFG = json.loads((P / "persona.json").read_text(encoding="utf-8"))
M = P / "_tmp" / "mont"; M.mkdir(parents=True, exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS")
GR = TR / "fr" / "_comum" / "graficos"; TK = TR / "takes"
PA = TR / "fr" / "_comum" / "padre"
SAIDA = M / "master.mp4"
FPS, SR = 30, 48000
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
ROSTO_SELF = tuple(CFG["rosto_selfie"])
ROSTO_SAC = (558, 650)
sys.path.insert(0, str(TR / "voz")); import montar_vozes as mv  # noqa


def rp(x):
    q = Path(x)
    return q if q.is_absolute() else (P / q).resolve()


# ---------------------------------------------------------------- vozes da persona
H = CFG["hook"]; RZ = CFG["reza"]; SF = CFG["selfie"]
HOOK_KEEP = H["keep"]                                 # trechos (a,b) do hook.mp3 mantidos, em sequência
HOOK_LEN = sum(b - a for a, b in HOOK_KEEP)
REZA_KEEP = RZ["keep"]                                # trechos (arquivo, a, b)
REZA_LEN = sum(b - a for _, a, b in REZA_KEEP) + 0.12 * (len(REZA_KEEP) - 1)
T_REZA = round(HOOK_LEN + 0.15, 2)
T_REZA_VOZ = T_REZA + 0.10
T_VIR = round(T_REZA_VOZ + REZA_LEN + 0.30, 2)
T_SELF = round(T_VIR + CFG.get("virada_dur", 2.45), 2)
PAD_GAP = 0.40

W_SELF = [dict(w=w["w"], ini=round(w["ini"], 3), fim=round(w["fim"], 3), personagem="persona", parte="selfie")
          for w in mv.palavras(rp(SF["alinhamento"]))]
W_PAD = json.loads((PA / "palavras.json").read_text(encoding="utf-8"))
SELF_DUR = W_SELF[-1]["fim"] + 0.15
T_PAD = round(T_SELF + SELF_DUR + PAD_GAP, 3)
PAD_FIM = W_PAD[-1]["fim"] + 0.30
NARR_FIM = T_PAD + PAD_FIM
SELF_VID_OFF = SF["video_offset"]                     # selfie.mp3 local -> tempo do vídeo HeyGen = local - offset

R_SELF = [tuple(x) for x in SF["cortes"]]
# [FR] sem quadro segurado: se o vídeo HeyGen acaba antes do fim da selfie + PAD_GAP, corta esse resto (vira corte seco p/ o padre)
_vd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(rp(SF["video"]))],
                           capture_output=True, text=True).stdout)
_vfim = SF["video_offset"] + _vd - 0.04
if _vfim < SELF_DUR + PAD_GAP:
    R_SELF.append((round(_vfim, 3), round(SELF_DUR + PAD_GAP, 3)))
R_PAD = [(2.40, 2.58), (6.56, 6.72), (8.04, 8.38), (11.62, 11.97), (16.53, 16.81), (18.70, 19.04),
         (21.95, 22.27), (30.87, 31.15), (34.48, 34.62)]   # padre FR: mesmas pausas do ES
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


CE = CFG["cenas"]


def cena(k, a, b):
    d = dict(CE[k]); d["src"] = rp(d["src"])
    if "centro" in d: d["centro"] = tuple(d["centro"])
    return ("take", a, b, d)


EDL = [cena("gancho", 0.0, T_REZA), cena("reza", T_REZA, T_VIR), cena("virada", T_VIR, T_SELF),
       cena("frustrado", s(0.0), s(SF["frustrado_fim"]))]
for a, b, z in SF["selfie_trechos"]:
    EDL.append(("selfie", s(a), T_PAD if b is None else s(b), dict(zoom=z)))
EDL += [
    ("pad", p(0.0), p(2.38), dict(zoom=1.0)),
    ("take", p(2.38), p(6.74), dict(src=TK / "medalla.mp4", ss=0.2)),
    ("pad", p(6.74), p(8.04), dict(zoom=1.0)),
    ("pad", p(8.38), p(11.62), dict(zoom=1.12)),
    ("take", p(11.62), p(14.00), dict(src=brv(35), ss=0.3)),
    ("take", p(14.00), p(16.84), dict(src=brv("03"), ss=0.6)),
    ("pad", p(16.84), p(18.70), dict(zoom=1.0)),
    ("take", p(18.70), p(22.30), dict(src=brv(47), ss=0.3)),
    ("pad", p(22.30), p(24.85), dict(zoom=1.12)),
    ("take", p(24.85), p(26.40), dict(src=brv(14), ss=1.0)),
    ("take", p(26.40), p(31.18), dict(src=brv(50), ss=0.5)),
    ("pad", p(31.18), p(34.48), dict(zoom=1.0)),
    ("pad", p(34.62), NARR_FIM, dict(zoom=1.12)),
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
        inp = ["-ss", f"{a - T_SELF - SELF_VID_OFF:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(rp(SF["video"]))]
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

    hook = lufs_norm(load(rp(H["audio"])), -18.0)
    wh = mv.palavras(rp(H["alinhamento"]))
    t = 0.0
    for a, b in HOOK_KEEP:
        put(hook[int(a * SR):int(b * SR)], t)
        ws += [dict(w=w["w"], ini=round(w["ini"] - a + t, 3), fim=round(w["fim"] - a + t, 3), personagem="persona", parte="hook")
               for w in wh if w["ini"] >= a - 1e-6 and w["fim"] <= b + 1e-6]
        t += b - a
    t = T_REZA_VOZ
    for arq, a, b in REZA_KEEP:
        rz = load(rp(arq), RZ.get("af", "aecho=0.8:0.5:45|95:0.22|0.12"))
        rz = lufs_norm(rz, RZ.get("lufs", -21.0))
        al = rp(arq).with_suffix("")
        wr = mv.palavras(Path(str(al) + ".alinhamento.json"))
        put(rz[int(a * SR):int(b * SR)], t)
        ws += [dict(w=w["w"], ini=round(w["ini"] - a + t, 3), fim=round(w["fim"] - a + t, 3), personagem="persona", parte="reza")
               for w in wr if w["ini"] >= a - 1e-6 and w["fim"] <= b + 1e-6]
        t += (b - a) + 0.12
    sel = lufs_norm(load(rp(SF["audio"])), -18.0)
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
    g0, g1 = S(T_VIR), S(T_SELF)
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
    run([sys.executable, str(P / "legenda_completa.py")])
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
    fc.append("[0:v]ass=leg.ass:fontsdir=fonts[l]"); ult = "[l]"
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
    (M / "tempos.json").write_text(json.dumps({"total": TOTAL, "cta": CTA, "T_REZA": T_REZA, "T_VIR": T_VIR,
                                               "T_SELF": T_SELF, "T_PAD": T_PAD, "remov": REMOV}, indent=1), encoding="utf-8")
    if "--plano" in sys.argv:
        for j in J: print(j[0], round(j[1], 2), round(j[2], 2), round(j[2] - j[1], 2), Path(str(j[5].get("src", ""))).name)
        print("T_REZA", T_REZA, "T_VIR", T_VIR, "T_SELF", T_SELF, "T_PAD", T_PAD, "TOTAL", TOTAL, "CTA", CTA); sys.exit()
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
