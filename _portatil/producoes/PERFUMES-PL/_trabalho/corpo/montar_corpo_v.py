import json, subprocess, sys
from comum_pl import palavras
ws = palavras('../audio/corpo_vera.alinhamento.json')
D = 0.057   # atraso da narração dentro do corpo
# (palavra PL, inicio palavra ES, corte ES opcional)
A = [("Teraz", 14.8, 14.80), ("Armaf", 21.86, 21.97), ("Zapach", 38.1, 38.43), ("Afnan.", 41.2, None),
     ("A", 50.12, 50.40), ("Zamów", 54.2, 54.57)]
es = [8.0667]; pl = [0.0]
i = 0
for w in ws:
    if i < len(A) and w[2] == A[i][0]:
        _, ew, cut = A[i]; c = cut if cut else ew
        es.append(c); pl.append(w[0] + D + (c - ew)); i += 1
assert i == len(A), i
fim = ws[-1][1] + D + 0.35
es.append(57.10); pl.append(fim)
seg = []
for k in range(len(es) - 1):
    r = (pl[k+1] - pl[k]) / (es[k+1] - es[k]); seg.append((es[k], es[k+1], r))
    print(f"{es[k]:.2f}-{es[k+1]:.2f} -> {pl[k]:.2f}-{pl[k+1]:.2f}  x{r:.3f}")
fc = []; 
for k, (a, b, r) in enumerate(seg):
    fc.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)*{r:.5f}[v{k}]")
fc.append("".join(f"[v{k}]" for k in range(len(seg))) + f"concat=n={len(seg)}:v=1:a=0,fps=30,trim=duration={fim:.3f}[out]")
json.dump({"D": D, "fim": fim, "es": es, "pl": pl}, open("mapa.json", "w"))
subprocess.run(["ffmpeg","-v","error","-y","-i","../lama/m17_limpo_v2.mp4","-filter_complex",";".join(fc),"-map","[out]",
    "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",
    "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1","corpo_v.mp4"], check=True)
print("fim", fim)
