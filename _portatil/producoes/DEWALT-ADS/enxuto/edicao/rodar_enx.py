# -*- coding: utf-8 -*-
"""Monta as execucoes do pacote enxuto (montar.py) e aplica a cama de musica trend bbywow -32 LUFS (mixar_cama.py).
  python rodar_enx.py [nome ...]   -> enxuto/entregas/DW7781_<nome>.mp4"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ED = Path(__file__).resolve().parent
ENT = ED.parent / "entregas"
PAINEL = r"C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py"
PY = sys.executable


def run(args):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ED,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode != 0:
        raise RuntimeError(" ".join(map(str, args)) + "\n" + r.stdout[-1500:] + r.stderr[-2500:])
    return r.stdout


plano = json.load(open(ED / "cfg_enx" / "_plano.json", encoding="utf-8"))
nomes = sys.argv[1:] or list(plano)
(ENT / "_provas").mkdir(parents=True, exist_ok=True)
relp = ED / "_relatorio_enx.json"
rel = json.load(open(relp, encoding="utf-8")) if relp.exists() else {}
t0 = time.time()
for k, n in enumerate(nomes, 1):
    subprocess.run([PY, PAINEL, "etapa", "montenx", "Montagem pacote enxuto DeWalt", "--texto", f"[{k}/{len(nomes)}] {n}",
                    "--k", str(k), "--n", str(len(nomes))], capture_output=True)
    r = {}
    out = run([PY, "montar.py", f"cfg_enx/{n}.json"])
    r["montar"] = json.loads(out[out.index("{\n"):out.rindex("}") + 1])
    base = ED / "_montado" / f"{n}.mp4"
    final = ENT / f"DW7781_{n}.mp4"
    out = run([PY, "mixar_cama.py", "bbywow", "--base", base, "--saida", final, "--tit", "0", "--cta", "0.8", "--tag", n])
    r["mix"] = json.loads(out.strip().splitlines()[-1])
    shutil.copy(ED / "_montado" / f"{n}_prova.jpg", ENT / "_provas" / f"DW7781_{n}_prova.jpg")
    subprocess.run([PY, PAINEL, "img", "montenx", str(ENT / "_provas" / f"DW7781_{n}_prova.jpg"), "--legenda", n],
                   capture_output=True)
    rel[n] = r
    el = time.time() - t0
    print(f"[{k}/{len(nomes)}] {n} ok | {100 * k // len(nomes)}% | falta ~{el / k * (len(nomes) - k) / 60:.1f} min", flush=True)
    json.dump(rel, open(relp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("FIM")
