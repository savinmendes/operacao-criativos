import json, sys, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import lufs, true_peak_db, finalizar_mix, SR
TL = json.load(open("timeline_de.json", encoding="utf-8"))
N = int(np.ceil(TL["duracao_final_s"] * SR)) + SR
out = np.zeros(N, np.float32)
aud = {b["id"]: sf.read(b["audio"], dtype="float32")[0] for b in TL["blocos"]}
ganho = {}
for f in sorted(set(b["falante"] for b in TL["blocos"])):
    x = np.concatenate([aud[b["id"]] for b in TL["blocos"] if b["falante"] == f])
    ganho[f] = 10 ** ((-16.5 - lufs(x)) / 20)
for b in TL["blocos"]:
    x = aud[b["id"]] * ganho[b["falante"]]
    a = max(0, int((b["audio_fala_ini"] - 0.06) * SR)); e = min(len(x), int((b["audio_fala_fim"] + 0.15) * SR))
    seg = x[a:e].copy(); r = int(0.01 * SR); seg[:r] *= np.linspace(0, 1, r); seg[-r:] *= np.linspace(1, 0, r)
    p = int(round((b["novo_ini"] - (b["audio_fala_ini"] - a / SR)) * SR))
    out[p:p + len(seg)] += seg
out = out[:int(round(TL["duracao_final_s"] * SR))]
out = finalizar_mix(out, alvo=-16.5, tp=-1.5)

sf.write("narracao_de_completa.wav", out, SR, subtype="PCM_24")
print("dur %.2f s" % (len(out) / SR), "LUFS %.1f" % lufs(out), "TP %.1f" % true_peak_db(out), {k: round(20 * np.log10(v), 1) for k, v in ganho.items()})
