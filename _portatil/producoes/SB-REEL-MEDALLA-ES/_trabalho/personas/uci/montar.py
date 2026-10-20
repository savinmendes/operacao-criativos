# -*- coding: utf-8 -*-
"""SB Medalla PERSONA (adaptado de _trabalho/montar_app.py + legenda_app.py). Fica dentro de personas/<slug>/.
Narração: <slug>/narracao_completa.* (build_voz.py). Sacerdote, b-rolls, CTA e selo idênticos à v2/app.
Linha do tempo de saída T = S(t): + G s do "depois" logo após a reza; - pausa do sacerdote (igual à app).
Selfie (HeyGen) sem pausas longas (já apertadas no áudio); cortes secos com zoom 1,0/1,13 nas fronteiras de frase.
Rodar:  python montar.py [--mapa] [--so-audio] [--so-final]  ->  <slug>/mont/master.mp4"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent
TR = P.parent.parent                      # _trabalho
M = P / "mont"; M.mkdir(exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS")
GR = TR / "graficos"; AV = TR / "avatar2"
CFG = json.loads((P / "cfg.json").read_text(encoding="utf-8"))
SAIDA = M / "master.mp4"
FPS = 30
TL = json.loads((P / "timeline.json").read_text())
W = json.loads((P / "narracao_completa.palavras.json").read_text(encoding="utf-8"))
C, G = TL["C"], 2.70
SAC_OFF = TL["sac"]
DS = SAC_OFF - 35.06                      # deslocamento dos tempos v2 do sacerdote
NARR_FIM = TL["total"] + 0.15
REMOV = [(55.95 + DS, 56.55 + DS)]
SAC_A_FIM = 21.25
SELFIE = P / "selfie.mp4"
SAC_A, SAC_B = AV / "sacA_high.mp4", AV / "sacB_high.mp4"
ROSTO_SELF = tuple(CFG.get("rosto_selfie", (540, 820)))
ROSTO_SAC = (558, 650)
ANTES, DEPOIS = P / "antes.mp4", P / "depois.mp4"


def S(t):
    x = t + (G if t >= C - 1e-9 else 0.0)
    for a, b in REMOV:
        if t >= b - 1e-9:
            x -= (b - a)
        elif t > a:
            x -= (t - a)
    return int(x * FPS + 0.5) / FPS


def brv(n):
    return next(p for p in BR.glob(f"SB-BRV-{n} *KLING25.mp4") if "REPROV" not in p.name)


# ---- marcos da selfie a partir das palavras ----
sel = [w for w in W if w.get("parte") == "selfie"]


def meio(i):           # meio da pausa entre sel[i] e sel[i+1]
    return round((sel[i]["fim"] + sel[i + 1]["ini"]) / 2, 3)


fim_frase = [i for i, w in enumerate(sel) if re.search(r"[.!?]$", w["w"])]
i_hasta = next(i for i, w in enumerate(sel) if w["w"].lower().startswith("hasta"))
i_una = i_hasta + 3                       # Hasta que, en | una transmisión en vivo,
i_un = next(i for i in range(i_una, len(sel)) if sel[i]["w"].lower() == "un")
i_poco = next(i for i, w in enumerate(sel) if w["w"].lower().startswith("poco,"))
assert sel[i_una]["w"].lower() == "una", sel[i_una]
f3 = [i for i in fim_frase if i < i_hasta]          # frases da fala 3
cortes3 = [C] + [meio(i) for i in f3[:-1]] + [meio(i_hasta - 1)]
EDL = [("take", 0.0, 6.30, dict(src=ANTES, ss=0.0, interp=True)),
       ("take", 6.30, C, dict(src=ANTES, ss=0.0, zoom=1.15, centro=tuple(CFG["centro_antes"]), interp=True)),
       ("gap", None, None, dict(src=DEPOIS, ss=0.0))]
z = 1.0
for a, b in zip(cortes3, cortes3[1:]):
    EDL.append(("selfie", a, b, dict(zoom=z))); z = 1.13 if z == 1.0 else 1.0
t_br0 = round(sel[i_una]["ini"] - 0.03, 3); t_br1 = meio(i_un - 1)
EDL.append(("selfie", cortes3[-1], t_br0, dict(zoom=z)))
EDL.append(("take", t_br0, t_br1, dict(src=brv(19), ss=1.0)))
f4 = next(i for i in fim_frase if i > i_un)            # "...San Benito."
EDL.append(("selfie", t_br1, meio(f4), dict(zoom=1.13)))
t_dep = round(sel[i_poco + 1]["ini"] - 0.03, 3)
EDL.append(("selfie", meio(f4), t_dep, dict(zoom=1.0)))
EDL.append(("take", t_dep, SAC_OFF, dict(src=DEPOIS, ss=CFG.get("ss_depois2", 1.3))))


def V(x):
    return x + DS


EDL += [
    ("sac", SAC_OFF, V(38.66), dict(zoom=1.0)),
    ("take", V(38.66), V(40.66), dict(src=brv(22), ss=1.0)),
    ("take", V(40.66), V(43.88), dict(src=brv("01"), ss=0.6)),
    ("sac", V(43.88), V(47.06), dict(zoom=1.12)),
    ("take", V(47.06), V(50.53), dict(src=brv("03"), ss=0.8)),
    ("sac", V(50.53), V(52.72), dict(zoom=1.0)),
    ("take", V(52.72), V(58.38), dict(src=brv(29), ss=0.0)),
    ("take", V(58.38), V(60.40), dict(src=brv("02"), ss=1.5)),
    ("sac", V(60.40), V(63.10), dict(zoom=1.12)),
    ("take", V(63.10), V(64.90), dict(src=brv(15), ss=1.5)),
    ("sac", V(64.90), V(67.70), dict(zoom=1.0)),
    ("take", V(67.70), NARR_FIM, dict(src=brv(50), ss=1.0)),
]
TOTAL = S(NARR_FIM)
CTA1 = S(V(53.29))
CTA2 = S(V(64.93))


def janelas():
    out = []
    for tipo, a, b, kw in EDL:
        if tipo == "gap":
            out.append((tipo, S(C) - G, S(C), a, b, kw))
        else:
            out.append((tipo, S(a) if a > 0 else 0.0, round(S(C) - G, 6) if abs(b - C) < 1e-9 else S(b), a, b, kw))
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
    vel = 1.0
    if tipo in ("take", "gap"):
        dur_src = 5.0 - kw.get("ss", 0.0)
        vel = min(1.0, max(0.5, dur_src / (n / FPS)))
        fr = "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if (kw.get("interp") or vel < 0.97) else "fps=30,"
        vf = f"setpts=(PTS-STARTPTS)/{vel:.4f}," + fr + crop_zoom(kw.get("zoom", 1.0), kw.get("centro", (540, 960))) + base
        inp = ["-ss", f"{kw['ss']:.3f}", "-i", str(kw["src"])]
    elif tipo == "selfie":
        loc = a - C
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
    return out, n, vel


def audio():
    SR = 48000

    def load(p, af=None):
        cmd = ["ffmpeg", "-v", "error", "-i", str(p)] + (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
        return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()

    voz = load(P / "narracao_completa.mp3")
    voz = np.pad(voz, ((0, max(0, int(NARR_FIM * SR) - len(voz) + 10)), (0, 0)))
    reza = load(P / "narracao_completa.mp3", f"atrim=0:{C},aecho=0.8:0.5:45|95:0.22|0.12")[:int(C * SR)]
    reza = np.pad(reza, ((0, max(0, int(C * SR) - len(reza))), (0, 0)))
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
    tr = load(TR / "audio" / "trilha_v2.wav")
    tr = np.pad(tr, ((0, max(0, n - len(tr))), (0, 0)))[:n]
    t = np.arange(n) / SR
    g0, g1 = S(C) - G, S(C)
    db = 9 * np.clip(np.minimum((t - (g0 - 0.6)) / 0.9, (g1 + 0.8 - t) / 1.2), 0, 1)
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


# ---------------- legenda (legenda_app.py adaptado) ----------------
def legenda():
    Wl = [dict(w, ini=S(w["ini"]), fim=S(w["fim"])) for w in W]
    CTA_T, Y_CTA, MAXP, MAXC, Y, FS = CTA1, 1330, 3, 16, 1460, 120

    def limpa(w):
        return re.sub(r"[.,;:!?¡¿«»<>…]", "", w).upper()

    def forte(w):
        return bool(re.search(r"[.!?…:;]$", w))

    JUNTA = {("san", "benito"), ("en", "vivo"), ("<<ver", "más"), ("«ver", "más")}
    vis = []
    for w in Wl:
        if vis and (re.sub(r"[^\w<«]", "", vis[-1]["w"].lower()), re.sub(r"[^\w]", "", w["w"].lower())) in JUNTA \
                and not re.search(r"[.,!?]$", vis[-1]["w"]):
            vis[-1] = dict(vis[-1], w=vis[-1]["w"] + " " + w["w"], fim=w["fim"])
        else:
            vis.append(dict(w))
    blocos, cur = [], []
    for w in vis:
        cand = cur + [w]
        txt = " ".join(limpa(x["w"]) for x in cand)
        mud = cur and cur[-1].get("personagem") != w.get("personagem")
        if cur and (len(cand) > MAXP or len(txt) > MAXC or mud):
            blocos.append(cur); cur = [w]
        else:
            cur = cand
        if forte(w["w"]) or (w["w"].endswith(",") and len(cur) >= 2):
            blocos.append(cur); cur = []
    if cur:
        blocos.append(cur)
    fix = []
    for b in blocos:
        if fix and len(b) == 1 and len(fix[-1]) < MAXP and not forte(fix[-1][-1]["w"]) \
                and len(" ".join(limpa(x["w"]) for x in fix[-1] + b)) <= MAXC:
            fix[-1] = fix[-1] + b
        else:
            fix.append(b)
    blocos = fix

    def ts(t):
        return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
            "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: C,Poppins ExtraBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,3,5,40,40,0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    AM, BRc = r"{\c&H54E5FE&}", r"{\c&HFFFFFF&}"
    L, js = [], []
    for i, b in enumerate(blocos):
        ini = b[0]["ini"]
        prox = blocos[i + 1][0]["ini"] if i + 1 < len(blocos) else TOTAL
        fim = min(prox, b[-1]["fim"] + 0.6) if i + 1 < len(blocos) else min(TOTAL, b[-1]["fim"] + 0.8)
        p = [{"w": limpa(x["w"]), "ini": x["ini"]} for x in b]
        js.append({"ini": ini, "fim": fim, "texto": " ".join(x["w"] for x in p)})
        for j, w in enumerate(p):
            a = ini if j == 0 else w["ini"]
            e = p[j + 1]["ini"] if j + 1 < len(p) else fim
            if e <= a:
                continue
            partes = [(AM if jj == j else BRc) + x["w"] for jj, x in enumerate(p)]
            pop = r"{\an5\pos(540,%d)" % (Y_CTA if a >= CTA_T - 0.05 else Y)
            if j == 0:
                pop += r"\fscx80\fscy80\t(0,90,\fscx106\fscy106)\t(90,160,\fscx100\fscy100)"
            pop += "}"
            L.append(f"Dialogue: 0,{ts(a)},{ts(e)},C,,0,0,0,,{pop}{' '.join(partes)}")
    (M / "leg.ass").write_text(head + "\n".join(L) + "\n", encoding="utf-8")
    (M / "leg_blocos.json").write_text(json.dumps(js, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(blocos), "blocos legenda")


def final():
    legenda()
    fonts = M / "fonts"
    if not fonts.exists():
        fonts.mkdir()
        for fz in (TR / "fonts").glob("*.ttf"):
            (fonts / fz.name).write_bytes(fz.read_bytes())
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    pngs = [("titulo_gancho.png", 0, 6.30), ("cta_setas.png", CTA1, TOTAL), ("cta_txt_masinfo.png", CTA1, CTA2),
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
    print("final ok", SAIDA, TOTAL)


if __name__ == "__main__":
    J = janelas()
    for (_, a0, b0, *_), (_, a1, *_) in zip(J, J[1:]):
        assert abs(b0 - a1) < 1e-6, (b0, a1)
    mapa = [dict(i=i, tipo=t, T_ini=round(A, 3), T_fim=round(B, 3), narr_ini=a, narr_fim=b,
                 fonte=Path(str(kw.get("src", SELFIE if t == "selfie" else "sacerdote"))).name, zoom=kw.get("zoom", 1.0))
            for i, (t, A, B, a, b, kw) in enumerate(J)]
    (M / "mapa_cenas.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1), encoding="utf-8")
    (M / "tempos.json").write_text(json.dumps({"total": TOTAL, "cta1": CTA1, "cta2": CTA2, "C": C, "G": G, "remov": REMOV}, indent=1), encoding="utf-8")
    if "--mapa" in sys.argv:
        for m in mapa:
            print(m["i"], m["tipo"], m["T_ini"], m["T_fim"], m["fonte"], m["zoom"])
        sys.exit(0)
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
