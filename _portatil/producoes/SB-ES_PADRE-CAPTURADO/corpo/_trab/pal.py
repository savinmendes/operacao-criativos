import json
def ali(p):
    a = json.load(open(p, encoding="utf-8"))
    ws, cur, t0 = [], "", None
    for c, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if c == " ":
            if cur: ws.append([cur, t0, pe])
            cur, t0 = "", None
        else:
            if t0 is None: t0 = s
            cur += c; pe = e
    if cur: ws.append([cur, t0, pe])
    return ws
