# -*- coding: utf-8 -*-
"""Monta os 14 videos DCD7781 (montar.py) e aplica a cama de musica trend (mixar_cama.py, BbY WOW instrumental, -32 LUFS sob a fala).
  python rodar_lote.py [nome ...]   (sem nome = todos os cfg/*_voz.json e *_fundo.json)"""
import json
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
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode != 0:
        raise RuntimeError(" ".join(map(str, args)) + "\n" + r.stdout[-1500:] + r.stderr[-2500:])
    return r.stdout


def painel(*a):
    subprocess.run([PY, PAINEL, *a], capture_output=True)


plano = json.load(open(ED / "cfg" / "_plano.json", encoding="utf-8"))
nomes = sys.argv[1:] or list(plano)
ENT.mkdir(exist_ok=True)
rel = {}
t0 = time.time()
for k, n in enumerate(nomes, 1):
    painel("etapa", "montagem7781", "Montagem DCD7781 (14 vídeos)", "--texto", f"[{k}/{len(nomes)}] {n}", "--k", str(k),
           "--n", str(len(nomes)))
    r = {}
    out = run([PY, "montar.py", f"cfg/{n}_voz.json"])
    r["montar_voz"] = json.loads(out[out.index("{\n"):out.rindex("}") + 1])
    base = ED / "_montado" / f"{n}_voz.mp4"
    final = ENT / f"DW7781_{n}.mp4"
    out = run([PY, "mixar_cama.py", "bbywow", "--base", base, "--saida", final, "--tit", "0", "--cta", "0.8", "--tag", n])
    r["mix"] = json.loads(out.strip().splitlines()[-1])
    if n.startswith("TR"):
        out = run([PY, "montar.py", f"cfg/{n}_fundo.json"])
        r["montar_fundo"] = json.loads(out[out.index("{\n"):out.rindex("}") + 1])
        shutil.copy(ED / "_montado" / f"{n}_fundo.mp4", ENT / f"DW7781_{n}_fundo-original.mp4")
    else:
        shutil.copy(base, ENT / f"DW7781_{n}_sem-musica.mp4")
    shutil.copy(ED / "_montado" / f"{n}_voz_prova.jpg", ENT / "_provas" / f"DW7781_{n}_prova.jpg") \
        if (ENT / "_provas").exists() else ((ENT / "_provas").mkdir(),
                                            shutil.copy(ED / "_montado" / f"{n}_voz_prova.jpg", ENT / "_provas" / f"DW7781_{n}_prova.jpg"))
    painel("img", "montagem7781", str(ENT / "_provas" / f"DW7781_{n}_prova.jpg"), "--legenda", n)
    rel[n] = r
    el = time.time() - t0
    print(f"[{k}/{len(nomes)}] {n} ok | {100 * k // len(nomes)}% | falta ~{el / k * (len(nomes) - k) / 60:.1f} min", flush=True)
    json.dump(rel, open(ED / "_relatorio_lote.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("FIM")
