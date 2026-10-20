import sys, numpy as np, librosa
for f in sys.argv[1:]:
    y,sr=librosa.load(f,sr=16000); e=librosa.feature.rms(y=y,frame_length=640,hop_length=160)[0]
    db=20*np.log10(e+1e-9); thr=db.max()-35; idx=np.where(db>thr)[0]
    print(f, round(idx[0]*0.01,2), round(idx[-1]*0.01+0.04,2), round(len(y)/sr,2))
