# -*- coding: utf-8 -*-
"""Montagem P9 DOÑA LUCÍA (lote Humillación v5) -> v5-personas/SB-ES_HUMILLACION_P9-LUCIA_FICTICIO.mp4 (+ _narracion.txt, _frames.jpg)
Tudo dentro da janela do post (720x840 em y=297, moldura "Fe en Noticias"), selo VIDEO FICTICIO o vídeo todo,
legenda palavra a palavra pelo roteiro, setas TOCA «VER MÁS» do início do CTA até o último quadro.
Uso: python montar.py [--saida x.mp4]"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

AQ = Path(__file__).resolve().parent; V5 = AQ.parents[1]; RAIZ = V5.parent
M = AQ / "mont"; M.mkdir(exist_ok=True); A = AQ / "audio"; TK = AQ / "takes"; IMG = AQ / "img"
G = RAIZ / "_trabalho" / "graficos"; GB = RAIZ / "v3" / "_trabalho" / "final_B"; GL = AQ / "graficos"
TRILHA_TRISTE = GB / "trilha" / "triste_1.mp3"; TRILHA_ESP = GB / "trilha" / "esperanca_1.mp3"
FPS, SR, WW, WH, WY = 30, 48000, 720, 840, 297
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
ARGS = sys.argv[1:]
OUT = Path(ARGS[ARGS.index("--saida") + 1]) if "--saida" in ARGS else V5 / "SB-ES_HUMILLACION_P9-LUCIA_FICTICIO.mp4"
AB = json.loads((M / "abertura.json").read_text())

# ------------------------------------------------------------------ texto do roteiro (ROTEIRO_PERSONAS_v2, P9)
TX = {
    "R00": "Imágenes impactantes: una peluquera fue humillada en su propio salón… por su fe.",
    "B02": "¿Y para esto rezas tanto? ¡Llama a tu Dios a ver si te arregla esto!",
    "B03": "Señora, yo hice lo mejor que pude. Por favor, cálmese.",
    "R01": "Al día siguiente, doña Lucía tenía la agenda llena por dos semanas.",
    "LV1": "Esa noche miré la agenda vacía y pensé en cerrar el salón que me costó toda la vida.",
    "L01": "Mi hermana me mandó la transmisión del padre Juan Méndez. La hice esa misma noche, como él enseña. Al otro día, el teléfono no paró de sonar.",
    "L02": "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche.",
    "L03": "Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito…",
    "L04": "y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?",
    "R02": "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo.",
}
NOME = {"R00": "REPORTERA (en PiP)", "B02": "CLIENTA", "B03": "DOÑA LUCÍA", "R01": "REPORTERA", "LV1": "DOÑA LUCÍA (voz en off)",
        "L01": "DOÑA LUCÍA", "L02": "DOÑA LUCÍA", "L03": "DOÑA LUCÍA", "L04": "DOÑA LUCÍA", "R02": "REPORTERA"}


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:2000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + (["-t", f"{t:.3f}"] if t else []) + \
          ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < int(0.5 * SR): a = np.concatenate([a, np.zeros((int(0.5 * SR) - len(a), 2), np.float32)])
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    raw.unlink(); l = [x for x in r.stderr.splitlines() if x.strip().startswith("I:")]
    v = float(l[-1].split()[1]); return v if v > -70 else -70.0


def fade(a, ms=12):
    n = min(int(ms / 1000 * SR), len(a) // 2)
    if n: a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a


def pal(i):
    return json.loads((A / f"{i}.palavras.json").read_text(encoding="utf-8"))


def com_roteiro(P, txt):
    R = txt.split()
    assert len(R) == len(P), (len(R), len(P), txt)
    return [dict(p, w=r) for p, r in zip(P, R)]


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout.strip())


# ------------------------------------------------------------------ linha do tempo
def plano():
    """lista de planos de vídeo (janela 720x840) e de falas (áudio + palavras no tempo final)"""
    PL, FA = [], []; t = 0.0
    # 1) abertura (take Seedance com câmera lenta + PiP da reportera)
    D = AB["N"] / FPS
    PL.append(dict(id="abertura", src=M / "abertura.mp4", ss=0.0, d=D, kind="pronto"))
    FA.append(dict(id="R00", audio=A / "R00.wav", T0=0.0, ss=0.0, d=dur(A / "R00.wav"), palavras=com_roteiro(pal("R00"), TX["R00"])))
    wh = json.loads((AQ / "voz" / "wh_sts.json").read_text(encoding="utf-8"))
    to = lambda x: x / 0.43 if x <= 2.3 else 2.3 / 0.43 + (x - 2.3)
    W = [dict(w=w["w"], ini=round(to(w["ini"]), 3), fim=round(to(w["fim"]), 3)) for w in wh]
    FA.append(dict(id="B02", audio=None, T0=0.0, palavras=com_roteiro(W[:15], TX["B02"])))
    FA.append(dict(id="B03", audio=None, T0=0.0, palavras=com_roteiro(W[15:], TX["B03"])))
    t = D
    # 2) virada sem fala: mãos com o crucifixo -> cadeira vazia -> 2 clientes -> salão cheio (HeyGen Video 1, 24 fps)
    for nome, ss, d in (("maos", 0.25, 2.6), ("vazio", 0.6, 1.7), ("duas", 0.5, 1.7), ("cheio", 0.5, 2.1)):
        PL.append(dict(id=nome, src=TK / f"v1_{nome}.mp4", ss=ss, d=d, kind="video", broll=nome)); t += d
    T_VIRADA = (D, t)
    # 3) reportera R01 (take HeyGen 4:5 na porta do salão)
    P = com_roteiro(pal("R01"), TX["R01"]); fim = P[-1]["fim"] + 0.25
    PL.append(dict(id="R01", src=TK / "hg_R01s.mp4", ss=0.0, d=fim, kind="video", y=0.35))
    FA.append(dict(id="R01", audio=A / "R01.wav", T0=t, ss=0.0, d=fim, palavras=P)); t += fim
    # 4) voz off LV1 sobre a noite com a agenda vazia (still com zoom lento)
    t += 0.15
    P = com_roteiro(pal("LV1"), TX["LV1"]); d = P[-1]["fim"] + 0.30
    PL.append(dict(id="noite", src=IMG / "noite.png", ss=0, d=d + 0.15, kind="img", broll="noite"))
    FA.append(dict(id="LV1", audio=A / "LV1.wav", T0=t, ss=0.0, d=d, palavras=P)); t += d
    # 5) entrevista: L01 (1ª frase em b-roll: celular à noite), L02..L04 rosto
    zoom = [1.0]
    for k, i in enumerate(("L01", "L02", "L03", "L04")):
        P = com_roteiro(pal(i), TX[i]); hg = TK / f"hg_{i}.mp4"
        a0 = max(0.0, P[0]["ini"] - 0.08); a1 = P[-1]["fim"] + (0.10 if i != "L04" else 0.22)
        d = a1 - a0
        if i == "L01":
            k_ = next(j for j, p in enumerate(P) if p["w"].startswith("Méndez"))
            c = (P[k_]["fim"] + P[k_ + 1]["ini"]) / 2 - a0
            PL.append(dict(id="celular", src=IMG / "celular.png", ss=0, d=c, kind="img", broll="celular"))
            PL.append(dict(id=i, src=hg, ss=a0 + c, d=d - c, kind="video", y=0.20, z=1.0))
        else:
            PL.append(dict(id=i, src=hg, ss=a0, d=d, kind="video", y=0.20, z=1.10 if k % 2 else 1.0))
        FA.append(dict(id=i, audio=A / f"{i}.wav", T0=t - a0, ss=0.0, d=dur(A / f"{i}.wav"), palavras=P)); t += d
    # 6) CTA da reportera (setas do início da fala até o fim; nada é falado depois)
    P = com_roteiro(pal("R02"), TX["R02"]); a0 = max(0.0, P[0]["ini"] - 0.05); fim = min(P[-1]["fim"] + 0.70, dur(TK / "hg_R02s.mp4") - 0.05)
    t += 0.10
    PL.append(dict(id="R02", src=TK / "hg_R02s.mp4", ss=a0, d=fim - a0, kind="video", y=0.35))
    FA.append(dict(id="R02", audio=A / "R02.wav", T0=t - a0, ss=0.0, d=dur(A / "R02.wav"), palavras=P))
    cta_t = t; t += fim - a0
    # quadros inteiros
    q = 0; tt = 0.0
    for p in PL:
        tt += p["d"]; n = round(tt * FPS) - q; p["q0"] = q; p["n"] = n; q += n
    total = q / FPS
    return PL, FA, total, cta_t, T_VIRADA


# ------------------------------------------------------------------ vídeo da janela
def render(p, out):
    n = p["n"]
    if p["kind"] == "pronto":
        v = f"[0:v]fps={FPS},setpts=PTS-STARTPTS"; ins = ["-i", p["src"]]
    elif p["kind"] == "img":
        v = (f"[0:v]scale={WW * 2}:{WH * 2}:force_original_aspect_ratio=increase,crop={WW * 2}:{WH * 2},"
             f"zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={WW}x{WH}:fps={FPS}")
        ins = ["-loop", "1", "-framerate", str(FPS), "-t", f"{n / FPS + 0.3:.3f}", "-i", p["src"]]
    else:
        y = p.get("y", 0.5); z = p.get("z", 1.0)
        v = (f"[0:v]fps={FPS},scale={WW}:{WH}:force_original_aspect_ratio=increase:flags=lanczos,"
             f"crop={WW}:{WH}:(iw-{WW})/2:(ih-{WH})*{y}")
        if z > 1.0:
            v += f",scale={int(WW * z) // 2 * 2}:{int(WH * z) // 2 * 2}:flags=lanczos,crop={WW}:{WH}:(iw-{WW})/2:(ih-{WH})*0.25"
        ins = ["-ss", f"{p['ss']:.3f}", "-t", f"{n / FPS + 0.4:.3f}", "-i", p["src"]]
    fc = v + f",format=yuv420p,tpad=stop_mode=clone:stop=3,trim=end_frame={n},setpts=PTS-STARTPTS[v]"
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-frames:v", n, "-r", FPS,
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", "-pix_fmt", "yuv420p", *TAG, "-an", out])
    k = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out]).stdout)
    if k != n: print(f"   !!! {out.name}: {k}/{n} quadros"); sys.exit(1)


def janela(PL):
    lista = []
    for f in M.glob("p_*.mp4"): f.unlink()
    for k, p in enumerate(PL):
        out = M / f"p_{k:03d}.mp4"; render(p, out); lista.append(out)
        print(f"  [{k + 1}/{len(PL)}] {p['q0'] / FPS:6.2f}s {p['n']:4d}q {p['id']}", flush=True)
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in lista), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "janela.mp4"])


# ------------------------------------------------------------------ áudio
def audio(FA, total, T_VIRADA, cta_t):
    N = int(round(total * SR)); voz = np.zeros((N, 2), np.float32); amb = np.zeros((N, 2), np.float32)
    def pos(buf, a, t0):
        s = int(round(t0 * SR)); n = min(len(a), N - s); buf[s:s + n] += a[:n]
    for f in FA:
        if not f["audio"]: continue
        a = fade(load(f["audio"], f["ss"], f["d"])); a *= 10 ** ((-15.0 - lufs(a)) / 20); pos(voz, a, f["T0"])
    # som nativo da briga (voz STS da Lucía já embutida), -16 LUFS, -5 dB sob a reportera
    nat = load(M / "abertura_nat.wav"); nat *= 10 ** ((-16 - lufs(nat)) / 20)
    fr0 = pal("R00")[-1]["fim"] + 0.05; tt = np.arange(len(nat)) / SR
    nat *= (10 ** (np.interp(tt, [0, fr0, fr0 + 0.3, 1e9], [-5, -5, 0, 0]) / 20)).astype(np.float32)[:, None]
    nat[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))[:, None]; pos(amb, nat, 0.0)
    # trilha triste (mãos/vazio) -> esperança (2 clientes / cheio) -> leito baixo até o fim
    v0, v1 = T_VIRADA; t_duas = v0 + 2.6 + 1.7
    tri = load(TRILHA_TRISTE); tri *= 10 ** ((-19 - lufs(tri)) / 20)
    nt = int((t_duas - v0 + 0.8) * SR); tri = tri[:nt].copy(); xf = int(0.8 * SR)
    tri[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))[:, None]; tri[-xf:] *= np.linspace(1, 0, xf)[:, None]
    pos(amb, tri, v0 - 0.1)
    es = load(TRILHA_ESP)
    need = N - int(t_duas * SR)
    while len(es) < need:
        cf = 2 * SR; w = np.linspace(0, 1, cf)[:, None]; x = load(TRILHA_ESP)
        es = np.concatenate([es[:-cf], es[-cf:] * (1 - w) + x[:cf] * w, x[cf:]])
    es = es[:need].copy(); es *= 10 ** ((-20 - lufs(es)) / 20)
    te = t_duas + np.arange(len(es)) / SR
    env = np.interp(te, [0, v1 - 0.2, v1 + 0.6, 1e9], [0, 0, -11, -11])            # baixa sob as falas
    es *= (10 ** (env / 20)).astype(np.float32)[:, None]
    es[:xf] *= np.linspace(0, 1, xf)[:, None]; pos(amb, es, t_duas)
    mix = voz + amb; mix[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"])
    raw.unlink(); print("audio ok")


# ------------------------------------------------------------------ legenda (estilo v4: 3 palavras, palavra atual amarela)
FS, Y_POST, Y_CTA = 64, 1072, 832
MAXP, MAXC = 3, 18
JUNTAR = [(["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["doña", "lucía"], "doña lucía"), (["juan", "méndez"], "juan méndez")]


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def palavras_tl(FA):
    out = []
    for f in FA:
        for p in f["palavras"]:
            w = limpa(p["w"])
            if w: out.append(dict(w=w, raw=p["w"], ini=f["T0"] + p["ini"], fim=f["T0"] + p["fim"], linha=f["id"]))
    out.sort(key=lambda x: x["ini"]); res, k = [], 0
    while k < len(out):
        for seq, rep in JUNTAR:
            if [x["w"] for x in out[k:k + len(seq)]] == seq and len({x["linha"] for x in out[k:k + len(seq)]}) == 1:
                res.append(dict(out[k], w=rep, fim=out[k + len(seq) - 1]["fim"], raw=out[k + len(seq) - 1]["raw"])); k += len(seq); break
        else: res.append(out[k]); k += 1
    return res


def blocos(W):
    B, cur = [], []
    for w in W:
        cand = cur + [w]; txt = " ".join(x["w"] for x in cand)
        if cur and (len(cand) > MAXP or len(txt) > MAXC or cur[-1]["linha"] != w["linha"] or w["ini"] - cur[-1]["fim"] > 0.6):
            B.append(cur); cand = [w]
        cur = cand
        if re.search(r"[.!?…:;]$", w["raw"]) or (w["raw"].endswith(",") and len(cur) >= 2): B.append(cur); cur = []
    if cur: B.append(cur)
    return B


def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(FA, total, cta_t):
    W = palavras_tl(FA); B = blocos(W); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total)
        y = Y_CTA if ini >= cta_t - 0.1 else Y_POST
        for j, w in enumerate(b):
            a = ini if j == 0 else max(ini, w["ini"] - 0.04); e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + x["w"] for jj, x in enumerate(b))
            pop = r"\fscx85\fscy85\t(0,80,\fscx104\fscy104)\t(80,140,\fscx100\fscy100)" if j == 0 else ""
            ev.append(f"Dialogue: 1,{ts(a)},{ts(e)},L,,0,0,0,,{{\\an5\\pos(360,{y}){pop}}}{txt}")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins SemiBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,2,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    (M / "leg.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    json.dump([dict(ini=round(b[0]["ini"], 3), texto=" ".join(x["w"] for x in b)) for b in B], open(M / "leg_blocos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)


# ------------------------------------------------------------------ vídeo final
def final(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    L = [(GB / "graficos" / "plate.png", None), (G / "header.png", None), (GL / "titulo_gancho.png", (0.0, 3.0)),
         (G / "cta_txt.png", (cta_t, None)), (G / "cta_setas.png", (cta_t, None)), (G / "selo.png", None)]
    ins = ["-reinit_filter", "0", "-i", "janela.mp4", "-i", "mix.wav"]
    for p, _ in L: ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total + 1:.3f}", "-i", str(p)]
    en = lambda r: "" if r is None else f":enable='gte(t,{r[0] - 1 / 60:.4f})" + (f"*lt(t,{r[1] - 1 / 60:.4f})'" if r[1] else "'")
    fc = [f"[2:v]format=yuv420p[pl]", f"[0:v]setpts=N/({FPS}*TB)[w]", f"[pl][w]overlay=0:{WY}:format=auto[o0]",
          f"[3:v]format=rgba[h];[o0][h]overlay=0:0:format=auto[o1]",
          f"[4:v]format=rgba[t];[o1][t]overlay=0:0:format=auto{en(L[2][1])}[o2]",
          f"[o2]ass=leg.ass:fontsdir=fonts[o3]",
          f"[5:v]format=rgba[c1];[o3][c1]overlay=0:-22:format=auto{en(L[3][1])}[o4]",
          f"[6:v]format=rgba[c2];[o4][c2]overlay=0:'-37+10*sin(2*PI*1.4*t)':format=auto{en(L[4][1])}[o5]",
          f"[7:v]format=rgba[s];[o5][s]overlay=0:0:format=auto,format=yuv420p[v]"]
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS,
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{total:.2f} s")


def folha(total):
    n = 30; fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    for k in range(n):
        t = (k + 0.5) * total / n
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=360:640", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", f"tile={n}x1", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


def narracion(FA, total, cta_t):
    mm = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"
    lin = []
    for f in sorted(FA, key=lambda f: f["T0"] + f["palavras"][0]["ini"]):
        t = f["T0"] + f["palavras"][0]["ini"]; lin.append(f"[{mm(t)}] {NOME[f['id']]}: {TX[f['id']]}")
    cab = f"""NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})
Lote "Humillación" · P9 DOÑA LUCÍA (peluquera). Tiempos = momento en que empieza cada frase en el video final. Texto = ROTEIRO_PERSONAS_v2.md (P9).
Personajes ficticios: REPORTERA (en PiP de 0:00 a 0:05 y luego frente al salón), CLIENTA y DOÑA LUCÍA (peluquera, ~50 años).
Sello "VIDEO FICTICIO" arriba a la derecha durante todo el video. Moldura de post "Fe en Noticias" todo el video. "(voz en off)" = narración sobre b-roll.
Voces: reportera Gabriela (ElevenLabs) · doña Lucía Azu (ElevenLabs; en la pelea, voz nativa del Seedance convertida a Azu con speech-to-speech) · clienta: voz nativa del Seedance.
0:00–0:05 la acción de la pelea va en cámara lenta (0,43x) bajo la reportera en PiP; título 0–3 s: "LA HUMILLARON EN SU SALÓN… AL DÍA SIGUIENTE PASÓ ESTO".
Sin voz (≈0:13–0:21): Lucía junta el crucifijo del suelo (música triste) → silla vacía → 2 clientas → salón lleno (música de esperanza).
CTA único al final (flechas TOCA «VER MÁS» desde {mm(cta_t)} hasta el final); nada se dice después del CTA.
"""
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


def main():
    PL, FA, total, cta_t, TV = plano()
    json.dump(dict(planos=[{k: str(v) if isinstance(v, Path) else v for k, v in p.items()} for p in PL],
                   falas=[dict(id=f["id"], T0=round(f["T0"], 3), ini=round(f["T0"] + f["palavras"][0]["ini"], 3), fim=round(f["T0"] + f["palavras"][-1]["fim"], 3)) for f in FA],
                   total=total, cta=cta_t, virada=TV), open(M / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"total {total:.2f} s, CTA {cta_t:.2f}")
    janela(PL); audio(FA, total, TV, cta_t); legenda(FA, total, cta_t); final(total, cta_t); folha(total); narracion(FA, total, cta_t)


if __name__ == "__main__":
    main()
