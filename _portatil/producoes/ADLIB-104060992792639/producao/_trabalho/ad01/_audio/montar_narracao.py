# Monta narracao_es.wav (= narr_mulher.wav, 1 personagem) e o alinhamento no tempo do vídeo 01.
# Cada bloco recebe atempo F (<=1,1) e entra em max(início original, fim anterior + GAP).
import json, re, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parent; AD = A.parent; T = A / "tts"
DUR = 131.233; SR = 44100; GAP = 0.32; LIMITE = 115.0
F = float(sys.argv[1]) if len(sys.argv) > 1 else 1.08
B = json.load(open(A / "blocos.json", encoding="utf-8"))

def lufs(f):
    o = subprocess.run(["ffmpeg","-i",str(f),"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])

pecas, C, S, E, tempos = [], [], [], [], []
fim_ant = -9
for b in B:
    al = json.load(open(T / f"{b['id']}.alinhamento.json", encoding="utf-8"))
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    idx = [i for i in range(len(ch)) if not ch[i].isspace()]
    i0, i1 = idx[0], idx[-1]
    c0 = max(0, s[i0] - 0.03)
    pos = max(b["ini"], fim_ant + GAP)          # onde a 1ª letra entra
    off = pos - s[i0] / F
    pecas.append((b["id"], off))
    if C:
        C.append(" "); S.append(E[-1]); E.append(E[-1])
    for i in range(i0, i1 + 1):
        C.append(ch[i]); S.append(round(s[i] / F + off, 3)); E.append(round(e[i] / F + off, 3))
    fim_ant = e[i1] / F + off
    tempos.append({"id": b["id"], "quem": "MULHER", "texto": b["texto"], "ini": round(pos, 2), "fim": round(fim_ant, 2)})
    print(b["id"], round(pos, 2), round(fim_ant, 2), "(orig", b["ini"], "-", b["fim"], ")")
print("fim da fala", round(fim_ant, 2), "limite", LIMITE, "OK" if fim_ant <= LIMITE else "ESTOURA")

ins, fil = [], []
for k, (bid, off) in enumerate(pecas):
    g = -16.0 - lufs(T / f"{bid}.mp3")
    ins += ["-i", str(T / f"{bid}.mp3")]
    fil.append(f"[{k}]aresample={SR},aformat=channel_layouts=mono,atempo={F},volume={g:.2f}dB,afade=t=in:d=0.02,"
               f"adelay={int(round(max(0, off) * 1000))}[a{k}]")
n = len(pecas)
fil.append(f"anullsrc=r={SR}:cl=mono,atrim=0:{DUR}[base]")
fil.append("[base]" + "".join(f"[a{k}]" for k in range(n)) + f"amix=inputs={n+1}:normalize=0:duration=first,alimiter=limit=0.95[o]")
for nome in ["narracao_es.wav", "narr_mulher.wav"]:
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fil),"-map","[o]","-ar",str(SR),"-c:a","pcm_s16le",str(AD / nome)],check=True)
(AD / "narracao_es.alinhamento.json").write_text(json.dumps({"characters":C,"character_start_times_seconds":S,"character_end_times_seconds":E},ensure_ascii=False),encoding="utf-8")
json.dump(tempos, open(A / "tempos_reais.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
