# -*- coding: utf-8 -*-
"""Le as caracteristicas de um video com ffprobe.

Separado da logica de correcao de proposito: aqui mora toda a sujeira de lidar
com arquivo de verdade (container que mente, stream sem bitrate declarado,
arquivo corrompido), e do outro lado fica a decisao, que e testavel sem disco.
"""
import json
import os
import subprocess

from .correcao import Medida

EXTENSOES = (".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v",
             ".mpeg", ".mpg", ".wmv", ".flv", ".ts")


class ErroSonda(Exception):
    pass


def _fracao(txt):
    """'30000/1001' -> 29.97. O ffprobe devolve fps como fracao."""
    if not txt:
        return None
    try:
        if "/" in txt:
            a, b = txt.split("/")
            return float(a) / float(b) if float(b) else None
        return float(txt)
    except (ValueError, ZeroDivisionError):
        return None


def medir(caminho, ffprobe="ffprobe", timeout=60):
    """Medida do video, ou ErroSonda se o arquivo nao for legivel."""
    cmd = [ffprobe, "-v", "error",
           "-show_entries",
           "stream=codec_type,codec_name,width,height,bit_rate,avg_frame_rate",
           "-show_entries", "format=bit_rate,duration,size",
           "-of", "json", caminho]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise ErroSonda(str(e))
    if r.returncode != 0:
        msg = r.stderr.decode("utf-8", "replace").strip().splitlines()
        raise ErroSonda(msg[-1] if msg else "ffprobe falhou")
    try:
        d = json.loads(r.stdout.decode("utf-8", "replace"))
    except ValueError as e:
        raise ErroSonda("saida do ffprobe ilegivel: %s" % e)

    v = a = None
    for s in d.get("streams") or []:
        if s.get("codec_type") == "video" and v is None:
            v = s
        elif s.get("codec_type") == "audio" and a is None:
            a = s
    if not v or not v.get("width") or not v.get("height"):
        raise ErroSonda("sem stream de video")

    fmt = d.get("format") or {}

    # O bitrate do stream e o numero certo, mas varios containers (webm, mkv,
    # e mp4 gerado por ferramenta de IA) simplesmente nao declaram. Nesse caso
    # cai para o do container e, em ultimo caso, calcula por tamanho/duracao —
    # que inclui o audio e portanto superestima um pouco. Superestimar aqui e o
    # erro seguro: no maximo a ferramenta deixa de corrigir um video limitrofe,
    # em vez de corrigir um que estava bom.
    kbps = None
    for origem in (v.get("bit_rate"), fmt.get("bit_rate")):
        try:
            if origem:
                kbps = float(origem) / 1000.0
                break
        except (TypeError, ValueError):
            pass
    if kbps is None:
        try:
            kbps = (float(fmt["size"]) * 8 / float(fmt["duration"])) / 1000.0
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            kbps = None

    try:
        dur = float(fmt.get("duration")) if fmt.get("duration") else None
    except (TypeError, ValueError):
        dur = None

    return Medida(
        largura=int(v["width"]), altura=int(v["height"]), kbps=kbps,
        fps=_fracao(v.get("avg_frame_rate")),
        codec_video=v.get("codec_name"),
        codec_audio=a.get("codec_name") if a else None,
        duracao=dur)


def listar_videos(pasta, recursivo=True):
    """Caminhos de video dentro da pasta, em ordem."""
    achados = []
    if recursivo:
        for raiz, dirs, arqs in os.walk(pasta):
            dirs[:] = [d for d in dirs if d not in ("corrigidos", "__pycache__")]
            for a in arqs:
                if a.lower().endswith(EXTENSOES):
                    achados.append(os.path.join(raiz, a))
    else:
        for a in os.listdir(pasta):
            p = os.path.join(pasta, a)
            if os.path.isfile(p) and a.lower().endswith(EXTENSOES):
                achados.append(p)
    return sorted(achados)
