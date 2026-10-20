# -*- coding: utf-8 -*-
"""Decide o que fazer com um video que a plataforma recusou.

Logica pura, sem tocar em disco nem chamar ffmpeg: recebe a medida de um video
e devolve o diagnostico e o plano. Fica separada do resto para poder ser testada
sem precisar de arquivo de verdade.

Duas regras governam o modulo:

1. **Subir resolucao nao cria detalhe e subir bitrate nao devolve qualidade
   perdida.** O arquivo passa a cumprir o minimo declarado, e e so isso. Um
   360x640 esticado para 540x960 continua com a nitidez de 360x640. Isso esta
   dito aqui porque quem le o codigo depois precisa saber que a ferramenta
   resolve a RECUSA, nao a qualidade.
2. **O bitrate tem de ser garantido, nao sugerido.** Com CRF o ffmpeg entrega o
   bitrate que achar suficiente, e em cena parada isso cai muito abaixo do
   minimo — o video seria recusado de novo. Por isso o plano fixa
   b:v = minrate = maxrate, que e o unico jeito de garantir o piso.
"""
import math

# Minimos da plataforma. Ficam aqui num lugar so porque mudam de tempos em
# tempos e sao a unica coisa que alguem vai querer ajustar sem ler o resto.
PERFIS = {
    "tiktok": {
        "nome": "TikTok Ads",
        "lado_curto_min": 540,
        "lado_longo_min": 960,
        "kbps_min": 350.0,
    },
    "meta": {
        # Meta aceita bem menos, mas serve para conferir o mesmo acervo contra
        # os dois destinos sem ter que medir duas vezes.
        "nome": "Meta Ads",
        "lado_curto_min": 500,
        "lado_longo_min": 500,
        "kbps_min": 0.0,
    },
}

# Quanto de bitrate por pixel por quadro. 0.08 e a faixa onde H.264 fica limpo
# em video de anuncio (muito corte, muito movimento) sem inflar o arquivo.
BPP_PADRAO = 0.08
# Piso proprio, bem acima do minimo da plataforma: se o alvo encostar nos 350 o
# arquivo passa raspando e qualquer remedicao do lado deles pode reprovar.
KBPS_PISO = 600.0


class Medida(object):
    """O que o ffprobe conseguiu ler de um video."""

    def __init__(self, largura, altura, kbps=None, fps=None,
                 codec_video=None, codec_audio=None, duracao=None):
        self.largura = largura
        self.altura = altura
        self.kbps = kbps
        self.fps = fps
        self.codec_video = codec_video
        self.codec_audio = codec_audio
        self.duracao = duracao

    @property
    def lado_curto(self):
        return min(self.largura, self.altura)

    @property
    def lado_longo(self):
        return max(self.largura, self.altura)

    def __repr__(self):
        return "Medida(%dx%d, %s kbps)" % (
            self.largura, self.altura,
            ("%.0f" % self.kbps) if self.kbps else "?")


def perfil(nome="tiktok"):
    return PERFIS[nome]


def avaliar(m, p):
    """Lista dos problemas. Vazia = o video passa.

    A comparacao e por lado curto e lado longo, nao por largura e altura: um
    video deitado de 1024x576 cumpre "pelo menos 540x960" tanto quanto um em pe
    de 576x1024, e tratar largura/altura ao pe da letra reprovaria o deitado
    sem motivo.
    """
    problemas = []
    if m.lado_curto < p["lado_curto_min"] or m.lado_longo < p["lado_longo_min"]:
        problemas.append("resolucao")
    if p["kbps_min"] > 0 and m.kbps is not None and m.kbps < p["kbps_min"]:
        problemas.append("bitrate")
    return problemas


def _par_acima(x):
    """Inteiro par >= x. H.264 com yuv420p exige dimensao par."""
    n = int(math.ceil(x))
    return n + (n % 2)


def escala_alvo(m, p):
    """(largura, altura) de saida, ou None se a resolucao ja serve.

    Mantem a proporcao: calcula um fator unico e aplica nos dois lados. Esticar
    so um lado para bater o minimo deformaria a imagem, e um anuncio deformado
    e pior do que um anuncio recusado.
    """
    fator = max(p["lado_curto_min"] / float(m.lado_curto),
                p["lado_longo_min"] / float(m.lado_longo))
    if fator <= 1.0:
        return None
    return _par_acima(m.largura * fator), _par_acima(m.altura * fator)


def bitrate_alvo(largura, altura, fps=None, bpp=BPP_PADRAO, piso=KBPS_PISO,
                 kbps_atual=None):
    """Bitrate de saida, em kbps.

    Sai do tamanho real do quadro, nao de um numero fixo: 540x960 e 1080x1920
    precisam de coisas muito diferentes. Nunca desce abaixo do piso nem abaixo
    do que o video ja tinha — reencodar para um bitrate menor so pioraria o
    arquivo, que e o oposto do pedido.
    """
    f = fps if (fps and fps > 0) else 30.0
    alvo = (largura * altura * f * bpp) / 1000.0
    alvo = max(alvo, piso)
    if kbps_atual:
        alvo = max(alvo, kbps_atual)
    return int(round(alvo))


class Plano(object):
    def __init__(self, precisa, problemas, escala=None, kbps=None,
                 copiar_audio=False):
        self.precisa = precisa
        self.problemas = problemas
        self.escala = escala
        self.kbps = kbps
        self.copiar_audio = copiar_audio

    def resumo(self):
        if not self.precisa:
            return "ja cumpre o minimo"
        partes = []
        if self.escala:
            partes.append("%dx%d" % self.escala)
        if self.kbps:
            partes.append("%d kbps" % self.kbps)
        return " · ".join(partes)


def planejar(m, p, bpp=BPP_PADRAO, piso=KBPS_PISO):
    """Do diagnostico ao que precisa ser feito."""
    problemas = avaliar(m, p)
    if not problemas:
        return Plano(False, problemas)

    esc = escala_alvo(m, p)
    larg, alt = esc if esc else (m.largura, m.altura)
    kbps = bitrate_alvo(larg, alt, m.fps, bpp, piso, m.kbps)
    # Audio so e reencodado quando nao e AAC: mexer num audio que ja esta no
    # formato certo so adiciona uma geracao de perda.
    copiar = (m.codec_audio or "").lower() == "aac"
    return Plano(True, problemas, esc, kbps, copiar)


def comando_ffmpeg(entrada, saida, plano, ffmpeg="ffmpeg"):
    """Linha de comando completa. Nunca escreve por cima da entrada."""
    if os_path_igual(entrada, saida):
        raise ValueError("saida nao pode ser igual a entrada: %s" % entrada)

    cmd = [ffmpeg, "-y", "-i", entrada]

    if plano.escala:
        # lanczos porque o padrao (bicubic) deixa o upscale mais borrado;
        # nenhum dos dois inventa detalhe, mas este fica menos mole.
        cmd += ["-vf", "scale=%d:%d:flags=lanczos" % plano.escala]

    cmd += ["-c:v", "libx264", "-preset", "medium",
            "-profile:v", "high", "-pix_fmt", "yuv420p"]

    # O trio b:v/minrate/maxrate e o que transforma o bitrate em piso garantido.
    # bufsize no dobro deixa o codificador respirar em cena de muito movimento
    # sem deixar a media cair.
    k = plano.kbps
    cmd += ["-b:v", "%dk" % k, "-minrate", "%dk" % k,
            "-maxrate", "%dk" % k, "-bufsize", "%dk" % (k * 2)]

    if plano.copiar_audio:
        cmd += ["-c:a", "copy"]
    else:
        cmd += ["-c:a", "aac", "-b:a", "128k", "-ar", "44100"]

    # faststart move o indice para o comeco: sem isso o player do gerenciador
    # de anuncios so comeca a mostrar depois de baixar o arquivo inteiro.
    cmd += ["-movflags", "+faststart", saida]
    return cmd


def os_path_igual(a, b):
    import os
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))
