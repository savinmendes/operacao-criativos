# Monta o vídeo IT (sem legenda/áudio): cenas com push-in leve (1.00->1.06) e fusão de 0,2 s, leitura/gravação bt601 fixa
import json,subprocess,numpy as np,cv2,sys
TL=json.load(open('timeline.json')); FPS=30; OW,OH=1080,1920; XF=0.1
O=json.load(open('ls/org.json'))
SRC={'hook':('ls/pt_hook.mp4',O['hook'][0]),'crown1':('ls/pt_crown1.mp4',O['crown1'][0]),'woman':('br23.mp4',None),'key':('br29.mp4',None),
'crown2':('ls/pt_crown2.mp4',O['crown2'][0]),'gate':('br20.mp4',None),'sad':('br07.mp4',None),'crown3':('ls/pt_crown3.mp4',O['crown3'][0]),'door':('br02.mp4',None)}
def info(p):
    o=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height,r_frame_rate','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip().split(',')
    a,b=o[2].split('/'); return int(o[0]),int(o[1]),int(a)/int(b)
class Rd:
    def __init__(s,p):
        s.w,s.h,s.fps=info(p); s.k=-1; s.f=None
        s.pr=subprocess.Popen(['ffmpeg','-v','error','-i',p,'-vf','scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24','-fps_mode','passthrough','-f','rawvideo','-'],stdout=subprocess.PIPE)
    def get(s,k):
        while s.k<k:
            b=s.pr.stdout.read(s.w*s.h*3)
            if len(b)<s.w*s.h*3: break
            s.f=np.frombuffer(b,np.uint8).reshape(s.h,s.w,3); s.k+=1
        return s.f
P=np.load('vinheta_params.npy'); yy,xx=np.mgrid[0:OH,0:OW].astype(np.float32); X=(xx+.5)/OW-.5; Y=(yy+.5)/OH-.5
D=np.sqrt((X/P[0])**2+(Y/P[1])**2); VIG=np.clip(P[2]+P[3]*D**2+P[4]*D**4,0.08,1.06).astype(np.float32)[...,None]  # vinheta do AD ES
JC0,JD=TL.get('jump',[1e9,0]); sc=TL['scenes']; total=TL['total']; N=int(round(total*FPS))
win=[]
for i,(n,s,e) in enumerate(sc):
    ws=s-(XF if i>0 else 0); we=e+(XF if i<len(sc)-1 else 0)
    p,org=SRC[n]; org=org if org is not None else ws-0.2
    win.append(dict(n=n,s=s,e=e,ws=ws,we=we,p=p,org=org,rd=None))
def frame(wd,T):
    if wd['rd'] is None: wd['rd']=Rd(wd['p'])
    r=wd['rd']; loc=T-wd['org']+(JD if wd['n']=='crown3' and T>=JC0 else 0); k=max(0,int(loc*r.fps+1e-6)); f=r.get(k)
    z=1.0+0.06*(T-wd['s'])/(wd['e']-wd['s']); z=max(1.0,z)
    sx=OW/r.w*z; sy=OH/r.h*z
    M=np.float32([[sx,0,OW/2-sx*r.w/2],[0,sy,OH/2-sy*r.h/2]])
    return cv2.warpAffine(f,M,(OW,OH),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REFLECT).astype(np.float32)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{OW}x{OH}','-r',str(FPS),'-i','-',
 '-vf','scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p','-c:v','libx264','-crf','12','-preset','medium','base_it.mp4'],stdin=subprocess.PIPE)
for j in range(N):
    T=j/FPS
    act=[w for w in win if w['ws']-1e-6<=T<w['we']]
    if len(act)==1: out=frame(act[0],T)
    else:
        a,b=act[0],act[1]; t=(T-b['ws'])/(a['we']-b['ws']); t=min(1,max(0,t))
        out=frame(a,T)*(1-t)+frame(b,T)*t
    enc.stdin.write(np.clip(out*VIG,0,255).astype(np.uint8).tobytes())
    if j%150==0: print(f'[{j}/{N}]',flush=True)
enc.stdin.close(); enc.wait(); print('ok')
