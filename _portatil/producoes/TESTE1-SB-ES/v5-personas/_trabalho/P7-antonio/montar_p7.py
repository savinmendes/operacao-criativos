# -*- coding: utf-8 -*-
"""Montagem P7 DON ANTONIO (lote Humillación v5) -> v5-personas/SB-ES_HUMILLACION_P7-ANTONIO_FICTICIO.mp4 (+ _narracion.txt, _frames.jpg)
Tudo dentro da moldura de post (plate + header "Fe en Noticias"), janela 720x840 em y=297; selo VIDEO FICTICIO o vídeo todo.
Ordem: abertura (abertura.py: briga + reportera PiP) -> virada sem fala (mãos/banco da praça/vizinha com a carta/família)
-> REPORTERA (R01) -> ANTONIO entrevistado na praça (A1, A2, P1, P2, P3; zoom alternado 100/112 % entre os takes) -> REPORTERA CTA (setas até o fim).
Uso: python montar_p7.py [--so-plano]"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).resolve().parent; M = AQ / "mont"; M.mkdir(exist_ok=True); W = AQ / "w"; T = AQ / "takes"; VZ = AQ / "voz"
RAIZ = Path(r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES"); G1 = RAIZ / "_trabalho" / "graficos"; GB = RAIZ / "v3" / "_trabalho" / "final_B"
OUT = RAIZ / "v5-personas" / "SB-ES_HUMILLACION_P7-ANTONIO_FICTICIO.mp4"
FPS, SR = 30, 48000
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
WIN = (0, 297, 720, 840)
SP = 1.05                                   # aceleração leve das falas da entrevista (vídeo + áudio juntos)
VIR = [("hv_maos", 0.70, 2.97, 40), ("hv_banco", 0.30, 2.10, 60), ("hv_vizinha", 1.00, 3.60, 60), ("hv_familia", 2.60, 4.93, 60)]   # (take, ini, fim, y0 do recorte em 720x960)
FALAS = [("R01", "rep", 80, 1.00), ("A1", "ant", 60, 1.00), ("A2", "ant", 60, 1.12), ("P1", "ant", 60, 1.00), ("P2", "ant", 60, 1.12),
         ("P3", "ant", 60, 1.00), ("CTA", "rep", 80, 1.12)]      # (id, quem, y0 do recorte 720x1280->840, zoom)
RUINS = {}                                  # id -> [(ini, fim)] em tempo do take (preenchido depois da revisão)
NOME = {"R00": "REPORTERA (en PiP)", "CAJERO": "CAJERO", "ANTONIO": "DON ANTONIO", "R01": "REPORTERA", "A1": "DON ANTONIO", "A2": "DON ANTONIO",
        "P1": "DON ANTONIO", "P2": "DON ANTONIO", "P3": "DON ANTONIO", "CTA": "REPORTERA"}
ARGS = sys.argv[1:]


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:2000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout.strip())


def load(p, ss=0.0, t=None, extra=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p)] + (["-af", extra] if extra else []) + \
          ["-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < SR // 2: a = np.concatenate([a, np.zeros((SR // 2 - len(a), 2), np.float32)])
    raw = W / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    raw.unlink(); v = float([x for x in r.stderr.splitlines() if x.strip().startswith("I:")][-1].split()[1]); return v if v > -70 else -70.0


# ------------------------------------------------------------------ reportera sobre a praça (chroma)
def alfa(f):
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def fundo_praca():
    p = W / "praca_bg.png"
    if not p.exists():
        run(["ffmpeg", "-v", "error", "-y", "-ss", "0.25", "-i", T / "hv_praca_fundo.mp4", "-frames:v", "1",
             "-vf", "scale=720:1260:flags=lanczos,pad=720:1280:0:20:color=black,crop=720:1280", W / "_bg.png"])
        im = cv2.imread(str(W / "_bg.png")); im[:20] = im[20:21]                     # 768x1344 -> 720x1260 (+ borda replicada)
        im = cv2.GaussianBlur(im, (0, 0), 2.2); cv2.imwrite(str(p), im)
    return cv2.imread(str(p)).astype(np.float32)


def rep_composto(i):
    out = W / f"rep_{i}.mp4"
    if out.exists(): return out
    src = T / f"hg_{i}.mp4"; t30 = W / f"_{i}30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"fps={FPS},scale=720:1280", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    bg = fundo_praca(); fr = list(quadros(t30, 0, None, 720, 1280))
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "10", "-preset", "medium", *ENC_TAG, str(out)], stdin=subprocess.PIPE)
    for f in fr:
        fg, a = alfa(f); ff.stdin.write(np.clip(fg * a[..., None] + bg * (1 - a[..., None]), 0, 255).astype(np.uint8).tobytes())
    ff.stdin.close(); ff.wait(); return out


# ------------------------------------------------------------------ plano
def plano():
    ab = json.loads((M / "ab.json").read_text(encoding="utf-8")); S = []; t = 0.0
    q = lambda x: round(x * FPS) / FPS
    S.append(dict(id="AB", tipo="ab", file=str(M / "ab.mp4"), T0=0.0, D=q(ab["dur"]), palavras=ab["palavras"]))
    t = S[-1]["D"]
    for nm, a, b, y0 in VIR:
        d = q(b - a); S.append(dict(id=nm, tipo="vir", file=str(T / f"{nm}.mp4"), ss=a, T0=t, D=d, y0=y0, palavras=[])); t += d
    for i, quem, y0, z in FALAS:
        j = json.loads((VZ / f"{i}.json").read_text(encoding="utf-8")); P = j["palavras"]
        u1 = min(j["dur"], P[-1]["fim"] + 0.16)
        d = q(u1 / SP)
        S.append(dict(id=i, tipo=quem, file=str(rep_composto(i) if quem == "rep" else T / f"hg_{i}.mp4"), ss=0.0, T0=t, D=d, y0=y0, zoom=z,
                      audio=str(VZ / f"{i}.wav"), u1=u1, palavras=[dict(w=p["w"], ini=t + p["ini"] / SP, fim=t + p["fim"] / SP, quem=i) for p in P]))
        t += d
    for s in S:
        if s["tipo"] == "ab": s["palavras"] = [dict(p) for p in s["palavras"]]
    return S, round(t, 4)


def render(s, out):
    n = int(round(s["D"] * FPS))
    if s["tipo"] == "ab":
        run(["ffmpeg", "-v", "error", "-y", "-i", s["file"], "-vf", f"fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p", "-frames:v", n,
             "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *TAG, "-an", out]); return n
    if s["tipo"] == "vir":
        v = f"setpts=PTS-STARTPTS,fps={FPS},scale=720:960:flags=lanczos,crop=720:840:0:{s['y0']}"
    else:
        sp = SP if s["tipo"] in ("ant", "rep") else 1.0
        z = s.get("zoom", 1.0); y0 = s["y0"]
        v = f"setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale=720:1280:flags=lanczos"
        if z > 1.0:
            W2, H2 = int(720 * z) // 2 * 2, int(1280 * z) // 2 * 2
            v += f",scale={W2}:{H2}:flags=lanczos,crop=720:840:{(W2 - 720) // 2}:{int(y0 * z + 0.10 * 840 * (z - 1))}"
        else: v += f",crop=720:840:0:{y0}"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s.get('ss', 0):.3f}", "-i", s["file"], "-vf", v + f",format=yuv420p,tpad=stop_mode=clone:stop=6,trim=end_frame={n}",
         "-frames:v", n, "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *TAG, "-an", out])
    return n


def corpo(S):
    L = []
    for k, s in enumerate(S):
        o = M / f"s_{k:02d}.mp4"; n = render(s, o); L.append(o)
        print(f"  [{k + 1}/{len(S)}] {s['T0']:6.2f} {s['id']:10s} {n}q", flush=True)
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in L), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "corpo.mp4"])


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)); mix = np.zeros((N, 2), np.float32)
    def pos(a, t0):
        s = int(round(t0 * SR)); n = min(len(a), N - s)
        if n > 0: mix[s:s + n] += a[:n]
    by = {s["id"]: s for s in S}
    pos(load(M / "ab.wav"), 0.0)
    for s in S:
        if s["tipo"] in ("ant", "rep"):
            a = load(s["audio"], 0.0, s["u1"], f"atempo={SP}" if SP != 1.0 else None)
            k = int(0.01 * SR); a[-k:] *= np.linspace(1, 0, k)[:, None]
            a *= 10 ** ((-15 - lufs(a)) / 20); pos(a, s["T0"])
    # trilha: triste nas mãos/banco -> esperança da vizinha até a reportera (abaixa sob a fala e some)
    tv = by["hv_maos"]["T0"]; te = by["hv_vizinha"]["T0"]; tr = by["R01"]["T0"]; xf = int(0.8 * SR)
    tri = load(GB / "trilha" / "triste_1.mp3"); tri *= 10 ** ((-16.5 - lufs(tri)) / 20)
    nt = min(len(tri), int((te - tv + 0.8) * SR)); tri = tri[:nt].copy()
    tri[:int(0.25 * SR)] *= np.linspace(0, 1, int(0.25 * SR))[:, None]; tri[-xf:] *= np.linspace(1, 0, xf)[:, None]; pos(tri, tv - 0.15)
    es = load(GB / "trilha" / "esperanca_1.mp3"); es *= 10 ** ((-17.5 - lufs(es)) / 20)
    ne = min(len(es), int((tr + 2.4 - te) * SR)); es = es[:ne].copy(); es[:xf] *= np.linspace(0, 1, xf)[:, None]
    env = np.ones(ne, np.float32); i0 = int((tr - 0.3 - te) * SR)
    if 0 < i0 < ne: env[i0:] = np.linspace(1, 10 ** (-12 / 20), ne - i0)
    es *= env[:, None]; es[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))[:, None]; pos(es, te)
    # ambiente da praça (bem baixo) sob a reportera e a entrevista
    amb = load(T / "hv_praca_fundo.mp4"); amb = np.concatenate([amb, amb[::-1], amb, amb[::-1], amb, amb[::-1], amb, amb[::-1], amb, amb[::-1]])
    t0 = tr; need = N - int(t0 * SR); amb = amb[:need].copy()
    if lufs(amb) > -60: amb *= 10 ** ((-40 - lufs(amb)) / 20); amb[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))[:, None]; pos(amb, t0)
    mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
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
JUNTAR = [(["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["don", "antonio"], "don antonio"), (["juan", "méndez"], "juan méndez")]


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def palavras_tl(S):
    out = []
    for s in S:
        for p in s["palavras"]:
            w = limpa(p["w"]); w = "Dios" if w == "dios" else w
            if w: out.append(dict(w=w, raw=p["w"], ini=p["ini"], fim=p["fim"], linha=p["quem"]))
    res, k = [], 0
    while k < len(out):
        for seq, rep in JUNTAR:
            if [x["w"] for x in out[k:k + len(seq)]] == seq and len({x["linha"] for x in out[k:k + len(seq)]}) == 1:
                res.append(dict(out[k], w=rep, fim=out[k + len(seq) - 1]["fim"], raw=out[k + len(seq) - 1]["raw"])); k += len(seq); break
        else: res.append(out[k]); k += 1
    return res


def blocos(Wd):
    B, cur = [], []
    for w in Wd:
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
    B = blocos(palavras_tl(S)); ev = []; FR = sorted(s["T0"] + s["D"] for s in S)
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total, min([f for f in FR if f >= b[-1]["fim"] - 0.01] or [total]) - 0.01)
        y = Y_CTA if ini >= cta_t - 0.1 else Y_POST
        for j, w in enumerate(b):
            a = ini if j == 0 else max(ini, w["ini"] - 0.04); e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + x["w"] for jj, x in enumerate(b))
            pop = r"\fscx85\fscy85\t(0,80,\fscx104\fscy104)\t(80,140,\fscx100\fscy100)" if j == 0 else ""
            ev.append(f"Dialogue: 1,{ts(a)},{ts(e)},L,,0,0,0,,{{\\an5\\pos(360,{y}){pop}}}{txt}")
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins SemiBold,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,2,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" % FS
    (M / "leg.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    json.dump([dict(ini=round(b[0]["ini"], 3), texto=" ".join(x["w"] for x in b)) for b in B], open(M / "leg_blocos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)


# ------------------------------------------------------------------ vídeo final
def video(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G1.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    pngs = [GB / "graficos" / "plate.png", G1 / "header.png", AQ / "graficos" / "titulo_gancho.png", G1 / "cta_txt.png", G1 / "cta_setas.png", G1 / "selo.png"]
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    for p in pngs: ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total + 1:.3f}", "-i", str(p)]
    fc = [f"[0:v]setpts=N/({FPS}*TB)[win]", "[2:v]format=rgba,fps=30[pl]", f"[pl][win]overlay={WIN[0]}:{WIN[1]}:format=auto[b0]",
          "[3:v]format=rgba[hd]", "[b0][hd]overlay=0:0:format=auto[b1]",
          "[4:v]format=rgba[ti]", "[b1][ti]overlay=0:0:format=auto:enable='lt(t,2.983)'[b2]",
          "[b2]ass=leg.ass:fontsdir=fonts[b3]",
          "[5:v]format=rgba[ct]", f"[b3][ct]overlay=0:-22:format=auto:enable='gte(t,{cta_t - 1 / 60:.4f})'[b4]",
          "[6:v]format=rgba[se]", f"[b4][se]overlay=0:'-37+10*sin(2*PI*1.4*t)':format=auto:eval=frame:enable='gte(t,{cta_t - 1 / 60:.4f})'[b5]",
          "[7:v]format=rgba[sl]", "[b5][sl]overlay=0:0:format=auto,format=yuv420p[v]"]
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
    lin = []; cur = None
    for s in S:
        for p in s["palavras"]:
            if cur is None or cur["quem"] != p["quem"]: cur = dict(quem=p["quem"], t=p["ini"], w=[]); lin.append(cur)
            cur["w"].append(p["w"])
    for c in lin:
        if c["quem"] == "R01": c["pre"] = f"[{mm(S[[x['id'] for x in S].index('hv_maos')]['T0'])}] (sin voz: Antonio junta los pedazos del papel y el rosario -> solo en el banco de la plaza -> una vecina le entrega una carta -> sonriendo con la familia a la mesa)"
    txt = [f"NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})",
           "Tiempos = momento en que empieza cada frase en el video final. Texto = ROTEIRO_PERSONAS_v2.md, P7 DON ANTONIO (jubilado).",
           "Personajes ficticios: REPORTERA, CAJERO (banco genérico, sin marca) y DON ANTONIO. Sello \"VIDEO FICTICIO\" todo el video.",
           "Voces: reportera Gabriela (ElevenLabs) · don Antonio Pa Gabriel (ElevenLabs; en la pelea, voz nativa convertida con speech-to-speech) · cajero voz nativa del take.",
           "Título 0–3 s: \"LO HUMILLARON POR SU FE… DÍAS DESPUÉS PASÓ ESTO\". CTA único al final (flechas TOCA «VER MÁS» desde el CTA hasta el final).", ""]
    for c in lin:
        if c.get("pre"): txt.append(c["pre"])
        txt.append(f"[{mm(c['t'])}] {NOME.get(c['quem'], c['quem'])}: {' '.join(c['w'])}")
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text("\n".join(txt) + "\n", encoding="utf-8"); return p


if __name__ == "__main__":
    S, total = plano()
    cta_t = next(s["T0"] for s in S if s["id"] == "CTA")
    for s in S: print(f"{s['T0']:7.2f} +{s['D']:5.2f} {s['id']}")
    print("TOTAL", total, "CTA", cta_t)
    json.dump(dict(total=total, cta_t=cta_t, itens=[{k: v for k, v in s.items() if k != "palavras"} for s in S]), open(AQ / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--so-plano" in ARGS: sys.exit()
    legenda(S, total, cta_t); corpo(S); audio(S, total); video(total, cta_t); print(narracion(S, total)); folha(total)
