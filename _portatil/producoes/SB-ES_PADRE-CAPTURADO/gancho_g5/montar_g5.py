# -*- coding: utf-8 -*-
"""Monta gancho_G5.mp4: âncora HeyGen (0–T_INS) + inserto do v4 (4,10–7,45 s) em janela sobre fundo desfocado,
faixa ÚLTIMA HORA, selo VIDEO DE FIELES, legenda palavra a palavra e selo VIDEO FICTICIO."""
import json, subprocess
from pathlib import Path
AQ = Path(__file__).resolve().parent
V4 = r"C:\Users\PICHAU\Downloads\SB-VIDEOS-FICTICIOS\03_GRIMORIO\GRIMORIO V2 - ES COLAR (VIDEO FICTICIO)_v4.mp4"
BED = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\audio\v4\sep\htdemucs\ini10\no_vocals.wav"
SELO = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\visual\overlays\selo_ficticio_mini_es.png"
ANC = AQ / "takes" / "ancora_heygen.mp4"; VOZ = AQ / "audio" / "ancora_v110.mp3"
T_INS, INS_A, INS_B = 6.5833, 4.1333, 7.45  # v4 q.123 (4,10) é quadro solto de transição: começa no 124
DUR = round(T_INS + (INS_B - INS_A), 3)
OUT = AQ / "gancho_G5.mp4"
leg = json.load(open(AQ / "overlays" / "legenda_itens.json", encoding="utf-8"))

ins = ["-i", str(ANC), "-ss", str(INS_A), "-t", str(INS_B - INS_A), "-i", V4, "-i", str(VOZ), "-i", BED,
       "-i", str(AQ / "overlays" / "faixa_ultima_hora.png"), "-i", str(AQ / "overlays" / "selo_video_fieles.png"), "-i", SELO]
for it in leg: ins += ["-i", it["png"]]
f = []
f.append(f"[0:v]fps=30,scale=720:1280,setsar=1,trim=0:{T_INS},setpts=PTS-STARTPTS,format=yuv420p[anc]")
f.append("[1:v]fps=30,setpts=PTS-STARTPTS[i1]")
f.append("[i1]crop=720:912:0:251,split[fg][bgs]")
f.append("[bgs]scale=-2:1280,crop=720:1280,boxblur=24:2,eq=brightness=-0.18:saturation=0.7[bg]")
f.append("[bg][fg]overlay=0:184,format=yuv420p[insv]")
f.append("[anc][insv]concat=n=2:v=1:a=0[base]")
cur = "base"
def ov(idx, a, b, nome):
    global cur
    f.append(f"[{cur}][{idx}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[{nome}]"); cur = nome
ov(4, 0, T_INS - 0.001, "o1")
ov(5, T_INS, DUR, "o2")
for k, it in enumerate(leg):
    a, b = it["ini"], min(it["fim"], DUR)
    if a >= DUR: continue
    ov(7 + k, a, b - 0.001, f"l{k}")
f.append("[6:v]format=rgba,colorchannelmixer=aa=0.10[selo10]")
f.append(f"[{cur}][selo10]overlay=0:0[fin]"); cur = "fin"  # selo VIDEO FICTICIO a 10% de opacidade (pedido 19/10)
# áudio: voz (-15 LUFS) + trilha do v4 (sem voz) sob a âncora + áudio original do inserto a partir de T_INS
f.append(f"[2:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,atrim=0:{T_INS+0.6},asetpts=PTS-STARTPTS[voz]")
f.append(f"[3:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T_INS+0.2},asetpts=PTS-STARTPTS,afade=t=out:st={T_INS-0.05}:d=0.2,volume=1.0[bed]")
f.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.12,afade=t=out:st={INS_B-INS_A-0.12}:d=0.12,adelay={int(T_INS*1000)}|{int(T_INS*1000)}[insa]")
f.append(f"[voz][bed][insa]amix=inputs=3:normalize=0:duration=longest,atrim=0:{DUR},asetpts=PTS-STARTPTS[aout]")
cmd = ["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(f), "-map", f"[{cur}]", "-map", "[aout]",
       "-t", str(DUR), "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
       "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
       "-r", "30", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(OUT)]
subprocess.run(cmd, check=True)
print("ok", OUT, "dur", DUR)
