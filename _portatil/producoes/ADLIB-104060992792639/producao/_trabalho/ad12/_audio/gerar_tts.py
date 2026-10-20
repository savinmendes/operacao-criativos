import json, subprocess, sys, os
from pathlib import Path
A = Path(__file__).resolve().parent; KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
VOZ = "ZsipxX9wNYg2lJhEScWc"
B = {b["id"]: b for b in json.load(open(A/"blocos.json", encoding="utf-8"))}
ids = sys.argv[1].split(","); vel = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0; suf = sys.argv[3] if len(sys.argv) > 3 else ""
env = dict(os.environ, PYTHONIOENCODING="utf-8")
for i in ids:
    out = A/"tts"/f"{i}{suf}.mp3"
    subprocess.run([sys.executable, "ferramentas/tts_elevenlabs.py", B[i]["texto"], "-o", str(out), "--voz", VOZ, "--velocidade", str(vel), "--sim"], cwd=KIT, env=env, check=True, capture_output=True)
    d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(out)]))
    print(i+suf, round(d,2), "janela", round(B[i]["fim"]-B[i]["ini"],2), len(B[i]["texto"]), flush=True)
