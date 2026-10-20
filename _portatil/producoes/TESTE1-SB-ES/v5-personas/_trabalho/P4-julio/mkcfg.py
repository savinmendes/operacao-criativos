# -*- coding: utf-8 -*-
"""gera cfg.json (timeline) a partir dos takes existentes; HeyGen ausente -> placeholder (imagem) para testar"""
import json, subprocess
from pathlib import Path
AQ = Path(__file__).resolve().parent
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode())
def pal(i): return json.loads((AQ / "voz" / f"{i}.palavras.json").read_text(encoding="utf-8"))
def hg(i, voz, z=1.0, cy=0.41, cx=0.5, ini=0.0):
    f = AQ / "takes" / f"hg_{i}.mp4"; d = dur(AQ / "voz" / f"{voz}.wav")
    if f.exists(): return dict(id=i, tipo="video", file=f"takes/hg_{i}.mp4", ini=ini, fim=ini + d, voz=voz, voz_ini=ini, z=z, cy=cy, cx=cx, amb=True)
    im = "img/reportera_obra.png" if i.startswith("R") else "img/julio_mestre.png"
    return dict(id=i, tipo="img", file=im, dur=d - ini, voz=voz, voz_ini=ini, z=(z, z), cy=cy, cx=cx, amb=True, placeholder=True)
pipf = AQ / "takes" / "hg_PIP.mp4"
cfg = dict(
    pip=dict(file="takes/hg_PIP.mp4" if pipf.exists() else "takes/hg_J1.mp4", ate=dur(AQ / "voz" / "R00.wav"), voz_fim=pal("R00")[-1]["fim"]),
    segs=[
        dict(id="BRIGA", tipo="briga", file="takes/briga_final.mov", ini=0.0, fim=12.25, cy=0.44, zoom_ini=1.3, zoom_ate=2.0, zc=(400, 300)),
        dict(id="MANOS", tipo="video", file="takes/k_manos.mp4", ini=1.6, fim=4.4, cy=0.5),
        dict(id="PARADA", tipo="img", file="img/parada2.png", dur=1.9, z=(1.0, 1.06), cy=0.55),
        dict(id="PLANOS", tipo="img", file="img/planos.png", dur=1.8, z=(1.07, 1.0), cy=0.5),
        dict(id="EQUIPE", tipo="img", file="img/equipe.png", dur=2.0, z=(1.0, 1.07), cy=0.45),
        hg("R01", "R01", 1.0, 0.39),
        hg("J1", "J1", 1.0, 0.41),
        dict(id="NOITE", tipo="img", file="img/noite.png", dur=dur(AQ / "voz" / "J2.wav"), voz="J2", z=(1.0, 1.08), cy=0.45),
        hg("J3", "J3", 1.12, 0.37, 0.48),
        hg("P1", "P1", 1.0, 0.41),
        hg("P2", "P2", 1.12, 0.37, 0.48),
        hg("P3", "P3", 1.0, 0.41),
        hg("R02", "R02", 1.06, 0.38),
    ])
(AQ / "cfg.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
print("placeholders:", [s["id"] for s in cfg["segs"] if s.get("placeholder")], "pip:", cfg["pip"]["file"])
