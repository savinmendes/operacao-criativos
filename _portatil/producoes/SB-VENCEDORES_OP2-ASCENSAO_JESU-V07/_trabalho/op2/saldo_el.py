import sys, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
k=chave()
s=requests.get("https://api.elevenlabs.io/v1/user/subscription",headers={"xi-api-key":k}).json()
print("usados",s.get("character_count"),"limite",s.get("character_limit"),"tier",s.get("tier"))
if len(sys.argv)>1:
    v=requests.get("https://api.elevenlabs.io/v1/voices/"+sys.argv[1],headers={"xi-api-key":k}).json()
    print(v.get("name"),v.get("category"),v.get("fine_tuning",{}).get("language"),v.get("labels"),v.get("settings"))
