# -*- coding: utf-8 -*-
"""SB-ES Humillación P5 Doña Marta -> v5-personas/SB-ES_HUMILLACION_P5-MARTA_FICTICIO.mp4 (+ _narracion.txt, _frames.jpg).
Linha do tempo linear (plano.json). Corpo composto em Python (leitura/gravação bt601 fixa, comum3),
moldura do post o vídeo todo (plate + header), PiP da reportera no início com zoom 130 % 0-2 s, título 0-3 s,
legenda ASS palavra a palavra, setas TOCA «VER MÁS» do CTA até o fim, selo VIDEO FICTICIO o vídeo todo.
Uso: python montar.py [--so-plano] [--so-final]"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; T = AQ / "takes"; V = AQ / "voz"; GR = AQ / "graficos"; M = AQ / "mont"; M.mkdir(exist_ok=True)
FONTES = AQ.parents[2] / "_trabalho" / "graficos"
OUT = Path(sys.argv[sys.argv.index("--saida") + 1]) if "--saida" in sys.argv else AQ.parents[1] / "SB-ES_HUMILLACION_P5-MARTA_FICTICIO.mp4"
FPS, SR, WW, WH, WY = 30, 48000, 720, 840, 297
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
PIP = dict(x=0, y=396, w=250, h=444, xc=233); NFADE = 4   # PiP menor que o da v4 (revisor: cobria o matón)
ARGS = sys.argv[1:]
CFG = json.loads((AQ / "cfg.json").read_text(encoding="utf-8")) if (AQ / "cfg.json").exists() else {}


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:1500]); print(r.stderr[-2500:]); sys.exit(1)
    return r


def vj(i): return json.loads((V / f"{i}.json").read_text(encoding="utf-8"))
def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


# ------------------------------------------------------------------ plano
GAP = 0.10
VIRADA = CFG.get("virada", [["maos", 1.20, 2.6], ["vazio", 2.40, 2.1], ["cinco", 1.80, 2.1], ["fila", 0.50, 2.5]])
HG_INI = CFG.get("hg_ini", {})
COBRE = CFG.get("cobre", {"M2": [[3.40, 5.95, "reza_noite", 0.3]], "M3": [[0.72, 3.13, "reza_alba", 0.3]]})   # b-roll sobre trecho do HeyGen (tempo do take)


def plano():
    S = []

    def seg(**k): S.append(k); return k
    B = CFG.get("briga", dict(ss=0.0, d=10.0, b02=4.75, b03=6.90))
    seg(id="briga", src=T / "briga_hg1.mp4", ss=B["ss"], d=B["d"], t0=0.0, zoom=[(0.0, 2.0, 1.30, 300, 330)], pip=T / "hg_R00.mp4",
        falas=[("B01", "R00", 0.0), ("B02", "B02", B["b02"]), ("B03", "B03", B["b03"])])
    t = B["d"]
    for nome, ss, d in VIRADA:
        seg(id=nome, src=T / f"{nome}.mp4", ss=ss, d=d, t0=t); t += d
    tv = t

    def hg(voz, zoom=1.0):
        nonlocal t
        src = T / f"hg_{voz}.mp4"; P = vj(voz)["palavras"]
        u0 = HG_INI.get(voz, max(0.0, P[0]["ini"] - 0.06)); u1 = min(P[-1]["fim"] + 0.14, dur(src) - 0.04)
        seg(id=voz, src=src, ss=u0, d=u1 - u0, t0=t, zoomfix=zoom, falas=[(voz, voz, t - u0)], hg=True, cobre=COBRE.get(voz, [])); t += (u1 - u0) + GAP
    hg("R01", 1.0)
    P = vj("M1")["palavras"]; u0 = max(0.0, P[0]["ini"] - 0.06); d1 = P[-1]["fim"] + 0.18 - u0
    seg(id="noite", src=T / "noite.mp4", ss=0.0, d=d1, t0=t, vel=min(1.0, 4.95 / d1), falas=[("M1", "M1", t - u0)]); t += d1 + GAP
    hg("M2", 1.0); hg("M3", 1.10); hg("M4", 1.0); hg("M5", 1.10); hg("CTA", 1.0)
    S[-1]["d"] += 0.30
    total = round(round((S[-1]["t0"] + S[-1]["d"]) * FPS) / FPS, 4)
    return S, total, tv


# ------------------------------------------------------------------ vídeo (corpo)
def janela(src, ss, d, vel=1.0):
    """quadros 720x840 (cover, 30 fps) do trecho a partir de ss, tocado na velocidade vel"""
    n = round(d * FPS); tmp = M / f"_{Path(src).stem}_{ss:.2f}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{d * vel + 0.5:.3f}", "-i", src, "-vf",
         f"setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS},scale={WW}:{WH}:force_original_aspect_ratio=increase:flags=lanczos,crop={WW}:{WH}:(iw-{WW})/2:(ih-{WH})*0.25,"
         f"tpad=stop_mode=clone:stop_duration=1", "-frames:v", n, "-an", "-c:v", "libx264", "-crf", "8", "-preset", "fast", tmp])
    fr = list(quadros(tmp, 0, n, WW, WH)); tmp.unlink()
    assert len(fr) == n, (src, len(fr), n)
    return fr


def zoom(f, z, cx, cy):
    cw, ch = WW / z, WH / z; x0 = min(max(cx - cw / 2, 0), WW - cw); y0 = min(max(cy - ch / 2, 0), WH - ch)
    Mx = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]])
    return cv2.warpAffine(f, Mx, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def alfa(f):
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def corpo(S, total):
    plate = cv2.imread(str(GR / "plate.png")); N = round(total * FPS)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, "-frames:v", str(N), str(M / "corpo.mp4")], stdin=subprocess.PIPE)
    k = 0
    for i, s in enumerate(S):
        q0 = round(s["t0"] * FPS); q1 = round(S[i + 1]["t0"] * FPS) if i + 1 < len(S) else N
        n = q1 - q0; fr = janela(s["src"], s["ss"], n / FPS, s.get("vel", 1.0)); NP = 0
        cob = set()
        for a, b, key, bss in s.get("cobre", []):
            j0, j1 = max(0, round((a - s["ss"]) * FPS)), min(n, round((b - s["ss"]) * FPS))
            fr[j0:j1] = janela(T / f"{key}.mp4", bss, (j1 - j0) / FPS); cob.update(range(j0, j1))
        if s.get("pip"):
            t30 = M / "_pip30.mp4"
            run(["ffmpeg", "-v", "error", "-y", "-i", s["pip"], "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
            tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30)]; t30.unlink()
            NP = len(tk); QS = NP - NFADE
        for j, f in enumerate(fr):
            t = j / FPS
            for a, b, z, cx, cy in s.get("zoom", []):
                if a <= t < b: f = zoom(f, z, cx, cy)
            if s.get("zoomfix", 1.0) > 1.0 and j not in cob: f = zoom(f, s["zoomfix"], 360, 330)
            if j < NP:
                fg, a = alfa(tk[j]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
                x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]; hh = min(h, WH - y0)
                A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]; A[:, PIP["xc"]:] = 0
                if j >= QS: A *= 1 - (j - QS + 1) / (NFADE + 1)
                f = np.clip(F * A[..., None] + f.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
            o = plate.copy(); o[WY:WY + WH] = f; ff.stdin.write(o.tobytes()); k += 1
        print(f"  {s['id']:6s} {q0 / FPS:6.2f} +{n / FPS:5.2f}", flush=True)
    ff.stdin.close(); ff.wait(); assert k == N, (k, N)


# ------------------------------------------------------------------ áudio
def load(p, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + (["-t", f"{t:.3f}"] if t else []) + \
          ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < SR // 2: a = np.concatenate([a, np.zeros((SR // 2 - len(a), 2), np.float32)])
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    raw.unlink(); return max(-70.0, float([x for x in r.stderr.splitlines() if x.strip().startswith("I:")][-1].split()[1]))


def norm(a, db): return a * 10 ** ((db - lufs(a)) / 20)


def fade(a, i=0.05, o=0.05):
    ni, no = int(i * SR), int(o * SR)
    if ni: a[:ni] *= np.linspace(0, 1, ni)[:, None]
    if no: a[-no:] *= np.linspace(1, 0, no)[:, None]
    return a


def env(n, xs, ys): return (10 ** (np.interp(np.arange(n) / SR, xs, ys) / 20)).astype(np.float32)[:, None]


def audio(S, total, tv):
    N = int(round(total * SR)); mix = np.zeros((N, 2), np.float32)

    def pos(a, t0):
        s = int(round(t0 * SR)); a = a[max(0, -s):]; s = max(0, s); n = min(len(a), N - s); mix[s:s + n] += a[:n]
    for s in S:
        for id_, voz, off in s.get("falas", []):
            pos(fade(norm(load(V / f"{voz}.wav"), -15.0), 0.01, 0.03), off)
    B = S[0]
    sfx = norm(load(AQ / "trilha" / "sfx_briga.mp3"), CFG.get("sfx_lufs", -21.0)); sfx *= env(len(sfx), [0, 3.9, 4.3, 99], [-7, -7, -10, -10])
    pos(fade(sfx, 0.02, 0.6), CFG.get("sfx_t", 0.6))
    amb = norm(load(AQ / "trilha" / "amb_feria.mp3"), -30.0); pos(fade(amb[:int((B["d"] + 0.3) * SR)].copy(), 0.05, 0.5), 0.0)
    ent = [s for s in S if s["id"] in ("R01", "M2", "M3", "M4", "M5")]
    t0, t1 = ent[0]["t0"], ent[-1]["t0"] + ent[-1]["d"]; amb2 = load(AQ / "trilha" / "amb_feria.mp3")
    while len(amb2) < (t1 - t0) * SR: amb2 = np.concatenate([amb2, amb2[::-1]])
    pos(fade(norm(amb2[:int((t1 - t0) * SR)].copy(), -36.0), 0.4, 0.6), t0)
    tm = next(s["t0"] for s in S if s["id"] == "maos"); tc = next(s["t0"] for s in S if s["id"] == "cinco"); tr = next(s["t0"] for s in S if s["id"] == "R01")
    tri = norm(load(AQ / "trilha" / "triste_1.mp3"), -19.0)[:int((tc - tm + 0.9) * SR)].copy(); pos(fade(tri, 0.4, 0.9), tm - 0.4)
    es = norm(load(AQ / "trilha" / "esperanca_1.mp3"), -20.0)[:int((tr + 2.4 - tc) * SR)].copy()
    es *= env(len(es), [0, tr - 0.3 - tc, tr + 1.6 - tc, 99], [0, 0, -12, -12]); pos(fade(es, 0.8, 0.6), tc - 0.2)
    mix[-int(0.25 * SR):] *= np.linspace(1, 0, int(0.25 * SR))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.7:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.4f}", "-c:a", "pcm_s16le", M / "mix.wav"])
    raw.unlink(); print("audio ok")


# ------------------------------------------------------------------ legenda
FS, Y_POST, Y_CTA, MAXP, MAXC = 64, 1072, 840, 3, 18


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def palavras(S):
    W = []
    for s in S:
        for id_, voz, off in s.get("falas", []):
            for p in vj(voz)["palavras"]:
                W.append(dict(w=limpa(p["w"]), raw=p["w"], ini=off + p["ini"], fim=off + p["fim"], linha=id_))
    W.sort(key=lambda x: x["ini"]); res, k = [], 0
    while k < len(W):
        par = [x["w"] for x in W[k:k + 2]]
        if par in (["san", "benito"], ["en", "vivo"]) and W[k]["linha"] == W[k + 1]["linha"]:
            res.append(dict(W[k], w=" ".join(par), fim=W[k + 1]["fim"], raw=W[k + 1]["raw"])); k += 2
        else: res.append(W[k]); k += 1
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
    W = palavras(S); B = blocos(W); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total); y = Y_CTA if ini >= cta_t - 0.1 else Y_POST
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
    json.dump([dict(ini=round(b[0]["ini"], 3), texto=" ".join(x["w"] for x in b)) for b in B], open(M / "leg_blocos.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)


# ------------------------------------------------------------------ final
def final(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in FONTES.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    L = [("header.png", 0, total + 5, "0"), ("titulo_gancho.png", 0, 3.0, "0")]
    C = [("cta_txt.png", cta_t, total + 5, "-22"), ("cta_setas.png", cta_t, total + 5, "-37+10*sin(2*PI*1.4*t)")]
    pngs = [p for p, *_ in L + C] + ["selo.png"]
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    for p in pngs: ins += ["-loop", "1", "-framerate", "30", "-t", f"{total + 1:.3f}", "-i", str(GR / p)]
    fc = [f"[0:v]setpts=N/({FPS}*TB)[base]"]; ult = "[base]"

    def ov(k, a, b, y, ult):
        en = "" if (a <= 0 and b > total) else f":enable='gte(t,{a - 1 / 60:.4f})*lt(t,{b - 1 / 60:.4f})'"
        fc.append(f"[{k + 2}:v]format=rgba[i{k}]"); out = f"[o{k}]"; fc.append(f"{ult}[i{k}]overlay=0:{y}:format=auto{en}{out}"); return out
    k = 0
    for p, a, b, y in L: ult = ov(k, a, b, y, ult); k += 1
    fc.append(f"{ult}ass=leg.ass:fontsdir=fonts[leg]"); ult = "[leg]"
    for p, a, b, y in C: ult = ov(k, a, b, y, ult); k += 1
    ult = ov(k, 0, total + 5, "0", ult); fc.append(f"{ult}format=yuv420p[v]")
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
         "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS, "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
         "-t", f"{total:.3f}", OUT], cwd=M)


def folha(total):
    n = 30; fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    for k in range(n): run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(k + 0.5) * total / n:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=360:640", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", f"tile={n}x1", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


ROT = {"R00": "Imágenes impactantes: una feriante fue atacada en plena feria… por su fe.",
       "B02": "¡Llama a tu Dios para que te recoja esto!", "B03": "Señor, yo no le hice nada. ¡Pare, por el amor de Dios!",
       "R01": "Al día siguiente, el puesto de doña Marta se quedó sin fruta antes del mediodía."}


def narracion(S, total):
    mm = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"
    nome = dict(R00="REPORTERA (en PiP)", B02="MATÓN", B03="DOÑA MARTA", R01="REPORTERA", M1="DOÑA MARTA (voz en off)", M2="DOÑA MARTA",
                M3="DOÑA MARTA (pedido)", M4="DOÑA MARTA (pedido)", M5="DOÑA MARTA (pedido)", CTA="REPORTERA (CTA)")
    lin = []
    for s in S:
        for id_, voz, off in s.get("falas", []):
            P = vj(voz)["palavras"]; tx = ROT.get(voz) or " ".join(p["w"] for p in P)
            lin.append(f"[{mm(off + P[0]['ini'])}] {nome.get(voz, voz)}: {tx}")
            if voz == "B03":
                lin.append(f"[{mm(S[1]['t0'])}] (sin voz: Marta recoge el crucifijo entre la fruta, música triste -> puesto vacío -> 5 clientes -> fila llena, música de esperanza)")
    cab = f"""NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})
Lote "Humillación" (v5 personas) · P5 DOÑA MARTA (puesto de frutas en la feria). Texto = ROTEIRO_PERSONAS_v2.md (P5 + [PEDIDO] + [CTA]).
Personajes ficticios: REPORTERA (en PiP desde 0:00 y luego en la calle), MATÓN (agresor) y DOÑA MARTA (feriante, 55-60 años).
Sello "VIDEO FICTICIO" arriba a la derecha todo el video. Marco de post "Fe en Noticias / Trabajador es humillado y algo impactante sucede (estándar del lote)" todo el video.
Título 0-3 s: "LA HUMILLARON POR SU FE… AL DÍA SIGUIENTE PASÓ ESTO". Flechas TOCA «VER MÁS» desde el CTA hasta el final; nada se dice después del CTA.
Voces (ElevenLabs): reportera Gabriela · matón Richard · doña Marta María Blanco (también en la pelea).
"""
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


if __name__ == "__main__":
    S, total, tv = plano(); cta_t = next(s["t0"] for s in S if s["id"] == "CTA")
    json.dump(dict(total=total, cta_t=cta_t, segs=[{k: (str(v) if isinstance(v, Path) else v) for k, v in s.items()} for s in S]),
              open(AQ / "plano.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for s in S: print(f"{s['t0']:6.2f} +{s['d']:5.2f} {s['id']:6s} ss {s['ss']:.2f} vel {s.get('vel', 1):.2f}")
    print("TOTAL", total, "CTA", cta_t)
    if "--so-plano" in ARGS: sys.exit()
    legenda(S, total, cta_t)
    if "--so-final" not in ARGS: corpo(S, total); audio(S, total, tv)
    final(total, cta_t); print(narracion(S, total)); folha(total); print("ok", OUT)
