# -*- coding: utf-8 -*-
"""alinhamento por caractere -> palavras [{w, ini, fim}]"""
import json, sys
def palavras(jp):
    a = json.load(open(jp, encoding="utf-8"))
    ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    out = []; cur = ""; i0 = None; i1 = None
    for c, s, e in zip(ch, st, en):
        if c.isspace():
            if cur: out.append(dict(w=cur, ini=i0, fim=i1)); cur = ""
            continue
        if not cur: i0 = s
        cur += c; i1 = e
    if cur: out.append(dict(w=cur, ini=i0, fim=i1))
    return out
if __name__ == "__main__":
    for f in sys.argv[1:]:
        P = palavras(f); print(f, "inicio", P[0]["ini"], "fim", P[-1]["fim"])
        for a, b in zip(P, P[1:]):
            if b["ini"] - a["fim"] > 0.3: print(f"   pausa {a['fim']:.2f}-{b['ini']:.2f} ({b['ini']-a['fim']:.2f}) depois de '{a['w']}'")
