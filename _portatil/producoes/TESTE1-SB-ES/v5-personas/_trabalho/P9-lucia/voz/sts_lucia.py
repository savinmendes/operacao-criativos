import sys, json, requests, numpy as np, subprocess
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
SR = 44100
with open("lucia_seg.wav", "rb") as f:
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-speech/D3ws14YxTqcjPaXEOehR", params={"output_format": f"pcm_{SR}"},
                      headers={"xi-api-key": chave()},
                      data={"model_id": "eleven_multilingual_sts_v2", "voice_settings": json.dumps({"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True}),
                            "remove_background_noise": "false"}, files={"audio": ("a.wav", f, "audio/wav")}, timeout=300)
r.raise_for_status()
y = np.frombuffer(r.content, np.int16).astype(np.float32) / 32768
n = int(3.5 * SR); print("dur api", len(y) / SR)
y = np.concatenate([y, np.zeros(max(0, n - len(y)), np.float32)])[:n]
open("lucia_sts.f32", "wb").write(y.tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "lucia_sts.f32", "-c:a", "pcm_s16le", "lucia_sts.wav"], check=True)
