# -*- coding: utf-8 -*-
"""Montagem P0 Aurelio (lote Humillación, roteiro v2) -> v5-personas/SB-ES_HUMILLACION_P0-AURELIO_FICTICIO.mp4
Tudo dentro da moldura do post (plate + header "Fe en Noticias"), selo VIDEO FICTICIO o vídeo todo, legenda ES palavra a
palavra pelo roteiro, título 0-3 s, setas TOCA «VER MÁS» do início do CTA até o fim. Configuração: plano.json.
Uso: python montar.py [--so-plano]"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

AQ = Path(__file__).resolve().parent; M = AQ / "mont"; M.mkdir(exist_ok=True)
RAIZ = Path(r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES"); G = RAIZ / "_trabalho" / "graficos"; GL = AQ / "graficos"
PLATE = RAIZ / "v3" / "_trabalho" / "final_B" / "graficos" / "plate.png"
NV = RAIZ / "_trabalho" / "audio" / "sep" / "htdemucs" / "orig" / "no_vocals.wav"
TRI = RAIZ / "v3" / "_trabalho" / "final_B" / "trilha" / "triste_1.mp3"; ESP = RAIZ / "v3" / "_trabalho" / "final_B" / "trilha" / "esperanca_1.mp3"
OUT = RAIZ / "v5-personas" / "SB-ES_HUMILLACION_P0-AURELIO_FICTICIO.mp4"
if "--teste" in sys.argv: OUT = AQ / "w" / "teste.mp4"
FPS, SR = 30, 48000
WIN = (0, 297, 720, 840)
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
PJ = sys.argv[sys.argv.index("--plano") + 1] if "--plano" in sys.argv else "plano.json"
P = json.loads((AQ / PJ).read_text(encoding="utf-8"))


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:1500]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + (["-t", f"{t:.3f}"] if t else []) + \
          ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < SR // 2: a = np.concatenate([a, np.zeros((SR // 2 - len(a), 2), np.float32)])
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    raw.unlink(); v = float([x for x in r.stderr.splitlines() if x.strip().startswith("I:")][-1].split()[1]); return v if v > -70 else -70.0


def fade(a, ms=12):
    n = min(int(ms / 1000 * SR), len(a) // 2)
    if n: a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a


def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout.strip())


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


# ------------------------------------------------------------------ timeline
def timeline():
    """P['segs']: [{id, tipo: abertura|mudo|fala, video, ss?, dur?, zoom?, cx?, audio?, json?, texto?, nome, cobre?: [[a,b,video,ss]]}]"""
    t = 0.0; S = []; PL = []
    for s in P["segs"]:
        s = dict(s); s["T0"] = round(t, 4)
        if s["tipo"] == "mudo":
            d = s["dur"]; PL.append(dict(t0=t, t1=t + d, file=s["video"], vt=s.get("ss", 0.0), zoom=s.get("zoom", 1.0), cx=s.get("cx", 0.5), cy=s.get("cy", 0.5), id=s["id"]))
            s["palavras"] = []
        else:
            j = json.loads((AQ / s["json"]).read_text(encoding="utf-8")); W = j["palavras"]
            u0 = s.get("u0", 0.0 if s["tipo"] == "abertura" else max(0.04, min(0.10, W[0]["ini"] - 0.05)))
            u1 = s.get("u1", min(j.get("dur", W[-1]["fim"] + 0.2), W[-1]["fim"] + 0.22))
            d = u1 - u0; s["uso"] = [u0, u1]
            if s.get("texto"): W = roteiro_nos_tempos(W, s["texto"])
            s["palavras"] = [dict(p, ini=t + p["ini"] - u0, fim=t + p["fim"] - u0) for p in W]
            cob = sorted(s.get("cobre", []))
            cur = t
            for a, b, f, ss in cob:
                A, B = t + a - u0, t + b - u0
                if A > cur + 1e-3: PL.append(dict(t0=cur, t1=A, file=s["video"], vt=u0 + cur - t, zoom=s.get("zoom", 1.0), cx=s.get("cx", 0.5), cy=s.get("cy", 0.5), id=s["id"]))
                PL.append(dict(t0=A, t1=B, file=f, vt=ss, zoom=1.0, cx=0.5, cy=0.5, id=s["id"] + ":broll:" + Path(f).stem)); cur = B
            if cur < t + d - 1e-3: PL.append(dict(t0=cur, t1=t + d, file=s["video"], vt=u0 + cur - t, zoom=s.get("zoom", 1.0), cx=s.get("cx", 0.5), cy=s.get("cy", 0.5), id=s["id"]))
        t += d; s["T1"] = round(t, 4); S.append(s)
    total = round(round(t * FPS) / FPS, 4)
    for p in PL: p["q0"] = round(p["t0"] * FPS)
    for k, p in enumerate(PL): p["n"] = (PL[k + 1]["q0"] if k + 1 < len(PL) else round(total * FPS)) - p["q0"]
    return S, [p for p in PL if p["n"] > 0], total


def roteiro_nos_tempos(Pw, txt):
    import difflib
    R = txt.split()
    if len(R) == len(Pw): return [dict(p, w=r) for p, r in zip(Pw, R)]
    a = [limpa(p["w"]) for p in Pw]; b = [limpa(r) for r in R]; out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal": out += [dict(Pw[i1 + k], w=R[j1 + k]) for k in range(i2 - i1)]
        elif j2 > j1 and i2 > i1:
            t0, t1 = Pw[i1]["ini"], Pw[i2 - 1]["fim"]; L = [len(limpa(R[j])) + 1 for j in range(j1, j2)]; s = sum(L); t = t0
            for k, j in enumerate(range(j1, j2)): d = (t1 - t0) * L[k] / s; out.append(dict(w=R[j], ini=round(t, 3), fim=round(t + d, 3))); t += d
        elif j2 > j1:
            t = out[-1]["fim"] if out else Pw[0]["ini"]
            for j in range(j1, j2): out.append(dict(w=R[j], ini=t, fim=t + 0.01))
    return out


# ------------------------------------------------------------------ vídeo
def tam(f):
    o = run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", f]).stdout.strip().split(",")
    return int(o[0]), int(o[1])


def render(p, out):
    n = p["n"]; w, h = tam(p["file"]); zw = p.get("zoom", 1.0)
    ins = ["-ss", f"{max(0, p['vt']):.3f}", "-t", f"{n / FPS + 0.5:.3f}", "-i", p["file"], "-loop", "1", "-framerate", "30", "-t", f"{n / FPS + 0.5:.3f}", "-i", PLATE]
    sw = WIN[2]; sh = WIN[3]
    # cover em 720x840 com recorte em (cx, cy)
    s = max(sw / w, sh / h) * zw; nw, nh = int(w * s + 0.999) // 2 * 2, int(h * s + 0.999) // 2 * 2
    nw, nh = max(nw, sw), max(nh, sh)
    x0 = int((nw - sw) * p.get("cx", 0.5)); y0 = int((nh - sh) * p.get("cy", 0.5))
    v = (f"[0:v]setpts=PTS-STARTPTS,fps={FPS},scale={nw}:{nh}:flags=lanczos,crop={sw}:{sh}:{x0}:{y0}[w];[1:v]fps={FPS}[pl];"
         f"[pl][w]overlay={WIN[0]}:{WIN[1]},format=yuv420p,tpad=stop_mode=clone:stop=6,trim=end_frame={n},setpts=PTS-STARTPTS[v]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", v, "-map", "[v]", "-frames:v", n, "-r", FPS,
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", "-pix_fmt", "yuv420p", *TAG, "-an", out])
    k = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out]).stdout)
    if k != n: print(f"!!! {out.name}: {k}/{n} quadros -> {p}"); sys.exit(1)


def corpo(PL):
    for f in M.glob("p_*.mp4"): f.unlink()
    L = []
    for k, p in enumerate(PL):
        o = M / f"p_{k:03d}.mp4"; render(p, o); L.append(o)
        print(f"  [{k + 1}/{len(PL)}] {p['t0']:6.2f} {p['n']:4d}q {p['id']} z{p.get('zoom', 1)}", flush=True)
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in L), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "corpo.mp4"])


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)); mix = np.zeros((N, 2), np.float32)
    def pos(a, t0):
        s = int(t0 * SR); n = min(len(a), N - s)
        if n > 0: mix[s:s + n] += a[:n]
    by = {s["id"]: s for s in S}
    for s in S:
        if s["tipo"] == "abertura":
            a = load(s["video"]); a *= 10 ** ((-15 - lufs(a)) / 20); pos(fade(a[:int(s["uso"][1] * SR)], 30), s["T0"])
        elif s["tipo"] == "fala":
            u0, u1 = s["uso"]; a = fade(load(s["audio"], u0, u1 - u0)); a *= 10 ** ((-15.0 - lufs(a)) / 20); pos(a, s["T0"])
    # trilha: triste no 1º mudo -> esperança no plano "virada_esp"; abaixa sob a reportera e some
    v0 = by[P["trilha"]["triste_de"]]["T0"]; v1 = by[P["trilha"]["esperanca_de"]]["T0"]; vR = by[P["trilha"]["ate"]]["T0"]
    tri = load(TRI); tri *= 10 ** ((-19 - lufs(tri)) / 20); xf = int(0.9 * SR)
    nt = min(len(tri), int((v1 - v0 + 0.9) * SR)); tri = tri[:nt].copy()
    tri[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]; tri[-xf:] *= np.linspace(1, 0, xf)[:, None]; pos(tri, v0)
    es = load(ESP); es *= 10 ** ((-20 - lufs(es)) / 20); ne = min(len(es), int((vR + 2.2 - v1) * SR)); es = es[:ne].copy()
    es[:xf] *= np.linspace(0, 1, xf)[:, None]; env = np.ones(ne, np.float32); i0 = int((vR - 0.3 - v1) * SR)
    if 0 < i0 < ne: env[i0:] = np.linspace(1, 10 ** (-12 / 20), ne - i0)
    es *= env[:, None]; es[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))[:, None]; pos(es, v1)
    # rua (demucs da cena original) baixinha sob a entrevista
    t0 = vR - 0.1; bed = load(NV, 25.33, total - t0 + 0.2)
    if len(bed): bed = fade(bed, 300); bed *= 10 ** ((-33 - lufs(bed)) / 20); pos(bed, t0)
    mix[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"])
    raw.unlink()


# ------------------------------------------------------------------ legenda
FS, Y_POST, Y_CTA, MAXP, MAXC = 64, 1072, 840, 3, 18
JUNTAR = [(["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["don", "aurelio"], "don aurelio"), (["juan", "méndez"], "juan méndez")]


def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(S, total, cta_t):
    out = []
    for s in S:
        for p in s["palavras"]:
            w = limpa(p["w"])
            if w: out.append(dict(w=w, raw=p["w"], ini=p["ini"], fim=p["fim"], linha=s["id"] + ":" + p.get("fala", "")))
    W, k = [], 0
    while k < len(out):
        for seq, rep in JUNTAR:
            if [x["w"] for x in out[k:k + len(seq)]] == seq: W.append(dict(out[k], w=rep, fim=out[k + len(seq) - 1]["fim"], raw=out[k + len(seq) - 1]["raw"])); k += len(seq); break
        else: W.append(out[k]); k += 1
    B, cur = [], []
    for w in W:
        cand = cur + [w]; txt = " ".join(x["w"] for x in cand)
        if cur and (len(cand) > MAXP or len(txt) > MAXC or cur[-1]["linha"] != w["linha"] or w["ini"] - cur[-1]["fim"] > 0.6): B.append(cur); cand = [w]
        cur = cand
        if re.search(r"[.!?…:;]$", w["raw"]) or (w["raw"].endswith(",") and len(cur) >= 2): B.append(cur); cur = []
    if cur: B.append(cur)
    ev = []
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
    json.dump([dict(ini=round(b[0]["ini"], 3), texto=" ".join(x["w"] for x in b)) for b in B], open(M / "leg_blocos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)


def video(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    L = [(G / "header.png", 0, total + 5, "0"), (GL / "titulo_gancho.png", 0, 3.0, "0")]
    C = [(G / "cta_txt.png", cta_t, total + 5, "-22"), (G / "cta_setas.png", cta_t, total + 5, "-37+10*sin(2*PI*1.4*t)"), (G / "selo.png", 0, total + 5, "0")]
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    for f, *_ in L + C: ins += ["-loop", "1", "-framerate", "30", "-t", f"{total + 1:.3f}", "-i", str(f)]
    fc = [f"[0:v]setpts=N/({FPS}*TB)[b0]"]; ult = "[b0]"; k = 2
    def ov(a, b, y, ult, k):
        en = f":enable='gte(t,{a - 1 / 60:.4f})*lt(t,{b - 1 / 60:.4f})'" if (a > 0 or b < total) else ""
        o = f"[o{k}]"; fc.append(f"[{k}:v]format=rgba[i{k}];{ult}[i{k}]overlay=0:{y}:format=auto{en}{o}"); return o
    for f, a, b, y in L: ult = ov(a, b, y, ult, k); k += 1
    fc.append(f"{ult}ass=leg.ass:fontsdir=fonts[leg]"); ult = "[leg]"
    for f, a, b, y in C: ult = ov(a, b, y, ult, k); k += 1
    fc.append(f"{ult}format=yuv420p[v]"); (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS,
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{total:.2f} s")


def folha(total):
    fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    n = 30
    for k in range(n):
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(k + 0.5) * total / n:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=360:640", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", f"tile={n}x1", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


def narracion(S, total):
    mm = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"; lin = []
    for s in S:
        if s["tipo"] == "fala": lin.append(f"[{mm(s['palavras'][0]['ini'])}] {s['nome']}: {s['texto']}")
        for nome, txt, t in s.get("narr", []): lin.append(f"[{mm(s['T0'] + t)}] {nome}: {txt}")
        if s["tipo"] == "mudo" and s.get("desc"): lin.append(f"[{mm(s['T0'])}] (sin voz) {s['desc']}")
    cab = (f"NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})\n"
           "Tiempos = momento en que empieza cada frase en el video final. Texto = ROTEIRO_PERSONAS_v2 (P0 · DON AURELIO).\n"
           "Personajes ficticios: REPORTERA (PiP al inicio, luego en la calle), AGRESOR, DON AURELIO (vendedor de hot dog). Sello \"VIDEO FICTICIO\" todo el video.\n"
           "Voces: reportera Gabriela (ElevenLabs) · don Aurelio Santiago (ElevenLabs) en el testimonio · agresor y Aurelio en la pelea = audio nativo Seedance.\n"
           "Título 0–3 s: \"LO HUMILLARON POR SU FE… AL DÍA SIGUIENTE PASÓ ESTO\". Flechas TOCA «VER MÁS» desde el CTA hasta el final; nada se dice después del CTA.\n")
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


if __name__ == "__main__":
    S, PL, total = timeline()
    cta_t = next(s["T0"] for s in S if s.get("cta"))
    json.dump(dict(total=total, cta_t=cta_t, segs=[{k: s.get(k) for k in ("id", "tipo", "T0", "T1", "uso", "video")} for s in S], planos=PL),
              open(AQ / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for p in PL: print(f"  {p['q0'] / FPS:6.2f} +{p['n'] / FPS:5.2f} {p['id']:28s} vt {p['vt']:6.2f} z{p['zoom']}")
    print("TOTAL", total, "CTA", cta_t)
    if "--so-plano" in sys.argv: sys.exit()
    legenda(S, total, cta_t)
    corpo(PL); audio(S, total); video(total, cta_t); print(narracion(S, total)); folha(total)
