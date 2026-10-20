# encurta pausas >0,35 s entre palavras das narrações TTS (para 0,25 s) e remapeia o alinhamento
import json, subprocess
MAXP, NOVA = 0.35, 0.25
for n in ["L4_oferta", "L5_dia", "L6_noche", "L7_finde", "L8_cta"]:
    a = json.load(open(f"audio/{n}.alinhamento.json", encoding="utf-8"))
    ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    # palavras: blocos de caracteres não-espaço
    words, i = [], 0
    while i < len(ch):
        if ch[i].isspace(): i += 1; continue
        j = i
        while j < len(ch) and not ch[j].isspace(): j += 1
        words.append((i, j - 1)); i = j
    cuts = []  # (ini, fim) a remover
    for (a0, a1), (b0, b1) in zip(words, words[1:]):
        ia = max(k for k in range(a0, a1 + 1) if ch[k].isalnum()) if any(ch[k].isalnum() for k in range(a0, a1 + 1)) else a1
        ib = min(k for k in range(b0, b1 + 1) if ch[k].isalnum()) if any(ch[k].isalnum() for k in range(b0, b1 + 1)) else b0
        g0, g1 = en[ia], st[ib]
        if g1 - g0 > MAXP:
            cuts.append((g0 + NOVA / 2, g1 - NOVA / 2))
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"audio/{n}.mp3"]))
    keep, t = [], 0.0
    for c0, c1 in cuts: keep.append((t, c0)); t = c1
    keep.append((t, dur))
    def remap(x):
        off = 0.0
        for c0, c1 in cuts:
            if x >= c1: off += c1 - c0
            elif x > c0: return c0 - off
        return x - off
    fc = "".join(f"[0:a]atrim={k0:.3f}:{k1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(k1-k0-0.01,0):.3f}:d=0.01[s{i}];" for i, (k0, k1) in enumerate(keep))
    fc += "".join(f"[s{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"audio/{n}.mp3", "-filter_complex", fc, "-map", "[o]", "-b:a", "192k", f"audio/{n}_c.mp3"], check=True)
    b = {"characters": ch, "character_start_times_seconds": [round(remap(x), 3) for x in st], "character_end_times_seconds": [round(remap(x), 3) for x in en]}
    json.dump(b, open(f"audio/{n}_c.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    d2 = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"audio/{n}_c.mp3"]))
    print(n, round(dur, 2), "->", round(d2, 2), "cortes", [(round(c0, 2), round(c1, 2)) for c0, c1 in cuts], "ultimo fim", b["character_end_times_seconds"][-1])
