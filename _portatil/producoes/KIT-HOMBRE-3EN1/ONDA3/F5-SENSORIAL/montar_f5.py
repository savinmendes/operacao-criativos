# -*- coding: utf-8 -*-
"""Monta o F5 Sensorial (sem fala): takes Kling + unboxing + pack, textos PNG, trilha + SFX. 720x1280 30 fps."""
import subprocess, sys
from pathlib import Path
P = Path(__file__).parent
T, AU, TX, WK = P / "takes", P / "audio", P / "txt", P / "_seg"
UB = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PROD1-EL-MAESTRO\unbox")
SELO = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\LOTE-15-10\_trabalho\A\overlay_selo.png")
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30,format=yuv420p"
ZOOM = "scale=1440:2560,zoompan=z='max(1.0,1.035-0.00016*on)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
K1 = sys.argv[1] if len(sys.argv) > 1 else str(T / "K1_armaf.mp4")
K2 = sys.argv[2] if len(sys.argv) > 2 else str(T / "K2_asad.mp4")
K3 = sys.argv[3] if len(sys.argv) > 3 else str(T / "K3_9pm.mp4")
I4 = P / "cenas" / "I4_pack.png"

# (arquivo, ss, dur, vf_extra, selo?)
PLANOS = [
    (K1, 1.0, 2.5, None, True),                 # 0.0  gancho: borrifada Armaf (a névoa sai da tampa ~0,5 s)
    (UB / "armaf_limpo.mp4", 0.0, 2.0, None, False),  # 2.5
    (K1, 3.5, 1.5, None, True),                 # 4.5  (continuação do mesmo take, sem repetir)
    (K2, 0.0, 3.5, None, True),                 # 6.0  Asad luz dourada
    (UB / "asad_limpo.mp4", 0.0, 2.2, None, False),   # 9.5
    (K3, 0.0, 3.5, None, True),                 # 11.7 9PM fumaça
    (UB / "9pm_limpo.mp4", 0.3, 2.6, None, False),    # 15.2
    (I4, 0.0, 7.4, ZOOM, True),                 # 17.8 pack luz dourada + oferta/CTA -> 25.2
]
TXT = [("t00_gancho", 0.0, 2.5),
       ("t_armaf_0", 2.5, 3.2), ("t_armaf_1", 3.2, 3.9), ("t_armaf_2", 3.9, 4.6), ("t_armaf_3", 4.6, 6.0),
       ("t_asad_0", 6.0, 6.8), ("t_asad_1", 6.8, 7.6), ("t_asad_2", 7.6, 8.4), ("t_asad_3", 8.4, 11.7),
       ("t_9pm_0", 11.7, 12.5), ("t_9pm_1", 12.5, 13.3), ("t_9pm_2", 13.3, 14.1), ("t_9pm_3", 14.1, 17.8),
       ("t90_oferta", 17.8, 20.6), ("t91_cta", 20.6, 25.2)]
SFX = [("sfx_borrifada", 0.4, 1.0), ("sfx_whoosh", 5.85, 0.55), ("sfx_whoosh", 11.55, 0.55),
       ("sfx_borrifada", 17.65, 0.8), ("sfx_whoosh", 20.5, 0.45)]
DUR = sum(p[2] for p in PLANOS)

def run(c): subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)

ins, fc = [], []
for i, (f, ss, d, vx, selo) in enumerate(PLANOS):
    if str(f).endswith(".png"):
        ins += ["-loop", "1", "-framerate", "30", "-t", str(d), "-i", str(f)]
    else:
        ins += ["-ss", str(ss), "-t", str(d), "-i", str(f)]
    chain = (vx + ",setsar=1,format=yuv420p") if vx else BASE
    fc.append(f"[{i}:v]{chain},trim=duration={d},setpts=PTS-STARTPTS[p{i}]")
n = len(PLANOS)
k = n
ins += ["-loop", "1", "-i", str(SELO)]; selo_i = k; k += 1
# selo por plano
t0 = 0.0; en = []
for i, (_, _, d, _, selo) in enumerate(PLANOS):
    en.append((t0, t0 + d, selo)); t0 += d
fc.append("".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v0]")
expr = "+".join(f"between(t,{a:.3f},{b - 0.001:.3f})" for a, b, s in en if s)
fc.append(f"[v0][{selo_i}:v]overlay=0:0:enable='{expr}':shortest=0:eof_action=pass[vs]")
last = "vs"
for j, (png, a, b) in enumerate(TXT):
    ins += ["-loop", "1", "-i", str(TX / f"{png}.png")]
    fc.append(f"[{last}][{k}:v]overlay=0:0:enable='between(t,{a},{b - 0.001})'[t{j}]"); last = f"t{j}"; k += 1
# setas do CTA (pulsando) abaixo do texto de pagamento
ins += ["-loop", "1", "-i", str(TX / "seta.png")]
fc.append(f"[{k}:v]split=3[s1][s2][s3]")
for q, x in enumerate([150, 302, 454]):
    fc.append(f"[{last}][s{q + 1}]overlay=x={x}:y='1125+10*sin(2*PI*2*t)':enable='between(t,21.2,{DUR})'[sa{q}]"); last = f"sa{q}"
k += 1
fc.append(f"[{last}]trim=duration={DUR},format=yuv420p[vout]")
# áudio: trilha + sfx
ins += ["-i", str(AU / "trilha.mp3")]; ti = k; k += 1
fc.append(f"[{ti}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{DUR},afade=t=out:st={DUR - 1.2}:d=1.2,volume=0.9[mus]")
al = ["[mus]"]
for j, (nome, at, vol) in enumerate(SFX):
    ins += ["-i", str(AU / f"{nome}.mp3")]
    ms = int(at * 1000)
    fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[x{j}]"); al.append(f"[x{j}]"); k += 1
fc.append("".join(al) + f"amix=inputs={len(al)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,atrim=0:{DUR}[aout]")
out = P / "_bruto.mp4"
run([*ins, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", str(DUR),
     "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
     "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(out)])
print("ok", round(DUR, 2), out)
