import json, sys
def pal(path):
    path = str(path)
    al = json.load(open(path, encoding="utf-8"))
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]; out = []; w = ""
    for c, x, y in zip(ch, s, e):
        if c.isspace():
            if w: out.append([w, ws, we]); w = ""
        else:
            if not w: ws = x
            w += c; we = y
    if w: out.append([w, ws, we])
    return out
if __name__ == "__main__":
    for k in sys.argv[1:]: print(k, " ".join(f"{w}[{a:.2f}-{b:.2f}]" for w, a, b in pal(f"tts/{k}.alinhamento.json")))
