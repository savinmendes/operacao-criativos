# -*- coding: utf-8 -*-
"""Entradas do HeyGen por cena com lipsync: lipsync/in/c<KK>.mp4 (vídeo da cena [ou recorte no rosto] + ÁUDIO PT ORIGINAL)
e lipsync/in/c<KK>_es.mp3 (só a voz do personagem no intervalo da cena). Uso: python prep_ls.py"""
import json, subprocess
from pathlib import Path
import plano
AQ = Path(__file__).resolve().parent; L = AQ / "lipsync" / "in"; SRC = r"C:\Users\PICHAU\Downloads\TESTE1.mp4"
QUEM = {"react": "mujer", "rep": "reportera", "aurA": "aurelio", "aurBC": "aurelio", "aurBC2": "aurelio"}
import sys
REUSO = json.load(open(AQ / "lipsync" / "mapa_reuso.json"))
only = sys.argv[1:]
CROP = {"react": (0, 470, 360, 640), "aurC": (300, 200, 420, 746)}   # x, y, w, h (9:16)
def run(c): subprocess.run(c, check=True)
info = {}
for k, c in enumerate(plano.segmentos()):
    if not c.get("ls"): continue
    p0 = c["pecas"][0]["nome"]; quem = QUEM.get(p0, "sacerdote"); nome = f"s{k:02d}"
    info[nome] = dict(k=k, quem=quem, q0=c["q0"], n=c["n"], crop=c.get("crop"), desc=c["desc"])
    if nome in REUSO or (only and nome not in only): continue
    dur = c["n"] / 30; cena = AQ / "mont" / f"cena_{k:02d}.mp4"
    # áudio PT original das peças (esticado pela vel da cena)
    ins, fc = [], []
    for j, p in enumerate(c["pecas"]):
        ins += ["-ss", f"{p['a']:.3f}", "-t", f"{p['b'] - p['a']:.3f}", "-i", SRC]
        fc.append(f"[{j}:a]aresample=48000,atempo={max(0.5, c['vel']):.4f},atrim=end={p['n'] / 30:.4f},asetpts=PTS-STARTPTS[a{j}]")
    fc.append("".join(f"[a{j}]" for j in range(len(c["pecas"]))) + f"concat=n={len(c['pecas'])}:v=0:a=1[a]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[a]", "-ac", "2", str(L / f"{nome}_pt.wav")])
    vf = []
    if c.get("crop"):
        x, y, w, h = c["crop"]; vf = ["-vf", f"crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos"]
    run(["ffmpeg", "-v", "error", "-y", "-i", str(cena), "-i", str(L / f"{nome}_pt.wav"), *vf, "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", str(L / f"{nome}.mp4")])
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['q0'] / 30:.4f}", "-t", f"{dur:.4f}", "-i", str(AQ / "voz" / f"trilha_{quem}.wav"),
         "-c:a", "libmp3lame", "-b:a", "192k", str(L / f"{nome}_es.mp3")])
    print(nome, quem, f"{dur:.2f}s", c["desc"], flush=True)
json.dump(info, open(AQ / "lipsync" / "jobs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
