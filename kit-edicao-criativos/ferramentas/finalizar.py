# -*- coding: utf-8 -*-
"""Finaliza e revisa um criativo antes de entregar.

  - reencoda no padrão de entrega (H.264 high, yuv420p, 30 fps, AAC 48 kHz estéreo 128k, +faststart)
    com bitrate calculado para caber no limite (padrão 30 MB)
  - decodifica o arquivo inteiro (acusa frame corrompido)
  - confere duração/resolução
  - gera uma folha de contato (frames lado a lado) para revisar sem abrir o vídeo

Exemplos:
  python finalizar.py bruto.mp4 -o "AD 08 - DESM-H09-GRAMA.mp4"
  python finalizar.py bruto.mp4 -o final.mp4 --limite 30 --frames 1,5,12,-2
  python finalizar.py final.mp4 --so-revisar
  python finalizar.py bruto_4x5.mp4 -o final.mp4 --formato 4:5 --resolucao 720     # 720x900
Resoluções de entrega aceitas: 9:16 720x1280/1080x1920, 4:5 720x900/1080x1350, 1:1 720x720/1080x1080.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import (W, H, FPS, run, dur, info, mb, checar_decodificacao, tmpdir, formato_de,  # noqa: E402
                   checar_resolucao, resolucao)


QUALIDADE_MIN_KBPS = 1500   # abaixo disso 1080x1920 fica visivelmente quadriculado


QUALIDADE_MIN_720_KBPS = 900


def bitrate_alvo(t: float, limite_mb: float, teto_kbps: int = 6000, piso: int | None = None) -> tuple[int, bool]:
    """(kbps de vídeo, cabe_no_limite). Vídeo longo que não cabe no limite sem cair abaixo da qualidade
    mínima usa o piso e passa do limite (com aviso) — nunca entra em looping."""
    piso = piso or QUALIDADE_MIN_KBPS
    total_kbps = limite_mb * 8 * 1024 * 0.93 / t          # 7% de folga para container
    v = int(min(teto_kbps, total_kbps - 128))
    if v < piso:
        prev = (piso + 128) * t / 8 / 1024
        print(f"aviso: {t / 60:.1f} min não cabe em {limite_mb:.0f} MB com qualidade; "
              f"usando {piso} kbps (~{prev:.0f} MB)")
        return piso, False
    return v, True


def _tamanho_entrada(entrada: str) -> tuple[int, int] | None:
    v = [s for s in info(entrada)["streams"] if s["codec_type"] == "video"]
    return (int(v[0]["width"]), int(v[0]["height"])) if v else None


def encode(entrada: str, saida: str, limite_mb: float = 30.0, teto_kbps: int = 6000, _tentativa: int = 0,
           tamanho: tuple[int, int] | None = None):
    """tamanho = (w, h) da entrega. None: 1080 de largura no formato da entrada (720x900 -> 1080x1350;
    entrada fora dos 3 formatos -> 1080x1920, como sempre)."""
    if tamanho is None:
        wh = _tamanho_entrada(entrada)
        tamanho = resolucao("1080", (formato_de(*wh) if wh else None) or "9:16")
    tw, th = tamanho
    t = dur(entrada)
    v_kbps, cabe = bitrate_alvo(t, limite_mb, teto_kbps, piso=QUALIDADE_MIN_720_KBPS if tw == 720 else None)
    run(["ffmpeg", "-i", entrada, "-vf", f"scale={tw}:{th}:flags=lanczos,fps={FPS},setsar=1",
         "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps * 1.5)}k", "-bufsize", f"{v_kbps * 2}k",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida])
    if cabe and mb(saida) > limite_mb and _tentativa < 2:   # raro: refaz com 85% (no máx. 2 vezes)
        return encode(entrada, saida, limite_mb * 0.85, teto_kbps, _tentativa + 1, tamanho)
    return saida


def folha_contato(video: str, destino: str, tempos: list[float] | None = None):
    t = dur(video)
    tempos = tempos or [0.5, t * 0.25, t * 0.5, t * 0.75, max(0, t - 0.8)]
    tempos = [x if x >= 0 else t + x for x in tempos]
    wk = tmpdir("fc_")
    for i, x in enumerate(tempos):
        run(["ffmpeg", "-ss", f"{x:.2f}", "-i", video, "-frames:v", "1", "-vf", "scale=360:-2", wk / f"f{i}.png"])
    ins = []
    for i in range(len(tempos)):
        ins += ["-i", wk / f"f{i}.png"]
    run(["ffmpeg", *ins, "-filter_complex", f"hstack=inputs={len(tempos)}", destino] if len(tempos) > 1
        else ["ffmpeg", *ins, destino])
    return destino


def revisar(video: str, folha: str | None = None, tempos=None, esperado: tuple[int, int] | None = None) -> bool:
    erro = checar_decodificacao(video)
    i = info(video)
    v = [s for s in i["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in i["streams"] if s["codec_type"] == "audio"]
    if esperado:   # resolução exata pedida pela receita
        res_ok = (int(v["width"]), int(v["height"])) == tuple(esperado)
    else:          # qualquer uma das 6 de entrega (9:16, 4:5, 1:1 em 720 ou 1080)
        res_ok = checar_resolucao(v["width"], v["height"])[0]
    ok = not erro and res_ok and a
    print(f"arquivo : {video}")
    print(f"duração : {float(i['format']['duration']):.2f}s | {v['width']}x{v['height']} | áudio: {'sim' if a else 'NÃO'} | {mb(video):.1f} MB")
    print(f"decodif.: {'OK' if not erro else 'ERRO -> ' + erro[:300]}")
    if folha:
        folha_contato(video, folha, tempos)
        print(f"frames  : {folha}")
    print("RESULTADO:", "OK" if ok else "VERIFICAR")
    return bool(ok)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("-o", "--saida")
    ap.add_argument("--limite", type=float, default=30.0, help="MB máximos (padrão 30)")
    ap.add_argument("--frames", help="tempos para a folha de contato, ex.: 1,5,12,-2 (negativo = do fim)")
    ap.add_argument("--so-revisar", action="store_true")
    ap.add_argument("--formato", default=None, help="9:16 | 4:5 | 1:1 (padrão: o da entrada; fora deles, 9:16)")
    ap.add_argument("--resolucao", default="1080", help='"720" ou "1080" (largura da entrega; padrão 1080)')
    a = ap.parse_args()
    tempos = [float(x) for x in a.frames.split(",")] if a.frames else None
    if a.so_revisar:
        alvo = a.entrada
        esperado = resolucao(a.resolucao, a.formato) if a.formato else None
    else:
        wh = _tamanho_entrada(a.entrada)
        esperado = resolucao(a.resolucao, a.formato or (formato_de(*wh) if wh else None) or "9:16")
        alvo = encode(a.entrada, a.saida or str(Path(a.entrada).with_name(Path(a.entrada).stem + "_final.mp4")),
                      a.limite, tamanho=esperado)
    revisar(alvo, str(Path(alvo).with_suffix("")) + "_frames.jpg", tempos, esperado)


if __name__ == "__main__":
    main()
