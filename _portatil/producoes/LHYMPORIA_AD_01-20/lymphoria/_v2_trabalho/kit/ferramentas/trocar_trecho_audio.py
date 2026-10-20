# -*- coding: utf-8 -*-
"""Troca um trecho da fala de um vídeo por uma fala nova (ex.: voz clonada dizendo outra marca),
ajustando a velocidade da fala nova para caber exatamente no mesmo tempo (vídeo não dessincroniza).

  python trocar_trecho_audio.py entrada.mp4 nova_fala.mp3 saida.mp4 --de 179.8 --ate 183.5
- Ajuste de velocidade limitado a 0,8x–1,25x (avisa se precisar mais).
- Cruzamento de 40 ms nas bordas para não estalar. Vídeo copiado sem reencode.
"""
from __future__ import annotations

import argparse
import subprocess


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("fala")
    ap.add_argument("saida")
    ap.add_argument("--de", type=float, required=True)
    ap.add_argument("--ate", type=float, required=True)
    a = ap.parse_args()
    alvo = a.ate - a.de
    df = dur(a.fala)
    # fala curta: desacelera no máx. até 0,85x (soa natural) e o resto vira pausa no fim
    tempo = max(0.85, df / alvo) if df <= alvo else min(1.25, df / alvo)
    if abs(tempo - df / alvo) > 1e-3:
        print(f"aviso: fala nova {df:.2f}s para {alvo:.2f}s exigiria {df / alvo:.2f}x; limitei a {tempo:.2f}x")
    fc = (f"[0:a]atrim=0:{a.de},asetpts=PTS-STARTPTS[a0];"
          f"[0:a]atrim={a.ate},asetpts=PTS-STARTPTS[a2];"
          f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atempo={tempo:.4f},apad,atrim=0:{alvo},"
          f"loudnorm=I=-16:TP=-1.5[a1];"
          f"[a0]aresample=48000,aformat=channel_layouts=stereo[b0];[a2]aresample=48000,aformat=channel_layouts=stereo[b2];"
          f"[b0][a1]acrossfade=d=0.04[x];[x][b2]acrossfade=d=0.04[o]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.entrada, "-i", a.fala, "-filter_complex", fc,
                    "-map", "0:v", "-map", "[o]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", a.saida], check=True)
    print(f"ok: {a.saida} | trecho {a.de:.2f}-{a.ate:.2f}s trocado (velocidade {tempo:.2f}x)")


if __name__ == "__main__":
    main()
