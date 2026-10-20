"""Orquestrador do pipeline de geração de criativos de vídeo.

Lê um roteiro (roteiro.json) com cenas de b-roll e/ou avatar falando, gera
cada asset via API (fal.ai, ElevenLabs, HeyGen) e junta tudo em um MP4 final
com ffmpeg. Roda 100% local via linha de comando: `python main.py`.

Requer FAL_KEY no .env (fal.ai/dashboard/keys). A Flora AI (lib/flora_client.py)
continua no projeto, pronta pra usar depois — ver README.md, seção "Flora AI".

Cada cena é processada de forma independente: se uma cena falhar (erro de
API, timeout etc.), o erro é logado e o pipeline segue para a próxima cena
em vez de derrubar a execução inteira. Cenas que falharam simplesmente não
entram no vídeo final.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys

from tqdm import tqdm

import config
from lib import elevenlabs_client, fal_client, heygen_client
from lib.ffmpeg_merge import baixar_arquivo, build_avatar_with_cutaways, merge_clips

ROTEIRO_PADRAO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roteiro.json")
ASPECT_RATIO_PADRAO = "9:16"


def carregar_roteiro(caminho: str) -> list[dict]:
    """Lê e valida o arquivo de roteiro (lista de cenas)."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        cenas = json.load(arquivo)

    if not isinstance(cenas, list) or not cenas:
        raise ValueError(f"Roteiro em '{caminho}' deve ser uma lista JSON não vazia de cenas.")

    return cenas


def _gerar_video_broll(prompt: str, duracao: int = 5, aspect_ratio: str = ASPECT_RATIO_PADRAO) -> str:
    """Gera um clipe de vídeo via fal.ai a partir de um prompt e retorna a URL."""
    return fal_client.generate_video(prompt=prompt, duration=duracao, aspect_ratio=aspect_ratio)


def processar_cena_broll(cena: dict, indice: int, aspect_ratio: str) -> str:
    """Gera um clipe de b-roll via fal.ai e retorna a URL."""
    return _gerar_video_broll(cena["prompt"], cena.get("duracao", 5), aspect_ratio)


def processar_cena_avatar(cena: dict, indice: int, aspect_ratio: str) -> str:
    """Gera imagem + fala + vídeo de avatar com lip-sync e retorna a URL/caminho do vídeo.

    Se a cena tiver um campo `cutaways` (lista de {a_partir_segundo, duracao,
    prompt}), gera um b-roll pra cada janela de corte e monta um único clipe
    onde o vídeo alterna avatar/b-roll nessas janelas enquanto o áudio da
    fala toca contínuo do início ao fim (ver lib/ffmpeg_merge.build_avatar_with_cutaways).
    Sem `cutaways`, o comportamento é o mesmo de sempre: devolve o vídeo do
    avatar falando do início ao fim, sem cortes.
    """
    imagem_url = fal_client.generate_image(prompt=cena["imagem_prompt"], aspect_ratio=aspect_ratio)

    imagem_local = baixar_arquivo(
        imagem_url, os.path.join(config.TMP_DIR, f"avatar_{indice}_imagem.png")
    )

    voice_id = config.require(config.ELEVENLABS_VOICE_ID, "ELEVENLABS_VOICE_ID")
    audio_local = elevenlabs_client.generate_speech(
        text=cena["fala"],
        voice_id=voice_id,
        output_path=os.path.join(config.TMP_DIR, f"avatar_{indice}_fala.mp3"),
    )

    video_id = heygen_client.create_avatar_video(
        image_url=imagem_local,
        audio_url_or_path=audio_local,
        aspect_ratio=aspect_ratio,
    )
    video_avatar_url = heygen_client.poll_video_status(video_id)

    cutaways_cena = cena.get("cutaways")
    if not cutaways_cena:
        return video_avatar_url

    cutaways_resolvidos = []
    for corte in cutaways_cena:
        clipe_url = _gerar_video_broll(corte["prompt"], corte["duracao"], aspect_ratio)
        cutaways_resolvidos.append(
            {
                "a_partir_segundo": corte["a_partir_segundo"],
                "duracao": corte["duracao"],
                "clipe": clipe_url,
            }
        )

    return build_avatar_with_cutaways(video_avatar_url, cutaways_resolvidos, aspect_ratio=aspect_ratio)


def rodar_pipeline(caminho_roteiro: str, aspect_ratio: str = ASPECT_RATIO_PADRAO) -> str | None:
    """Roda o pipeline completo: lê o roteiro, gera cada cena, junta tudo no final.

    Returns:
        Caminho do MP4 final, ou None se nenhuma cena foi gerada com sucesso.
    """
    cenas = carregar_roteiro(caminho_roteiro)
    os.makedirs(config.TMP_DIR, exist_ok=True)

    clipes_gerados: list[str] = []
    falhas: list[str] = []

    for indice, cena in enumerate(tqdm(cenas, desc="Gerando cenas", unit="cena")):
        tipo = cena.get("tipo")
        try:
            if tipo == "broll":
                url = processar_cena_broll(cena, indice, aspect_ratio)
            elif tipo == "avatar":
                url = processar_cena_avatar(cena, indice, aspect_ratio)
            else:
                raise ValueError(f"Tipo de cena desconhecido: {tipo!r}")

            clipes_gerados.append(url)
            print(f"[cena {indice}] OK ({tipo})")

        except Exception as exc:  # noqa: BLE001 - qualquer falha de cena não deve derrubar o pipeline
            falhas.append(f"cena {indice} ({tipo}): {exc}")
            print(f"[cena {indice}] ERRO ({tipo}): {exc}", file=sys.stderr)

    if not clipes_gerados:
        print("Nenhuma cena foi gerada com sucesso — nada para juntar.", file=sys.stderr)
        return None

    print(f"\nJuntando {len(clipes_gerados)} clipe(s) no vídeo final...")
    try:
        caminho_final = merge_clips(clipes_gerados, aspect_ratio=aspect_ratio)
    except Exception as exc:  # noqa: BLE001 - erro no merge nao deve gerar traceback cru
        print(f"\nERRO ao juntar os clipes no vídeo final: {exc}", file=sys.stderr)
        print(
            "Os clipes gerados com sucesso continuam disponíveis em "
            f"{config.TMP_DIR} (verifique se o ffmpeg está instalado e no PATH).",
            file=sys.stderr,
        )
        return None

    print(f"\nVídeo final salvo em: {caminho_final}")
    if falhas:
        print(f"\n{len(falhas)} cena(s) falharam e não entraram no vídeo final:")
        for falha in falhas:
            print(f"  - {falha}")

    return caminho_final


def abrir_pasta_output() -> None:
    """Abre a pasta de output no explorador de arquivos (Windows); ignora em outros OS."""
    if platform.system() == "Windows":
        os.startfile(config.OUTPUT_DIR)  # type: ignore[attr-defined]
    elif platform.system() == "Darwin":
        subprocess.run(["open", config.OUTPUT_DIR], check=False)
    else:
        subprocess.run(["xdg-open", config.OUTPUT_DIR], check=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera um criativo de vídeo a partir de um roteiro.json")
    parser.add_argument(
        "--roteiro", default=ROTEIRO_PADRAO, help="Caminho do arquivo de roteiro JSON (padrão: roteiro.json)"
    )
    parser.add_argument(
        "--aspect-ratio", default=ASPECT_RATIO_PADRAO, help='Proporção do vídeo final (padrão: "9:16")'
    )
    args = parser.parse_args()

    caminho_final = rodar_pipeline(args.roteiro, aspect_ratio=args.aspect_ratio)

    if caminho_final:
        abrir_pasta_output()


if __name__ == "__main__":
    main()
