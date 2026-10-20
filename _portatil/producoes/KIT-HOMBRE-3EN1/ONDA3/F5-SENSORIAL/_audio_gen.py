import os, json, requests
from dotenv import dotenv_values
K = dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key = next(v for k, v in K.items() if "ELEVEN" in k.upper())
H = {"xi-api-key": key, "Content-Type": "application/json"}
def sub():
    r = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers=H); d = r.json()
    return d.get("character_count"), d.get("character_limit")
print("antes", sub())
if not os.path.exists("audio/trilha.mp3"):
    r = requests.post("https://api.elevenlabs.io/v1/music", headers=H, json={
        "prompt": "Dark luxurious cinematic trap instrumental for a premium men's perfume commercial: deep sub bass, slow heavy 808 groove at 75 BPM, middle-eastern oud melody and darbuka hits, dramatic string swells, a big bass drop at about 3 seconds, sexy and powerful, confident night-time mood, builds to a climactic finish at 28 seconds then a clean ending hit. No vocals.",
        "music_length_ms": 30000, "force_instrumental": True}, timeout=300)
    print("music", r.status_code, r.headers.get("content-type")); 
    if r.ok: open("audio/trilha.mp3", "wb").write(r.content)
    else: print(r.text[:500])
for nome, txt, d in [("sfx_borrifada", "Close-up perfume atomizer spray, two quick crisp pressurized mist sprays, fine hiss, clean studio, no music", 1.5),
                     ("sfx_whoosh", "Deep cinematic whoosh transition with a soft low boom, luxury commercial, no music", 1.2)]:
    if os.path.exists(f"audio/{nome}.mp3"): continue
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers=H, json={"text": txt, "duration_seconds": d, "prompt_influence": 0.6}, timeout=120)
    print(nome, r.status_code)
    if r.ok: open(f"audio/{nome}.mp3", "wb").write(r.content)
    else: print(r.text[:300])
print("depois", sub())
