# Encurta as pausas internas da voz do hook (Lily 1.1) para caber em <=7,6 s; regrava alinhamento deslocado.
import json, re, subprocess, numpy as np, soundfile as sf
SR = 44100; MANTER = 0.17
src = "hookpf7_lily.mp3"
a = subprocess.run(["ffmpeg","-v","error","-i",src,"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True).stdout
x = np.frombuffer(a, np.float32).reshape(-1, 2).copy()
log = subprocess.run(["ffmpeg","-hide_banner","-i",src,"-af","silencedetect=n=-40dB:d=0.08","-f","null","-"],capture_output=True,text=True).stderr
ini = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", log)]; fim = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", log)]
dur = len(x) / SR
cortes = []  # (t_ini_corte, t_fim_corte)
for s, e in zip(ini, fim):
    if s < 0.05 or e > dur - 0.05: continue
    if e - s > MANTER:
        m = (s + e) / 2; cortes.append((m - (e - s - MANTER) / 2, m + (e - s - MANTER) / 2))
partes = []; p = 0.0
for c0, c1 in cortes:
    partes.append(x[int(p*SR):int(c0*SR)]); p = c1
partes.append(x[int(p*SR):])
# micro crossfade de 10 ms em cada emenda
y = partes[0]
for q in partes[1:]:
    k = int(0.01*SR); y = np.concatenate([y[:-k], y[-k:]*np.linspace(1,0,k)[:,None] + q[:k]*np.linspace(0,1,k)[:,None], q[k:]])
sf.write("hookpf7_lily_curta.wav", y, SR, subtype="PCM_24")
def novo(t):
    d = 0.0
    for c0, c1 in cortes:
        if t >= c1: d += c1 - c0
        elif t > c0: d += t - c0
    return t - d
al = json.load(open("hookpf7_lily.alinhamento.json", encoding="utf-8"))
al["character_start_times_seconds"] = [novo(t) for t in al["character_start_times_seconds"]]
al["character_end_times_seconds"] = [novo(t) for t in al["character_end_times_seconds"]]
json.dump(al, open("hookpf7_lily_curta.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("cortes", [(round(a,2), round(b,2)) for a, b in cortes], "dur", round(len(y)/SR, 3), "fala ate", round(al["character_end_times_seconds"][-1], 3))
