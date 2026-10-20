# -*- coding: utf-8 -*-
"""Troca a voz de uma fala pela voz única da consultora (ElevenLabs Speech-to-Speech / voice changer),
mantendo o tempo da fala (o lipsync do take continua batendo).

  python sts.py entrada.mp4 saida.wav [--voz Om4SAFCLA5Ecbue3cvcc] [--demucs] [--estabilidade 0.5]

- entrada: vídeo ou áudio (usa a 1ª faixa de áudio).
- --demucs: separa a voz da música/ruído antes (python -m demucs --two-stems=vocals) e converte só a voz;
  a música separada sai junto como <saida>_fundo.wav (para remixar se quiser).
- A saída é cortada/completada com silêncio para ter EXATAMENTE a duração da entrada (o script mostra a
  diferença bruta devolvida pela API).
- A chave vem do .env do kit (tts_elevenlabs.chave), nunca é impressa.
Custo: cobra créditos por duração do áudio (~1.000 caracteres por minuto no plano).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
import requests

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
sys.path.insert(0, str(KIT))
from tts_elevenlabs import chave  # noqa: E402

VOZ_PADRAO = "Om4SAFCLA5Ecbue3cvcc"  # Consultora Yara BF (clone do gancho aprovado)
SR = 44100


def dur(p) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode().strip())


def para_wav(src, dst, sr=SR, mono=True):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-ac", "1" if mono else "2",
                    "-ar", str(sr), "-c:a", "pcm_s16le", str(dst)], check=True)


def separar(wav: Path, wk: Path) -> tuple[Path, Path]:
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals", "-o", str(wk), str(wav)], check=True)
    pasta = next(wk.glob(f"*/{wav.stem}"))
    return pasta / "vocals.wav", pasta / "no_vocals.wav"


def converter(wav: Path, voz: str, estab: float, simil: float, ruido: bool) -> np.ndarray:
    with open(wav, "rb") as f:
        r = requests.post(f"https://api.elevenlabs.io/v1/speech-to-speech/{voz}",
                          params={"output_format": f"pcm_{SR}"},
                          headers={"xi-api-key": chave()},
                          data={"model_id": "eleven_multilingual_sts_v2",
                                "voice_settings": json.dumps({"stability": estab, "similarity_boost": simil,
                                                              "style": 0.0, "use_speaker_boost": True}),
                                "remove_background_noise": "true" if ruido else "false"},
                          files={"audio": (wav.name, f, "audio/wav")}, timeout=600)
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:500]}")
    return np.frombuffer(r.content, dtype=np.int16)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--voz", default=VOZ_PADRAO)
    ap.add_argument("--demucs", action="store_true", help="separa voz x música antes de converter")
    ap.add_argument("--estabilidade", type=float, default=0.5)
    ap.add_argument("--similaridade", type=float, default=0.75)
    ap.add_argument("--remover-ruido", action="store_true", help="remove_background_noise da API")
    a = ap.parse_args()

    wk = Path(tempfile.mkdtemp(prefix="sts_"))
    src = wk / "entrada.wav"
    para_wav(a.entrada, src)
    d_in = dur(src)
    fundo = None
    if a.demucs:
        voz_wav, fundo = separar(src, wk)
        src = wk / "voz.wav"
        para_wav(voz_wav, src)
    pcm = converter(src, a.voz, a.estabilidade, a.similaridade, a.remover_ruido)
    d_api = len(pcm) / SR
    n = int(round(d_in * SR))
    pcm = pcm[:n] if len(pcm) >= n else np.concatenate([pcm, np.zeros(n - len(pcm), np.int16)])
    Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(a.saida, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(f"entrada {d_in:.3f}s | API devolveu {d_api:.3f}s (dif {d_api - d_in:+.3f}s) | saída {n / SR:.3f}s -> {a.saida}")
    if fundo is not None:
        out_f = str(Path(a.saida).with_suffix("")) + "_fundo.wav"
        para_wav(fundo, out_f, mono=False)
        print("fundo (sem voz):", out_f)


if __name__ == "__main__":
    main()
