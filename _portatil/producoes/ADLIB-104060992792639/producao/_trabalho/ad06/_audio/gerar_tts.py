import json, subprocess, sys, os
from pathlib import Path
A=Path(__file__).parent; KIT=Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
VOZ={"MULHER":"ZsipxX9wNYg2lJhEScWc"}
B={b["id"]:b for b in json.load(open(A/"blocos.json",encoding="utf-8"))}
args=sys.argv[1:]  # id[=vel][:sufixo]
tot=0
for a in args:
    i,_,suf=a.partition(":"); i,_,vel=i.partition("="); vel=vel or "1.0"
    b=B[i]; out=A/"tts"/f"{i}{suf}.mp3"
    env=dict(os.environ,PYTHONIOENCODING="utf-8")
    subprocess.run([sys.executable,"ferramentas/tts_elevenlabs.py",b["texto"],"-o",str(out),"--voz",VOZ[b["quem"]],"--velocidade",vel,"--sim"],cwd=KIT,env=env,check=True,capture_output=True)
    d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(out)]))
    tot+=len(b["texto"]); print(i,suf,vel,"dur",round(d,2),"slot",round(b["fim"]-b["ini"],2),"chars",len(b["texto"]))
print("chars",tot)
