# -*- coding: utf-8 -*-
"""Semelhança de locutor (resemblyzer) entre narração original e a gerada com voz clonada."""
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav

S = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20")
L = S / "lymphoria" / "_trabalho"
casos = [("AD 06", 0, 52, L / "ad06" / "narr_fim.mp3"),
         ("AD 21", 290, 316.5, L / "ad21" / "narr_fim.mp3"),
         ("AD 24", 433, 475, L / "ad24" / "narr_fim.mp3"),
         ("AD 04", 28, 107, L / "ad04" / "narr_fim_univ.mp3")]
enc = VoiceEncoder(verbose=False)
tmp = Path(tempfile.mkdtemp())


def wav(src, de=None, ate=None, nome="x"):
    out = tmp / f"{nome}.wav"
    corte = ["-ss", str(de), "-to", str(ate)] if de is not None else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", *corte, "-i", str(src), "-ac", "1", "-ar", "16000", str(out)], check=True)
    return enc.embed_utterance(preprocess_wav(out))


for ad, de, ate, gen in casos:
    o = wav(S / f"{ad}.mp4", de, ate, ad.replace(" ", "") + "o")
    g = wav(gen, nome=ad.replace(" ", "") + "g")
    print(f"{ad}: semelhança {float(np.dot(o, g)):.3f}")
