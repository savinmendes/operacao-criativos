# Monta narracao_es.wav (1 personagem: Desatadora/mulher) e o alinhamento no tempo do vídeo.
# Blocos em sequência: posição = fim do anterior + pausa; atempo por bloco (voz total <= 1,1x).
import json, re, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parent; AD = A.parent; T = A / "tts"
CFG = json.load(open(A / "blocos.json", encoding="utf-8"))
DUR = CFG["dur"]; SR = 44100

def lufs(f):
    o = subprocess.run(["ffmpeg","-i",str(f),"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

def fala(b, de=0.0, ate=1e9):
    al = json.load(open(T/f"{b}.alinhamento.json", encoding="utf-8"))
    c, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    idx = [k for k in range(len(c)) if not c[k].isspace() and s[k] >= de - 1e-6 and e[k] <= ate + 1e-6]
    return al, s[idx[0]], e[idx[-1]]

PECAS = []; t = None
for p in CFG["blocos"]:
    b, tempo = p["b"], p.get("atempo", CFG.get("atempo", 1.0))
    al, s0, e0 = fala(b, p.get("de", 0.0), p.get("ate", 1e9))
    c0 = max(0.0, s0 - 0.03)
    ini = p["pos"] if "pos" in p else t + p.get("pausa", 0.45)   # início da fala no vídeo
    pos = ini                                                   # onde o 1º som (c0) cai
    fim = pos + (e0 - c0) / tempo
    PECAS.append(dict(b=b, c0=c0, c1=min(e0 + 0.12, p.get("ate", 1e9) + 0.12), pos=pos, tempo=tempo, al=al))
    t = fim
ganho = {b: -16.0 - lufs(T/f"{b}.mp3") for b in {p["b"] for p in PECAS}}

ins, fil = [], []
for i, p in enumerate(PECAS):
    ins += ["-i", str(T/f"{p['b']}.mp3")]
    fil.append(f"[{i}]aresample={SR},aformat=channel_layouts=mono,atrim={p['c0']}:{p['c1']},asetpts=N/SR/TB,"
               f"atempo={p['tempo']},volume={ganho[p['b']]:.2f}dB,afade=t=in:d=0.015,afade=t=out:st={(p['c1']-p['c0'])/p['tempo']-0.06:.3f}:d=0.06,"
               f"adelay={int(round(p['pos']*1000))}[a{i}]")
n = len(PECAS)
fil.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{DUR}[base]")
fil.append("[base]" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n+1}:normalize=0:duration=first,alimiter=limit=0.95[o]")
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fil),"-map","[o]","-ar",str(SR),"-c:a","pcm_s16le",str(AD/"narracao_es.wav")],check=True)

C, S, E, tempos = [], [], [], []
for p in PECAS:
    ch, s, e = p["al"]["characters"], p["al"]["character_start_times_seconds"], p["al"]["character_end_times_seconds"]
    idx = [i for i in range(len(ch)) if s[i] >= p["c0"] - 0.01 and s[i] < p["c1"] - 0.1]
    while idx and ch[idx[0]].isspace(): idx.pop(0)
    while idx and ch[idx[-1]].isspace(): idx.pop()
    if C: C.append(" "); S.append(E[-1]); E.append(E[-1])
    f = lambda x: round(p["pos"] + (x - p["c0"]) / p["tempo"], 3)
    for i in idx: C.append(ch[i]); S.append(f(s[i])); E.append(f(e[i]))
    tempos.append({"b": p["b"], "texto": "".join(ch[i] for i in idx), "ini": f(s[idx[0]]), "fim": f(e[idx[-1]]), "atempo": p["tempo"]})
(AD/"narracao_es.alinhamento.json").write_text(json.dumps({"characters":C,"character_start_times_seconds":S,"character_end_times_seconds":E},ensure_ascii=False),encoding="utf-8")
json.dump(tempos, open(A/"tempos_reais.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
for x in tempos: print(x["b"], x["ini"], x["fim"], x["texto"][:70])
