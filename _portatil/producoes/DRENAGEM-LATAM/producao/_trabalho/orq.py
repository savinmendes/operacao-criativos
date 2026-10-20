# -*- coding: utf-8 -*-
"""Variante do processar_ad.py com: troca de vários textos numa passada (textos_lote.py), remoção de trechos,
início cortado e gancho novo colado antes. Tempos da receita sempre no relógio do full_up720.

  python orq.py receita.json [--so-parte1]
Receita: {"ad":"ad05","corte":300.4,"saida":"AD 05 - ...mp4",
  "takes":[{"orig":"flora/t1.mp4","edit_url":"https://...","inicio":..,"quadros":..}],
  "blur":[{"de":..,"ate":..,"caixas":"x0,y0,x1,y1;..."}],
  "textos":[{... formato textos_lote.py ...}],
  "audios":[{"mp3":"p1.mp3","de":..,"ate":..}],
  "remover":[[ini,fim],...], "inicio":42.3, "hook":"hook_final.mp4"}
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
TRAB = Path(__file__).parent
R = json.load(open(sys.argv[1], encoding="utf-8-sig"))
P = TRAB / R["ad"]
SO_P1 = "--so-parte1" in sys.argv


def run(*a):
    print(">>", " ".join(str(x) for x in a[:4]), flush=True)
    subprocess.run([str(x) for x in a], check=True)


def py(tool, *a):
    run(sys.executable, tool, *a)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


trechos = []
for t in R.get("takes", []):
    orig = P / t["orig"]
    ed = orig.with_name(orig.stem + "_edit.mp4")
    fin = orig.with_name(orig.stem + "_final.mp4")
    if not ed.exists():
        urllib.request.urlretrieve(t["edit_url"], ed)
    if not fin.exists():
        py(KIT / "encaixar_edit.py", orig, ed, fin, "--dur", f"{t['quadros'] / 30:.3f}", *t.get("args", []))
    trechos.append({"clipe": str(fin), "inicio": t["inicio"], "quadros": t["quadros"]})
for e in R.get("extras", []):
    trechos.append({"clipe": str(P / e["clipe"]), "inicio": e["inicio"], "quadros": e["quadros"]})

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
    py(KIT / "substituir_trechos.py", cur, o, P / "trechos.json")
    cur = o
for b in R.get("blur", []):
    o = prox()
    py(KIT / "desfocar_regioes.py", cur, o, "--de", b["de"], "--ate", b["ate"], "--caixas", b["caixas"])
    cur = o
if R.get("blur_movel"):
    (P / "blur_movel.json").write_text(json.dumps(R["blur_movel"]), encoding="utf-8")
    o = prox()
    py(TRAB / "blur_movel.py", cur, o, P / "blur_movel.json")
    cur = o
if R.get("textos"):
    (P / "textos.json").write_text(json.dumps(R["textos"], ensure_ascii=False), encoding="utf-8")
    o = prox()
    py(TRAB / "textos_lote.py", cur, o, P / "textos.json")
    cur = o
for au in R.get("audios", []):
    o = prox()
    py(KIT / "trocar_trecho_audio.py", cur, P / au["mp3"], o, "--de", au["de"], "--ate", au["ate"])
    cur = o
corpo_tratado = P / "corpo_tratado.mp4"   # relógio original, 0..corte (usado também na versão curta)
if corpo_tratado.exists():
    corpo_tratado.unlink()
cur.replace(corpo_tratado)

# trechos mantidos (início, remoções)
ini = R.get("inicio", 0.0)
keep, t0 = [], ini
for a, b in sorted(R.get("remover", [])):
    keep.append((t0, a))
    t0 = b
keep.append((t0, R["corte"]))
partes = []
if R.get("hook"):
    partes.append(P / R["hook"])
for i, (a, b) in enumerate(keep):
    o = P / f"k{i}.mp4"
    run("ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", corpo_tratado, "-vf", "fps=30,setpts=PTS-STARTPTS",
        "-af", "aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,afade=t=in:d=0.03,"
        f"afade=t=out:st={max(0, b - a - 0.03):.3f}:d=0.03",
        "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", o)
    partes.append(o)
parte1 = P / "parte1.mp4"
ins = sum([["-i", str(p)] for p in partes], [])
fc = "".join(f"[{i}:v][{i}:a]" for i in range(len(partes))) + f"concat=n={len(partes)}:v=1:a=1[v][a]"
run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "15",
    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", parte1)
print("parte1", dur(parte1), flush=True)
if SO_P1:
    sys.exit(0)
saida = TRAB.parent / R["saida"]
a = [TRAB / "montar_fim_universal.py", P, parte1, P / "narr_fim.mp3", saida, "--res", "720"]
if R.get("cauda"):
    a += ["--cauda", P / R["cauda"]]
run(sys.executable, *a)
print("PRONTO", saida, flush=True)
