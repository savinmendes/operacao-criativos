import json, sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import T, M
P = json.load(open(M / "params.json")); F0 = int(round(P["T0"] * 30)); NF = P["NF"]
L = [t for t in json.load(open(T / "voz" / "lotes.json", encoding="utf-8"))["trechos"] if int(t["id"][1:]) >= 22]
out = []
for b in range((NF + 8999) // 9000):
    a, e = F0 + b * 9000, F0 + min(NF, (b + 1) * 9000)
    need = [t["id"] for t in L if round(t["novo_fim"] * 30) > a and round(t["novo_ini"] * 30) < e]
    falta = [i for i in need if not (M / "comp" / f"{i}.json").exists()]
    feito = (M / "blocos" / f"bl{b:02d}.mp4").exists()
    print(b, "pronto" if not falta else f"falta {len(falta)}", "renderizado" if feito else "")
