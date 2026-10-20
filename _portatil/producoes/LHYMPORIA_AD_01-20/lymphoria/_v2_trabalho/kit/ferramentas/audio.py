# -*- coding: utf-8 -*-
"""Áudio dos criativos.

  mix        -> narração a -15 LUFS + trilha baixa (-29 LUFS, corte em 2,5 kHz, abaixa sozinha quando a voz entra)
  trocar     -> põe um áudio novo (narração) num vídeo, cortando/estendendo para caber
  pausas     -> corta as pausas longas da fala (vídeo + áudio juntos), deixa respiros curtos
  normalizar -> só deixa a voz em -15 LUFS

Exemplos:
  python audio.py mix narr.wav trilha.mp3 -o mix.wav
  python audio.py trocar video.mp4 narr.mp3 -o video_narrado.mp4 [--trilha trilha.mp3]
  python audio.py pausas video.mp4 -o sem_pausas.mp4 --min 0.35 --manter 0.12
  python audio.py normalizar narr.mp3 -o narr_norm.wav
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import run, dur, tmpdir, vf_vertical  # noqa: E402
from legenda import _pausas  # noqa: E402

VOZ_LUFS, MUSICA_LUFS = -15, -29


def normalizar(voz: str, saida: str, lufs: float = VOZ_LUFS):
    run(["ffmpeg", "-i", voz, "-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", saida])
    return saida


def mix(voz: str, trilha: str, saida: str, total: float | None = None, musica_lufs: float = MUSICA_LUFS):
    total = total or dur(voz)
    run(["ffmpeg", "-i", voz, "-stream_loop", "-1", "-i", trilha, "-filter_complex",
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total},asetpts=N/SR/TB,"
         f"loudnorm=I={musica_lufs}:TP=-6:LRA=11,equalizer=f=2500:t=q:w=1.2:g=-5,afade=t=in:d=0.3,"
         f"afade=t=out:st={max(0, total - 1.5):.2f}:d=1.5[m];"
         f"[0:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I={VOZ_LUFS}:TP=-1.5:LRA=11,"
         f"apad=whole_dur={total},asplit=2[v][vk];"
         f"[m][vk]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=300[md];"
         f"[v][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89[a]",
         "-map", "[a]", "-ar", "48000", "-t", f"{total}", saida])
    return saida


def trocar(video: str, audio: str, saida: str, trilha: str | None = None):
    """Vídeo fica com a duração do áudio (corta o vídeo ou congela o último frame)."""
    t = dur(audio)
    wk = tmpdir("aud_")
    a = str(wk / "a.wav")
    if trilha:
        mix(audio, trilha, a, t)
    else:
        normalizar(audio, a)
    run(["ffmpeg", "-i", video, "-i", a, "-filter_complex",
         f"[0:v]tpad=stop_mode=clone:stop_duration={t},trim=0:{t},setpts=PTS-STARTPTS[v]",
         "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-threads", "4", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-shortest", saida])
    return saida


def cortar_pausas(video: str, saida: str, min_pausa: float = 0.35, manter: float = 0.12):
    """Remove silêncios >= min_pausa, deixando `manter` s de respiro em cada lado do corte."""
    total = dur(video)
    keep, t = [], 0.0
    for a, b in _pausas(video, min_pausa):
        fim = min(total, a + manter)
        if fim > t:
            keep.append((t, fim))
        t = max(t, b - manter)
    if t < total:
        keep.append((t, total))
    fc = []
    for i, (a, b) in enumerate(keep):
        fc.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];"
                  f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                  f"afade=t=out:st={max(0, b - a - 0.02):.3f}:d=0.02[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=1[v][a]")
    run(["ffmpeg", "-i", video, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-threads", "4", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", saida])
    print(f"{total:.2f}s -> {dur(saida):.2f}s ({len(keep)} trechos)")
    return saida


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    m = sp.add_parser("mix"); m.add_argument("voz"); m.add_argument("trilha"); m.add_argument("-o", required=True)
    t = sp.add_parser("trocar"); t.add_argument("video"); t.add_argument("audio"); t.add_argument("-o", required=True)
    t.add_argument("--trilha")
    p = sp.add_parser("pausas"); p.add_argument("video"); p.add_argument("-o", required=True)
    p.add_argument("--min", type=float, default=0.35); p.add_argument("--manter", type=float, default=0.12)
    n = sp.add_parser("normalizar"); n.add_argument("voz"); n.add_argument("-o", required=True)
    a = ap.parse_args()
    if a.cmd == "mix":
        mix(a.voz, a.trilha, a.o)
    elif a.cmd == "trocar":
        trocar(a.video, a.audio, a.o, a.trilha)
    elif a.cmd == "pausas":
        cortar_pausas(a.video, a.o, a.min, a.manter)
    else:
        normalizar(a.voz, a.o)
    print("ok:", a.o)


if __name__ == "__main__":
    main()
