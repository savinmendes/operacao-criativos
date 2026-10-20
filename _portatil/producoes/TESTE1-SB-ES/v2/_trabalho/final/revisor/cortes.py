import json
from PIL import Image, ImageDraw
t=json.load(open(r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\v2\_trabalho\final\timeline_v2.json",encoding="utf-8"))
P=t['planos']; B=[p['q0'] for p in P[1:]]
W,H=180,320
def fr(i): return Image.open(f"f/{i+1:05d}.jpg").resize((W,H))
for s in range(0,len(B),8):
    grp=B[s:s+8]; rows=(len(grp)+1)//2
    im=Image.new("RGB",(8*W+20,rows*(H+22)),"black"); d=ImageDraw.Draw(im)
    for k,q in enumerate(grp):
        r,c=k//2,k%2
        x0=c*(4*W+20); y0=r*(H+22)
        pl=P[s+k]; pn=P[s+k+1]
        d.text((x0+2,y0+2),f"q{q} t={q/30:.2f}s {pl.get('broll',pl['item'])}->{pn.get('broll',pn['item'])} z{pn.get('zoom','')}",fill="yellow")
        for j,qq in enumerate([q-2,q-1,q,q+1]):
            im.paste(fr(qq),(x0+j*W,y0+20))
    im.save(f"cortes_{s//8:02d}.jpg",quality=85)
print(len(B))
