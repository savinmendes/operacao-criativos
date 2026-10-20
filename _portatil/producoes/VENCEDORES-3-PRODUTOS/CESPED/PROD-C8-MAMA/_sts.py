import sys,requests
from dotenv import dotenv_values
K=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
V="dQafQNlqLLJDepKplzjl"
src,dst=sys.argv[1],sys.argv[2]
r=requests.post("https://api.elevenlabs.io/v1/audio-isolation",headers={"xi-api-key":K},files={"audio":open(src,"rb")});r.raise_for_status()
open("audio/selfie_iso.mp3","wb").write(r.content)
r=requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{V}",headers={"xi-api-key":K},files={"audio":open("audio/selfie_iso.mp3","rb")},
  data={"model_id":"eleven_multilingual_sts_v2","remove_background_noise":"true"});r.raise_for_status()
open(dst,"wb").write(r.content);print("ok",dst)
