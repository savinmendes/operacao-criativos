"""corpo_ad07.mp4 = base_lipsync.mp4 (24 fps) + narracao_es.wav + fundo (demucs no_vocals), cortado 0,7 s depois da última fala, fade 0,3 s."""
import json, subprocess
t = json.load(open("_audio/tempos_reais.json", encoding="utf-8"))
fim = round(t[-1]["fim"] + 0.7, 3)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
subprocess.run(["ffmpeg","-v","error","-y","-i","base_lipsync.mp4","-i","narracao_es.wav","-i","_audio/demucs/htdemucs/orig/no_vocals.wav","-filter_complex",
    f"[0:v]trim=0:{fim},setpts=PTS-STARTPTS[v];"
    f"[1:a]aformat=channel_layouts=stereo,atrim=0:{fim}[n];[2:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{fim}[f];"
    f"[n][f]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95,afade=t=out:st={fim-0.3}:d=0.3,asetpts=PTS-STARTPTS[a]",
    "-map","[v]","-map","[a]","-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,
    "-c:a","aac","-b:a","192k","-ar","48000","corpo_ad07.mp4"], check=True)
print("ok corpo", fim)
