"""narracao_es.wav do 03 (1 personagem: padre) + alinhamento. Cada bloco: atempo F em [1,0;1,1] (o menor que cabe antes do
proximo bloco PT), entrando em max(inicio PT, fim anterior + GAP)."""
import json, re, subprocess
from pathlib import Path
A=Path(__file__).resolve().parent; AD=A.parent; T=A/"tts"
DUR=96.433; SR=44100; GAP=0.28
B=json.load(open(A/"blocos.json",encoding="utf-8-sig"))
def lufs(f):
    o=subprocess.run(["ffmpeg","-i",str(f),"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS",o)[-1])
C,S,E,tempos,pecas=[],[],[],[],[]; fim_ant=-9
for k,b in enumerate(B):
    al=json.load(open(T/f"{b['id']}.alinhamento.json",encoding="utf-8"))
    ch,s,e=al["characters"],al["character_start_times_seconds"],al["character_end_times_seconds"]
    idx=[i for i in range(len(ch)) if not ch[i].isspace()]; i0,i1=idx[0],idx[-1]
    pos=max(b["ini"],fim_ant+GAP)
    lim=B[k+1]["ini"]-0.15 if k+1<len(B) else 95.6
    dur=e[i1]-s[i0]; F=min(1.1,max(1.0,dur/max(0.1,lim-pos)))
    off=pos-s[i0]/F; pecas.append((b["id"],off,F))
    if C: C.append(" "); S.append(E[-1]); E.append(E[-1])
    for i in range(i0,i1+1): C.append(ch[i]); S.append(round(s[i]/F+off,3)); E.append(round(e[i]/F+off,3))
    fim_ant=e[i1]/F+off
    tempos.append({"id":b["id"],"quem":"PADRE","texto":b["texto"],"ini":round(pos,2),"fim":round(fim_ant,2),"F":round(F,3)})
    print(b["id"],round(pos,2),round(fim_ant,2),"F",round(F,3),"(PT",b["ini"],"-",b["fim"],")")
ins,fil=[],[]
for k,(bid,off,F) in enumerate(pecas):
    g=-16.0-lufs(T/f"{bid}.mp3"); ins+=["-i",str(T/f"{bid}.mp3")]
    fil.append(f"[{k}]aresample={SR},aformat=channel_layouts=mono,atempo={F:.4f},volume={g:.2f}dB,afade=t=in:d=0.02,adelay={int(round(max(0,off)*1000))}[a{k}]")
n=len(pecas); fil.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{DUR}[base]")
fil.append("[base]"+"".join(f"[a{k}]" for k in range(n))+f"amix=inputs={n+1}:normalize=0:duration=first,alimiter=limit=0.95[o]")
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fil),"-map","[o]","-ar",str(SR),"-c:a","pcm_s16le",str(AD/"narracao_es.wav")],check=True)
(AD/"narracao_es.alinhamento.json").write_text(json.dumps({"characters":C,"character_start_times_seconds":S,"character_end_times_seconds":E},ensure_ascii=False),encoding="utf-8")
json.dump(tempos,open(A/"tempos_reais.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)

