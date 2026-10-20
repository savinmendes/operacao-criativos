import json,subprocess,numpy as np,cv2
V=r'C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\06_ADS-6\SB-IT-ADS-6.mp4'
B=json.load(open('blocos.json',encoding='utf8'))
seen={};
for s,e,t in B:
    if t not in seen: seen[t]=[s,e]
    else: seen[t][1]=e
items=sorted(seen.items(),key=lambda x:x[1][0])
def frame(t):
    b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i',V,'-frames:v','1','-vf','crop=1080:320:0:1340','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(320,1080,3).copy()
tiles=[]
for t,(s,e) in items:
    im=frame((s+e)/2)
    im=cv2.resize(im,(540,160))
    cv2.putText(im,f'{(s+e)/2:.1f}',(4,18),cv2.FONT_HERSHEY_SIMPLEX,0.55,(0,0,255),2)
    tiles.append(im)
n=40
for k in range(0,len(tiles),n):
    ch=tiles[k:k+n]
    while len(ch)%4: ch.append(np.zeros_like(tiles[0]))
    rows=[np.hstack(ch[i:i+4]) for i in range(0,len(ch),4)]
    cv2.imwrite(f'leg_{k//n+1}.jpg',np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,80])
print(len(tiles))
