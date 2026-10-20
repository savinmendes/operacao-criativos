# entradas HeyGen: video = base limpa (ADS 12 ES, sem legenda) + audio ES original; audio FR separado
import numpy as np, subprocess, json, sys, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
BASE=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\08_ADS-12\_trabalho\lama\base_limpa2.mp4"
CJ=json.load(open("cortes_fr.json")); C,ES,SW=CJ["C"],CJ["ES"],CJ["SW"]
B=list(quadros(BASE)); FPS=30
def enc(frames,out):
    p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-an",*ENC_VF,"-c:v","libx264","-crf","14","-preset","medium",*ENC_TAG,out],stdin=subprocess.PIPE)
    for f in frames: p.stdin.write(np.ascontiguousarray(f).tobytes())
    p.stdin.close(); p.wait()
def blend(x):
    j=int(np.floor(x)); a=x-j; j=min(j,len(B)-1); k=min(j+1,len(B)-1)
    return B[j] if a<0.05 else cv2.addWeighted(B[j],1-a,B[k],a,0)
# A: PiP 0..SW (mesmos quadros do 13.13F) + tela cheia a partir do quadro 175
n1=int(round(SW*FPS)); nA=int(round(C[1]*FPS)); A=[B[i] for i in range(n1)]+[B[175+i] for i in range(nA-n1)]
json.dump({"A_idx":list(range(n1))+[175+i for i in range(nA-n1)]},open("heygen_in/A_idx.json","w"))
enc(A,"heygen_in/A_v.mp4")
t1=n1/FPS; t2=(nA-n1)/FPS
subprocess.run(["ffmpeg","-v","error","-y","-i","es12.mp4","-filter_complex",
  f"[0:a]atrim=0:{t1},asetpts=N/SR/TB[a1];[0:a]atrim={175/FPS}:{175/FPS+t2},asetpts=N/SR/TB[a2];[a1][a2]concat=n=2:v=0:a=1[a]",
  "-map","[a]","-ar","48000","-ac","2","heygen_in/A_es.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","heygen_in/A_v.mp4","-i","heygen_in/A_es.wav","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","heygen_in/A_src.mp4"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/voz_fr.wav","-af",f"atrim=0:{nA/FPS}","-c:a","libmp3lame","-b:a","192k","heygen_in/A_fr.mp3"],check=True)
# F: cena final, 26,1 s do ES em diante, desacelerada para caber a fala FR
nF=int(round((C[6]-C[5])*FPS)); FS=(C[6]-C[5])/(ES[6]-ES[5]-0.02)
F=[blend(783+j/FS) for j in range(nF)]; enc(F,"heygen_in/F_v.mp4")
subprocess.run(["ffmpeg","-v","error","-y","-i","es12.mp4","-af",f"atrim={ES[5]}:{ES[6]},asetpts=N/SR/TB,atempo={1/FS:.5f}","-ar","48000","-ac","2","heygen_in/F_es.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","heygen_in/F_v.mp4","-i","heygen_in/F_es.wav","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","heygen_in/F_src.mp4"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/voz_fr.wav","-af",f"atrim={C[5]}:{C[6]},asetpts=N/SR/TB","-c:a","libmp3lame","-b:a","192k","heygen_in/F_fr.mp3"],check=True)
json.dump({"FS":FS,"nA":nA,"n1":n1,"nF":nF},open("heygen_in/info.json","w")); print("FS",FS,"nA",nA,"n1",n1,"nF",nF)
