import cv2,glob,re
from rapidocr_onnxruntime import RapidOCR
o=RapidOCR()
PL=set("ZAPAMIĘTAJĄ CIĘ PO ZAPACHU 3 PERFUMY W CENIE 1 A KAŻDE WNĘTRZE ZACHOWA TWÓJ ŚLAD 100 SZTUK TERAZ ALBO NIGDY OTO OD KTÓRYCH KOBIETY TRACĄ GŁOWĘ".split())
for n in ["PL_PF-7","PL_PF-MASC-17","PL_PF-MASC-18","PL_PF-MASC-TESTE-1","PL_PF-MASC-TESTE-3"]:
    out=open(f'ocr_{n}.txt','w',encoding='utf-8')
    for i,f in enumerate(sorted(glob.glob(f'q/{n}/*.jpg'))):
        im=cv2.imread(f)
        for tag,crop in [('topo',im[0:130]),('faixa',im[700:960])]:
            r,_=o(crop)
            if r:
                txt=' | '.join(f"{x[1]}({x[2]:.2f})" for x in r)
                out.write(f"{i*0.5:.1f} {tag}: {txt}\n")
    out.close(); print(n,'ok',flush=True)
