# -*- coding: utf-8 -*-
"""Prepara um AD final (só o .mp4 final da pasta producao) para servir de corpo e/ou fonte de tomadas do gancho.

  python prep_fonte.py <NN> [--ate 90]

Gera em variacoes/fontes/NN/:
  palavras.json  -> transcrição por palavra dos primeiros --ate s (faster-whisper small, cpu_threads=4)
  banco.json     -> tomadas (scdet) dos primeiros --ate s, com grupo de cena contínua (mesmo cenário em cortes seguidos)
  folha.jpg      -> folha de contato 1 q/s para conferir
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

PROD = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao")
V = Path(__file__).resolve().parent
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")


def final_de(nn):
    c = [p for p in PROD.glob(f"AD {nn} - *.mp4") if "CURTO" not in p.name]
    if not c:
        raise SystemExit(f"AD {nn} final ainda não existe")
    return c[0]


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nn")
    ap.add_argument("--ate", type=float, default=90)
    ap.add_argument("--sem-whisper", action="store_true")
    a = ap.parse_args()
    f = final_de(a.nn)
    O = V / "fontes" / a.nn
    O.mkdir(parents=True, exist_ok=True)
    (O / "final.txt").write_text(str(f), encoding="utf-8")

    # tomadas
    r = subprocess.run(["ffmpeg", "-hide_banner", "-t", str(a.ate), "-i", str(f), "-an", "-vf",
                        "scdet=threshold=10,metadata=print", "-f", "null", "-"], capture_output=True, text=True)
    cortes = [0.0] + [float(l.split("lavfi.scd.time:")[1]) for l in r.stderr.splitlines() if "lavfi.scd.time:" in l]
    cortes.append(min(a.ate, dur(f)))
    tomadas = []
    cap = cv2.VideoCapture(str(f))

    def quadro(t):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, im = cap.read()
        return cv2.resize(im, (90, 160)) if ok else None

    for i in range(len(cortes) - 1):
        ini, fim = cortes[i], cortes[i + 1]
        tomadas.append({"ini": round(ini, 3), "fim": round(fim, 3), "dur": round(fim - ini, 3),
                        "q0": quadro(ini + 0.1), "q1": quadro(max(ini + 0.1, fim - 0.15))})
    # grupo de cena contínua: fim de uma tomada parecido com início da seguinte (histograma HSV)
    def hist(im):
        h = cv2.calcHist([cv2.cvtColor(im, cv2.COLOR_BGR2HSV)], [0, 1], None, [30, 32], [0, 180, 0, 256])
        return cv2.normalize(h, h).flatten()
    g = 0
    for i, t in enumerate(tomadas):
        if i and t["q0"] is not None and tomadas[i - 1]["q1"] is not None:
            c = cv2.compareHist(hist(tomadas[i - 1]["q1"]), hist(t["q0"]), cv2.HISTCMP_CORREL)
            t["sim_ant"] = round(float(c), 3)
            if c < 0.70:
                g += 1
        t["grupo"] = g
    for t in tomadas:
        t.pop("q0"); t.pop("q1")
    json.dump(tomadas, open(O / "banco.json", "w", encoding="utf-8"), indent=0)
    print(f"{len(tomadas)} tomadas, {g + 1} grupos")

    subprocess.run([sys.executable, str(KIT / "folhas_contato.py"), "--cada", "1", "--de", "0", "--ate", str(a.ate),
                    "--saida", str(O / "folha"), str(f)], check=True, capture_output=True)

    if not a.sem_whisper:
        from faster_whisper import WhisperModel
        wav = O / "ini.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", str(a.ate), "-i", str(f), "-ac", "1", "-ar", "16000", str(wav)], check=True)
        m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
        segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True, vad_filter=False)
        pal = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words]
        json.dump(pal, open(O / "palavras.json", "w", encoding="utf-8"), ensure_ascii=False)
        print(" ".join(f"{w}[{a0:.1f}-{a1:.1f}]" for w, a0, a1 in pal if a0 < 45))


if __name__ == "__main__":
    main()
