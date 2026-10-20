# Trilha: demucs no_vocals do ES re-temporizado (cena 1 e 7 alongadas como o video) a -32 LUFS + voz IT a -16 LUFS
import subprocess
B="demucs/no_vocals.wav"
fc=("[0:a]atrim=0:5.067,asetpts=PTS-STARTPTS,atempo=0.926834[a];"
    "[0:a]atrim=5.067:26.1,asetpts=PTS-STARTPTS[b];"
    "[0:a]atrim=26.1,asetpts=PTS-STARTPTS,atempo=0.885246[c];"
    "[a][b][c]concat=n=3:v=0:a=1,aresample=48000,loudnorm=I=-32:TP=-6:LRA=11,apad,atrim=0:32.6[bed];"
    "[1:a]aresample=48000,loudnorm=I=-16:TP=-2:LRA=11,apad,atrim=0:32.6[v];"
    "[v][bed]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95,aformat=sample_rates=48000:channel_layouts=stereo[o]")
subprocess.run(["ffmpeg","-v","error","-y","-i",B,"-i","audio/voz_it.wav","-filter_complex",fc,"-map","[o]","-t","32.6","audio/mix_it.wav"],check=True)
print("ok")
