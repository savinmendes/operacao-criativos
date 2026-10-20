# limpeza de chiado (receita SB-FR) por bloco, com perfil de ruido unico por falante
import json, os, sys, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import load, palavras, perfil_ruido, portao_espectral, mascara_fala, portao_tempo, filtro, EQ_VOZ, metricas, SR
import gerar
FAL = gerar.FAL
os.makedirs("voz_limpa", exist_ok=True)
por = {}
for b in gerar.BL: por.setdefault(FAL[b["id"]]["falante"], []).append(b["id"])
rel = {}
for f, ids in por.items():
    xs = {i: load(f"tts/{i}.mp3", ch=1) for i in ids}
    amostra = np.concatenate([xs[i] for i in ids][:60])
    N, nq = perfil_ruido(amostra, q=35)
    for i in ids:
        x = xs[i]; pw = palavras(f"tts/{i}.alinhamento.json")
        y = portao_espectral(x, N, k=2.0, piso_db=-18, fmin=5000)
        mk, thr = mascara_fala(y, pw, pre=0.05, pos=0.08, rel_db=35, abs_db=-50, dil=0.02)
        z = portao_tempo(y, mk, fade=0.015, atn_db=-60)
        z = filtro(z, EQ_VOZ)
        sf.write(f"voz_limpa/{i}.wav", z, SR, subtype="FLOAT")
    a = np.concatenate([xs[i] for i in ids]); bz = np.concatenate([load(f"voz_limpa/{i}.wav", ch=1) for i in ids])
    rel[f] = {"blocos": len(ids), "antes": metricas(a), "depois": metricas(bz)}
    print(f, rel[f], flush=True)
json.dump(rel, open("chiado_medicao.json", "w", encoding="utf-8"), indent=1)
