import os, requests
from dotenv import load_dotenv
load_dotenv(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
k=os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY")
r=requests.post("https://api.elevenlabs.io/v1/music",headers={"xi-api-key":k},json={
 "prompt":"Upbeat playful Latin cumbia instrumental, festive Chilean picada restaurant vibe, accordion, guira, bass and congas, cheerful and cheeky, steady groove, no vocals",
 "music_length_ms":40000,"force_instrumental":True},timeout=300)
print(r.status_code, r.headers.get("content-type"))
if r.ok: open("audio/trilha.mp3","wb").write(r.content)
else: print(r.text[:500])
