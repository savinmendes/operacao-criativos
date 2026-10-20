# -*- coding: utf-8 -*-
"""Mostra a transcrição de um AD a partir de um tempo e lista menções à marca/oferta.
  python ver_texto.py 05 [--de 50]"""
import json
import re
import sys
from pathlib import Path

ad = sys.argv[1]
de = float(sys.argv[sys.argv.index("--de") + 1]) if "--de" in sys.argv else None
P = Path(__file__).parent / "transcricoes_palavras" / f"AD {ad}.json"
pal = json.loads(P.read_text(encoding="utf-8"))
dur = pal[-1][2] if pal else 0
padrao = re.compile(r"(?i)maya|berra|verra|vera\b|linfor|lymph|descuento|%|garant|clic|enlace|link|precio|oferta|walmart|gnc|libras|cofepris")
hits = [f"{w}@{a:.1f}" for w, a, b in pal if padrao.search(w)]
print(f"AD {ad} | {dur:.0f}s | marcas/oferta: {' '.join(hits)}")
if de is None:
    de = max(0, dur - 60)
print(" ".join(f"{a:.1f}:{w}" for w, a, b in pal if a >= de))
