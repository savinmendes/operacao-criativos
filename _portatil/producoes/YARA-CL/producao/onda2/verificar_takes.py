# -*- coding: utf-8 -*-
"""Transcreve os takes (whisper medium, GPU) e compara com a fala do roteiro.
  python verificar_takes.py            -> todos os .mp4 de takes/ ainda sem _transcricao.json
Saída: takes/<nome>_transcricao.json + resumo no terminal (fala esperada × ouvida)."""
import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, r"C:/Users/PICHAU/Downloads/Produtividade com ia/ferramentas/transcritor-youtube")
from lib import whisper_local as wl  # noqa: E402

AQUI = Path(__file__).parent
TAKES = AQUI / "takes"
ROT = json.loads((AQUI.parent.parent / "preprod" / "onda2" / "roteiro_onda2.json").read_text(encoding="utf-8"))


def fala_esperada(nome):
    c, t = nome.split("_", 1)  # ex.: C7, T2_cta
    for k, v in ROT.get(c, {}).items():
        if isinstance(v, dict) and k.split("_")[0] == t.split("_")[0]:
            return v.get("fala", "")
    return ""


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return [w.strip("¿?¡!.,…:;\"'") for w in s.split() if w.strip("¿?¡!.,…:;\"'")]


def main():
    m, disp = wl.carregar("medium", "auto")
    print("dispositivo:", disp, flush=True)
    for v in sorted(TAKES.glob("*.mp4")):
        dst = v.with_name(v.stem + "_transcricao.json")
        if dst.exists():
            continue
        segs, info = m.transcribe(str(v), language="es", vad_filter=True, word_timestamps=True)
        segs = list(segs)
        palavras = [{"p": w.word.strip(), "ini": round(w.start, 2), "fim": round(w.end, 2)}
                    for s in segs for w in (s.words or [])]
        texto = " ".join(s.text.strip() for s in segs)
        esp = fala_esperada(v.stem)
        faltam = [w for w in norm(esp) if w not in norm(texto)]
        dst.write_text(json.dumps({"texto": texto, "esperado": esp, "faltam": faltam, "palavras": palavras},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n== {v.name}\n  esperado: {esp}\n  ouvido:   {texto}\n  faltam:   {faltam}", flush=True)


if __name__ == "__main__":
    main()
