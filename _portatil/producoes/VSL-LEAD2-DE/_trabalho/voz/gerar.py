import json, os, sys, re, concurrent.futures as cf, time
import tts
R = r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho"
BL = [b for b in json.load(open(R + r"\roteiro\roteiro_de.json", encoding="utf-8")) if not b.get("cortar")]
FAL = json.load(open("blocos_falante.json", encoding="utf-8"))
VOZ = json.load(open(R + r"\_vozes.json", encoding="utf-8"))
NORM = [("Kapitel 3, Vers 10", "Kapitel drei, Vers zehn"), ("57 Sekunden", "siebenundfünfzig Sekunden"),
        ("St. Benedikt", "Sankt Benedikt"), ("67 Jahre", "siebenundsechzig Jahre"), ("93-jähriger", "dreiundneunzigjähriger"),
        ("500-mal", "fünfhundertmal"), ("März 2025", "März zweitausendfünfundzwanzig"),
        ("November 2024", "November zweitausendvierundzwanzig"), ("49 Euro und 37 Cent", "neunundvierzig Euro und siebenunddreißig Cent"),
        ("300 Exemplare", "dreihundert Exemplare"), ("200 davon", "Zweihundert davon"), ("37 Euro", "siebenunddreißig Euro"),
        ("90-Tage-Garantie", "Neunzig-Tage-Garantie"), ("90 Tage", "neunzig Tage"), ("48 Stunden", "achtundvierzig Stunden")]
EXTRA = json.load(open("norm_extra.json", encoding="utf-8")) if os.path.exists("norm_extra.json") else {}
def texto_tts(b):
    t = EXTRA.get(b["id"], b["de"])
    for a, c in NORM: t = t.replace(a, c)
    return t
def job(i, force=False):
    b = BL[i]; f = FAL[b["id"]]["falante"]; v = VOZ[f]
    out = f"tts/{b['id']}.mp3"
    if os.path.exists(out) and not force: return b["id"], 0
    prev = " ".join(texto_tts(x) for x in BL[max(0, i - 2):i] if FAL[x["id"]]["falante"] == f) or None
    nxt = " ".join(texto_tts(x) for x in BL[i + 1:i + 2] if FAL[x["id"]]["falante"] == f) or None
    for tent in range(4):
        try:
            al, cost = tts.tts(v["voice_id"], texto_tts(b), out, settings=v["voice_settings"], prev=prev, nxt=nxt, lang="de")
            return b["id"], int(cost or 0)
        except Exception as e:
            print("erro", b["id"], str(e)[:200], file=sys.stderr); time.sleep(5 * (tent + 1))
    return b["id"], -1
if __name__ == "__main__":
    os.makedirs("tts", exist_ok=True)
    ids = sys.argv[1:]
    force = "--force" in ids; ids = [x for x in ids if x != "--force"]
    idx = [i for i, b in enumerate(BL) if not ids or b["id"] in ids]
    log = open("custo_chars.log", "a", encoding="utf-8"); tot = 0; k = 0
    with cf.ThreadPoolExecutor(4) as ex:
        for bid, c in ex.map(lambda i: job(i, force), idx):
            k += 1; tot += max(c, 0); log.write(f"{bid}\t{c}\n"); log.flush()
            if k % 10 == 0 or k == len(idx): print(f"[{k}/{len(idx)}] {100*k//len(idx)}% chars={tot}", flush=True)
