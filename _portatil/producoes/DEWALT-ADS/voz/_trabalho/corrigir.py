# -*- coding: utf-8 -*-
"""Regrava segmentos com palavra errada até o whisper ouvir o texto certo (máx. N tentativas).
  python corrigir.py id:i[:texto_tts_alternativo] ...
Guarda a melhor tentativa. Atualiza voz/<id>.mp3, alinhamento e relatorio_voz.json.
"""
import json, shutil, sys, difflib
from pathlib import Path
from faster_whisper import WhisperModel
import gerar_voz as G
from checar_whisper import norm  # noqa: reutiliza normalização (o import roda a checagem? não: protegido abaixo)

VOZ = G.VOZ
cfg = json.loads((VOZ / "_trabalho" / "voz_cfg.json").read_text(encoding="utf-8"))
itens = {i["id"]: i for i in cfg["itens"]}
m = WhisperModel(sys.argv[1] if sys.argv[1] in ("small", "medium") else "small", device="cpu", compute_type="int8")
alvos = [a for a in sys.argv[1:] if ":" in a]
TENT = 4


def ouvir(audio, ini, fim):
    segs, _ = m.transcribe(str(audio), language="es", word_timestamps=True)
    ws = [w for s in segs for w in s.words if ini - 0.15 <= (w.start + w.end) / 2 <= fim + 0.15]
    return " ".join(w.word for w in ws).strip()


def nota(esperado, ouvido):
    a, b = norm(esperado), norm(ouvido)
    b = " ".join(b).replace("the walt", "dewalt").replace("de wolt", "dewalt").replace("thewalt", "dewalt").split()
    falt = [x for x in a if x not in b]
    return difflib.SequenceMatcher(None, a, b).ratio() - 0.2 * len(falt), falt


rel_p = VOZ / "_trabalho" / "relatorio_voz.json"
for alvo in alvos:
    partes = alvo.split(":", 2)
    iid, i = partes[0], int(partes[1])
    item = itens[iid]
    if len(partes) == 3:
        item["segmentos"][i]["tts"] = partes[2]
    seg = G.SEG / f"{iid}_{i:02d}.mp3"
    melhor = None
    for t in range(TENT):
        if seg.exists():
            seg.unlink()
        Path(str(seg) + ".json").unlink(missing_ok=True)
        r = G.processar(item)
        s = r["segmentos"][i]
        ouvido = ouvir(VOZ / f"{iid}.mp3", s["inicio"], s["fim"])
        n, falt = nota(s["texto"], ouvido)
        print(f"{iid}[{i}] tentativa {t+1}: {n:.2f} faltando={falt} | {ouvido}", flush=True)
        if melhor is None or n > melhor[0]:
            melhor = (n, t)
            shutil.copy(seg, str(seg) + ".best")
            shutil.copy(str(seg) + ".json", str(seg) + ".best.json")
        if not falt:
            break
    shutil.copy(str(seg) + ".best", seg)
    shutil.copy(str(seg) + ".best.json", str(seg) + ".json")
    r = G.processar(item)
    old = json.loads(rel_p.read_text(encoding="utf-8"))
    old[iid] = r
    rel_p.write_text(json.dumps(old, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"=> {iid}[{i}] ficou a tentativa {melhor[1]+1} (nota {melhor[0]:.2f})", flush=True)

(VOZ / "_trabalho" / "voz_cfg.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
