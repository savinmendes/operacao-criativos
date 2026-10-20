import sys
PAD_EDL = '''EDL += [
    ("pad", p(0.0), p(2.40), dict(zoom=1.0)),
    ("take", p(2.40), p(6.70), dict(src=TK / "medalla.mp4", ss=0.2)),
    ("pad", p(6.70), p(8.10), dict(zoom=1.0)),
    ("pad", p(8.34), p(11.66), dict(zoom=1.12)),
    ("take", p(11.66), p(14.00), dict(src=brv(35), ss=0.3)),
    ("take", p(14.00), p(16.78), dict(src=brv("03"), ss=0.6)),
    ("pad", p(16.78), p(18.74), dict(zoom=1.0)),
    ("take", p(18.74), p(22.22), dict(src=brv(47), ss=0.3)),
    ("pad", p(22.22), p(24.95), dict(zoom=1.12)),
    ("take", p(24.95), p(26.55), dict(src=brv(14), ss=1.0)),
    ("take", p(26.55), p(31.10), dict(src=brv(50), ss=0.5)),
    ("pad", p(31.10), p(34.50), dict(zoom=1.0)),
    ("pad", p(34.60), NARR_FIM, dict(zoom=1.12)),
]'''
R_PAD = "R_PAD = [(2.40, 2.55), (6.58, 6.70), (8.10, 8.34), (11.66, 11.92), (16.56, 16.78), (18.74, 18.98), (21.98, 22.22), (30.90, 31.10), (34.50, 34.60)]  # padre FR"

def sub(s, a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a))
    return s.replace(a, b)

def comum(s):
    i = s.index("R_PAD = ["); j = s.index("]", s.index("(32.90, 33.14)")) + 1
    s = s[:i] + R_PAD + s[j:]
    i = s.index('    ("pad", p(0.0), p(2.10)'); j = s.index("]\n", i) + 1
    k = s.rindex("EDL += [", 0, i)
    s = s[:k] + PAD_EDL + s[j:]
    s = sub(s, 'startswith("toca")', 'startswith("appuie")')
    s = sub(s, '("titulo_gancho.png", 0, T_REZA), ("cta_masinfo_unico.png", CTA, TOTAL), ("selo_ficticio_mini.png", 0, TOTAL)',
            '("titulo_gancho_fr.png", 0, T_REZA), ("cta_ensavoirplus_unico_fr.png", CTA, TOTAL), ("selo_ficticio_mini_fr.png", 0, TOTAL)')
    return s

f = sys.argv[1]
s = open(f, encoding="utf-8").read().replace("\r\n", "\n")
s = comum(s)
if f.endswith("montar.py"):   # uci / feria
    s = sub(s, 'AQ = Path(__file__).resolve().parent                       # personas/<slug>/completa\nTR = AQ.parents[2]                                        # _trabalho',
            'AQ = Path(__file__).resolve().parent                       # _trabalho/fr/<slug>  (versao FR)\nTR = AQ.parents[1]                                        # _trabalho\nPP = TR / "personas" / AQ.name                            # takes da persona (iguais ao ES)')
    s = sub(s, 'GR = TR / "graficos"; TK = TR / "takes"\nPA = TR / "completa" / "padre"',
            'GR = TR / "fr" / "_comum" / "graficos"; TK = TR / "takes"\nPA = TR / "fr" / "_comum" / "padre"')
    s = sub(s, 'REZA_SRC = AQ.parent / CFG["reza_src"]', 'REZA_SRC = AQ / CFG["reza_src"]')
    s = sub(s, 'T_REZA = 5.80\nT_VIRA = 10.40\nT_SELF = 12.85',
            '''T_REZA = round(max(5.80, HOOK_FIM + 0.30), 3)
_REZA_FIM = T_REZA + CFG.get("reza_atraso", 0.15) + sum(b - a for a, b in REZA) + 0.25 * (len(REZA) - 1)
T_VIRA = round(max(10.40, _REZA_FIM + 0.90), 3)
T_SELF = round(T_VIRA + 2.45, 3)''')
    s = sub(s, 'SELF_DUR = W_SELF[-1]["fim"] + 0.15\nT_PAD = round(T_SELF + SELF_DUR + PAD_GAP, 3)',
            'SELF_DUR = CFG["self_dur"]\nPAD_GAP = max(0.0, min(PAD_GAP, CFG["selfie_mp3_dur"] - SELF_DUR - 0.04))  # sem quadro segurado no fim da selfie\nT_PAD = round(T_SELF + SELF_DUR + PAD_GAP, 3)')
    s = sub(s, 'd = dict(d); d["src"] = AQ.parent / d["src"]', 'd = dict(d); d["src"] = PP / d["src"]')
    # reza com tempos reais de palavra (alinhamento FR)
    s = sub(s, '''        pal = txt.split(); d = (b - a - 0.1) / len(pal)
        ws += [dict(w=x, ini=round(t + 0.05 + k * d, 3), fim=round(t + 0.05 + (k + 1) * d - 0.03, 3), personagem=PERS, parte="reza")
               for k, x in enumerate(pal)]''',
            '''        ws += [dict(w, ini=round(w["ini"] - a + t, 3), fim=round(min(w["fim"], b) - a + t, 3), personagem=PERS, parte="reza")
               for w in mv.palavras(AQ / "reza.alinhamento.json") if a <= w["ini"] < b - 0.1]''')
    s = sub(s, 'for (a, b), txt in zip(REZA, REZA_TXT):', 'for a, b in REZA:')
    s = sub(s, 'REZA_TXT = CFG["reza_txt"]                                # palavras de cada trecho (legenda)\n', '')
else:   # desempleado (montar_completa.py)
    s = sub(s, 'P = Path(__file__).resolve().parent            # personas/<slug>/completa\nPP = P.parent                                   # personas/<slug>\nAQ = P.parents[2]                               # _trabalho\nSLUG = PP.name',
            'P = Path(__file__).resolve().parent            # _trabalho/fr/<slug> (versao FR)\nAQ = P.parents[1]                               # _trabalho\nSLUG = P.name\nPP = AQ / "personas" / SLUG                     # takes da persona (iguais ao ES)\nPC = PP / "completa"')
    s = sub(s, 'GR = AQ / "graficos"; TK = AQ / "takes"\nPA = AQ / "completa" / "padre"\nSELFIE = P / "selfie_final.mp4"',
            'GR = AQ / "fr" / "_comum" / "graficos"; TK = AQ / "takes"\nPA = AQ / "fr" / "_comum" / "padre"\nSELFIE = P / "selfie_heygen.mp4"\nSELF_HG0 = CFG["selfie_heygen_ini"]')
    s = sub(s, 'SELF_DUR = W_SELF[-1]["fim"] + 0.15', 'SELF_DUR = CFG["self_dur"]\nPAD_GAP = max(0.0, min(PAD_GAP, dur(P / "selfie.mp3") - SELF_DUR - 0.04))  # sem quadro segurado')
    s = sub(s, 'R_SELF = cortes_selfie()', 'R_SELF = [tuple(x) for x in CFG["r_self"]]  # calculado p/ o audio FR (1o corte = frustrado -> selfie HeyGen)')
    s = sub(s, 'src=P / "gancho_amplo.mp4"', 'src=PC / "gancho_amplo.mp4"')
    s = sub(s, 'src=P / "frustrado.mp4"', 'src=PC / "frustrado.mp4"')
    s = sub(s, '''_z = [1.13, 1.0]
for k, (a0, b0) in enumerate(R_SELF):
    fim = s(R_SELF[k + 1][0]) if k + 1 < len(R_SELF) else T_PAD
    EDL.append(("selfie", s(b0), fim, dict(zoom=_z[k % 2])))''',
            '''_z = 1.13
for k, (a0, b0) in enumerate(R_SELF):
    fim_l = R_SELF[k + 1][0] if k + 1 < len(R_SELF) else None
    pts = [b0] + [e for e in CFG.get("self_trocas", []) if b0 < e < (fim_l if fim_l is not None else 1e9)] + [fim_l]
    for a1, b1 in zip(pts, pts[1:]):
        EDL.append(("selfie", s(a1), s(b1) if b1 is not None else T_PAD, dict(zoom=_z)))
        _z = 1.0 if _z > 1.0 else 1.13''')
    s = sub(s, 'inp = ["-ss", f"{a - T_SELF:.3f}"', 'inp = ["-ss", f"{a - T_SELF - SELF_HG0:.3f}"')
    s = sub(s, 'rz = load(PP / "reza.mp3")', 'rz = load(P / "reza.mp3")')
    s = sub(s, 'mv.palavras(PP / "reza.alinhamento.json")', 'mv.palavras(P / "reza.alinhamento.json")')
open(f, "w", encoding="utf-8").write(s)
print("patch ok", f)
