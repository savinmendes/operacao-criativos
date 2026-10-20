# Trilha: demucs no_vocals do ES re-temporizado (cena 1: 5,067->5,6 s; cena 7: 5,4->6,5 s) a -32 LUFS + voz PL a -16 LUFS
import subprocess
B="demucs/no_vocals.wav"; T=33.133
fc=("[0:a]atrim=0:5.067,asetpts=PTS-STARTPTS,atempo=0.904821[a];"
    "[0:a]atrim=5.067:26.1,asetpts=PTS-STARTPTS[b];"
    "[0:a]atrim=26.1,asetpts=PTS-STARTPTS,atempo=0.830769[c];"
    f"[a][b][c]concat=n=3:v=0:a=1,aresample=48000,loudnorm=I=-32:TP=-6:LRA=11,apad,atrim=0:{T}[bed];"
    f"[1:a]aresample=48000,loudnorm=I=-16:TP=-2:LRA=11,apad,atrim=0:{T}[v];"
    "[v][bed]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95,aformat=sample_rates=48000:channel_layouts=stereo[o]")
subprocess.run(["ffmpeg","-v","error","-y","-i",B,"-i","audio/voz_pl.wav","-filter_complex",fc,"-map","[o]","-t",str(T),"audio/mix_pl.wav"],check=True)
print("ok")
