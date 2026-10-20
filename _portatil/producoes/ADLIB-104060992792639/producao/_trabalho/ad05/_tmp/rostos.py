import cv2
c=cv2.VideoCapture('../../../UNICOS_HD/05.mp4')
det=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
for i in [5,35,70,90,120,155,200,240,280,1275,1320]:
    c.set(1,i); ok,f=c.read(); g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    fs=det.detectMultiScale(g,1.1,5,minSize=(40,40))
    print(i,[tuple(int(v) for v in x) for x in fs])
    for (x,y,w,h) in fs: cv2.rectangle(f,(x,y),(x+w,y+h),(0,0,255),3)
    cv2.imwrite(f'_tmp/rosto_{i}.jpg',cv2.resize(f,(360,640)))
