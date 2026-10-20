import cv2, json
d = json.load(open('track.json'))
B = {int(k):v for k,v in d['B'].items()}
x0,y0,x1,y1 = B[357]; w,h=x1-x0,y1-y0
px,py=x0,y0
prev = cv2.cvtColor(cv2.imread('fr/0357.png'), cv2.COLOR_BGR2GRAY)
for n in range(356,338,-1):
    g = cv2.cvtColor(cv2.imread(f'fr/{n:04d}.png'), cv2.COLOR_BGR2GRAY)
    tpl = prev[py:py+h, px:px+w]
    S=10; sx0,sy0=px-S,py-S
    r = cv2.matchTemplate(g[sy0:py+h+S, sx0:px+w+S], tpl, cv2.TM_CCOEFF_NORMED)
    _,mv,_,ml = cv2.minMaxLoc(r)
    px,py = sx0+ml[0], sy0+ml[1]; prev=g
    B[n]=[px,py,px+w,py+h]; print(n, round(mv,2), px, py)
open('caixaB.txt','w').write(";".join(f"{n-339}:{','.join(map(str,B[n]))}" for n in sorted(B)))
