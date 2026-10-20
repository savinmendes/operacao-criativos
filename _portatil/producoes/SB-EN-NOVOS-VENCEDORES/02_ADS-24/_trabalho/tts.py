import requests, json, base64, sys
from dotenv import dotenv_values
k=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key=[v for kk,v in k.items() if "ELEVEN" in kk.upper()][0]
R=json.load(open("roteiro_en.json",encoding="utf-8"))
quem=sys.argv[1]; voz=sys.argv[2]; speed=float(sys.argv[3]); stab=float(sys.argv[4]) if len(sys.argv)>4 else 0.5
txt=" ".join(R[quem])
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps?output_format=mp3_44100_192",headers={"xi-api-key":key},
  json={"text":txt,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":stab,"similarity_boost":0.8,"style":0.25,"use_speaker_boost":True,"speed":speed}},timeout=600)
j=r.json()
if "audio_base64" not in j: print(str(j)[:500]); raise SystemExit(1)
open(f"audio/{quem}.mp3","wb").write(base64.b64decode(j["audio_base64"]))
json.dump(j["alignment"],open(f"audio/{quem}.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print(quem,"chars",len(txt),"dur",j["alignment"]["character_end_times_seconds"][-1])
