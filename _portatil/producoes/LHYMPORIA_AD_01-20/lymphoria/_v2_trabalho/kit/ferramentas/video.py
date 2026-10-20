# -*- coding: utf-8 -*-
"""Operações de vídeo do dia a dia.

  vertical   -> converte qualquer vídeo para 1080x1920/30fps preenchendo o quadro (sem barra preta)
  dividida   -> tela dividida SEM borda: vídeo de cima + vídeo de baixo (ex.: avatar em cima, b-roll embaixo)
  montagem   -> junta trechos (arquivo,início,fim) em sequência, com velocidade opcional (hook rápido)
  hook       -> substitui a imagem dos primeiros N s de um corpo por um hook (o áudio do corpo continua)
  takes      -> b-roll sem repetir: cada take com 4–5 s (câmera lenta até 0,5× se o trecho for curto)
  concat     -> une vídeos já no mesmo padrão (concat demuxer, sem reencode)

Exemplos:
  python video.py vertical in.mp4 -o out.mp4
  python video.py dividida avatar.mp4 broll.mp4 -o split.mp4 --proporcao 0.5 --audio cima
  python video.py montagem "a.mp4,0.9,1.6" "b.mp4,1.2,2.7" -o hook.mp4 --vel 1.3
  python video.py hook corpo.mp4 hook.mp4 -o ad.mp4
  python video.py takes narr.wav t1.mp4 t2.mp4 t3.mp4 -o broll.mp4 --alvo 4.8
  python video.py concat p1.mp4 p2.mp4 -o final.mp4
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import W, H, FPS, run, dur, tmpdir, vf_vertical, tem_audio  # noqa: E402

ENC = ["-c:v", "libx264", "-threads", "4", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def vertical(entrada: str, saida: str):
    run(["ffmpeg", "-i", entrada, "-vf", vf_vertical(), *ENC, "-c:a", "aac", "-b:a", "160k", "-ar", "48000", saida])
    return saida


def dividida(cima: str, baixo: str, saida: str, proporcao: float = 0.5, audio: str = "cima"):
    """Sem borda nem linha: cada metade é recortada para preencher; duração = vídeo que dá o áudio."""
    h1 = int(H * proporcao) // 2 * 2
    h2 = H - h1
    fonte_audio = cima if audio == "cima" else baixo
    t = dur(fonte_audio)
    idx = 0 if audio == "cima" else 1
    args = ["ffmpeg", "-i", cima, "-stream_loop", "-1", "-i", baixo] if audio == "cima" else \
           ["ffmpeg", "-stream_loop", "-1", "-i", cima, "-i", baixo]
    fc = (f"[0:v]scale={W}:{h1}:force_original_aspect_ratio=increase,crop={W}:{h1},setsar=1,fps={FPS}[a];"
          f"[1:v]scale={W}:{h2}:force_original_aspect_ratio=increase,crop={W}:{h2},setsar=1,fps={FPS}[b];"
          f"[a][b]vstack=inputs=2[v]")
    amap = ["-map", f"{idx}:a?"]
    run(args + ["-filter_complex", fc, "-map", "[v]", *amap, "-t", f"{t}", *ENC,
                "-c:a", "aac", "-b:a", "160k", saida])
    return saida


def montagem(trechos: list[tuple[str, float, float]], saida: str, vel: float = 1.0):
    wk = tmpdir("mont_")
    partes = []
    for i, (f, a, b) in enumerate(trechos):
        o = wk / f"p{i}.mp4"
        run(["ffmpeg", "-ss", f"{a}", "-t", f"{b - a}", "-i", f, "-an", "-vf",
             f"setpts=(PTS-STARTPTS)/{vel}," + vf_vertical(), *ENC, o])
        partes.append(o)
    return concat([str(p) for p in partes], saida)


def hook(corpo: str, video_hook: str, saida: str, ate: float | None = None):
    """Imagem do hook por cima dos primeiros `ate` s (padrão: duração do hook). Som do corpo intacto."""
    ate = ate or dur(video_hook)
    run(["ffmpeg", "-i", corpo, "-i", video_hook, "-filter_complex",
         f"[0:v]{vf_vertical()}[c];[1:v]trim=0:{ate},setpts=PTS-STARTPTS,{vf_vertical()}[h];"
         f"[c][h]overlay=0:0:eof_action=pass[v]",
         "-map", "[v]", "-map", "0:a?", *ENC, "-c:a", "aac", "-b:a", "160k", saida])
    return saida


def takes(audio: str, arquivos: list[str], saida: str, alvo: float = 4.8):
    """Cobre a duração do áudio com takes diferentes (nunca repete). Velocidade = máx(0,5; mín(1; dur/alvo))."""
    total, t, i = dur(audio), 0.0, 0
    wk = tmpdir("tk_")
    partes = []
    while t < total - 0.05:
        if i >= len(arquivos):
            raise SystemExit(f"Faltam takes: cobri {t:.1f}s de {total:.1f}s com {len(arquivos)} takes (não repito take).")
        f = arquivos[i]
        d = dur(f)
        vel = max(0.5, min(1.0, d / alvo))
        tela = min(alvo, d / vel, total - t)
        o = wk / f"t{i}.mp4"
        run(["ffmpeg", "-i", f, "-an", "-t", f"{tela * vel:.3f}", "-vf",
             f"setpts=(PTS-STARTPTS)/{vel}," + vf_vertical(), *ENC, o])
        partes.append(str(o))
        t += tela
        i += 1
    v = wk / "v.mp4"
    concat(partes, str(v))
    run(["ffmpeg", "-i", v, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "160k", "-shortest", saida])
    print(f"{i} takes, {total:.1f}s")
    return saida


def concat(arquivos: list[str], saida: str):
    wk = tmpdir("cc_")
    lst = wk / "l.txt"
    lst.write_text("".join(f"file '{Path(a).resolve().as_posix()}'\n" for a in arquivos), encoding="utf-8")
    run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", saida])
    return saida


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    v = sp.add_parser("vertical"); v.add_argument("entrada"); v.add_argument("-o", required=True)
    d = sp.add_parser("dividida"); d.add_argument("cima"); d.add_argument("baixo"); d.add_argument("-o", required=True)
    d.add_argument("--proporcao", type=float, default=0.5); d.add_argument("--audio", choices=["cima", "baixo"], default="cima")
    m = sp.add_parser("montagem"); m.add_argument("trechos", nargs="+", help='"arquivo,ini,fim"'); m.add_argument("-o", required=True)
    m.add_argument("--vel", type=float, default=1.0)
    h = sp.add_parser("hook"); h.add_argument("corpo"); h.add_argument("hook"); h.add_argument("-o", required=True)
    h.add_argument("--ate", type=float)
    t = sp.add_parser("takes"); t.add_argument("audio"); t.add_argument("arquivos", nargs="+"); t.add_argument("-o", required=True)
    t.add_argument("--alvo", type=float, default=4.8)
    c = sp.add_parser("concat"); c.add_argument("arquivos", nargs="+"); c.add_argument("-o", required=True)
    a = ap.parse_args()
    if a.cmd == "vertical":
        vertical(a.entrada, a.o)
    elif a.cmd == "dividida":
        dividida(a.cima, a.baixo, a.o, a.proporcao, a.audio)
    elif a.cmd == "montagem":
        tr = [(x.split(",")[0], float(x.split(",")[1]), float(x.split(",")[2])) for x in a.trechos]
        montagem(tr, a.o, a.vel)
    elif a.cmd == "hook":
        hook(a.corpo, a.hook, a.o, a.ate)
    elif a.cmd == "takes":
        takes(a.audio, a.arquivos, a.o, a.alvo)
    else:
        concat(a.arquivos, a.o)
    print("ok:", a.o)


if __name__ == "__main__":
    main()
