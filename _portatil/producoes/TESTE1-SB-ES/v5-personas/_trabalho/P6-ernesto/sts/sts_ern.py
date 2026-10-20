# STS só na fala do Ernesto na briga (slow timeline 9.30 s -> fim): vocals demucs -> Jose (lQFpy8cEH4bDaHre2DpA); remonta no_vocals + vocals(agressor) + STS
import sys, json, subprocess, numpy as np, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
SR = 44100; A = 9.85; D = "sts/sep/htdemucs/briga/"
def load(p): return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
voc, fundo = load(D + "vocals.wav"), load(D + "no_vocals.wav"); s = int(A * SR)
seg = voc[s:]; subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", "sts/ern_in.wav"], input=seg.tobytes(), check=True)
with open("sts/ern_in.wav", "rb") as f:
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-speech/lQFpy8cEH4bDaHre2DpA", params={"output_format": f"pcm_{SR}"}, headers={"xi-api-key": chave()},
                      data={"model_id": "eleven_multilingual_sts_v2", "voice_settings": json.dumps({"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True}),
                            "remove_background_noise": "false"}, files={"audio": f}, timeout=300)
assert r.status_code == 200, r.text[:300]
o = np.frombuffer(r.content, np.int16).astype(np.float32) / 32768; print("dur in", len(seg) / SR, "out", len(o) / SR)
o = np.concatenate([o, np.zeros(max(0, len(seg) - len(o)), np.float32)])[:len(seg)]
o *= (np.sqrt(np.mean(seg ** 2)) + 1e-9) / (np.sqrt(np.mean(o ** 2)) + 1e-9)
xf = int(0.02 * SR); w = np.linspace(0, 1, xf); o[:xf] = seg[:xf] * (1 - w) + o[:xf] * w
v2 = voc.copy(); v2[s:] = o; mix = v2 + fundo
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", "sts/briga_sts.wav"], input=mix.tobytes(), check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "takes/briga2_slow.mov", "-i", "sts/briga_sts.wav", "-map", "0:v", "-map", "1:a", "-c", "copy", "takes/briga2_slow_sts.mov"], check=True)
print("ok")
