import subprocess, sys, json
T = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\_trabalho"; O = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\originais"
fim = json.load(open(T + r"\corpo\mapa.json"))["fim"]
V = {
 "17":  (T + r"\hooks\out_h17.mp4", 8.0667, True),
 "18":  (T + r"\hooks\out_h18.mp4", 8.0667, True),
 "t1":  (O + r"\PF Masc testeLatam(1).mp4", 3.5667, False),
 "t3":  (O + r"\PF Masc testeLatam(3).mp4", 3.5667, False),
 "pf7": (O + r"\PF 7.mp4", 7.8333, False),
}
for k in (sys.argv[1:] or V):
    hook, H, selo_hook = V[k]
    en = "1" if selo_hook else f"gte(t\,{H})"
    fc = (f"[0:v]trim=0:{H},setpts=PTS-STARTPTS,fps=30,format=yuv420p[h];[1:v]setpts=PTS-STARTPTS,fps=30,format=yuv420p[c];"
          f"[h][c]concat=n=2:v=1:a=0[v];[v][2:v]overlay=0:0:enable='{en}':format=yuv420[s];[s]ass=leg_{k}.ass:fontsdir=fonts[out]")
    subprocess.run(["ffmpeg","-v","error","-y","-reinit_filter","0","-i",hook,"-reinit_filter","0","-i",T + r"\corpo\corpo_v.mp4",
        "-loop","1","-i",T + r"\overlay\selo_pl.png","-i",T + rf"\mix\mix_{k}.wav",
        "-filter_complex",fc,"-map","[out]","-map","3:a","-t",f"{H+fim:.3f}",
        "-c:v","libx264","-crf","15","-preset","medium","-profile:v","high","-pix_fmt","yuv420p",
        "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
        "-c:a","aac","-b:a","192k","-ar","48000",f"bruto_{k}.mp4"], check=True)
    print(k, "ok", flush=True)
