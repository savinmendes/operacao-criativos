import json, subprocess, os
from mapa import en2es
os.makedirs("heygen_in",exist_ok=True)
for n,a,b in json.load(open("chunks.json")):
    d=b-a; s=en2es(a)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.4f}","-i","base_en_v1.mp4","-ss",f"{max(0,s):.4f}","-i","es_st.wav",
      "-map","0:v","-map","1:a","-frames:v",str(round(d*30)),"-t",f"{d:.4f}","-c:v","libx264","-crf","14","-preset","fast",
      "-c:a","aac","-b:a","192k","-af","apad","-shortest","heygen_in/"+n+".mp4"],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.4f}","-t",f"{d:.4f}","-i","audio/voz_raw.wav","-c:a","libmp3lame","-b:a","192k","heygen_in/"+n+"_en.mp3"],check=True)
    print(n, round(d,2))
