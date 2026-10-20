import json,re,subprocess,sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
termos=["maya","verra","mayaverra","sesenta","60 d","hecho en","estados unidos","ozempic","tiktok","cofepris","cáncer","cancer","precio","link","dólar","dolar","pesos","45 d","probado"]
for f in sys.argv[1:]:
    subprocess.run(["ffmpeg","-v","error","-y","-i",f,"-vn","-ac","1","-ar","16000","rev.wav"],check=True)
    segs,_=m.transcribe("rev.wav",language="es",condition_on_previous_text=False,vad_filter=False)
    txt=[(s.start,s.end,s.text.strip()) for s in segs]
    out=f.rsplit(".",1)[0]+"_transcricao.txt"
    open(out,"w",encoding="utf-8").write("\n".join(f"{a:7.1f} {b:7.1f} {t}" for a,b,t in txt))
    print("==",f)
    for a,b,t in txt:
        if any(k in t.lower() for k in termos): print("ACHOU",round(a,1),t)
    print("fim fala:",round(txt[-1][1],1),txt[-1][2])
