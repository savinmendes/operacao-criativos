# -*- coding: utf-8 -*-
"""Troca o bloco 1 (gancho) de um AD de persona por um gancho novo, mantendo os blocos 2..N idênticos.
Uso: python montar_h2.py config.json
config: {"pasta", "take", "ss", "dur", "palavras": [[w, ini, fim] em tempo do take], "manchete", "manchete_y",
         "chaves_extra": [...], "sufixo": "H2", "nome": "PERFUMES-CL_P1_EL-MAESTRO"}
Não sobrescreve nada que já existe: escreve _seg_h2/, corpo_h2.mp4, corpo_h2.alinhamento.json, receita_h2.json."""
import json, subprocess, sys
from pathlib import Path

cfg = json.load(open(sys.argv[1], encoding="utf-8"))
P = Path(cfg["pasta"])
SELO = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\LOTE-15-10\_trabalho\A\overlay_selo.png")
WK = P / "_seg_h2"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
suf = cfg.get("sufixo", "H2").lower()


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))


ss, d = cfg["ss"], cfg["dur"]
g1 = WK / "01_gancho.mp4"
run(["-ss", str(ss), "-t", str(d), "-i", cfg["take"], "-loop", "1", "-framerate", "30", "-i", str(SELO),
     "-f", "lavfi", "-t", str(d), "-i", "anullsrc=r=48000:cl=stereo",
     "-filter_complex",
     f"[0:v]{BASE},trim=duration={d},setpts=PTS-STARTPTS[v0];[v0][1:v]overlay=0:0:shortest=1[vo];"
     f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[a0];"
     f"[a0][2:a]amix=inputs=2:normalize=0:duration=longest,atrim=duration={d}[ao]",
     "-map", "[vo]", "-map", "[ao]", "-t", str(d), *ENC, str(g1)])

velhos = [l.split("'")[1] for l in (P / "_seg" / "lista.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
d_old = dur(velhos[0])
d_new = dur(g1)
lst = WK / "lista.txt"
lst.write_text("".join(f"file '{Path(s).as_posix()}'\n" for s in [g1.as_posix()] + velhos[1:]), encoding="utf-8")
corpo = P / f"corpo_{suf}.mp4"
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(corpo)])

# alinhamento: palavras novas + alinhamento antigo a partir do fim do bloco 1, deslocado
old = json.load(open(P / "corpo.alinhamento.json", encoding="utf-8"))
A = {"characters": [], "character_start_times_seconds": [], "character_end_times_seconds": []}
pal = [(w, a - ss, b - ss) for w, a, b in cfg["palavras"]]
for w, a, b in pal:
    s = w + " "
    step = (b - a) / max(len(w), 1)
    for ci, ch in enumerate(s):
        st = a + min(ci, len(w)) * step
        A["characters"].append(ch); A["character_start_times_seconds"].append(round(st, 3))
        A["character_end_times_seconds"].append(round(st + step, 3))
delta = d_new - d_old
for ch, a, b in zip(old["characters"], old["character_start_times_seconds"], old["character_end_times_seconds"]):
    if a < d_old - 0.01:
        continue
    A["characters"].append(ch); A["character_start_times_seconds"].append(round(a + delta, 3))
    A["character_end_times_seconds"].append(round(b + delta, 3))
alin = P / f"corpo_{suf}.alinhamento.json"
json.dump(A, open(alin, "w", encoding="utf-8"), ensure_ascii=False)

r = json.load(open(P / "receita.json", encoding="utf-8"))
nome = cfg["nome"]
r["saida"] = (P / f"{nome}_{cfg.get('sufixo', 'H2')}.mp4").as_posix()
r["corpo"] = corpo.as_posix()
r["legenda"]["fonte"] = "alinhamento:" + alin.as_posix()
r["legenda"]["chaves"] = cfg.get("chaves_extra", []) + [c for c in r["legenda"]["chaves"]][cfg.get("pular_chaves", 0):]
r["manchete"] = {"texto": cfg["manchete"], "y": cfg["manchete_y"], "ate": round(d_new, 2)}
json.dump(r, open(P / f"receita_{suf}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("bloco1 antigo", d_old, "novo", d_new, "corpo", dur(corpo))
print("".join(A["characters"])[:200])
