# Cartão v2 SEM EMOJI (reprovação Meta 18/10/2026): caixa branca arredondada única cobrindo todo o cartão original
# (inclusive a linha de emojis 🙏🔮✨❤️‍🩹 queimada na base), sem ‼️; 1ª linha em vermelho escuro como destaque.
# Uso: python card_v2_sem_emoji.py <saida.png> <tamanho_fonte> "<linha1>" "<linha2>" "<linha3>"
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
out, fs, l1, l2, l3 = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
X0,Y0,X1,Y1,R = 16,304,1064,724,34      # cartão original (com a aba dos emojis): x 26-1056, y 316-711 -> folga
S=4                                       # supersampling p/ borda suave
FONT=r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf"
m=Image.new("L",(1080*S,1920*S),0); ImageDraw.Draw(m).rounded_rectangle((X0*S,Y0*S,X1*S,Y1*S),R*S,fill=255)
alpha=m.resize((1080,1920),Image.LANCZOS)
img=Image.new("RGB",(1080,1920),(255,255,255)); d=ImageDraw.Draw(img)
F=ImageFont.truetype(FONT,fs)
PITCH=int(fs*1.62); cy=(Y0+Y1)/2
for i,(t,cor) in enumerate([(l1,(168,0,0)),(l2,(0,0,0)),(l3,(0,0,0))]):
    b=d.textbbox((0,0),"Hg"+t,font=F); hb=d.textbbox((0,0),"H",font=F)
    w=d.textlength(t,font=F); assert w<X1-X0-40, (t,w)
    ymid=cy+(i-1)*PITCH            # centro da altura de maiúscula
    y=ymid-(hb[1]+hb[3])/2
    d.text((540-w/2,y),t,font=F,fill=cor)
rgba=np.dstack([np.array(img),np.array(alpha)]); Image.fromarray(rgba).save(out); print("ok",out)
