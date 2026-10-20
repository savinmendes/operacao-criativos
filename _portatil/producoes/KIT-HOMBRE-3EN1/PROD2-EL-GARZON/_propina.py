import os, requests, base64, json, subprocess
from dotenv import load_dotenv
load_dotenv(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
k=os.environ["ELEVENLABS_API_KEY"]; V="BPwS5yO6aXvwg8auqNwS"
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps",headers={"xi-api-key":k},
 json={"text":"Nunca me habían dejado tanta propina.","model_id":"eleven_multilingual_v2","language_code":"es"},timeout=120)
d=r.json(); open("audio/_prop_tts.mp3","wb").write(base64.b64decode(d["audio_base64"]))
a=d["alignment"]; s="".join(a["characters"]); i=s.find("propina")
print("propina", a["character_start_times_seconds"][i], a["character_end_times_seconds"][i+6])
json.dump(a,open("audio/_prop_tts.json","w",encoding="utf-8"))
