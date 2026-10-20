"""Narracao do 02: gancho (voz nova "ORACAO-02 mulher shopping", h0.mp3 em 3 pedacos encaixados nas frases do PT)
+ narracao do AD 01 (mesmo texto/imagem) a partir de 8,40 s do 01, deslocada +44 quadros (1,4667 s)."""
import json, re, subprocess
from pathlib import Path
A=Path(__file__).resolve().parent; AD=A.parent
DUR=132.2; SR=44100; OFF=44/30; CUT01=8.40
# pedacos do h0: (ini_h0, fim_h0, onde_entra_no_02)
P=[(0.0,2.53,0.05),(2.53,6.61,2.456),(6.61,8.40,7.531)]
def lufs(f):
    o=subprocess.run(["ffmpeg","-i",str(f),"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS",o)[-1])
g=-16.0-lufs(A/"tts/h0.mp3")
fil=[]; ins=["-i",str(A/"tts/h0.mp3"),"-i",str(A/"ad01_snap/narracao_es.wav")]
for k,(a,b,p) in enumerate(P):
    fil.append(f"[0:a]aresample={SR},aformat=channel_layouts=mono,atrim={a}:{b},asetpts=PTS-STARTPTS,volume={g:.2f}dB,afade=t=in:d=0.01,afade=t=out:st={b-a-0.02}:d=0.02,adelay={int(round(p*1000))}[h{k}]")
fil.append(f"[1:a]aresample={SR},aformat=channel_layouts=mono,atrim={CUT01},asetpts=PTS-STARTPTS,adelay={int(round((CUT01+OFF)*1000))}[c]")
fil.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{DUR}[base]")
fil.append("[base][h0][h1][h2][c]amix=inputs=5:normalize=0:duration=first,alimiter=limit=0.95[o]")
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fil),"-map","[o]","-ar",str(SR),"-c:a","pcm_s16le",str(AD/"narracao_es.wav")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"narracao_es.wav"),"-af","atrim=0:9.5333","-c:a","pcm_s16le",str(AD/"narr_gancho.wav")],check=True)
# alinhamento
h=json.load(open(A/"tts/h0.alinhamento.json",encoding="utf-8")); C,S,E=[],[],[]
for (a,b,p) in P:
    for c,s,e in zip(h["characters"],h["character_start_times_seconds"],h["character_end_times_seconds"]):
        if a<=s<b:
            C.append(c); S.append(round(s-a+p,3)); E.append(round(min(e,b)-a+p,3))
w=json.load(open(A/"ad01_snap/narracao_es.alinhamento.json",encoding="utf-8"))
first=True
for c,s,e in zip(w["characters"],w["character_start_times_seconds"],w["character_end_times_seconds"]):
    if s>=CUT01:
        if first and c.isspace(): continue
        if first: C.append(" "); S.append(E[-1]); E.append(E[-1]); first=False
        C.append(c); S.append(round(s+OFF,3)); E.append(round(e+OFF,3))
(AD/"narracao_es.alinhamento.json").write_text(json.dumps({"characters":C,"character_start_times_seconds":S,"character_end_times_seconds":E},ensure_ascii=False),encoding="utf-8")
t=json.load(open(A/"ad01_snap/tempos_reais.json",encoding="utf-8"))
out=[{"id":"h0","quem":"MULHER SHOPPING","texto":"".join(h["characters"]).strip(),"ini":0.09,"fim":round(S[len([1 for _ in C])-1] if False else 9.07,2)}]
for b in t[1:]: out.append({**b,"quem":"DESATADORA","ini":round(b["ini"]+OFF,2),"fim":round(b["fim"]+OFF,2)})
json.dump(out,open(A/"tempos_reais.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok", "".join(C)[:200]); print("fim fala", out[-1]["fim"])
