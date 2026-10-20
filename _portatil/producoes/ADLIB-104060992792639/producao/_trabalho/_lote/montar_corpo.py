# -*- coding: utf-8 -*-
"""corpo_adNN.mp4 = base_lipsync.mp4 + narracao_es.wav (no nivel da voz original) + fundo demucs no_vocals (nivel original),
cortado em FIM s com fade de 0,3 s no audio e no video. Uso: python montar_corpo.py NN fim [--sem-fundo]"""
import sys, re, subprocess
nn, fim = sys.argv[1], float(sys.argv[2]); fundo = "--sem-fundo" not in sys.argv
def lufs(f, extra=[]):
    o = subprocess.run(["ffmpeg","-i",f,*extra,"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
dem = "_audio/demucs/htdemucs/orig/"
lv, ln = lufs(dem + "vocals.wav"), lufs("narracao_es.wav")
g = lv - ln; print(f"voz original {lv:.1f} LUFS, narracao {ln:.1f} -> ganho {g:+.1f} dB; fundo {lufs(dem+'no_vocals.wav'):.1f} LUFS")
ins = ["-i","base_lipsync.mp4","-i","narracao_es.wav"] + (["-i", dem + "no_vocals.wav"] if fundo else [])
af = f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.2f}dB[n]"
if fundo: af += f";[2:a]aresample=48000,aformat=channel_layouts=stereo[f];[n][f]amix=inputs=2:normalize=0:duration=first[m]"
else: af += ";[n]anull[m]"
af += f";[m]atrim=0:{fim},afade=t=out:st={fim-0.3:.3f}:d=0.3,alimiter=limit=0.95[a]"
vf = f"[0:v]trim=0:{fim},setpts=PTS-STARTPTS,fade=t=out:st={fim-0.3:.3f}:d=0.3[v]"
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",vf+";"+af,"-map","[v]","-map","[a]","-threads","4",
    "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p","-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",
    "-c:a","aac","-b:a","192k","-ar","48000",f"corpo_ad{nn}.mp4"],check=True)
print("ok", f"corpo_ad{nn}.mp4", lufs(f"corpo_ad{nn}.mp4"), "LUFS")
