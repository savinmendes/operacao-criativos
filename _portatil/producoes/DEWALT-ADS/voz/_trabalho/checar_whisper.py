# -*- coding: utf-8 -*-
"""Confere cada áudio de voz/ com whisper (es) contra o texto do roteiro, por segmento."""
import json, re, sys, unicodedata, difflib
from pathlib import Path
from faster_whisper import WhisperModel

VOZ = Path(r"C:\Users\PICHAU\Downloads\DEWALT-ADS\voz")
cfg = json.loads((VOZ / "_trabalho" / "voz_cfg.json").read_text(encoding="utf-8"))
rel = json.loads((VOZ / "_trabalho" / "relatorio_voz.json").read_text(encoding="utf-8"))
so = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else None

NUM = {"1750": "mil setecientas cincuenta", "17": "diecisiete", "15": "quince", "13": "trece", "20": "veinte", "2": "dos"}


def norm(t):
    t = t.lower().replace("%", " por ciento").replace("20v", "veinte volts")
    t = re.sub(r"(\d)[.,](\d{3})", r"\1\2", t)
    for k in sorted(NUM, key=len, reverse=True):
        t = re.sub(rf"\b{k}\b", NUM[k], t)
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = " " + re.sub(r"\s+", " ", t).strip() + " "
    for v in ("de walt", "diwalt", "the walt", "thewalt", "de wolt", "de wall"):
        t = t.replace(f" {v} ", " dewalt ")
    return t.split()


def main():
    import os
    m = WhisperModel(os.environ.get("WM", "small"), device="cpu", compute_type="int8")
    saida = {}
    for item in cfg["itens"]:
        iid = item["id"]
        if so and iid not in so:
            continue
        segs, _ = m.transcribe(str(VOZ / f"{iid}.mp3"), language="es", word_timestamps=True, vad_filter=False)
        words = [(w.start, w.end, w.word) for s in segs for w in s.words]
        rows = []
        for k, s in enumerate(rel[iid]["segmentos"]):
            ini, fim = s["inicio"] - 0.2, s["fim"] + 0.2
            ouvido = " ".join(w[2] for w in words if ini <= (w[0] + w[1]) / 2 <= fim)
            a, b = norm(s["texto"]), norm(ouvido)
            sm = difflib.SequenceMatcher(None, a, b)
            dif = [(" ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
            rows.append({"i": k, "esperado": s["texto"], "ouvido": ouvido.strip(), "ratio": round(sm.ratio(), 3), "dif": dif})
        saida[iid] = rows
        ruins = [r for r in rows if r["dif"]]
        print(f"== {iid}: {len(rows)} seg, {len(ruins)} com diferença")
        for r in ruins:
            print(f"   [{r['i']}] {r['ratio']} {r['dif']} | ouvido: {r['ouvido']}")
    p = VOZ / "_trabalho" / "whisper_check.json"
    old = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    old.update(saida)
    p.write_text(json.dumps(old, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
