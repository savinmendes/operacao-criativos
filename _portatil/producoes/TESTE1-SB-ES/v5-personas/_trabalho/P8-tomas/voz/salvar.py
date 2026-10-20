import sys, json, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
H={"xi-api-key":chave(),"Content-Type":"application/json"}
d=json.load(open("voz/design.json")); gid=d["previews"][1]["gid"]
r=requests.post("https://api.elevenlabs.io/v1/text-to-voice",headers=H,json=dict(voice_name="Don Tomas P8 - Colombiano 65 (SB v5)",voice_description=d["desc"],generated_voice_id=gid),timeout=120)
print(r.status_code, r.text[:400])
