import requests
from dotenv import dotenv_values
K=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")["ELEVENLABS_API_KEY"]
r=requests.post("https://api.elevenlabs.io/v1/music",headers={"xi-api-key":K},json={
 "prompt":"Instrumental Latin acoustic folk: gentle nylon-string guitar and soft piano, tender and slightly melancholic at the start, then warm and hopeful with light percussion and charango from the middle on. Emotional family feeling, no vocals.",
 "music_length_ms":42000,"force_instrumental":True},timeout=300)
r.raise_for_status(); open("audio/trilha.mp3","wb").write(r.content); print(len(r.content))
