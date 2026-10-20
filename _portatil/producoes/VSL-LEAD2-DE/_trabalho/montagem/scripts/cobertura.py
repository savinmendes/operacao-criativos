# -*- coding: utf-8 -*-
"""Plano de b-roll para os trechos usar_broll (timeline nova, antes do corte T0). Saida: cobertura.json"""
import sys, json, re
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import T, M
L = {t["id"]: t for t in json.load(open(T / "voz" / "lotes.json", encoding="utf-8"))["trechos"]}
PW = json.load(open(T / "voz" / "alinhamento_de.json", encoding="utf-8"))["palavras"]
MIN = 1.0
def pausas_alinh(a, b, minimo=0.25):
    ws = [w for w in PW if w["fim"] > a and w["ini"] < b]; r = []
    for x, y in zip(ws, ws[1:]):
        if y["ini"] - x["fim"] >= minimo: r.append([x["fim"], y["ini"]])
    return r
cov = []  # (ini, fim, id, motivo)
dados = {"L058": [[569.57, 570.1], [572.4, 573.6], [575.13, 575.73]],
         "L059": [[579.2, 579.8], [581.5, 582.7], [584.57, 584.93], [586.2, 586.67]],
         "L060": [[590.47, 590.83], [591.97, 592.9]]}
for i in ["L098", "L160", "L261", "L263", "L274"]:
    dados[i] = pausas_alinh(L[i]["novo_ini"], L[i]["novo_fim"]) or pausas_alinh(L[i]["novo_ini"], L[i]["novo_fim"], 0.15)
for i, ps in dados.items():
    t = L[i]; a0, b0 = t["novo_ini"], t["novo_fim"]
    iv = []
    for s, e in ps:
        if e - s < MIN:
            c = (s + e) / 2; s, e = c - MIN / 2, c + MIN / 2
        s, e = max(a0, s), min(b0, e)
        if b0 - e < 0.5: e = b0          # nao deixa sobra minuscula de lipsync
        if s - a0 < 0.5: s = a0
        if iv and s - iv[-1][1] < 2.5: iv[-1][1] = e
        else: iv.append([s, e])
    for s, e in iv: cov.append([round(s, 3), round(e, 3), i, "pausas"])
for i in ["L070", "L077", "L079", "L091", "L103", "L110", "L178"] + [k for k in ["L098", "L160", "L261", "L263", "L274"] if not dados[k]]:
    cov.append([L[i]["novo_ini"], L[i]["novo_fim"], i, "trecho inteiro (sem pausa medivel)"])
cov.append([round(L["L244"]["novo_ini"] + 5.27, 3), round(L["L244"]["novo_ini"] + 7.3, 3), "L244", "apos 5,27 s (mao no rosto) ate o crucifixo"])
cov.sort()
# junta coberturas encostadas (trechos vizinhos)
mg = []
for c in cov:
    if mg and c[0] - mg[-1][1] < 0.8: mg[-1][1] = max(mg[-1][1], c[1]); mg[-1][2] += "+" + c[2]
    else: mg.append(list(c))
POOL = [  # (orig_ini, orig_fim, nome, novo_onde_aparece)
    [206.2, 222.5, "igreja geral (nave)", None], [278.4, 283.0, "pulpito vazio A", None],
    [452.6, 456.2, "altar ao longe", 347.5], [457.2, 462.2, "pulpito vazio B", 352.5],
    [582.4, 585.0, "estatua A", 477.0], [2146.4, 2149.4, "estatua B", 2126.6], [2149.6, 2153.8, "igreja + altar", 2130.0]]
GR = [0, 1, 2, 1, 3, 3, 4]  # grupos visuais: nave, pulpito(A,B), altar, estatua(A,B), igreja+altar
cursor = [p[0] for p in POOL]; ultimo = [-1e9] * 5
plano = []
for s_, e, ids, mot in mg:
    t = s_; usado_aqui = set()
    if any(L[x]['cena'] == 'padre_pulpito' for x in ids.split('+')): usado_aqui.add(1)
    while e - t > 0.05:
        rest = e - t
        cand = []
        for j, p in enumerate(POOL):
            if GR[j] in usado_aqui or (p[3] is not None and abs(p[3] - t) < 150): continue
            cand.append((ultimo[GR[j]], j))
        cand.sort()
        longe = [c for c in cand if t - c[0] >= 90] or [c for c in cand if t - c[0] >= 45]
        j = (longe or cand)[0][1]; p = POOL[j]
        d = min(rest, 4.5, p[1] - p[0] - 0.05)
        if 0 < rest - d < 1.2: d = rest if rest <= min(5.0, p[1] - p[0] - 0.05) else rest - 1.2
        if cursor[j] + d > p[1]: cursor[j] = p[0]
        plano.append({"novo_ini": round(t, 3), "novo_fim": round(t + d, 3), "src_ini": round(cursor[j], 3), "broll": p[2], "trechos": ids, "motivo": mot, "zoom": t >= 2136.4})
        cursor[j] += d + 0.3; ultimo[GR[j]] = t + d; usado_aqui.add(GR[j]); t += d
json.dump(plano, open(M / "cobertura.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for x in plano: print(x["novo_ini"], x["novo_fim"], x["src_ini"], x["broll"], x["trechos"])
print(len(plano), "pecas", round(sum(x["novo_fim"] - x["novo_ini"] for x in plano), 1), "s")
for i in ["L098", "L160", "L261", "L263", "L274"]: print(i, dados[i])
