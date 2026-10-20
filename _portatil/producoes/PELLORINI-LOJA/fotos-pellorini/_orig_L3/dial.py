from PIL import Image
D={'pellorini-clovera_1':(1587,1211),'pellorini-clovera_6':(1007,1348),'pellorini-fiorella_1':(1536,1211),'pellorini-grazia_3':(1075,1007),'pellorini-luna-perla_1':(1543,1160),'pellorini-lunetta_1':(1502,1092),'pellorini-serafina_1':(1587,1058),'pellorini-serpina_1':(1195,887),'pellorini-valore_2':(1024,1178)}
rows=[]
for n,(x,y) in D.items():
  o=Image.open(n+'.png').convert('RGB');g=Image.open(n+'_gen.png').convert('RGB')
  b=(x-200,y-200,x+200,y+200)
  im=Image.new('RGB',(800,400));im.paste(o.crop(b),(0,0));im.paste(g.crop(b),(400,0));rows.append(im)
for k in range(0,9,5):
  part=rows[k:k+5];out=Image.new('RGB',(800,400*len(part)))
  for i,r in enumerate(part): out.paste(r,(0,400*i))
  out.save(f'dials_{k}.jpg',quality=88)
