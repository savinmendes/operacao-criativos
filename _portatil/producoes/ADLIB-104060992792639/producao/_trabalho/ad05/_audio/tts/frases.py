import json,re,sys
for b in sys.argv[1:]:
    al=json.load(open(f"{b}.alinhamento.json",encoding="utf-8"))
    ch,s,e=al["characters"],al["character_start_times_seconds"],al["character_end_times_seconds"]
    txt="".join(ch); i=0
    print("==",b,len(ch),round(e[-1],2))
    for m in re.finditer(r"[^.?!:]+[.?!:]?",txt):
        a,z=m.start(),m.end()-1
        while a<z and txt[a].isspace(): a+=1
        if z<=a: continue
        print(f"  {s[a]:6.2f}-{e[z]:6.2f} {txt[a:z+1]}")
