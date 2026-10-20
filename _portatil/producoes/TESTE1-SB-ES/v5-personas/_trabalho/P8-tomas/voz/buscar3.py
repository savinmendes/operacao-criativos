import sys, json, requests, re
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
H={"xi-api-key":chave()}
n=0
for page in range(0,12):
    r=requests.get("https://api.elevenlabs.io/v1/shared-voices",headers=H,params=dict(page_size=100,page=page,language="es",gender="male",age="old"),timeout=60).json()
    vs=r.get("voices",[])
    for v in vs:
        n+=1
        t=(v.get("name","")+" "+(v.get("description") or "")).lower()
        if re.search(r"colomb|andin|andean|bogot|paisa|ecuador|peru|bolivi|quito|medell|antioq|cali|boyac",t):
            print(v["voice_id"],"|",v["name"],"|",v.get("accent"),v.get("cloned_by_count"),"|",(v.get("description") or "")[:200].replace("\n"," "))
    if not r.get("has_more"): break
print("total",n)
