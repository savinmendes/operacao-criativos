import cv2, sys, json
def track(ref, box, a, b):
    x0,y0,x1,y1 = box; w,h = x1-x0, y1-y0
    pos = {ref:(x0,y0)}
    tpl0 = cv2.cvtColor(cv2.imread(f'fr/{ref:04d}.png'), cv2.COLOR_BGR2GRAY)[y0:y1, x0:x1]
    for rng in (range(ref+1, b+1), range(ref-1, a-1, -1)):
        px,py = x0,y0; tpl = tpl0
        for n in rng:
            g = cv2.cvtColor(cv2.imread(f'fr/{n:04d}.png'), cv2.COLOR_BGR2GRAY)
            sx0, sy0 = max(0,px-30), max(0,py-30)
            reg = g[sy0:py+h+30, sx0:px+w+30]
            r = cv2.matchTemplate(reg, tpl, cv2.TM_CCOEFF_NORMED)
            _, mv, _, ml = cv2.minMaxLoc(r)
            px, py = sx0+ml[0], sy0+ml[1]
            pos[n] = (px,py)
            print(n, round(mv,2), px, py, file=sys.stderr)
    return {n:(x,y,x+w,y+h) for n,(x,y) in pos.items()}
A = track(318, (396,603,514,637), 306, 338)
B = track(359, (436,534,552,567), 339, 377)
json.dump({'A':A,'B':B}, open('track.json','w'))
def keys(d, start): return ";".join(f"{n-start}:{','.join(map(str,d[n]))}" for n in sorted(d))
open('caixaA.txt','w').write(keys(A,306)); open('caixaB.txt','w').write(keys(B,339))
