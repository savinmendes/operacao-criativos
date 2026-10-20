# Regrava SO a frase trocada, mesma voz/config do tts.py original, com previous_text/next_text p/ casar a entonação
import requests, json, base64
from dotenv import dotenv_values
k=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key=[v for kk,v in k.items() if "ELEVEN" in kk.upper()][0]
VOZ="nPczCjzI2devNBz1zQrb"  # Brian
TXT="Not by chance, but because this message is meant for you."
PREV="God stopped you right here to speak to you."
NEXT="No other message like this will come. What is about to be released from heaven will move your soul."
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps?output_format=mp3_44100_192",headers={"xi-api-key":key},
  json={"text":TXT,"previous_text":PREV,"next_text":NEXT,"model_id":"eleven_multilingual_v2",
        "voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.25,"use_speaker_boost":True,"speed":1.08}},timeout=300)
j=r.json()
if "audio_base64" not in j: print(str(j)[:500]); raise SystemExit(1)
open("audio/frase01_nova.mp3","wb").write(base64.b64decode(j["audio_base64"]))
json.dump(j["alignment"],open("audio/frase01_nova.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print("chars",len(TXT),"dur",j["alignment"]["character_end_times_seconds"][-1])
