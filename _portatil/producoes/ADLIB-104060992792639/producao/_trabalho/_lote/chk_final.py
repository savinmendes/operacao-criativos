# -*- coding: utf-8 -*-
"""Recorta do vídeo FINAL os trechos de lipsync para o revisar_ad.py --lipsync / checar_lipsync.py.
Uso (na pasta adNN): python chk_final.py final.mp4 base_limpa.mp4 original.mp4 narracao_es.wav trechos.json saida_dir
trechos.json: [{"nome", "q0", "q1", "rosto": [x, y, w, h] ou null}]
Gera saida_dir/full_<nome>.mp4 (vídeo final + ES), es_<nome>.mp3, orig_<nome>.mp4 (base limpa + PT) e imprime o argumento --lipsync."""
import sys, json, subprocess
from pathlib import Path
fin, base, orig, narr, tj, out = sys.argv[1:7]
O = Path(out); O.mkdir(parents=True, exist_ok=True); args = []
fim = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",fin]))
for t in json.load(open(tj, encoding="utf-8")):
    q0, q1 = t["q0"], t["q1"]; t0 = q0 / 30; t1 = min((q1 + 1) / 30, fim - 0.35)   # sem o fade final
    sel = r"select='between(t\,%.4f\,%.4f)',setpts=PTS-STARTPTS" % (t0, t1 - 0.001)
    n = t["nome"]
    subprocess.run(["ffmpeg","-v","error","-y","-i",fin,"-i",narr,"-filter_complex",f"[0:v]{sel}[v];[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]",
        "-map","[v]","-map","[a]","-r","30","-c:v","libx264","-crf","14","-c:a","aac",str(O / f"full_{n}.mp4")], check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",base,"-i",orig,"-filter_complex",f"[0:v]{sel}[v];[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]",
        "-map","[v]","-map","[a]","-r","30","-c:v","libx264","-crf","16","-c:a","aac",str(O / f"orig_{n}.mp4")], check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",narr,"-af",f"atrim={t0}:{t1},asetpts=PTS-STARTPTS","-ac","1","-c:a","libmp3lame","-b:a","192k",str(O / f"es_{n}.mp3")], check=True)
    a = f"{(O / f'full_{n}.mp4').resolve()}:{(O / f'es_{n}.mp3').resolve()}:{(O / f'orig_{n}.mp4').resolve()}"
    if t.get("rosto"): a += ":" + ";".join(str(int(v)) for v in t["rosto"])
    args.append(a)
(O / "lipsync_arg.txt").write_text(",".join(args), encoding="utf-8"); print(len(args), "trechos ->", O / "lipsync_arg.txt")
