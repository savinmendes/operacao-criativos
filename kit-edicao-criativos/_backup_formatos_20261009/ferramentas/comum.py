# -*- coding: utf-8 -*-
"""Funções comuns do kit de edição de criativos (Windows / Linux / macOS).

Padrões do manual: vídeo vertical 1080x1920, 30 fps, H.264 yuv420p, AAC 48 kHz estéreo.
Requer ffmpeg e ffprobe no PATH.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
FONTS = KIT / "fonts"
ANTON = FONTS / "Anton-Regular.ttf"
POPPINS = FONTS / "Poppins-Bold.ttf"

W, H, FPS = 1080, 1920, 30

# Metadados de cor iguais em todas as partes de um corpo. Partes com tags diferentes (ex.: HeyGen sem tag +
# vídeo original tv/bt709) fazem o ffmpeg reconfigurar o filtergraph no meio e perder overlays/áudio bufferizado.
COR = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       # o x264 só grava range/matriz; o bsf força também primárias/transferência no SPS (ffprobe mostra bt709 nos 4)
       "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0"]


def resolucao(nome: str | int = "1080") -> tuple[int, int]:
    """'720' -> (720, 1280); '1080' -> (1080, 1920)."""
    return (720, 1280) if str(nome) == "720" else (W, H)

# Emoji colorido: Windows usa Segoe UI Emoji; Linux Noto; macOS Apple Color Emoji.
EMOJI_FONTS = [
    Path("C:/Windows/Fonts/seguiemj.ttf"),
    Path("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"),
    Path("/System/Library/Fonts/Apple Color Emoji.ttc"),
]


def emoji_font() -> Path | None:
    for p in EMOJI_FONTS:
        if p.exists():
            return p
    return None


def run(args: list, cwd: str | Path | None = None, quiet: bool = True) -> str:
    """Roda um comando e levanta erro com o fim do stderr se falhar."""
    args = [str(a) for a in args]
    if args[0] == "ffmpeg" and quiet and "-v" not in args:
        args = [args[0], "-v", "error", "-y"] + args[1:]
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(f"Falhou: {' '.join(args)[:300]}\n{r.stderr[-2000:]}")
    return r.stdout


def dur(path: str | Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())


def tem_audio(path: str | Path) -> bool:
    out = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", path])
    return bool(out.strip())


def info(path: str | Path) -> dict:
    out = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration,size",
               "-of", "json", path])
    return json.loads(out)


def vf_vertical(w: int = W, h: int = H, fps: int = FPS) -> str:
    """Escala preenchendo o quadro (corta o excesso), sem barras pretas."""
    return f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},fps={fps},setsar=1"


def tmpdir(prefix: str = "kit_") -> Path:
    d = Path(tempfile.mkdtemp(prefix=prefix))
    return d


def preparar_fontsdir(destino: Path) -> Path:
    """Copia as fontes do kit para <destino>/fonts (o filtro ass do ffmpeg lê por caminho relativo,
    o que evita o problema de 'C:' em caminhos do Windows)."""
    fd = destino / "fonts"
    fd.mkdir(parents=True, exist_ok=True)
    for f in FONTS.glob("*.ttf"):
        shutil.copy2(f, fd / f.name)
    return fd


def checar_decodificacao(path: str | Path) -> str:
    """Decodifica o arquivo inteiro. Retorna '' se ok, ou o erro."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stderr.strip()


def mb(path: str | Path) -> float:
    return os.path.getsize(path) / 1048576
