import requests, json, sys
from dotenv import dotenv_values
k=dotenv_values(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env")
key=[v for kk,v in k.items() if "ELEVEN" in kk.upper()][0]
src,lang,out=sys.argv[1],sys.argv[2],sys.argv[3]
r=requests.post("https://api.elevenlabs.io/v1/speech-to-text",headers={"xi-api-key":key},
  data={"model_id":"scribe_v1","language_code":lang,"timestamps_granularity":"word"},files={"file":open(src,"rb")},timeout=600)
j=r.json(); 
if "words" not in j: print(j); sys.exit(1)
res=[{"w":w["text"].strip(),"s":round(w["start"],2),"e":round(w["end"],2)} for w in j["words"] if w.get("type")=="word"]
json.dump(res,open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=0)
# frases por pontuação
fr=[];cur=[]
for w in res:
    cur.append(w)
    if w["w"][-1:] in ".?!…": fr.append(cur);cur=[]
if cur: fr.append(cur)
for c in fr: print(f"[{c[0]['s']:6.2f}-{c[-1]['e']:6.2f}] "+" ".join(x["w"] for x in c))
