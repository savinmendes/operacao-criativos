import sys,subprocess,numpy as np
sys.path.insert(0,r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
import checar_lipsync as cl
v,a=sys.argv[1],sys.argv[2]
o=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height,r_frame_rate','-of','csv=p=0',v],capture_output=True,text=True).stdout.strip().split(',')
W,H=int(o[0]),int(o[1]); fps=eval(o[2])
F=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',v,'-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout,np.uint8).reshape(-1,H,W,3)
au=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',a,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
det=cl.Rastreador()
for k in range(len(F)):
    p=det.pontos(F[k]); t=k/fps
    seg=au[int(t*16000):int((t+1/fps)*16000)]; db=20*np.log10(np.sqrt((seg**2).mean())+1e-9) if len(seg) else -99
    op=np.linalg.norm(p[13]-p[14])/np.linalg.norm(p[234]-p[454]) if p is not None else -1
    print(f"{t:5.2f} {db:6.1f} {'#'*int(op*200)}")
