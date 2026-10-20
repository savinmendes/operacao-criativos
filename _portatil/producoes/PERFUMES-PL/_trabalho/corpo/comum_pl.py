import json, re
def palavras(alin):
    a = json.load(open(alin, encoding="utf-8"))
    ch, s, e = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    out = []; cur = ""; t0 = None; t1 = None
    for c, a0, a1 in zip(ch, s, e):
        if c.isspace():
            if cur: out.append([t0, t1, cur]); cur = ""
            continue
        if not cur: t0 = a0
        cur += c; t1 = a1
    if cur: out.append([t0, t1, cur])
    return out
