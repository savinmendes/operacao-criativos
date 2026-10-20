# -*- coding: utf-8 -*-
"""Extração para o estudo: fala (faster-whisper, es) e texto na tela (RapidOCR, 1 quadro a cada 3 s) + folha de contato.
  python extrair.py fala | tela
Rodar em sequência (fala depois tela): os dois juntos disputam a CPU. Mostra [k/N], % e tempo restante."""
import json
import sys
import time
from pathlib import Path

D = Path(__file__).resolve().parent
VID = sorted((D.parent / "originais").glob("*.mp4"))


def fmt(s):
    s = int(max(0, s)); return f"{s // 60}min{s % 60:02d}s"


def prog(k, n, t0, nome, feito, total):
    dec = time.time() - t0
    print(f"[{k}/{n}] {nome} | {feito / total:.0%} | decorrido {fmt(dec)} | falta ~{fmt(dec / max(feito, 1e-6) * (total - feito))}", flush=True)


def durs():
    import cv2
    out = {}
    for v in VID:
        c = cv2.VideoCapture(str(v)); out[v] = c.get(7) / (c.get(5) or 30)
    return out


if sys.argv[1] == "fala":
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=8)
    (D / "fala").mkdir(exist_ok=True)
    dd = durs(); total = sum(dd.values()); feito = 0; t0 = time.time()
    for k, v in enumerate(VID, 1):
        o = D / "fala" / f"{v.stem}.json"
        if not o.exists():
            segs, info = m.transcribe(str(v), language="es", vad_filter=True)
            o.write_text(json.dumps([[round(s.start, 1), round(s.end, 1), s.text.strip()] for s in segs], ensure_ascii=False),
                         encoding="utf-8")
        feito += dd[v]; prog(k, len(VID), t0, v.stem, feito, total)
else:
    import cv2
    import numpy as np
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    (D / "tela").mkdir(exist_ok=True); (D / "folhas").mkdir(exist_ok=True)
    dd = durs(); total = sum(dd.values()); feito = 0; t0 = time.time()
    for k, v in enumerate(VID, 1):
        o = D / "tela" / f"{v.stem}.json"
        if not o.exists():
            c = cv2.VideoCapture(str(v)); fps = c.get(5) or 30; n = int(c.get(7))
            passo = int(fps * 3); res, ult, thumbs = [], None, []
            for f in range(0, n, passo):
                c.set(1, f); ok, im = c.read()
                if not ok:
                    break
                r, _ = ocr(im)
                txt = " | ".join(t for _, t, conf in (r or []) if conf > 0.6)
                if txt and txt != ult:
                    res.append([round(f / fps, 1), txt])
                ult = txt
                th = cv2.resize(im, (90, 160)); cv2.putText(th, f"{int(f / fps // 60)}:{int(f / fps % 60):02d}", (2, 12), 0, 0.38, (0, 255, 255), 1)
                thumbs.append(th)
            o.write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
            # folha de contato (1 quadro a cada 3 s, até 200 quadros por folha)
            for p in range(0, len(thumbs), 200):
                ch = thumbs[p:p + 200]
                while len(ch) % 20: ch.append(np.zeros_like(thumbs[0]))
                cv2.imwrite(str(D / "folhas" / f"{v.stem}_{p // 200 + 1}.jpg"),
                            np.vstack([np.hstack(ch[i:i + 20]) for i in range(0, len(ch), 20)]), [cv2.IMWRITE_JPEG_QUALITY, 80])
        feito += dd[v]; prog(k, len(VID), t0, v.stem, feito, total)
