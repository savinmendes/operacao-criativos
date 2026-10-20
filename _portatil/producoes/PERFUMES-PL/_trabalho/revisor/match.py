import cv2,glob,numpy as np,sys,subprocess
vid, odir, times = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
O=[cv2.imread(f) for f in sorted(glob.glob(odir+'/*.jpg'))]
Os=[cv2.resize(o,(90,160))[45:95].astype(int) for o in O]  # mid region rows ~ y 360-760
for t in times:
    subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',vid,'-frames:v','1','-vf','scale=360:640','-y','tmp.png'])
    p=cv2.imread('tmp.png'); ps=cv2.resize(p,(90,160))[45:95].astype(int)
    d=[np.abs(ps-o).mean() for o in Os]; i=int(np.argmin(d))
    print(t, 'orig', i/10, round(d[i],1))
    cv2.imwrite(f'ev/cmp_{t}.jpg', np.hstack([p,O[i]]))
