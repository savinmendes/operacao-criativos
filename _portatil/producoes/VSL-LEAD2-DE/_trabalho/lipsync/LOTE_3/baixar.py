# -*- coding: utf-8 -*-
"""Baixa as saidas do HeyGen (jobs.json {id: job_id}) para heygen/<id>.mp4 assim que ficam prontas e roda colar.py
em cada uma. Para quando todas baixaram ou apos ~90 min. Uso: python baixar.py"""
import json, subprocess, sys, time
from pathlib import Path
W = Path(__file__).resolve().parent
(W / "heygen").mkdir(exist_ok=True)
t0 = time.time()
while time.time() - t0 < 90 * 60:
    jobs = json.load(open(W / "jobs.json"))
    falta = 0
    for i, j in sorted(jobs.items()):
        dst = W / "heygen" / f"{i}.mp4"
        if dst.exists():
            continue
        tmp = dst.with_suffix(".tmp")
        code = subprocess.run(["curl", "-s", "-L", "-o", str(tmp), "-w", "%{http_code}",
                               f"https://resource2.heygen.ai/video_translate/{j}/original.mp4"],
                              capture_output=True, text=True).stdout
        ok = code == "200" and subprocess.run(["ffprobe", "-v", "error", str(tmp)]).returncode == 0
        if ok:
            tmp.replace(dst)
            print(i, "baixado", flush=True)
            subprocess.run([sys.executable, str(W / "colar.py"), i])
        else:
            tmp.unlink(missing_ok=True); falta += 1
    print(f"[{len(jobs) - falta}/{len(jobs)}] prontos, {int((time.time() - t0) / 60)} min", flush=True)
    if falta == 0:
        break
    time.sleep(60)
print("FIM", flush=True)
