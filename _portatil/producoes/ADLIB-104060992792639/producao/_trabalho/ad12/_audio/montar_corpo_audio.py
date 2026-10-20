# audio do corpo = narracao_es.wav + fundo (no_vocals do demucs, nivel original), cortado em DUR com fade de 0,3 s.
# Uso: python _audio/montar_corpo_audio.py AD_DIR fundo.wav [fundo_gancho.wav ate_s]
import sys, json, numpy as np, soundfile as sf, subprocess, tempfile, os
AD = sys.argv[1]; FUNDO = sys.argv[2]
DUR = json.load(open(os.path.join(AD, "tempos_reais.json")))["dur"]; SR = 48000; tmp = tempfile.mkdtemp()
def rd(p, ch):
    o = os.path.join(tmp, "x.wav"); subprocess.run(["ffmpeg","-v","error","-y","-i",p,"-ar",str(SR),"-ac",str(ch),o],check=True); return sf.read(o)[0]
n = rd(os.path.join(AD, "narracao_es.wav"), 1); f = rd(FUNDO, 2)
if len(sys.argv) > 3:
    g = rd(sys.argv[3], 2); ate = float(sys.argv[4]); k = int(ate * SR); x = int(0.15 * SR)
    w = np.ones(len(f)); w[:k - x] = 0; w[k - x:k + x] = np.linspace(0, 1, 2 * x)
    g = np.concatenate([g, np.zeros((max(0, len(f) - len(g)), 2))])[:len(f)]
    f = f * w[:, None] + g * (1 - w[:, None])
m = int(round(DUR * SR)); n = np.concatenate([n, np.zeros(m)])[:m]; f = np.concatenate([f, np.zeros((m, 2))])[:m]
o = n[:, None] + f; k = int(0.3 * SR); o[-k:] *= np.linspace(1, 0, k)[:, None]
sf.write(os.path.join(AD, "audio_corpo.wav"), np.clip(o, -1, 1), SR, subtype="PCM_16"); print("ok", len(o) / SR)
