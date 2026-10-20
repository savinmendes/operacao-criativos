import json, subprocess, numpy as np
S = json.load(open("segs_es_t.json", encoding="utf-8"))
SR = 48000; TOT = 139.167
def ler(p):
    r = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(r, np.float32)
src = {"m": "voz/moca_es.wav", "p": "voz/padre_es.wav"}
out = np.zeros(int(SR * TOT), np.float32); prev = 0; pal = []; plano = []
for k, s in enumerate(S):
    d = s["es_fim"] - s["es_ini"]; nxt = S[k+1]["a"] if k+1 < len(S) else 139.1
    sp = min(1.1, max(1.0, d / (nxt - s["a"] - 0.2)))
    t = max(s["a"] - 0.4, prev + 0.22) if k else 0.15
    a0 = max(0, s["es_ini"] - 0.06); a1 = s["es_fim"] + 0.10
    tmp = f"voz/_seg{s['i']:02d}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src[s["quem"]],"-af",f"atrim={a0:.3f}:{a1:.3f},asetpts=PTS-STARTPTS,atempo={sp:.4f}",
                    "-ac","1","-ar",str(SR),tmp],check=True)
    x = ler(tmp); n0 = int((t - (s["es_ini"] - a0) / sp) * SR)
    out[n0:n0 + len(x)] += x[:len(out) - n0]
    for w, a, b in s["pal"]:
        pal.append([w, round(t + (a - s["es_ini"]) / sp, 3), round(t + (b - s["es_ini"]) / sp, 3), s["quem"], s["i"]])
    prev = t + d / sp
    plano.append(dict(i=s["i"], quem=s["quem"], ini=round(t, 3), fim=round(prev, 3), sp=round(sp, 3), texto=s["texto"]))
    print(s["i"], round(t, 2), round(prev, 2), round(sp, 3))
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
subprocess.run(["ffmpeg","-v","error","-y","-f","s16le","-ar",str(SR),"-ac","1","-i","-","narr_es_raw.wav"],input=pcm.tobytes(),check=True)
json.dump(pal, open("palavras_final.json","w",encoding="utf-8"), ensure_ascii=False)
json.dump(plano, open("plano_fala.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
