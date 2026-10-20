# -*- coding: utf-8 -*-
"""Ranking 02 → SB ES «Jefe humilla». Briga original (patrão com lipsync colado só na boca, legenda PT coberta por caixa opaca,
faixa vermelha ES por cima da PT) + plano aberto original (jump cuts) + selfie nova (Avatar IV, jump cuts nas pausas)
+ Juan Méndez (Avatar IV no cenário do padre, moldura da live) com b-rolls originais (legenda PT tirada com LaMa) nas
fronteiras de palavra. Saída 1 passada, matriz bt601/tv FIXA. uso: python montar.py [--so-audio] [--de s --ate s --saida x.mp4]"""
import json, re, subprocess, argparse
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent; T = P / "_trab"; T.mkdir(exist_ok=True); B = P / "broll"; OV = P / "ov"
ORIG = P.parents[1] / "02_331k_DR0OM-REWzS.mp4"
ap = argparse.ArgumentParser(); ap.add_argument("--so-audio", action="store_true"); ap.add_argument("--de", type=float, default=0)
ap.add_argument("--ate", type=float, default=None); ap.add_argument("--saida", default=str(T / "_video.mp4")); a_ = ap.parse_args()
FPS = 30; SR = 48000
AVJ = json.load(open(P / "avatares.json", encoding="utf-8"))
P1 = [dict(w=w, ini=x, fim=y) for w, x, y in __import__("pal").pal(P / "tts" / "P1.alinhamento.json") if not w.startswith("[")]
TEMPO_P = 1.08; P_A0 = 0.04            # es_P.wav = P1.mp3 a partir de 0,04 s com atempo 1,08
def lw(w): return re.sub(r"[¡!¿?,.:;«»…]", "", w).lower()
def wsrc(av, prefix, linha=None, n=0, fim=False, exato=False):
    c = [p for p in AVJ[av]["palavras"] if (lw(p["w"]) == prefix if exato else lw(p["w"]).startswith(prefix)) and (linha is None or p["linha"] == linha)]
    return c[n]["fim" if fim else "ini"]

# ---------------- linha do tempo (segmentos de base) ----------------
# cada segmento: g0, g1, tipo, fonte, s0 (tempo na fonte em g0), zoom
SEG = []; g = 0.0
def add(dur, tipo, fonte, s0=0.0, zoom=1.0):
    global g; SEG.append(dict(g0=round(g, 4), g1=round(g + dur, 4), tipo=tipo, fonte=fonte, s0=s0, zoom=zoom)); g += dur
add(7.10, "briga", "briga")
add(2.20, "aberto", "w1"); add(2.30, "aberto", "w2")
M_OFF_INI = 0.30                         # «Sí» entra 0,30 s depois do início do w3
M_S0 = 1.62                              # selfie começa no «Pero»
w3dur = M_S0 - 0.25 + M_OFF_INI          # w3 vai até o corte para a selfie
add(w3dur, "aberto", "w3")
G_MSI = g - (M_S0 - 0.25) - 0.25        # tempo global do src 0 do áudio M (parte do plano aberto)
for (s0, s1), z in zip([(M_S0, 5.12), (5.60, 10.86), (11.12, 16.31)], (1.0, 1.08, 1.0)):
    add(s1 - s0, "mulher", "M", s0, z)
G_JUAN = g
for (s0, s1), z in zip([(0.20, 7.32), (7.55, 30.62)], (1.0, 1.08)):
    add(s1 - s0, "padre", "A", s0, z)
add(26.30 - 0.20, "padre", "B", 0.20, 1.0)
T_END = g; NOUT = int(round(T_END * FPS))
def g_de(av, s):
    for sg in SEG:
        if sg["fonte"] == av and sg["s0"] <= s <= sg["s0"] + (sg["g1"] - sg["g0"]) + 1e-6: return sg["g0"] + s - sg["s0"]
    return None
# coberturas (b-roll em tela cheia) em tempo de fonte do avatar
CV_SRC = [
 ("A", wsrc("A", "capaz") - 0.04, wsrc("A", "y", "J06") - 0.03, "jesus"),
 ("A", wsrc("A", "oh") - 0.04, wsrc("A", "guardián") - 0.03, "vela"),
 ("A", wsrc("A", "que", "J07") - 0.04, wsrc("A", "con", "J07", exato=True) - 0.03, "cruz"),
 ("A", wsrc("A", "con", "J07", exato=True) - 0.03, wsrc("A", "alto") - 0.03, "igreja"),
 ("A", wsrc("A", "la", "J08") - 0.02, wsrc("A", "esta") - 0.04, "leitura"),
 ("A", wsrc("A", "por", "J09") - 0.04, wsrc("A", "solo", "J09") - 0.03, "manuscrito"),
 ("A", wsrc("A", "solo", "J09") - 0.03, 30.62, "procissao"),
 ("B", wsrc("B", "recibimos") - 0.04, wsrc("B", "pero") - 0.03, "wa"),
 ("B", wsrc("B", "tiene") - 0.03, wsrc("B", "por") - 0.03, "maos"),
 ("B", wsrc("B", "y", "J12") - 0.03, wsrc("B", "vuelve") - 0.03, "bracos"),
 ("B", wsrc("B", "envía") - 0.03, wsrc("B", "toca") - 0.03, "nuvens"),
]
CV = [(round(g_de(av, a), 4), round(g_de(av, b), 4), n) for av, a, b, n in CV_SRC]
for c in CV: print(f"  {c[2]:10s} {c[0]:6.2f}-{c[1]:6.2f} ({c[1]-c[0]:.2f}s)")
T_ALTO = g_de("A", wsrc("A", "alto")); T_AQUI = g_de("A", wsrc("A", "aquí", fim=True))
T_POR = g_de("B", wsrc("B", "por") - 0.03); T_PASO = g_de("B", wsrc("B", "paso", n=1, fim=True, exato=True))
T_TOCA = g_de("B", wsrc("B", "toca")); T_VIR = T_POR
print(f"fim {T_END:.2f}  juan {G_JUAN:.2f}  alto {T_ALTO:.2f}  virada {T_VIR:.2f}  toca {T_TOCA:.2f}")

# ---------------- palavras no tempo global (legenda) ----------------
PAL = [dict(w=p["w"], ini=round((max(p["ini"], P_A0) - P_A0) / TEMPO_P, 3), fim=round((p["fim"] - P_A0) / TEMPO_P, 3), q="briga") for p in P1]
for p in AVJ["M"]["palavras"]:
    if p["ini"] < M_S0 - 0.05: PAL.append(dict(w=p["w"], ini=round(G_MSI + p["ini"], 3), fim=round(G_MSI + p["fim"], 3), q="aberto"))
    else:
        gi = g_de("M", p["ini"]); gf = g_de("M", p["fim"])
        if gi is not None: PAL.append(dict(w=p["w"], ini=round(gi, 3), fim=round(gf if gf else gi + 0.3, 3), q="mulher"))
for av in ("A", "B"):
    for p in AVJ[av]["palavras"]:
        gi = g_de(av, p["ini"]); gf = g_de(av, p["fim"])
        if gi is not None: PAL.append(dict(w=p["w"], ini=round(gi, 3), fim=round(gf if gf else gi + 0.3, 3), q="padre"))
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
AV = {"M": Avatar(P / "mulher/M.mp4"), "A": Avatar(P / "avatar/A.mp4"), "B": Avatar(P / "avatar/B.mp4")}
BRIGA = Pngs("briga_ls") if (B / "briga_ls").exists() else Pngs("briga")
WS = {n: Pngs(n) for n in ("w1", "w2", "w3")}
BRP = {n: Pngs(n) for _, _, n in CV if n != "wa"}
WA = [Image.open(P / "wa" / f"wa{i}.png").convert("RGBA") for i in (1, 2, 3)]

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
BL = []
grupos = []
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
# caixa opaca que cobre a legenda PT da briga (115-604 x 707-775) em todos os quadros
CAIXA = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); ImageDraw.Draw(CAIXA).rounded_rectangle((92, 692, 628, 794), 18, fill=(14, 14, 14, 255))
Y_LEG = {"briga": 743, "aberto": 743, "mulher": 880, "padre": 690}

# ---------------- sobreposições ----------------
def rgba(n): return Image.open(OV / n).convert("RGBA")
FAIXA, MOLD, SELO, ELIM, VIVO, TOCA, SETA = (rgba(n) for n in ("faixa.png", "moldura_jm.png", "selo10.png", "eliminado.png", "en_vivo.png", "toca.png", "seta.png"))
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
_wabg = {}
def tela_wa(t, t0, t1, fav):
    """prints de WhatsApp em cascata sobre o quadro do padre desfocado e escurecido"""
    base = cv2.GaussianBlur(fav, (0, 0), 9).astype(np.float32) * 0.55
    im = Image.fromarray(base.astype(np.uint8)).convert("RGBA")
    passo = (t1 - t0) / 3
    for i in range(3):
        ti = t0 + i * passo - (0.0 if i == 0 else 0.0)
        if t < ti: break
        key = i
        if key not in _wabg:
            w = WA[i].resize((540, 675), Image.LANCZOS)
            card = Image.new("RGBA", (556, 691), (0, 0, 0, 0)); ImageDraw.Draw(card).rounded_rectangle((0, 0, 555, 690), 22, fill=(255, 255, 255, 255))
            m = Image.new("L", (540, 675), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 539, 674), 18, fill=255); card.paste(w, (8, 8), m)
            _wabg[key] = card.rotate((-4, 3, -2)[i], expand=True, resample=Image.BICUBIC)
        c = pop(_wabg[i], t, ti, 0.16)
        cx, cy = (330, 560, 390)[i], (520, 640, 760)[i]
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); a = c.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.5))
        shi = Image.new("RGBA", c.size, (0, 0, 0, 0)); shi.putalpha(a); centro(im, shi, cx + 6, cy + 10); centro(im, c, cx, cy)
    return np.asarray(im.convert("RGB"))

# ---------------- quadro base ----------------
def base(t):
    for c0, c1, n in CV:
        if c0 <= t < c1:
            if n == "wa":
                sg = next(s for s in SEG if s["g0"] <= t < s["g1"]); fav = AV[sg["fonte"]].quadro(int(round((sg["s0"] + t - sg["g0"]) * 25)))
                return tela_wa(t, c0, c1, fav), "broll"
            fr = BRP[n]; vel = max(0.5, min(1.0, len(fr) / 30 / (c1 - c0))); return fr.q(int((t - c0) * vel * 30)), "broll"
    sg = next((s for s in SEG if s["g0"] <= t < s["g1"]), SEG[-1])
    if sg["tipo"] == "briga": return BRIGA.q(int(round(t * 30))), "briga"
    if sg["tipo"] == "aberto": return WS[sg["fonte"]].q(int(round((t - sg["g0"]) * 30))), "aberto"
    s = sg["s0"] + t - sg["g0"]; f = AV[sg["fonte"]].quadro(int(round(s * 25)))
    return zoom(f, sg["zoom"], cy=0.30 if sg["tipo"] == "mulher" else 0.22), sg["tipo"]
if not a_.so_audio:
    j0 = int(round(a_.de * FPS)); j1 = NOUT if a_.ate is None else int(round(a_.ate * FPS))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "30", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
                            "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-profile:v", "high",
                            "-color_range", "tv", "-colorspace", "smpte170m", "-color_primaries", "smpte170m", "-color_trc", "smpte170m", a_.saida],
                           stdin=subprocess.PIPE)
    for j in range(j0, j1):
        t = j / FPS
        if j % 150 == 0: print(f"[{j}/{NOUT}] {100 * j // NOUT}%", flush=True)
        f, tipo = base(t)
        if tipo == "padre":
            f = glitch(f, t); dx, dy = tremor(t)
            if dx or dy: f = zoom(f, 1.03, dx, dy)
        im = Image.fromarray(np.ascontiguousarray(f)).convert("RGBA")
        if tipo == "briga": im.alpha_composite(FAIXA); im.alpha_composite(CAIXA)
        if tipo == "padre": im.alpha_composite(MOLD)
        if T_ELIM0 <= t < T_ELIM1 and ((t - T_ELIM0) % 0.6) < 0.42: centro(im, ELIM, 360, 930)
        if T_POR <= t < T_PASO + 0.1: im.alpha_composite(pop(VIVO, t, T_POR), (24, 168))
        if t >= T_TOCA:
            centro(im, pop(TOCA, t, T_TOCA), 360, 935)
            dyy = int(round(16 * np.sin(2 * np.pi * 1.6 * (t - T_TOCA))))
            for x in (200, 391): im.alpha_composite(SETA, (x, 1010 + dyy))
        lg, q = leg(t)
        if lg is not None and not (t >= T_TOCA):
            im.alpha_composite(lg, (0, Y_LEG.get(tipo if tipo in Y_LEG else q, 690) - 55))
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
put(voz, fade(ld(P / "lipsync/in/es_P.wav"), 0.005, 0.03), 0.0)
MW = ld(P / "mulher/M.wav"); put(voz, fade(MW[int(0.20 * SR):int((M_S0 - 0.03) * SR)], 0.008, 0.02), G_MSI + 0.20)
WAV = {"M": MW, "A": ld(P / "avatar/A.wav"), "B": ld(P / "avatar/B.wav")}
for sg in SEG:
    if sg["fonte"] in WAV:
        a = int(sg["s0"] * SR); n = int((sg["g1"] - sg["g0"]) * SR); put(voz, fade(WAV[sg["fonte"]][a:a + n], 0.008, 0.008), sg["g0"])
# a fala do patrão vem do TTS gritado: um pouco mais alta que o resto
iB = int(7.1 * SR); vb = voz[:iB].copy(); vr = voz[iB:].copy()
vb *= 10 ** ((-16.0 - med.integrated_loudness(vb)) / 20); vr *= 10 ** ((-18.0 - med.integrated_loudness(vr)) / 20); voz = np.concatenate([vb, vr])
def norm(y, alvo):
    y = y.T if y.ndim > 1 else np.stack([y, y], 1); return y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)
mus = np.zeros((NA, 2))
amb = norm(ld(P / "demucs/htdemucs/orig/no_vocals.wav", False)[:, :int(7.1 * SR)], -30.0); put2 = lambda s, t0: mus.__setitem__(slice(int(t0 * SR), int(t0 * SR) + len(s)), mus[int(t0 * SR):int(t0 * SR) + len(s)] + s[:max(0, min(len(s), NA - int(t0 * SR)))])
def add2(s, t0):
    i = int(round(t0 * SR)); n = min(len(s), NA - i); mus[i:i + n] += s[:n]
add2(fade(amb, 0.0, 0.08), 0.0)
# plano aberto: som original do take (choro/ambiente, sem fala)
og = ld(P / "demucs/orig.wav", False)   # áudio original 0-21 s
for sg in SEG:
    if sg["tipo"] == "aberto":
        src0 = {"w1": 7.45, "w2": 13.97, "w3": 16.60}[sg["fonte"]]; a = int(src0 * SR); n = int((sg["g1"] - sg["g0"]) * SR)
        add2(fade(og[:, a:a + n].T * 10 ** (-6 / 20), 0.06, 0.06), sg["g0"])
V4M = Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\musica")
ten = norm(ld(V4M / "tensao.mp3", False), -32.0); esp = norm(ld(V4M / "esperanca.mp3", False), -32.0)
T_TEN = SEG[3]["g1"] - 0.6           # tensão entra um pouco antes da selfie
need = T_VIR - T_TEN + 0.3
if need * SR > len(ten):              # emenda a tensão com crossfade de 1 s (volta para 8 s)
    xf = int(1.0 * SR); a = ten[:len(ten) - xf]; b = ten[int(8 * SR):]
    cross = ten[len(ten) - xf:] * np.linspace(1, 0, xf)[:, None] + b[:xf] * np.linspace(0, 1, xf)[:, None]
    ten = np.concatenate([a, cross, b[xf:]])
s = fade(ten[:int(need * SR)], 0.6, 0.3); add2(s, T_TEN)
s = fade(esp[:NA - int(T_VIR * SR)], 0.5, 0.8); add2(s, T_VIR)
g_ = rng.standard_normal(int(0.38 * SR)) * 0.5; g_ = np.sign(g_) * (np.abs(g_) > 0.6) * np.repeat(rng.random(len(g_) // 400 + 1) > 0.4, 400)[:len(g_)]
g_ *= np.linspace(1, 0, len(g_)) ** 0.7; g_ *= 0.05 / (np.sqrt(np.mean(g_ ** 2)) + 1e-9); add2(np.stack([g_, g_], 1), T_ALTO)
print("tensão", round(len(ten) / SR, 1), "precisa", round(need, 1), "| esperança", round(len(esp) / SR, 1), "precisa", round(T_END - T_VIR, 1))
mix = mus + voz[:, None]
sf.write(T / "_mix.wav", mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T / "_mix.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled",
                "-ar", "48000", "-c:a", "pcm_s16le", str(T / "audio.wav")], check=True)
m2 = sf.read(T / "audio.wav")[0]
print("LUFS final", round(med.integrated_loudness(m2), 1), "| voz", round(med.integrated_loudness(voz), 1), "| trilha", round(med.integrated_loudness(mus), 1))
