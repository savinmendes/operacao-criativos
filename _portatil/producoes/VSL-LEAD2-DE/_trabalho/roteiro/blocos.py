import json
S=json.load(open(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_estudo\transcricao_es.json",encoding='utf-8'))
FORCE=[288.0,327.1,393.87,403.5,584.0,706.0,618.1,659.1,706.2]  # quebras obrigatorias
blocks=[];cur=[]
def close():
    global cur
    if cur: blocks.append(cur); cur=[]
for i,s in enumerate(S):
    if cur:
        gap=s['ini']-cur[-1]['fim']
        if gap>2.0 or any(cur[-1]['fim']<=f+0.3 and s['ini']>=f-0.6 for f in FORCE): close()
    cur.append(s)
    t=s['texto'].rstrip()
    dur=cur[-1]['fim']-cur[0]['ini']
    end=t.endswith(('.','?','!'))
    if (end and dur>=7) or dur>=16 or (end and len(cur)>=4): close()
close()
out=[]
for k,b in enumerate(blocks,1):
    out.append({"id":f"B{k:03d}","ini_es":round(b[0]['ini'],2),"fim_es":round(b[-1]['fim'],2),"es":" ".join(x['texto'] for x in b)})
json.dump(out,open("blocos_es.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(out))
def mm(t): return f"{int(t//60):02d}:{t%60:05.2f}"
with open("blocos_es.txt","w",encoding="utf-8") as f:
    for o in out: f.write(f"{o['id']} {mm(o['ini_es'])}-{mm(o['fim_es'])} | {o['es']}\n")
