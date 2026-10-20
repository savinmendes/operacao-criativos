# -*- coding: utf-8 -*-
"""Abertura H2 (Onda 3, Parte B): troca SÓ o bloco 1 do corpo desta persona.
Lê h2.json da pasta: {"take": "takes/H2_gancho.mp4", "ss": 0.0, "dur": 4.0,
  "palavras": [["texto", ini, fim], ...] (tempo do take), "gancho_antigo": 4.1}
Gera _seg_h2/01_gancho_h2.mp4, concatena (cópia sem reencode) com _seg/02..07 já existentes
(os mesmos do corpo.mp4 original) -> corpo_h2.mp4 + corpo_h2.alinhamento.json.
Não sobrescreve nenhum arquivo do vídeo original."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
SELO = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\LOTE-15-10\_trabalho\A\overlay_selo.png")  # só leitura
WK = P / "_seg_h2"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
H = json.load(open(P / "h2.json", encoding="utf-8"))
ss, dur, old = float(H["ss"]), float(H["dur"]), float(H["gancho_antigo"])


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


# 1) bloco 1 novo: take Seedance com a fala nativa + selo de pagamento na entrega
b1 = WK / "01_gancho_h2.mp4"
fc = (f"[0:v]{BASE},trim=duration={dur},setpts=PTS-STARTPTS[v0];[v0][1:v]overlay=0:0:shortest=1[vc];"
      f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo[a0];"
      f"[a0][3:a]amix=inputs=2:normalize=0:duration=longest,atrim=duration={dur}[ao]")
run(["-ss", str(ss), "-t", str(dur), "-i", str(P / H["take"]),
     "-loop", "1", "-t", str(dur), "-i", str(SELO),
     "-ss", str(ss), "-t", str(dur), "-i", str(P / H["take"]),
     "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo",
     "-filter_complex", fc, "-map", "[vc]", "-map", "[ao]", "-t", str(dur), *ENC, str(b1)])

# 2) concat com os blocos 2..7 originais (idênticos)
orig = [l.split("'")[1] for l in (P / "_seg" / "lista.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
assert Path(orig[0]).name.startswith("01_"), orig[0]
lst = WK / "lista_h2.txt"
lst.write_text("".join(f"file '{s}'\n" for s in [b1.as_posix(), *orig[1:]]), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo_h2.mp4")])

# 3) alinhamento: palavras novas + alinhamento original a partir do fim do gancho antigo, deslocado
A = json.load(open(P / "corpo.alinhamento.json", encoding="utf-8"))
N = {"characters": [], "character_start_times_seconds": [], "character_end_times_seconds": []}
pal = [(w, a - ss, b - ss) for w, a, b in H["palavras"]]
for i, (w, a, b) in enumerate(pal):
    step = (b - a) / max(len(w), 1)
    for c_i, ch in enumerate(w + " "):
        st = a + min(c_i, len(w)) * step
        N["characters"].append(ch); N["character_start_times_seconds"].append(round(st, 3))
        N["character_end_times_seconds"].append(round(st + step, 3))
d = dur - old
for ch, a, b in zip(A["characters"], A["character_start_times_seconds"], A["character_end_times_seconds"]):
    if a >= old - 0.01:
        N["characters"].append(ch); N["character_start_times_seconds"].append(round(a + d, 3))
        N["character_end_times_seconds"].append(round(b + d, 3))
json.dump(N, open(P / "corpo_h2.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("delta", round(d, 2)); print("".join(N["characters"]))
