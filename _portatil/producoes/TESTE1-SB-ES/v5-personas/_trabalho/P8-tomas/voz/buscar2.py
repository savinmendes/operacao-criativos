import sys, json, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
H={"xi-api-key":chave()}
for q in [dict(language="es",accent="peruvian",gender="male"),dict(language="es",accent="ecuadorian",gender="male"),dict(language="es",accent="bolivian",gender="male"),dict(language="es",accent="colombian",gender="male",search="abuelo"),dict(language="es",accent="colombian",gender="male",search="mayor"),dict(language="es",accent="colombian",gender="male",search="old"),dict(language="es",accent="colombian",gender="male",search="señor")]:
    r=requests.get("https://api.elevenlabs.io/v1/shared-voices",headers=H,params=dict(page_size=30,**q),timeout=60).json()
    for v in r.get("voices",[]):
        print(q.get("accent"),q.get("search",""),"|",v["voice_id"],"|",v["name"],"|",v.get("age"),v.get("use_case"),v.get("cloned_by_count"),"|",(v.get("description") or "")[:120].replace("\n"," "))
