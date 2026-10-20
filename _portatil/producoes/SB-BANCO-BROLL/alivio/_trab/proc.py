# uso: python proc.py NN nome "url"  -> baixa, normaliza 720x1280 30fps CRF22 bt601, apaga bruto, gera folha 4 quadros
import sys, subprocess, urllib.request, os
nn, nome, url = sys.argv[1], sys.argv[2], sys.argv[3]
base = r"C:\Users\PICHAU\Downloads\SB-BANCO-BROLL\alivio"
trab = os.path.join(base, "_trab")
bruto = os.path.join(trab, f"bruto_{nn}.mp4")
out = os.path.join(base, f"alivio_{nn}_{nome}.mp4")
urllib.request.urlretrieve(url, bruto)
vf = ("scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,"
      "scale=out_color_matrix=bt601:out_range=tv,format=yuv420p")
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",bruto,"-an","-vf",vf,"-c:v","libx264","-crf","22","-preset","medium",
                "-colorspace","smpte170m","-color_primaries","smpte170m","-color_trc","smpte170m","-color_range","tv",
                "-movflags","+faststart",out],check=True)
os.remove(bruto)
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],capture_output=True,text=True).stdout)
ts = [0, 1.5, 3.0, min(4.8, dur-0.1)]
folha = os.path.join(trab, f"qa_{nn}.jpg")
ins=[]; 
for t in ts: ins += ["-ss",str(t),"-i",out]
fc = "".join(f"[{i}:v]trim=end_frame=1,scale=270:480[v{i}];" for i in range(4)) + "[v0][v1][v2][v3]hstack=4"
subprocess.run(["ffmpeg","-y","-loglevel","error",*ins,"-filter_complex",fc,"-frames:v","1","-q:v","4",folha],check=True)
print(nn, out, round(dur,2), os.path.getsize(out)//1024, "KB")
