from PIL import Image, ImageDraw
import glob, os, sys
n=sys.argv[1]
fs=sorted(glob.glob(n+'/fr/*.jpg'),key=lambda f: float(os.path.basename(f)[:-4]))
ims=[Image.open(f) for f in fs]; w,h=ims[0].size; cols=5; rows=(len(ims)+cols-1)//cols
M=Image.new('RGB',(w*cols,h*rows))
for i,(f,im) in enumerate(zip(fs,ims)):
    d=ImageDraw.Draw(im); d.text((5,5),os.path.basename(f),fill=(255,255,0))
    M.paste(im,((i%cols)*w,(i//cols)*h))
M.save(n+'/fr_sheet.jpg')
