import json, sys, urllib.request
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
r = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation", data=json.dumps(dict(text="Busy Latin American city street ambience at a bus stop during the day: distant bus engines idling and passing, light traffic, faint crowd murmur, no music, no clear voices, no horns", duration_seconds=22, prompt_influence=0.5)).encode(), method="POST", headers={"xi-api-key": chave(), "Content-Type": "application/json"})
open("voz/rua.mp3", "wb").write(urllib.request.urlopen(r, timeout=180).read()); print("ok")
