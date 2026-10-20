import json, sys, subprocess
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
VOZ = "UNDKAyEJ2rTv99l7gCy5"   # ORACAO-11 mulher (Desatadora)
B = json.load(open("blocos.json", encoding="utf-8"))
so = sys.argv[1:]
tot = 0
for b in B:
    if so and b["id"] not in so: continue
    vel = b.get("vel", 1.0)
    T.gerar(b["texto"], f"tts/{b['id']}.mp3", VOZ, velocidade=vel)
    tot += len(b["texto"])
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"tts/{b['id']}.mp3"],capture_output=True,text=True).stdout)
    print(b["id"], f"{d:.2f}s janela {b['fim']-b['ini']:.2f}s razao {d/(b['fim']-b['ini']):.2f}", flush=True)
print("caracteres", tot)
