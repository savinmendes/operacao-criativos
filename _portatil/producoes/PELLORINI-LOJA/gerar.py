import json,re,sys
d=json.loads(sys.stdin.read())["data"]["products"]["nodes"]
json.dump(d,open("backup_produtos_admin.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
def novo(t):
    t=t.replace("Pelvini®","Pellorini").replace("Pelvini","Pellorini")
    t=re.sub(r"Pellorini\s*-\s*","Pellorini ",t); t=re.sub(r"\(\s*","(",t); t=re.sub(r"\s*\)",")",t); t=re.sub(r"\s{2,}"," ",t).strip()
    return t
vars_={}; parts=[]; decl=[]; linhas=[]
for i,p in enumerate(d):
    inp={"id":p["id"],"title":novo(p["title"]),"vendor":"Pellorini"}
    desc=p["descriptionHtml"]
    nd=desc.replace("Signature Pelvini design","Signature Pellorini design").replace("The Hudson Aurora Watch","The Aurora Watch")
    if nd!=desc: inp["descriptionHtml"]=nd
    vars_[f"p{i}"]=inp; decl.append(f"$p{i}: ProductUpdateInput!")
    parts.append(f"a{i}: productUpdate(product: $p{i}) {{ product {{ title vendor }} userErrors {{ field message }} }}")
    linhas.append(f"{p['title']}  ->  {inp['title']}" + ("  [+descrição]" if "descriptionHtml" in inp else ""))
q="mutation("+", ".join(decl)+") {\n"+"\n".join(parts)+"\n}"
open("mut.graphql","w",encoding="utf-8").write(q); json.dump(vars_,open("mut_vars.json","w",encoding="utf-8"),ensure_ascii=False)
open("trocas_titulos.txt","w",encoding="utf-8").write("\n".join(linhas)); print("\n".join(linhas))
