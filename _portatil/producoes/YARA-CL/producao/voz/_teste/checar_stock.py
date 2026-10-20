import numpy as np, librosa
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
for p in ["Liquidación de stock por Black Friday.", "Liquidação de estoque por Black Friday."]:
    segs, info = m.transcribe("gancho_2s.wav", language="es", initial_prompt=p, word_timestamps=True)
    print("prompt:", p, "->", " ".join(s.text for s in segs))
y, sr = librosa.load("gancho.wav", sr=16000)
f0, vf, vp = librosa.pyin(y[int(1.0*sr):int(1.9*sr)], fmin=80, fmax=500, sr=sr, frame_length=1024, hop_length=160)
t = 1.0 + np.arange(len(f0))*0.01
for ti, f, v in zip(t, f0, vf):
    print(f"{ti:.2f} {'V' if v else '.'} {0 if np.isnan(f) else int(f)}")
