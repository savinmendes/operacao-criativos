# -*- coding: utf-8 -*-
"""Montagem P2 ROSA (lote Humillación v5) -> v5-personas/SB-ES_HUMILLACION_P2-ROSA_FICTICIO.mp4 (+ _narracion.txt, _frames.jpg)
Molde visual = v4 B (moldura de post Fe en Noticias, janela 720x840 em y=297, título 0-3 s, legenda palavra a palavra,
selo VIDEO FICTICIO, setas TOCA «VER MÁS» do início do CTA até o fim). Cada plano de b-roll usado uma vez só.
Uso: python montar_p2.py [--so-plano]"""
import json, re, subprocess, sys, difflib
from pathlib import Path
import numpy as np

AQ = Path(__file__).resolve().parent; RAIZ = AQ.parents[2]; V5 = AQ.parents[1]
M = AQ / "mont"; M.mkdir(exist_ok=True); GR = AQ / "graficos"; T = AQ / "takes"; A = AQ / "audio"
GFONT = RAIZ / "_trabalho" / "graficos"
OUT = V5 / "SB-ES_HUMILLACION_P2-ROSA_FICTICIO.mp4"
FPS, SR = 30, 48000
WIN = (0, 297, 720, 840)
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
TRILHA = RAIZ / "v3" / "_trabalho" / "final_B" / "trilha"
ITENS = json.loads((A / "itens.json").read_text(encoding="utf-8"))
SLOW_T, SLOW_D = 2.80, 4.45 - 2.80          # prep_briga.py: 0-2,80 s esticado para 4,45 s

TX = {  # texto exato do roteiro (ROTEIRO_PERSONAS_v2.md, P2)
    "R00": "Imágenes impactantes: una costurera fue humillada por una clienta… por su fe.",
    "CLI": "¿Y tu Dios no te enseñó a coser? ¡Llámalo a ver si te ayuda!",
    "ROS": "Señora, yo lo hice con todo mi cariño. No me hable así, por favor.",
    "R01": "Al día siguiente, el taller de doña Rosa tenía encargos hasta el fin de mes.",
    "RA1": "Esa noche lloré sobre la máquina de coser.",
    "RA2": "Treinta años cosiendo… y me sentí una inútil.",
    "RA3": "Mi comadre me mandó la transmisión del padre Juan Méndez.",
    "RA4": "La hice esa misma noche, como él enseña. Al otro día, entraron tres clientas que yo ni conocía.",
    "RP1": "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche.",
    "RP2": "Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito…",
    "RP3": "y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?",
    "CTA": "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo.",
}
NOME = {"R00": "REPORTERA (en PiP)", "CLI": "CLIENTA", "ROS": "DOÑA ROSA", "R01": "REPORTERA", "RA1": "DOÑA ROSA (voz en off)",
        "RA2": "DOÑA ROSA", "RA3": "DOÑA ROSA (voz en off)", "RA4": "DOÑA ROSA", "RP1": "DOÑA ROSA [PEDIDO]", "RP2": "DOÑA ROSA [PEDIDO]",
        "RP3": "DOÑA ROSA [PEDIDO]", "CTA": "REPORTERA [CTA]"}


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:2000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout.strip())


def load(p, ss=0.0, t=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < SR // 2: a = np.concatenate([a, np.zeros((SR // 2 - len(a), 2), np.float32)])
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    raw.unlink(); v = float([x for x in r.stderr.splitlines() if x.strip().startswith("I:")][-1].split()[1]); return v if v > -70 else -70.0


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def texto_roteiro(P, txt):
    R = txt.split()
    if len(R) == len(P): return [dict(p, w=r) for p, r in zip(P, R)]
    a = [limpa(p["w"]) for p in P]; b = [limpa(r) for r in R]; out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal": out += [dict(P[i1 + k], w=R[j1 + k]) for k in range(i2 - i1)]
        elif j2 > j1 and i2 > i1:
            t0, t1 = P[i1]["ini"], P[i2 - 1]["fim"]; L = [len(limpa(R[j])) + 1 for j in range(j1, j2)]; s = sum(L); t = t0
            for k, j in enumerate(range(j1, j2)): d = (t1 - t0) * L[k] / s; out.append(dict(w=R[j], ini=t, fim=t + d)); t += d
        elif j2 > j1:
            t = out[-1]["fim"] if out else P[0]["ini"]
            for j in range(j1, j2): out.append(dict(w=R[j], ini=t, fim=t + 0.01))
    return out


def pal(i, off=0.0, bloco=None):
    return [dict(w=p["w"], ini=p["ini"] + off, fim=p["fim"] + off, bloco=bloco or i) for p in texto_roteiro(ITENS[i]["palavras"], TX[i])]


# ------------------------------------------------------------------ segmentos
def segmentos():
    S = []
    # 1) abertura (já composta: janela 720x840 + PiP + áudio)
    wb = json.loads((T / "whisper_briga.json").read_text(encoding="utf-8"))
    sh = lambda t: t * (1 + SLOW_D / SLOW_T) if t < SLOW_T else t + SLOW_D
    wb = [dict(w=x["w"], ini=sh(x["ini"]), fim=sh(x["fim"])) for x in wb]
    k = next(j for j, x in enumerate(wb) if limpa(x["w"]) == "señora")
    W = pal("R00") + [dict(p, bloco="CLI") for p in texto_roteiro(wb[:k], TX["CLI"])] + [dict(p, bloco="ROS") for p in texto_roteiro(wb[k:], TX["ROS"])]
    S.append(dict(id="AB", file=M / "abertura.mp4", ss=0, dur=dur(M / "abertura.mp4"), janela=True, audio=M / "abertura.wav", amix="pronto", words=W, blocos=["R00", "CLI", "ROS"]))
    # 2) virada sem fala (cada plano uma vez)
    S.append(dict(id="MAOS", file=T / "v1_maos.mp4", ss=0.3, dur=2.6, cy=None, words=[], blocos=[]))
    S.append(dict(id="VAZIO", file=T / "v1_vazio.mp4", ss=1.5, dur=4.3, cy=None, words=[], blocos=[]))
    S.append(dict(id="CHEIO", file=T / "v1_cheio.mp4", ss=0.3, dur=2.3, cy=None, words=[], blocos=[]))
    # 3) reportera / Rosa / CTA
    def hg(i, f, z=1.0, cy=0.30):
        d = dur(T / f); return dict(id=i, file=T / f, ss=0, dur=min(d, ITENS[i]["dur"]), cy=cy, zoom=z, audio=T / f, words=pal(i), blocos=[i])
    def vo(i, f, ss=0.2):
        d = ITENS[i]["dur"] + 0.12; return dict(id=i, file=T / f, ss=ss, dur=d, cy=None, audio=AQ / f"vo_{i}.wav", words=pal(i), blocos=[i])
    S.append(hg("R01", "hg_R01.mp4", cy=CY_REP))
    S.append(vo("RA1", "v1_noite.mp4"))
    S.append(hg("RA2", "hg_RA2.mp4", 1.0, CY_ROSA))
    S.append(vo("RA3", "v1_celular.mp4"))
    S.append(hg("RA4", "hg_RA4.mp4", 1.12, CY_ROSA))
    S.append(hg("RP1", "hg_RP1.mp4", 1.0, CY_ROSA))
    S.append(hg("RP2", "hg_RP2.mp4", 1.12, CY_ROSA))
    S.append(hg("RP3", "hg_RP3.mp4", 1.0, CY_ROSA))
    S.append(hg("CTA", "hg_CTA.mp4", cy=CY_REP))
    t = 0.0
    for s in S:
        n = int(round(s["dur"] * FPS)); s["n"] = n; s["T0"] = round(t, 4); t += n / FPS
    return S, round(t, 4)


CY_REP, CY_ROSA = 0.22, 0.30


def render(s, out):
    n = s["n"]
    if s.get("janela"):
        v = "[0:v]fps=30"
    else:
        zz = s.get("zoom", 1.0); w, h = WIN[2], WIN[3]
        sw, sh = int(720 * zz) // 2 * 2, None
        v = f"[0:v]fps=30,scale={sw}:-2:flags=lanczos"
        # recorte da janela: cy = posição relativa do centro do recorte na altura da fonte escalada
        cy = s.get("cy")          # posição relativa do rosto na fonte -> rosto a 40 % da altura da janela
        yexp = f"(ih-{h})/2" if cy is None else f"max(0\\,min(ih-{h}\\,ih*{cy}-{0.40 * h:.0f}))"
        v += f",crop={w}:{h}:(iw-{w})/2:{yexp}"
    fc = v + f",format=yuv420p,tpad=stop_mode=clone:stop=6,trim=end_frame={n},setpts=PTS-STARTPTS[v]"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['ss']:.3f}", "-i", s["file"], "-filter_complex", fc, "-map", "[v]", "-frames:v", n, "-r", FPS,
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *TAG, "-an", out])


COBRE = {"RA4": (3.45, "v1_costura.mp4", 0.2, 1.25, 0.58), "RP2": (6.00, "v1_oracion.mp4", 0.3, 1.0, None)}   # costura: zoom 1,25 corta o decalque dourado da máquina   # (a partir de s no take, b-roll, ss): voz segue do take


def partes(S):
    P = []
    for s in S:
        if s["id"] not in COBRE or not (T / COBRE[s["id"]][1]).exists(): P.append(s); continue
        a, f, ss, zz, cy = COBRE[s["id"]]; na = int(round(a * FPS))
        P.append(dict(s, n=na, id=s["id"] + "a"))
        P.append(dict(id=s["id"] + "_broll", file=T / f, ss=ss, n=s["n"] - na, cy=cy, zoom=zz, T0=s["T0"] + na / FPS))
    return P


def corpo(S):
    L = []; S = partes(S)
    for k, s in enumerate(S):
        o = M / f"s_{k:02d}_{s['id']}.mp4"; render(s, o); L.append(o); print(f"  [{k + 1}/{len(S)}] {s['id']} {s['T0']:.2f} +{s['n'] / 30:.2f}", flush=True)
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in L), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "janela.mp4"])


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)); voz = np.zeros((N, 2), np.float32); mus = np.zeros((N, 2), np.float32)
    def pos(buf, a, t0):
        s = int(round(t0 * SR)); n = min(len(a), N - s); buf[s:s + n] += a[:n]
    by = {s["id"]: s for s in S}
    for s in S:
        if not s.get("audio"): continue
        d = s["n"] / FPS
        if s.get("amix") == "pronto": a = load(s["audio"], 0, d)
        else:
            a = load(s["audio"], 0, d); a *= 10 ** ((-15 - lufs(a)) / 20)
        f = int(0.008 * SR); a[:f] *= np.linspace(0, 1, f)[:, None]; a[-f:] *= np.linspace(1, 0, f)[:, None]
        pos(voz, a, s["T0"])
    ab = voz[:int(by["AB"]["n"] / FPS * SR)]
    # trilha: triste (mãos + vazio) -> esperança (clientes entrando/cheio), abaixa sob a reportera e vira cama -32 LUFS até o fim
    t4 = by["MAOS"]["T0"]; t5 = by["VAZIO"]["T0"] + 2.9; tR = by["R01"]["T0"]
    tri = load(TRILHA / "triste_2.mp3"); tri *= 10 ** ((-19 - lufs(tri)) / 20)
    while len(tri) < int((t5 - t4 + 1.0) * SR): tri = np.concatenate([tri, tri])
    tri = tri[:int((t5 - t4 + 1.0) * SR)].copy(); xf = int(1.0 * SR)
    tri[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))[:, None]; tri[-xf:] *= np.linspace(1, 0, xf)[:, None]
    pos(mus, tri, t4 - 0.25)
    es = load(TRILHA / "esperanca_1.mp3"); es *= 10 ** ((-20 - lufs(es)) / 20)
    need = int((total - t5) * SR) + SR; base = es.copy()
    while len(es) < need:
        cf = 2 * SR; w = np.linspace(0, 1, cf)[:, None]; es = np.concatenate([es[:-cf], es[-cf:] * (1 - w) + base[:cf] * w, base[cf:]])
    es = es[:need]; es[:xf] *= np.linspace(0, 1, xf)[:, None]
    t = np.arange(len(es)) / SR + t5
    g = np.interp(t, [0, tR - 0.3, tR + 0.4, 1e9], [0, 0, -12, -12])                         # -20 -> -32 LUFS sob as falas
    es *= (10 ** (g / 20)).astype(np.float32)[:, None]
    pos(mus, es, t5)
    mix = voz + mus; mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"]); raw.unlink()


# ------------------------------------------------------------------ legenda (estilo v4)
FS, Y_POST, Y_CTA = 64, 1072, 840
MAXP, MAXC = 3, 18
JUNTAR = [(["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["doña", "rosa"], "doña rosa"), (["juan", "méndez"], "juan méndez")]


def palavras_tl(S):
    out = []
    for s in S:
        for p in s["words"]:
            w = limpa(p["w"])
            if w: out.append(dict(w=w, raw=p["w"], ini=s["T0"] + p["ini"], fim=s["T0"] + p["fim"], linha=p.get("bloco", s["id"]), segfim=s["T0"] + s["n"] / FPS))
    res, k = [], 0
    while k < len(out):
        for seq, rep in JUNTAR:
            if [x["w"] for x in out[k:k + len(seq)]] == seq:
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


def legenda(S, total, cta_t):
    W = palavras_tl(S); B = blocos(W); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total, b[-1]["segfim"]); y = Y_CTA if ini >= cta_t - 0.1 else Y_POST
        for j, w in enumerate(b):
            a = ini if j == 0 else max(ini, w["ini"] - 0.04); e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + x["w"] for jj, x in enumerate(b))
            pop = r"\fscx85\fscy85\t(0,80,\fscx104\fscy104)\t(80,140,\fscx100\fscy100)" if j == 0 else ""
            ev.append(f"Dialogue: 1,{ts(a)},{ts(e)},L,,0,0,0,,{{\\an5\\pos(360,{y}){pop}}}{txt}")
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 720\nPlayResY: 1280\nWrapStyle: 2\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: L,Poppins SemiBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,2,5,70,70,0,1\n\n[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    (M / "leg.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    json.dump([dict(ini=round(b[0]["ini"], 3), texto=" ".join(x["w"] for x in b)) for b in B], open(M / "leg_blocos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)


def video(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in GFONT.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    L = lambda p: ["-loop", "1", "-framerate", "30", "-t", f"{total + 1:.3f}", "-i", str(GR / p)]
    ins = ["-i", str(GR / "plate.png"), "-reinit_filter", "0", "-i", "janela.mp4", "-i", "mix.wav"] + L("header.png") + L("titulo_gancho.png") + L("cta_txt.png") + L("cta_setas.png") + L("selo.png")
    c = cta_t - 1 / 60
    fc = [f"[0:v]loop=-1:1:0,fps=30,trim=end_frame={int(round(total * FPS))},setpts=N/(30*TB),format=rgba[pl]",
          "[1:v]setpts=N/(30*TB)[jw]",
          f"[pl][jw]overlay={WIN[0]}:{WIN[1]}:format=auto[a0]",
          "[a0][3:v]overlay=0:0:format=auto[a1]",
          "[a1][4:v]overlay=0:0:format=auto:enable='lt(t,2.983)'[a2]",
          "[a2]ass=leg.ass:fontsdir=fonts[a3]",
          f"[a3][5:v]overlay=0:-22:format=auto:enable='gte(t,{c:.4f})'[a4]",
          f"[a4][6:v]overlay=0:'-37+10*sin(2*PI*1.4*t)':format=auto:enable='gte(t,{c:.4f})'[a5]",
          "[a5][7:v]overlay=0:0:format=auto,format=yuv420p[v]"]
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "2:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS,
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{total:.2f} s")


def folha(total):
    n = 30; fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    for k in range(n):
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(k + 0.5) * total / n:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=360:640", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", f"tile={n}x1", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


def narracion(S, total):
    def mmss(t): return f"{int(t // 60):02d}:{int(t % 60):02d}"
    lin = []; vistos = set()
    for s in S:
        for p in s["words"]:
            b = p.get("bloco", s["id"])
            if b in vistos: continue
            vistos.add(b); lin.append(f"[{mmss(s['T0'] + p['ini'])}] {NOME[b]}: {TX[b]}")
    by = {s["id"]: s for s in S}
    cab = (f"NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})\n"
           "Tiempos = momento en que empieza cada frase en el video final. Texto = ROTEIRO_PERSONAS_v2.md (P2 · DOÑA ROSA).\n"
           "Personajes ficticios: REPORTERA (en PiP desde 0:00, luego en pantalla), CLIENTA, DOÑA ROSA (costurera, 60 años).\n"
           "Sello \"VIDEO FICTICIO\" arriba a la derecha todo el video. \"(voz en off)\" = narración sobre b-roll de la propia Rosa, sin rostro.\n"
           "Voces: reportera Gabriela (ElevenLabs) · doña Rosa Luisa (ElevenLabs; en la pelea, voz nativa del take convertida a Luisa con speech-to-speech) · clienta voz nativa del take.\n"
           f"Sin voz [{mmss(by['MAOS']['T0'])}–{mmss(by['R01']['T0'])}]: Rosa recoge el crucifijo del suelo (música triste) -> taller vacío -> 2 clientas entrando -> percheros llenos (música de esperanza).\n"
           "Título 0–3 s: \"LA HUMILLARON POR SU FE… / AL DÍA SIGUIENTE PASÓ ESTO\". Flechas TOCA «VER MÁS» desde el CTA hasta el final; nada se dice después del CTA.\n")
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


if __name__ == "__main__":
    S, total = segmentos(); cta_t = next(s["T0"] for s in S if s["id"] == "CTA")
    for s in S: print(f"{s['T0']:6.2f} +{s['n'] / 30:5.2f} {s['id']:6s} {Path(s['file']).name}  {' '.join(p['w'] for p in s['words'])[:70]}")
    print("TOTAL", total, "CTA", cta_t)
    json.dump(dict(total=total, cta_t=cta_t, seg=[{k: str(v) if isinstance(v, Path) else v for k, v in s.items() if k != "words"} for s in S]),
              open(AQ / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--so-plano" in sys.argv: sys.exit()
    legenda(S, total, cta_t); corpo(S); audio(S, total); video(total, cta_t); folha(total); print(narracion(S, total))
