# -*- coding: utf-8 -*-
"""Troca falas na faixa de voz (demucs) e remixa com o fundo (no_vocals), sem tirar a música.
  python trocar_falas.py plano.json
plano = {"vocals": ..., "fundo": ..., "saida": "audio.wav", "ate": 30.97 (opcional),
         "trocas": [{"janela": [a, b],                # zera a voz original aqui (com rampa de 30 ms)
                     "pecas": [{"src": "t.mp3", "de": 1.5, "ate": 6.45, "em": 39.55, "tempo": 1.03}]}]}
Cada peça: recorta [de, ate] do src, aplica atempo, iguala o RMS ao da voz original na janela e cola em "em".
"""
import json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np

SR = 44100


def ler(p, extra=None):
    c = ["ffmpeg", "-v", "error", "-i", str(p)] + (extra or []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(c, capture_output=True, check=True).stdout, np.float32)
    return a.reshape(-1, 2).copy()


def rms(x):
    return float(np.sqrt(np.mean(x ** 2) + 1e-12))


def main():
    pl = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    voz = ler(pl["vocals"])
    fundo = ler(pl["fundo"])
    n = min(len(voz), len(fundo))
    voz, fundo = voz[:n], fundo[:n]
    nova = voz.copy()
    rel = []
    for tr in pl["trocas"]:
        a, b = (int(t * SR) for t in tr["janela"])
        ref = rms(voz[a:b][np.abs(voz[a:b]).max(1) > 0.01]) if (np.abs(voz[a:b]).max(1) > 0.01).any() else rms(voz[a:b])
        r = int(0.03 * SR)
        env = np.ones(b - a, np.float32)
        env[:r] = np.linspace(1, 0, r); env[-r:] = np.linspace(0, 1, r); env[r:-r] = 0
        nova[a:b] *= env[:, None]
        xs = []
        for pc in tr["pecas"]:
            filt = f"atrim={pc['de']}:{pc['ate']},asetpts=PTS-STARTPTS"
            if abs(pc.get("tempo", 1) - 1) > 1e-3:
                filt += f",atempo={pc['tempo']}"
            filt += ",afade=t=in:d=0.02,areverse,afade=t=in:d=0.03,areverse"
            xs.append(ler(pc["src"], ["-af", filt]))
        allx = np.concatenate(xs)
        sel = allx[np.abs(allx).max(1) > 0.01]
        g = ref / rms(sel if len(sel) else allx)
        for pc, x in zip(tr["pecas"], xs):
            x = x * g
            i = int(pc["em"] * SR)
            j = min(n, i + len(x))
            nova[i:j] += x[: j - i]
            rel.append(f"{pc['src']} [{pc['de']}-{pc['ate']}] tempo {pc.get('tempo', 1)} -> {pc['em']:.2f}-{pc['em'] + len(x) / SR:.2f}s ganho {g:.2f}")
    mix = nova + fundo
    if pl.get("ate"):
        m = int(pl["ate"] * SR)
        mix = mix[:m]
        f = int(0.12 * SR)
        mix[-f:] *= np.linspace(1, 0, f)[:, None]
    pk = np.abs(mix).max()
    if pk > 0.99:
        mix *= 0.99 / pk
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s16le", pl["saida"]], input=mix.astype(np.float32).tobytes(), check=True)
    print("\n".join(rel))
    print("ok", pl["saida"], f"{len(mix) / SR:.3f}s")


if __name__ == "__main__":
    main()
