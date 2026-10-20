# -*- coding: utf-8 -*-
"""Caminho B: transcreve o áudio localmente com faster-whisper.

Só entra quando o vídeo não tem legenda nenhuma. Baixa apenas a faixa de áudio
(não o vídeo), transcreve e apaga o arquivo — o disco desta máquina é curto e um
lote de 200 vídeos em mp4 encheria tudo.

O import de faster_whisper é preguiçoso de propósito: quem só usa legenda não
precisa ter a biblioteca instalada nem esperar o carregamento do CUDA.
"""
import os
import shutil
import tempfile

import yt_dlp

_MODELO = None
_DISPOSITIVO = None
_CHAVE = None
_DLLS_REGISTRADAS = False


class ErroWhisper(Exception):
    pass


def _registrar_dlls_cuda():
    """Ensina o Windows a achar as DLLs do CUDA instaladas via pip.

    O ctranslate2 carrega cublas64_12.dll e as do cuDNN em tempo de execução, e
    são elas que vêm nos pacotes nvidia-cublas-cu12 / nvidia-cudnn-cu12. Ficam
    dentro de site-packages/nvidia/*/bin, que não está em lugar nenhum que o
    Windows procure sozinho.

    Precisa dos dois registros. `add_dll_directory` cobre quem carrega com as
    flags novas de busca; o PATH cobre o ctranslate2, que não usa. Só o primeiro
    não resolve — foi assim que este bug apareceu.

    E precisa rodar ANTES de qualquer import de faster_whisper/ctranslate2, por
    isso é chamado na importação deste módulo e não dentro de carregar(). Sem
    isso o modelo é construído com device='cuda' sem reclamar e só estoura na
    primeira transcrição, com o lote já rodando.
    """
    global _DLLS_REGISTRADAS
    if _DLLS_REGISTRADAS:
        return
    _DLLS_REGISTRADAS = True
    try:
        import nvidia
    except ImportError:
        return
    achados = []
    for base in list(getattr(nvidia, "__path__", [])):
        for raiz, _, arquivos in os.walk(base):
            if any(a.lower().endswith(".dll") for a in arquivos):
                achados.append(raiz)
                if hasattr(os, "add_dll_directory"):
                    try:
                        os.add_dll_directory(raiz)
                    except OSError:
                        pass
    if achados:
        os.environ["PATH"] = os.pathsep.join(achados) + os.pathsep + os.environ.get("PATH", "")


_registrar_dlls_cuda()


def disponivel():
    try:
        import faster_whisper  # noqa: F401
        return True
    except ImportError:
        return False


def _testar_de_verdade(modelo):
    """Roda o encoder em 1 segundo de silêncio para provar que a GPU funciona.

    Construir WhisperModel(device='cuda') não prova nada: o carregamento das
    bibliotecas CUDA é preguiçoso e só falha lá na frente. Melhor descobrir agora,
    em um segundo de áudio, do que no vídeo 47 de um lote de 200.
    """
    import numpy as np
    silencio = np.zeros(16000, dtype=np.float32)
    segmentos, _ = modelo.transcribe(silencio, vad_filter=False, beam_size=1)
    list(segmentos)      # transcribe é preguiçoso; consumir força o encoder a rodar


def carregar(tamanho="large-v3", dispositivo="auto", avisar=None):
    """Carrega o modelo uma vez por processo. Devolve (modelo, dispositivo).

    O cache é chaveado pelo par (tamanho, dispositivo) pedido. Guardar só o
    modelo faria a segunda chamada com outro tamanho devolver o anterior em
    silêncio, e o rótulo gravado na transcrição mentiria sobre o que a produziu.
    """
    global _MODELO, _DISPOSITIVO, _CHAVE
    if _MODELO is not None and _CHAVE == (tamanho, dispositivo):
        return _MODELO, _DISPOSITIVO

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise ErroWhisper(
            "faster-whisper não está instalado. Rode: pip install faster-whisper")

    if dispositivo == "cuda":
        tentativas = [("cuda", "float16")]
    elif dispositivo == "cpu":
        tentativas = [("cpu", "int8")]
    else:
        tentativas = [("cuda", "float16"), ("cpu", "int8")]

    ultimo = None
    for disp, precisao in tentativas:
        try:
            m = WhisperModel(tamanho, device=disp, compute_type=precisao)
            _testar_de_verdade(m)
        except Exception as e:
            ultimo = e
            if disp == "cuda" and avisar:
                avisar("GPU indisponível (%s). Caindo para CPU, que é bem mais "
                       "lenta. Para resolver: pip install nvidia-cublas-cu12 "
                       "nvidia-cudnn-cu12" % str(e).strip().splitlines()[0][:90])
            continue
        _MODELO, _DISPOSITIVO, _CHAVE = m, disp, (tamanho, dispositivo)
        return _MODELO, _DISPOSITIVO

    raise ErroWhisper("não consegui carregar o modelo: %s" % ultimo)


def baixar_audio(url, destino):
    """Baixa só a faixa de áudio. Devolve o caminho do arquivo gerado."""
    opcoes = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(destino, "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        # m4a a 64k é de sobra para fala e mantém o arquivo pequeno; o Whisper
        # reamostra para 16 kHz mono internamente de qualquer jeito.
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "64",
        }],
    }
    try:
        with yt_dlp.YoutubeDL(opcoes) as y:
            y.download([url])
    except Exception as e:
        raise ErroWhisper(str(e).strip().splitlines()[0] if str(e) else repr(e))

    arquivos = [os.path.join(destino, f) for f in os.listdir(destino)]
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    if not arquivos:
        raise ErroWhisper("o download não gerou arquivo de áudio")
    return max(arquivos, key=os.path.getsize)


def transcrever_arquivo(caminho, tamanho="large-v3", idioma=None,
                        dispositivo="auto", avisar=None):
    """Transcreve um arquivo de vídeo ou áudio que já está no disco.

    Mesmo motor do caminho do YouTube, sem a etapa de download. O faster-whisper
    aceita vídeo direto porque chama o ffmpeg por baixo, então não é preciso
    extrair o áudio antes.
    """
    if not os.path.isfile(caminho):
        raise ErroWhisper("arquivo não encontrado: %s" % caminho)
    modelo, disp = carregar(tamanho, dispositivo, avisar)
    segmentos, info = modelo.transcribe(
        caminho,
        language=idioma,
        vad_filter=True,
        beam_size=5,
        condition_on_previous_text=False,
    )
    saida = []
    for s in segmentos:
        texto = (s.text or "").strip()
        if texto:
            saida.append({"inicio": float(s.start), "texto": texto})
    return saida, "whisper-%s/%s/%s" % (tamanho, disp, info.language), info


def transcrever(url, tamanho="large-v3", idioma=None, dispositivo="auto", avisar=None):
    """URL -> (segmentos, rótulo do motor).

    O áudio vai para uma pasta temporária e é apagado no finally, inclusive
    quando a transcrição falha no meio.
    """
    modelo, disp = carregar(tamanho, dispositivo, avisar)
    pasta = tempfile.mkdtemp(prefix="transcritor_")
    try:
        audio = baixar_audio(url, pasta)
        segmentos, info = modelo.transcribe(
            audio,
            language=idioma,
            vad_filter=True,        # corta silêncio: evita o Whisper alucinar em trecho mudo
            beam_size=5,
            condition_on_previous_text=False,  # reduz repetição em loop
        )
        saida = []
        for s in segmentos:
            texto = (s.text or "").strip()
            if texto:
                saida.append({"inicio": float(s.start), "texto": texto})
        return saida, "whisper-%s/%s/%s" % (tamanho, disp, info.language)
    finally:
        shutil.rmtree(pasta, ignore_errors=True)
