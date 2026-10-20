cd "/c/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos"; export PYTHONIOENCODING=utf-8
python - <<'PY' > /tmp/grim_cmds.txt
import json
R=json.load(open(r"C:/Users/PICHAU/Downloads/GRIMORIO_analise/_trabalho_es/audio/roteiro.json",encoding="utf-8"))
V={"rep":"cIBxLwfshLYhRB9lCXEg","chora":"sKgg4MPUDBy69X7iv3fA","roxo":"BskzYZ6zvapoZ3mBu93C"}
for k,r in enumerate(R):
    prev=" ".join(x["t"] for x in R[max(0,k-2):k] if x["voz"]==r["voz"])
    nxt=" ".join(x["t"] for x in R[k+1:k+2] if x["voz"]==r["voz"])
    print("\t".join([r["id"],V[r["voz"]],r["t"],prev,nxt,str(r.get("estab",0.5 if r["voz"]=="roxo" else 0.4)),str(r.get("estilo",0.0 if r["voz"]=="roxo" else 0.3))]))
PY
while IFS=$'\t' read -r i v t p n e s; do python "/c/Users/PICHAU/Downloads/GRIMORIO_analise/_trabalho_es/audio/tts_es.py" "$i" "$v" "$t" "$p" "$n" "$e" "$s" & 
 while [ $(jobs -r | wc -l) -ge 4 ]; do sleep 0.5; done; done < /tmp/grim_cmds.txt; wait
