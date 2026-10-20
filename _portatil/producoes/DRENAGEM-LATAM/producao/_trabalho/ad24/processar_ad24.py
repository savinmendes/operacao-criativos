# -*- coding: utf-8 -*-
"""AD 24 (longo 12:56 -> ~7 min e curto ~85 s). Como processar_ad.py, mas a parte 1 é feita de TRECHOS
não contíguos do vídeo tratado (takes Kling encaixados).

  python processar_ad24.py r24.json            -> monta longo e curto
  python processar_ad24.py r24.json --so-base  -> só a base tratada (takes)
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
P = Path(__file__).parent
TRAB = P.parent
R = json.load(open(sys.argv[1], encoding="utf-8-sig"))


def run(*a):
    print(">>", " ".join(str(x) for x in a[:4]), flush=True)
    subprocess.run([str(x) for x in a], check=True)


def py(tool, *a):
    run(sys.executable, KIT / tool, *a)


# 1) takes Kling: baixa + encaixa
trechos = []
for t in R.get("takes", []):
    orig = P / t["orig"]
    ed = orig.with_name(orig.stem + "_edit.mp4")
    fin = orig.with_name(orig.stem + "_final.mp4")
    if not ed.exists():
        urllib.request.urlretrieve(t["edit_url"], ed)
    if not fin.exists():
        py("encaixar_edit.py", orig, ed, fin, "--dur", f"{t['quadros'] / 30:.3f}")
    trechos.append({"clipe": str(fin), "inicio": t["inicio"], "quadros": t["quadros"]})
for e in R.get("extras", []):
    trechos.append({"clipe": str(P / e["clipe"]), "inicio": e["inicio"], "quadros": e["quadros"]})

# 2) base (até o fim do último trecho usado) + trocas
base = P / "base.mp4"
if not base.exists():
    run("ffmpeg", "-v", "error", "-y", "-i", P / "full_up720.mp4", "-t", R["corte"], "-c:v", "libx264", "-crf", "15",
        "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", base)
tratado = P / "tratado.mp4"
cur = base
if tratado.exists() and "--refazer" not in sys.argv:
    trechos = []; R["blur"] = []
if trechos:
    (P / "trechos.json").write_text(json.dumps(trechos), encoding="utf-8")
    o = P / "b1.mp4"
    py("substituir_trechos.py", cur, o, P / "trechos.json")
    cur = o
for k, b in enumerate(R.get("blur", []), 2):
    o = P / f"b{k}.mp4"
    py("desfocar_regioes.py", cur, o, "--de", b["de"], "--ate", b["ate"], "--caixas", b["caixas"])
    cur = o
if cur != base:
    if tratado.exists():
        tratado.unlink()
    cur.replace(tratado)
if "--so-base" in sys.argv:
    sys.exit(0)


def concatena(segs, saida):
    """Corta [ini, fim] do vídeo tratado e junta, com micro-fade de áudio (15 ms) em cada emenda."""
    fc, ins = [], ""
    for i, (a, b) in enumerate(segs):
        d = b - a
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
        fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,"
                  f"afade=t=out:st={d - 0.015:.3f}:d=0.015[a{i}]")
        ins += f"[v{i}][a{i}]"
    fc.append(f"{ins}concat=n={len(segs)}:v=1:a=1[v][a]")
    run("ffmpeg", "-v", "error", "-y", "-i", tratado, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", saida)


for nome in ("longo", "curto"):
    v = R[nome]
    pasta = P if nome == "longo" else P / "curto"
    parte1 = pasta / "parte1.mp4"
    concatena(v["segmentos"], parte1)
    run(sys.executable, TRAB / "montar_fim_universal.py", pasta, parte1, pasta / "narr_fim.mp3",
        TRAB.parent / v["saida"], "--res", "720")
    print("PRONTO", v["saida"], flush=True)
