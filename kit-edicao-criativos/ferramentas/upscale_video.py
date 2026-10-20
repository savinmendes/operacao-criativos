# -*- coding: utf-8 -*-
"""Upscale IA (Real-ESRGAN) de um vídeo inteiro em blocos, sem encher o disco, com progresso e tempo restante.

  python upscale_video.py entrada.mp4 saida.mp4 [--ate 316.6] [--escala 3] [--modelo realesr-animevideov3]

- Processa blocos de 30 s: extrai quadros -> Real-ESRGAN (GPU) -> grava o bloco em vídeo -> apaga os PNGs.
- No fim junta os blocos e põe o áudio original (cortado em --ate, com fade de 0,12 s).
- Para 360x640 com escala 3 a saída é 1080x1920.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

RE = Path(__file__).resolve().parent.parent / "_ferramentas_extras" / "realesrgan" / "realesrgan-ncnn-vulkan.exe"


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def fmt(s):
    s = int(max(0, s))
    return f"{s // 60}min{s % 60:02d}s" if s >= 60 else f"{s}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--ate", type=float, default=None)
    ap.add_argument("--escala", type=int, default=3)
    ap.add_argument("--modelo", default="realesr-animevideov3")
    ap.add_argument("--bloco", type=float, default=30.0)
    a = ap.parse_args()
    total = a.ate or dur(a.entrada)
    wk = Path(tempfile.mkdtemp(prefix="up_"))
    blocos, t, t0, k = [], 0.0, time.time(), 0
    nome = Path(a.saida).stem
    while t < total - 1e-3:
        d = min(a.bloco, total - t)
        fin, fout = wk / "in", wk / "out"
        for p in (fin, fout):
            shutil.rmtree(p, ignore_errors=True)
            p.mkdir()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", a.entrada, "-t", f"{d:.3f}",
                        "-fps_mode", "passthrough", str(fin / "%05d.png")], check=True)
        subprocess.run([str(RE), "-i", str(fin), "-o", str(fout), "-n", a.modelo, "-s", str(a.escala), "-f", "png"],
                       check=True, capture_output=True)
        bp = wk / f"b{k:04d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", str(fout / "%05d.png"),
                        "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", str(bp)], check=True)
        blocos.append(bp)
        t += d
        k += 1
        dec = time.time() - t0
        print(f"[{nome}] {t:.0f}/{total:.0f}s de vídeo | {t / total:.0%} | decorrido {fmt(dec)} | "
              f"falta ~{fmt(dec / t * (total - t))}", flush=True)
    lista = wk / "lista.txt"
    lista.write_text("".join(f"file '{b.as_posix()}'\n" for b in blocos), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-ss", "0",
                    "-t", f"{total:.3f}", "-i", a.entrada, "-map", "0:v", "-map", "1:a?", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-af", f"afade=t=out:st={max(0, total - 0.12):.3f}:d=0.12", "-shortest", a.saida], check=True)
    shutil.rmtree(wk, ignore_errors=True)
    print(f"ok: {a.saida} ({fmt(time.time() - t0)})", flush=True)


if __name__ == "__main__":
    main()
