# TTS IT com timestamps (ElevenLabs). uso: python tts_it.py <txt> <saida.mp3> <voice_id> [modelo] [speed] [lang]
import sys, json, base64, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
txt=open(sys.argv[1],encoding="utf-8").read().strip().replace("\n"," ")
out=sys.argv[2]; vid=sys.argv[3]; mod=sys.argv[4] if len(sys.argv)>4 else "eleven_multilingual_v2"
sp=float(sys.argv[5]) if len(sys.argv)>5 else 1.0; lang=sys.argv[6] if len(sys.argv)>6 else "it"
body={"text":txt,"model_id":mod,"voice_settings":{"stability":0.5,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True,"speed":sp}}
if lang!="-": body["language_code"]=lang
import os
if os.environ.get("PREV"): body["previous_text"]=open(os.environ["PREV"],encoding="utf-8").read().strip()
if os.environ.get("NEXT"): body["next_text"]=open(os.environ["NEXT"],encoding="utf-8").read().strip()
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps",params={"output_format":"mp3_44100_128"},
  headers={"xi-api-key":chave(),"Content-Type":"application/json"},json=body,timeout=300)
if r.status_code!=200: print("ERRO",r.status_code,r.text[:400]); sys.exit(1)
d=r.json(); open(out,"wb").write(base64.b64decode(d["audio_base64"]))
al=d["alignment"]; json.dump(al,open(out.rsplit(".",1)[0]+".alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print("ok",out,round(al["character_end_times_seconds"][-1],2),"s",len(txt),"chars")
