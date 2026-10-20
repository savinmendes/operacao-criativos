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


# ---------------------------------------------------------------- formatos de entrega
# Receita: "formato": "9:16" (padrão) | "4:5" | "1:1"  +  "resolucao": "720" | "1080" (largura).
FORMATOS = {"9:16": (9, 16), "4:5": (4, 5), "1:1": (1, 1)}
FORMATO_PADRAO = "9:16"


def _formato(formato: str | None) -> str:
    f = FORMATO_PADRAO if formato in (None, "") else str(formato).strip()
    if f not in FORMATOS:
        raise ValueError(f"formato '{formato}' inválido; use um de {', '.join(FORMATOS)}")
    return f


def dimensoes(formato: str | None = FORMATO_PADRAO, base: int = 1080) -> tuple[int, int]:
    """(largura, altura) do formato com largura `base`: 9:16 -> 1080x1920, 4:5 -> 1080x1350, 1:1 -> 1080x1080
    (base 720 -> 720x1280 / 720x900 / 720x720). Altura sempre par (yuv420p)."""
    a, b = FORMATOS[_formato(formato)]
    h = int(round(base * b / a))
    return int(base), h + (h % 2)


def resolucao(nome: str | int = "1080", formato: str | None = FORMATO_PADRAO) -> tuple[int, int]:
    """'720' -> (720, 1280); '1080' -> (1080, 1920). Com formato: resolucao('720', '4:5') -> (720, 900)."""
    return dimensoes(formato, 720 if str(nome) == "720" else W)


RESOLUCOES_VALIDAS = {dimensoes(f, b): f for f in FORMATOS for b in (720, 1080)}


def formato_de(w: int, h: int) -> str | None:
    """Formato de uma resolução de entrega válida (ex.: 720x900 -> '4:5'); None se não for uma das 6."""
    return RESOLUCOES_VALIDAS.get((int(w), int(h)))


def checar_resolucao(w: int, h: int, formato: str | None = None) -> tuple[bool, str]:
    """(ok, mensagem). Sem formato: aceita as 6 resoluções de entrega; com formato: só as 2 dele (720/1080)."""
    if formato:
        aceitas = [dimensoes(formato, b) for b in (720, 1080)]
    else:
        aceitas = list(RESOLUCOES_VALIDAS)
    if (int(w), int(h)) in aceitas:
        return True, f"{w}x{h} ({formato_de(w, h)})"
    txt = " ou ".join(f"{a}x{b}" for a, b in aceitas)
    return False, f"resolução {w}x{h} (esperado {txt}{' para ' + formato if formato else ''})"


# ---------------------------------------------------------------- layout por formato
# Coordenadas no quadro BASE de 1080 de largura do formato (1080x1920 / 1080x1350 / 1080x1080), como sempre
# foi no 9:16: com "resolucao": "720" as camadas são posicionadas no quadro base e reduzidas só na saída.
# Padrões do 9:16 = os de antes. 4:5 e 1:1: legenda/manchete/faixa proporcionais à altura; setas e selo
# encolhem (escala ~ raiz da altura relativa) e o selo sobe para perto do topo (não cabe entre legenda e setas).
_SETA_PX, _SELO_W, _SELO_H = 194, 760, 360       # PNGs de overlays.seta()/selo() em escala 1
_LAYOUT_916 = dict(legenda_drop=1060, legenda_sb=1480, selo_x=160, selo_y=1225, cta_y=1630, cta_x=[300, 610],
                   manchete_y=140, faixa_y=150)
_ESCALA = {"9:16": 1.0, "4:5": 0.85, "1:1": 0.75}
_SELO_TOPO = {"4:5": 0.18, "1:1": 0.20}          # fração da altura (abaixo da manchete do hook)


def layout_padrao(formato: str | None = FORMATO_PADRAO, estilo: str = "drop") -> dict:
    f = _formato(formato)
    Wb, Hb = dimensoes(f, W)
    if f == "9:16":
        L = {k: v for k, v in _LAYOUT_916.items() if not k.startswith("legenda_")}
        L.update(W=Wb, H=Hb, cta_x=list(_LAYOUT_916["cta_x"]), selo_escala=1.0, cta_escala=1.0,
                 legenda_y=_LAYOUT_916["legenda_sb" if estilo == "sb" else "legenda_drop"])
        return L
    k = Hb / H
    s = _ESCALA[f]
    seta = _SETA_PX * s
    osc = 20 * s
    margem = 0.04 * Hb
    cta_y = int(min(_LAYOUT_916["cta_y"] * k, Hb - margem - seta - osc))
    # centro das setas igual ao do 9:16 (x + 97)
    cta_x = [int(round(x + _SETA_PX / 2 - seta / 2)) for x in _LAYOUT_916["cta_x"]]
    leg_sb = int(_LAYOUT_916["legenda_sb"] * k)
    leg_sb = min(leg_sb, int(cta_y - osc - 116 * 0.7 - 0.02 * Hb))     # sb não encosta nas setas
    return dict(W=Wb, H=Hb,
                legenda_y=leg_sb if estilo == "sb" else int(_LAYOUT_916["legenda_drop"] * k),
                selo_escala=s, selo_x=int(round((Wb - _SELO_W * s) / 2)), selo_y=int(_SELO_TOPO[f] * Hb),
                cta_escala=s, cta_x=cta_x, cta_y=cta_y,
                manchete_y=int(_LAYOUT_916["manchete_y"] * k), faixa_y=int(_LAYOUT_916["faixa_y"] * k))


def resolver_y(spec: dict | None, chave: str, altura: int, padrao):
    """Posição de uma camada: spec[chave] (px absolutos no quadro base) vence; senão spec[chave+'_rel']
    (0–1 da altura do quadro); senão o padrão."""
    spec = spec or {}
    if spec.get(chave) is not None:
        return spec[chave]
    rel = spec.get(chave + "_rel")
    if rel is not None:
        if not 0 <= float(rel) <= 1:
            raise ValueError(f"{chave}_rel={rel} fora de 0–1")
        return int(round(float(rel) * altura))
    return padrao

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
