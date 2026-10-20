# -*- coding: utf-8 -*-
"""Busca vozes da biblioteca ElevenLabs parecidas com uma amostra e ranqueia por semelhança de locutor (resemblyzer).
  python comparar_vozes.py amostra.mp3 pasta_saida"""
import os
import subprocess
import sys

import numpy as np
import requests
from resemblyzer import VoiceEncoder, preprocess_wav

sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import tts_elevenlabs as T  # noqa: E402

amostra, pasta = sys.argv[1], sys.argv[2]
os.makedirs(pasta, exist_ok=True)
vozes = requests.post("https://api.elevenlabs.io/v1/similar-voices", headers={"xi-api-key": T.chave()},
                      files={"audio_file": open(amostra, "rb")}, data={"top_k": "10"}).json()["voices"]
enc = VoiceEncoder()


def emb(p):
    wav = p + ".wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "1", "-ar", "16000", wav], check=True)
    return enc.embed_utterance(preprocess_wav(wav))


ref = emb(amostra)
res = []
for v in vozes:
    p = os.path.join(pasta, v["voice_id"] + ".mp3")
    open(p, "wb").write(requests.get(v["preview_url"]).content)
    res.append((float(np.dot(ref, emb(p))), v["voice_id"], v["name"]))
for s, i, n in sorted(res, reverse=True):
    print(f"{s:.3f}  {i}  {n}")
