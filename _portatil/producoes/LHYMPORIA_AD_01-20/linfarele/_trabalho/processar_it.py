# -*- coding: utf-8 -*-
"""Pipeline de um AD Linfarele (IT) a partir de uma receita JSON.

  python processar_it.py receita.json

Receita: {"ad":"ad06","corte":52.4,"saida":"AD 06 - LINFARELE-...-IT.mp4",
  "takes":[{"orig":"flora/t1.mp4","edit_url":"https://...","inicio":0.0,"quadros":162}],
  "audios":[{"mp3":"p1.mp3","de":..,"ate":..}]}
Base = up720.mp4 (vídeo sem legenda, 720p) + dub_it.mp3 (dublagem italiana), cortados em "corte".
Fim: fotos Linfarele + narração clonada (narr_fim.mp3) + legenda italiana no vídeo inteiro + selo IT + setas.
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import legenda as LEG  # noqa: E402

T = Path(__file__).parent
RENDER = T.parent.parent / "lymphoria" / "_trabalho" / "ad04" / "render_parte2.py"
FOTO1 = T / "assets" / "linf_1_sq.jpg"
FOTO_KIT = T / "assets" / "linf_3_sq.jpg"
SELO = ["SPEDIZIONE GRATUITA", "GARANZIA", "90 GIORNI", "SODDISFATTI O RIMBORSATI"]
R = json.load(open(sys.argv[1], encoding="utf-8-sig"))
P = T / R["ad"]


def run(*a):
    print(">>", " ".join(str(x) for x in a[:4]), flush=True)
    subprocess.run([str(x) for x in a], check=True)


def py(tool, *a):
    run(sys.executable, KIT / "ferramentas" / tool, *a)


trechos = []
for t in R.get("takes", []):
    orig = P / t["orig"]
    ed = orig.with_name(orig.stem + "_edit.mp4")
    fin = orig.with_name(orig.stem + "_final.mp4")
    if not ed.exists():
        urllib.request.urlretrieve(t["edit_url"], ed)
    if not fin.exists():
        py("encaixar_edit.py", orig, ed, fin, "--dur", f"{t['quadros'] / 30:.3f}", "--sem-legenda")
    trechos.append({"clipe": str(fin), "inicio": t["inicio"], "quadros": t["quadros"]})

base = P / "base.mp4"
if not base.exists():
    run("ffmpeg", "-v", "error", "-y", "-i", P / "up720.mp4", "-i", P / "dub_it.mp3", "-map", "0:v", "-map", "1:a",
        "-t", R["corte"], "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", base)
cur, etapa = base, 0


def prox():
    global etapa
    etapa += 1
    return P / f"b{etapa}.mp4"


if trechos:
    (P / "trechos.json").write_text(json.dumps(trechos), encoding="utf-8")
    o = prox()
    py("substituir_trechos.py", cur, o, P / "trechos.json")
    cur = o
for au in R.get("audios", []):
    o = prox()
    py("trocar_trecho_audio.py", cur, P / au["mp3"], o, "--de", au["de"], "--ate", au["ate"])
    cur = o
parte1 = P / "parte1.mp4"
if parte1.exists():
    parte1.unlink()
cur.replace(parte1)

narr = P / "narr_fim.mp3"
ali = str(narr.with_suffix("")) + ".alinhamento.json"
pal = LEG.palavras_por_alinhamento(ali, 0)
t_ord = next(b for w, b, *_ in pal if LEG._limpa(w).startswith("ordini"))
run(sys.executable, RENDER, narr, P / "parte2.mp4", f"{FOTO1}:0", f"{FOTO_KIT}:{t_ord:.3f}")
d1 = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", parte1],
                          capture_output=True, text=True).stdout)
saida = T.parent / R["saida"]
rec = {
    "saida": str(saida),
    "estilo": "drop",
    "corpo": "parte2.mp4",
    "hook": {"tipo": "antes", "video": str(parte1)},
    "legenda_hook": {"fonte": "transcrever", "idioma": "it", "modelo": "medium",
                     "corrigir": [[r"^l'?infarele", "Linfarele"], [r"^ma(i|y)a ?ver+a", "Linfarele"]]},
    "legenda": {"fonte": f"alinhamento:{ali}", "chaves": ["linfarele", "miele", "gratuita", "novanta"]},
    "selo": {"linhas": SELO, "x": 160, "y": 1225, "desde": round(d1 + t_ord, 2)},
    "cta": {"palavra": "tocca"},
    "limite_mb": 30,
    "resolucao": "720",
}
(P / "receita_final.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
py("montar_ad.py", P / "receita_final.json")
print("PRONTO", saida, flush=True)
