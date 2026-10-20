"""Mixa instrumental de música trend sob a voz do AD-C.
uso: python mixar.py <nome> <instrumental.wav> <inicio_aprox_s> [--alvo-musica -24] [--sem-alinhar]
Alinha um onset forte (batida) do instrumental com t=1.5 s (fim do título).
"""
import sys, subprocess, json, re, argparse
import numpy as np, librosa

BASE = r"C:\Users\PICHAU\Downloads\YARA-CL\entregas\AD-C_yara-kit3_bf_es-cl.mp4"
OUTDIR = r"C:\Users\PICHAU\Downloads\YARA-CL\entregas"
DUR = 48.133333
T_TIT, T_CTA = 1.5, DUR - 1.8

def lufs(args_in, filt):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args_in, "-filter_complex", filt + ",ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    pk = re.findall(r"Peak:\s+(-?[\d.inf]+) dBFS", r.stderr)
    return I, (float(pk[-1]) if pk and pk[-1] != "-inf" else None)

ap = argparse.ArgumentParser()
ap.add_argument("nome"); ap.add_argument("inst"); ap.add_argument("ini", type=float)
ap.add_argument("--alvo-musica", type=float, default=-24.0)
ap.add_argument("--sem-alinhar", action="store_true")
a = ap.parse_args()

# 1) achar onset forte perto de ini+1.5 e ajustar o início para cair em 1.5 s
ini = a.ini
if not a.sem_alinhar:
    y, sr = librosa.load(a.inst, sr=22050, mono=True, offset=max(0, ini - 1.0), duration=6.0)
    env = librosa.onset.onset_strength(y=y, sr=sr)
    t = librosa.times_like(env, sr=sr) + max(0, ini - 1.0)
    alvo = ini + T_TIT
    m = (t > alvo - 1.0) & (t < alvo + 1.0)
    # pondera força por proximidade
    score = env[m] * np.exp(-((t[m] - alvo) ** 2) / (2 * 0.5 ** 2))
    tk = t[m][int(np.argmax(score))]
    ini = tk - T_TIT
    print(f"onset forte em {tk:.3f}s da música -> início {ini:.3f}s")

seg = f"-ss {ini:.3f} -t {DUR + 0.3:.3f}".split()
# 2) nível da música crua (sem ducking)
I_m, _ = lufs([*seg, "-i", a.inst], "[0:a]anull")
# sidechain: voz da base
vol_env = f"volume='if(lt(t,{T_TIT}),1.5,if(gt(t,{T_CTA:.3f}),1.5,1))':eval=frame"

def grafo(g_db, final_gain_db=0.0, limiter=True):
    return (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={g_db:.2f}dB,{vol_env}[m0];"
            f"[0:a]asplit=2[v][sc];"
            f"[m0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350:makeup=1[md];"
            f"[md]afade=t=in:st=0:d=0.05,afade=t=out:st={DUR - 0.8:.3f}:d=0.8[mf];"
            f"[v][mf]amix=inputs=2:normalize=0:duration=first,volume={final_gain_db:.2f}dB"
            + (",alimiter=limit=0.85:level=false" if limiter else "")
            + f",apad,atrim=0:{DUR:.6f}[out]")

# 3) ganho para música crua ~ alvo+4 (o ducking tira ~4-6 dB sob a voz)
g = (a.alvo_musica + 4) - I_m
# mede música após ducking (sem voz no mix) iterando 1x
def music_only(gdb):
    f = (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={gdb:.2f}dB,{vol_env}[m0];"
         f"[0:a]asplit=2[v][sc];[m0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350:makeup=1[md];"
         f"[v]anullsink;[md]atrim=0:{DUR:.3f}")
    return lufs(["-i", BASE, *seg, "-i", a.inst], f)[0]
Im1 = music_only(g); g += a.alvo_musica - Im1; Im2 = music_only(g)
print(f"música crua {I_m:.1f} LUFS; sob a voz após ducking {Im2:.1f} LUFS (ganho {g:+.1f} dB)")

# 4) loudness final -14.5
Imix, _ = lufs(["-i", BASE, *seg, "-i", a.inst], grafo(g, 0, False).replace("[out]", ""))
fg = -14.5 - Imix
out = f"{OUTDIR}\\AD-C_yara-kit3_bf_es-cl_trend-{a.nome}.mp4"
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", BASE, *seg, "-i", a.inst,
       "-filter_complex", grafo(g, fg), "-map", "0:v", "-map", "[out]", "-c:v", "copy",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
If, pk = lufs(["-i", out], "[0:a]anull")
print(f"saida {out}\n  final {If:.1f} LUFS, pico {pk} dBFS")
json.dump({"nome": a.nome, "inst": a.inst, "inicio_s": round(ini, 3), "ganho_musica_db": round(g, 2),
           "musica_sob_voz_lufs": round(Im2, 1), "final_lufs": If, "pico_dbfs": pk},
          open(rf"C:\Users\PICHAU\Downloads\YARA-CL\producao\musica_trend\mix_{a.nome}.json", "w"), indent=1)
