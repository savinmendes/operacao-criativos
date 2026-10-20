# voz IT a -17 LUFS + musica do original (demucs no_vocals) a -32 LUFS
import json, subprocess
T=json.load(open("tempos.json"))["TOTAL"]
subprocess.run(["ffmpeg","-v","error","-y","-i","demucs/no_vocals.wav","-t",str(T),"-af",f"afade=t=out:st={T-1.5}:d=1.5,volume=14.200000000000003dB,aresample=48000","-ac","2","audio/trilha.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/voz_it.wav","-af","loudnorm=I=-17:TP=-2:LRA=11,aresample=48000","-ac","2","audio/voz_n.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/voz_n.wav","-i","audio/trilha.wav","-filter_complex","[0][1]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95","-ar","48000","audio/mix_it.wav"],check=True)
