# -*- coding: utf-8 -*-
"""Monta a trilha ES: falas TTS posicionadas + no_vocals original (com S s inseridos na cena do produto).
Saídas: voz_es.wav (só voz, timeline final), mix_es.wav, palavras_es.json (timeline final), plano_audio.json"""
import json, subprocess, numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from pathlib import Path
AQ = Path(__file__).resolve().parent
SR = 44100
A = 3779 / 30          # 125.9667: início da cena do print (vira produto) -> recebe a inserção
S = 120 / 30           # 4,0 s inseridos
R = {r["id"]: r for r in json.load(open(AQ / "roteiro.json", encoding="utf-8"))}
# id: (início na timeline FINAL, fator de velocidade)
PLANO = {"01": (0.05, 1.05), "02": (4.40, 1.0), "03": (8.05, 1.0), "04": (14.65, 1.0), "05": (16.92, 1.0),
         "06": (22.00, 1.0), "07": (32.80, 1.03), "08": (44.20, 1.0),
         "11": (61.22, 1.0), "12": (67.62, 1.0), "13": (73.86, 1.0), "14": (81.90, 1.0), "15": (87.42, 1.0),
         "16": (90.06, 1.0), "17": (95.80, 1.1), "18": (105.30, 1.0), "19": (112.00, 1.0),
         "20": (120.30, 1.08), "21": (131.60, 1.0),
         "22": (133.30 + S, 1.0), "23": (136.90 + S, 1.0), "24": (141.90 + S, 1.04), "25": (145.00 + S, 1.0), "26": (150.72 + S, 1.0)}
PT12 = [48.36, 49.04, 50.24, 50.76, 51.76, 52.46, 53.54, 54.40, 55.52, 56.50, 58.00, 59.34, 60.30]  # Crux..Ignis, Veritas..Triunfos
def ali(i):
    a = json.load(open(AQ / f"tts/{i}.alinhamento.json", encoding="utf-8"))
    ws, cur, t0 = [], "", None
    for c, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if c == " ":
            if cur: ws.append([cur, t0, pe])
            cur, t0 = "", None
        else:
            if t0 is None: t0 = s
            cur += c; pe = e
    if cur: ws.append([cur, t0, pe])
    return ws
def carrega(i):
    y, _ = librosa.load(AQ / f"tts/{i}.mp3", sr=SR, mono=True); return y
def estica(y, f):
    if abs(f - 1) < 1e-3: return y
    t = AQ / "_tmp/_st_in.wav"; o = AQ / "_tmp/_st_out.wav"; sf.write(t, y, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(t), "-af", f"atempo={f}", str(o)], check=True)
    return sf.read(o)[0]
def fade(y, a=0.01, b=0.03):
    y = y.copy(); na, nb = int(a * SR), int(b * SR)
    y[:na] *= np.linspace(0, 1, na); y[-nb:] *= np.linspace(1, 0, nb); return y
voc_o, _ = librosa.load(AQ / "vocals.wav", sr=SR, mono=True)
nov, _ = librosa.load(AQ / "no_vocals.wav", sr=SR, mono=False)
mix_o, _ = librosa.load(AQ / "audio_orig.wav", sr=SR, mono=False)
med = pyln.Meter(SR)
DUR = mix_o.shape[1] / SR + S
voz = np.zeros(int(DUR * SR) + SR)
pal, plano = [], []
def orig_t(t):  # timeline final -> original (para medir a fala original da mesma janela)
    return t if t < A else max(A, t - S)
def coloca(y, t, ws, rid, f, o0, o1):
    lo = med.integrated_loudness(voc_o[int(o0 * SR): int(o1 * SR)]) if o1 - o0 > 0.5 else None
    li = med.integrated_loudness(y) if len(y) > 0.45 * SR else None
    if lo is not None and li is not None and np.isfinite(lo) and np.isfinite(li): y = y * 10 ** ((lo - li) / 20)
    n = int(round(t * SR)); voz[n: n + len(y)] += y
    for w, a, b in ws: pal.append({"w": w, "ini": round(t + a / f, 3), "fim": round(t + b / f, 3), "id": rid})
    plano.append({"id": rid, "ini": round(t, 3), "fim": round(t + len(y) / SR, 3), "vel": f, "lufs_orig": None if lo is None else round(lo, 1)})
for i, (t, f) in PLANO.items():
    ws = ali(i); y = carrega(i)
    s0 = max(0, ws[0][1] - 0.03); s1 = ws[-1][2] + 0.08
    y = fade(y[int(s0 * SR): int(s1 * SR)])
    ws = [[w, a - s0, b - s0] for w, a, b in ws]
    y = estica(y, f)
    r = R[i]; o0 = r["ini"]; o1 = r["fim"]
    coloca(y, t, ws, i, f, o0, o1)
# 12 palavras: cada palavra ES no início da palavra PT correspondente
w9, w10 = ali("09"), ali("10"); y9, y10 = carrega("09"), carrega("10")
itens = [(w, a, b, y9) for w, a, b in w9] + [(w, a, b, y10) for w, a, b in w10]
# "Spiritus y Triumphus": 'y' vai junto de Spiritus
grupos = []
for w, a, b, y in itens:
    if w == "y": grupos[-1][2] = b; grupos[-1][4].append((w, a, b)); continue
    grupos.append([w, a, b, y, [(w, a, b)]])
pt = [48.36, 49.04, 50.24, 50.76, 51.76, 52.46, 53.54, 54.40, 55.52, 56.50, 58.00, 60.30]
lo12 = med.integrated_loudness(voc_o[int(48.3 * SR): int(61.1 * SR)])
seg = []
for (w, a, b, y, sub), t in zip(grupos, pt):
    c = fade(y[int(max(0, a - 0.02) * SR): int((b + 0.06) * SR)], 0.005, 0.03)
    seg.append((t, c, [[x, xa - max(0, a - 0.02), xb - max(0, a - 0.02)] for x, xa, xb in sub]))
cat = np.concatenate([c for _, c, _ in seg]); g = 10 ** ((lo12 - med.integrated_loudness(cat)) / 20)
for t, c, sub in seg:
    n = int(t * SR); voz[n: n + len(c)] += c * g
    for x, xa, xb in sub: pal.append({"w": x, "ini": round(t + xa, 3), "fim": round(t + xb, 3), "id": "12p"})
plano.append({"id": "09-10", "ini": 48.36, "fim": 61.1, "vel": 1.0, "obs": "palavra a palavra no tempo das PT"})
pal.sort(key=lambda d: d["ini"])
# trocas de legenda (números por extenso -> algarismos)
for r in R.values():
    for de, para in r.get("leg", []):
        toks = de.split(); i = 0
        while i < len(pal):
            if pal[i]["id"] == r["id"] and [p["w"].strip(",.") for p in pal[i:i + len(toks)]] == toks:
                fim = pal[i + len(toks) - 1]; pont = fim["w"][len(toks[-1]):] if fim["w"].startswith(toks[-1]) else ""
                pal[i: i + len(toks)] = [{"w": para + pont, "ini": pal[i]["ini"], "fim": fim["fim"], "id": r["id"]}]
            i += 1
voz = voz[: int(DUR * SR)]
# música: no_vocals com S s inseridos em A (repete A..A+S, costuras 60 ms)
iA, nS = int(round(A * SR)), int(round(S * SR)); c = int(0.06 * SR); w = np.sin(np.linspace(0, np.pi / 2, c)) ** 2
ins = nov[:, iA: iA + nS + c].copy()
mus = np.concatenate([nov[:, :iA], ins[:, :nS], nov[:, iA:]], axis=1)
mus[:, iA + nS: iA + nS + c] = ins[:, nS: nS + c] * (1 - w) + nov[:, iA: iA + c] * w
mus = mus[:, : len(voz)]
if mus.shape[1] < len(voz): mus = np.pad(mus, ((0, 0), (0, len(voz) - mus.shape[1])))
sf.write(AQ / "_tmp/voz_bruta.wav", voz, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQ / "_tmp/voz_bruta.wav"), "-af", "volume=0.7dB,alimiter=limit=0.80:attack=3:release=60:level=disabled",
                "-c:a", "pcm_f32le", str(AQ / "voz_es.wav")], check=True)
voz = sf.read(AQ / "voz_es.wav")[0][: len(voz)]
mix = mus + voz[None, :]
sf.write(AQ / "_tmp/mix_bruto.wav", mix.T, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQ / "_tmp/mix_bruto.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled",
                "-c:a", "pcm_s16le", str(AQ / "mix_es.wav")], check=True)
mix = sf.read(AQ / "mix_es.wav")[0].T
json.dump(pal, open(AQ / "palavras_es.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump({"A": A, "S": S, "dur": DUR, "linhas": plano}, open(AQ / "plano_audio.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("LUFS mix orig", round(med.integrated_loudness(mix_o.T), 2), "| mix ES", round(med.integrated_loudness(mix.T), 2),
      "| voz orig", round(med.integrated_loudness(voc_o), 2), "| voz ES", round(med.integrated_loudness(voz), 2), "| pico", round(float(np.abs(mix).max()), 3))
# checa sobreposição de falas
pl = sorted(plano, key=lambda d: d["ini"])
for a, b in zip(pl, pl[1:]):
    if b["ini"] < a["fim"] - 0.02: print("SOBREPOE", a["id"], a["fim"], b["id"], b["ini"])
