# Gera cada frase PL separada (voz Jesus The Chosen, multilingual_v2) com alinhamento; imprime duracoes
import sys, json, subprocess
sys.path.insert(0,r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
VOZ="AkQxVSf1kENGmX9WjeDE"
F=json.load(open("frases.json",encoding="utf-8"))
so=sys.argv[1:]
for f in F:
    if so and f["id"] not in so: continue
    T.gerar(f["txt"].replace("«","\"").replace("»","\""),f"audio/{f['id']}.mp3",voz=VOZ,modelo=f.get("modelo","eleven_multilingual_v2"),estabilidade=f.get("stab",0.5),similaridade=0.8,velocidade=f.get("vel",1.0))
for f in F:
    d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"audio/{f['id']}.mp3"],capture_output=True,text=True).stdout)
    print(f["id"],round(d,2),"janela",f["janela"],round(f["janela"][1]-f["janela"][0],2),f["txt"])
