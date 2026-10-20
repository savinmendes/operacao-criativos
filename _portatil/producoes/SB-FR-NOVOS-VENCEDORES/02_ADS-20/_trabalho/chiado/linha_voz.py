# Reproduz a linha do tempo de voz_fr.py (mesmos cortes/pausas) a partir de fontes dadas, sem gravar tempos.json
import sys, json, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import load, palavras, SR
W = r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\02_ADS-20\_trabalho"
C0 = 4.38; PAUSA = 0.20; TAIL = 0.4
def linha(h1, h2, c):
    """h1,h2,c: arrays (n,2) 48k das fontes (originais ou limpas, mesmo comprimento das originais)"""
    pw = palavras(W + r"\audio\corpo_fr.alinhamento.json")
    L = [l for l in open(W + r"\audio\corpo_fr.txt", encoding="utf-8") if l.strip()]
    idx = []; n = 0
    for l in L: n += len(l.split()); idx.append(n - 1)
    ins = [((pw[q][2] + pw[q + 1][1]) / 2, PAUSA) for q in idx[:-1]]
    out = []; prev = 0
    for t, d in ins:
        k = int(t * SR); out += [c[prev:k], np.zeros((int(d * SR), 2), np.float32)]; prev = k
    fim = pw[-1][2] + 0.2; out += [c[prev:int(fim * SR)]]
    corpo = np.concatenate(out)
    TOTAL = round(C0 + len(corpo) / SR + TAIL, 2)
    v = np.zeros((int(TOTAL * SR) + 10, 2), np.float32)
    def put(x, t): i = int(t * SR); v[i:i + len(x)] += x
    put(h1, 0.08); put(h2, 2.45); put(corpo, C0)
    T0 = json.load(open(W + r"\tempos.json"))
    assert TOTAL == T0["TOTAL"] and all(abs(a[0] - b[0]) < 1e-6 for a, b in zip(ins, T0["pausas"])), "linha do tempo diferente do original"
    return v, TOTAL
def fontes():
    return load(W + r"\audio\hook1_fr.mp3"), load(W + r"\audio\hook2_fr.mp3"), load(W + r"\audio\corpo_fr.mp3")
