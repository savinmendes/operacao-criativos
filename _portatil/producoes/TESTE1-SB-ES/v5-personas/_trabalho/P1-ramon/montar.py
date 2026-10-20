# -*- coding: utf-8 -*-
"""P1 Ramón (taxista) - lote Humillación v5. Montagem no estilo v4-B (moldura de post o vídeo todo, janela 720x840 em y=297).
Segmentos: abertura (reportera PiP + briga Seedance) -> virada sem fala (mãos/vazio/dois/fila) -> reportera R01 -> Ramón (RA1, RA2, PEDa, PEDb)
-> reportera CTA (setas do início da fala até o fim). Legenda palavra a palavra pelo roteiro, selo VIDEO FICTICIO, título 0-3 s.
Uso: python montar.py [--so-plano] [--so-final]"""
import json, re, subprocess, sys, difflib
from pathlib import Path
import numpy as np

AQ = Path(__file__).resolve().parent; RAIZ = AQ.parents[2]; V5 = AQ.parents[1]
A = AQ / "audio"; T = AQ / "takes"; M = AQ / "mont"; M.mkdir(exist_ok=True)
G = RAIZ / "_trabalho" / "graficos"; GV = RAIZ / "v3" / "_trabalho" / "final_B" / "graficos"
OUT = V5 / "SB-ES_HUMILLACION_P1-RAMON_FICTICIO.mp4"
FPS, SR = 30, 48000
WIN = (0, 297, 720, 840)
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
ARGS = sys.argv[1:]
PLANO = json.loads((AQ / "plano.json").read_text(encoding="utf-8"))


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:2000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=0.0, t=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < SR // 2: a = np.concatenate([a, np.zeros((SR // 2 - len(a), 2), np.float32)])
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    raw.unlink(); l = [x for x in r.stderr.splitlines() if x.strip().startswith("I:")]
    v = float(l[-1].split()[1]); return v if v > -70 else -70.0


def fade(a, ms=12):
    n = min(int(ms / 1000 * SR), len(a) // 2)
    if n: a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout.strip())


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def texto_roteiro(P, txt):
    """palavras (com tempo) -> texto exato do roteiro mantendo os tempos (1:1 ou difflib)"""
    R = txt.split()
    if len(R) == len(P): return [dict(p, w=r) for p, r in zip(P, R)]
    a = [limpa(p["w"]) for p in P]; b = [limpa(r) for r in R]; out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal": out += [dict(P[i1 + k], w=R[j1 + k]) for k in range(i2 - i1)]
        elif j2 > j1 and i2 > i1:
            t0, t1 = P[i1]["ini"], P[i2 - 1]["fim"]; L = [len(limpa(R[j])) + 1 for j in range(j1, j2)]; s = sum(L); t = t0
            for k, j in enumerate(range(j1, j2)): d = (t1 - t0) * L[k] / s; out.append(dict(w=R[j], ini=round(t, 3), fim=round(t + d, 3))); t += d
        elif j2 > j1:
            t = out[-1]["fim"] if out else P[0]["ini"]
            for j in range(j1, j2): out.append(dict(w=R[j], ini=t, fim=t + 0.01))
    return out


# ------------------------------------------------------------------ timeline
def timeline():
    S = []; t = 0.0
    for s in PLANO["segmentos"]:
        s = dict(s); s["gap"] = s.get("gap", 0.0); t += s["gap"]
        s["T0"] = round(round(t * FPS) / FPS, 4); s["n"] = int(round(s["dur"] * FPS)); t = s["T0"] + s["n"] / FPS
        P = []
        for f in s.get("falas", []):                              # {json, off (no segmento), texto}
            j = json.loads((AQ / f["json"]).read_text(encoding="utf-8")); W = j["palavras"] if isinstance(j, dict) else j
            W = [dict(w=p["w"], ini=p["ini"] + f.get("off", 0.0), fim=p["fim"] + f.get("off", 0.0), linha=f["id"]) for p in W
                 if f.get("de", -1) <= p["ini"] <= f.get("ate", 1e9)]
            W = texto_roteiro(W, f["texto"]) if f.get("texto") else W
            P += [dict(p, linha=f["id"]) for p in W]
        s["palavras"] = P; S.append(s)
    return S, round(t, 4)


# ------------------------------------------------------------------ vídeo
def render(s, out):
    n = s["n"]; src = AQ / s["video"]
    if s.get("img"):
        ins = ["-loop", "1", "-framerate", "30", "-t", f"{n / 30 + 0.3:.3f}", "-i", src]
        z = s.get("kb", 0.05)
        v = (f"[0:v]scale={WIN[2] * 2}:{WIN[3] * 2}:force_original_aspect_ratio=increase,crop={WIN[2] * 2}:{WIN[3] * 2},"
             f"zoompan=z='1+{z}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={WIN[2]}x{WIN[3]}:fps=30")
    else:
        vel = s.get("vel", 1.0)
        ins = ["-ss", f"{s['ss']:.3f}", "-t", f"{n / 30 * vel + 0.5:.3f}", "-i", src]
        cx, cy = s.get("cx", 0.5), s.get("cy", 0.5)
        v = (f"[0:v]setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS},scale={WIN[2]}:{WIN[3]}:force_original_aspect_ratio=increase:flags=lanczos,"
             f"crop={WIN[2]}:{WIN[3]}:(iw-{WIN[2]})*{cx}:(ih-{WIN[3]})*{cy}")
        z = s.get("zoom", 1.0)
        if z > 1.0:
            v += (f",scale={int(WIN[2] * z) // 2 * 2}:{int(WIN[3] * z) // 2 * 2}:flags=lanczos,"
                  f"crop={WIN[2]}:{WIN[3]}:{int(WIN[2] / 2 * (z - 1))}:{int(WIN[3] * s.get('zy', 0.35) * (z - 1))}")
    fc = v + f",format=yuv420p,tpad=stop_mode=clone:stop=3,trim=end_frame={n},setpts=PTS-STARTPTS[v]"
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-frames:v", n, "-r", FPS,
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", "-pix_fmt", "yuv420p", *TAG, "-an", out])
    k = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out]).stdout)
    if k != n: print(f"!!! {out.name}: {k}/{n} quadros"); sys.exit(1)


def planos(S):
    """segmentos de fala do Ramón: zoom 100/112 alternado por frase (cortes entre palavras)"""
    L = []; z = 0
    for s in S:
        if not s.get("frases"): L.append(s); continue
        P = [p for p in s["palavras"]]; cortes = [0.0]
        for x, y in zip(P, P[1:]):
            if re.search(r"[.!?…,]$", x["w"]) and y["ini"] - cortes[-1] >= 1.6 and s["dur"] - y["ini"] >= 1.2:
                cortes.append(round(((x["fim"] + y["ini"]) / 2) * FPS) / FPS)
        cortes.append(s["n"] / FPS); acc = 0
        for a, b in zip(cortes, cortes[1:]):
            p = dict(s); p["ss"] = s["ss"] + a; nn = int(round(b * FPS)) - int(round(a * FPS)); p["n"] = nn
            p["zoom"] = 1.12 if z % 2 else 1.0; z += 1; p["id"] = f"{s['id']}_{len(L)}"; L.append(p)
    return L


def corpo(S):
    lista = []
    for f in M.glob("p_*.mp4"): f.unlink()
    for k, s in enumerate(planos(S)):
        out = M / f"p_{k:03d}.mp4"; render(s, out); lista.append(out); print(f"  [{k + 1}] {s['id']} {s['n']}q z{s.get('zoom', 1)}", flush=True)
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in lista), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "corpo.mp4"])


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)); mix = np.zeros((N, 2), np.float32)
    def pos(a, t0):
        s = int(round(t0 * SR)); n = max(0, min(len(a), N - s)); mix[s:s + n] += a[:n]
    for s in S:
        for x in s.get("audio", []):               # {arq, ss, t, off, lufs, duck:[[t,db],...]}
            a = load(AQ / x["arq"], x.get("ss", 0.0), x.get("t") or s["n"] / FPS - x.get("off", 0.0))
            a = fade(a, x.get("fade_ms", 12)); a *= 10 ** ((x.get("lufs", -15.0) - lufs(a)) / 20)
            if x.get("env"):
                tt = np.arange(len(a)) / SR; xs, ys = zip(*x["env"])
                a *= (10 ** (np.interp(tt, xs, ys) / 20)).astype(np.float32)[:, None]
            pos(a, s["T0"] + x.get("off", 0.0))
    for x in PLANO.get("trilhas", []):              # {arq, de, ate, lufs, fi, fo}
        d = x["ate"] - x["de"]; a = load(AQ / x["arq"], x.get("ss", 0.0))
        if x.get("loop"):
            while len(a) < d * SR: a = np.concatenate([a, load(AQ / x["arq"], 0.5)])
        a = a[:int(d * SR)]; a *= 10 ** ((x["lufs"] - lufs(a)) / 20)
        fi, fo = int(x.get("fi", 0.05) * SR), int(x.get("fo", 0.6) * SR)
        a[:fi] *= np.linspace(0, 1, fi)[:, None]; a[-fo:] *= np.linspace(1, 0, fo)[:, None]
        pos(a, x["de"])
    k = int(0.4 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"])
    raw.unlink(); print("audio ok")


# ------------------------------------------------------------------ legenda (estilo v4)
FS, Y_POST, Y_CTA = 64, 1072, 840
MAXP, MAXC = 3, 18
JUNTAR = [(["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["don", "ramón"], "don ramón"), (["juan", "méndez"], "juan méndez")]


def palavras_tl(S):
    out = []
    for s in S:
        for p in s["palavras"]:
            w = limpa(p["w"])
            if w: out.append(dict(w=w, raw=p["w"], ini=s["T0"] + p["ini"], fim=s["T0"] + p["fim"], linha=f"{s['id']}:{p['linha']}", fseg=s["T0"] + s["n"] / FPS))
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
    fix = []
    for b in B:
        if fix and len(b) == 1 and len(fix[-1]) < MAXP and fix[-1][-1]["linha"] == b[0]["linha"] and not re.search(r"[.!?…:;]$", fix[-1][-1]["raw"]) \
                and len(" ".join(x["w"] for x in fix[-1] + b)) <= MAXC and b[0]["ini"] - fix[-1][-1]["fim"] < 0.4:
            fix[-1] = fix[-1] + b
        else: fix.append(b)
    return fix


def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(S, total, cta_t):
    B = blocos(palavras_tl(S)); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total, max(b[-1]["fseg"], b[-1]["fim"] + 0.05)); y = Y_CTA if ini >= cta_t - 0.1 else Y_POST
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
    pngs = [GV / "plate.png", G / "header.png", AQ / "graficos" / "titulo_gancho.png", G / "cta_txt.png", G / "cta_setas.png", G / "selo.png"]
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    for p in pngs: ins += ["-loop", "1", "-framerate", "30", "-t", f"{total + 1:.3f}", "-i", str(p)]
    t0, t1 = PLANO.get("titulo", [0.0, 3.0]); e = lambda a, b: f":enable='gte(t,{a - 1 / 60:.4f})*lt(t,{b - 1 / 60:.4f})'"
    fc = [f"[2:v]fps={FPS},format=yuv420p[pl]", f"[0:v]setpts=N/({FPS}*TB)[c]", f"[pl][c]overlay={WIN[0]}:{WIN[1]}:shortest=1[b0]",
          "[3:v]format=rgba[hd]", "[b0][hd]overlay=0:0[b1]", "[4:v]format=rgba[ti]", f"[b1][ti]overlay=0:0{e(t0, t1)}[b2]",
          "[b2]ass=leg.ass:fontsdir=fonts[b3]", "[5:v]format=rgba[ct]", f"[b3][ct]overlay=0:-22{e(cta_t, total + 5)}[b4]",
          "[6:v]format=rgba[se]", f"[b4][se]overlay=0:'-37+10*sin(2*PI*1.4*t)'{e(cta_t, total + 5)}[b5]",
          "[7:v]format=rgba[sl]", "[b5][sl]overlay=0:0,format=yuv420p[v]"]
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS,
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{total:.2f} s")


def folha(total):
    n = 30; fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    for k in range(n):
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(k + 0.5) * total / n:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=240:426", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", "tile=10x3", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


def narracion(S, total):
    mm = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"; lin = []
    for s in S:
        for f in s.get("falas", []):
            P = [p for p in s["palavras"] if p["linha"] == f["id"]]
            if P: lin.append(f"[{mm(s['T0'] + P[0]['ini'])}] {f['quem']}: {f['texto']}")
        if s.get("sem_fala"): lin.append(f"[{mm(s['T0'])}] (sin voz) {s['sem_fala']}")
    cab = (f"NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})\n"
           "Lote \"Humillación\" v5, persona P1 DON RAMÓN (taxista). Personajes ficticios; sello \"VIDEO FICTICIO\" arriba a la derecha todo el video.\n"
           "Voces: reportera Gabriela (ElevenLabs) · Ramón Salvatore (ElevenLabs) en la entrevista · pasajero en la pelea: audio nativo del video IA; Ramón en la pelea: nativo convertido a la voz Salvatore (speech-to-speech).\n"
           f"Título 0–3 s: \"LO HUMILLARON POR SU FE… / AL DÍA SIGUIENTE PASÓ ESTO\". CTA único al final (flechas TOCA «VER MÁS» desde {mm(PLANO['_cta_t'])}); nada se dice después del CTA.\n")
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


if __name__ == "__main__":
    S, total = timeline()
    cta = next(s for s in S if s["id"] == "CTA"); cta_t = cta["T0"]; PLANO["_cta_t"] = cta_t
    for s in S: print(f"{s['T0']:7.2f} +{s['n'] / 30:5.2f} {s['id']:8s} {' '.join(p['w'] for p in s['palavras'])[:80]}")
    print("TOTAL", total, "CTA", cta_t)
    json.dump(dict(total=total, cta_t=cta_t, segmentos=[{k: s[k] for k in ("id", "T0", "n", "video")} for s in S]), open(AQ / "timeline.json", "w", encoding="utf-8"), indent=1)
    if "--so-plano" in ARGS: sys.exit()
    legenda(S, total, cta_t)
    if "--so-final" not in ARGS: corpo(S); audio(S, total)
    video(total, cta_t); print(narracion(S, total)); folha(total)
