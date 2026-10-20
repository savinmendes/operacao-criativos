# -*- coding: utf-8 -*-
"""Estudo dos 30 criativos TikTok: transcrição (fala) e OCR (texto na tela) de cada vídeo.
  python analisar.py fala   -> _analise/fala/<pasta>_<NN>.json  (faster-whisper, inglês)
  python analisar.py tela   -> _analise/tela/<pasta>_<NN>.json  (RapidOCR, 1 quadro/s)
Mostra progresso [k/N] e tempo restante."""
import json
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
VIDEOS = sorted(BASE.glob("produto-*/*.mp4"))


def fmt(s):
    s = int(max(0, s))
    return f"{s // 60}min{s % 60:02d}s"


def progresso(k, n, t0, nome):
    dec = time.time() - t0
    print(f"[{k}/{n}] {nome} | {k / n:.0%} | decorrido {fmt(dec)} | falta ~{fmt(dec / k * (n - k))}", flush=True)


def fala():
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    (OUT / "fala").mkdir(exist_ok=True)
    t0 = time.time()
    for k, v in enumerate(VIDEOS, 1):
        o = OUT / "fala" / f"{v.parent.name}_{v.stem}.json"
        if not o.exists():
            segs, info = m.transcribe(str(v), language="en", vad_filter=True)
            o.write_text(json.dumps([[round(s.start, 1), round(s.end, 1), s.text.strip()] for s in segs],
                                    ensure_ascii=False, indent=0), encoding="utf-8")
        progresso(k, len(VIDEOS), t0, o.stem)


def tela():
    import cv2
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    (OUT / "tela").mkdir(exist_ok=True)
    t0 = time.time()
    for k, v in enumerate(VIDEOS, 1):
        o = OUT / "tela" / f"{v.parent.name}_{v.stem}.json"
        if not o.exists():
            c = cv2.VideoCapture(str(v))
            fps = c.get(cv2.CAP_PROP_FPS) or 30
            n = int(c.get(cv2.CAP_PROP_FRAME_COUNT))
            res, ultimo = [], None
            passo = int(round(fps * 1.5))
            for f in range(0, n, passo):
                c.set(cv2.CAP_PROP_POS_FRAMES, f)
                ok, im = c.read()
                if not ok:
                    break
                im = cv2.resize(im, (480, 854))
                r, _ = ocr(im)
                txt = " | ".join(t for _, t, conf in (r or []) if conf > 0.6)
                if txt and txt != ultimo:
                    res.append([round(f / fps, 1), txt])
                ultimo = txt
            o.write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
        progresso(k, len(VIDEOS), t0, o.stem)


{"fala": fala, "tela": tela}[sys.argv[1]]()
