# -*- coding: utf-8 -*-
"""Troca MAYAVERRA -> LYMPHORIA na faixa verde (band_fix do ad25), sem Kling. Gera bf/tN_fix.mp4 + extras.json"""
import json, subprocess, sys
from pathlib import Path
P = Path(__file__).parent; (P / "bf").mkdir(exist_ok=True)
BF = P.parent / "ad25" / "band_fix.py"
# (inicio s, quadros, roi em 360p, min_area 360p)
TAKES = [(407.10, 86, (140, 418, 225, 452), 40),
         (419.00, 51, (140, 305, 205, 335), 15),
         (420.70, 52, (60, 230, 320, 330), 300),
         (482.93, 122, (125, 395, 210, 425), 40),
         (531.67, 100, (85, 270, 140, 302), 10)]
so = [int(x) for x in sys.argv[1:]] or range(1, len(TAKES) + 1)
ext = []
for i, (ini, q, roi, ma) in enumerate(TAKES, 1):
    o = P / "bf" / f"t{i}.mp4"; f = P / "bf" / f"t{i}_fix.mp4"
    if i in so:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", str(P / "full_up720.mp4"), "-frames:v", str(q), "-an",
                        "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", "-r", "30", str(o)], check=True)
        r2 = ",".join(str(v * 2) for v in roi)
        subprocess.run([sys.executable, str(BF), str(o), str(f), "--roi", r2, "--min-area", str(ma * 4)], check=True)
    ext.append({"clipe": f"bf/t{i}_fix.mp4", "inicio": ini, "quadros": q})
json.dump(ext, open(P / "extras.json", "w"), indent=1)
