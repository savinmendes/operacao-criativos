# -*- coding: utf-8 -*-
"""Ranking 01 v3 (raio-x) + ganchos G1-G5.
v3: 1 s de tela dividida VAZIO | LOTADO -> repórter (notícia) -> dono (Avatar IV) -> Juan; b-rolls que provam; fala nova JN
(«Imagina pagar la última cuota…», avatar C). Ganchos: gancho novo + o corpo da v3 a partir de «No lo van a creer».
uso: python montar3.py [--gancho G1..G5] [--so-audio] [--de s --ate s]   (saída em _trab/v3_<nome>_video.mp4 + _audio.wav)"""
import json, re, subprocess, argparse
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent; T = P / "_trab"; T.mkdir(exist_ok=True); B = P / "broll"; OV = P / "ov"
ap = argparse.ArgumentParser(); ap.add_argument("--gancho", default=None); ap.add_argument("--so-audio", action="store_true")
ap.add_argument("--de", type=float, default=0); ap.add_argument("--ate", type=float, default=None); a_ = ap.parse_args()
NOME = a_.gancho or "V3"
FPS = 30
TP = json.load(open(P / "tempos3.json", encoding="utf-8")); PAL = TP["palavras"]
T_END = round(TP["fim_fala"] + 0.5, 2)
def lw(w): return re.sub(r"[¡!¿?,.:;«»…]", "", w).lower()
def wt(prefix, linha, exato=False, n=1):
    c = [p["ini"] for p in PAL if p["linha"] == linha and (lw(p["w"]) == prefix if exato else lw(p["w"]).startswith(prefix))]
    return c[n - 1]
LIN = {l["k"]: l for l in TP["linhas"]}
# ---------------- plano v3 ----------------
T_SPLIT = 1.0                                   # tela dividida 0-1 s; notícia (orig 0-5,6) de 1,0 a 6,6
T_DA, T_CH, T_DB, T_JM = 6.60, 6.60 + 178 / 30, 18.50, 23.85
A_OFF = 24.05 - 0.25; B_OFF = 55.695 - 0.25
DELTA, C_OFF, T_JN0, T_JN1, T_J11B = TP["delta"], TP["c_off"], TP["jn_ini"], TP["jn_fim"], TP["j11b_ini"]
T_ALTO = wt("alto", "J07")
T_DORMIR = wt("y", "JN", True) - 0.04
BR = [
 (wt("no", "J04") - 0.06, wt("pero", "J05") - 0.02, "moedas"),          # era a planta
 (wt("pero", "J05") - 0.02, wt("pero", "J05") + 1.01, "casa"),
 (wt("pero", "J05") + 1.01, wt("pero", "J05") + 2.01, "cozinha"),
 (wt("pero", "J05") + 2.01, wt("y", "J05") - 0.06, "feliz"),
 (wt("y", "J05") - 0.06, wt("y", "J05") + 1.74, "notif"),               # era o carro VW
 (wt("oh", "J06") - 0.05, wt("guardián", "J06") - 0.04, "sb"),
 (wt("con", "J06", True) - 0.04, T_ALTO - 0.02, "igreja"),
 (LIN["J07"]["fim"] + 0.02, wt("por", "J08") - 0.04, "biblia"),         # esconde a troca A→B
 (wt("y", "J08") - 0.05, wt("muchos", "J09") - 0.03, "reza"),
 (wt("claro", "J09") - 0.05, wt("la", "J09") - 0.03, "silhueta"),
 (wt("es", "J09", True) - 0.05, wt("salmo", "J10") - 0.05, "casal"),
 (wt("salmo", "J10") - 0.05, wt("riqueza", "J10") - 0.06, "salmo"),
 (wt("y", "J10", True) - 0.04, wt("y", "J10", True, 2) - 0.04, "mesa"),
 (wt("para", "J10") - 0.04, LIN["J10"]["fim"] + 0.12, "bracos"),
 (wt("en", "J11a", True) - 0.05, T_JN0 - 0.05, "famcel"),
 (T_DORMIR, T_J11B - 0.03, "dormir"),                                   # esconde a troca C→B
 (wt("envía", "J12") - 0.05, wt("toca", "J12") - 0.05, "abraco"),
]
# ---------------- leitura ----------------
CORTE = {"casa": (0, 7), "chora": (8, 0), "carro": (11, 0), "sb": (0, 4), "biblia": (3, 13), "silhueta": (0, 13)}
class Pngs:
    def __init__(s, d, a=None, b=None):
        s.fs = sorted((B / d / "limpo").glob("f_*.png")) if (B / d / "limpo").exists() else sorted((B / d).glob("f_*.png")); s.c = {}
        x, y = CORTE.get(d, (0, 0)); s.fs = s.fs[x:len(s.fs) - y]
        if a is not None or b is not None: s.fs = s.fs[a:b]
    def __len__(s): return len(s.fs)
    def q(s, k):
        k = max(0, min(len(s.fs) - 1, k))
        if k not in s.c:
            if len(s.c) > 8: s.c.clear()
            s.c[k] = np.asarray(Image.open(s.fs[k]).convert("RGB"))
        return s.c[k]
class Rolo:
    """imagem alta (notificações) rolando"""
    def __init__(s, p): s.im = np.asarray(Image.open(p).convert("RGB"))
    def __len__(s): return 10 ** 6
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
AV = {"A": Avatar(P / "avatar/A.mp4"), "B": Avatar(P / "avatar/B.mp4"), "D": Avatar(P / "dono2/D.mp4"), "C": Avatar(P / "v3/C.mp4"),
      "Ch": Avatar(P / "v3/C.mp4")}
NEWS_LS, NEWS = Pngs("news_ls"), Pngs("news")
CH = Pngs("cheio", 0, 101); CH_FIM = Pngs("cheio", 101, None)            # fim do lotado fica para a tela dividida / ganchos
BRP = {d: (Rolo(P / "v3/notif.png") if d == "notif" else Pngs(d)) for _, _, d in BR}
REF_BAND = NEWS.q(90).astype(np.int16)
# ---------------- legenda ----------------
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
FL = ImageFont.truetype(str(POP / "Poppins-Bold.ttf"), 42); VERDE = (24, 200, 24)
def blocos(pal):
    out, cur = [], []
    for p in pal:
        cur.append(p); txt = " ".join(lw(x["w"]) for x in cur)
        if len(cur) >= 3 or len(txt) >= 15 or re.search(r"[,.:;!?»…]$", p["w"]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def montar_bl(pal):
    bl = []
    for ln in dict.fromkeys(p["linha"] for p in pal):
        lp = [p for p in pal if p["linha"] == ln]
        lp = ([p for p in lp if p["ini"] < 18.3], [p for p in lp if p["ini"] >= 18.3]) if ln == "D2" else (lp,)
        for part in lp:
            bs = blocos(part)
            for i, b in enumerate(bs):
                prox = bs[i + 1][0]["ini"] - 0.04 if i + 1 < len(bs) else b[-1]["fim"] + 0.35
                bl.append(dict(ini=max(0, b[0]["ini"] - 0.04), fim=prox, ws=[(lw(x["w"]), x["ini"]) for x in b]))
    bl.sort(key=lambda x: x["ini"])
    for x, y in zip(bl, bl[1:]): x["fim"] = min(x["fim"], y["ini"])
    return bl
BL = montar_bl(PAL)
_cache = {}
def leg(t, bl=None, tag="v"):
    bl = BL if bl is None else bl
    for k, b in enumerate(bl):
        if b["ini"] <= t < b["fim"]:
            at = max([i for i, (_, wi) in enumerate(b["ws"]) if wi <= t + 0.02] or [0]); key = (tag, k, at)
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
def rgba(n, d=OV): return Image.open(d / n).convert("RGBA")
FAIXA, ROD, MOLD, SELO, ELIM, SALMO, VIVO, TOCA, SETA = (rgba(n) for n in ("faixa.png", "rodape.png", "moldura_jm.png", "selo10.png", "eliminado.png",
                                                                          "salmo.png", "en_vivo.png", "toca.png", "seta.png"))
VID_ELIM = rgba("eliminado.png", Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\ov"))   # «VIDEO ELIMINADO»
T_TOCA = wt("toca", "J12"); T_SAL0, T_SAL1 = wt("salmo", "J10") - 0.05, LIN["J10"]["fim"] + 0.12
T_VIVO0, T_VIVO1 = wt("por", "J11a") - 0.05, T_JN0 - 0.05
T_ELIM0, T_ELIM1 = T_ALTO + 0.35, wt("transmisión", "J07") + 0.9
def pop(im, t, t0, dur=0.18):
    u = (t - t0) / dur
    if u >= 1.6: return im
    s = 0.7 + 0.36 * min(max(u, 0), 1) if u < 1 else 1.06 - 0.06 * (u - 1) / 0.6
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
def centro(base, im, cx, cy): base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
def pop_full(im, t, t0):
    u = (t - t0) / 0.22
    if u >= 1.6 or u < 0: return im if u >= 1.6 else None
    bb = im.getbbox(); c = im.crop(bb); s = 0.7 + 0.36 * min(u, 1) if u < 1 else 1.06 - 0.06 * (u - 1) / 0.6
    c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.BICUBIC)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    out.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2))); return out
rng = np.random.default_rng(7)
def glitch(f, t, t0, dur=0.55):
    u = (t - t0) / dur
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
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2: return np.zeros(f.shape[:2], np.float32)
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); keep = (lab == k).astype(np.uint8)
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    keep = cv2.dilate(keep, np.ones((3, 3), np.uint8))
    velho = (f[960:].min(2) > 205) & (REF_BAND[960:].min(2) > 205)
    fb = f[960:].astype(np.int16); branco = (fb.min(2) > 175) & ((fb.max(2) - fb.min(2)) < 45); branco[:, 350:] = False
    velho |= branco
    keep[cv2.dilate(velho.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 0
    full = np.zeros(f.shape[:2], np.float32); full[960:] = cv2.GaussianBlur(keep.astype(np.float32), (5, 5), 0); full[945:960] = full[962]
    return full
def dividida(k):
    """VAZIO (orig 5,6-6,6 s, não usado depois) | LOTADO (fim do take cheio). Corte central de 356 px de cada."""
    l = NEWS.q(168 + k); r = CH_FIM.q(k)
    f = np.empty((1280, 720, 3), np.uint8); f[:, :358] = l[:, 170:528]; f[:, 362:] = r[:, 182:540]; f[:, 358:362] = 255
    f[132:318] = (198, 12, 16)          # faixa antiga cortada fora do lugar: fundo vermelho de borda a borda sob a faixa nova
    return f
# ---------------- quadro base v3 ----------------
def base(t):
    if t < T_SPLIT: return dividida(int(t * 30)), "news"
    if t < T_DA:
        k = int(round((t - T_SPLIT) * 30)); return (NEWS_LS.q(k) if k < len(NEWS_LS) else NEWS.q(k)), "news"
    if t < T_CH: return AV["D"].quadro(int(round((t - T_DA) * 25))), "dono"
    if t < T_DB:
        vel = max(0.5, min(1.0, len(CH) / 30 / (T_DB - T_CH))); return CH.q(int((t - T_CH) * vel * 30)), "cheio"
    if t < T_JM: return AV["D"].quadro(int(round((178 / 30 + t - 18.35) * 25))), "dono"
    for t0, t1, d in BR:
        if t0 <= t < t1:
            fr = BRP[d]
            if isinstance(fr, Rolo):
                u = (t - t0) / (t1 - t0); u = u * u * (3 - 2 * u); H = fr.im.shape[0]; y = int(150 + (H - 1280 - 150) * u * 0.6); return fr.im[y:y + 1280], "broll"
            vel = max(0.5, min(1.0, len(fr) / 30 / (t1 - t0))); return fr.q(int((t - t0) * vel * 30)), "broll"
    if t < B_OFF + 0.25 - 0.2: return AV["A"].quadro(int(round((t - A_OFF) * 25))), "padre"
    if t < T_JN0 - 0.05: return AV["B"].quadro(int(round((t - B_OFF) * 25))), "padre"
    if t < T_J11B - 0.03: return AV["C"].quadro(int(round((t - C_OFF) * 25))), "padre"
    return AV["B"].quadro(int(round((t - DELTA - B_OFF) * 25))), "padre"
def quadro_v3(t):
    f, tipo = base(t)
    if tipo == "padre":
        f = glitch(f, t, T_ALTO); dx, dy = tremor(t)
        if dx or dy: f = cv2.warpAffine(f, np.float32([[1.03, 0, dx - 10.8], [0, 1.03, dy - 19.2]]), (720, 1280), borderMode=cv2.BORDER_REFLECT)
    im = Image.fromarray(np.ascontiguousarray(f)).convert("RGBA")
    if tipo in ("news", "cheio"):
        im.alpha_composite(ROD)
        if tipo == "news" and T_SPLIT <= t < T_SPLIT + 1.9:
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
    if lg is not None: im.alpha_composite(lg, (0, (775 if tipo == "dono" else 685) - 55))
    im.alpha_composite(SELO)
    return np.asarray(im.convert("RGB"))
# ---------------- ganchos ----------------
TTD = P / "tts"
def pal_tts(k, off):
    al = json.load(open(TTD / f"{k}.alinhamento.json", encoding="utf-8"))
    out = []; w = ""
    for c, x, y in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if w: out.append(dict(w=w, ini=round(ws + off, 3), fim=round(we + off, 3), linha=k)); w = ""
        else:
            if not w: ws = x
            w += c; we = y
    if w: out.append(dict(w=w, ini=round(ws + off, 3), fim=round(we + off, 3), linha=k))
    return out
def dur_tts(k): return librosa.get_duration(path=str(TTD / f"{k}.mp3"))
C_INFO = json.load(open(P / "v3/C.json", encoding="utf-8"))
G5V = P / "v3/moedas.mp4"
HOOK = None
if a_.gancho:
    g = a_.gancho
    TIT = None
    if g == "G1":
        T0 = 0.5; C0 = C_INFO["JG1"]["ini_c"] - T0; H = C_INFO["total"] - C0 - 0.05
        VO = [("JG1", C_INFO["JG1"]["a"], T0)]; bed = "tensao"
        ft = ImageFont.truetype(str(POP / "Poppins-ExtraBold.ttf"), 44)
        TIT = Image.new("RGBA", (720, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(TIT)
        d.rounded_rectangle((26, 8, 694, 222), 24, fill=(0, 0, 0, 205))
        d.ellipse((60, 36, 92, 68), fill=(235, 30, 30, 255)); d.text((106, 52), "EN VIVO:", font=ft, anchor="lm", fill=(235, 30, 30, 255))
        for i, l in enumerate(["la oración a San Benito", "que casi nadie conoce"]): d.text((360, 118 + i * 58), l.upper(), font=ImageFont.truetype(str(POP / "Poppins-ExtraBold.ttf"), 38), anchor="mm", fill=(255, 255, 255, 255))
        def hframe(t):
            im = Image.fromarray(np.ascontiguousarray(AV["Ch"].quadro(int(round((t + C0) * 25))))).convert("RGBA"); im.alpha_composite(MOLD)
            im.alpha_composite(VIVO, (24, 168)); centro(im, pop(TIT, t, 0.05, 0.22), 360, 905); return im, "padre"
    elif g == "G2":
        T0 = 0.15; d2 = dur_tts("G2"); H = T0 + d2 + 1.05; T_CUT = T0 + d2 + 0.05
        VO = [("G2", 0.0, T0)]; bed = "sfx"
        VAZ = Pngs("news", 72, 168)
        def hframe(t):
            if t < T_CUT:
                vel = min(1.0, len(VAZ) / 30 / T_CUT); f = VAZ.q(int(t * vel * 30))
            else: f = CH_FIM.q(int((t - T_CUT) * 30))
            im = Image.fromarray(np.ascontiguousarray(f)).convert("RGBA"); im.alpha_composite(ROD); fx = pop_full(FAIXA, t, 0.0)
            if fx is not None: im.alpha_composite(fx)
            return im, "news"
    elif g == "G3":
        T0 = 0.15; d3 = dur_tts("G3"); H = T0 + d3 + 0.7; TG = T0 + d3 - 0.6
        VO = [("G3", 0.0, T0)]; bed = "sfx"
        def hframe(t):
            f = CH_FIM.q(int(min(t, 2.0) * 0.5 * 30))
            for tg in (0.35, 1.45, TG): f = glitch(f, t, tg, 0.4)
            im = Image.fromarray(np.ascontiguousarray(f)).convert("RGBA"); im.alpha_composite(ROD); im.alpha_composite(FAIXA)
            if t >= TG + 0.1 and ((t - TG - 0.1) % 0.6) < 0.45: centro(im, VID_ELIM, 360, 930)
            return im, "news"
    elif g == "G4":
        T0 = 0.15; d4 = dur_tts("G4"); H = T0 + d4 + 0.45
        VO = [("G4", 0.0, T0)]; bed = "tensao"
        VAZ = Pngs("news", 72, 168)
        def hframe(t):
            vel = max(0.5, min(1.0, len(VAZ) / 30 / H)); f = VAZ.q(int(t * vel * 30))
            im = Image.fromarray(np.ascontiguousarray(f)).convert("RGBA"); im.alpha_composite(ROD); im.alpha_composite(FAIXA); return im, "news"
    elif g == "G5":
        T0 = 0.2; d5 = dur_tts("G5"); H = T0 + d5 + 0.45
        VO = [("G5", 0.0, T0)]; bed = "tensao"
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(G5V), "-vf", "scale=720:1280:in_color_matrix=bt709:in_range=limited:flags=accurate_rnd+full_chroma_int+lanczos,format=rgb24",
                            "-f", "rawvideo", "-"], capture_output=True).stdout
        G5F = np.frombuffer(r, np.uint8).reshape(-1, 1280, 720, 3); vel5 = max(0.5, min(1.0, len(G5F) / 24 / H))   # Kling 24 qps
        def hframe(t): return Image.fromarray(np.ascontiguousarray(G5F[min(len(G5F) - 1, int(t * vel5 * 24))])).convert("RGBA"), "broll"
    HPAL = []
    for k, a, t0 in VO: HPAL += [dict(p, ini=p["ini"] - a, fim=p["fim"] - a) for p in pal_tts(k, t0)]
    HBL = montar_bl(HPAL)
    HOOK = dict(H=round(H, 3), VO=VO, bed=bed, frame=hframe, bl=HBL)
    print(g, "gancho", round(H, 2), "s")
# ---------------- vídeo ----------------
if HOOK: LINHA = [("h", j / FPS) for j in range(int(round(HOOK["H"] * FPS)))] + [("v", T_DA + j / FPS) for j in range(int(round((T_END - T_DA) * FPS)))]
else: LINHA = [("v", j / FPS) for j in range(int(round(T_END * FPS)))]
NOUT = len(LINHA); OUTV = T / f"v3_{NOME}_video.mp4"
if not a_.so_audio:
    j0 = int(round(a_.de * FPS)); j1 = NOUT if a_.ate is None else int(round(a_.ate * FPS))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "30", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
                            "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-profile:v", "high",
                            "-color_range", "tv", "-colorspace", "smpte170m", "-color_primaries", "smpte170m", "-color_trc", "smpte170m", str(OUTV)],
                           stdin=subprocess.PIPE)
    for j in range(j0, j1):
        src, t = LINHA[j]
        if j % 300 == 0: print(f"[{j}/{NOUT}] {100 * j // NOUT}%", flush=True)
        if src == "h":
            im, tipo = HOOK["frame"](t)
            lg = leg(t, HOOK["bl"], "h")
            if lg is not None: im.alpha_composite(lg, (0, 685 - 55))
            im.alpha_composite(SELO); fr = np.asarray(im.convert("RGB"))
        else: fr = quadro_v3(t)
        enc.stdin.write(np.ascontiguousarray(fr).tobytes())
    enc.stdin.close(); enc.wait(); print("vídeo ok", OUTV.name, NOUT, "quadros")
# ---------------- áudio ----------------
SR = 48000; med = pyln.Meter(SR); NA = int(round(T_END * SR))
voz = librosa.load(P / "voz3.wav", sr=SR, mono=True)[0][:NA]; voz = np.pad(voz, (0, NA - len(voz)))
voz *= 10 ** ((-18.0 - med.integrated_loudness(voz)) / 20)
def norm(y, alvo):
    y = y.T if y.ndim > 1 else np.stack([y, y], 1); return y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)
def fade(s, a=0.3, b=0.3):
    s = s.copy(); na, nb = int(a * SR), int(b * SR)
    if na: s[:na] *= np.linspace(0, 1, na)[:, None]
    if nb: s[-nb:] *= np.linspace(1, 0, nb)[:, None]
    return s
V4M = Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\musica")
sfx = norm(librosa.load(P / "musica_sfx_restaurante.mp3", sr=SR, mono=False)[0], -28.0)
ten = norm(librosa.load(V4M / "tensao.mp3", sr=SR, mono=False)[0], -32.0); esp = norm(librosa.load(V4M / "esperanca.mp3", sr=SR, mono=False)[0], -32.0)
mus = np.zeros((NA, 2))
a = int(T_DA * SR); mus[:a] += fade(sfx[:a], 0.15, 0.35)                                   # notícia
c0, c1 = int(T_CH * SR), int(T_DB * SR); mus[c0:c1] += fade(sfx[a:a + c1 - c0], 0.25, 0.3)  # corte do salão
a = int(T_JM * SR); T_VIR = wt("claro", "J09") - 0.05; b = int(T_VIR * SR)
s = ten[:b - a + int(0.3 * SR)].copy(); s = fade(s, 0.4, 0.3); mus[a:a + len(s)] += s
s = fade(esp[: NA - b], 0.5, 0.8); mus[b:b + len(s)] += s
g = rng.standard_normal(int(0.38 * SR)) * 0.5; g = np.sign(g) * (np.abs(g) > 0.6) * np.repeat(rng.random(len(g) // 400 + 1) > 0.4, 400)[:len(g)]
g *= np.linspace(1, 0, len(g)) ** 0.7; g *= 0.05 / (np.sqrt(np.mean(g ** 2)) + 1e-9); ga = int(T_ALTO * SR); mus[ga:ga + len(g)] += np.stack([g, g], 1)
mix = mus + voz[:, None]
if HOOK:
    NH = int(round(HOOK["H"] * SR)); hv = np.zeros(NH)
    for k, a0, t0 in HOOK["VO"]:
        y = librosa.load(TTD / f"{k}.mp3", sr=SR, mono=True)[0][int(a0 * SR):]; n = min(len(y), NH - int(t0 * SR)); hv[int(t0 * SR):int(t0 * SR) + n] += y[:n]
    hv *= 10 ** ((-18.0 - med.integrated_loudness(np.pad(hv, (0, max(0, SR - NH))))) / 20)
    bedv = sfx[-NH - int(0.5 * SR):-int(0.5 * SR)] if HOOK["bed"] == "sfx" else ten[-NH:] * 0.9
    hm = fade(bedv[:NH], 0.1, 0.25) + hv[:, None]
    if a_.gancho == "G3":
        for tg in (0.35, 1.45):
            gg = g[:int(0.3 * SR)]; i0 = int(tg * SR); hm[i0:i0 + len(gg)] += np.stack([gg, gg], 1)
    corpo = mix[int(T_DA * SR):]
    mix = np.concatenate([hm, corpo])
sf.write(T / f"_mix_{NOME}.wav", mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T / f"_mix_{NOME}.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled",
                "-ar", "48000", "-c:a", "pcm_s16le", str(T / f"v3_{NOME}_audio.wav")], check=True)
m2 = sf.read(T / f"v3_{NOME}_audio.wav")[0]
print("LUFS final", round(med.integrated_loudness(m2), 1), "| dur áudio", round(len(m2) / SR, 2), "| vídeo", round(NOUT / FPS, 2))
