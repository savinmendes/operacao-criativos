"""corpo_adNN.mp4 = base_lipsync.mp4 (24 fps) + audio_corpo.wav, cortado em DUR (tempos_reais.json). Uso: python montar_corpo.py AD_DIR NN"""
import json, subprocess, sys, os
AD, NN = sys.argv[1], sys.argv[2]
fim = json.load(open(os.path.join(AD, "tempos_reais.json")))["dur"]
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
subprocess.run(["ffmpeg","-v","error","-y","-i",os.path.join(AD,"base_lipsync.mp4"),"-i",os.path.join(AD,"audio_corpo.wav"),"-filter_complex",
    f"[0:v]trim=0:{fim},setpts=PTS-STARTPTS[v];[1:a]atrim=0:{fim},asetpts=PTS-STARTPTS[a]",
    "-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-preset","medium","-threads","4","-pix_fmt","yuv420p",*COR,
    "-c:a","aac","-b:a","192k","-ar","48000",os.path.join(AD,f"corpo_ad{NN}.mp4")], check=True)
print("ok corpo", fim)
