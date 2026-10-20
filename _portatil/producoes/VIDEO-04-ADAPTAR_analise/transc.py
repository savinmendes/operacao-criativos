import os, sys
L=r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib"
os.add_dll_directory(L); os.environ["PATH"]=L+";"+os.environ["PATH"]
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",device="cuda",compute_type="float16")
segs,info=m.transcribe(sys.argv[1],language="es",vad_filter=True,condition_on_previous_text=False)
print("idioma",info.language,round(info.language_probability,2))
def f(t): return f"{int(t//60)}:{t%60:05.2f}"
with open(sys.argv[2],"w",encoding="utf-8") as o:
    for s in segs: o.write(f"[{f(s.start)}] {s.text.strip()}\n")
