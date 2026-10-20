# Monta narracao_es.wav (sequencial, gap fixo entre blocos) + alinhamento no tempo do video. Uso: python montar_narracao.py [AD_DIR] [b0_arquivo]
import json, re, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parent; AD = Path(sys.argv[1]) if len(sys.argv) > 1 else A.parent; T = A / "tts"
SR = 44100; GAP = 0.46; INI = 0.15
B0 = sys.argv[2] if len(sys.argv) > 2 else "b0"
ORDEM = [B0] + [f"b{i}" for i in range(1, 12)]
def lufs(f):
    o = subprocess.run(["ffmpeg","-i",str(f),"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
def fala(b):
    al = json.load(open(T/f"{b}.alinhamento.json", encoding="utf-8"))
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    idx = [i for i in range(len(ch)) if not ch[i].isspace()]
    return al, s[idx[0]], e[idx[-1]]
pecas = []; t = INI
for b in ORDEM:
    al, s0, s1 = fala(b); pos = t - s0; pecas.append((b, pos, al)); t = pos + s1 + GAP
FIM = t - GAP; DUR = round(FIM + 0.7, 3)
ins, fil = [], []
for i, (b, pos, al) in enumerate(pecas):
    g = -16.0 - lufs(T/f"{b}.mp3"); ins += ["-i", str(T/f"{b}.mp3")]
    fil.append(f"[{i}]aresample={SR},aformat=channel_layouts=mono,volume={g:.2f}dB,afade=t=in:d=0.02,adelay={int(round(pos*1000))}[a{i}]")
n = len(pecas)
fil.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{DUR}[base]")
fil.append("[base]" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n+1}:normalize=0:duration=first,alimiter=limit=0.95[o]")
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fil),"-map","[o]","-ar",str(SR),"-c:a","pcm_s16le",str(AD/"narracao_es.wav")],check=True)
C, S, E, tempos = [], [], [], []
for b, pos, al in pecas:
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    idx = [i for i in range(len(ch))]
    while ch[idx[0]].isspace(): idx.pop(0)
    while ch[idx[-1]].isspace(): idx.pop()
    if C: C.append(" "); S.append(E[-1]); E.append(E[-1])
    for i in idx: C.append(ch[i]); S.append(round(s[i]+pos,3)); E.append(round(e[i]+pos,3))
    tempos.append({"id": b, "ini": round(s[idx[0]]+pos,2), "fim": round(e[idx[-1]]+pos,2), "texto": "".join(ch[i] for i in idx)})
(AD/"narracao_es.alinhamento.json").write_text(json.dumps({"characters":C,"character_start_times_seconds":S,"character_end_times_seconds":E},ensure_ascii=False),encoding="utf-8")
json.dump({"dur": DUR, "fim_fala": round(FIM,3), "blocos": tempos}, open(AD/"tempos_reais.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
for x in tempos: print(x["id"], x["ini"], x["fim"], x["texto"][:50])
print("DUR", DUR)
