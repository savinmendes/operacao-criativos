# -*- coding: utf-8 -*-
"""Recorta os takes com frasco do parte1_up.mp4 (sem áudio). Take < MIN s é estendido em vai-e-volta
(o trecho tocado para frente e para trás) até MIN s; depois da edição usa-se só a duração original."""
import json
import subprocess
from pathlib import Path

W = Path(__file__).parent
SRC = W / "parte1_up.mp4"
MIN = 3.2
TAKES = {2: (13.700, 16.300), 3: (21.467, 26.067), 4: (26.067, 27.233),
         5: (37.600, 38.933), 6: (48.467, 50.167), 7: (50.167, 50.700)}
info = {}
for n, (a, b) in TAKES.items():
    d = b - a
    out = W / "flora" / f"take{n}.mp4"
    if d >= MIN:
        vf = "null"
    else:
        reps = int(MIN // (2 * d)) + 1
        parts = "".join(f"[f{i}][r{i}]" for i in range(reps))
        split = f"split={reps}" + "".join(f"[s{i}]" for i in range(reps))
        chains = ";".join(f"[s{i}]split[f{i}][x{i}];[x{i}]reverse[r{i}]" for i in range(reps))
        vf = f"{split};{chains};{parts}concat=n={2 * reps}:v=1:a=0,trim=0:{MIN},setpts=PTS-STARTPTS"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(SRC), "-an",
                    "-filter_complex" if vf != "null" else "-vf", vf, "-c:v", "libx264", "-crf", "16",
                    "-pix_fmt", "yuv420p", str(out)], check=True)
    info[n] = {"ini": a, "fim": b, "dur": round(d, 3), "estendido": d < MIN}
    print(n, info[n])
json.dump(info, open(W / "flora" / "takes.json", "w"), indent=1)
