from pathlib import Path
p=Path("montar_completa_fr.py"); s=p.read_text(encoding="utf-8")
ab=Path("../abuela/montar_completa_persona_fr.py").read_text(encoding="utf-8")
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old,s.count(old)); s=s.replace(old,new)
rep('''"""SB série COMPLETA: cópia de _trabalho/montar_completa2.py adaptada a uma persona (fica em personas/<slug>/completa/).''',
'''"""FR: cópia de personas/campesino/completa/montar_completa.py (ES) adaptada ao francês: vozes FR (voz/), selfie HeyGen FR
(selfie_final.mp4 começa em SELF_OFF da selfie.mp3), reza FR inteira (voz/reza.mp3), padre/gráficos FR (_comum), legenda FR.
Takes, B-roll, trilha e zooms iguais ao ES (cfg_comp_es.json). Cortes do padre ancorados nas mesmas frases da fala FR.
--- docstring ES ---
SB série COMPLETA: cópia de _trabalho/montar_completa2.py adaptada a uma persona (fica em personas/<slug>/completa/).''')
rep('''P = Path(__file__).resolve().parent            # personas/<slug>/completa
PP = P.parent                                   # personas/<slug>
AQ = P.parents[2]                               # _trabalho
SLUG = PP.name
CFG = json.loads((P / "cfg_comp.json").read_text(encoding="utf-8"))''',
'''P = Path(__file__).resolve().parent            # fr/<slug>
AQ = Path("C:/Users/PICHAU/Downloads/SB-REEL-MEDALLA-ES/_trabalho")
SLUG = P.name
PP = AQ / "personas" / SLUG                     # antes/depois ES
PC = PP / "completa"                            # gancho_amplo/frustrado ES
V = P / "voz"
CFG = json.loads((P / "cfg_comp_es.json").read_text(encoding="utf-8"))
SELF_OFF = json.loads((P / "config_fr.json").read_text(encoding="utf-8"))["selfie_off"]''')
rep('''GR = AQ / "graficos"; TK = AQ / "takes"
PA = AQ / "completa" / "padre"''','''GR = AQ / "fr" / "_comum" / "graficos"; TK = AQ / "takes"
PA = AQ / "fr" / "_comum" / "padre"''')
rep('mv.palavras(P / "hook.alinhamento.json")','mv.palavras(V / "hook.alinhamento.json")')
rep('''REZA = CFG["reza"]                               # trechos de ../reza.mp3''','''W_REZA0 = mv.palavras(V / "reza.alinhamento.json")
REZA = [[0.0, round(W_REZA0[-1]["fim"] + 0.15, 3)]]   # reza FR inteira (o ES cortava 2 trechos de ../reza.mp3)''')
rep('mv.palavras(P / "selfie.alinhamento.json")','mv.palavras(V / "selfie.alinhamento.json")')
rep('''PAD_FIM = W_PAD[-1]["fim"] + 0.30''','''PAD_FIM = min(W_PAD[-1]["fim"] + 0.30, dur(PA / "padre_parte1.mp4") + dur(PA / "padre_parte2.mp4") - 0.04)''')
i0=ab.index("def plano_padre():"); i1=ab.index("B_PAD, R_PAD = plano_padre()")
plano=ab[i0:i1]
rep('''R_SELF = cortes_selfie()
R_PAD = [(2.20, 2.45), (5.85, 6.05), (7.27, 7.49), (10.33, 10.60), (15.70, 15.98), (17.62, 17.90),
         (21.18, 21.48), (28.80, 29.40), (32.90, 33.14)]''', plano + '''B_PAD, R_PAD = plano_padre()
R_SELF = cortes_selfie()
assert R_SELF[0][0] < SELF_OFF < R_SELF[0][1], (R_SELF[0], SELF_OFF)''')
rep('''dict(src=P / "gancho_amplo.mp4"''','''dict(src=PC / "gancho_amplo.mp4"''')
rep('''dict(src=P / "frustrado.mp4"''','''dict(src=PC / "frustrado.mp4"''')
j0=s.index('EDL += [\n    ("pad", p(0.0), p(2.10)'); j1=s.index("TOTAL = S(NARR_FIM)")
k0=ab.index("b = [0.0] + B_PAD + [None]"); k1=ab.index("TOTAL = S(NARR_FIM)")
s=s[:j0]+ab[k0:k1]+s[j1:]
rep('startswith("toca")','startswith("appuie")')
rep('''inp = ["-ss", f"{a - T_SELF:.3f}"''','''inp = ["-ss", f"{a - T_SELF - SELF_OFF:.3f}"''')
rep('''load(P / "hook.mp3")''','''load(V / "hook.mp3")''')
rep('''rz = load(PP / "reza.mp3")''','''rz = load(V / "reza.mp3")''')
rep('''mv.palavras(PP / "reza.alinhamento.json")''','''mv.palavras(V / "reza.alinhamento.json")''')
rep('''load(P / "selfie.mp3")''','''load(V / "selfie.mp3")''')
rep('''pad = load(PA / "padre.mp3")''','''pad = load(PA / "padre.mp3")[:int(PAD_FIM * SR)]''')
rep('''str(P / "legenda_comp.py")''','''str(P / "legenda_comp_fr.py")''')
rep('''pngs = [("titulo_gancho.png", 0, T_REZA), ("cta_masinfo_unico.png", CTA, TOTAL), ("selo_ficticio_mini.png", 0, TOTAL)]''',
'''pngs = [("titulo_gancho_fr.png", 0, T_REZA), ("cta_ensavoirplus_unico_fr.png", CTA, TOTAL), ("selo_ficticio_mini_fr.png", 0, TOTAL)]''')
rep('''print("TOTAL", TOTAL, "CTA", CTA); sys.exit()''','''print("R_SELF", R_SELF, "R_PAD", R_PAD); print("TOTAL", TOTAL, "CTA", CTA); sys.exit()''')
p.write_text(s,encoding="utf-8")
