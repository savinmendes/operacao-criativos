# -*- coding: utf-8 -*-
"""Roda o checar_lipsync.py do kit (criterio oficial: pausas >= 8 quadros) e, quando a voz DE nao tem pausa longa,
o mesmo indice com pausas curtas (>= 4 quadros, 1 quadro de borda), como no s08 do AD 01 (LICOES-LIPSYNC.md).
Uso: python medir.py saida.mp4 audio_novo.mp3 original.mp4 [--sem-audio-original] -> imprime JSON."""
import sys, json, io, contextlib
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as C

saida, an, orig = sys.argv[1:4]
ao = False if "--sem-audio-original" in sys.argv else None
with contextlib.redirect_stdout(io.StringIO()):
    r = C.checar(saida, an, orig, ao)
out = {"indice": r.get("indice_pausa"), "n_pausa": r.get("n_pausa"), "status": r.get("status"), "mudou": r.get("mudou"),
       "corr_novo": r.get("corr_novo"), "corr_original": r.get("corr_original"), "motivo": r.get("motivo"),
       "texto": C.formatar(r)}
if out["indice"] is None:
    orig_mp = C.mascara_pausas
    C.mascara_pausas = lambda fala, min_q=4, borda=1: orig_mp(fala, 4, 1)
    C.MIN_Q_PAUSA = 4
    with contextlib.redirect_stdout(io.StringIO()):
        r2 = C.checar(saida, an, orig, ao)
    out["indice_curto"] = r2.get("indice_pausa"); out["n_pausa_curto"] = r2.get("n_pausa")
print(json.dumps(out, ensure_ascii=False, default=float))
