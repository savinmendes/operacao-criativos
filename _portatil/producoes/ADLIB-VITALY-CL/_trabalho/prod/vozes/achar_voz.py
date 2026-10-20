# -*- coding: utf-8 -*-
"""Acha a voz do ElevenLabs (biblioteca compartilhada + conta) mais parecida com uma amostra (resemblyzer).
  python achar_voz.py amostra.wav saida.json [--genero female] [--idade young]"""
import sys, json, subprocess, tempfile, urllib.request, urllib.parse
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
amostra, saida = sys.argv[1], sys.argv[2]
gen = sys.argv[sys.argv.index("--genero")+1] if "--genero" in sys.argv else "female"
idade = sys.argv[sys.argv.index("--idade")+1] if "--idade" in sys.argv else None
K = T.chave()
def get(url):
    r = urllib.request.Request(url, headers={"xi-api-key": K})
    return json.loads(urllib.request.urlopen(r, timeout=60).read())
cands = {}
for v in get("https://api.elevenlabs.io/v1/voices").get("voices", []):
    if v.get("preview_url"): cands[v["voice_id"]] = (v["name"], v["preview_url"], "conta")
for q in [dict(language="es"), dict(language="es", accent="latin american"), dict(language="es", use_cases="social_media"), dict(language="es", category="professional")]:
    for page in range(3):
        p = dict(page_size=100, gender=gen, page=page, **q)
        if idade: p["age"] = idade
        try:
            d = get("https://api.elevenlabs.io/v1/shared-voices?" + urllib.parse.urlencode(p))
        except Exception as e:
            print("erro", e); break
        for v in d.get("voices", []):
            if v.get("preview_url"): cands[v["voice_id"]] = (v["name"], v["preview_url"], v.get("public_owner_id", ""))
        if not d.get("has_more"): break
print(len(cands), "candidatas")
enc = VoiceEncoder(verbose=False); tmp = Path(tempfile.mkdtemp())
def emb(src):
    o = tmp / ("e%d.wav" % abs(hash(src)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", str(o)], check=True)
    return enc.embed_utterance(preprocess_wav(o))
alvo = emb(amostra)
res = []
for vid, (nome, url, own) in cands.items():
    try:
        f = tmp / (vid + ".mp3"); urllib.request.urlretrieve(url, f)
        res.append((float(np.dot(alvo, emb(str(f)))), vid, nome, own))
    except Exception as e:
        pass
res.sort(reverse=True)
for r in res[:12]: print("%.3f %s %s %s" % r)
Path(saida).write_text(json.dumps(res[:30], ensure_ascii=False, indent=1), encoding="utf-8")
