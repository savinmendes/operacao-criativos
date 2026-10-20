# -*- coding: utf-8 -*-
"""CORPO SB ES «Padre capturado»: V0 (gancho v4 com título Juan Méndez + corpo novo) e corpo a partir da selfie.
Quadros do v4 refeitos a partir da base sem legenda (mesma lógica do montar_final.py do v4) + bocas novas do HeyGen + b-roll do banco
+ arroba nova + legenda + EN VIVO + CTA com setas + selo. Áudio: voz do v4 nos trechos mantidos, falas novas, trilha do v4 (demucs)."""
import json, pickle, subprocess, sys, numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from pathlib import Path
from PIL import Image, ImageDraw
T = Path(__file__).resolve().parent; C = T.parent
sys.path.insert(0, str(T))
import cor, arroba, legenda2
from plano import *
from pal import ali
AQ = GA / "audio"
sys.path.insert(0, str(AQ)); import legenda_es
SR = 44100; FPS = 30
# ---------------- linha do tempo (quadros) ----------------
def nq(s): return int(round(s * FPS))
SEGS = [("G", "v4", 0, 240), ("S1", "v4", 241, 507), ("S2", "linha", "chora"), ("S3", "linha", "jm1"), ("S4", "v4", 980, 1325),
        ("S5", "linha", "jm2"), ("S6", "v4", 2492, 2701), ("S7", "v4", 3197, 3556), ("S8", "linha", "jm3")]
tl = []; j = 0
for s in SEGS:
    n = (s[3] - s[2] + 1) if s[1] == "v4" else nq(LINHAS[s[2]]["fim"])
    tl.append(dict(id=s[0], tipo=s[1], a=s[2], b=s[3] if s[1] == "v4" else None, j0=j, n=n)); j += n
NOUT = j; J_SELFIE = tl[1]["j0"]
print("quadros", NOUT, "dur", NOUT / FPS, "| selfie em", J_SELFIE / FPS)
# ---------------- legenda ----------------
P4 = json.load(open(AQ / "palavras_es.json", encoding="utf-8"))
DM = json.load(open(AQ / "v2/difmask.json"))
def geo_i(i): return "rm" if 2280 <= i < 2622 else "r"
grupos = []
for s in tl:
    t0, t1 = s["j0"] / FPS, (s["j0"] + s["n"]) / FPS
    if s["id"] == "G": continue
    ws = []
    if s["tipo"] == "v4":
        a, b = s["a"] / FPS, (s["b"] + 1) / FPS; st = "c" if s["id"] == "S1" else "r"
        for p in P4:
            if a <= p["ini"] < b - 0.05:
                i = int(p["ini"] * FPS)
                ws.append(dict(w=p["w"], ini=t0 + p["ini"] - a, fim=t0 + min(p["fim"], b) - a, st=st, geo="c" if st == "c" else geo_i(i)))
    else:
        L = LINHAS[s["a"]]; st = "c" if s["a"] == "chora" else "r"
        for w, x0, x1 in ali(T / "tts" / f"{L['tts']}.alinhamento.json"):
            ws.append(dict(w=w, ini=t0 + L["lead"] + x0, fim=t0 + L["lead"] + x1, st=st, geo="c" if st == "c" else "r"))
    grupos.append((t0, t1, ws))
LEG = legenda2.Legenda(grupos)
LEG_G = legenda_es.Legenda(AQ / "palavras_es.json")
# ---------------- CTA ----------------
s8 = tl[-1]; T_S8 = s8["j0"] / FPS
toca = next(x0 for w, x0, x1 in ali(T / "tts" / "jm3.alinhamento.json") if w.lower().startswith("toca"))
T_CTA = T_S8 + LINHAS["jm3"]["lead"] + toca
T_VIVO = T_S8 + 3.10
print("CTA em", round(T_CTA, 2), "| EN VIVO em", round(T_VIVO, 2))
OVD = T / "ov"
def rgba(p): return Image.open(OVD / p).convert("RGBA")
TIT, SELO, VIVO, TOCA, SETA = rgba("titulo_gancho_jm.png"), rgba("selo.png"), rgba("en_vivo.png"), rgba("toca.png"), rgba("seta.png")
# ---------------- áudio ----------------
def ld(p): return librosa.load(p, sr=SR, mono=True)[0]
def fade(y, a=0.01, b=0.03):
    y = y.copy(); na, nb = int(a * SR), int(b * SR)
    y[:na] *= np.linspace(0, 1, na); y[len(y) - nb:] *= np.linspace(1, 0, nb); return y
med = pyln.Meter(SR)
voz4 = sf.read(AQ / "voz_es.wav")[0]
if voz4.ndim > 1: voz4 = voz4.mean(1)
nov = sf.read(AQ / "no_vocals.wav")[0]                  # estéreo, timeline original (= v4 antes de 125,97 s)
mixg = sf.read(AQ / "v4" / "mix_v4.wav")[0]               # áudio final do v4 (gancho com grito novo + igreja)
NA = int(round(NOUT / FPS * SR))
voz = np.zeros(NA); mus = np.zeros((NA, 2))
L_C = med.integrated_loudness(voz4[int(8.05 * SR): int(16.93 * SR)]); L_R = med.integrated_loudness(voz4[int(22.0 * SR): int(44.0 * SR)])
def sa(jq): return int(round(jq / FPS * SR))
# trilha: contínua a partir de 8,033 s; S6 com a trilha do próprio trecho (transição em chicote); depois segue do fim do S6
cur = J_SELFIE / FPS; blocos_mus = []
for s in tl[1:]:
    src = s["a"] / FPS if s["id"] == "S6" else cur
    if blocos_mus and abs(blocos_mus[-1][2] + blocos_mus[-1][1] / FPS - src) < 1e-6:
        blocos_mus[-1][1] += s["n"]                       # mesma fonte contínua: junta
    else:
        blocos_mus.append([s["j0"], s["n"], src])
    cur = src + s["n"] / FPS
XF = int(0.25 * SR)
for k, (j0, n, src) in enumerate(blocos_mus):
    a = sa(j0); b = sa(j0 + n); i0 = int(round(src * SR))
    pre = XF if k else 0; pos = XF if k < len(blocos_mus) - 1 else 0
    seg = nov[i0 - pre: i0 + (b - a) + pos].copy(); st = a - pre
    w = np.ones(len(seg))
    if pre: w[:2 * pre] = np.sin(np.linspace(0, np.pi / 2, 2 * pre)) ** 2
    if pos: w[-2 * pos:] = np.minimum(w[-2 * pos:], np.cos(np.linspace(0, np.pi / 2, 2 * pos)) ** 2)
    else: e = int(0.6 * SR); w[-e:] = np.minimum(w[-e:], np.linspace(1, 0, e))
    seg = seg * w[:, None]; e2 = min(NA, st + len(seg)); mus[st:e2] += seg[: e2 - st]
print("trilha:", [(round(j0 / FPS, 2), round(n / FPS, 2), round(src, 2)) for j0, n, src in blocos_mus])
# voz
for s in tl[1:]:
    a = sa(s["j0"]); n = sa(s["j0"] + s["n"]) - a
    if s["tipo"] == "v4":
        i0 = int(round(s["a"] / FPS * SR)); y = fade(voz4[i0: i0 + n], 0.01, 0.03)
    else:
        L = LINHAS[s["a"]]; y = ld(T / "tts" / f"{L['tts']}.mp3")
        alvo = L_C if s["a"] == "chora" else L_R
        y = y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)
        y = np.concatenate([np.zeros(int(L["lead"] * SR)), fade(y, 0.005, 0.03)])[:n]
    voz[a: a + len(y)] += y
mix = mus + voz[:, None]
sf.write(T / "_mix_bruto.wav", mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T / "_mix_bruto.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled",
                "-c:a", "pcm_f32le", str(T / "_mix_lim.wav")], check=True)
mix = sf.read(T / "_mix_lim.wav")[0][:NA]
ag = sa(J_SELFIE); mix[:ag] = mixg[:ag]
c = int(0.02 * SR); w = np.linspace(0, 1, c)[:, None]; mix[ag:ag + c] = mixg[ag:ag + c] * (1 - w) + mix[ag:ag + c] * w
sf.write(T / "audio_v0.wav", mix, SR, subtype="PCM_16"); sf.write(T / "audio_corpo.wav", mix[ag:], SR, subtype="PCM_16")
LUFS_V0 = med.integrated_loudness(mix); LUFS_C = med.integrated_loudness(mix[ag:])
print("LUFS V0", round(LUFS_V0, 1), "| corpo", round(LUFS_C, 1), "| voz alvo chora", round(L_C, 1), "roxo", round(L_R, 1))
if "--so-audio" in sys.argv: sys.exit()
# ---------------- quadros ----------------
import cv2
OLD = {}
for nome in ["L01", "L07", "L10", "L12", "L13"]: OLD.update(pickle.load(open(AQ / "lipsync/patch" / f"{nome}.pkl", "rb")))
NEW = {n: pickle.load(open(T / "ls" / "patch" / f"{n}.pkl", "rb")) for n in ["jm1", "jm2", "jm3a", "jm3b"]}
AV_C = cor.ler(AVC); AV_G = cor.ler(AQ / "v3/sd1.mp4")
CHORA = cor.ler(T / "ls" / "patch" / "chora_prev.mp4")
def ler_m(p, matriz):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"scale=720:1280:in_color_matrix={matriz}:in_range=limited:flags=accurate_rnd+full_chroma_int+bitexact,format=rgb24",
                        "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(r, np.uint8).reshape(-1, 1280, 720, 3)
def cola(f, cam):
    x, y, L = cam; hh, ww = L.shape[:2]; al = L[..., 3:4].astype(np.float32) / 255
    f = f.copy(); f[y:y + hh, x:x + ww] = np.clip(L[..., :3] * al + f[y:y + hh, x:x + ww] * (1 - al) + 0.5, 0, 255).astype(np.uint8); return f
def avatar(i, f):
    if 123 <= i <= 230:
        k = min(len(AV_G) - 1, int(round(0.45 * 24 + (i - 123) * 24 / 30))); g = cv2.resize(AV_G[k], (720, 960), interpolation=cv2.INTER_AREA)[24:936]
        f = f.copy(); f[248:1160] = g; return f
    if 239 <= i <= 658: return AV_C[min(len(AV_C) - 1, int((i - 239) * 25 / 30))]
    return f
SOLTO = {2622, 2623, 2624}
VF_OUT = "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int+bitexact,format=yuv420p"
TAG = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
def enc(p): return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "30", "-i", "-",
                                     "-vf", VF_OUT, "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-profile:v", "high", *TAG, str(p)], stdin=subprocess.PIPE)
E0, E1 = enc(T / "_v0_video.mp4"), enc(T / "_corpo_video.mp4")
log = {"borrao": 0}
def compor(f, j, i_base):
    t = j / FPS; im = Image.fromarray(f).convert("RGBA")
    if j < 239: im.alpha_composite(TIT)
    lg = LEG_G.em(t) if j < J_SELFIE else LEG.em(t)
    if lg is not None: im.alpha_composite(lg)
    elif i_base is not None and j >= J_SELFIE and i_base >= 667:
        d = DM[i_base] if i_base < len(DM) else None
        cx = legenda2.GEO[geo_i(i_base)][1]
        if d is not None and d[4] >= 500 and d[1] < cx[3] and d[3] > cx[1]:
            ImageDraw.Draw(im).rounded_rectangle(cx, legenda2.RAIO, fill=legenda2.CAIXA_COR); log["borrao"] += 1
    if t >= T_VIVO: im.alpha_composite(VIVO, (360 - VIVO.width // 2, 128))
    if t >= T_CTA:
        im.alpha_composite(TOCA, (360 - TOCA.width // 2, 912))
        dy = int(round(13 * np.sin(2 * np.pi * 1.6 * (t - T_CTA))))
        for x in (200, 407): im.alpha_composite(SETA, (x, 1012 + dy))
    im.alpha_composite(SELO)
    o = np.asarray(im.convert("RGB")); E0.stdin.write(o.tobytes())
    if j >= J_SELFIE: E1.stdin.write(o.tobytes())
g230 = None
for s in tl:
    print(f"[{s['j0']}/{NOUT}] {s['id']} {100 * s['j0'] // NOUT}%", flush=True)
    if s["tipo"] == "v4":
        F = cor.ler(BASE, s["a"], s["b"]); hold = None
        for k, i in enumerate(range(s["a"], s["b"] + 1)):
            f = F[k]
            if i == 2621: hold = f.copy()
            if i in SOLTO and hold is not None: f = hold
            elif 123 <= i <= 230 or 239 <= i <= 658:
                f = avatar(i, f)
                if i == 230: g230 = f.copy(); g230[:248] = 0
            elif 231 <= i <= 238:
                w = (i - 230) / 9; f = np.clip(g230 * (1 - w) + AV_C[0] * w + 0.5, 0, 255).astype(np.uint8)
            elif i in OLD: f = cola(f, OLD[i])
            if i >= 659: f = arroba.aplica(f)
            compor(f, s["j0"] + k, i if i >= 659 else None)
        del F
    else:
        partes = PARTES[s["a"]]; cache = {}
        for k in range(s["n"]):
            u = k / FPS
            p = next((p for p in partes if p[0] <= u < p[1]), partes[-1]); a, b, tipo, ref, tref = p
            tt = tref + (u - a); ib = None
            if tipo == "broll":
                if ref not in cache: cache[ref] = ler_m(BR / ref, "bt601" if "sagrado_34" in ref else "bt709")
                fr = cache[ref]; f = fr[min(len(fr) - 1, int(round(tt * 30)))]
            elif ref == "chora":
                f = CHORA[min(len(CHORA) - 1, int(tt * 25))]
            else:
                P = NEW[ref]; q0, q1 = JOBS[ref]["src"][1:]; kk = min(int(round(tt * 30)), q1 - q0)
                if ref not in cache: cache[ref] = cor.ler(BASE, q0, q1)
                f = cache[ref][kk]
                if kk in P["camadas"]: f = cola(f, P["camadas"][kk])
                f = arroba.aplica(f); ib = q0 + kk
            compor(f, s["j0"] + k, ib)
        cache.clear()
for e in (E0, E1): e.stdin.close(); e.wait()
def mux(v, a, o):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-i", str(a), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", str(o)], check=True)
mux(T / "_v0_video.mp4", T / "audio_v0.wav", C / "V0_COMPLETA.mp4")
mux(T / "_corpo_video.mp4", T / "audio_corpo.wav", C / "corpo_a_partir_selfie.mp4")
info = {"corpo_a_partir_selfie.mp4": {"duracao_s": round((NOUT - J_SELFIE) / FPS, 3), "quadros": NOUT - J_SELFIE, "selfie_1o_quadro_s": 0.0,
          "lufs_integrado": round(LUFS_C, 1), "fps": 30, "resolucao": "720x1280", "audio": "AAC 48 kHz estéreo",
          "nota": "1º quadro = selfie do padre chorando (quadro 241 do v4). A fala «Es indignante…» começa em ~0,02 s e a trilha de tensão já entra tocando: na colagem, corte seco no vídeo e crossfade de ~0,15 s só no áudio."},
        "V0_COMPLETA.mp4": {"duracao_s": round(NOUT / FPS, 3), "quadros": NOUT, "selfie_1o_quadro_s": round(J_SELFIE / FPS, 3), "lufs_integrado": round(LUFS_V0, 1)},
        "cta_setas_s_no_corpo": round(T_CTA - J_SELFIE / FPS, 2), "en_vivo_s_no_corpo": round(T_VIVO - J_SELFIE / FPS, 2),
        "segmentos": [{k: s[k] for k in ("id", "tipo", "a", "b")} | {"ini_V0": round(s["j0"] / FPS, 3), "fim_V0": round((s["j0"] + s["n"]) / FPS, 3)} for s in tl],
        "log": log}
json.dump(info, open(C / "corpo_info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", log)
