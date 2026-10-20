from PIL import Image,ImageDraw
S=4; w,h=190,225
im=Image.new('RGBA',(w*S,h*S),(0,0,0,0)); d=ImageDraw.Draw(im)
def P(pts): return [(x*S,y*S) for x,y in pts]
sh=[(60,8),(130,8),(130,112),(178,112),(95,215),(12,112),(60,112)]
d.polygon(P(sh),fill=(0,0,0,255))
# body (inset)
ins=[(66,14),(124,14),(124,118),(165,118),(95,205),(25,118),(66,118)]
d.polygon(P(ins),fill=(253,199,49,255))
d.rectangle([66*S,14*S,124*S,70*S],fill=(255,226,140,255))
im=im.resize((w,h),Image.LANCZOS); im.save('seta_amarela.png'); print(im.size)
