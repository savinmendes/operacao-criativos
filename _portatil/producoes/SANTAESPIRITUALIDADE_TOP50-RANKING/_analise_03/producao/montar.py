# -*- coding: utf-8 -*-
"""Ranking 03 → SB ES «Despedida cámara». Gancho de telejornal: câmera de segurança original (faixa e rodapé ES por cima,
logo NV inventado) + mulher nova em chroma (Avatar IV em fundo verde, recolocada no lugar da original apagada com LaMa)
+ V.O. sobre os takes da câmera; selfie nova (Avatar IV chorando -> sorrindo) com b-roll original na fala da oração;
Juan Méndez (Avatar IV no cenário do padre original, moldura da live) com b-rolls originais/banco SB nas fronteiras de palavra.
B-roll com pessoa: legenda nova numa caixa opaca no lugar da antiga; sem pessoa: legenda antiga tirada com LaMa.
Saída 1 passada, matriz bt601/tv FIXA. uso: python montar.py [--so-audio] [--de s --ate s --saida x.mp4]"""
import json, re, subprocess, argparse
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent; T = P / "_trab"; T.mkdir(exist_ok=True); B = P / "broll"; OV = P / "ov"
ap = argparse.ArgumentParser(); ap.add_argument("--so-audio", action="store_true"); ap.add_argument("--de", type=float, default=0)
ap.add_argument("--ate", type=float, default=None); ap.add_argument("--saida", default=str(T / "_video.mp4")); a_ = ap.parse_args()
FPS = 30; SR = 48000
AVJ = json.load(open(P / "avatares.json", encoding="utf-8"))
W2 = [dict(w=w, ini=x, fim=y) for w, x, y in __import__("pal").pal(P / "tts" / "W2.alinhamento.json")]
def lw(w): return re.sub(r"[¡!¿?,.:;«»…]", "", w).lower()
def wsrc(av, prefix, linha=None, n=0, fim=False, exato=False):
    c = [p for p in AVJ[av]["palavras"] if (lw(p["w"]) == prefix if exato else lw(p["w"]).startswith(prefix)) and (linha is None or p["linha"] == linha)]
    return c[n]["fim" if fim else "ini"]

# ---------------- linha do tempo ----------------
SEG = []; g = 0.0
def add(dur, tipo, fonte, s0=0.0, zoom=1.0):
    global g; SEG.append(dict(g0=round(g, 4), g1=round(g + dur, 4), tipo=tipo, fonte=fonte, s0=s0, zoom=zoom)); g += dur
C_S0 = 0.15; C_FIM = AVJ["C"]["linhas"][0]["fim"] + 0.12
add(C_FIM - C_S0, "chroma", "C", C_S0)                       # mulher em chroma sobre a câmera (0..~2,3 s do original)
G_W2 = g + 0.08                                              # V.O. W2 começa logo depois
w2fim = G_W2 + W2[-1]["fim"] + 0.25
cam = [(3.00, 5.50), (5.90, 7.90), (9.60, None)]
for k, (s0, s1) in enumerate(cam):
    dur = (s1 - s0) if s1 else (w2fim - g)
    add(dur, "cam", "cam", s0)
for (s0, s1), z in zip([(0.15, 6.62)], (1.0,)):
    add(s1 - s0, "mulher", "M1", s0, z)
for (s0, s1), z in zip([(0.15, 7.46), (7.56, 14.46)], (1.0, 1.08)):
    add(s1 - s0, "mulher", "M2", s0, z)
G_JUAN = g
for (s0, s1), z in zip([(0.15, 13.02), (13.08, 25.40), (25.45, 34.62)], (1.0, 1.08, 1.0)):
    add(s1 - s0, "padre", "A", s0, z)
for (s0, s1), z in zip([(0.15, 14.56), (14.61, 23.46), (23.51, 40.20)], (1.08, 1.0, 1.08)):
    add(s1 - s0, "padre", "B", s0, z)
T_END = g; NOUT = int(round(T_END * FPS))
def g_de(av, s):
    for sg in SEG:
        if sg["fonte"] == av and sg["s0"] - 1e-6 <= s <= sg["s0"] + (sg["g1"] - sg["g0"]) + 1e-6: return sg["g0"] + s - sg["s0"]
    return None
CAIXA_BR = {"ajoelhado", "pintura", "rosario", "mar", "rezando", "bracos", "mulher_sorri", "sombra", "abraco", "multidao"}
CV_SRC = [
 ("M1", 0.15, wsrc("M1", "de", "W3") - 0.03, "rezando"),
 ("M1", wsrc("M1", "de", "W3") - 0.03, wsrc("M1", "llorando") - 0.12, "mar"),
 ("M2", wsrc("M2", "me", "W4", exato=True) - 0.04, wsrc("M2", "para", "W4") - 0.10, "sagrado_35"),
 ("A", wsrc("A", "porque", "J07") - 0.04, wsrc("A", "ya", "J07") - 0.04, "ajoelhado"),
 ("A", wsrc("A", "oh") - 0.04, wsrc("A", "guardián") - 0.03, "pintura"),
 ("A", wsrc("A", "que", "J08") - 0.04, wsrc("A", "con", "J08", exato=True) - 0.03, "cruz"),
 ("A", wsrc("A", "con", "J08", exato=True) - 0.03, wsrc("A", "alto") - 0.03, "rosario"),
 ("A", wsrc("A", "la", "J10") - 0.04, wsrc("A", "al", "J10", exato=True) - 0.03, "altar"),
 ("A", wsrc("A", "milagros") - 0.04, wsrc("A", "deudas") - 0.03, "mulher_sorri"),
 ("A", wsrc("A", "deudas") - 0.03, wsrc("A", "puertas") - 0.03, "alivio_11"),
 ("A", wsrc("A", "puertas") - 0.03, 34.62, "alivio_25"),
 ("B", wsrc("B", "no", "J11", exato=True) - 0.04, wsrc("B", "muchos") - 0.03, "vela"),
 ("B", wsrc("B", "la", "J12", exato=True) - 0.04, wsrc("B", "y", "J12", exato=True) - 0.03, "sombra"),
 ("B", wsrc("B", "y", "J12", exato=True) - 0.03, wsrc("B", "y", "J12", n=1, exato=True) - 0.03, "abraco"),
 ("B", wsrc("B", "acuérdate") - 0.04, wsrc("B", "por", "J14") - 0.03, "biblia"),
 ("B", wsrc("B", "a", "J14", n=1, exato=True) - 0.04, wsrc("B", "vuelve") - 0.03, "multidao"),
 ("B", wsrc("B", "envía") - 0.04, wsrc("B", "toca") - 0.03, "bracos"),
]
CV = [(round(g_de(av, a), 4), round(g_de(av, b), 4), n) for av, a, b, n in CV_SRC]
for c in CV: print(f"  {c[2]:12s} {c[0]:6.2f}-{c[1]:6.2f} ({c[1]-c[0]:.2f}s)")
T_ALTO = g_de("A", wsrc("A", "alto")); T_AQUI = g_de("A", wsrc("A", "aquí", fim=True))
T_POR = g_de("B", wsrc("B", "por", "J14") - 0.03); T_PASO = g_de("B", wsrc("B", "paso", "J14", n=1, fim=True, exato=True))
T_DEUT = g_de("B", wsrc("B", "deuteronomio")); T_DEUT1 = g_de("B", wsrc("B", "por", "J14") - 0.03)
T_TOCA = g_de("B", wsrc("B", "toca"))
print(f"fim {T_END:.2f}  juan {G_JUAN:.2f}  alto {T_ALTO:.2f}  vivo {T_POR:.2f}  toca {T_TOCA:.2f}")

# ---------------- palavras no tempo global (legenda) ----------------
PAL = [dict(w=p["w"], ini=round(g_de("C", p["ini"]), 3), fim=round(g_de("C", p["fim"]) or (C_FIM - C_S0), 3), q="cam") for p in AVJ["C"]["palavras"]]
PAL += [dict(w=p["w"], ini=round(G_W2 + p["ini"], 3), fim=round(G_W2 + p["fim"], 3), q="cam") for p in W2]
for av, q in (("M1", "mulher"), ("M2", "mulher"), ("A", "padre"), ("B", "padre")):
    for p in AVJ[av]["palavras"]:
        gi = g_de(av, p["ini"]); gf = g_de(av, p["fim"])
        if gi is not None: PAL.append(dict(w=p["w"], ini=round(gi, 3), fim=round(gf if gf else gi + 0.3, 3), q=q))
PAL.sort(key=lambda p: p["ini"])
json.dump(dict(seg=SEG, cv=CV, palavras=PAL, fim=T_END), open(P / "tempos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

# ---------------- leitura ----------------
class Pngs:
    def __init__(s, d):
        s.fs = sorted((B / d / "limpo").glob("f_*.png")) if (B / d / "limpo").exists() else sorted((B / d).glob("f_*.png")); s.c = {}
    def __len__(s): return len(s.fs)
    def q(s, k):
        k = max(0, min(len(s.fs) - 1, k))
        if k not in s.c:
            if len(s.c) > 8: s.c.clear()
            s.c[k] = np.asarray(Image.open(s.fs[k]).convert("RGB"))
        return s.c[k]
class Avatar:
    def __init__(s, p): s.p = p; s.pr = None; s.i = -1; s.f = None
    def quadro(s, k):
        if s.pr is not None and k < s.i:
            s.pr.kill(); s.pr = None; s.i = -1
        if s.pr is None:
            s.pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(s.p), "-vf", "scale=in_color_matrix=bt601:in_range=limited:flags=accurate_rnd+full_chroma_int,format=rgb24",
                                     "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        while s.i < k:
            b = s.pr.stdout.read(720 * 1280 * 3)
            if len(b) < 720 * 1280 * 3: break
            s.f = np.frombuffer(b, np.uint8).reshape(1280, 720, 3); s.i += 1
        return s.f
AV = {"C": Avatar(P / "mulher/C.mp4"), "M1": Avatar(P / "mulher/M1.mp4"), "M2": Avatar(P / "mulher/M2.mp4"), "A": Avatar(P / "avatar/A.mp4"), "B": Avatar(P / "avatar/B.mp4")}
HOOK = Pngs("hook")
BRP = {n: Pngs(n) for _, _, n in CV}
ORIG = str(P.parents[1] / "03_288k_DQxVwd5kbGY.mp4")
class Cam:
    """quadros do original lidos sob demanda (bt709/tv da etiqueta)"""
    def __init__(s): s.c = {}
    def q(s, t):
        k = int(round(t * 30))
        if k not in s.c:
            if len(s.c) > 4: s.c.clear()
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{k / 30:.4f}", "-i", ORIG, "-frames:v", "1", "-vf",
                                  "scale=in_color_matrix=bt709:in_range=limited:flags=accurate_rnd+full_chroma_int,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
            s.c[k] = np.frombuffer(raw[:720 * 1280 * 3], np.uint8).reshape(1280, 720, 3)
        return s.c[k]
class CamSeq:
    """leitura sequencial dos trechos da câmera (mais rápido que buscar quadro a quadro)"""
    def __init__(s, t0, dur):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-i", ORIG, "-t", f"{dur + 0.2}", "-vf",
                              "scale=in_color_matrix=bt709:in_range=limited:flags=accurate_rnd+full_chroma_int,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
        s.F = np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720, 3)
    def q(s, k): return s.F[max(0, min(len(s.F) - 1, k))]
CAMS = {sg["s0"]: CamSeq(sg["s0"], sg["g1"] - sg["g0"]) for sg in SEG if sg["tipo"] == "cam"}

# ---------------- legenda (palavra a palavra, 1 palavra verde) ----------------
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
FL = ImageFont.truetype(str(POP / "Poppins-Bold.ttf"), 42); VERDE = (24, 200, 24)
def blocos(pal):
    out, cur = [], []
    for p in pal:
        cur.append(p); txt = " ".join(lw(x["w"]) for x in cur)
        if len(cur) >= 3 or len(txt) >= 15 or re.search(r"[,.:;!?»…]$", p["w"]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
BL = []; grupos = []
for p in PAL:
    if grupos and grupos[-1][-1]["q"] == p["q"] and p["ini"] - grupos[-1][-1]["fim"] < 0.6: grupos[-1].append(p)
    else: grupos.append([p])
for gr in grupos:
    bs = blocos(gr)
    for i, b in enumerate(bs):
        ini = max(0, b[0]["ini"] - 0.04)
        prox = bs[i + 1][0]["ini"] - 0.04 if i + 1 < len(bs) else b[-1]["fim"] + 0.30
        BL.append(dict(ini=ini, fim=prox, q=b[0]["q"], ws=[(lw(x["w"]), x["ini"]) for x in b]))
BL.sort(key=lambda x: x["ini"])
for x, y in zip(BL, BL[1:]): x["fim"] = min(x["fim"], y["ini"])
_cache = {}
def leg(t):
    for k, b in enumerate(BL):
        if b["ini"] <= t < b["fim"]:
            at = max([i for i, (_, wi) in enumerate(b["ws"]) if wi <= t + 0.02] or [0]); key = (k, at)
            if key not in _cache:
                ws = [w for w, _ in b["ws"]]; esp = FL.getlength(" "); L = [FL.getlength(w) for w in ws]; tot = sum(L) + esp * (len(ws) - 1)
                im = Image.new("RGBA", (720, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 360 - tot / 2
                sh = Image.new("RGBA", (720, 110), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh); xx = x
                for w, l in zip(ws, L): ds.text((xx + 2, 58), w, font=FL, anchor="lm", fill=(0, 0, 0, 200), stroke_width=5, stroke_fill=(0, 0, 0, 200)); xx += l + esp
                im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
                for i, (w, l) in enumerate(zip(ws, L)):
                    d.text((x, 55), w, font=FL, anchor="lm", fill=VERDE if i == at else (255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0)); x += l + esp
                _cache[key] = im
            return _cache[key], b["q"]
    return None, None
# caixa opaca que cobre a legenda PT queimada dos b-rolls com pessoa (legenda PT em ~150-570 x 700-765)
CAIXA = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); ImageDraw.Draw(CAIXA).rounded_rectangle((70, 686, 650, 800), 18, fill=(14, 14, 14, 255))
Y_LEG = {"chroma": 640, "cam": 640, "mulher": 880, "padre": 690, "broll": 690, "caixa": 743}

# ---------------- sobreposições ----------------
def rgba(n): return Image.open(OV / n).convert("RGBA")
FAIXA, ROD, MOLD, SELO, ELIM, VIVO, TOCA, SETA, DEUT = (rgba(n) for n in ("faixa.png", "rodape.png", "moldura_jm.png", "selo10.png", "eliminado.png", "en_vivo.png", "toca.png", "seta.png", "deut.png"))
T_ELIM0, T_ELIM1 = T_ALTO + 0.35, T_AQUI + 0.25
def pop(im, t, t0, dur=0.18):
    u = (t - t0) / dur
    if u >= 1.6: return im
    s = 0.7 + 0.36 * min(u, 1) if u < 1 else 1.06 - 0.06 * (u - 1) / 0.6
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
def centro(base, im, cx, cy): base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
rng = np.random.default_rng(7)
def glitch(f, t):
    u = (t - T_ALTO) / 0.55
    if not (0 <= u < 1): return f
    gq = f.copy(); k = int(14 * (1 - u) + 4)
    gq[..., 0] = np.roll(f[..., 0], k, 1); gq[..., 2] = np.roll(f[..., 2], -k, 1)
    for _ in range(7):
        y = rng.integers(0, 1240); h = rng.integers(8, 48); dx = rng.integers(-60, 60); gq[y:y + h] = np.roll(gq[y:y + h], dx, 1)
    if u < 0.25: gq = np.clip(gq.astype(np.int16) + 60, 0, 255).astype(np.uint8)
    return gq
def tremor(t):
    u = t - T_ALTO
    if not (0 <= u < 0.9): return 0, 0
    a = 16 * (1 - u / 0.9); return int(a * np.sin(u * 83)), int(a * np.cos(u * 61))
def zoom(f, z, dx=0, dy=0, cy=0.42):
    if z == 1.0 and not dx and not dy: return f
    return cv2.warpAffine(f, np.float32([[z, 0, dx - 360 * (z - 1)], [0, z, dy - 1280 * cy * (z - 1)]]), (720, 1280), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
# mulher em chroma: chave de verde + supressão do verde, escala 0,66, base encostada no rodapé/borda de baixo
CK_S, CK_X, CK_Y = 0.66, 268, 1280 - int(round(1280 * 0.66))
def chroma(t):
    f = AV["C"].quadro(int(round((C_S0 + t) * 25))).astype(np.float32)
    r, gg, b = f[..., 0], f[..., 1], f[..., 2]
    d = gg - np.maximum(r, b)
    a = 1 - np.clip((d - 18) / 40, 0, 1)
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    f[..., 1] = np.minimum(gg, np.maximum(r, b) + 6)            # tira o verde que vaza no cabelo
    w, h = int(720 * CK_S), int(1280 * CK_S)
    fs = cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA); as_ = cv2.resize(a, (w, h), interpolation=cv2.INTER_AREA)
    return fs, as_
def base(t):
    for c0, c1, n in CV:
        if c0 <= t < c1:
            fr = BRP[n]; vel = max(0.5, min(1.0, len(fr) / 30 / (c1 - c0))); return fr.q(int((t - c0) * vel * 30)), ("caixa" if n in CAIXA_BR else "broll")
    sg = next((s for s in SEG if s["g0"] <= t < s["g1"]), SEG[-1])
    if sg["tipo"] == "chroma":
        bg = np.asarray(HOOK.q(int(round(t * 30)))).astype(np.float32)
        im = Image.fromarray(bg.astype(np.uint8)).convert("RGBA"); im.alpha_composite(ROD); im.alpha_composite(FAIXA)
        bg = np.asarray(im.convert("RGB")).astype(np.float32)
        fs, a = chroma(t); h, w = a.shape; y0 = CK_Y; y1 = min(1280, y0 + h); x0 = CK_X; x1 = min(720, x0 + w)
        reg = bg[y0:y1, x0:x1]; aa = a[:y1 - y0, :x1 - x0, None]
        bg[y0:y1, x0:x1] = fs[:y1 - y0, :x1 - x0] * aa + reg * (1 - aa)
        return bg.astype(np.uint8), "chroma"
    if sg["tipo"] == "cam": return CAMS[sg["s0"]].q(int(round((t - sg["g0"]) * 30))), "cam"
    s = sg["s0"] + t - sg["g0"]; f = AV[sg["fonte"]].quadro(int(round(s * 25)))
    return zoom(f, sg["zoom"], cy=0.30 if sg["tipo"] == "mulher" else 0.22), sg["tipo"]
if not a_.so_audio:
    j0 = int(round(a_.de * FPS)); j1 = NOUT if a_.ate is None else int(round(a_.ate * FPS))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "30", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
                            "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-profile:v", "high",
                            "-color_range", "tv", "-colorspace", "smpte170m", "-color_primaries", "smpte170m", "-color_trc", "smpte170m", a_.saida],
                           stdin=subprocess.PIPE)
    ult = None
    for j in range(j0, j1):
        t = j / FPS
        if j % 150 == 0: print(f"[{j}/{NOUT}] {100 * j // NOUT}%", flush=True)
        f, tipo = base(t)
        if tipo == "padre":
            f = glitch(f, t); dx, dy = tremor(t)
            if dx or dy: f = zoom(f, 1.03, dx, dy)
        im = Image.fromarray(np.ascontiguousarray(f)).convert("RGBA")
        if tipo == "cam": im.alpha_composite(ROD); im.alpha_composite(FAIXA)
        if tipo == "caixa": im.alpha_composite(CAIXA)
        if tipo == "padre": im.alpha_composite(MOLD)
        if T_ELIM0 <= t < T_ELIM1 and ((t - T_ELIM0) % 0.6) < 0.42: centro(im, ELIM, 360, 930)
        if T_DEUT <= t < T_DEUT1: centro(im, pop(DEUT, t, T_DEUT), 360, 470)
        if T_POR <= t < T_PASO + 0.1: im.alpha_composite(pop(VIVO, t, T_POR), (24, 168))
        if t >= T_TOCA:
            centro(im, pop(TOCA, t, T_TOCA), 360, 935)
            dyy = int(round(16 * np.sin(2 * np.pi * 1.6 * (t - T_TOCA))))
            for x in (200, 391): im.alpha_composite(SETA, (x, 1010 + dyy))
        lg, q = leg(t)
        if lg is not None: ult = lg
        elif tipo == "caixa": lg = ult            # caixa nunca fica vazia nas pausas: mantém a última legenda
        if lg is not None and not (t >= T_TOCA):
            im.alpha_composite(lg, (0, Y_LEG.get(tipo, Y_LEG.get(q, 690)) - 55))
        im.alpha_composite(SELO)
        enc.stdin.write(np.asarray(im.convert("RGB")).tobytes())
    enc.stdin.close(); enc.wait(); print("vídeo ok")

# ---------------- áudio ----------------
med = pyln.Meter(SR); NA = int(round(NOUT / FPS * SR))
def ld(p, mono=True): return librosa.load(str(p), sr=SR, mono=mono)[0]
def fade(s, n0, n1):
    s = s.copy(); a = int(n0 * SR); b = int(n1 * SR)
    if a: s[:a] *= np.linspace(0, 1, a) if s.ndim == 1 else np.linspace(0, 1, a)[:, None]
    if b: s[-b:] *= np.linspace(1, 0, b) if s.ndim == 1 else np.linspace(1, 0, b)[:, None]
    return s
voz = np.zeros(NA)
def put(dst, s, t0):
    i = int(round(t0 * SR)); n = min(len(s), len(dst) - i); dst[i:i + n] += s[:n]
put(voz, fade(ld(P / "tts/W2.mp3"), 0.005, 0.05), G_W2)
# selfie: de-esser + shelf -4 dB acima de 6,5 kHz (M1/M2 tinham agudos 6-10 dB acima do Juan) -> mulher/M*_de.wav
WAV = {k: ld(P / ("mulher" if k in ("C", "M1", "M2") else "avatar") / (f"{k}_de.wav" if k in ("M1", "M2") else f"{k}.wav")) for k in ("C", "M1", "M2", "A", "B")}
for sg in SEG:
    if sg["fonte"] in WAV:
        a = int(sg["s0"] * SR); n = int((sg["g1"] - sg["g0"]) * SR); put(voz, fade(WAV[sg["fonte"]][a:a + n], 0.008, 0.008), sg["g0"])
# mulher (gancho + selfie) e Juan normalizados separadamente
iJ = int(G_JUAN * SR); vm = voz[:iJ].copy(); vj = voz[iJ:].copy()
vm *= 10 ** ((-17.5 - med.integrated_loudness(vm)) / 20); vj *= 10 ** ((-18.0 - med.integrated_loudness(vj)) / 20); voz = np.concatenate([vm, vj])
def norm(y, alvo):
    y = y.T if y.ndim > 1 else np.stack([y, y], 1); return y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)
mus = np.zeros((NA, 2))
def add2(s, t0):
    i = int(round(t0 * SR)); n = min(len(s), NA - i); mus[i:i + n] += s[:n]
V4M = Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\musica")
ten = norm(ld(V4M / "tensao.mp3", False), -32.0); esp = norm(ld(V4M / "esperanca.mp3", False), -32.0)
need = T_ALTO + 0.3
if need * SR > len(ten):              # emenda a tensão com crossfade de 1 s (volta para 8 s)
    xf = int(1.0 * SR)
    while need * SR > len(ten):
        a = ten[:len(ten) - xf]; b = ten[int(8 * SR):]
        cross = ten[len(ten) - xf:] * np.linspace(1, 0, xf)[:, None] + b[:xf] * np.linspace(0, 1, xf)[:, None]
        ten = np.concatenate([a, cross, b[xf:]])
add2(fade(ten[:int(need * SR)], 0.3, 0.3), 0.0)
need_e = T_END - T_ALTO
if need_e * SR > len(esp):
    xf = int(1.0 * SR)
    while need_e * SR > len(esp):
        a = esp[:len(esp) - xf]; b = esp[int(8 * SR):]
        cross = esp[len(esp) - xf:] * np.linspace(1, 0, xf)[:, None] + b[:xf] * np.linspace(0, 1, xf)[:, None]
        esp = np.concatenate([a, cross, b[xf:]])
add2(fade(esp[:NA - int(T_ALTO * SR)], 0.5, 0.8), T_ALTO)
g_ = rng.standard_normal(int(0.38 * SR)) * 0.5; g_ = np.sign(g_) * (np.abs(g_) > 0.6) * np.repeat(rng.random(len(g_) // 400 + 1) > 0.4, 400)[:len(g_)]
g_ *= np.linspace(1, 0, len(g_)) ** 0.7; g_ *= 0.05 / (np.sqrt(np.mean(g_ ** 2)) + 1e-9); add2(np.stack([g_, g_], 1), T_ALTO)
print("tensão", round(len(ten) / SR, 1), "precisa", round(need, 1), "| esperança", round(len(esp) / SR, 1), "precisa", round(need_e, 1))
np.save(T / "_voz.npy", voz)
mix = mus + voz[:, None]
sf.write(T / "_mix.wav", mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T / "_mix.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled",
                "-ar", "48000", "-c:a", "pcm_s16le", str(T / "audio.wav")], check=True)
m2 = sf.read(T / "audio.wav")[0]
print("LUFS final", round(med.integrated_loudness(m2), 1), "| voz", round(med.integrated_loudness(voz), 1), "| trilha", round(med.integrated_loudness(mus), 1))
