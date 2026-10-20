# -*- coding: utf-8 -*-
"""Monta um AD do lote Lymphoria: parte 1 (já tratada) + fim universal (fotos do produto + narração clonada)
+ legenda só no fim + selo universal + setas de CTA, e finaliza pelo kit (≤30 MB, revisão, _frames.jpg).

  python montar_fim_universal.py <pasta_ad> <parte1.mp4> <narr_fim.mp3> "<saida final.mp4>" [--cauda original.wav]
--cauda: áudio extra colado DEPOIS da narração (ex.: frase original do narrador para fechar).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import legenda as LEG  # noqa: E402

TRAB = Path(__file__).parent
FOTO1 = TRAB / "ad04" / "prod_1.jpg"
FOTO_KIT = TRAB / "ad04" / "kit3_quadrado.jpg"
SELO = ["ENVÍO GRATIS A DOMICILIO", "PAGO CONTRA", "ENTREGA", "¡PAGAS AL RECIBIR!"]

ap = argparse.ArgumentParser()
ap.add_argument("pasta")
ap.add_argument("parte1")
ap.add_argument("narr")
ap.add_argument("saida")
ap.add_argument("--cauda", default=None)
ap.add_argument("--res", default="720", help="720 (padrão p/ origem 360p) ou 1080")
a = ap.parse_args()
pasta = Path(a.pasta)
ali = str(Path(a.narr).with_suffix("")) + ".alinhamento.json"
pal = LEG.palavras_por_alinhamento(ali, 0)
t_pides = next(b for w, b, *_ in pal if LEG._limpa(w).startswith("pides"))

narr = a.narr
if a.cauda:  # narração + respiro + frase original
    narr = str(pasta / "narr_fim_com_cauda.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.narr, "-i", a.cauda, "-filter_complex",
                    "[0:a]aresample=48000,aformat=channel_layouts=mono,apad=pad_dur=0.35[x];"
                    "[1:a]aresample=48000,aformat=channel_layouts=mono[y];[x][y]concat=n=2:v=0:a=1",
                    narr], check=True)

subprocess.run([sys.executable, str(TRAB / "ad04" / "render_parte2.py"), narr, str(pasta / "parte2.mp4"),
                f"{FOTO1}:0", f"{FOTO_KIT}:{t_pides:.3f}"], check=True)
d1 = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.parte1],
                          capture_output=True, text=True).stdout)
rec = {
    "saida": str(Path(a.saida)),
    "estilo": "drop",
    "corpo": "parte2.mp4",
    "hook": {"tipo": "antes", "video": str(Path(a.parte1))},
    "legenda": {"fonte": f"alinhamento:{ali}", "chaves": ["lymphoria", "miel", "gratis", "recibir", "noventa"]},
    "selo": {"linhas": SELO, "x": 160, "y": 1225, "desde": round(d1 + t_pides, 2)},
    "cta": {"palavra": "toca"},
    "limite_mb": 30,
    "resolucao": a.res,
}
(pasta / "receita_final.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
subprocess.run([sys.executable, str(KIT / "ferramentas" / "montar_ad.py"), str(pasta / "receita_final.json")], check=True)
