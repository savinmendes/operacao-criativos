# Regrava SO a frase trocada (sem "ultimo avviso"), mesma voz/config do tts.py IT (Brian, multilingual_v2, it, speed 1.08), com previous_text/next_text
import requests, json, base64
from dotenv import dotenv_values
k=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key=[v for kk,v in k.items() if "ELEVEN" in kk.upper()][0]
VOZ="nPczCjzI2devNBz1zQrb"  # Brian
TXT="Non per caso, ma perché questo messaggio è proprio per te."
PREV="Dio ti ha fermato proprio qui per parlare a te."
NEXT="Non arriverà un altro messaggio come questo. Quello che sta per essere liberato dal cielo ti scuoterà l'anima."
r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps?output_format=mp3_44100_192",headers={"xi-api-key":key},
  json={"text":TXT,"previous_text":PREV,"next_text":NEXT,"model_id":"eleven_multilingual_v2","language_code":"it",
        "voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.25,"use_speaker_boost":True,"speed":1.08}},timeout=300)
j=r.json()
if "audio_base64" not in j: print(str(j)[:500]); raise SystemExit(1)
open("audio/frase01_nova.mp3","wb").write(base64.b64decode(j["audio_base64"]))
json.dump(j["alignment"],open("audio/frase01_nova.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print("chars",len(TXT),"dur",j["alignment"]["character_end_times_seconds"][-1])
