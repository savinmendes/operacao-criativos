# v2: audio ES esticado (atempo) no mesmo fator do video -> boca original sincronizada com a fala ES da entrada
import json, subprocess, os
from mapa import en2es
os.makedirs("heygen_in2",exist_ok=True)
for n,a,b in json.load(open("chunks.json")):
    d=b-a; s0=en2es(a); s1=en2es(b); f=(s1-s0)/d; nf=round(d*30)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.4f}","-i","base_en_v1.mp4","-ss",f"{s0:.4f}","-t",f"{s1-s0:.4f}","-i","es_st.wav",
      "-map","0:v","-map","1:a","-frames:v",str(nf),"-af",f"atempo={f:.5f},apad","-t",f"{d:.4f}","-c:v","libx264","-crf","14","-preset","fast",
      "-c:a","aac","-b:a","192k","heygen_in2/"+n+".mp4"],check=True)
    subprocess.run(["cp","heygen_in/"+n+"_en.mp3","heygen_in2/"+n+"_en.mp3"])
    print(n, round(d,2), "fator", round(f,3))
