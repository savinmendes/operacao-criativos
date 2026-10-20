# PL_PF-7 com hook falado: hook = saída do lipsync HeyGen (cor bt601/tv fixa), corpo/selo/legenda iguais ao montar_final.py.
import subprocess, json
T = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\_trabalho"; P = T + r"\pf7hook"
fim = json.load(open(T + r"\corpo\mapa.json"))["fim"]; H = 7.8333
hook = P + r"\out_pf7.mp4"
fc = (f"[0:v]trim=0:{H},setpts=PTS-STARTPTS,fps=30,scale=720:1280:in_color_matrix=bt601:out_color_matrix=bt601:in_range=tv:out_range=tv,format=yuv420p[h];"
      f"[1:v]setpts=PTS-STARTPTS,fps=30,format=yuv420p[c];"
      f"[h][c]concat=n=2:v=1:a=0[v];[v][2:v]overlay=0:0:enable='gte(t\,{H})':format=yuv420[s];[s]ass=leg_pf7_falado.ass:fontsdir=fonts[out]")
subprocess.run(["ffmpeg","-v","error","-y","-reinit_filter","0","-i",hook,"-reinit_filter","0","-i",T + r"\corpo\corpo_v.mp4",
    "-loop","1","-i",T + r"\overlay\selo_pl.png","-i",P + r"\mix_pf7_hook-falado.wav",
    "-filter_complex",fc,"-map","[out]","-map","3:a","-t",f"{H+fim:.3f}",
    "-c:v","libx264","-crf","15","-preset","medium","-profile:v","high","-pix_fmt","yuv420p",
    "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
    "-c:a","aac","-b:a","192k","-ar","48000",P + r"\bruto_pf7_falado.mp4"], check=True)
print("ok")
