# v3 (compliance: fala do marido reescrita, b5v3 + b5v3s2). Monta narracao_es.wav, narr_<pers>.wav, fundo_es.wav e o alinhamento no tempo do vídeo NOVO
# (tempo novo = tempo original, exceto o trecho 53,583-56,5 s do original, que foi cortado: depois dele, t_novo = t_orig - 2,9167).
import json, re, subprocess
from pathlib import Path
A = Path(__file__).resolve().parent; AD = A.parent; T = A / "tts"
SR = 44100
CUT_A, CUT_B = 1286/24, 1356/24
DUR = 2368/24 - (CUT_B - CUT_A)          # 95.75 s (fim da tomada da Desatadora)
FIM = 95.5                               # corte final (~0,7 s após a última fala)
# (bloco, frases [i0,i1] inclusivas, posição no vídeo novo, quem)
PECAS = [("b0",(0,0),0.10,"CLARA"), ("b1",(0,0),3.95,"MARIDO"), ("b2",(0,0),6.15,"CLARA"), ("b3",(0,0),8.95,"MARIDO"),
         ("b4",(0,0),12.15,"CLARA"), ("b4",(1,1),18.10,"CLARA"), ("b4",(2,2),23.84,"CLARA"),
         ("b5v3",(0,1),27.25,"MARIDO"), ("b5v3s2",(0,0),31.28,"MARIDO"), ("b5v3",(3,3),37.30,"MARIDO"), ("b5v3",(4,4),42.85,"MARIDO"), ("b5v3",(5,5),47.90,"MARIDO"),
         ("b6",(0,0),54.30,"DESATADORA"), ("b6",(1,2),61.70,"DESATADORA"), ("b6",(3,3),65.70,"DESATADORA"), ("b6",(4,4),71.45,"DESATADORA"),
         ("b6",(5,5),73.40,"DESATADORA"), ("b6",(6,6),75.35,"DESATADORA"), ("b6",(7,7),83.50,"DESATADORA"), ("b6",(8,8),84.95,"DESATADORA"),
         ("b6",(9,9),90.40,"DESATADORA")]

def frases(b):
    al = json.load(open(T/f"{b}.alinhamento.json", encoding="utf-8"))
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    txt = "".join(ch); out = []
    for m in re.finditer(r"[^.?!:]+[.?!:]?", txt):
        a, z = m.start(), m.end()-1
        while a < z and txt[a].isspace(): a += 1
        if z <= a: continue
        out.append((a, z))
    return ch, s, e, out

def lufs(f):
    o = subprocess.run(["ffmpeg","-i",str(f),"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

ganho = {b: -16.0 - lufs(T/f"{b}.mp3") for b in sorted({p[0] for p in PECAS})}
info = []
for b,(i0,i1),pos,q in PECAS:
    ch,s,e,fr = frases(b)
    a, z = fr[i0][0], fr[i1][1]
    c0 = max(0.0, s[a]-0.06); c1 = e[z]+0.12
    info.append(dict(b=b,c0=c0,c1=c1,pos=pos,q=q,idx=list(range(a,z+1)),ch=ch,s=s,e=e))

def mix(pecas, saida):
    ins, fil = [], []
    for i,p in enumerate(pecas):
        ins += ["-i", str(T/f"{p['b']}.mp3")]
        fil.append(f"[{i}]aresample={SR},aformat=channel_layouts=mono,atrim={p['c0']:.3f}:{p['c1']:.3f},asetpts=N/SR/TB,volume={ganho[p['b']]:.2f}dB,"
                   f"afade=t=in:d=0.02,afade=t=out:st={p['c1']-p['c0']-0.05:.3f}:d=0.05,adelay={int(round((p['pos']-0.06)*1000))}[a{i}]")
    n = len(pecas)
    fil.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{DUR}[base]")
    fil.append("[base]" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n+1}:normalize=0:duration=first,alimiter=limit=0.95[o]")
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fil),"-map","[o]","-ar",str(SR),"-c:a","pcm_s16le",str(saida)],check=True)

mix(info, AD/"narracao_es.wav")
for q in sorted({p["q"] for p in info}):
    mix([p for p in info if p["q"]==q], AD/f"narr_{q.lower()}.wav")
# fundo (demucs no_vocals) no tempo novo, com o mesmo corte (crossfade curto)
nv = A/"demucs/htdemucs/orig/no_vocals.wav"
subprocess.run(["ffmpeg","-v","error","-y","-i",str(nv),"-i",str(nv),"-filter_complex",
    f"[0]atrim=0:{CUT_A+0.05:.4f},asetpts=N/SR/TB[x];[1]atrim={CUT_B-0.05:.4f},asetpts=N/SR/TB[y];[x][y]acrossfade=d=0.1,aresample={SR},atrim=0:{DUR:.4f}[o]",
    "-map","[o]","-c:a","pcm_s16le",str(AD/"fundo_es.wav")],check=True)
# alinhamento
C,S,E = [],[],[]; tempos=[]
for p in info:
    idx=p["idx"]; off=p["pos"]-p["s"][idx[0]]
    if C: C.append(" "); S.append(E[-1]); E.append(E[-1])
    for i in idx: C.append(p["ch"][i]); S.append(round(p["s"][i]+off,3)); E.append(round(p["e"][i]+off,3))
    tempos.append({"quem":p["q"],"texto":"".join(p["ch"][i] for i in idx),"ini":round(p["s"][idx[0]]+off,2),"fim":round(p["e"][idx[-1]]+off,2)})
(AD/"narracao_es.alinhamento.json").write_text(json.dumps({"characters":C,"character_start_times_seconds":S,"character_end_times_seconds":E},ensure_ascii=False),encoding="utf-8")
json.dump(tempos, open(A/"tempos_reais.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
prev=0
for t in tempos:
    print(f"{t['quem']:10} {t['ini']:6.2f}-{t['fim']:6.2f} {'SOBREPOE ' if t['ini']<prev else ''}{t['texto'][:70]}"); prev=t["fim"]
