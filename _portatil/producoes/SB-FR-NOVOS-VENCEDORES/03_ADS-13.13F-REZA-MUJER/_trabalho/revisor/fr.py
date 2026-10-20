import subprocess,numpy as np,cv2,sys
def frames(path,w=720,h=1280):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',path,'-vf','scale=in_range=tv:in_color_matrix=bt601:out_range=pc,format=bgr24','-f','rawvideo','-'],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(w*h*3)
        if len(b)<w*h*3: break
        yield np.frombuffer(b,np.uint8).reshape(h,w,3)
