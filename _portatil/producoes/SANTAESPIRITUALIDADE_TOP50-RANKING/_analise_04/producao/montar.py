# -*- coding: utf-8 -*-
"""Ranking 04 → SB ES «Sueldo». Apresentadora (Avatar IV, PIP como no original) sobre Juan Méndez parado; Juan (Avatar IV no
cenário da catedral do original) com b-rolls originais (legenda PT coberta por caixa opaca) e do banco SB nas fronteiras de
palavra; senhor anônimo novo (Avatar IV no sofá do original) com rótulo TESTIMONIO; EN VIVO + moldura da live só no fecho.
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
def lw(w): return re.sub(r"[¡!¿?,.:;«»…]", "", w).lower()
def wsrc(av, prefix, linha=None, n=0, fim=False, exato=True):
    c = [p for p in AVJ[av]["palavras"] if (lw(p["w"]) == prefix if exato else lw(p["w"]).startswith(prefix)) and (linha is None or p["linha"] == linha)]
    return c[n]["fim" if fim else "ini"]

# ---------------- linha do tempo ----------------
SEG = []; g = 0.0
def add(s0, s1, tipo, fonte, zoom=1.0):
    global g; SEG.append(dict(g0=round(g, 4), g1=round(g + s1 - s0, 4), tipo=tipo, fonte=fonte, s0=s0, zoom=zoom)); g += s1 - s0
add(0.0, 21.78, "padre", "A"); add(21.78, 29.25, "padre", "A", 1.08); add(29.25, 46.05, "padre", "A")
add(0.10, 11.00, "padre", "B"); add(11.00, 23.35, "padre", "B", 1.08)
add(0.12, 7.55, "senhor", "S"); add(7.55, 13.80, "senhor", "S", 1.07)
add(23.42, 35.12, "padre", "B"); add(35.12, 41.75, "padre", "B", 1.08)
T_END = g; NOUT = int(round(T_END * FPS))
P_OFF = 0.10                                  # apresentadora: P src = t + P_OFF
T_PIP = round(wsrc("A", "cuando") - 0.06, 3)  # PIP sai quando o Juan começa a falar
def g_de(av, s):
    for sg in SEG:
        if sg["fonte"] == av and sg["s0"] - 1e-6 <= s <= sg["s0"] + (sg["g1"] - sg["g0"]) + 1e-6: return sg["g0"] + s - sg["s0"]
    return None
CV_SRC = [
 ("A", wsrc("A", "y", "J02") - 0.04, wsrc("A", "te", "J03") - 0.03, "dinheiro"),
 ("A", wsrc("A", "antes", "J03") - 0.04, wsrc("A", "me", "J03") - 0.03, "rosa_olha"),
 ("A", wsrc("A", "me", "J03") - 0.03, wsrc("A", "para", "J04") - 0.03, "rosa_reza"),
 ("A", wsrc("A", "antigua") - 0.04, wsrc("A", "y", "J05") - 0.03, "vela_livro"),
 ("A", wsrc("A", "guardián") - 0.04, wsrc("A", "arcanos") - 0.03, "cruz_mar"),
 ("A", wsrc("A", "arcanos") - 0.03, wsrc("A", "que", "J06") - 0.03, "moca_branca"),
 ("A", wsrc("A", "que", "J06") - 0.03, wsrc("A", "las", "J06") - 0.03, "cruz_sol"),
 ("A", wsrc("A", "las", "J06") - 0.03, wsrc("A", "con", "J06") - 0.03, "terco"),
 ("A", wsrc("A", "el", "J07") - 0.04, wsrc("A", "decir", "J07") - 0.03, "maos"),
 ("A", wsrc("A", "me", "J07") - 0.04, 46.05, "celular_live"),
 ("B", 0.10, wsrc("B", "ya") - 0.03, "moca_sorri"),
 ("B", wsrc("B", "ya") - 0.03, wsrc("B", "después") - 0.03, "mesa"),
 ("B", wsrc("B", "después") - 0.03, wsrc("B", "pero", "J09") - 0.03, "familia"),
 ("B", wsrc("B", "no", "J09") - 0.04, wsrc("B", "y", "J10") - 0.03, "manuscrito"),
 ("B", wsrc("B", "con", "J10") - 0.04, wsrc("B", "y", "J10", n=1) - 0.03, "piggy"),
 ("B", wsrc("B", "y", "J10", n=1) - 0.03, wsrc("B", "miren") - 0.03, "padaria"),
 ("B", wsrc("B", "pero", "J13") - 0.04, wsrc("B", "por", "J14") - 0.03, "selfie"),
 ("B", wsrc("B", "vuelve") - 0.04, wsrc("B", "envía") - 0.03, "idosa_cel"),
 ("B", wsrc("B", "envía") - 0.03, wsrc("B", "toca") - 0.03, "familia_cel"),
]
CV = [(round(g_de(av, a), 4), round(g_de(av, b), 4), n) for av, a, b, n in CV_SRC]
for c in CV: print(f"  {c[2]:12s} {c[0]:6.2f}-{c[1]:6.2f} ({c[1]-c[0]:.2f}s)")
T_ALTO = g_de("A", wsrc("A", "alto")); T_AQUI = g_de("A", wsrc("A", "aquí", fim=True))
T_POR = g_de("B", wsrc("B", "por", "J14") - 0.03); T_PASO = g_de("B", wsrc("B", "paso", n=1, fim=True))
T_TOCA = g_de("B", wsrc("B", "toca")); T_S0 = next(s["g0"] for s in SEG if s["tipo"] == "senhor"); T_S1 = [s["g1"] for s in SEG if s["tipo"] == "senhor"][-1]
print(f"fim {T_END:.2f}  pip {T_PIP:.2f}  alto {T_ALTO:.2f}  senhor {T_S0:.2f}-{T_S1:.2f}  vivo {T_POR:.2f}  toca {T_TOCA:.2f}")

# ---------------- palavras no tempo global (legenda) ----------------
PAL = [dict(w=p["w"], ini=round(p["ini"] - P_OFF, 3), fim=round(p["fim"] - P_OFF, 3), q="pip") for p in AVJ["P"]["palavras"]]
for av, q in (("A", "padre"), ("B", "padre"), ("S", "senhor")):
    for p in AVJ[av]["palavras"]:
        gi = g_de(av, p["ini"]); gf = g_de(av, p["fim"])
        if gi is not None: PAL.append(dict(w=p["w"], ini=round(gi, 3), fim=round(gf if gf else gi + 0.3, 3), q=q))
PAL.sort(key=lambda p: p["ini"])
json.dump(dict(seg=SEG, cv=CV, palavras=PAL, fim=T_END, alto=T_ALTO, toca=T_TOCA), open(P / "tempos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

# ---------------- leitura ----------------
class Pngs:
    def __init__(s, d): s.fs = sorted((B / d).glob("f_*.png")); s.c = {}
    def __len__(s): return len(s.fs)
    def q(s, k):
        k = max(0, min(len(s.fs) - 1, k))
        if k not in s.c:
            if len(s.c) > 8: s.c.clear()
            s.c[k] = np.asarray(Image.open(s.fs[k]).convert("RGB"))
        return s.c[k]
class Avatar:
    def __init__(s, p, w=720, h=1280): s.p = p; s.pr = None; s.i = -1; s.f = None; s.w = w; s.h = h
    def quadro(s, k):
        if s.pr is not None and k < s.i:
            s.pr.kill(); s.pr = None; s.i = -1
        if s.pr is None:
            s.pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(s.p), "-vf", "scale=in_color_matrix=bt601:in_range=limited:flags=accurate_rnd+full_chroma_int,format=rgb24",
                                     "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        while s.i < k:
            b = s.pr.stdout.read(s.w * s.h * 3)
            if len(b) < s.w * s.h * 3: break
            s.f = np.frombuffer(b, np.uint8).reshape(s.h, s.w, 3); s.i += 1
        return s.f
AV = {"A": Avatar(P / "avatar/A.mp4"), "B": Avatar(P / "avatar/B.mp4"), "S": Avatar(P / "senhor/S.mp4")}
APR = Avatar(P / "apresentadora/P.mp4", 1280, 720)
BRP = {n: Pngs(n) for _, _, n in CV}
CAIXAS = json.load(open(B / "caixas.json"))

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
# caixa opaca sobre a legenda PT de cada b-roll original (mesmo lugar), com largura mínima para a legenda ES
CXIM, CXY = {}, {}
for n, bx in CAIXAS.items():
    if not bx: continue
    x0, y0, x1, y1 = bx; h = max(290, (x1 - x0) // 2 + 8); x0, x1 = min(x0, 360 - h), max(x1, 360 + h)
    im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((x0, y0, x1, y1), 18, fill=(14, 14, 14, 255))
    CXIM[n] = im; CXY[n] = (y0 + y1) // 2
Y_LEG = {"padre": 965, "senhor": 965, "pip": 1185, "broll": 965}

# ---------------- sobreposições ----------------
def rgba(n): return Image.open(OV / n).convert("RGBA")
MOLD, SELO, ELIM, VIVO, TOCA, SETA, TEST, PSOM, PBOR = (rgba(n) for n in ("moldura_jm.png", "selo10.png", "eliminado.png", "en_vivo.png", "toca.png", "seta.png", "testimonio.png", "pip_sombra.png", "pip_borda.png"))
PMASK = Image.open(OV / "pip_mask.png").convert("L")
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
def pip(im, t):
    f = APR.quadro(int(round((t + P_OFF) * 25)))
    c = Image.fromarray(np.ascontiguousarray(f[:, 264:1196])).resize((660, 510), Image.LANCZOS).convert("RGBA")
    lay = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); lay.paste(c, (44, 600))
    m = Image.new("L", (720, 1280), 0); m.paste(PMASK, (0, 0)); lay.putalpha(m)
    im.alpha_composite(PSOM); im.alpha_composite(lay); im.alpha_composite(PBOR)

# ---------------- quadro base ----------------
def base(t):
    for c0, c1, n in CV:
        if c0 <= t < c1:
            fr = BRP[n]; vel = max(0.45, min(1.0, len(fr) / 30 / (c1 - c0))); return fr.q(int((t - c0) * vel * 30)), "broll", n
    sg = next((s for s in SEG if s["g0"] <= t < s["g1"]), SEG[-1])
    s = sg["s0"] + t - sg["g0"]; f = AV[sg["fonte"]].quadro(int(round(s * 25)))
    return zoom(f, sg["zoom"], cy=0.22 if sg["tipo"] == "padre" else 0.30), sg["tipo"], None
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
        f, tipo, nb = base(t)
        f = glitch(f, t); dx, dy = tremor(t)
        if dx or dy: f = zoom(f, 1.03, dx, dy)
        im = Image.fromarray(np.ascontiguousarray(f)).convert("RGBA")
        if nb in CXIM: im.alpha_composite(CXIM[nb])
        if t < T_PIP: pip(im, t)
        if tipo == "padre" and t >= T_POR: im.alpha_composite(MOLD)
        if tipo == "senhor": im.alpha_composite(pop(TEST, t, T_S0 + 0.15), (18, 160))
        if T_ELIM0 <= t < T_ELIM1 and ((t - T_ELIM0) % 0.6) < 0.42: centro(im, ELIM, 360, 640)
        if T_POR <= t < T_PASO + 0.1: im.alpha_composite(pop(VIVO, t, T_POR), (24, 168))
        if t >= T_TOCA:
            centro(im, pop(TOCA, t, T_TOCA), 360, 935)
            dyy = int(round(16 * np.sin(2 * np.pi * 1.6 * (t - T_TOCA))))
            for x in (200, 391): im.alpha_composite(SETA, (x, 1010 + dyy))
        lg, q = leg(t)
        if lg is not None and not (t >= T_TOCA):
            y = 1185 if t < T_PIP else (CXY[nb] if nb in CXY else Y_LEG.get(tipo, 965))
            im.alpha_composite(lg, (0, y - 55))
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
PW = ld(P / "apresentadora/P.wav"); put(voz, fade(PW[int(P_OFF * SR):int((T_PIP + P_OFF) * SR)], 0.005, 0.03), 0.0)
WAV = {"A": ld(P / "avatar/A.wav"), "B": ld(P / "avatar/B.wav"), "S": ld(P / "senhor/S.wav")}
for sg in SEG:
    a = int(sg["s0"] * SR); n = int((sg["g1"] - sg["g0"]) * SR); put(voz, fade(WAV[sg["fonte"]][a:a + n], 0.008, 0.008), sg["g0"])
# trechos com tratamento de agudos (chiado) — preenchido depois da conferência por trecho (chiado.json)
CH = json.load(open(P / "chiado.json")) if (P / "chiado.json").exists() else []
for c in CH:
    i0, i1 = int(c["ini"] * SR), int(c["fim"] * SR); seg = voz[i0:i1].astype(np.float32)
    if len(seg) < 2048: continue
    l0 = med.integrated_loudness(seg) if len(seg) > SR * 0.5 else None
    tmp_in, tmp_out = T / "_ch_in.wav", T / "_ch_out.wav"; sf.write(tmp_in, seg, SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp_in), "-af", c["af"], "-c:a", "pcm_f32le", str(tmp_out)], check=True)
    out = sf.read(tmp_out)[0][:len(seg)]
    if l0 is not None and np.isfinite(l0): out = out * 10 ** ((l0 - med.integrated_loudness(out)) / 20)
    n = int(0.02 * SR); w = np.ones(len(out)); w[:n] = np.linspace(0, 1, n); w[-n:] = np.linspace(1, 0, n)
    voz[i0:i0 + len(out)] = voz[i0:i0 + len(out)] * (1 - w) + out * w
voz *= 10 ** ((-18.0 - med.integrated_loudness(voz)) / 20)
def norm(y, alvo):
    y = y.T if y.ndim > 1 else np.stack([y, y], 1); return y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)
mus = np.zeros((NA, 2))
def add2(s, t0):
    i = int(round(t0 * SR)); n = min(len(s), NA - i); mus[i:i + n] += s[:n]
def estica(tr, need, volta=8.0):
    while need * SR > len(tr):
        xf = int(1.0 * SR); a = tr[:len(tr) - xf]; b = tr[int(volta * SR):]
        cross = tr[len(tr) - xf:] * np.linspace(1, 0, xf)[:, None] + b[:xf] * np.linspace(0, 1, xf)[:, None]
        tr = np.concatenate([a, cross, b[xf:]])
    return tr
V4M = Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\musica")
ten = norm(ld(V4M / "tensao.mp3", False), -32.0); esp = norm(ld(V4M / "esperanca.mp3", False), -32.0)
need = T_ALTO + 0.3; ten = estica(ten, need); add2(fade(ten[:int(need * SR)], 0.4, 0.3), 0.0)
ne = T_END - T_ALTO; esp = estica(esp, ne); add2(fade(esp[:int(ne * SR)], 0.5, 0.8), T_ALTO)
g_ = rng.standard_normal(int(0.38 * SR)) * 0.5; g_ = np.sign(g_) * (np.abs(g_) > 0.6) * np.repeat(rng.random(len(g_) // 400 + 1) > 0.4, 400)[:len(g_)]
g_ *= np.linspace(1, 0, len(g_)) ** 0.7; g_ *= 0.05 / (np.sqrt(np.mean(g_ ** 2)) + 1e-9); add2(np.stack([g_, g_], 1), T_ALTO)
mix = mus + voz[:, None]
sf.write(T / "_mix.wav", mix, SR, subtype="FLOAT"); sf.write(T / "_voz.wav", voz, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T / "_mix.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled",
                "-ar", "48000", "-c:a", "pcm_s16le", str(T / "audio.wav")], check=True)
m2 = sf.read(T / "audio.wav")[0]
print("LUFS final", round(med.integrated_loudness(m2), 1), "| voz", round(med.integrated_loudness(voz), 1), "| trilha", round(med.integrated_loudness(mus), 1))
