# -*- coding: utf-8 -*-
"""VIDEO 04 → SB ES «La oración escondida». Tela dividida (Juan Méndez na live em cima, b-roll embaixo) com trechos em tela cheia.
Leitura de cada fonte com a matriz da etiqueta dela; saída única com matriz bt601/tv FIXA (etiqueta smpte170m/tv), 1 passada.
uso: python montar.py [--so-audio] [--de s --ate s --saida x.mp4]"""
import json, re, subprocess, sys, argparse
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent; T = P / "_trab"; T.mkdir(exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SB-BANCO-BROLL")
ap = argparse.ArgumentParser(); ap.add_argument("--so-audio", action="store_true"); ap.add_argument("--de", type=float, default=0)
ap.add_argument("--ate", type=float, default=None); ap.add_argument("--saida", default=str(T / "_video.mp4")); a_ = ap.parse_args()
FPS = 30; SEAM = 716; BH = 1280 - SEAM
TP = json.load(open(P / "tempos.json", encoding="utf-8")); PAL = TP["palavras"]
T_END = 85.30; NOUT = int(round(T_END * FPS))
T_SW = 43.05                         # troca A→B (no glitch do ¡Alto!)
def at_avatar(t):
    return ("A", t + 0.25) if t < T_SW else ("B", t - 43.155 + 0.25)
# ---------------- plano ----------------
# modo F (tela cheia, Juan) : (ini, fim, zoom0, zoom1)
FULL = [(0.0, 3.90, 1.0, 1.14), (24.40, 27.85, 1.0, 1.08), (60.30, 64.62, 1.0, 1.05), (64.62, 68.10, 1.13, 1.17), (78.80, T_END, 1.0, 1.07)]
# b-roll embaixo: (ini, fim, tipo, fonte, opções)
B = [
 (3.90, 9.15, "vid", P / "broll/gen_pergaminho.mp4", dict(y=330, src_in=0.0)),
 (9.15, 13.95, "vid", P / "broll/gen_corrente.mp4", dict(y=380, src_in=0.0)),
 (13.95, 15.45, "vid", BR / "problema/problema_01_contas-mesa-cozinha.mp4", dict()),
 (15.45, 16.85, "vid", BR / "problema/problema_10_porta-aco-cadeado.mp4", dict()),
 (16.85, 19.95, "vid", BR / "oracion/oracion_11_hombre-rezando-carro.mp4", dict()),
 (19.95, 21.85, "vid", BR / "problema/problema_19_pote-moedas.mp4", dict()),
 (21.85, 23.30, "vid", BR / "problema/problema_12_casal-discutindo-costas.mp4", dict()),
 (23.30, 24.40, "vid", BR / "problema/problema_30_mulher-vela-apagao.mp4", dict()),
 (27.85, 29.00, "png", P / "broll/orig/ros/limpo", dict(y=450)),
 (29.00, 30.00, "png", P / "broll/orig/sen/limpo", dict(y=260)),
 (30.00, 32.00, "png", P / "broll/orig/sb/limpo", dict(y=60, y1=620)),
 (32.00, 34.50, "vid", BR / "sagrado/sagrado_08_manuscrito-iluminado-vela.mp4", dict()),
 (34.50, 37.90, "png", P / "broll/orig/sbluz/limpo", dict(y=330)),
 (37.90, 40.60, "vid", BR / "sagrado/sagrado_26_cruz-pedra-tempestade.mp4", dict()),
 (40.60, T_SW, "vid", BR / "sagrado/sagrado_25_cruz-pedra-topo-montanha.mp4", dict()),
 (T_SW, 46.85, "vid", BR / "problema/problema_11_celular-sem-mensagens.mp4", dict()),
 (46.85, 49.45, "vid", BR / "sagrado/sagrado_35_celular-acendendo-escuro.mp4", dict()),
 (49.45, 52.20, "wa", P / "wa/wa1.png", dict()),
 (52.20, 54.95, "wa", P / "wa/wa2.png", dict()),
 (54.95, 57.75, "wa", P / "wa/wa3.png", dict()),
 (57.75, 60.30, "vid", BR / "sagrado/sagrado_32_idosa-celular-emocionada.mp4", dict()),
 (68.10, 71.45, "vid", BR / "oracion/oracion_30_capilla-noche-velas.mp4", dict()),
 (71.45, 74.60, "vid", BR / "sagrado/sagrado_34_familia-celular-juntos.mp4", dict()),
 (74.60, 78.80, "png", P / "broll/orig/chave/limpo", dict(y=420)),
]
# ---------------- leitura ----------------
def matriz(p):
    o = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_space,color_range,r_frame_rate",
                                   "-of", "json", str(p)], capture_output=True, text=True).stdout)["streams"][0]
    cs = o.get("color_space", ""); m = "bt709" if cs == "bt709" else "bt601"
    rg = "full" if o.get("color_range") == "pc" else "limited"; a, b = o["r_frame_rate"].split("/")
    return m, rg, int(a) / int(b)
def ler_vid(p, t0, dur, w=720, h=1280):
    m, rg, fps = matriz(p)
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", str(p), "-t", f"{dur + 0.2:.3f}", "-vf",
                        f"scale={w}:{h}:in_color_matrix={m}:in_range={rg}:flags=accurate_rnd+full_chroma_int+lanczos,format=rgb24",
                        "-fps_mode", "passthrough", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(r, np.uint8).reshape(-1, h, w, 3), fps
class Avatar:
    """leitura sequencial (A/B, 25 qps, sem etiqueta → bt601/tv)"""
    def __init__(s, p): s.p = p; s.pr = None; s.i = -1; s.f = None
    def abrir(s):
        s.pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(s.p), "-vf", "scale=in_color_matrix=bt601:in_range=limited:flags=accurate_rnd+full_chroma_int,format=rgb24",
                                 "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    def quadro(s, k):
        if s.pr is None: s.abrir()
        while s.i < k:
            b = s.pr.stdout.read(720 * 1280 * 3)
            if len(b) < 720 * 1280 * 3: break
            s.f = np.frombuffer(b, np.uint8).reshape(1280, 720, 3); s.i += 1
        return s.f
AV = {"A": Avatar(P / "avatar/A.mp4"), "B": Avatar(P / "avatar/B.mp4")}
# ---------------- legenda (palavra a palavra, 1 palavra verde, na emenda) ----------------
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
FL = ImageFont.truetype(str(POP / "Poppins-Bold.ttf"), 42)
VERDE = (24, 200, 24)
def limpa(w): return re.sub(r"[¡!¿?,.:;«»…]", "", w).lower()
def blocos(pal):
    out, cur = [], []
    for p in pal:
        cur.append(p); txt = " ".join(limpa(x["w"]) for x in cur)
        if len(cur) >= 3 or len(txt) >= 15 or re.search(r"[,.:;!?»…]$", p["w"]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
BL = []
for ln in range(1, 14):
    bs = blocos([p for p in PAL if p["linha"] == ln])
    for i, b in enumerate(bs):
        ini = max(0, b[0]["ini"] - 0.04)
        prox = bs[i + 1][0]["ini"] - 0.04 if i + 1 < len(bs) else b[-1]["fim"] + 0.35
        BL.append(dict(ini=ini, fim=prox, ws=[(limpa(x["w"]), x["ini"]) for x in b]))
for x, y in zip(BL, BL[1:]): x["fim"] = min(x["fim"], y["ini"])
_cache = {}
def leg(t):
    for k, b in enumerate(BL):
        if b["ini"] <= t < b["fim"]:
            at = max([i for i, (_, wi) in enumerate(b["ws"]) if wi <= t + 0.02] or [0])
            key = (k, at)
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
OV = P / "ov"
def rgba(n): return Image.open(OV / n).convert("RGBA")
MOLD, SELO, TIT, BLOQ, FORMA, ELIM, VIVO, TOCA, SETA = (rgba(n) for n in ("moldura_jm.png", "selo10.png", "titulo.png", "bloqueado.png",
                                                                          "forma_correcta.png", "eliminado.png", "en_vivo.png", "toca.png", "seta.png"))
def wt(prefix, linha):
    return next(p["ini"] for p in PAL if p["linha"] == linha and limpa(p["w"]).startswith(prefix))
T_BLOQ = wt("bloqueado", 5) - 0.05; T_FORMA = wt("correcta", 10) - 0.05; T_TOCA = wt("toca", 13)
T_ALTO = T_SW; T_ELIM = T_ALTO + 0.35
T_VIVO0, T_VIVO1 = 68.10, 78.80
print(f"BLOQUEADO {T_BLOQ:.2f} | FORMA CORRECTA {T_FORMA:.2f} | CTA {T_TOCA:.2f}")
def pop(im, t, t0, dur=0.18):
    """entrada com 'pop' (escala 0,7→1,06→1)"""
    u = (t - t0) / dur
    if u >= 1.6: return im
    s = 0.7 + 0.36 * min(u, 1) if u < 1 else 1.06 - 0.06 * (u - 1) / 0.6
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
def centro(base, im, cx, cy): base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
# ---------------- efeitos ----------------
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
def zoom(f, z, cx=360, cy=430):
    if abs(z - 1) < 1e-3: return f
    M = np.float32([[z, 0, cx - z * cx], [0, z, cy - z * cy]])
    return cv2.warpAffine(f, M, (720, 1280), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
# ---------------- b-roll ----------------
def preparar(seg):
    t0, t1, tipo, src, o = seg; dur = t1 - t0
    if tipo == "vid":
        fr, fps = ler_vid(src, o.get("src_in", 0.05), 5.0)
        disp = len(fr) / fps - 0.05; vel = max(0.5, min(1.0, disp / dur))
        def f(t, fr=fr, fps=fps, vel=vel, y=o.get("y", 358)):
            k = min(len(fr) - 1, int(round((t - t0) * vel * fps))); return fr[k][y:y + BH]
        return f, vel
    if tipo == "png":
        fs = sorted(src.glob("f_*.png")); disp = len(fs) / 30; vel = max(0.5, min(1.0, disp / dur))
        cache = {}
        def f(t, fs=fs, vel=vel):
            k = min(len(fs) - 1, int(round((t - t0) * vel * 30)))
            if k not in cache: cache.clear(); cache[k] = np.asarray(Image.open(fs[k]).convert("RGB"))
            y = o.get("y", 358)
            if "y1" in o: u = (t - t0) / dur; e = u * u * (3 - 2 * u); y = int(o["y"] + (o["y1"] - o["y"]) * e)
            return cache[k][y:y + BH]
        return f, vel
    if tipo == "wa":
        im = np.asarray(Image.open(src).convert("RGB")); H = im.shape[0]
        def f(t, im=im, H=H):
            u = (t - t0) / dur; y = int((H - BH) * min(1, u * 1.15)); return im[y:y + BH]
        return f, 1.0
if not a_.so_audio:
    j0 = int(round(a_.de * FPS)); j1 = NOUT if a_.ate is None else int(round(a_.ate * FPS))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "30", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
                            "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-profile:v", "high",
                            "-color_range", "tv", "-colorspace", "smpte170m", "-color_primaries", "smpte170m", "-color_trc", "smpte170m", a_.saida],
                           stdin=subprocess.PIPE)
    seg_atual = None; fn = None; vel_log = {}
    for j in range(j0, j1):
        t = j / FPS
        if j % 150 == 0: print(f"[{j}/{NOUT}] {100 * j // NOUT}%", flush=True)
        nome, at = at_avatar(t); af = AV[nome].quadro(int(round(at * 25)))
        full = next((x for x in FULL if x[0] <= t < x[1]), None)
        if full:
            u = (t - full[0]) / (full[1] - full[0])
            if full[0] == 0.0: z = 1.0 + 0.10 * min(1, (t / 0.5)) ** 0.5 + 0.04 * u      # zoom rápido no início
            else: z = full[2] + (full[3] - full[2]) * u
            f = zoom(af, z)
        else:
            seg = next(x for x in B if x[0] <= t < x[1])
            if seg is not seg_atual: seg_atual = seg; fn, vel = preparar(seg); vel_log[str(seg[3].name)] = round(vel, 2)
            f = np.empty((1280, 720, 3), np.uint8); f[:SEAM] = af[40:40 + SEAM]; f[SEAM:] = fn(t)
        f = glitch(f, t)
        dx, dy = tremor(t)
        if dx or dy: f = cv2.warpAffine(f, np.float32([[1.03, 0, dx - 10.8], [0, 1.03, dy - 19.2]]), (720, 1280), borderMode=cv2.BORDER_REFLECT)
        im = Image.fromarray(f).convert("RGBA")
        im.alpha_composite(MOLD)
        giant = None
        if t < 3.90: centro(im, pop(TIT, t, 0.10), 360, 1010)
        if T_BLOQ <= t < 27.85: giant = pop(BLOQ, t, T_BLOQ); centro(im, giant, 360, 985)
        if T_FORMA <= t < 68.10: giant = pop(FORMA, t, T_FORMA); centro(im, giant, 360, 1000)
        if T_ELIM <= t < 49.45 and ((t - T_ELIM) % 0.6) < 0.42: centro(im, ELIM, 360, SEAM + BH // 2 + 20)
        if T_VIVO0 <= t < T_VIVO1: im.alpha_composite(VIVO, (24, 1280 - VIVO.height - 40))
        if t >= T_TOCA:
            centro(im, pop(TOCA, t, T_TOCA), 360, 905)
            dyy = int(round(16 * np.sin(2 * np.pi * 1.6 * (t - T_TOCA))))
            for x in (200, 391): im.alpha_composite(SETA, (x, 985 + dyy))
        if giant is None:
            lg = leg(t)
            if lg is not None: im.alpha_composite(lg, (0, SEAM - 55))
        im.alpha_composite(SELO)
        enc.stdin.write(np.asarray(im.convert("RGB")).tobytes())
    enc.stdin.close(); enc.wait(); print("vídeo ok", vel_log)
# ---------------- áudio ----------------
SR = 48000; med = pyln.Meter(SR); NA = int(round(NOUT / FPS * SR))
voz = librosa.load(P / "voz.wav", sr=SR, mono=True)[0][:NA]; voz = np.pad(voz, (0, NA - len(voz)))
voz *= 10 ** ((-18.0 - med.integrated_loudness(voz)) / 20)   # mono -18 = -15 em estéreo
def trilha(nome, alvo=-32.0):
    y = librosa.load(P / "musica" / f"{nome}.mp3", sr=SR, mono=False)[0]
    y = y.T if y.ndim > 1 else np.stack([y, y], 1)
    return y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)
ten, esp = trilha("tensao"), trilha("esperanca")
mus = np.zeros((NA, 2))
a = int(T_ALTO * SR); s = ten[:a].copy(); n = int(0.12 * SR); s[-n:] *= np.linspace(1, 0, n)[:, None]; s[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))[:, None]
mus[:a] += s
b0 = int((T_ALTO + 0.45) * SR); s = esp[: NA - b0].copy(); n = int(1.4 * SR); s[:n] *= (np.linspace(0, 1, n) ** 1.5)[:, None]
e = int(0.8 * SR); s[-e:] *= np.linspace(1, 0, e)[:, None]; mus[b0:b0 + len(s)] += s
# glitch: ruído digital curto
g = rng.standard_normal(int(0.38 * SR)) * 0.5; g = np.sign(g) * (np.abs(g) > 0.6) * np.repeat(rng.random(len(g) // 400 + 1) > 0.4, 400)[:len(g)]
g *= np.linspace(1, 0, len(g)) ** 0.7; g *= 0.05 / (np.sqrt(np.mean(g ** 2)) + 1e-9)
mus[a:a + len(g)] += np.stack([g, g], 1)
mix = mus + voz[:, None]
sf.write(T / "_mix.wav", mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T / "_mix.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled",
                "-ar", "48000", "-c:a", "pcm_s16le", str(T / "audio.wav")], check=True)
m2 = sf.read(T / "audio.wav")[0]
print("LUFS final", round(med.integrated_loudness(m2), 1), "| voz", round(med.integrated_loudness(voz), 1), "| trilha", round(med.integrated_loudness(mus), 1))
