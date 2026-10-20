import cv2,glob,sys,numpy as np
fs=sorted(glob.glob("f05/*.jpg")); y0,y1=850,1280; sc=0.5; cols=6; per=48
for s in range(0,len(fs),per):
    tiles=[]
    for i,f in enumerate(fs[s:s+per]):
        im=cv2.imread(f)[y0:y1]; im=cv2.resize(im,None,fx=sc,fy=sc)
        cv2.putText(im,f"{(s+i)/2:.1f}",(5,20),0,0.6,(0,255,255),2); tiles.append(im)
    while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
    rows=[np.hstack(tiles[r:r+cols]) for r in range(0,len(tiles),cols)]
    cv2.imwrite(f"banda_{s//per}.jpg",np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])
