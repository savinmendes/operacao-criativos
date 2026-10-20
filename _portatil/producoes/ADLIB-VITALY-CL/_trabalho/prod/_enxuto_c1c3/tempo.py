# -*- coding: utf-8 -*-
"""Acelera narração (atempo) e reescala o alinhamento ElevenLabs.
  python tempo.py narr.mp3 fator saida.mp3"""
import json, subprocess, sys
src, f, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f"atempo={f}", "-c:a", "libmp3lame", "-q:a", "2", out], check=True)
ali = json.load(open(src[:-4] + ".alinhamento.json", encoding="utf-8"))
def esc(a):
    for k in ("character_start_times_seconds", "character_end_times_seconds"):
        a[k] = [t / f for t in a[k]]
for k in ("alignment", "normalized_alignment"):
    if k in ali and ali[k]: esc(ali[k])
if "characters" in ali: esc(ali)
json.dump(ali, open(out[:-4] + ".alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok", out)
