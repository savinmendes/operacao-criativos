# -*- coding: utf-8 -*-
"""Pipeline completo de um AD Lymphoria a partir de uma receita JSON (pula etapas cujo arquivo já existe).

  python processar_ad.py receita.json

Receita: {"ad":"ad12","corte":294.9,"saida":"AD 12 - ...mp4",
  "takes":[{"orig":"flora/t1.mp4","edit_url":"https://...","inicio":222.6,"quadros":31}],
  "extras":[{"clipe":"flora/cobre_tela.mp4","inicio":218.87,"quadros":34}],
  "blur":[{"de":..,"ate":..,"caixas":"x0,y0,x1,y1;..."}],
  "textos":[{"de":..,"ate":..,"caixa":"..","texto":"..","ref":299.9,"fonte":"Poppins-Bold.ttf"}],
  "audios":[{"mp3":"p1.mp3","de":..,"ate":..}],
  "cauda":null}
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
TRAB = Path(__file__).parent.parent  # script mora em ad03/
R = json.load(open(sys.argv[1], encoding="utf-8-sig"))
P = TRAB / R["ad"]


def run(*a):
    print(">>", " ".join(str(x) for x in a[:4]), flush=True)
    subprocess.run([str(x) for x in a], check=True)


def py(tool, *a):
    run(sys.executable, KIT / tool, *a)


# 1) takes Kling: baixa + encaixa
trechos = []
for i, t in enumerate(R.get("takes", []), 1):
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

# 2) base cortada
base = P / "base.mp4"
if not base.exists():
    run("ffmpeg", "-v", "error", "-y", "-i", P / "full_up720.mp4", "-t", R["corte"], "-c:v", "libx264", "-crf", "15",
        "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", base)
cur = base
etapa = 0


def prox():
    global etapa
    etapa += 1
    return P / f"b{etapa}.mp4"


if trechos:
    (P / "trechos.json").write_text(json.dumps(trechos), encoding="utf-8")
    o = prox()
    py("substituir_trechos.py", cur, o, P / "trechos.json")
    cur = o
for b in R.get("blur", []):
    o = prox()
    py("desfocar_regioes.py", cur, o, "--de", b["de"], "--ate", b["ate"], "--caixas", b["caixas"])
    cur = o
for t in R.get("textos", []):
    o = prox()
    a = ["--de", t["de"], "--ate", t["ate"], "--caixa", t["caixa"], "--texto", t["texto"]]
    for k in ("ref", "px", "contorno", "fonte"):
        if k in t:
            a += [f"--{k}", t[k]]
    if t.get("maiusc"):
        a.append("--maiusc")
    py("trocar_texto_tela.py", cur, o, *a)
    cur = o
for au in R.get("audios", []):
    o = prox()
    py("trocar_trecho_audio.py", cur, P / au["mp3"], o, "--de", au["de"], "--ate", au["ate"])
    cur = o

# 3) versão editada sem cortes fica guardada (serve para o CURTO); parte1 = só os trechos de cortes_longo.json
editado = P / "editado_full.mp4"
if cur != editado:
    if editado.exists():
        editado.unlink()
    cur.replace(editado)
parte1 = P / "parte1.mp4"
run(sys.executable, P / "concat_cortes.py", editado, P / R["cortes"], parte1)
if R.get("curto"):
    C = P / "curto"
    run(sys.executable, P / "concat_cortes.py", editado, P / R["cortes_curto"], C / "parte1.mp4")
    run(sys.executable, TRAB / "montar_fim_universal.py", C, C / "parte1.mp4", C / "narr_fim.mp3", TRAB.parent / R["curto"], "--res", "720")
    print("PRONTO", TRAB.parent / R["curto"], flush=True)
saida = TRAB.parent / R["saida"]
a = [TRAB / "montar_fim_universal.py", P, parte1, P / "narr_fim.mp3", saida, "--res", "720"]
if R.get("cauda"):
    a += ["--cauda", P / R["cauda"]]
run(sys.executable, *a)
print("PRONTO", saida, flush=True)
