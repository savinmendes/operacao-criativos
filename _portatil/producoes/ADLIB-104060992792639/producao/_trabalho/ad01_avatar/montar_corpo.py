"""corpo_avatar.mp4 = heygen_avatar.mp4 (imagem) + narracao_es (copia do ad01) + fundo.wav (musica do original),
cortado 0,7 s depois da ultima fala, fade 0,3 s."""
import json, subprocess
a = json.load(open("narracao_es.alinhamento.json", encoding="utf-8"))
fim = round(a["character_end_times_seconds"][-1] + 0.7, 3)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
subprocess.run(["ffmpeg","-v","error","-y","-i","heygen_avatar.mp4","-i","narracao_es_full.wav","-i","fundo.wav","-filter_complex",
    f"[0:v]scale=720:1280:flags=lanczos,fps=30,tpad=stop_mode=clone:stop_duration=2,trim=0:{fim},setpts=PTS-STARTPTS[v];"
    f"[1:a]aformat=channel_layouts=stereo,atrim=0:{fim}[n];[2:a]aformat=channel_layouts=stereo,atrim=0:{fim}[f];"
    f"[n][f]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95,afade=t=out:st={fim-0.3}:d=0.3,asetpts=PTS-STARTPTS[a]",
    "-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,
    "-c:a","aac","-b:a","192k","-ar","48000","corpo_avatar.mp4"], check=True)
print("ok corpo", fim)
