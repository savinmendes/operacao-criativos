import numpy as np, librosa, json
from faster_whisper import WhisperModel
def env(p):
    y, sr = librosa.load(p, sr=16000); return librosa.feature.rms(y=y, frame_length=400, hop_length=160)[0]
o = env("gancho.wav")
fd, _ = librosa.load("_teste/sts_gancho_demucs_fundo.wav", sr=16000)
print("fundo demucs rms dBFS: %.1f" % (20*np.log10(np.sqrt(np.mean(fd**2))+1e-9)))
yo,_=librosa.load("gancho.wav",sr=16000); print("gancho rms dBFS: %.1f" % (20*np.log10(np.sqrt(np.mean(yo**2)))))
for n in ["_teste/sts_gancho.wav", "_teste/sts_gancho_demucs.wav"]:
    s = env(n); m = min(len(o), len(s))
    a = (o[:m] > o.max()*0.05).astype(float); b = (s[:m] > s.max()*0.05).astype(float)
    xc = [np.mean(a[max(0,k):m+min(0,k)] == b[max(0,-k):m-max(0,k)]) for k in range(-20, 21)]
    lag = np.argmax(xc) - 20
    print(n, "lag=%+d ms" % (lag*10), "concordância fala/silêncio=%.2f" % max(xc))
w = WhisperModel("medium", device="cpu", compute_type="int8")
res = {}
for n in ["_teste/sts_gancho.wav", "_teste/sts_gancho_demucs.wav", "T3_yara.mp3", "T4_yara_close.mp3", "T5_moi.mp3",
          "T7_elixir.mp3", "T10_cta.mp3", "N_yara.mp3", "N_moi.mp3", "N_elixir.mp3"]:
    segs, info = w.transcribe(n, language="es", word_timestamps=True)
    segs = list(segs); txt = " ".join(s.text.strip() for s in segs)
    print(f"{n}: {txt}")
    if "sts" in n:
        print("   palavras:", [(x.word.strip(), round(x.start,2)) for s in segs for x in s.words][:8])
