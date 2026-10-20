import os,sys,json,base64,requests
from dotenv import load_dotenv
load_dotenv(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
K=os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY") or os.environ.get("XI_API_KEY")
V="7UEcc2wDVftk45UjyB46"
nome,txt=sys.argv[1],sys.argv[2]
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps",headers={"xi-api-key":K},
 json={"text":txt,"model_id":"eleven_multilingual_v2","language_code":"es","voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.3,"speed":1.12}})
r.raise_for_status(); d=r.json()
open(f"audio/{nome}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
json.dump(d["alignment"],open(f"audio/{nome}.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print(nome,"ok",d["alignment"]["character_end_times_seconds"][-1])
