# Título do gancho em FR no mesmo desenho do ES: 3 faixas (branca/texto vermelho, branca/texto preto, vermelha/texto branco)
from PIL import Image, ImageDraw, ImageFont
F="fonts/Poppins-ExtraBold.ttf"
ROWS=[("QUELQUE CHOSE D'INATTENDU",(255,255,255),(222,29,47)),("EST ARRIVÉ PENDANT LA PRIÈRE",(255,255,255),(15,15,15)),("À SAINT BENOÎT",(224,28,44),(255,255,255))]
Y=[(1022,1109),(1118,1205),(1214,1301)]
sz=62
while True:
    f=ImageFont.truetype(F,sz); w=max(f.getbbox(t)[2]-f.getbbox(t)[0] for t,_,_ in ROWS)
    if w<=930: break
    sz-=1
im=Image.new("RGBA",(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
for (t,bg,fg),(y0,y1) in zip(ROWS,Y):
    bb=f.getbbox(t); tw=bb[2]-bb[0]; x0=540-tw//2-34; x1=540+tw//2+34
    d.rectangle([x0,y0,x1,y1],fill=bg)
    # centro vertical pela altura das maiúsculas
    cap=f.getbbox("H"); ch=cap[3]-cap[1]; ty=(y0+y1)//2-ch//2-cap[1]+2
    d.text((540-tw//2-bb[0],ty),t,font=f,fill=fg)
print("fonte",sz)
im.save("titulo_fr.png")
im.crop((0,1000,1080,1320)).save("folhas/z_titulo_fr.png")
