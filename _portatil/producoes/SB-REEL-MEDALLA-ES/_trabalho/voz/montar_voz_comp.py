# -*- coding: utf-8 -*-
"""Versão COMPLETA: monta a narração única (tempo = tempo do vídeo) a partir de
  hook firme (comp/hook) + reza da v2 cortada (Oh glorioso San Benito… / Sácame de esta escasez.) com reverb na montagem
  + pausa do salão cheio + selfie ("Pasé casi seis meses sin clientes." da v2 + comp/selfie_nova)
  + padre (comp/padre) com pausas longas encurtadas.
Saídas em voz/comp/: narracao.mp3, narracao.palavras.json, timeline.json, selfie_heygen.mp3, padre_A.mp3, padre_B.mp3"""
import json, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
import montar_vozes as mv

V = Path(__file__).resolve().parent
D = V / "comp"
SR = mv.SR
F = int(0.01 * SR)


def cut(x, a, b):
    y = x[int(a * SR):int(b * SR)].copy()
    y[:F] *= np.linspace(0, 1, F); y[-F:] *= np.linspace(1, 0, F)
    return y


def ws_in(ws, a, b, extra):
    return [dict(w, **extra) for w in ws if w["ini"] >= a - 1e-6 and w["fim"] <= b + 1e-6]


def encurtar(x, ws, maxp, alvo):
    """encurta pausas > maxp para 'alvo' s; devolve áudio e palavras re-temporizadas."""
    out, nws, t_out, cur = [], [], 0.0, 0.0
    cortes = []
    for k in range(1, len(ws)):
        a, b = ws[k - 1]["fim"], ws[k]["ini"]
        if b - a > maxp:
            m = (a + b) / 2
            cortes.append((m - alvo / 2, m + alvo / 2, b - a))
    pos = 0.0; shift = 0.0; segs = []
    for (ka, kb, _), in zip(cortes):
        pass
    # trechos mantidos: [0, c1a] + [c1b-alvo.. ] -> mantém alvo/2 de cada lado da pausa
    keep, s = [], 0.0
    for a_p, b_p, dur in cortes:
        meio = (a_p + b_p) / 2
        pa = meio - dur / 2; pb = meio + dur / 2          # pausa real
        keep.append((s, pa + alvo / 2)); s = pb - alvo / 2
    keep.append((s, len(x) / SR))
    partes = [cut(x, a, b) for a, b in keep]
    # remapeia palavras
    def mp(t):
        acc = 0.0
        for a, b in keep:
            if t <= b + 1e-6:
                return acc + (t - a)
            acc += b - a
        return acc
    nws = [dict(w, ini=round(mp(w["ini"]), 3), fim=round(mp(w["fim"]), 3)) for w in ws]
    return np.concatenate(partes), nws


class Linha:
    def __init__(self):
        self.a = []; self.t = 0.0; self.ws = []

    def add(self, x, ws, t_src0, extra=None):
        for w in ws:
            d = dict(w); d["ini"] = round(w["ini"] - t_src0 + self.t, 3); d["fim"] = round(w["fim"] - t_src0 + self.t, 3)
            if extra: d.update(extra)
            self.ws.append(d)
        self.a.append(x); self.t += len(x) / SR

    def sil(self, s):
        self.a.append(np.zeros(int(round(s * SR)), np.float32)); self.t += s


# fontes
hook = mv.normalizar(mv.carregar(D / "hook.mp3"), -18.0); wh = mv.palavras(D / "hook.alinhamento.json")
com2 = mv.carregar(V / "v2" / "comerciante.mp3")            # já normalizado na v2 (reza -20, selfie -18)
wc2 = json.loads((V / "v2" / "comerciante.palavras.json").read_text(encoding="utf-8"))
sn = mv.normalizar(mv.carregar(D / "selfie_nova.mp3"), -18.0); wsn = mv.palavras(D / "selfie_nova.alinhamento.json")
pa = mv.normalizar(mv.carregar(D / "padre.mp3"), -18.0); wpa = mv.palavras(D / "padre.alinhamento.json")

L = Linha()
info = {}
# 1) hook firme
L.add(cut(hook, 0.0, 5.65), ws_in(wh, 0, 5.65, {}), 0.0, {"personagem": "comerciante", "parte": "hook"})
L.sil(0.15)
info["reza_ini"] = L.t
# 2) reza (v2): "Oh glorioso San Benito..." + "Sácame de esta escasez."
L.add(cut(com2, 0.15, 2.48), ws_in(wc2, 0.15, 2.48, {}), 0.15, {"personagem": "comerciante", "parte": "reza"})
L.sil(0.12)
L.add(cut(com2, 6.82, 8.92), ws_in(wc2, 6.82, 8.92, {}), 6.82, {"personagem": "comerciante", "parte": "reza"})
info["reza_fim"] = L.t
# 3) salão cheio sem fala
L.sil(2.5)
info["selfie_ini"] = L.t
# 4) selfie: "Pasé casi seis meses sin clientes." (v2) + nova
ini_p = next(w for w in wc2 if w["w"].startswith("pas"))["ini"] - 0.06
fim_c = next(w for w in wc2 if w["w"].startswith("clientes"))["fim"] + 0.06
ws_p = ws_in(wc2, ini_p, fim_c, {})
ws_p[0] = dict(ws_p[0], w="Pasé")
L.add(cut(com2, ini_p, fim_c), ws_p, ini_p, {"personagem": "comerciante", "parte": "selfie"})
L.sil(0.30)
sn2, wsn2 = encurtar(sn, wsn, 0.30, 0.24)
L.add(sn2, wsn2, 0.0, {"personagem": "comerciante", "parte": "selfie"})
info["selfie_fim"] = L.t
L.sil(0.40)
info["padre_ini"] = L.t
# 5) padre (pausas > 0,5 s -> 0,45 s)
pa2, wpa2 = encurtar(pa, wpa, 0.50, 0.45)
L.add(pa2, wpa2, 0.0, {"personagem": "sacerdote"})
info["padre_fim"] = L.t
L.sil(0.25)
info["total"] = round(L.t, 3)

audio = np.concatenate(L.a)
sf.write(D / "narracao.wav", audio, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(D / "narracao.wav"), "-b:a", "192k", str(D / "narracao.mp3")], check=True)
(D / "narracao.palavras.json").write_text(json.dumps(L.ws, ensure_ascii=False, indent=1), encoding="utf-8")

# trechos p/ HeyGen
def exporta(a, b, nome):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(D / "narracao.wav"),
                    "-b:a", "192k", str(D / nome)], check=True)

exporta(info["selfie_ini"], info["selfie_fim"] + 0.2, "selfie_heygen.mp3")
# padre: corte na maior pausa perto do meio
pw = [w for w in L.ws if w["personagem"] == "sacerdote"]
meio = (info["padre_ini"] + info["padre_fim"]) / 2
gaps = [((pw[k - 1]["fim"] + pw[k]["ini"]) / 2, pw[k]["ini"] - pw[k - 1]["fim"]) for k in range(1, len(pw))]
corte = max(gaps, key=lambda g: g[1] - abs(g[0] - meio) * 0.05)[0]
info["padre_corte"] = round(corte, 3)
exporta(info["padre_ini"], corte, "padre_A.mp3")
exporta(corte, info["padre_fim"] + 0.2, "padre_B.mp3")
(D / "timeline.json").write_text(json.dumps({k: round(v, 3) for k, v in info.items()}, indent=1), encoding="utf-8")
print({k: round(v, 3) for k, v in info.items()})
