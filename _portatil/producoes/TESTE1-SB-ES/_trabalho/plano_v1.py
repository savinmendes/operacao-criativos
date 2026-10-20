# -*- coding: utf-8 -*-
"""Plano da montagem: posição de cada fala na linha do tempo final (T) e lista de cenas.
python plano.py  -> imprime a linha do tempo e confere as fontes."""
import json
from pathlib import Path
AQ = Path(__file__).resolve().parent
FPS = 30
ORDEM = [("L01", 0.0), ("L02", 0.0), ("L03", 0.10), ("L04", 0.12), ("L05", 0.30), ("L06", 0.35), ("L07", 0.10),
         ("L08", 0.35), ("L09", 0.45), ("L09b", 0.40), ("L10", 0.50), ("L11", 0.45), ("L12", 0.45)]
CAUDA = 1.0
LIN = {}; t = 0.0
for i, gap in ORDEM:
    d = json.loads((AQ / "voz" / "c" / f"{i}.json").read_text(encoding="utf-8"))
    t += gap; d["T0"] = round(t, 3); LIN[i] = d; t += d["dur"]
TOTAL = round(round((t + CAUDA) * FPS) / FPS, 4)

def W(i, txt, n=1):
    """início absoluto (T) da n-ésima palavra que começa com txt na fala i"""
    k = 0
    for p in LIN[i]["palavras"]:
        w = p["w"].lower().strip("¿¡.,;:!?…")
        if w == txt.lower():
            k += 1
            if k == n: return round(LIN[i]["T0"] + p["ini"], 3)
    raise KeyError((i, txt, n))
def FIM(i):
    return round(LIN[i]["T0"] + LIN[i]["palavras"][-1]["fim"], 3)

# peças de fonte (s no TESTE1, cortes limpos)
P = dict(
    react=(0.0, 3.38), agr=(3.40, 10.25), vazio=(10.28, 13.37), mult1=(13.42, 15.95), mult2=(15.95, 19.07),
    rep=(19.12, 25.0), aurA=(25.03, 31.0), aurB=(31.0, 37.48), aurC=(37.5, 39.8),
    P1=(40.62, 46.75), tecl=(46.80, 47.82), P2=(47.92, 51.40), sb_pe=(50.30, 52.58), sb_esc=(52.60, 54.95),
    sb_mar=(55.0, 57.95), mul1=(58.0, 60.03), P3=(60.10, 63.05), board=(63.15, 73.75), P4=(73.99, 75.58),
    mul2=(75.95, 77.85), P5=(80.32, 82.10), perg=(82.20, 85.50), P6=(85.62, 88.75), cruz=(88.85, 90.05),
    mont=(90.10, 91.95), hrez=(92.0, 93.9), P7=(93.97, 95.80), praia=(95.86, 97.18), P8=(97.27, 98.95),
    congr=(98.97, 100.55), carro=(104.88, 106.95), mrez=(107.05, 108.95), P9=(113.50, 118.93),
    P10=(129.72, 132.77), divid=(132.82, 139.68), P11=(139.72, 141.75))
def S(T, pecas, **kw): return dict(T=round(T, 3), pecas=pecas, **kw)
CENAS = [
    S(0.0, ["react"], ls=True, desc="react mujer + câmera"),
    S(LIN["L02"]["T0"] - 0.05, ["agr"], desc="câmera de segurança: agressão"),
    S(FIM("L03") + 0.45, ["rep"], ls=True, desc="reportera"),
    S(W("L04", "uno") - 0.10, ["mult1"], desc="câmera: multidão (más buscados)"),
    S(LIN["L05"]["T0"] - 0.05, ["aurA"], ls=True, desc="Aurelio A"),
    S(W("L05", "sentir") - 0.05, ["vazio"], desc="carrito vazio (olvidado)"),
    S(W("L05", "rezaba") - 0.10, ["hrez"], desc="homem rezando"),
    S(W("L05", "nada") - 0.25, ["mrez"], desc="mulher rezando"),
    S(W("L05", "hasta") - 0.05, ["aurB"], ls=True, desc="Aurelio B"),
    S(W("L05", "al") - 0.05, ["mult2"], desc="câmera: multidão (llenó de clientes)"),
    S(W("L05", "no", 2) - 0.60, ["aurC"], ls=True, crop=True, desc="Aurelio C (repórter na borda: recorte)"),
    S(FIM("L05") + 0.12, [("aurA", 0.0, 1.18), ("aurB", 0.0, 1.18)], ls=True, desc="Aurelio D zoom (pede a transmissão)"),
    # sacerdote (moldura EN VIVO em todas as peças P*)
    S(LIN["L08"]["T0"] - 0.10, ["P1"], ls=True, desc="padre P1"),
    S(W("L08", "presten") - 0.10, ["P2"], ls=True, desc="padre P2"),
    S(W("L08", "pronto") - 0.30, ["tecl"], desc="teclado (no quieren)"),
    S(W("L08", "pronto") + 0.72, ["P3", "P4", "P5"], ls=True, desc="padre P3+P4+P5"),
    S(W("L09", "oh") - 0.05, ["sb_pe"], desc="San Benito de pé"),
    S(W("L09", "guardián") - 0.10, ["sb_esc"], desc="San Benito escrevendo"),
    S(W("L09", "que", 1) - 0.10, ["sb_mar"], desc="San Benito no penhasco"),
    S(W("L09", "y", 1) - 0.10, ["mul1"], desc="mulher rezando 1"),
    S(W("L09", "con", 2) - 0.10, ["cruz", "mul2"], desc="cruz + mulher rezando 2"),
    S(W("L09", "palabras") - 0.10, ["board"], board=True, desc="quadro das 12 palavras"),
    S(LIN["L10"]["T0"] - 0.10, ["P6", "P7"], ls=True, desc="padre P6+P7"),
    S(W("L10", "están") - 0.10, ["carro"], desc="homem no carro sorrindo"),
    S(W("L10", "todos", 1) - 0.10, ["P8"], ls=True, desc="padre P8"),
    S(W("L10", "fue", 1) - 0.10, ["perg"], desc="pergaminho (escrita)"),
    S(W("L10", "y", 1) - 0.05, ["mont"], desc="montanhas (secreto)"),
    S(W("L10", "durante") - 0.10, ["P9", ("P8", 0.3, 1.0), ("P7", 1.0, 1.0)], ls=True, desc="padre P9+P8"),
    S(W("L10", "yo") - 0.10, ["praia"], desc="menino na praia (viaje)"),
    S(W("L10", "italia") - 0.30, ["P10", "P5"], ls=True, desc="padre P10+P5"),
    S(W("L10", "congreso") - 0.35, ["congr"], desc="congresso"),
    S(W("L10", "recibí") - 0.05, [], chat=True, desc="WhatsApp + transferência (ES)"),
    S(W("L10", "al", 1) - 0.10, ["P11", "P1"], ls=True, desc="padre P11"),
    S(LIN["L11"]["T0"] - 0.15, ["divid"], desc="dívidas -> alívio (futuro)"),
    S(LIN["L12"]["T0"] - 0.10, ["P3", "P9"], ls=True, desc="padre CTA 1"),
    S(W("L12", "toca") - 0.10, ["P6", "P2", "P11"], ls=True, desc="padre CTA 2 (Ver más)"),
    S(W("L12", "vuelve") - 0.10, [("P1", 2.5, 1.0), "P10", "P4"], ls=True, desc="padre CTA 3 (envía)"),
]
CTA_T = W("L12", "toca")

def segmentos():
    """cada cena -> lista de peças (src_a, src_b, zoom, q0, n) com vel única por cena"""
    out = []
    for k, c in enumerate(CENAS):
        fim = CENAS[k + 1]["T"] if k + 1 < len(CENAS) else TOTAL
        c = dict(c); c["fim"] = round(fim, 3); q0 = round(c["T"] * FPS); q1 = round(fim * FPS); c["q0"], c["n"] = q0, q1 - q0
        if c.get("chat"): c["pecas"] = []; out.append(c); continue
        pcs = []
        for p in c["pecas"]:
            nome, off, z = (p, 0.0, 1.0) if isinstance(p, str) else p
            a, b = P[nome]; pcs.append((nome, a + off, b, z))
        disp = sum(b - a for _, a, b, _ in pcs); prec = c["n"] / FPS
        vel = min(1.0, disp / prec); c["vel"] = round(vel, 3)
        res = []; q = q0; rest = c["n"]
        for nome, a, b, z in pcs:
            if rest <= 0: break
            nq = min(rest, int(round((b - a) / vel * FPS)))
            if nq <= 0: continue
            res.append(dict(nome=nome, a=round(a, 3), b=round(a + nq / FPS * vel, 3), zoom=z, q0=q, n=nq)); q += nq; rest -= nq
        if rest > 0: res[-1]["n"] += rest; res[-1]["b"] = round(res[-1]["b"] + rest / FPS * vel, 3)
        c["pecas"] = res; out.append(c)
    return out

if __name__ == "__main__":
    for i, d in LIN.items(): print(f"{i:5s} T {d['T0']:7.2f}-{d['T0'] + d['dur']:7.2f} ({d['p']})")
    print("TOTAL", TOTAL, "CTA", CTA_T)
    for c in segmentos():
        alerta = "" if c.get("vel", 1) >= (0.9 if c.get("ls") else 0.85) else "  !!! LENTO"
        print(f"{c['T']:7.2f}-{c['fim']:7.2f} ({c['fim']-c['T']:5.2f}) vel {c.get('vel',1):.2f}{alerta} {c['desc']}")
        for p in c["pecas"]: print(f"            {p['nome']:6s} {p['a']:7.2f}-{p['b']:7.2f} z{p['zoom']} q{p['q0']}+{p['n']}")
