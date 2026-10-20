# Monta a timeline DE: secoes de video com fator de tempo, posicao de cada bloco DE, trechos de lipsync e lotes.
import json, sys, difflib, re
import numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import palavras
import gerar

R = r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho"
FMIN, FMAX = 0.90, 1.12
CMIN_PREF, CMAX_PREF = 0.70, 1.40
CORTE = (276.4, 403.8)
FIM_VIDEO = 2563.30
LIP_MAX = 12.0

BL = gerar.BL; FAL = gerar.FAL
# ---------- fala DE por bloco ----------
for b in BL:
    pw = palavras(f"tts/{b['id']}.alinhamento.json")
    b["pw"] = pw; b["s0"] = pw[0][1]; b["e0"] = pw[-1][2]; b["D"] = b["e0"] - b["s0"]
    b["falante"] = FAL[b["id"]]["falante"]

# ---------- cenas corrigidas ----------
cen = json.load(open(R + r"\base\cenas.json", encoding="utf-8"))["cenas"]
ROSTO = {"abertura_figura_branca": "apresentador", "padre_altar": "padre", "padre_pulpito": "padre", "padre_medio": "padre",
         "padre_close": "padre", "dep1": "depoente1", "dep2": "depoente2", "dep3": "depoente3"}
cenas = []
for c in cen:
    a, b, t = c["ini"], c["fim"], c["tipo"]
    if b <= 580.3 or a >= 706.0: pass
    elif a < 580.3: b = 580.3
    elif b > 706.0: a = 706.0
    else: continue
    cenas.append({"ini": a, "fim": b, "tipo": t})
cenas += [{"ini": 580.3, "fim": 585.2, "tipo": "broll_crucifixo_estatua"}, {"ini": 585.2, "fim": 618.2, "tipo": "dep1"},
          {"ini": 618.2, "fim": 659.1, "tipo": "dep2"}, {"ini": 659.1, "fim": 706.0, "tipo": "dep3"}]
cenas.sort(key=lambda c: c["ini"])
# conserta continuidade
for x, y in zip(cenas, cenas[1:]):
    if abs(x["fim"] - y["ini"]) > 0.01: x["fim"] = y["ini"]
for c in cenas: c["rosto"] = ROSTO.get(c["tipo"])

# ---------- secoes ----------
MACRO = [(0.0, 205.73), (205.73, 223.4), (223.4, CORTE[0]), (CORTE[1], 580.3), (580.3, 584.9), (584.9, 618.2), (618.2, 659.1),
         (659.1, 706.0), (706.0, FIM_VIDEO)]
def blocos_em(a, b): return [x for x in BL if x["ini_es"] >= a - 1e-6 and x["fim_es"] <= b + 1e-6]
assert sum(len(blocos_em(a, b)) for a, b in MACRO) == len(BL), "bloco fora das secoes"
bordas = [c["ini"] for c in cenas]
def sub_ancoras(a, b):
    bs = blocos_em(a, b); anc = [a]
    for x, y in zip(bs, bs[1:]):
        g0, g1 = x["fim_es"], y["ini_es"]
        cut = [t for t in bordas if g0 + 0.05 <= t <= g1 - 0.05]
        if cut: anc.append(cut[0])
        elif g1 - g0 >= 2.0: anc.append((g0 + g1) / 2)
    anc.append(b); return anc

def resolver(a, b):
    """fator F e escala de pausa c para a secao [a,b]"""
    bs = blocos_em(a, b); L = b - a
    if not bs: return dict(F=1.0, c=1.0, ok=True, pausas=[], bs=bs)
    p = [bs[0]["ini_es"] - a] + [y["ini_es"] - x["fim_es"] for x, y in zip(bs, bs[1:])] + [b - bs[-1]["fim_es"]]
    pmin = [min(p[0], 0.05)] + [min(q, 0.15) for q in p[1:-1]] + [min(p[-1], 0.05)]
    D = sum(x["D"] for x in bs)
    soma = lambda c: sum(max(m, c * q) for m, q in zip(pmin, p))
    def c_para(P):  # inverte soma(c)=P
        lo, hi = 0.0, 50.0
        if soma(0) > P: return None
        for _ in range(60):
            mid = (lo + hi) / 2
            (lo, hi) = (mid, hi) if soma(mid) < P else (lo, mid)
        return (lo + hi) / 2
    F = 1.0; c = c_para(F * L - D); ok = True
    if c is None or c < CMIN_PREF:
        F = min(FMAX, (D + soma(CMIN_PREF)) / L); c = c_para(F * L - D)
        if c is None:
            ok = False; F = (D + soma(0)) / L; c = 0.0
    elif c > CMAX_PREF:
        F = max(FMIN, (D + soma(CMAX_PREF)) / L); c = c_para(F * L - D)
    pz = [max(m, c * q) for m, q in zip(pmin, p)]
    return dict(F=F, c=c, ok=ok, pausas=pz, bs=bs)

secoes = []
for A, B in MACRO:
    anc = sub_ancoras(A, B) if (B - A) > 60 else [A, B]
    seg = [[x, y] for x, y in zip(anc, anc[1:])]
    # funde secoes inviaveis ou muito curtas com a vizinha
    mudou = True
    while mudou and len(seg) > 1:
        mudou = False
        for i, (x, y) in enumerate(seg):
            r = resolver(x, y)
            if not r["ok"] or (r["F"] in (FMIN, FMAX) and False) or (y - x) < 6.0:
                j = i + 1 if i + 1 < len(seg) else i - 1
                lo, hi = min(i, j), max(i, j)
                seg[lo:hi + 1] = [[seg[lo][0], seg[hi][1]]]; mudou = True; break
    for x, y in seg: secoes.append([x, y])

# ---------- layout ----------
t_novo = 0.0; SEC = []; COLOC = {}
for x, y in secoes:
    r = resolver(x, y); L = y - x; Ln = r["F"] * L
    s = {"src_ini": round(x, 3), "src_fim": round(y, 3), "novo_ini": round(t_novo, 3), "novo_fim": round(t_novo + Ln, 3),
         "fator": round(r["F"], 4), "escala_pausas": round(r["c"], 3), "blocos": [b["id"] for b in r["bs"]],
         "dentro_limite": bool(r["ok"] and FMIN - 1e-6 <= r["F"] <= FMAX + 1e-6)}
    t = t_novo
    for k, b in enumerate(r["bs"]):
        t += r["pausas"][k]
        COLOC[b["id"]] = t; t += b["D"]
    assert abs(t + (r["pausas"][-1] if r["bs"] else 0) - (t_novo + Ln if r["bs"] else t)) < 0.02 or not r["bs"], (x, y)
    SEC.append(s); t_novo += Ln
DUR = t_novo

def mapa(t):
    """tempo original -> timeline nova (None se cortado)"""
    if CORTE[0] < t < CORTE[1]: return None
    for s in SEC:
        if s["src_ini"] - 0.002 <= t <= s["src_fim"] + 0.002:
            return s["novo_ini"] + s["fator"] * (t - s["src_ini"])
    return None
def inv(tn):
    for s in SEC:
        if s["novo_ini"] - 0.02 <= tn <= s["novo_fim"] + 0.02:
            return s["src_ini"] + (tn - s["novo_ini"]) / s["fator"], s["fator"]
    return None, None

# ---------- palavras na timeline nova (texto de exibicao) ----------
def tok(t): return t.split()
PAL = []
for b in BL:
    off = COLOC[b["id"]] - b["s0"]
    tts_w = [[w[0], w[1] + off, w[2] + off] for w in b["pw"]]
    disp = tok(b["de"])
    sm = difflib.SequenceMatcher(None, [w[0] for w in tts_w], disp, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                PAL.append({"bloco": b["id"], "falante": b["falante"], "palavra": disp[j1 + k], "ini": round(tts_w[i1 + k][1], 3), "fim": round(tts_w[i1 + k][2], 3)})
        elif j2 > j1:
            if i2 > i1: a0, a1 = tts_w[i1][1], tts_w[i2 - 1][2]
            else:  # insercao sem audio (raro): cola no vizinho
                ref = tts_w[min(i1, len(tts_w) - 1)]; a0, a1 = ref[1], ref[1]
            n = j2 - j1
            for k in range(n):
                PAL.append({"bloco": b["id"], "falante": b["falante"], "palavra": disp[j1 + k],
                            "ini": round(a0 + (a1 - a0) * k / n, 3), "fim": round(a0 + (a1 - a0) * (k + 1) / n, 3)})
PAL.sort(key=lambda w: w["ini"])

# ---------- lipsync ----------
fala_orig = [(b["ini_es"], b["fim_es"]) for b in BL]
trechos = []
for c in cenas:
    if not c["rosto"]: continue
    a, b = c["ini"], c["fim"]
    if a < CORTE[1] and b > CORTE[0]:
        if a < CORTE[0]: b = CORTE[0]
        else: a = max(a, CORTE[1])
    if b - a < 0.2: continue
    na, nb = mapa(a), mapa(b)
    if na is None or nb is None: continue
    ws = [w for w in PAL if w["fim"] > na and w["ini"] < nb]
    org = any(x < b and y > a for x, y in fala_orig)
    if not ws and not org: continue
    cur = na
    cortes = []
    while nb - cur > LIP_MAX:
        cand = []
        for w1, w2 in zip(ws, ws[1:]):
            g = w2["ini"] - w1["fim"]; m = (w1["fim"] + w2["ini"]) / 2
            if cur + 3.0 < m <= cur + LIP_MAX: cand.append((g, m))
        boas = [x for x in cand if x[0] >= 0.12]
        if boas: m = max(boas, key=lambda x: (round(x[0], 1), x[1]))[1]
        elif cand: m = max(cand, key=lambda x: (x[0] > 0.02, x[1]))[1]
        else: m = cur + LIP_MAX
        cortes.append(m); cur = m
    pts = [na] + cortes + [nb]
    for x, y in zip(pts, pts[1:]):
        wz = [w for w in PAL if w["ini"] >= x - 0.02 and w["fim"] <= y + 0.02]
        oi, f1 = inv(x + 1e-4); of, f2 = inv(y - 1e-4)
        if oi is None or of is None: print("inv falhou", c, x, y, DUR); continue
        trechos.append({"falante": c["rosto"], "cena": c["tipo"], "novo_ini": round(x, 3), "novo_fim": round(y, 3), "dur": round(y - x, 3),
                        "orig_ini": round(oi, 3), "orig_fim": round(of, 3), "fator": f1 if f1 == f2 else [f1, f2],
                        "fala_de": bool(wz), "texto": " ".join(w["palavra"] for w in wz)})
for i, t in enumerate(trechos): t["id"] = f"L{i + 1:03d}"

# lotes: 4 grupos de minutos de rosto parecidos, em ordem
tot = sum(t["dur"] for t in trechos); alvo = tot / 4; lotes = [[]]; acc = 0
for t in trechos:
    if acc >= alvo * len(lotes) and len(lotes) < 4: lotes.append([])
    lotes[-1].append(t); acc += t["dur"]
LOT = []
for k, g in enumerate(lotes):
    for t in g: t["lote"] = k + 1
    LOT.append({"lote": k + 1, "trechos": len(g), "min_rosto": round(sum(t["dur"] for t in g) / 60, 2),
                "novo_ini": g[0]["novo_ini"], "novo_fim": g[-1]["novo_fim"],
                "falantes": sorted(set(t["falante"] for t in g)), "ids": [g[0]["id"], g[-1]["id"]],
                "maior_trecho_s": max(t["dur"] for t in g)})

blocos_out = []
for b in BL:
    n0 = COLOC[b["id"]]
    blocos_out.append({"id": b["id"], "falante": b["falante"], "ini_es": b["ini_es"], "fim_es": b["fim_es"],
                       "novo_ini": round(n0, 3), "novo_fim": round(n0 + b["D"], 3), "dur_de": round(b["D"], 3),
                       "dur_es": round(b["fim_es"] - b["ini_es"], 3), "audio": f"voz_limpa/{b['id']}.wav",
                       "audio_fala_ini": round(b["s0"], 3), "audio_fala_fim": round(b["e0"], 3), "de": b["de"]})
cen_out = []
for c in cenas:
    a, b = c["ini"], c["fim"]
    if a < CORTE[1] and b > CORTE[0]:
        if a >= CORTE[0] and b <= CORTE[1]: continue
        if a < CORTE[0]: b = CORTE[0]
        else: a = CORTE[1]
    cen_out.append({"tipo": c["tipo"], "rosto": c["rosto"], "orig_ini": round(a, 3), "orig_fim": round(b, 3),
                    "novo_ini": round(mapa(a), 3), "novo_fim": round(mapa(b), 3)})
TL = {"fonte": r"C:\Users\PICHAU\Downloads\Lead 2.mp4", "corte_papa_orig": list(CORTE), "duracao_final_s": round(DUR, 3),
      "regra": "video: cada secao src_ini-src_fim toca com setpts=fator (fator>1 = mais lento). Fala DE: blocos[].novo_ini (inicio da 1a palavra). "
               "Mapeamento linear dentro de cada secao: novo = novo_ini + fator*(t_orig - src_ini).",
      "secoes_video": SEC, "blocos": blocos_out, "cenas": cen_out}
json.dump(TL, open("timeline_de.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"duracao_final_s": round(DUR, 3), "palavras": PAL}, open("alinhamento_de.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump({"regras": ["trechos <= 12 s, cortados no meio de pausas entre palavras DE (ou na troca de cena)",
                      "entrada do HeyGen: video do trecho orig_ini-orig_fim com o AUDIO ORIGINAL (es), esticado pelo mesmo fator (setpts/atempo); audio novo = narracao_de_completa.wav de novo_ini a novo_fim",
                      "mode speed; 1 rosto por plano; fala_de=false -> so fechar boca/sem lipsync (sem fala DE no trecho)"],
           "total_trechos": len(trechos), "min_rosto_total": round(tot / 60, 2), "lotes": LOT, "trechos": trechos},
          open("lotes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("duracao final %.1f s (%.2f min)" % (DUR, DUR / 60), "secoes", len(SEC), "fora do limite", sum(not s["dentro_limite"] for s in SEC))
print("fatores min %.3f max %.3f" % (min(s["fator"] for s in SEC), max(s["fator"] for s in SEC)))
for s in SEC:
    if not s["dentro_limite"] or s["escala_pausas"] < 0.5: print("  atencao", s)
print("trechos", len(trechos), "min rosto %.1f" % (tot / 60), [(l["lote"], l["trechos"], l["min_rosto"]) for l in LOT])
print("maior trecho %.2f" % max(t["dur"] for t in trechos), "menor %.2f" % min(t["dur"] for t in trechos))
