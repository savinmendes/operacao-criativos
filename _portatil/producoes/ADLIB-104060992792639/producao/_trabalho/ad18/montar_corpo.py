"""corpo_ad18.mp4 = base_lipsync.mp4 (até FIM) + narracao_es.wav + _audio/demucs/htdemucs/orig/no_vocals.wav (nível original), fade 0,3 s no fim."""
import subprocess
FIM = 100.13
subprocess.run(["ffmpeg","-v","error","-y","-i","base_lipsync.mp4","-i","narracao_es.wav","-i","_audio/demucs/htdemucs/orig/no_vocals.wav","-filter_complex",
    f"[1]aresample=48000,aformat=channel_layouts=stereo[n];[2]aresample=48000,aformat=channel_layouts=stereo[f];"
    f"[n][f]amix=inputs=2:normalize=0:duration=first,atrim=0:{FIM},afade=t=out:st={FIM-0.3}:d=0.3,alimiter=limit=0.95[a];"
    f"[0:v]trim=0:{FIM},setpts=PTS-STARTPTS[v]",
    "-map","[v]","-map","[a]","-r","30","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p",
    "-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",
    "-c:a","aac","-b:a","192k","-ar","48000","corpo_ad18.mp4"],check=True)
print(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","corpo_ad18.mp4"]).decode())
