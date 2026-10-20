"""Junta os clipes de b-roll + avatar em um único MP4 final (9:16).

Baixa os assets remotos (URLs) para uma pasta temporária local, normaliza
todos os clipes para a mesma resolução/fps/taxa de amostragem de áudio, e
concatena com o concat demuxer do ffmpeg (exige que os clipes já estejam no
mesmo formato — por isso a normalização é feita antes, em vez de tentar
concatenar direto e deixar o ffmpeg reconciliar formatos diferentes).
"""

from __future__ import annotations

import os
import subprocess
import time

import requests

import config

RESOLUCOES_POR_ASPECT_RATIO = {
    "9:16": (720, 1280),
    "16:9": (1280, 720),
    "1:1": (1080, 1080),
}

FPS_PADRAO = 30
AUDIO_SAMPLE_RATE = 44100

# CRF baixo (mais qualidade) + preset lento: os clipes são curtos, então o
# tempo extra de encode não pesa, mas o ganho de qualidade é grande. Com o
# preset "veryfast" e CRF padrão (23) o bitrate caía de ~8Mbps (bruto do
# fal.ai) pra ~1,9Mbps num re-encode só — visivelmente pior, e pior ainda
# nos blocos de avatar+cutaways, que passam por dois re-encodes.
CRF_QUALIDADE = "18"
PRESET_ENCODE = "slow"


def baixar_arquivo(url_ou_caminho: str, destino: str) -> str:
    """Baixa um arquivo remoto (http/https) para `destino`, ou apenas retorna
    o caminho se já for um arquivo local existente.
    """
    if os.path.isfile(url_ou_caminho):
        return url_ou_caminho

    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
    resposta = requests.get(url_ou_caminho, timeout=120)
    resposta.raise_for_status()
    with open(destino, "wb") as arquivo:
        arquivo.write(resposta.content)
    return destino


def obter_duracao(caminho_arquivo: str) -> float:
    """Retorna a duração (em segundos) de um arquivo de vídeo/áudio via ffprobe."""
    comando = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        caminho_arquivo,
    ]
    resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
    return float(resultado.stdout.strip())


def _tem_audio(caminho_arquivo: str) -> bool:
    """Verifica se um arquivo de vídeo tem alguma faixa de áudio."""
    comando = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=codec_type",
        "-of", "csv=p=0",
        caminho_arquivo,
    ]
    resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
    return bool(resultado.stdout.strip())


def _normalizar_clipe(caminho_entrada: str, caminho_saida: str, aspect_ratio: str) -> None:
    """Reescala/pad + normaliza fps e taxa de amostragem de áudio de um clipe.

    Clipes gerados sem áudio nativo (ex.: b-roll com generate_audio=False)
    recebem uma faixa de silêncio — sem isso, misturar um clipe sem áudio com
    um clipe com áudio no concat final faz o ffmpeg descartar o áudio do
    vídeo inteiro (os streams precisam ser consistentes entre todos os
    clipes concatenados).
    """
    largura, altura = RESOLUCOES_POR_ASPECT_RATIO.get(aspect_ratio, RESOLUCOES_POR_ASPECT_RATIO["9:16"])
    filtro_video = (
        f"scale={largura}:{altura}:force_original_aspect_ratio=decrease,"
        f"pad={largura}:{altura}:(ow-iw)/2:(oh-ih)/2,"
        f"fps={FPS_PADRAO},setsar=1"
    )

    if _tem_audio(caminho_entrada):
        comando = [
            "ffmpeg",
            "-y",
            "-i", caminho_entrada,
            "-vf", filtro_video,
            "-ar", str(AUDIO_SAMPLE_RATE),
            "-c:v", "libx264",
            "-preset", PRESET_ENCODE,
            "-crf", CRF_QUALIDADE,
            "-c:a", "aac",
            "-b:a", "192k",
            caminho_saida,
        ]
    else:
        comando = [
            "ffmpeg",
            "-y",
            "-i", caminho_entrada,
            "-f", "lavfi",
            "-i", f"anullsrc=channel_layout=stereo:sample_rate={AUDIO_SAMPLE_RATE}",
            "-vf", filtro_video,
            "-c:v", "libx264",
            "-preset", PRESET_ENCODE,
            "-crf", CRF_QUALIDADE,
            "-c:a", "aac",
            "-b:a", "192k",
            "-map", "0:v",
            "-map", "1:a",
            "-shortest",
            caminho_saida,
        ]

    subprocess.run(comando, check=True, capture_output=True)


def merge_clips(
    caminhos_ou_urls: list[str],
    aspect_ratio: str = "9:16",
) -> str:
    """Baixa, normaliza e concatena uma lista ordenada de clipes em um MP4 final.

    Args:
        caminhos_ou_urls: lista de caminhos locais ou URLs dos clipes, na
            ordem em que devem aparecer no vídeo final.
        aspect_ratio: proporção final do vídeo (ex.: "9:16").

    Returns:
        Caminho do arquivo MP4 final gerado em `output/final_<timestamp>.mp4`.
    """
    if not caminhos_ou_urls:
        raise ValueError("Nenhum clipe fornecido para o merge.")

    os.makedirs(config.TMP_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    clipes_normalizados: list[str] = []
    for indice, origem in enumerate(caminhos_ou_urls):
        bruto = baixar_arquivo(origem, os.path.join(config.TMP_DIR, f"bruto_{indice}.mp4"))
        normalizado = os.path.join(config.TMP_DIR, f"norm_{indice}.mp4")
        _normalizar_clipe(bruto, normalizado, aspect_ratio)
        clipes_normalizados.append(normalizado)

    lista_concat = os.path.join(config.TMP_DIR, "concat_list.txt")
    with open(lista_concat, "w", encoding="utf-8") as arquivo:
        for clipe in clipes_normalizados:
            caminho_absoluto = os.path.abspath(clipe).replace("'", r"'\''")
            arquivo.write(f"file '{caminho_absoluto}'\n")

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    saida_final = os.path.join(config.OUTPUT_DIR, f"final_{timestamp}.mp4")

    comando = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", lista_concat,
        "-c", "copy",
        saida_final,
    ]
    subprocess.run(comando, check=True, capture_output=True)

    return saida_final


def _calcular_segmentos(duracao_total: float, cutaways_ordenados: list[dict]) -> list[dict]:
    """Monta a lista alternada de segmentos (avatar/cutaway) que cobre toda a
    duração do áudio do avatar, pulando segmentos de duração zero (cutaway
    que começa em 0s, ou que termina exatamente no fim do áudio).
    """
    segmentos: list[dict] = []
    cursor = 0.0

    for indice, corte in enumerate(cutaways_ordenados):
        inicio_corte = corte["a_partir_segundo"]
        fim_corte = inicio_corte + corte["duracao"]

        if inicio_corte > cursor:
            segmentos.append({"tipo": "avatar", "inicio": cursor, "fim": inicio_corte})

        segmentos.append({"tipo": "cutaway", "indice": indice})
        cursor = fim_corte

    if cursor < duracao_total:
        segmentos.append({"tipo": "avatar", "inicio": cursor, "fim": duracao_total})

    return segmentos


def build_avatar_with_cutaways(
    avatar_video_path: str,
    cutaways: list[dict],
    aspect_ratio: str = "9:16",
) -> str:
    """Monta um único clipe onde o vídeo alterna entre o avatar e clipes de
    b-roll (cutaways) em janelas de tempo específicas, mantendo o áudio da
    fala do avatar tocando contínuo do início ao fim, sem cortes.

    Reproduz o estilo de edição clássico de anúncio (avatar fala, corta pro
    b-roll ilustrando o que está sendo dito, volta pro avatar) — diferente de
    `merge_clips`, que concatena clipes inteiros em sequência.

    Args:
        avatar_video_path: caminho local ou URL do vídeo do avatar (com áudio).
        cutaways: lista de dicts, cada um com:
            - "a_partir_segundo" (float): quando, na fala do avatar, o corte começa.
            - "duracao" (float): duração do cutaway em segundos.
            - "clipe" (str): caminho local ou URL do clipe de b-roll já gerado.
        aspect_ratio: proporção do vídeo (ex.: "9:16").

    Returns:
        Caminho do MP4 intermediário gerado (para ser usado como "mais uma
        cena" na lista passada a `merge_clips`).
    """
    if not cutaways:
        raise ValueError("build_avatar_with_cutaways chamado sem cutaways — use o vídeo do avatar direto.")

    os.makedirs(config.TMP_DIR, exist_ok=True)

    avatar_bruto = baixar_arquivo(avatar_video_path, os.path.join(config.TMP_DIR, "cutaway_avatar_bruto.mp4"))
    avatar_normalizado = os.path.join(config.TMP_DIR, "cutaway_avatar_norm.mp4")
    _normalizar_clipe(avatar_bruto, avatar_normalizado, aspect_ratio)
    duracao_total = obter_duracao(avatar_normalizado)

    cutaways_ordenados = sorted(cutaways, key=lambda c: c["a_partir_segundo"])

    clipes_cutaway_normalizados: list[str] = []
    for indice, corte in enumerate(cutaways_ordenados):
        bruto = baixar_arquivo(corte["clipe"], os.path.join(config.TMP_DIR, f"cutaway_{indice}_bruto.mp4"))
        normalizado = os.path.join(config.TMP_DIR, f"cutaway_{indice}_norm.mp4")
        _normalizar_clipe(bruto, normalizado, aspect_ratio)
        clipes_cutaway_normalizados.append(normalizado)

    segmentos = _calcular_segmentos(duracao_total, cutaways_ordenados)

    entradas = ["-i", avatar_normalizado]
    for clipe in clipes_cutaway_normalizados:
        entradas += ["-i", clipe]

    partes_filtro: list[str] = []
    labels: list[str] = []
    for indice_segmento, segmento in enumerate(segmentos):
        label = f"s{indice_segmento}"
        if segmento["tipo"] == "avatar":
            partes_filtro.append(
                f"[0:v]trim=start={segmento['inicio']}:end={segmento['fim']},"
                f"setpts=PTS-STARTPTS[{label}]"
            )
        else:
            indice_cutaway = segmento["indice"]
            indice_entrada = indice_cutaway + 1  # input 0 é o avatar
            duracao_corte = cutaways_ordenados[indice_cutaway]["duracao"]
            partes_filtro.append(
                f"[{indice_entrada}:v]trim=start=0:end={duracao_corte},"
                f"setpts=PTS-STARTPTS[{label}]"
            )
        labels.append(f"[{label}]")

    filtro_concat = "".join(labels) + f"concat=n={len(labels)}:v=1:a=0[outv]"
    filter_complex = ";".join(partes_filtro) + ";" + filtro_concat

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    saida = os.path.join(config.TMP_DIR, f"bloco_avatar_cutaways_{timestamp}.mp4")

    comando = [
        "ffmpeg",
        "-y",
        *entradas,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-preset", PRESET_ENCODE,
        "-crf", CRF_QUALIDADE,
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        saida,
    ]
    subprocess.run(comando, check=True, capture_output=True)

    return saida
