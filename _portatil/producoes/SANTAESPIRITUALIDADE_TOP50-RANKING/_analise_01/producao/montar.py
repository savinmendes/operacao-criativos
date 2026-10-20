# -*- coding: utf-8 -*-
"""Ranking 01 → SB ES «Restaurante noticia». Takes originais (legenda PT tirada com LaMa, repórter/dono com lipsync HeyGen colado
só na boca) + Juan Méndez (Avatar IV) no cenário do frade com moldura da live. Saída 1 passada, matriz bt601/tv FIXA.
uso: python montar.py [--so-audio] [--de s --ate s --saida x.mp4]"""
import json, re, subprocess, argparse
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent; T = P / "_trab"; T.mkdir(exist_ok=True); B = P / "broll"; OV = P / "ov"
ap = argparse.ArgumentParser(); ap.add_argument("--so-audio", action="store_true"); ap.add_argument("--de", type=float, default=0)
ap.add_argument("--ate", type=float, default=None); ap.add_argument("--saida", default=str(T / "_video.mp4")); a_ = ap.parse_args()
FPS = 30
TP = json.load(open(P / "tempos.json", encoding="utf-8")); PAL = TP["palavras"]
T_END = round(TP["fim_fala"] + 0.5, 2); NOUT = int(round(T_END * FPS))
def wt(prefix, linha, exato=False):
    lw = lambda p: re.sub(r"[¡!¿?,.:;«»…]", "", p["w"]).lower()
    return next(p["ini"] for p in PAL if p["linha"] == linha and (lw(p) == prefix if exato else lw(p).startswith(prefix)))
# ---------------- plano ----------------
T_DA, T_CH, T_DB, T_JM = 6.60, 6.60 + 178 / 30, 18.50, 23.85   # DB começa no «La» (pausa coberta pelo salão cheio)
A_OFF = 24.05 - 0.25                     # tempo global = t_avatar + A_OFF
B_OFF = 55.695 - 0.25
T_ALTO = wt("alto", "J07")
# (ini, fim, pasta) b-roll em tela cheia por cima do padre (cortes em fronteira de palavra)
BR = [
 (wt("no", "J04") - 0.06, wt("pero", "J05") - 0.02, "roxo"),
 (wt("pero", "J05") - 0.02, wt("pero", "J05") + 1.01, "casa"),
 (wt("pero", "J05") + 1.01, wt("pero", "J05") + 2.01, "cozinha"),
 (wt("pero", "J05") + 2.01, wt("y", "J05") - 0.06, "feliz"),   # banco SB (a chora original ficou manchada pela LaMa)
 (wt("y", "J05") - 0.06, wt("y", "J05") + 1.74, "carro"),
 (wt("oh", "J06") - 0.05, wt("guardián", "J06") - 0.04, "sb"),
 (wt("con", "J06", True) - 0.04, T_ALTO - 0.02, "igreja"),
 (TP["linhas"][7]["fim"] + 0.02, wt("por", "J08") - 0.04, "biblia"),     # esconde a troca A→B
 (wt("y", "J08") - 0.05, wt("muchos", "J09") - 0.03, "reza"),
 (wt("claro", "J09") - 0.05, wt("la", "J09") - 0.03, "silhueta"),
 (wt("salmo", "J10") - 0.05, wt("riqueza", "J10") - 0.06, "salmo"),
 (wt("para", "J10") - 0.04, TP["linhas"][10]["fim"] + 0.12, "bracos"),
 (wt("partir", "J11") - 0.15, wt("vuelve", "J11") - 0.04, "brinde"),
]
for b in BR: print(f"{b[2]:9s} {b[0]:.2f}-{b[1]:.2f} ({b[1]-b[0]:.2f}s)")
# ---------------- leitura ----------------
CORTE = {"casa": (0, 7), "chora": (8, 0), "carro": (11, 0), "sb": (0, 4), "biblia": (3, 13), "silhueta": (0, 13)}   # quadros de dissolve/flash
class Pngs:
    def __init__(s, d):
        s.fs = sorted((B / d / "limpo").glob("f_*.png")) if (B / d / "limpo").exists() else sorted((B / d).glob("f_*.png")); s.c = {}
        a, b = CORTE.get(d, (0, 0)); s.fs = s.fs[a:len(s.fs) - b]
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
        if s.pr is None:
            s.pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(s.p), "-vf", "scale=in_color_matrix=bt601:in_range=limited:flags=accurate_rnd+full_chroma_int,format=rgb24",
                                     "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        while s.i < k:
            b = s.pr.stdout.read(720 * 1280 * 3)
            if len(b) < 720 * 1280 * 3: break
            s.f = np.frombuffer(b, np.uint8).reshape(1280, 720, 3); s.i += 1
        return s.f
AV = {"A": Avatar(P / "avatar/A.mp4"), "B": Avatar(P / "avatar/B.mp4"), "D": Avatar(P / "dono2/D.mp4")}   # D = dono (Avatar IV, retrato nítido)
NEWS_LS, NEWS, DA, CH, DB = Pngs("news_ls"), Pngs("news"), Pngs("donoA"), Pngs("cheio"), Pngs("donoB")
BRP = {d: Pngs(d) for _, _, d in BR}
REF_BAND = NEWS.q(90).astype(np.int16)    # rodapé sem a repórter (orig 3,0 s)
# ---------------- legenda (palavra a palavra, 1 palavra verde) ----------------
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
FL = ImageFont.truetype(str(POP / "Poppins-Bold.ttf"), 42); VERDE = (24, 200, 24)
def limpa(w): return re.sub(r"[¡!¿?,.:;«»…]", "", w).lower()
def blocos(pal):
    out, cur = [], []
    for p in pal:
        cur.append(p); txt = " ".join(limpa(x["w"]) for x in cur)
        if len(cur) >= 3 or len(txt) >= 15 or re.search(r"[,.:;!?»…]$", p["w"]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
BL = []
for ln in dict.fromkeys(p["linha"] for p in PAL):
    lp = [p for p in PAL if p["linha"] == ln]
    if ln == "D2": lp = [p for p in lp if p["ini"] < 18.3], [p for p in lp if p["ini"] >= 18.3]
    else: lp = (lp,)
    for part in lp:
        bs = blocos(part)
        for i, b in enumerate(bs):
            ini = max(0, b[0]["ini"] - 0.04)
            prox = bs[i + 1][0]["ini"] - 0.04 if i + 1 < len(bs) else b[-1]["fim"] + 0.35
            BL.append(dict(ini=ini, fim=prox, ws=[(limpa(x["w"]), x["ini"]) for x in b]))
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
            return _cache[key]
    return None
# ---------------- sobreposições ----------------
def rgba(n): return Image.open(OV / n).convert("RGBA")
FAIXA, ROD, MOLD, SELO, ELIM, SALMO, VIVO, TOCA, SETA = (rgba(n) for n in ("faixa.png", "rodape.png", "moldura_jm.png", "selo10.png", "eliminado.png",
                                                                          "salmo.png", "en_vivo.png", "toca.png", "seta.png"))
T_TOCA = wt("toca", "J12"); T_SAL0, T_SAL1 = wt("salmo", "J10") - 0.05, TP["linhas"][10]["fim"] + 0.12
T_VIVO0, T_VIVO1 = wt("por", "J11") - 0.05, wt("partir", "J11") - 0.15
T_ELIM0, T_ELIM1 = T_ALTO + 0.35, wt("transmisión", "J07") + 0.9
def pop(im, t, t0, dur=0.18):
    u = (t - t0) / dur
    if u >= 1.6: return im
    s = 0.7 + 0.36 * min(u, 1) if u < 1 else 1.06 - 0.06 * (u - 1) / 0.6
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
def centro(base, im, cx, cy): base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
def pop_full(im, t, t0):
    """pop de camada de tela cheia (faixa) a partir do centro dela"""
    u = (t - t0) / 0.22
    if u >= 1.6 or u < 0: return im if u >= 1.6 else None
    bb = im.getbbox(); c = im.crop(bb); s = 0.7 + 0.36 * min(u, 1) if u < 1 else 1.06 - 0.06 * (u - 1) / 0.6
    c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.BICUBIC)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    out.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2))); return out
rng = np.random.default_rng(7)
def glitch(f, t):
    u = (t - T_ALTO) / 0.55
    if not (0 <= u < 1): return f
    g = f.copy(); k = int(14 * (1 - u) + 4)
    g[..., 0] = np.roll(f[..., 0], k, 1); g[..., 2] = np.roll(f[..., 2], -k, 1)
    for _ in range(7):
        y = rng.integers(0, 1240); h = rng.integers(8, 48); dx = rng.integers(-60, 60); g[y:y + h] = np.roll(g[y:y + h], dx, 1)
    if u < 0.25: g = np.clip(g.astype(np.int16) + 60, 0, 255).astype(np.uint8)
    return g
def tremor(t):
    u = t - T_ALTO
    if not (0 <= u < 0.9): return 0, 0
    a = 16 * (1 - u / 0.9); return int(a * np.sin(u * 83)), int(a * np.cos(u * 61))
def mascara_reporter(f):
    d = np.abs(f[960:].astype(np.int16) - REF_BAND[960:]).max(2)
    m = (d > 28).astype(np.uint8); m[:, :300] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))   # tira contornos finos das letras/logo
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2: return np.zeros(f.shape[:2], np.float32)
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); keep = (lab == k).astype(np.uint8)
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    keep = cv2.dilate(keep, np.ones((3, 3), np.uint8))
    velho = (f[960:].min(2) > 205) & (REF_BAND[960:].min(2) > 205)          # letra antiga visível (igual à referência)
    fb = f[960:].astype(np.int16); branco = (fb.min(2) > 175) & ((fb.max(2) - fb.min(2)) < 45); branco[:, 350:] = False
    velho |= branco                                                           # restos de letra branca junto ao cabelo
    keep[cv2.dilate(velho.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 0
    full = np.zeros(f.shape[:2], np.float32); full[960:] = cv2.GaussianBlur(keep.astype(np.float32), (5, 5), 0); full[945:960] = full[962]   # acima de 960 (rodapé translúcido) repete a silhueta
    return full
# ---------------- quadro base ----------------
def base(t):
    """devolve (quadro RGB, tipo) tipo in news/dono/cheio/padre/broll"""
    if t < T_DA:
        k = int(round(t * 30))
        return (NEWS_LS.q(k) if k < len(NEWS_LS) else NEWS.q(k)), "news"
    if t < T_CH: return AV["D"].quadro(int(round((t - T_DA) * 25))), "dono"
    if t < T_DB:
        vel = min(1.0, len(CH) / 30 / (T_DB - T_CH)); return CH.q(int((t - T_CH) * vel * 30)), "cheio"
    if t < T_JM: return AV["D"].quadro(int(round((178 / 30 + t - 18.35) * 25))), "dono"
    for t0, t1, d in BR:
        if t0 <= t < t1:
            fr = BRP[d]; vel = max(0.5, min(1.0, len(fr) / 30 / (t1 - t0))); return fr.q(int((t - t0) * vel * 30)), "broll"
    if t < B_OFF + 0.25 - 0.2: return AV["A"].quadro(int(round((t - A_OFF) * 25))), "padre"
    return AV["B"].quadro(int(round((t - B_OFF) * 25))), "padre"
for t0, t1, d in BR:
    v = len(BRP[d]) / 30 / (t1 - t0); print(f"  vel {d}: {min(1, v):.2f}" + ("  <0,5!" if v < 0.5 else ""))
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
            if dx or dy: f = cv2.warpAffine(f, np.float32([[1.03, 0, dx - 10.8], [0, 1.03, dy - 19.2]]), (720, 1280), borderMode=cv2.BORDER_REFLECT)
        im = Image.fromarray(np.ascontiguousarray(f)).convert("RGBA")
        if tipo in ("news", "cheio"):
            im.alpha_composite(ROD)
            if tipo == "news" and t < 1.9:
                m = mascara_reporter(f)[..., None]
                arr = np.asarray(im).astype(np.float32); arr[..., :3] = f * m + arr[..., :3] * (1 - m); im = Image.fromarray(arr.astype(np.uint8), "RGBA")
            fx = pop_full(FAIXA, t, 0.0) if tipo == "news" else FAIXA
            if fx is not None: im.alpha_composite(fx)
        if tipo == "padre": im.alpha_composite(MOLD)
        if T_ELIM0 <= t < T_ELIM1 and ((t - T_ELIM0) % 0.6) < 0.42: centro(im, ELIM, 360, 930)
        if T_SAL0 <= t < T_SAL1: centro(im, pop(SALMO, t, T_SAL0), 360, 905)
        if T_VIVO0 <= t < T_VIVO1: im.alpha_composite(pop(VIVO, t, T_VIVO0), (24, 168))
        if t >= T_TOCA:
            centro(im, pop(TOCA, t, T_TOCA), 360, 905)
            dyy = int(round(16 * np.sin(2 * np.pi * 1.6 * (t - T_TOCA))))
            for x in (200, 391): im.alpha_composite(SETA, (x, 985 + dyy))
        lg = leg(t)
        if lg is not None: im.alpha_composite(lg, (0, (775 if tipo == "dono" else 685) - 55))   # dono: abaixo do queixo
        im.alpha_composite(SELO)
        enc.stdin.write(np.asarray(im.convert("RGB")).tobytes())
    enc.stdin.close(); enc.wait(); print("vídeo ok")
# ---------------- áudio ----------------
SR = 48000; med = pyln.Meter(SR); NA = int(round(NOUT / FPS * SR))
voz = librosa.load(P / "voz.wav", sr=SR, mono=True)[0][:NA]; voz = np.pad(voz, (0, NA - len(voz)))
voz *= 10 ** ((-18.0 - med.integrated_loudness(voz)) / 20)
def norm(y, alvo):
    y = y.T if y.ndim > 1 else np.stack([y, y], 1); return y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)
V4M = Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\musica")
amb = norm(librosa.load(P / "demucs/htdemucs/orig/no_vocals.wav", sr=SR, mono=False)[0][:, :int(T_JM * SR)], -33.0)
ten = norm(librosa.load(V4M / "tensao.mp3", sr=SR, mono=False)[0], -32.0); esp = norm(librosa.load(V4M / "esperanca.mp3", sr=SR, mono=False)[0], -32.0)
mus = np.zeros((NA, 2))
a = int(T_JM * SR); s = amb[:a].copy(); n = int(0.4 * SR); s[-n:] *= np.linspace(1, 0, n)[:, None]; mus[:len(s)] += s
T_VIR = wt("claro", "J09") - 0.05; b = int(T_VIR * SR)
s = ten[:b - a + int(0.3 * SR)].copy(); s[:int(0.4 * SR)] *= np.linspace(0, 1, int(0.4 * SR))[:, None]; n = int(0.3 * SR); s[-n:] *= np.linspace(1, 0, n)[:, None]
mus[a:a + len(s)] += s
s = esp[: NA - b].copy(); n = int(0.5 * SR); s[:n] *= np.linspace(0, 1, n)[:, None]; e = int(0.8 * SR); s[-e:] *= np.linspace(1, 0, e)[:, None]; mus[b:b + len(s)] += s
g = rng.standard_normal(int(0.38 * SR)) * 0.5; g = np.sign(g) * (np.abs(g) > 0.6) * np.repeat(rng.random(len(g) // 400 + 1) > 0.4, 400)[:len(g)]
g *= np.linspace(1, 0, len(g)) ** 0.7; g *= 0.05 / (np.sqrt(np.mean(g ** 2)) + 1e-9); ga = int(T_ALTO * SR); mus[ga:ga + len(g)] += np.stack([g, g], 1)
print("tensão disponível", round(len(ten) / SR, 1), "precisa", round(T_VIR - T_JM, 1), "| esperança", round(len(esp) / SR, 1), "precisa", round(T_END - T_VIR, 1))
mix = mus + voz[:, None]
sf.write(T / "_mix.wav", mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T / "_mix.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled",
                "-ar", "48000", "-c:a", "pcm_s16le", str(T / "audio.wav")], check=True)
m2 = sf.read(T / "audio.wav")[0]
print("LUFS final", round(med.integrated_loudness(m2), 1), "| voz", round(med.integrated_loudness(voz), 1), "| trilha", round(med.integrated_loudness(mus), 1))
