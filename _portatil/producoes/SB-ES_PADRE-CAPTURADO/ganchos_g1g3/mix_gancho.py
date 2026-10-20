# -*- coding: utf-8 -*-
"""Áudio do gancho: voz (ElevenLabs) com reverb do lugar + ambiente de tumulto + áudio nativo do Seedance (opcional)
+ trilha do v4 (demucs no_vocals do trecho inicial) terminando exatamente em 8,05 s do v4, para a música seguir
contínua no corte para a selfie (o corpo começa em 8,05 s do v4).
uso: python mix_gancho.py cfg.json -> wav estéreo 48 kHz
cfg: {"dur", "voz", "voz_t0", "voz_trim":[a,b] opcional, "voz_lufs": -15, "reverb": "igreja"|"rua",
      "amb": arq|null, "amb_lufs": -27, "nativo": arq|null, "nativo_lufs": -27, "nativo_ss": 0, "musica_lufs": null, "out"}"""
import sys, json, subprocess, numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from pathlib import Path
SR = 48000; med = pyln.Meter(SR)
MUS = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\audio\v4\sep\htdemucs\ini10\no_vocals.wav"
CORTE_V4 = 241 / 30   # 1º quadro da selfie no v4 (corpo_info.json)
TMP = Path(__file__).resolve().parent / "_tmp"; TMP.mkdir(exist_ok=True)
def ld(p, ss=0.0, dur=None):
    y, _ = librosa.load(p, sr=SR, mono=True, offset=ss, duration=dur); return y
def fx(y, f):
    sf.write(TMP / "_in.wav", y, SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(TMP / "_in.wav"), "-af", f, "-c:a", "pcm_f32le", str(TMP / "_out.wav")], check=True)
    return sf.read(TMP / "_out.wav")[0]
def norm(y, alvo):
    return y * 10 ** ((alvo - med.integrated_loudness(y)) / 20)
def fade(y, a=0.01, b=0.05):
    y = y.copy(); na, nb = int(a * SR), int(b * SR); y[:na] *= np.linspace(0, 1, na); y[-nb:] *= np.linspace(1, 0, nb); return y
def main(c):
    n = int(round(c["dur"] * SR)); out = np.zeros(n)
    # trilha do v4: termina em 8,05 s do v4 = fim do gancho
    m0 = max(0.0, CORTE_V4 - c["dur"]); mus = ld(MUS, m0, CORTE_V4 - m0)
    if c.get("musica_lufs") is not None: mus = norm(mus, c["musica_lufs"])
    out[n - len(mus):] += mus[: n]
    if c.get("amb"):
        a = ld(c["amb"]); a = np.tile(a, int(np.ceil(n / len(a))))[:n]
        a = fx(a, "highpass=f=80" + (",aecho=0.8:0.5:70:0.2" if c.get("reverb") == "igreja" else ""))[:n]
        env = np.ones(n); fi = int(0.2 * SR); env[:fi] = np.linspace(0, 1, fi)
        out += norm(a, c.get("amb_lufs", -27)) * env
    if c.get("nativo"):
        a = ld(c["nativo"], c.get("nativo_ss", 0.0), c["dur"]); a = np.pad(a, (0, max(0, n - len(a))))[:n]
        out += norm(a, c.get("nativo_lufs", -27))
    v = ld(c["voz"])
    if c.get("voz_trim"): v = v[int(c["voz_trim"][0] * SR): int(c["voz_trim"][1] * SR)]
    rv = "highpass=f=110,aecho=0.85:0.5:40|85:0.16|0.09" if c.get("reverb") == "igreja" else "highpass=f=110,aecho=0.8:0.4:25:0.08"
    v = norm(fx(fade(v), rv), c.get("voz_lufs", -15)); k = int(c["voz_t0"] * SR)
    out[k: k + len(v)] += v[: n - k]
    pk = np.abs(out).max()
    if pk > 0.89: out *= 0.89 / pk
    sf.write(c["out"], np.stack([out, out], 1), SR, subtype="PCM_16")
    print("ok", c["out"], "LUFS", round(med.integrated_loudness(out), 1), "pico", round(float(min(pk, 0.89)), 3))
if __name__ == "__main__":
    main(json.load(open(sys.argv[1], encoding="utf-8")))
