# -*- coding: utf-8 -*-
"""Remenda um AD já montado: encaixa mais um take Kling na parte1.mp4 existente e remonta o fim.
  python remendar_ad.py ad14 <edit_url> flora2/t6.mp4 382.167 38 "AD 14 - ....mp4"
orig = take cortado da parte1.mp4 (legenda já trocada), para o encaixe restaurar a legenda certa."""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
T = Path(__file__).parent
ad, url, orig, ini, q, saida = sys.argv[1:7]
P = T / ad
orig = P / orig
ed = orig.with_name(orig.stem + "_edit.mp4")
fin = orig.with_name(orig.stem + "_final.mp4")
if not ed.exists():
    urllib.request.urlretrieve(url, ed)
subprocess.run([sys.executable, KIT / "encaixar_edit.py", orig, ed, fin, "--dur", f"{int(q) / 30:.3f}"], check=True)
(P / "trechos_remendo.json").write_text(json.dumps([{"clipe": str(fin), "inicio": float(ini), "quadros": int(q)}]))
p1b = P / "parte1_remendo.mp4"
subprocess.run([sys.executable, KIT / "substituir_trechos.py", P / "parte1.mp4", p1b, P / "trechos_remendo.json"], check=True)
p1b.replace(P / "parte1.mp4")
subprocess.run([sys.executable, T / "montar_fim_universal.py", P, P / "parte1.mp4", P / "narr_fim.mp3",
                T.parent / saida, "--res", "720"], check=True)
print("PRONTO", saida)
