# -*- coding: utf-8 -*-
"""SB série COMPLETA: cópia de _trabalho/montar_completa2.py adaptada a uma persona (fica em personas/<slug>/completa/).
Narração (t) = gancho firme (hook.mp3) + reza cortada de ../reza.mp3 (reverb) + virada sem voz (../depois.mp4)
  + selfie (selfie.mp3: 1ª frase sobre o take 'frustrado', resto HeyGen selfie_final.mp4) + padre IDÊNTICO ao Medalla COMPLETA.
Config: cfg_comp.json.   Rodar:  python montar_completa.py [--plano] [--so-audio] [--so-final]  ->  mont/master.mp4
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent            # personas/<slug>/completa
PP = P.parent                                   # personas/<slug>
AQ = P.parents[2]                               # _trabalho
SLUG = PP.name
CFG = json.loads((P / "cfg_comp.json").read_text(encoding="utf-8"))
M = P / "mont"; M.mkdir(exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS")
GR = AQ / "graficos"; TK = AQ / "takes"
PA = AQ / "completa" / "padre"
SELFIE = P / "selfie_final.mp4"
SAIDA = M / "master.mp4"
FPS, SR = 30, 48000
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
ROSTO_SELF = tuple(CFG["rosto_selfie"])
ROSTO_SAC = (558, 650)
sys.path.insert(0, str(AQ / "voz")); import montar_vozes as mv  # noqa

# ---------------------------------------------------------------- linha do tempo da narração (t)
W_HOOK = [dict(w, personagem=SLUG, parte="hook") for w in mv.palavras(P / "hook.alinhamento.json")]
HOOK_FIM = W_HOOK[-1]["fim"] + 0.12
T_REZA = round(max(5.5, HOOK_FIM + 0.30), 3)
REZA = CFG["reza"]                               # trechos de ../reza.mp3
REZA_GAP = 0.35
REZA_FIM = T_REZA + sum(b - a for a, b in REZA) + REZA_GAP * (len(REZA) - 1)
C = round(REZA_FIM + 0.45, 3)                     # corte p/ a virada (depois.mp4), sem voz
T_SELF = round(C + 2.45, 3)
PAD_GAP = 0.40
W_SELF = [dict(w, personagem=SLUG, parte="selfie") for w in mv.palavras(P / "selfie.alinhamento.json")]
W_PAD = json.loads((PA / "palavras.json").read_text(encoding="utf-8"))


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


SELF_DUR = W_SELF[-1]["fim"] + 0.15
T_PAD = round(T_SELF + SELF_DUR + PAD_GAP, 3)
PAD_FIM = W_PAD[-1]["fim"] + 0.30
NARR_FIM = T_PAD + PAD_FIM


def cortes_selfie():
    """pausas da selfie viram jump cut (deixa 0,22 s). A 1ª frase sempre fecha num corte (frustrado -> selfie).
    Trechos menores que 1,2 s não ganham corte (evita pisca-pisca)."""
    i1 = next(i for i, w in enumerate(W_SELF) if re.search(r"[.!?]$", w["w"]))
    out, ult = [], 0.0
    for i in range(len(W_SELF) - 1):
        a, b = W_SELF[i]["fim"], W_SELF[i + 1]["ini"]
        if i != i1 and (b - a < 0.40 or a - ult < 1.2 or SELF_DUR - b < 1.2):
            continue
        sobra = min(0.22, b - a)
        ra, rb = round(a + sobra / 2, 3), round(b - sobra / 2, 3)
        if rb - ra < 0.02:
            ra, rb = round((a + b) / 2 - 0.01, 3), round((a + b) / 2 + 0.01, 3)
        out.append((ra, rb)); ult = rb
    return out


R_SELF = cortes_selfie()
R_PAD = [(2.20, 2.45), (5.85, 6.05), (7.27, 7.49), (10.33, 10.60), (15.70, 15.98), (17.62, 17.90),
         (21.18, 21.48), (28.80, 29.40), (32.90, 33.14)]
REMOV = [(T_SELF + a, T_SELF + b) for a, b in R_SELF] + [(T_PAD + a, T_PAD + b) for a, b in R_PAD]


def S(t):
    x = t
    for a, b in REMOV:
        if t >= b - 1e-9:
            x -= (b - a)
        elif t > a:
            x -= (t - a)
    return int(x * FPS + 0.5) / FPS


def brv(n):
    return next(p for p in BR.glob(f"SB-BRV-{n} *KLING25.mp4") if "REPROV" not in p.name)


def s(x): return T_SELF + x       # local selfie -> t
def p(x): return T_PAD + x        # local padre  -> t


EDL = [
    ("take", 0.0, T_REZA, dict(src=P / "gancho_amplo.mp4", ss=0.0, zoom=CFG.get("zoom_gancho", 1.12),
                               centro=tuple(CFG.get("centro_gancho", (540, 1100))), interp=True)),
    ("take", T_REZA, C, dict(src=PP / "antes.mp4", ss=0.0, zoom=1.15, centro=tuple(CFG["centro_antes"]), interp=True)),
    ("take", C, T_SELF, dict(src=PP / "depois.mp4", ss=CFG.get("ss_depois", 0.4))),
    ("take", s(0.0), s(R_SELF[0][0]), dict(src=P / "frustrado.mp4", ss=CFG.get("ss_frustrado", 0.2))),
]
_z = [1.13, 1.0]
for k, (a0, b0) in enumerate(R_SELF):
    fim = s(R_SELF[k + 1][0]) if k + 1 < len(R_SELF) else T_PAD
    EDL.append(("selfie", s(b0), fim, dict(zoom=_z[k % 2])))
EDL += [
    ("pad", p(0.0), p(2.10), dict(zoom=1.0)),
    ("take", p(2.10), p(6.07), dict(src=TK / "medalla.mp4", ss=0.2)),
    ("pad", p(6.07), p(7.27), dict(zoom=1.0)),
    ("pad", p(7.49), p(10.33), dict(zoom=1.12)),
    ("take", p(10.33), p(12.70), dict(src=brv(35), ss=0.3)),
    ("take", p(12.70), p(16.02), dict(src=brv("03"), ss=0.6)),
    ("pad", p(16.02), p(17.62), dict(zoom=1.0)),
    ("take", p(17.62), p(21.53), dict(src=brv(47), ss=0.3)),
    ("pad", p(21.53), p(23.62), dict(zoom=1.12)),
    ("take", p(23.62), p(25.25), dict(src=brv(14), ss=1.0)),
    ("take", p(25.25), p(29.47), dict(src=brv(50), ss=0.5)),
    ("pad", p(29.47), p(32.90), dict(zoom=1.0)),
    ("pad", p(33.14), NARR_FIM, dict(zoom=1.12)),
]
TOTAL = S(NARR_FIM)
TOCA = next(w for w in W_PAD if w["w"].lower().startswith("toca"))["ini"]
CTA = S(p(TOCA))


