# -*- coding: utf-8 -*-
"""Montagem P6 · DON ERNESTO (mesero) -> v5-personas/SB-ES_HUMILLACION_P6-ERNESTO_FICTICIO.mp4 (+ _narracion.txt, _frames.jpg).
Moldura de post "Fe en Noticias" o vídeo todo (plate + header da v4), janela 720x840 em y=297.
Sequência (plano.json): abertura (PiP + briga Seedance) -> virada sem fala (mãos/vazio/2 mesas/cheio, trilha triste -> esperança)
-> R01 reportera -> Ernesto J1..J4 (HeyGen; trechos sobre b-roll inédito) -> CTA reportera (setas até o fim).
Legenda palavra a palavra pelo roteiro (estilo v4), título 0-3 s, selo VIDEO FICTICIO o vídeo todo.
Uso: python montar_p6.py [--so-plano]"""
import json, re, subprocess, sys, difflib
from pathlib import Path
import numpy as np
from PIL import Image

AQ = Path(__file__).resolve().parent; V5 = AQ.parents[1]; RAIZ = V5.parent
G = RAIZ / "_trabalho" / "graficos"; GB = RAIZ / "v3" / "_trabalho" / "final_B" / "graficos"
M = AQ / "mont"; M.mkdir(exist_ok=True)
OUT = V5 / "SB-ES_HUMILLACION_P6-ERNESTO_FICTICIO.mp4"
FPS, SR = 30, 48000
WIN = (0, 297, 720, 840)
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
PL = json.loads((AQ / "plano.json").read_text(encoding="utf-8"))


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


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout.strip())


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def texto_roteiro(P, txt):
    """troca as palavras (whisper/alinhamento) pelas do roteiro mantendo os tempos"""
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
    """itens de fala em sequência; cada item: audio (arquivo), palavras (tempo do arquivo), uso [a,b], gap antes, planos de vídeo
    relativos ao item (de, ate em tempo do arquivo de áudio) -> tempo final"""
    t = 0.0; S = []
    for it in PL["itens"]:
        it = dict(it); g = it.get("gap", 0.0) if S else 0.0
        t += g; it["T0"] = round(t, 4)
        u0, u1 = it["uso"]; t += u1 - u0; it["T1"] = round(t, 4)
        S.append(it)
    total = round(round((t + PL.get("cauda", 0.6)) * FPS) / FPS, 4)
    return S, total


def planos(S, total):
    """cada plano: fonte, vt (tempo na fonte), [t0,t1) final, zoom, vel; o vídeo de um item vai do seu T0 até o T0 do próximo"""
    L = []
    for k, it in enumerate(S):
        V0 = it["T0"]; V1 = S[k + 1]["T0"] if k + 1 < len(S) else total
        u0 = it["uso"][0]
        for p in it["video"]:
            a = V0 + (p["de"] - u0) if p.get("de") is not None else V0
            b = V0 + (p["ate"] - u0) if p.get("ate") is not None else V1
            a, b = max(a, V0), min(b, V1)
            if b - a < 0.05: continue
            vt = p.get("vt", 0.0) if "vt" in p else (p.get("off", 0.0) + u0 + (a - V0))
            L.append(dict(t0=a, t1=b, file=str(AQ / p["fonte"]), vt=vt, zoom=p.get("zoom", 1.0), vel=p.get("vel", 1.0), tipo=p.get("tipo", "video"),
                          id=p.get("id", Path(p["fonte"]).stem), item=it["id"], broll=p.get("broll", False), kb=p.get("kb", 0.0),
                          cy=p.get("cy", 0.5)))
    for p in L: p["q0"] = round(p["t0"] * FPS)
    for k, p in enumerate(L): p["n"] = (L[k + 1]["q0"] if k + 1 < len(L) else round(total * FPS)) - p["q0"]
    return [p for p in L if p["n"] > 0]


def render(p, out):
    n = p["n"]; W, H = WIN[2], WIN[3]
    if p["tipo"] == "img":
        fc = (f"[0:v]scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
              f"zoompan=z='1+{p['kb'] or 0.05}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30,"
              f"trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[v]")
        ins = ["-loop", "1", "-framerate", "30", "-t", f"{n / 30 + 0.3:.3f}", "-i", p["file"]]
    else:
        vel = p["vel"]; ins = ["-ss", f"{max(0, p['vt']):.3f}", "-t", f"{n / 30 * vel + 0.4:.3f}", "-i", p["file"]]
        v = f"[0:v]setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}:(iw-{W})/2:(ih-{H})*{p['cy']}"
        z = p["zoom"]
        if z > 1.0: v += f",scale={int(W * z) // 2 * 2}:{int(H * z) // 2 * 2}:flags=lanczos,crop={W}:{H}:(iw-{W})/2:(ih-{H})*0.35"
        if p["kb"]:
            v += f",scale={W * 2}:{H * 2}:flags=lanczos,zoompan=z='1+{p['kb']}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30"
        fc = v + f",format=yuv420p,tpad=stop_mode=clone:stop=3,trim=end_frame={n},setpts=PTS-STARTPTS[v]"
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-frames:v", n, "-r", FPS,
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", "-pix_fmt", "yuv420p", *TAG, "-an", out])
    k = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out]).stdout)
    if k != n: print(f"   !!! {out.name}: {k}/{n} quadros"); sys.exit(1)


def janela(Lp):
    for f in M.glob("p_*.mp4"): f.unlink()
    lista = []
    for k, p in enumerate(Lp):
        o = M / f"p_{k:03d}.mp4"; render(p, o); lista.append(o)
        print(f"  [{k + 1}/{len(Lp)}] {p['t0']:6.2f} {p['n']:4d}q {p['id']} vt {p['vt']:.2f} z{p['zoom']}", flush=True)
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in lista), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "janela.mp4"])


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)); voz = np.zeros((N, 2), np.float32); amb = np.zeros((N, 2), np.float32)
    for it in S:
        if not it.get("audio"): continue
        u0, u1 = it["uso"]; a = fade(load(AQ / it["audio"], u0, u1 - u0))
        a *= 10 ** ((it.get("lufs", -15.0) - lufs(a)) / 20); s = int(it["T0"] * SR); n = min(len(a), N - s); voz[s:s + n] += a[:n]
    def pos(arq, t0, t1, db, fi=0.05, fo=0.6, ss=0.0, env=None):
        a = load(AQ / arq, ss)
        need = int((t1 - t0) * SR)
        while len(a) < need: a = np.concatenate([a, a])                      # loop simples (bed/ambiente)
        a = a[:need].copy(); a *= 10 ** ((db - lufs(a)) / 20)
        ni, no = int(fi * SR), int(fo * SR)
        if ni: a[:ni] *= np.linspace(0, 1, ni)[:, None]
        if no: a[-no:] *= np.linspace(1, 0, no)[:, None]
        if env: a *= np.interp(np.arange(len(a)) / SR + t0, env[0], env[1]).astype(np.float32)[:, None]
        s = int(t0 * SR); n = min(len(a), N - s); amb[s:s + n] += a[:n]
    by = {it["id"]: it for it in S}
    def tref(x):
        if isinstance(x, (int, float)): return float(x)
        m = re.match(r"^(\w+?)(\.fim)?([+-][\d.]+)?$", x); it = by[m.group(1)]
        return (it["T1"] if m.group(2) else it["T0"]) + float(m.group(3) or 0)
    for m in PL["musica"]:
        t0, t1 = tref(m["t0"]), min(tref(m["t1"]) if m["t1"] != "fim" else total, total)
        env = None
        if m.get("duck"): env = ([tref(x[0]) for x in m["duck"]], [10 ** (x[1] / 20) for x in m["duck"]])
        pos(m["arquivo"], t0, t1, m["lufs"], m.get("fi", 0.05), m.get("fo", 0.6), m.get("ss", 0.0), env)
    mix = voz + amb; mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"])
    raw.unlink()


# ------------------------------------------------------------------ legenda (estilo v4)
FS, Y_POST, Y_CTA = 64, 1072, 840
MAXP, MAXC = 3, 18
JUNTAR = [(["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["don", "ernesto"], "don ernesto"), (["juan", "méndez"], "juan méndez")]


def palavras_tl(S):
    out = []
    for it in S:
        u0, u1 = it["uso"]
        for p in it["palavras"]:
            if p["ini"] < u0 - 0.05 or p["ini"] > u1: continue
            w = limpa(p["w"])
            if not w: continue
            out.append(dict(w=w, raw=p["w"], ini=it["T0"] + p["ini"] - u0, fim=it["T0"] + p["fim"] - u0, linha=f"{it['id']}:{p.get('frase', '')}:{p.get('quem', '')}", tfim=it["T1"]))
    res, k = [], 0
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
    fix = []
    for b in B:
        if fix and len(b) == 1 and len(fix[-1]) < MAXP and fix[-1][-1]["linha"] == b[0]["linha"] and not re.search(r"[.!?…:;]$", fix[-1][-1]["raw"]) \
                and len(" ".join(x["w"] for x in fix[-1] + b)) <= MAXC and b[0]["ini"] - fix[-1][-1]["fim"] < 0.4:
            fix[-1] = fix[-1] + b
        else: fix.append(b)
    return fix


def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(S, total, cta_t):
    W = palavras_tl(S); B = blocos(W); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total, b[-1].get("tfim", total) - 0.01)
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
def video(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    T = f"{total + 1:.3f}"; img = lambda p: ["-loop", "1", "-framerate", "30", "-t", T, "-i", str(p)]
    ins = ["-reinit_filter", "0", "-i", "janela.mp4", "-i", "mix.wav", *img(GB / "plate.png"), *img(G / "header.png"),
           *img(AQ / "graficos" / "titulo_gancho.png"), *img(G / "cta_txt.png"), *img(G / "cta_setas.png"), *img(G / "selo.png")]
    a = cta_t - 1 / 60
    fc = [f"[2:v]fps={FPS},format=yuv420p[pl]", f"[0:v]setpts=N/({FPS}*TB)[w]",
          f"[pl][w]overlay={WIN[0]}:{WIN[1]}:shortest=0:eof_action=pass[b0]",
          "[3:v]format=rgba[hd]", "[b0][hd]overlay=0:0[b1]",
          "[4:v]format=rgba[ti]", f"[b1][ti]overlay=0:0:enable='lt(t,{PL['titulo_ate']:.3f})'[b2]",
          "[b2]ass=leg.ass:fontsdir=fonts[b3]",
          "[5:v]format=rgba[ct]", f"[b3][ct]overlay=0:-22:enable='gte(t,{a:.4f})'[b4]",
          "[6:v]format=rgba[se]", f"[b4][se]overlay=0:'-37+10*sin(2*PI*1.4*t)':enable='gte(t,{a:.4f})'[b5]",
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
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(k + 0.5) * total / n:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=360:640", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", f"tile={n}x1", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


def narracion(S, total):
    mm = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"
    lin = []
    for it in S:
        u0 = it["uso"][0]
        for fr in it.get("frases", []):
            P = [p for p in it["palavras"] if p.get("frase") == fr["id"]]
            t = it["T0"] + (P[0]["ini"] - u0 if P else 0)
            lin.append(f"[{mm(t)}] {fr['quem']}: {fr['texto']}")
    cab = f"""NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})
Lote "Humillación" v5 · P6 DON ERNESTO (mesero). Tiempos = momento en que empieza cada frase en el video final.
Personajes ficticios: REPORTERA (en PiP desde 0:00 y luego en el lugar), CLIENTE (agresor), DON ERNESTO (mesero, 55 años).
Sello "VIDEO FICTICIO" arriba a la derecha durante todo el video. Moldura de post "Fe en Noticias" todo el video.
Voces: reportera Gabriela (ElevenLabs hHjbwzYZW17oh0p05AKv) · don Ernesto Jose (ElevenLabs lQFpy8cEH4bDaHre2DpA, acento mexicano) ·
cliente en la pelea: voz nativa del Seedance; don Ernesto en la pelea: Seedance convertido a la voz Jose (speech-to-speech).
{PL['nota_virada']}
Título 0–{PL['titulo_ate']:.0f} s: "LO HUMILLARON POR SU FE… / AL DÍA SIGUIENTE PASÓ ESTO". CTA único al final (flechas TOCA «VER MÁS» desde el CTA hasta el último cuadro); nada se dice después.
"""
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


def preparar(S):
    for it in S:
        P = []
        for fr in it.get("frases", []):
            src = [dict(p, frase=fr["id"], quem=fr["quem"]) for p in it["palavras_fonte"] if p.get("frase", fr["id"]) == fr["id"]]
            P += texto_roteiro(src, fr["texto"]) if src else []
            for p in P: p.setdefault("frase", fr["id"]); p.setdefault("quem", fr["quem"])
        it["palavras"] = P


if __name__ == "__main__":
    S, total = timeline()
    for it in S:
        js = json.loads((AQ / it["palavras_json"]).read_text(encoding="utf-8")) if it.get("palavras_json") else []
        it["palavras_fonte"] = js["palavras"] if isinstance(js, dict) else js
    preparar(S)
    Lp = planos(S, total)
    cta = next(it for it in S if it["id"] == "RCTA"); cta_t = round(round(cta["T0"] * FPS) / FPS, 4)
    rep = {}
    for p in Lp:
        if p["broll"]: rep.setdefault(p["id"], []).append(round(p["t0"], 2))
    probs = [f"b-roll {k} usado {len(v)}x em {v}" for k, v in rep.items() if len(v) > 1]
    for it in S: print(f"{it['T0']:7.2f}-{it['T1']:7.2f} {it['id']:6s} {' '.join(p['w'] for p in it['palavras'])[:90]}")
    for p in Lp: print(f"   {p['q0'] / 30:7.2f} +{p['n'] / 30:5.2f} {p['id']:22s} vt {p['vt']:6.2f} z {p['zoom']} {'BROLL' if p['broll'] else ''}")
    print("TOTAL", total, "CTA", cta_t, "| repetições:", probs or "nenhuma")
    json.dump(dict(total=total, cta_t=cta_t, planos=Lp, itens=[{k: it.get(k) for k in ("id", "T0", "T1", "uso", "audio")} for it in S], repeticoes=probs),
              open(AQ / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--so-plano" in sys.argv: sys.exit()
    legenda(S, total, cta_t); janela(Lp); audio(S, total); video(total, cta_t); print(narracion(S, total)); folha(total)
