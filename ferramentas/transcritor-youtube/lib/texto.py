# -*- coding: utf-8 -*-
"""Manipulação de texto, tempo e identificadores.

Tudo aqui é função pura: nada de rede, disco ou GPU. É de propósito — esta é a
parte que quebra em silêncio (um ID extraído errado faz o vídeo ser baixado de
novo; um timestamp deslocado inutiliza a transcrição para achar o hook), então
precisa ser testável sem depender do YouTube estar no ar.
"""
import json
import re

# O ID de vídeo do YouTube tem exatamente 11 caracteres do alfabeto base64-url.
_ID = r"[0-9A-Za-z_-]{11}"

_PADROES = [
    re.compile(r"[?&]v=(" + _ID + r")(?![0-9A-Za-z_-])"),
    re.compile(r"youtu\.be/(" + _ID + r")(?![0-9A-Za-z_-])"),
    re.compile(r"/shorts/(" + _ID + r")(?![0-9A-Za-z_-])"),
    re.compile(r"/embed/(" + _ID + r")(?![0-9A-Za-z_-])"),
    re.compile(r"/live/(" + _ID + r")(?![0-9A-Za-z_-])"),
]

_SO_ID = re.compile(r"^" + _ID + r"$")

_PROIBIDOS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def extrair_id(url):
    """Devolve o ID de 11 caracteres, ou None se a URL não aponta para um vídeo.

    Playlists e canais voltam None de propósito: eles precisam ser expandidos em
    vídeos pelo yt-dlp antes de virarem itens da fila, senão a fila guardaria uma
    entrada que nunca dá para transcrever.
    """
    if not url:
        return None
    url = url.strip()
    if not url:
        return None
    if _SO_ID.match(url):
        return url
    for p in _PADROES:
        m = p.search(url)
        if m:
            return m.group(1)
    return None


def e_lista(url):
    """A URL é de playlist ou canal (precisa ser expandida antes de entrar na fila)?"""
    if not url:
        return False
    u = url.strip().lower()
    if extrair_id(u):
        return False
    return ("youtube.com" in u or "youtu.be" in u) and (
        "list=" in u or "/@" in u or "/c/" in u or "/channel/" in u or "/user/" in u)


def formatar_tempo(segundos):
    """Segundos -> MM:SS, ou H:MM:SS quando passa de uma hora."""
    s = int(max(0, segundos or 0))
    h, resto = divmod(s, 3600)
    m, s = divmod(resto, 60)
    if h:
        return "%d:%02d:%02d" % (h, m, s)
    return "%02d:%02d" % (m, s)


def nome_arquivo_seguro(titulo, limite=120):
    """Título -> nome de arquivo que o Windows aceita.

    Mantém acentos (são legíveis e o NTFS lida bem), tira o que o Windows proíbe,
    e corta o fim. Nome terminando em ponto ou espaço é recusado sem aviso pelo
    Windows, por isso a limpeza final.
    """
    n = _PROIBIDOS.sub("", titulo or "")
    n = re.sub(r"\s+", " ", n).strip()
    n = n[:limite].strip(" .")
    return n or "sem-titulo"


def agrupar_blocos(segmentos, janela=30):
    """Junta segmentos curtos em blocos de ~`janela` segundos.

    A legenda do YouTube vem picada em trechos de 1 a 3 segundos, o que gera uma
    parede de timestamps ilegível. Agrupar por janela devolve algo que dá para
    ler e ainda permite localizar o trecho no vídeo.
    """
    blocos = []
    atual = None
    for s in segmentos or []:
        texto = (s.get("texto") or "").strip()
        if not texto:
            continue
        inicio = float(s.get("inicio") or 0)
        if atual is None or inicio - atual["inicio"] >= janela:
            atual = {"inicio": inicio, "partes": [texto]}
            blocos.append(atual)
        else:
            atual["partes"].append(texto)
    return [{"inicio": b["inicio"], "texto": " ".join(b["partes"])} for b in blocos]


def parse_json3(bruto):
    """Legenda no formato json3 do YouTube -> lista de segmentos.

    json3 é o formato preferido porque traz o tempo em milissegundos já separado,
    sem precisar parsear texto de timecode.
    """
    try:
        dados = json.loads(bruto)
    except (ValueError, TypeError):
        return []
    saida = []
    for ev in dados.get("events") or []:
        segs = ev.get("segs")
        if not segs:
            continue
        texto = "".join(x.get("utf8", "") for x in segs)
        texto = re.sub(r"\s+", " ", texto).strip()
        if not texto:
            continue
        saida.append({"inicio": (ev.get("tStartMs") or 0) / 1000.0, "texto": texto})
    return saida


_TIMECODE = re.compile(
    r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{1,3})\s*-->\s*"
    r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{1,3})")
_TAG = re.compile(r"<[^>]*>")


def parse_vtt(bruto):
    """Legenda WebVTT -> lista de segmentos. Usado quando json3 não está disponível."""
    segmentos = []
    inicio = None
    buffer = []

    def fechar():
        if inicio is None:
            return
        texto = re.sub(r"\s+", " ", " ".join(buffer)).strip()
        if texto:
            segmentos.append({"inicio": inicio, "texto": texto})

    for linha in (bruto or "").splitlines():
        m = _TIMECODE.search(linha)
        if m:
            fechar()
            h, mi, s, ms = m.group(1), m.group(2), m.group(3), m.group(4)
            inicio = int(h) * 3600 + int(mi) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000.0
            buffer = []
            continue
        if inicio is None:
            continue
        if not linha.strip():
            fechar()
            inicio, buffer = None, []
            continue
        buffer.append(_TAG.sub("", linha).strip())
    fechar()

    # A legenda automática repete a linha anterior em cada cue para dar efeito de
    # rolagem. Sem tirar isso, a transcrição sai com tudo duplicado.
    # Ao fundir, fica o texto mais completo (o do cue novo) com o tempo do mais
    # antigo: a fala começou ali, e é esse tempo que serve para achar o trecho
    # no vídeo depois.
    limpos = []
    for s in segmentos:
        if limpos and (s["texto"] == limpos[-1]["texto"]
                       or s["texto"].startswith(limpos[-1]["texto"] + " ")):
            limpos[-1] = {"inicio": limpos[-1]["inicio"], "texto": s["texto"]}
        else:
            limpos.append(s)
    return limpos
