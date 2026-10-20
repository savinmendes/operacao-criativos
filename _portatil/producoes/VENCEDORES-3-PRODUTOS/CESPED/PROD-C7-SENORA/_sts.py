import os,sys,subprocess,requests
from dotenv import load_dotenv
load_dotenv(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
K=os.environ["ELEVENLABS_API_KEY"]; V="7UEcc2wDVftk45UjyB46"
src,nome=sys.argv[1],sys.argv[2]
raw=f"audio/{nome}_raw.wav"
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vn","-ac","1","-ar","44100",raw],check=True)
r=requests.post("https://api.elevenlabs.io/v1/audio-isolation",headers={"xi-api-key":K},files={"audio":open(raw,"rb")}); r.raise_for_status()
open(f"audio/{nome}_voz.mp3","wb").write(r.content)
r=requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{V}",headers={"xi-api-key":K},files={"audio":open(f"audio/{nome}_voz.mp3","rb")},
  data={"model_id":"eleven_multilingual_sts_v2","remove_background_noise":"true","voice_settings":'{"stability":0.5,"similarity_boost":0.85}'}); r.raise_for_status()
open(f"audio/{nome}_louis.mp3","wb").write(r.content); print("ok")
