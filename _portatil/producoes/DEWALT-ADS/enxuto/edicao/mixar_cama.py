"""COPIA DEWALT-ADS (10/10/2026): --base/--saida obrigatorios, --cta (duracao do cartao), arquivos de trabalho em edicao/_mix/.
Remix das versões com música do AD-C com a música como "cama" (bem mais baixa).
uso: python mixar_cama.py <versao> [--alvo-fala -32] [--alvo-borda -24] [--duck 11] [--base v.mp4 --saida o.mp4 --tit 1.5 --tag H2]
versoes: A B C (leitos de producao/musica) | bbywow bambam superestrella (instrumentais demucs)

Ducking por envelope calculado da voz (VAD por frase), ataque 20 ms, release 250 ms.
Música sob a fala no corpo ~ -32 LUFS; título (0-1,5 s) e cartão final (últimos 1,8 s) até ~-24 LUFS.
Mix final -14,5 LUFS, pico <= -1 dBTP, vídeo -c:v copy.
"""
import argparse, json, re, subprocess, sys
import numpy as np, pyloudnorm as pyln
from scipy.signal import resample_poly

Y = r"C:\Users\PICHAU\Downloads\YARA-CL"
BASE = rf"{Y}\entregas\AD-C_yara-kit3_bf_es-cl.mp4"
SR = 48000
T_TIT, CTA = 1.5, 1.8

ap = argparse.ArgumentParser()
ap.add_argument("versao")
ap.add_argument("--alvo-fala", type=float, default=-32.0)
ap.add_argument("--alvo-borda", type=float, default=-24.0)
ap.add_argument("--duck", type=float, default=11.0)
ap.add_argument("--base", help="video sem musica (padrao: AD-C)")
ap.add_argument("--saida", help="mp4 de saida (padrao: entregas/AD-C_..._<versao>.mp4)")
ap.add_argument("--tit", type=float, default=T_TIT, help="duracao do titulo de abertura (s)")
ap.add_argument("--tag", default="", help="sufixo dos arquivos de trabalho (_mix_/_stem_/mix_*.json)")
ap.add_argument("--cta", type=float, default=CTA, help="duracao do cartao final (s)")
a = ap.parse_args()
v = a.versao
if a.base: BASE = a.base
T_TIT = a.tit
CTA = a.cta
import os
MIXD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_mix"); os.makedirs(MIXD, exist_ok=True)
TAG = v + (f"_{a.tag}" if a.tag else "")

def dec(path, ss=0.0, t=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", path]
    if t: cmd += ["-t", f"{t:.3f}"]
    cmd += ["-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)

DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                                     "stream=duration", "-of", "csv=p=0", BASE]).decode())
N = int(round(DUR * SR))
voz = dec(BASE)
voz = np.pad(voz, ((0, max(0, N - len(voz))), (0, 0)))[:N]

if v in ("A", "B", "C"):
    src, ini = rf"{Y}\producao\musica\_leito_{v}.wav", 0.0
    out = rf"{Y}\entregas\AD-C_yara-kit3_bf_es-cl_musica-{v}.mp4"
else:
    cfg = json.load(open(rf"{Y}\producao\musica_trend\mix_{v}.json"))
    src, ini = rf"{Y}\producao\musica_trend\sep\htdemucs\{v}\no_vocals.wav", cfg["inicio_s"]
    out = rf"{Y}\entregas\AD-C_yara-kit3_bf_es-cl_trend-{v}.mp4"
if a.saida: out = a.saida
mus = dec(src, ini, DUR + 0.3)
mus = np.pad(mus, ((0, max(0, N - len(mus))), (0, 0)))[:N]

# --- VAD por frase (quadros de 10 ms) ---
H = SR // 100
nf = N // H
rms = np.sqrt((voz[:nf * H].mean(1).reshape(nf, H) ** 2).mean(1) + 1e-12)
db = 20 * np.log10(rms)
fala = db > max(-45.0, np.percentile(db, 95) - 30)
# fecha lacunas curtas (< 300 ms) entre sílabas/palavras -> frase
k = 30
idx = np.where(fala)[0]
for i0, i1 in zip(idx[:-1], idx[1:]):
    if 1 < i1 - i0 <= k: fala[i0:i1] = True
# remove ruídos isolados < 60 ms
lab = np.diff(np.r_[0, fala.astype(int), 0]); st, en = np.where(lab == 1)[0], np.where(lab == -1)[0]
for s, e in zip(st, en):
    if e - s < 6: fala[s:e] = False

# --- envelope de ducking (dB) com ataque 20 ms / release 250 ms ---
alvo = np.where(fala, -a.duck, 0.0)
alvo_s = np.repeat(alvo, H); alvo_s = np.pad(alvo_s, (0, N - len(alvo_s)), mode="edge")
ca, cr = np.exp(-1 / (0.020 * SR)), np.exp(-1 / (0.250 * SR))
env = np.empty(N); g = 0.0
# lookahead de 10 ms para o ataque não deixar escapar o início da sílaba
la = int(0.010 * SR); alvo_la = np.r_[alvo_s[la:], np.full(la, alvo_s[-1])]
for i in range(N):
    x = alvo_la[i]; c = ca if x < g else cr
    g = c * g + (1 - c) * x; env[i] = g
duck = 10 ** (env / 20)

t = np.arange(N) / SR
fala_s = np.repeat(fala, H); fala_s = np.pad(fala_s, (0, N - len(fala_s)), mode="edge")
corpo = (t >= T_TIT) & (t < DUR - CTA)
m_fala = fala_s & corpo
borda_tit = t < T_TIT
borda_cta = t >= DUR - CTA

meter = pyln.Meter(SR)
def L(x, m=None):
    x = x if m is None else x[m]
    return meter.integrated_loudness(x) if len(x) > SR // 2 else float("nan")

# fade in 50 ms / out 0,8 s na música
fade = np.ones(N); nfi = int(0.05 * SR); fade[:nfi] = np.linspace(0, 1, nfi)
nfo = int(0.8 * SR); fade[-nfo:] = np.minimum(fade[-nfo:], np.linspace(1, 0, nfo))

def montar_musica(G, lt, lc):
    lift = np.zeros(N)
    lift[borda_tit] = lt; lift[borda_cta] = lc
    # rampa de 0,3 s na saída do título e na entrada do cartão
    r = int(0.3 * SR); i = int(T_TIT * SR)
    lift[i:i + r] = np.linspace(lt, 0, r)
    j = int((DUR - CTA) * SR)
    lift[j - r:j] = np.linspace(0, lc, r)
    return mus * (10 ** ((G + lift) / 20) * duck * fade)[:, None]

G = a.alvo_fala - L(mus * duck[:, None], m_fala)
lt = lc = 0.0
for _ in range(3):
    mm = montar_musica(G, lt, lc)
    G += a.alvo_fala - L(mm, m_fala)
    mm = montar_musica(G, lt, lc)
    lt = min(12.0, max(0.0, lt + a.alvo_borda - L(mm, borda_tit)))
    lc = min(12.0, max(0.0, lc + a.alvo_borda - L(mm, borda_cta)))
mm = montar_musica(G, lt, lc)

med = {
    "musica_fala_corpo_lufs": L(mm, m_fala),
    "voz_fala_corpo_lufs": L(voz, m_fala),
    "musica_titulo_lufs": L(mm, borda_tit),
    "musica_cartao_lufs": L(mm, borda_cta),
    "musica_pausas_corpo_lufs": L(mm, corpo & ~fala_s),
    "pausas_corpo_s": float((corpo & ~fala_s).sum() / SR),
}
med["razao_voz_musica_lu"] = med["voz_fala_corpo_lufs"] - med["musica_fala_corpo_lufs"]
# razão por frase (pior caso)
lab = np.diff(np.r_[0, m_fala.astype(np.int8), 0]); st, en = np.where(lab == 1)[0], np.where(lab == -1)[0]
rz = [L(voz[s:e]) - L(mm[s:e]) for s, e in zip(st, en) if e - s > SR // 2]
med["razao_min_por_frase_lu"] = float(np.nanmin(rz)) if rz else None

mix = voz + mm
# --- loudness final -14,5 e true peak <= -1 dBTP (limitador simples com lookahead sobre sinal 4x) ---
mix *= 10 ** ((-14.5 - L(mix)) / 20)
def tp(x): return 20 * np.log10(np.abs(resample_poly(x, 4, 1, axis=0)).max() + 1e-12)
teto = 10 ** (-1.6 / 20)
for _ in range(4):
    if tp(mix) <= -1.5: break
    up = np.abs(resample_poly(mix, 4, 1, axis=0)).max(1).reshape(-1, 4).max(1)[:N]
    need = np.minimum(1.0, teto / np.maximum(up, 1e-9))
    w = int(0.005 * SR)  # 5 ms: mínimo deslizante + suavização (release ~ 60 ms)
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    gr = uniform_filter1d(minimum_filter1d(need, 2 * w + 1), 2 * w + 1)
    mix *= gr[:, None]
    mix *= 10 ** ((-14.5 - L(mix)) / 20)
med["pre_aac_lufs"], med["pre_aac_tp"] = L(mix), tp(mix)

wav = os.path.join(MIXD, f"_mix_{TAG}.wav")
import soundfile as sf
sf.write(wav, mix.astype(np.float32), SR, subtype="FLOAT")
sf.write(os.path.join(MIXD, f"_stem_{TAG}.wav"), mm.astype(np.float32), SR, subtype="FLOAT")

def gravar(gain_db):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", BASE, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", f"volume={gain_db:.2f}dB", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-t", f"{DUR:.6f}", "-movflags", "+faststart", out], check=True)
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out, "-map", "0:a", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True, errors="ignore").stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1])
    P = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
    return I, P
gdb = 0.0
I, P = gravar(gdb)
if P > -1.0:
    gdb = -1.05 - P; I, P = gravar(gdb)
med["final_lufs"], med["final_tp_dbtp"] = I, P
med.update({"versao": v, "fonte": src, "inicio_s": ini, "ganho_musica_db": G, "lift_titulo_db": lt,
            "lift_cartao_db": lc, "duck_db": a.duck, "ataque_ms": 20, "release_ms": 250, "saida": out})
json.dump({k: (round(x, 2) if isinstance(x, float) else x) for k, x in med.items()},
          open(os.path.join(MIXD, f"mix_{TAG}.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: (round(x, 1) if isinstance(x, float) else x) for k, x in med.items()}, ensure_ascii=False))
