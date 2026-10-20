# -*- coding: utf-8 -*-
"""Legenda corrida (palavra a palavra, blocos curtos) no padrão do manual.

Três jeitos de saber o tempo de cada palavra (do melhor para o pior):
  1. --alinhamento: JSON de tempos por caractere do ElevenLabs (tts_elevenlabs.py salva junto do mp3);
  2. --transcrever: faster-whisper com word_timestamps (roda local no PC, baixa o modelo na 1ª vez);
  3. --texto: frases conhecidas (uma por linha) distribuídas pelas pausas da voz (proporcional às letras).

Estilos prontos:
  drop -> Poppins Bold ~107, centro y=1060 (criativos de produto/drop)
  sb   -> Anton ~116, centro y=1480 (San Benito / público sênior)

Uso:
  python legenda.py VIDEO_OU_AUDIO --transcrever --idioma es -o leg.ass
  python legenda.py narr.mp3 --alinhamento narr.json -o leg.ass --estilo sb --chaves "dios,ventana"
  python legenda.py corpo.mp4 --texto frases.txt -o leg.ass
  python legenda.py corpo.mp4 --transcrever --queimar saida.mp4      # gera e já aplica no vídeo
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from comum import ANTON, POPPINS, W, H, run, dur, tmpdir, preparar_fontsdir  # noqa: E402

ESTILOS = {
    "drop": dict(fonte=POPPINS, nome="Poppins", px=107, y=1060, contorno=10, sombra=4),
    "sb":   dict(fonte=ANTON,   nome="Anton",   px=116, y=1480, contorno=9,  sombra=3),
}
MAXW = 980          # largura máxima do bloco (auto-escala abaixo disso)
MAX_PAL, MAX_CHR = 3, 16
AMARELO, BRANCO = r"{\c&H00FFFF&}", r"{\c&HFFFFFF&}"
NBSP = " "     # use espaço duro para manter palavras juntas, ex.: «Ver más»


# ---------------------------------------------------------------- tempos das palavras
def _envelope(media: str, hop: float = 0.02):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", media, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(float)
    n = int(16000 * hop)
    env = np.array([20 * np.log10(np.sqrt(np.mean(a[i:i + n] ** 2)) + 1e-9) for i in range(0, len(a), n)])
    return env, hop


def _pausas(media: str, min_pausa: float = 0.30):
    """Lista de (ini, fim) de silêncios >= min_pausa."""
    env, hop = _envelope(media)
    voz = env > (np.percentile(env, 90) - 25)
    out, i = [], 0
    while i < len(voz):
        if not voz[i]:
            j = i
            while j < len(voz) and not voz[j]:
                j += 1
            if (j - i) * hop >= min_pausa:
                out.append((i * hop, j * hop))
            i = j
        else:
            i += 1
    return out


def palavras_por_texto(frases: list[str], media: str) -> list[tuple[str, float, float]]:
    """Distribui as frases pelas pausas mais longas e as palavras pelo nº de letras."""
    env, hop = _envelope(media)
    total = len(env) * hop
    voz = env > (np.percentile(env, 90) - 22)
    pausas = sorted(_pausas(media), key=lambda p: p[1] - p[0], reverse=True)[: max(0, len(frases) - 1)]
    cortes = sorted((a + b) / 2 for a, b in pausas)
    lim = [0.0] + cortes + [total]
    frases = list(frases)
    while len(frases) > len(lim) - 1:          # menos pausas que frases: junta o par vizinho mais curto
        i = min(range(len(frases) - 1), key=lambda k: len(frases[k]) + len(frases[k + 1]))
        frases[i:i + 2] = [frases[i] + " " + frases[i + 1]]
    out = []
    for k, fr in enumerate(frases):
        a, b = lim[k], lim[min(k + 1, len(lim) - 1)]
        ia, ib = int(a / hop), int(b / hop)
        idx = np.where(voz[ia:ib])[0]
        if not len(idx):
            continue
        s0, s1 = (ia + idx[0]) * hop, (ia + idx[-1] + 1) * hop
        ws = [x for x in fr.split(" ") if x]
        pesos = [len(re.sub(r"[^\wáéíóúñü]", "", w, flags=re.I)) + 1.5 + (2.5 if w.endswith(",") else 0) for w in ws]
        t, tot = s0, sum(pesos)
        for w, p in zip(ws, pesos):
            d = (s1 - s0) * p / tot
            out.append((w, round(t, 3), round(t + d, 3)))
            t += d
    return out


def palavras_por_alinhamento(json_path: str, deslocamento: float = 0.0):
    """Lê o alinhamento por caractere do ElevenLabs (characters / character_start_times_seconds / ..._end_...)."""
    d = json.load(open(json_path, encoding="utf-8"))
    al = d.get("alignment") or d.get("normalized_alignment") or d
    chars, ini, fim = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    out, cur, t0 = [], "", None
    for c, a, b in zip(chars, ini, fim):
        if c.isspace() and c != NBSP:
            if cur:
                out.append((cur, t0 + deslocamento, ult + deslocamento))
            cur, t0 = "", None
        else:
            if t0 is None:
                t0 = a
            cur += c
            ult = b
    if cur:
        out.append((cur, t0 + deslocamento, ult + deslocamento))
    return out


def palavras_por_whisper(media: str, idioma: str = "es", modelo: str = "small"):
    from faster_whisper import WhisperModel  # pip install faster-whisper
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(media, language=idioma, word_timestamps=True, vad_filter=True)
    out = []
    for s in segs:
        for w in s.words or []:
            txt = w.word.strip()
            if txt:
                out.append((txt, round(w.start, 3), round(w.end, 3)))
    return out


# ---------------------------------------------------------------- ASS
def _blocos(pal):
    bl, cur = [], []
    for w in pal:
        txt = " ".join(x[0] for x in cur + [w])
        if cur and (len(cur) >= MAX_PAL or len(txt) > MAX_CHR):
            bl.append(cur)
            cur = []
        cur.append(w)
        if w[0].endswith((".", ":", ",", "?", "!")):
            bl.append(cur)
            cur = []
    if cur:
        bl.append(cur)
    return bl


def _ts(t: float) -> str:
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _limpa(w: str) -> str:
    return re.sub(r"[^\wáéíóúñü«»" + NBSP + "]", "", w.lower(), flags=re.I)


def gera_ass(pal, destino: str, estilo: str = "drop", chaves: set[str] | None = None,
             y: int | None = None, fim_total: float | None = None, chave_auto: bool = True) -> str:
    """Escreve o .ass. Em cada bloco, no máximo 1 palavra amarela (das `chaves` ou, se chave_auto,
    a palavra mais longa com 5+ letras a cada 2 blocos)."""
    e = ESTILOS[estilo]
    y = y or e["y"]
    f = ImageFont.truetype(str(e["fonte"]), e["px"])
    asc, desc = f.getmetrics()
    fs_ass = round(e["px"] * (asc + desc) / e["px"])  # libass usa ascent+descent como tamanho
    chaves = {_limpa(c) for c in (chaves or set())}
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,{e['nome']},{fs_ass},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,{-1 if estilo == 'drop' else 0},0,0,0,100,100,1,0,1,{e['contorno']},{e['sombra']},5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    bl = _blocos(pal)
    linhas = []
    for i, b in enumerate(bl):
        ini = b[0][1]
        fim = bl[i + 1][0][1] if i + 1 < len(bl) else (fim_total or b[-1][2] + 0.6)
        fim = min(fim, b[-1][2] + 0.6)
        txt = " ".join(w[0] for w in b).upper()
        larg = f.getlength(txt)
        esc = min(100, int(100 * MAXW / larg)) if larg > MAXW else 100
        alvo = None
        for w in b:
            if _limpa(w[0]) in chaves:
                alvo = w
                break
        if alvo is None and chave_auto and not chaves and i % 2 == 0:
            cand = [w for w in b if len(_limpa(w[0])) >= 5]
            alvo = max(cand, key=lambda w: len(w[0])) if cand else None
        partes = [(AMARELO if w is alvo else BRANCO) + w[0].upper() for w in b]
        pop = (r"{\an5\pos(540," + str(y) + r")\fscx" + str(int(esc * .8)) + r"\fscy" + str(int(esc * .8)) +
               r"\t(0,90,\fscx" + str(esc + 6) + r"\fscy" + str(esc + 6) + r")\t(90,160,\fscx" + str(esc) +
               r"\fscy" + str(esc) + r")}")
        linhas.append(f"Dialogue: 0,{_ts(ini)},{_ts(fim)},C,,0,0,0,,{pop}{' '.join(partes)}")
    Path(destino).write_text(head + "\n".join(linhas) + "\n", encoding="utf-8")
    return destino


def queimar(video: str, ass: str, saida: str, crf: int = 18):
    """Aplica o .ass no vídeo (copia ass + fontes para uma pasta temporária e roda o ffmpeg lá dentro,
    para o caminho não ter 'C:' — o filtro ass do ffmpeg quebra com isso no Windows)."""
    wk = tmpdir("leg_")
    preparar_fontsdir(wk)
    (wk / "leg.ass").write_text(Path(ass).read_text(encoding="utf-8"), encoding="utf-8")
    run(["ffmpeg", "-i", str(Path(video).resolve()), "-vf", "ass=leg.ass:fontsdir=fonts",
         "-c:v", "libx264", "-threads", "4", "-crf", crf, "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy",
         str(Path(saida).resolve())], cwd=wk)
    return saida


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("midia", help="vídeo ou áudio com a narração")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--transcrever", action="store_true")
    g.add_argument("--texto", help="arquivo .txt, uma frase por linha")
    g.add_argument("--alinhamento", help="JSON de alinhamento do ElevenLabs")
    ap.add_argument("--idioma", default="es")
    ap.add_argument("--modelo-whisper", default="small")
    ap.add_argument("--deslocamento", type=float, default=0.0, help="soma N s nos tempos (áudio que começa depois)")
    ap.add_argument("--estilo", choices=list(ESTILOS), default="drop")
    ap.add_argument("--y", type=int, help="centro vertical da legenda (px)")
    ap.add_argument("--chaves", default="", help="palavras amarelas, separadas por vírgula")
    ap.add_argument("-o", "--saida", default="legenda.ass")
    ap.add_argument("--queimar", help="se informado, aplica a legenda e salva este vídeo")
    a = ap.parse_args()

    if a.transcrever:
        pal = palavras_por_whisper(a.midia, a.idioma, a.modelo_whisper)
    elif a.alinhamento:
        pal = palavras_por_alinhamento(a.alinhamento, a.deslocamento)
    else:
        frases = [l.strip() for l in open(a.texto, encoding="utf-8") if l.strip()]
        pal = palavras_por_texto(frases, a.midia)
    chaves = {c.strip() for c in a.chaves.split(",") if c.strip()}
    gera_ass(pal, a.saida, a.estilo, chaves, a.y, dur(a.midia))
    print(f"{len(pal)} palavras -> {a.saida}")
    if a.queimar:
        queimar(a.midia, a.saida, a.queimar)
        print("vídeo legendado:", a.queimar)


if __name__ == "__main__":
    main()
