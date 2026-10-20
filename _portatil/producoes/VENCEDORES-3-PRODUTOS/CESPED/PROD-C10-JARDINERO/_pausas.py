"""Encurta pausas > MAXP para MAXP nas narrações TTS e remapeia o alinhamento. Gera audio/<n>_c.mp3 + .alinhamento_c.json"""
import json, re, subprocess
MAXP = 0.28
TEMPO = 1.05
for n in ["L3_probe", "L4_mecanismo", "L5_virada", "L6_cta"]:
    f = f"audio/{n}.mp3"
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
    log = subprocess.run(["ffmpeg","-i",f,"-af","silencedetect=n=-38dB:d=0.3","-f","null","-"],capture_output=True,text=True).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]; se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    cortes = []  # (ini, fim) a remover
    for a, b in zip(ss, se):
        if b >= dur - 0.05: continue  # silêncio final: mantém
        m = (a + b) / 2; meio = MAXP / 2
        cortes.append((m - (b - a) / 2 + meio, m + (b - a) / 2 - meio))
    keep, t = [], 0.0
    for a, b in cortes: keep.append((t, a)); t = b
    keep.append((t, dur))
    def mapa(x):
        acc = 0.0
        for a, b in keep:
            if x <= b: return acc + max(0.0, x - a)
            acc += b - a
        return acc
    sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f,"-af",f"aselect='{sel}',asetpts=N/SR/TB,atempo={TEMPO}","-ar","44100","-b:a","192k",f"audio/{n}_c.mp3"],check=True)
    d = json.load(open(f"audio/{n}.alinhamento.json", encoding="utf-8"))
    d["character_start_times_seconds"] = [round(mapa(x)/TEMPO,3) for x in d["character_start_times_seconds"]]
    d["character_end_times_seconds"] = [round(mapa(x)/TEMPO,3) for x in d["character_end_times_seconds"]]
    json.dump(d, open(f"audio/{n}.alinhamento_c.json","w",encoding="utf-8"), ensure_ascii=False)
    nd = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"audio/{n}_c.mp3"],capture_output=True,text=True).stdout)
    print(n, round(dur,2), "->", round(nd,2), "fala termina", d["character_end_times_seconds"][-1], [(round(a,2),round(b,2)) for a,b in cortes])
