# Monta narracao_es.wav, narr_jesus.wav, narr_mulher.wav e o alinhamento no tempo do video.
import json, re, subprocess
from pathlib import Path
A = Path(__file__).resolve().parent; AD = A.parent; T = A / "tts"
DUR = 106.2; SR = 44100
# (bloco, corte_ini, corte_fim, posicao_no_video, quem)
PECAS = [("c0", 0, None, 0.55, "MULHER"),
         ("c1", 0, None, 9.85, "MULHER"),
         ("b2v2", 0, None, 19.45, "MULHER"),
         ("b3v2", 0, None, 29.30, "MULHER"),
         ("b4v2", 0, None, 42.40, "MULHER"),
         ("c5", 0, None, 56.30, "MULHER"),
         ("b6", 0, None, 69.70, "MULHER"),
         ("c7", 0, None, 76.70, "MULHER"),
         ("b8", 0, None, 89.20, "MULHER")]

def dur(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)]))

def lufs(f):
    o = subprocess.run(["ffmpeg","-i",str(f),"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

ganho = {b: -16.0 - lufs(T/f"{b}.mp3") for b in sorted({p[0] for p in PECAS})}

def mix(pecas, saida):
    ins, fil = [], []
    for i,(b,c0,c1,pos,q) in enumerate(pecas):
        ins += ["-i", str(T/f"{b}.mp3")]
        tr = f"atrim={c0}" + (f":{c1}" if c1 else "")
        fil.append(f"[{i}]aresample={SR},aformat=channel_layouts=mono,{tr},asetpts=N/SR/TB,volume={ganho[b]:.2f}dB,"
                   f"afade=t=in:d=0.02,adelay={int(round(pos*1000))}[a{i}]")
    n = len(pecas)
    fil.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{DUR}[base]")
    fil.append("[base]" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n+1}:normalize=0:duration=first,alimiter=limit=0.95[o]")
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fil),"-map","[o]","-ar",str(SR),"-c:a","pcm_s16le",str(saida)],check=True)

mix(PECAS, AD/"narracao_es.wav")
mix([p for p in PECAS if p[4]=="MULHER"], AD/"narr_mulher.wav")

# alinhamento por caractere no tempo do video
C, S, E = [], [], []
tempos = []
for b,c0,c1,pos,q in PECAS:
    al = json.load(open(T/f"{b}.alinhamento.json", encoding="utf-8"))
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    idx = [i for i in range(len(ch)) if s[i] >= c0 and (c1 is None or s[i] < c1)]
    while idx and ch[idx[0]].isspace(): idx.pop(0)
    while idx and ch[idx[-1]].isspace(): idx.pop()
    if C:
        C.append(" "); S.append(E[-1]); E.append(E[-1])
    off = pos - c0
    primeiro = True
    for i in idx:
        cc = ch[i].upper() if (primeiro and c0 > 0) else ch[i]; primeiro = False
        C.append(cc); S.append(round(s[i]+off,3)); E.append(round(e[i]+off,3))
    tempos.append({"quem": q, "texto": "".join(C[len(C)-len(idx):]), "ini": round(s[idx[0]]+off,2), "fim": round(e[idx[-1]]+off,2)})
(AD/"narracao_es.alinhamento.json").write_text(json.dumps({"characters":C,"character_start_times_seconds":S,"character_end_times_seconds":E},ensure_ascii=False),encoding="utf-8")
json.dump(tempos, open(A/"tempos_reais.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
for t in tempos: print(t["quem"], t["ini"], t["fim"], t["texto"][:60])
for f in ["narracao_es.wav","narr_mulher.wav"]: print(f, round(dur(AD/f),2))
