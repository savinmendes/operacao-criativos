# upload REST (chave do gerador-criativos-video, nao impressa). uso: python up.py arquivo...  -> appends id em up.json
import sys, json, os, requests
from pathlib import Path
K = None
for l in open(r"C:\Users\PICHAU\Downloads\Produtividade com ia\ferramentas\gerador-criativos-video\.env", encoding="utf-8"):
    if l.startswith("HEYGEN_API_KEY="): K = l.split("=", 1)[1].strip().strip('"')
J = Path(__file__).parent.parent / "up.json"
db = json.load(open(J)) if J.exists() else {}
for f in sys.argv[1:]:
    n = os.path.basename(f)
    if n in db: continue
    ct = "video/mp4" if n.endswith(".mp4") else "audio/mpeg"
    for t in range(3):
        try:
            with open(f, "rb") as fh:
                r = requests.post("https://api.heygen.com/v3/assets", headers={"X-Api-Key": K}, files={"file": (n, fh, ct)}, timeout=300)
            d = r.json(); aid = (d.get("data") or {}).get("asset_id") or (d.get("data") or {}).get("id")
            if aid: break
            print(n, r.status_code, str(d)[:300])
        except Exception as e: print(n, "erro", e)
    else: continue
    import time; time.sleep(2.2)
    db[n] = aid; json.dump(db, open(J, "w"), indent=1); print(n, aid, flush=True)
