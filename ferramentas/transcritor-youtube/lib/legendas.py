# -*- coding: utf-8 -*-
"""Caminho A: pega a legenda que o YouTube já tem.

É sempre a primeira tentativa porque custa segundos e zero GPU. A legenda manual
(feita por gente) vem antes da automática; dentro de cada tipo, a ordem de idioma
é português primeiro, porque é o que a operação usa.
"""
import requests

import yt_dlp

from .texto import parse_json3, parse_vtt

IDIOMAS = ["pt", "pt-BR", "pt-PT", "pt-orig", "es", "es-419", "en", "en-US", "en-orig"]

_OPCOES_BASE = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "noprogress": True,
}


class ErroYoutube(Exception):
    pass


def info_video(url):
    """Metadados do vídeo, sem baixar nada."""
    try:
        with yt_dlp.YoutubeDL(dict(_OPCOES_BASE)) as y:
            return y.extract_info(url, download=False)
    except Exception as e:                       # yt-dlp levanta vários tipos
        raise ErroYoutube(str(e).strip().splitlines()[0] if str(e) else repr(e))


def expandir(url):
    """Playlist ou canal -> lista de URLs de vídeo.

    Usa extract_flat: sem isso o yt-dlp abriria cada vídeo da playlist só para
    montar a lista, o que num canal inteiro leva minutos.
    """
    op = dict(_OPCOES_BASE)
    op["extract_flat"] = "in_playlist"
    try:
        with yt_dlp.YoutubeDL(op) as y:
            info = y.extract_info(url, download=False)
    except Exception as e:
        raise ErroYoutube(str(e).strip().splitlines()[0] if str(e) else repr(e))

    urls = []

    def caminhar(no):
        if not isinstance(no, dict):
            return
        if no.get("_type") in ("playlist", "multi_video"):
            for filho in no.get("entries") or []:
                caminhar(filho)
            return
        vid = no.get("id")
        if vid:
            urls.append("https://www.youtube.com/watch?v=" + vid)

    caminhar(info)
    return urls


def _ranque_idioma(lang, idiomas, original):
    """Posição do idioma na preferência. Menor é melhor.

    O idioma original do vídeo vem sempre na frente, mesmo que a lista de
    preferência diga outra coisa: transcrição traduzida serve para entender o
    assunto, não para estudar a copy, que é o uso aqui.
    """
    base = (lang or "").lower()
    curto = base.split("-")[0]
    if original:
        o = original.lower()
        if base == o or curto == o.split("-")[0]:
            return -1
    for i, pref in enumerate(idiomas):
        p = pref.lower()
        if base == p or curto == p.split("-")[0]:
            return i
    return len(idiomas) + 1


def _baixar(formatos):
    """Baixa a faixa preferindo json3 (tempo já em ms) e caindo para vtt."""
    por_ext = {}
    for f in formatos or []:
        if f.get("url"):
            por_ext.setdefault(f.get("ext"), f["url"])
    for ext in ("json3", "srv3", "vtt", "srt"):
        url = por_ext.get(ext)
        if not url:
            continue
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
        except requests.RequestException:
            continue
        bruto = r.text
        segs = parse_json3(bruto) if ext in ("json3", "srv3") else parse_vtt(bruto)
        if segs:
            return segs
    return None


def buscar(info, idiomas=None, max_tentativas=6, baixar=None):
    """Tenta extrair a legenda do dicionário de info do yt-dlp.

    Devolve (segmentos, idioma, tipo) ou (None, None, None) se o vídeo não tem
    legenda alguma — caso em que o chamador cai para o Whisper.

    A ordenação é por idioma PRIMEIRO e só depois por manual/automática. Parece
    detalhe, mas inverter isso quebra o caso comum de canal brasileiro que sobe
    legenda manual só em inglês para alcance: a regra "manual sempre ganha"
    escolheria a tradução em inglês e descartaria a legenda automática em
    português, que é a fala de verdade. Dentro do mesmo idioma, aí sim a manual
    ganha — tem pontuação e acerta nome de produto.
    """
    idiomas = idiomas or IDIOMAS
    original = info.get("language")
    baixar = baixar or _baixar

    candidatos = []
    for tipo, chave, peso in (("legenda", "subtitles", 0),
                              ("auto-legenda", "automatic_captions", 1)):
        for lang, formatos in (info.get(chave) or {}).items():
            if not formatos:
                continue
            r = _ranque_idioma(lang, idiomas, original)
            if r > len(idiomas):          # idioma que ninguém pediu: só se não houver mais nada
                r = len(idiomas) + 1
            candidatos.append((r, peso, lang, tipo, formatos))

    candidatos.sort(key=lambda c: (c[0], c[1]))

    # Teto de tentativas. O YouTube oferece ~157 idiomas de auto-legenda por vídeo,
    # quase todos tradução automática do original. Sem teto, um vídeo cujo download
    # esteja falhando faz o código tentar centenas de URLs em sequência — o que
    # martela o YouTube e provoca exatamente o bloqueio por volume que fez as
    # requisições começarem a pendurar. As primeiras tentativas já são as de melhor
    # idioma; se nenhuma delas responde, o problema não é a lista, é a conexão.
    for _, _, lang, tipo, formatos in candidatos[:max_tentativas]:
        segs = baixar(formatos)
        if segs:
            return segs, lang, tipo
    return None, None, None
