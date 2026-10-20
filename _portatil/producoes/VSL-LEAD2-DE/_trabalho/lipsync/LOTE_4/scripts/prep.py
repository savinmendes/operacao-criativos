# -*- coding: utf-8 -*-
"""Entradas do lipsync do LOTE 4. Uso: python prep.py [ids...]
in/es_<id>.mp4: video do original (orig_ini..orig_fim) com AUDIO ES original, ambos esticados pelo fator, N quadros
                (N = quadros da timeline nova); L244: so o trecho do pulpito, recortado no rosto e ampliado 2x.
in/de_<id>.mp3: narracao DE da timeline nova (mesmos N quadros)."""
import sys, json, subprocess
from pathlib import Path
L = Path(__file__).resolve().parents[1]; W = L.parents[1]
SRC = r"C:\Users\PICHAU\Downloads\Lead 2.mp4"; NARR = W / "voz" / "narracao_de_completa.wav"
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ESPECIAL = {"L244": {"orig_fim": 2142.5, "crop": [280, 20, 240, 320]}}   # pulpito: rosto pequeno; depois mao no rosto + b-roll
def plano():
    d = json.load(open(W / "voz" / "lotes.json", encoding="utf-8"))
    out = []
    for t in d["trechos"]:
        if t["lote"] != 4: continue
        q0 = round(t["novo_ini"] * 30); q1 = round(t["novo_fim"] * 30); t = dict(t); t["q0"], t["N"] = q0, q1 - q0
        e = ESPECIAL.get(t["id"])
        t["env_orig_fim"] = e["orig_fim"] if e else t["orig_fim"]; t["crop"] = e["crop"] if e else None
        t["envN"] = round((t["env_orig_fim"] - t["orig_ini"]) * t["fator"] * 30) if e else t["N"]
        out.append(t)
    return out
def main():
    so = set(sys.argv[1:]); D = L / "in"; D.mkdir(exist_ok=True)
    P = plano(); json.dump(P, open(L / "plano.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for t in P:
        if so and t["id"] not in so: continue
        i = t["id"]; f = t["fator"]; a0 = t["orig_ini"]; dur_o = t["env_orig_fim"] - a0; n = t["envN"]
        vf = f"setpts=(PTS-STARTPTS)*{f},fps=30,tpad=stop_mode=clone:stop=10"
        if t["crop"]:
            x, y, w, h = t["crop"]; vf += f",crop={w}:{h}:{x}:{y},scale={2*w}:{2*h}:flags=lanczos"
        out = D / f"es_{i}.mp4"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a0:.3f}","-t",f"{dur_o+0.5:.3f}","-i",SRC,
            "-filter_complex",f"[0:v]{vf}[v];[0:a]asetpts=PTS-STARTPTS,atrim=0:{dur_o:.4f},atempo={1/f:.6f},apad,atrim=0:{n/30:.4f}[a]",
            "-map","[v]","-map","[a]","-frames:v",str(n),"-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,
            "-c:a","aac","-b:a","192k","-ar","44100",str(out)], check=True)
        t0 = t["q0"] / 30
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t0:.4f}","-t",f"{n/30:.4f}","-i",str(NARR),"-ac","1",
            "-c:a","libmp3lame","-b:a","192k",str(D / f"de_{i}.mp3")], check=True)
        nq = int(subprocess.check_output(["ffprobe","-v","error","-count_frames","-select_streams","v","-show_entries","stream=nb_read_frames","-of","csv=p=0",str(out)]))
        print(i, "N", n, "quadros", nq, "ok" if nq == n else "DIFERENTE", flush=True)
main()
