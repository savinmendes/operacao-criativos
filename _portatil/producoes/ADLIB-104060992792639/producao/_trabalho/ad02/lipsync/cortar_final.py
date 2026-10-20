# -*- coding: utf-8 -*-
"""Corta o AD 02 FINAL em trechos de lipsync (gancho h1 + s02..s13 do AD 01 deslocados +44 q) para o revisar_ad --lipsync.
Gera final_loteA/f_*.mp4 (final), e_*.mp3 (narracao ES do 02), o_*.mp4 (base_sem_legenda do 02) e lipsync_arg.txt."""
import json, subprocess
from pathlib import Path
AQ = Path(__file__).resolve().parent; AD = AQ.parent; OFF = 44
FIN = AD.parent.parent / "AD 02 - ORACION-TRES-BENDICIONES-SHOPPING-ES-LATAM.mp4"
OUT = AQ / "final_loteA"; OUT.mkdir(exist_ok=True)
NMAX = 3509
seg = [("h1", 0, 285, "258;357;234;278")]
for s in json.loads((AD.parent / "ad01/segmentos.json").read_text())["segmentos"]:
    if s["nome"] == "s01": continue
    seg.append((s["nome"], s["quadro_ini"] + OFF, min(s["quadro_fim"] + OFF, NMAX), "330;280;200;260"))
parts = []
for n, a, b, r in seg:
    for src, out in ((FIN, OUT / f"f_{n}.mp4"), (AD / "base_sem_legenda.mp4", OUT / f"o_{n}.mp4")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"trim=start_frame={a}:end_frame={b+1},setpts=PTS-STARTPTS",
                        "-an", "-threads", "4", "-c:v", "libx264", "-crf", "14", str(out)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AD / "narracao_es.wav"), "-af", f"atrim={a/30}:{(b+1)/30},asetpts=PTS-STARTPTS",
                    "-ac", "1", "-c:a", "libmp3lame", "-b:a", "192k", str(OUT / f"e_{n}.mp3")], check=True)
    parts.append(f"f_{n}.mp4:e_{n}.mp3:o_{n}.mp4:{r}")   # relativo: rodar o revisar_ad dentro de final_loteA
(OUT / "lipsync_arg.txt").write_text(",".join(parts), encoding="utf-8"); print(len(parts), "trechos")
