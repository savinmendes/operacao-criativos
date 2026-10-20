# -*- coding: utf-8 -*-
"""Remove legenda/texto queimado (ou marca d'água) de uma faixa do vídeo.

Modos:
  inpaint (padrão) -> detecta os pixels de texto (claros/amarelos com contorno escuro) dentro da faixa
                      e reconstrói com OpenCV (bom para legenda branca/amarela sobre fundo variado)
  blur             -> desfoca a faixa inteira (rápido, deixa mancha)
  delogo           -> filtro delogo do ffmpeg num retângulo (bom para logo fixo pequeno)
  cortar           -> recorta e reescala para tirar a faixa (perde parte do quadro)

Coordenadas sempre no tamanho ORIGINAL do vídeo. Use --preview para salvar um frame com a máscara.

Exemplos:
  python remover_legenda.py in.mp4 out.mp4 --faixa 0,1250,1080,350
  python remover_legenda.py in.mp4 out.mp4 --faixa 120,600,480,200 --modo delogo
  python remover_legenda.py in.mp4 out.mp4 --faixa 0,1250,1080,350 --preview mascara.png
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from comum import run, info, tem_audio  # noqa: E402


def mascara_texto(roi: np.ndarray, sens: int = 200) -> np.ndarray:
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    v, s, h = hsv[..., 2], hsv[..., 1], hsv[..., 0]
    branco = (v >= sens) & (s <= 60)
    amarelo = (h >= 18) & (h <= 40) & (s >= 120) & (v >= 170)
    m = ((branco | amarelo) * 255).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    return cv2.dilate(m, np.ones((7, 7), np.uint8), iterations=2)   # pega o contorno preto junto


def inpaint(entrada: str, saida: str, faixa, sens: int = 200, raio: int = 5):
    x, y, w, h = faixa
    st = [s for s in info(entrada)["streams"] if s["codec_type"] == "video"][0]
    W, H = int(st["width"]), int(st["height"])
    num, den = st["r_frame_rate"].split("/")
    fps = float(num) / float(den)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", entrada, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                           stdout=subprocess.PIPE)
    tmp = str(Path(saida).with_suffix(".tmp.mp4"))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", f"{fps}", "-i", "-", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                            "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    n = W * H * 3
    while True:
        buf = dec.stdout.read(n)
        if len(buf) < n:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
        roi = fr[y:y + h, x:x + w]
        m = mascara_texto(roi, sens)
        if m.any():
            fr[y:y + h, x:x + w] = cv2.inpaint(roi, m, raio, cv2.INPAINT_TELEA)
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    if tem_audio(entrada):
        run(["ffmpeg", "-i", tmp, "-i", entrada, "-map", "0:v", "-map", "1:a", "-c", "copy", saida])
        Path(tmp).unlink()
    else:
        Path(tmp).replace(saida)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada"); ap.add_argument("saida")
    ap.add_argument("--faixa", required=True, help="x,y,largura,altura da área com o texto")
    ap.add_argument("--modo", choices=["inpaint", "blur", "delogo", "cortar"], default="inpaint")
    ap.add_argument("--sens", type=int, default=200, help="brilho mínimo do texto (inpaint); baixe se sobrar texto")
    ap.add_argument("--preview", help="salva um frame do meio com a máscara em vermelho e não processa")
    a = ap.parse_args()
    x, y, w, h = [int(v) for v in a.faixa.split(",")]

    if a.preview:
        t = float(info(a.entrada)["format"]["duration"]) / 2
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", a.entrada, "-frames:v", "1",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        fr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        m = mascara_texto(fr[y:y + h, x:x + w], a.sens)
        fr[y:y + h, x:x + w][m > 0] = (0, 0, 255)
        cv2.rectangle(fr, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.imwrite(a.preview, fr)
        print("preview salvo:", a.preview)
        return

    if a.modo == "inpaint":
        inpaint(a.entrada, a.saida, (x, y, w, h), a.sens)
    elif a.modo == "blur":
        run(["ffmpeg", "-i", a.entrada, "-filter_complex",
             f"[0:v]split[a][b];[b]crop={w}:{h}:{x}:{y},boxblur=20:2[bl];[a][bl]overlay={x}:{y}[v]",
             "-map", "[v]", "-map", "0:a?", "-c:a", "copy", "-crf", "18", a.saida])
    elif a.modo == "delogo":
        run(["ffmpeg", "-i", a.entrada, "-vf", f"delogo=x={x}:y={y}:w={w}:h={h}",
             "-c:a", "copy", "-crf", "18", a.saida])
    else:  # cortar: mantém tudo acima da faixa (texto embaixo) e volta ao tamanho original
        st = [s for s in info(a.entrada)["streams"] if s["codec_type"] == "video"][0]
        W, H = int(st["width"]), int(st["height"])
        keep_h = y if y > H / 2 else H - (y + h)
        top = 0 if y > H / 2 else y + h
        keep_w = int(keep_h * W / H) // 2 * 2
        run(["ffmpeg", "-i", a.entrada, "-vf",
             f"crop={keep_w}:{keep_h}:{(W - keep_w) // 2}:{top},scale={W}:{H}:flags=lanczos",
             "-c:a", "copy", "-crf", "18", a.saida])
    print("ok:", a.saida)


if __name__ == "__main__":
    main()
