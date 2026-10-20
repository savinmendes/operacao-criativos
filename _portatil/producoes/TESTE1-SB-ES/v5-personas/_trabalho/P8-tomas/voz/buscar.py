import sys, json, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
H={"xi-api-key":chave()}
seen=set()
for q in [dict(language="es",accent="colombian",gender="male",age="old"),dict(language="es",accent="colombian",gender="male"),dict(language="es",search="colombiano abuelo"),dict(language="es",search="andino"),dict(language="es",search="paisa"),dict(language="es",gender="male",age="old",accent="latin american")]:
    r=requests.get("https://api.elevenlabs.io/v1/shared-voices",headers=H,params=dict(page_size=40,**q),timeout=60).json()
    for v in r.get("voices",[]):
        if v["voice_id"] in seen: continue
        seen.add(v["voice_id"])
        print(q.get("accent",q.get("search","")),"|",v["voice_id"],"|",v["name"],"|",v.get("accent"),v.get("age"),v.get("gender"),v.get("use_case"),"|",(v.get("description") or "")[:110].replace("\n"," "))
