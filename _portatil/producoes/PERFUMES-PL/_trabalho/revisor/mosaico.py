import cv2, glob, os, sys, numpy as np
def sheets(n, y0, y1, tag, per=24, cols=2):
    fs = sorted(glob.glob(f"q/{n}/*.jpg"))
    os.makedirs("sheets", exist_ok=True)
    for k in range(0, len(fs), per):
        tiles=[]
        for i,f in enumerate(fs[k:k+per]):
            im = cv2.imread(f)[y0:y1]
            t = (k+i)*0.5
            cv2.putText(im, f"{t:.1f}s", (5,25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
            tiles.append(im)
        while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
        rows=[np.hstack(tiles[r:r+cols]) for r in range(0,len(tiles),cols)]
        cv2.imwrite(f"sheets/{n}_{tag}_{k//per:02d}.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
for n in sys.argv[1:]:
    sheets(n, 770, 930, "faixa")
    sheets(n, 0, 130, "topo", per=40)
