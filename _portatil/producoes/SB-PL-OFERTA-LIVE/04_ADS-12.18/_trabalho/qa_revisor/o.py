import cv2
from rapidocr_onnxruntime import RapidOCR
V=r"C:\Users\PICHAU\Downloads\SB-PL-OFERTA-LIVE\04_ADS-12.18\SB-PL-ADS-12.18.mp4"
ocr=RapidOCR(); cap=cv2.VideoCapture(V); fps=cap.get(5); n=int(cap.get(7))
t=0.0
while t<33.1:
    cap.set(cv2.CAP_PROP_POS_FRAMES,int(t*fps)); ok,f=cap.read()
    if not ok: break
    r,_=ocr(f)
    txt=" | ".join(f"{x[1]}@{int(x[0][0][1])}" for x in (r or []))
    print(f"{t:5.2f} {txt}")
    t+=0.5
