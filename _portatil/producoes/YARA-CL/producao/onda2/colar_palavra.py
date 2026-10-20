# -*- coding: utf-8 -*-
"""Troca uma palavra mal pronunciada num áudio de take pela mesma palavra em TTS (mesma voz).
  python colar_palavra.py entrada_vz.wav saida.wav --ini 2.50 --fim 3.74 --texto "muñecas" --voz <voice_id>
- Silencia [ini, fim] no áudio original e cola o TTS (sem silêncio nas pontas) começando em ini.
- Se o TTS for mais longo que o buraco, acelera até 1.25x; se ainda não couber, avisa.
- A duração final é igual à da entrada (o vídeo continua sincronizado)."""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, r"C:/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos/ferramentas")
from tts_elevenlabs import gerar  # noqa: E402


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--ini", type=float, required=True)
    ap.add_argument("--fim", type=float, required=True)
    ap.add_argument("--texto", required=True)
    ap.add_argument("--voz", required=True)
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp())
    bruto = tmp / "tts.mp3"
    gerar(a.texto, str(bruto), voz=a.voz)
    limpo = tmp / "tts.wav"
    # tira silêncio do começo e do fim
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bruto), "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                    "-ar", "48000", "-ac", "2", str(limpo)], check=True)
    buraco = a.fim - a.ini
    d = dur(limpo)
    tempo = 1.0
    if d > buraco:
        tempo = min(d / buraco, 1.25)
        if d / tempo > buraco + 0.02:
            print(f"aviso: TTS {d:.2f}s não cabe em {buraco:.2f}s mesmo a 1.25x")
    total = dur(a.entrada)
    ms = int(a.ini * 1000)
    filtro = (f"[0:a]aresample=48000,aformat=channel_layouts=stereo,"
              f"volume=enable='between(t,{a.ini:.3f},{a.fim:.3f})':volume=0[o];"
              f"[1:a]atempo={tempo:.3f},adelay={ms}|{ms}[p];"
              f"[o][p]amix=inputs=2:duration=first:normalize=0,atrim=0:{total:.3f}[s]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.entrada, "-i", str(limpo), "-filter_complex", filtro,
                    "-map", "[s]", "-ar", "48000", a.saida], check=True)
    print(f"ok: '{a.texto}' {d:.2f}s (x{tempo:.2f}) em {a.ini:.2f}-{a.fim:.2f} -> {a.saida} ({dur(a.saida):.3f}s)")


if __name__ == "__main__":
    main()
