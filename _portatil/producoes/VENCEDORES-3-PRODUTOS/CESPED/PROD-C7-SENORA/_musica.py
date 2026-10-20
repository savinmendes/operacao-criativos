import os,requests
from dotenv import load_dotenv
load_dotenv(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
K=os.environ["ELEVENLABS_API_KEY"]
p=("Instrumental latin acoustic pop for a family story ad, 40 seconds. First 10 seconds: soft melancholic nylon guitar and light piano, "
   "sad and intimate. Then it turns warm and hopeful: upbeat strummed acoustic guitar, cajón percussion, bright bass, a happy Sunday family feeling until the end. No vocals.")
r=requests.post("https://api.elevenlabs.io/v1/music",headers={"xi-api-key":K},json={"prompt":p,"music_length_ms":40000,"force_instrumental":True},timeout=300)
print(r.status_code, r.headers.get("content-type"))
r.raise_for_status(); open("audio/trilha.mp3","wb").write(r.content); print("ok",len(r.content))
