import json, os, glob, re
from rapidocr_onnxruntime import RapidOCR
eng = RapidOCR()
BASE = r"C:\Users\PICHAU\Downloads\MOPA VERDE - H2O X5"
BR = re.compile(r"H\s*2\s*[O0]|X\s*5|FBX5|USE CODE|\$|£|UK|USA|1300|watt|million|99", re.I)
def run(path):
    res, _ = eng(path)
    out = []
    for box, txt, sc in (res or []):
        xs = [p[0] for p in box]; ys = [p[1] for p in box]
        out.append({"texto": txt, "conf": round(float(sc), 2), "caixa": [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))]})
    return out
# videos: 4 fps
res_v = {}
for d in sorted(glob.glob("frames/*")):
    vid = os.path.basename(d)
    if os.path.exists(f"ocr/{vid}_ocr.json"): continue
    fr = sorted(glob.glob(d + "/*.jpg")); linhas = []
    for i, f in enumerate(fr):
        t = i * 1.0
        for b in run(f):
            if b["conf"] < 0.6: continue
            linhas.append((t, b))
    # dedupe: group identical normalized text across consecutive samples
    grupos = {}
    for t, b in linhas:
        k = re.sub(r"\W", "", b["texto"].lower())
        g = grupos.get(k)
        if g and t - g[-1]["fim"] <= 1.0: g[-1]["fim"] = t; continue
        grupos.setdefault(k, []).append({"texto": b["texto"], "ini": t, "fim": t, "caixa": b["caixa"]})
    eventos = sorted([e for v in grupos.values() for e in v], key=lambda e: e["ini"])
    for e in eventos: e["fim"] = round(e["fim"] + 1.0, 2); e["marca_ou_alerta"] = bool(BR.search(e["texto"]))
    res_v[vid] = eventos
    json.dump(eventos, open(f"ocr/{vid}_ocr.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(vid, len(eventos))
for f in sorted(glob.glob(os.path.join(BASE, "IMAGENS", "*.jpg"))):
    iid = os.path.basename(f)[:2]; bl = run(f)
    for b in bl: b["marca_ou_alerta"] = bool(BR.search(b["texto"])); b["remover"] = bool(re.search(r"FBX5|USE CODE", b["texto"], re.I))
    json.dump(bl, open(f"ocr/img_{iid}_ocr.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("img", iid, len(bl))
