import requests
from dotenv import dotenv_values
key = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": key},
    json={"prompt": "Instrumental for a 35 second social ad in two moods: first 10 seconds tense, suspenseful plucked strings and low pulsing synth (disgust/shock moment in a backyard), then a turn to warm, upbeat, bright latin pop with acoustic guitar, light percussion and claps, hopeful family vibe, steady groove until the end", "music_length_ms": 40000, "force_instrumental": True}, timeout=300)
print(r.status_code)
if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
else: print(r.text[:500])
