import os, json, requests
ENV = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\.env"
def key():
    for l in open(ENV, encoding="utf-8"):
        l = l.strip()
        if l.startswith("ELEVENLABS_API_KEY") or l.startswith("ELEVEN_API_KEY") or l.startswith("XI_API_KEY"):
            return l.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("chave nao achada")
H = lambda: {"xi-api-key": key()}
