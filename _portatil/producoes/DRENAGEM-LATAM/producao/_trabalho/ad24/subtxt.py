# Reescreve o texto dentro das caixas brancas da legenda queimada (mantém as caixas), num intervalo.
import cv2,numpy as np,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
ent,sai,de,ate=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4]); linhas=sys.argv[5].split("|")
FONT=r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Medium.ttf"
Y0,Y1=860,1120
cap=cv2.VideoCapture(ent); W,H=int(cap.get(3)),int(cap.get(4))
p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-i",ent,"-map","0:v","-map","1:a","-c:v","libx264","-crf","14","-pix_fmt","yuv420p","-c:a","copy",sai],stdin=subprocess.PIPE)
n=0
while True:
    ok,f=cap.read()
    if not ok: break
    if de*30-0.5<=n<ate*30-0.5:
        boxes=[(89,918,630,978),(128,978,591,1026)]
        f[921:976,93:626]=255; f[970:1023,132:587]=255
        img=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(img); fnt=ImageFont.truetype(FONT,44)
        for (x0,y0,x1,y1),txt in zip(boxes,linhas):
            bb=fnt.getbbox(txt); tw=fnt.getlength(txt)
            d.text(((x0+x1)/2-tw/2,(y0+y1)/2-(bb[1]+bb[3])/2-2),txt,font=fnt,fill=(0,0,0))
        f=cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
    p.stdin.write(f.tobytes()); n+=1
p.stdin.close(); p.wait(); print("ok")
