# -*- coding: utf-8 -*-
"""Legenda DE no estilo da original (branca, caixa escura translucida por linha, embaixo, ate 2 linhas)."""
import sys, json, re
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import T, M
P = json.load(open(M / "params.json")); T0 = P["T0"]; DUR = P["NF"] / 30
pw = [w for w in json.load(open(T / "voz" / "alinhamento_de.json", encoding="utf-8"))["palavras"] if w["ini"] >= T0]
MAXC = 44  # ~2 linhas de 22-26
TROCA = {"neunundneunzig": "99", "dreiundzwanzigsten": "23.", "vierundzwanzigsten": "24.", "neunzigtausend": "90.000",
         "fünfunddreißigtausend": "35.000", "neunundzwanzigtausendsiebenhundert": "29.700", "Seelische": "seelische"}
def limpa(s):
    s = s.replace("„", "").replace("“", "").replace('"', "")
    core = s.rstrip(".,;:!?"); tail = s[len(core):]
    return TROCA.get(core, core) + tail
chunks = []; cur = []
for i, w in enumerate(pw):
    cur.append(w)
    txt = " ".join(limpa(x["palavra"]) for x in cur)
    nxt = pw[i + 1] if i + 1 < len(pw) else None
    fim_frase = re.search(r"[.?!:;]$", limpa(w["palavra"])) is not None
    virg = limpa(w["palavra"]).endswith((",", "–"))
    gap = (nxt["ini"] - w["fim"]) if nxt else 9
    prox_len = len(txt) + 1 + len(limpa(nxt["palavra"])) if nxt else 999
    if (nxt is None or fim_frase or gap > 0.45 or prox_len > MAXC or (virg and len(txt) > 22)
            or nxt["bloco"] != w["bloco"]):
        chunks.append(cur); cur = []
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
L = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 960", "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
     "[V4+ Styles]",
     "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
     "Style: Leg,Segoe UI Semibold,53,&H00FFFFFF,&H00FFFFFF,&H8C000000,&H00000000,0,0,0,0,100,100,0,0,3,4,0,2,48,48,80,1", "",
     "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
out = []
for k, c in enumerate(chunks):
    a = c[0]["ini"] - T0; b = c[-1]["fim"] - T0 + 0.35
    if k + 1 < len(chunks): b = min(b, chunks[k + 1][0]["ini"] - T0 - 0.02)
    b = max(b, a + 0.4); b = min(b, DUR)
    txt = " ".join(limpa(x["palavra"]) for x in c).rstrip(",;:–- ")
    if not re.search(r"[0-9]{1,2}[.]$", txt): txt = txt.rstrip(".")  # mantem o ponto do ordinal (am 24.)
    txt = txt.replace(" – ", " – ")
    out.append((a, b, txt))
    L.append(f"Dialogue: 0,{ts(a)},{ts(b)},Leg,,0,0,0,,{txt}")
open(M / "legenda_de.ass", "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump(out, open(M / "legenda_de.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "legendas; maior", max(len(t) for _, _, t in out))
