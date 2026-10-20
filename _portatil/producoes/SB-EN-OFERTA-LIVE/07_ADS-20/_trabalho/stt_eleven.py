import requests,json,sys
k=[l.split('=',1)[1].strip().strip('"') for l in open(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env",encoding="utf-8") if l.startswith("ELEVEN")][0]
src,lang,out=sys.argv[1:4]
r=requests.post("https://api.elevenlabs.io/v1/speech-to-text",headers={"xi-api-key":k},
  data={"model_id":"scribe_v1","language_code":lang,"timestamps_granularity":"word"},files={"file":open(src,"rb")},timeout=600)
r.raise_for_status(); j=r.json()
ws=[{"w":w["text"],"s":round(w["start"],2),"e":round(w["end"],2)} for w in j["words"] if w.get("type")=="word"]
json.dump(ws,open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(j["text"])
