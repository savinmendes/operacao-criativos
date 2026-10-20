# TTS IT (ElevenLabs API, voz Jesus The Chosen) com alinhamento. uso: python tts_it.py nome "texto" [modelo] [velocidade]
import sys, json, base64, requests
from pathlib import Path
KEY=[l.split("=",1)[1].strip().strip('"') for l in Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env").read_text(encoding="utf-8").splitlines() if l.startswith("ELEVENLABS_API_KEY=")][0]
VOZ="AkQxVSf1kENGmX9WjeDE"
nm,txt=sys.argv[1],sys.argv[2]; mod=sys.argv[3] if len(sys.argv)>3 else "eleven_multilingual_v2"; vel=float(sys.argv[4]) if len(sys.argv)>4 else 1.0
body={"text":txt,"model_id":mod,"voice_settings":{"stability":0.5,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True,"speed":vel}}
if mod!="eleven_multilingual_v2": body["language_code"]="it"
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps",params={"output_format":"mp3_44100_128"},
    headers={"xi-api-key":KEY,"Content-Type":"application/json"},json=body,timeout=300)
if r.status_code!=200: raise SystemExit(f"{r.status_code} {r.text[:300]}")
d=r.json(); Path(f"audio/{nm}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
json.dump(d["alignment"],open(f"audio/{nm}.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
Path(f"audio/{nm}.txt").write_text(txt,encoding="utf-8")
print(nm,"dur",round(d["alignment"]["character_end_times_seconds"][-1],2))
