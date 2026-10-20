# entradas do lipsync: video (com audio ES original) + mp3 EN separado. hook = recorte 9:16 só do Jesus (PIP)
import subprocess, numpy as np, cv2, json
from comum3 import quadros, ENC_VF, ENC_TAG
FPS=30
SEG={"hook":(0,152,(340,520,380,676)),"jb":(152,300,None),"cta":(783,945,None)}  # quadros [q0,q1)
json.dump(SEG,open("heygen_in/seg.json","w"))
for nm,(q0,q1,cx) in SEG.items():
    enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        "-ss",f"{q0/FPS:.4f}","-t",f"{(q1-q0)/FPS:.4f}","-i","fontes/es.mp4","-map","0:v","-map","1:a",*ENC_VF,"-c:v","libx264","-crf","14",
        "-preset","medium",*ENC_TAG,"-c:a","aac","-b:a","192k","-shortest",f"heygen_in/{nm}_src.mp4"],stdin=subprocess.PIPE)
    for f in quadros("fontes/es.mp4",q0,q1-q0):
        if cx:
            x,y,w,h=cx; f=cv2.resize(f[y:y+h,x:x+w],(720,1280),interpolation=cv2.INTER_LANCZOS4)
        enc.stdin.write(f.tobytes())
    enc.stdin.close(); enc.wait()
    print(nm, subprocess.run(["ffprobe","-v","error","-count_frames","-show_entries","stream=nb_read_frames,duration","-of","csv=p=0",f"heygen_in/{nm}_src.mp4"],capture_output=True,text=True).stdout.split())
