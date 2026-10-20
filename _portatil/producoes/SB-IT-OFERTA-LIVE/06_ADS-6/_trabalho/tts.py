import requests, json, base64, sys
from dotenv import dotenv_values
k=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key=[v for kk,v in k.items() if "ELEVEN" in kk.upper()][0]
VOZ="nPczCjzI2devNBz1zQrb"  # Brian - Deep, Resonant and Comforting (mesma do EN)
MODEL=sys.argv[1] if len(sys.argv)>1 else "eleven_multilingual_v2"
SPEED=float(sys.argv[2]) if len(sys.argv)>2 else 1.08
txt=" ".join(json.load(open("roteiro_it.json",encoding="utf-8"))).replace("«","").replace("»","")
open("audio/narracao_it.txt","w",encoding="utf-8").write(txt)
body={"text":txt,"model_id":MODEL,"voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.25,"use_speaker_boost":True,"speed":SPEED}}
if len(sys.argv)>3: body["language_code"]="it"
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps?output_format=mp3_44100_192",headers={"xi-api-key":key},json=body,timeout=600)
j=r.json()
if "audio_base64" not in j: print(str(j)[:500]); raise SystemExit(1)
open("audio/narracao_it.mp3","wb").write(base64.b64decode(j["audio_base64"]))
json.dump(j["alignment"],open("audio/narracao_it.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print("chars",len(txt),"dur",j["alignment"]["character_end_times_seconds"][-1])
