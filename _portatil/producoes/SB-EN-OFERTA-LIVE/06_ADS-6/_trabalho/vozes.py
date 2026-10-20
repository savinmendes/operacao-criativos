import requests, json, os
from dotenv import dotenv_values
k=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key=[v for kk,v in k.items() if "ELEVEN" in kk.upper()][0]
r=requests.get("https://api.elevenlabs.io/v1/voices",headers={"xi-api-key":key}).json()
vs=r["voices"]; print(len(vs))
json.dump([{"id":v["voice_id"],"name":v["name"],"cat":v.get("category"),"labels":v.get("labels"),"desc":(v.get("description") or "")[:80]} for v in vs],open("vozes.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
for v in vs:
    l=v.get("labels") or {}
    print(v["voice_id"],"|",v["name"],"|",v.get("category"),"|",l.get("gender"),l.get("age"),l.get("accent"),l.get("language"))
