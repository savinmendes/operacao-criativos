import json, sys, urllib.request
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import chave
AQ = Path(__file__).resolve().parent / "trilha"
def req(url, body):
    r = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers={"xi-api-key": chave(), "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=180) as f: return f.read()
for nome, d, txt in [("sfx_briga", 6.0, "Violent scene at an outdoor street market: a wooden fruit stall is kicked hard, wooden crates bang and crash, many oranges and apples fall and roll on concrete pavement, people gasp, busy market crowd ambience"),
                     ("amb_feria", 10.0, "Busy outdoor Latin American street market ambience, distant vendors and crowd murmur, light traffic, no music")]:
    if (AQ / f"{nome}.mp3").exists(): continue
    (AQ / f"{nome}.mp3").write_bytes(req("https://api.elevenlabs.io/v1/sound-generation", dict(text=txt, duration_seconds=d, prompt_influence=0.5))); print("ok", nome)
