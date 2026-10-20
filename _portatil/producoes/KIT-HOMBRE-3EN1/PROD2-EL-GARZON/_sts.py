import os, requests, subprocess
from dotenv import load_dotenv
load_dotenv(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
k=os.environ["ELEVENLABS_API_KEY"]; V="BPwS5yO6aXvwg8auqNwS"
subprocess.run(["ffmpeg","-v","error","-y","-i","takes/V3_selfie.mp4","-vn","-ac","1","-ar","44100","audio/v3_raw.wav"],check=True)
r=requests.post("https://api.elevenlabs.io/v1/audio-isolation",headers={"xi-api-key":k},files={"audio":open("audio/v3_raw.wav","rb")},timeout=300)
print("iso",r.status_code); r.raise_for_status(); open("audio/v3_voz.mp3","wb").write(r.content)
r=requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{V}",headers={"xi-api-key":k},
  data={"model_id":"eleven_multilingual_sts_v2","remove_background_noise":"false"},files={"audio":open("audio/v3_voz.mp3","rb")},timeout=300)
print("sts",r.status_code); r.raise_for_status(); open("audio/v3_damian.mp3","wb").write(r.content)
