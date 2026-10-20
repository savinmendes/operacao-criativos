import json,sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\voz"); import montar_vozes
al, out, pers, parte = sys.argv[1:5]
ws = montar_vozes.palavras(al)
ws = [dict(w, ini=round(w["ini"],3), fim=round(w["fim"],3), personagem=pers, parte=parte) for w in ws]
Path(out).write_text(json.dumps(ws, ensure_ascii=False, indent=1), encoding="utf-8")
for a,b in zip(ws,ws[1:]):
    if b["ini"]-a["fim"]>0.15: print(f'pausa {a["fim"]:.2f}-{b["ini"]:.2f} ({b["ini"]-a["fim"]:.2f}) apos {a["w"]}')
print("fim", ws[-1]["fim"], len(ws))
