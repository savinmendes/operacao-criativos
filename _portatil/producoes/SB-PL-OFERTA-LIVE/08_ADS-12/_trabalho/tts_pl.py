# Gera a voz PL (Jesus The Chosen, eleven_multilingual_v2, tenta language_code=pl) com alinhamento
import sys, json, base64, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
VOZ="AkQxVSf1kENGmX9WjeDE"; out=sys.argv[1]; modelo=sys.argv[2] if len(sys.argv)>2 else "eleven_multilingual_v2"
txt=open("audio/voz_pl.txt",encoding="utf-8").read().strip()
body={"text":txt,"model_id":modelo,"language_code":"pl",
      "voice_settings":{"stability":0.5,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True,"speed":1.0}}
H={"xi-api-key":chave(),"Content-Type":"application/json"}
U=f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps"
r=requests.post(U,params={"output_format":"mp3_44100_128"},headers=H,json=body,timeout=300)
if r.status_code!=200:
    print("com language_code falhou:",r.status_code,r.text[:200]); body.pop("language_code")
    r=requests.post(U,params={"output_format":"mp3_44100_128"},headers=H,json=body,timeout=300)
if r.status_code!=200: raise SystemExit(r.text[:300])
d=r.json(); open(out,"wb").write(base64.b64decode(d["audio_base64"]))
json.dump(d.get("normalized_alignment") or d["alignment"],open(out[:-4]+".alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print("ok",out,len(txt),"chars", "language_code" in body)
