# -*- coding: utf-8 -*-
"""Montagem da v2 enxuta (~2:00, 720x1280 30 fps) -> v2/SB-ES_NOTICIA-AURELIO_v2_FICTICIO.mp4 (+ _narracion.txt).
Ordem: react (take novo) + piloto (briga + reportera) -> Aurelio (takes novos + narração sobre b-roll) -> "¡Claro!" (só voz)
-> segmentação nova (TTS Gabriela) -> padre EN VIVO (punch-in 100/112 por frase) -> oração (exatamente a v1)
-> prova (918 AÑOS, prints, +497) -> futuro (L11) -> CTA (take P6 + setas TOCA «VER MÁS»).
Takes vêm dos manifest.json dos agentes (fontes.py); sem manifest usa placeholders da v1 (--ph força placeholder).
Uso: python montar_v2.py [--ph] [--saida arquivo.mp4] [--so-plano]"""
import json, re, subprocess, sys, importlib.util
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import fontes

AQ = Path(__file__).resolve().parent; V2T = AQ.parent; V2 = V2T.parent; V1 = V2.parent / "_trabalho"
M = AQ / "mont"; M.mkdir(exist_ok=True); G = V1 / "graficos"; GV = AQ / "graficos"; GV.mkdir(exist_ok=True)
FPS, SR = 30, 48000
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
BASE = V1 / "lama" / "base_limpa.mp4"; NV = V1 / "audio" / "sep" / "htdemucs" / "orig" / "no_vocals.wav"
V1CORPO = V1 / "mont" / "corpo.mp4"; PILCORPO = V2T / "mont" / "corpo.mp4"; PILMIX = V2T / "mont" / "mix.wav"
ARGS = sys.argv[1:]
OUT = Path(ARGS[ARGS.index("--saida") + 1]) if "--saida" in ARGS else V2 / "SB-ES_NOTICIA-AURELIO_v2_FICTICIO.mp4"
WIN = (0, 297, 720, 840)                    # janela do vídeo dentro da moldura do post
BANDA = (128, 1140)                         # moldura EN VIVO: faixas de UI (topo < 128, base > 1140) ficam sem zoom
ZOOM = 1.12; ZC = (360, 560)                # punch-in do padre: escala e centro
CAUDA = 0.8


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:2500]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + (["-t", f"{t:.3f}"] if t else []) + \
          ["-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < int(0.5 * SR): a = np.concatenate([a, np.zeros((int(0.5 * SR) - len(a), 2), np.float32)])
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    raw.unlink(); l = [x for x in r.stderr.splitlines() if x.strip().startswith("I:")]
    return float(l[-1].split()[1])


def fade(a, ms=12):
    n = min(int(ms / 1000 * SR), len(a) // 2)
    if n: a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"]", "", w).lower()


def v1json(i): return json.loads((V1 / "voz" / "c" / f"{i}.json").read_text(encoding="utf-8"))


# ------------------------------------------------------------------ catálogo de b-roll (base_limpa, s) e regras de corte
BR = dict(vazio=(10.45, 13.30, "post"), mult1=(13.42, 15.95, "post"), mult2=(15.95, 19.20, "post"),
          tecl=(46.75, 47.85, ""), sb_pe=(51.45, 52.25, ""), sb_esc=(52.55, 55.30, ""), sb_mar=(55.36, 58.17, ""), mul1=(58.25, 59.93, ""),
          perg_a=(82.55, 84.30, ""), perg_b=(84.30, 85.57, ""), cruz=(88.82, 89.97, ""), mont=(90.45, 91.55, ""), hrez=(92.40, 93.90, ""),
          praia=(95.86, 97.20, ""), congr=(99.03, 101.17, ""), mrez1=(106.56, 107.70, ""), mrez2=(107.70, 108.80, ""),
          divid=(132.83, 139.67, ""))
CHAT = dict(chat1=G / "chat_1.png", chat2=G / "chat_2.png")      # Geralda (WhatsApp) / Rosa María (transferência)
POOL = dict(aurelio=["mult1", "vazio"], padre=["mont", "cruz", "hrez"], react=["mult1"], reportera=["mrez1", "cruz", "mont"])
COBRE_KW = [("escuche", ["mul1"]), ("secreto", ["sb_esc"]), ("video", ["mul1"]), ("benito", ["sb_pe"]), ("golpe", ["mult1"]), ("mí", ["mult1"])]
VEL_MIN = 0.80
# kw/ate = frases (palavras limpas); br = b-rolls em ordem; dur = s mínimos (corta na próxima fronteira de palavra)
REGRAS = [
    dict(ag="aurelio", kw="sentir", br=["vazio"], ate=["rezaba", "hasta"]),
    dict(ag="aurelio", kw="rezaba", br=["hrez", "mrez1", "mrez2"], ate=["hasta"]),
    dict(ag="aurelio", kw="al día", br=["mult2"], ate=["no lo"]),
    dict(ag="padre", kw="no quieren", br=["tecl", "perg_b"], ate=["repitan"]),
    dict(ag="padre", kw="están llegando", br=["chat1"], dur=2.2),
    dict(ag="padre", kw="fue escrita", br=["perg_a"], dur=1.9, so_take=True),
    dict(ag="padre", kw="monjes", br=["sb_pe", "sb_mar"], ate=["yo", "la última"], recua=True),
    dict(ag="padre", kw="italia", br=["praia", "mont", "cruz"], ate=["la última"], recua_ate="yo"),
    dict(ag="padre", kw="congreso", br=["congr"], ate=["recibí"], recua_ate="la última"),
    dict(ag="padre", kw="recibí", br=["chat2"], ate=[]),
    dict(ag="padre", kw="imagina", br=["divid"], ate=[]),
    dict(ag="reportera", kw="si tú", br=["mrez1", "mrez2", "cruz", "mont"], ate=[]),
    dict(ag="reportera", kw="claro", br=["mult1"], ate=[]),
]
GIGANTES = [("olvidado de mí", "SE OLVIDÓ\\NDE MÍ"), ("forma correcta", "LA FORMA\\NCORRECTA"),
            ("918", "918 AÑOS"), ("novecientos dieciocho", "918 AÑOS"), ("497", "+497"), ("cuatrocientos noventa", "+497")]
TITULO = ("LO QUE PASÓ DESPUÉS", "NADIE LO PUEDE", "EXPLICAR"); TITULO_T = 3.0
NOME = {"react": "MUJER (react)", "piloto": None, "aurelio": "DON AURELIO", "reportera": "REPORTERA", "padre": "SACERDOTE"}


# ------------------------------------------------------------------ itens fixos (piloto, oração v1, falas v1, TTS novo)
def item_piloto(com_react):
    sp = importlib.util.spec_from_file_location("piloto", V2T / "piloto.py"); pil = importlib.util.module_from_spec(sp); sp.loader.exec_module(pil)
    t0 = pil.TB if com_react else 0.0
    P = []
    for p in pil.palavras():
        if p["ini"] < t0 - 0.01: continue
        if p["w"] == "don aurelio":                # desfaz a junção do piloto (a legenda junta de novo)
            m = (p["ini"] + p["fim"]) / 2; P += [dict(w="don", ini=p["ini"], fim=m, linha=p["linha"]), dict(w=p["raw"], ini=m, fim=p["fim"], linha=p["linha"])]
        else: P.append(dict(w=p["raw"], ini=p["ini"], fim=p["fim"], linha=p["linha"]))
    quem = {"B0": "AGRESOR", "B1": "DON AURELIO", "L04": "REPORTERA", "L01": "MUJER (react)"}
    return dict(id="PIL", ag="piloto", tipo="fixo", video=str(PILCORPO), audio=str(PILMIX), v_off=0.0, uso=[t0, pil.TOTAL],
                palavras=P, texto="", ruins=[], post=True, quem_linha=quem)


def item_reza():
    """oração exatamente como a v1: corpo v1 66,22-90,90 (padre reza -> San Benito -> mulheres -> quadro) + L09/L09b com reverb"""
    T0v, T1v = 66.22, 90.90; d9, d9b = v1json("L09"), v1json("L09b"); o9, o9b = 66.24 - T0v, 82.44 - T0v
    N = int((T1v - T0v) * SR); a = np.zeros((N + SR, 2), np.float32)
    for d, o, i in ((d9, o9, "L09"), (d9b, o9b, "L09b")):
        x = load(V1 / "voz" / "c" / f"{i}.wav"); s = int(o * SR); a[s:s + len(x)] += x[:len(a) - s]
    raw = M / "_r.f32"; raw.write_bytes(a.tobytes())
    rv = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af",
                                       "aecho=0.8:0.55:45|95:0.20|0.10", "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)
    raw.unlink(); wav = M / "REZA.wav"; salvar(rv[:N], wav)
    P = [dict(p, ini=p["ini"] + o9, fim=p["fim"] + o9, linha="L09") for p in d9["palavras"]] + \
        [dict(p, ini=p["ini"] + o9b, fim=p["fim"] + o9b, linha="L09b") for p in d9b["palavras"]]
    board0 = 79.75 - T0v
    return dict(id="REZA", ag="padre", tipo="fixo", video=str(V1CORPO), audio=str(wav), v_off=T0v, uso=[0.0, T1v - T0v],
                palavras=P, texto="", ruins=[], abre_broll=(68.33 - T0v, ["hrez", "praia"]), board=(board0, T1v - T0v), oracao=True)


def item_v1(i, ag, ident):
    d = v1json(i); P = d["palavras"]
    return dict(id=ident, ag=ag, tipo="voz", video=None, audio=str(V1 / "voz" / "c" / f"{i}.wav"), v_off=0.0,
                uso=[max(0, P[0]["ini"] - 0.08), min(d["dur"], P[-1]["fim"] + 0.12)], palavras=P, texto=" ".join(p["w"] for p in P), ruins=[])


def item_seg():
    sys.path.insert(0, str(V1 / "voz")); from palavras import palavras
    P = palavras(AQ / "voz" / "SEG.alinhamento.json"); a = load(AQ / "voz" / "SEG.mp3")
    cortes = []
    for x, y in zip(P, P[1:]):          # pausa longa ("cambia… mira") -> 0,42 s
        g = y["ini"] - x["fim"]
        if g > 0.45: rem = g - 0.42; c0 = x["fim"] + 0.21; cortes.append((c0, c0 + rem))
    partes, t = [], 0.0
    for c0, c1 in cortes: partes.append(fade(a[int(t * SR):int(c0 * SR)].copy(), 8)); t = c1
    partes.append(a[int(t * SR):]); out = np.concatenate(partes)
    mapa = lambda tt: tt - sum(min(max(tt - c0, 0), c1 - c0) for c0, c1 in cortes)
    W = [dict(w=p["w"], ini=round(mapa(p["ini"]), 3), fim=round(mapa(p["fim"]), 3)) for p in P]
    wav = AQ / "voz" / "SEG.wav"; salvar(out[:int((W[-1]["fim"] + 0.2) * SR)], wav)
    return dict(id="SEG", ag="reportera", tipo="voz", video=None, audio=str(wav), v_off=0.0, uso=[max(0, W[0]["ini"] - 0.08), W[-1]["fim"] + 0.15],
                palavras=W, texto="Si tú también rezas y sientes que nada cambia… mira esto.", ruins=[])


def salvar(a, out):
    raw = Path(str(out) + ".f32"); raw.write_bytes(np.ascontiguousarray(a, np.float32).tobytes())
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-c:a", "pcm_s16le", out]); raw.unlink()


# ------------------------------------------------------------------ sequência
def classe_padre(it):
    t = " ".join(limpa(p["w"]) for p in it["palavras"]) or limpa(it["texto"])
    if re.search(r"\b(toca|ver más|pero atención|aquí abajo)\b", t): return "cta"
    if re.search(r"\bimagina\b", t): return "fut"
    if re.search(r"poderosísima|testimonios|escrita|918|novecientos|monjes|italia|congreso|497|cuatrocientos|secreto", t): return "prova"
    return "mec"


def sequencia(F):
    S = []
    react = F["react"]
    for it in react: S.append(dict(it, gap=0.0, post=True))
    S.append(dict(item_piloto(bool(react)), gap=0.0))
    for k, it in enumerate(F["aurelio"]): S.append(dict(it, gap=0.15 if k == 0 else 0.22, post=True))
    S.append(dict(item_v1("L07", "reportera", "CLARO"), gap=0.12))
    S.append(dict(item_seg(), gap=0.30))
    pad = {c: [it for it in F["padre"] if classe_padre(it) == c] for c in ("mec", "prova", "fut", "cta")}
    for k, it in enumerate(pad["mec"]): S.append(dict(it, gap=0.40 if k == 0 else 0.22, live=True))
    S.append(dict(item_reza(), gap=0.40, live=False))
    for k, it in enumerate(pad["prova"]): S.append(dict(it, gap=0.45 if k == 0 else 0.22, live=True))
    fut = pad["fut"] or [dict(item_v1("L11", "padre", "FUT"))]
    for k, it in enumerate(fut): S.append(dict(it, gap=0.40 if k == 0 else 0.22, live=True))
    for k, it in enumerate(pad["cta"]): S.append(dict(it, gap=0.40 if k == 0 else 0.22, live=True))
    for it in S:                                   # fora do corte enxuto
        P = it["palavras"]; k = achar(P, "fue increíble")
        if k is not None and k >= len(P) - 3 and k > 0:
            it["palavras"] = P[:k]; it["uso"] = [it["uso"][0], min(it["uso"][1], P[k - 1]["fim"] + 0.15)]; print(f"   [{it['id']}] cortado 'Fue increíble'")
    def sobra(it, lado):                           # s de vídeo do take antes/depois do trecho usado
        if it["id"] in ("PIL", "REZA"): return 0.0 if lado == "depois" else 99.0
        if it["tipo"] != "take": return 99.0
        if lado == "antes": return 0.06 if it.get("apara_ini") else it["uso"][0]
        return 0.06 if it.get("apara_fim") else max(0.0, it["dur"] - it["uso"][1])
    def abre_broll(it):                            # o item começa em b-roll? (então a pausa fica no b-roll, não na cauda do rosto)
        if it["tipo"] == "voz" or it.get("abre_broll"): return True
        if it["tipo"] != "take": return False
        C = coberturas(it); return bool(C) and C[0][0] <= it["uso"][0] + 0.15
    t = 0.0
    for k, it in enumerate(S):
        if k: it["gap"] = min(it["gap"], sobra(S[k - 1], "depois") + sobra(it, "antes"))
        t += it["gap"]; it["T0"] = round(t, 3); t += it["uso"][1] - it["uso"][0]; it["Tfala"] = round(t, 3)
    total = round(round((t + min(CAUDA, sobra(S[-1], "depois"))) * FPS) / FPS, 4)
    for k, it in enumerate(S):                    # fronteira visual: o anterior usa a própria sobra; o resto vem do lead do próximo
        it["V0"] = 0.0 if k == 0 else S[k - 1]["V1"]
        if k + 1 == len(S): it["V1"] = total
        elif it["tipo"] == "take" and abre_broll(S[k + 1]): it["V1"] = round(it["Tfala"] + min(0.04, S[k + 1]["gap"]), 4)
        else: it["V1"] = round(it["Tfala"] + min(S[k + 1]["gap"], sobra(it, "depois")), 4)
        it["Tend"] = it["V1"]
    return S, total


# ------------------------------------------------------------------ planos (vídeo)
def achar(P, frase, de=0):
    seq = frase.split()
    for k in range(de, len(P) - len(seq) + 1):
        if [limpa(P[k + j]["w"]) for j in range(len(seq))] == seq: return k
    return None


def coberturas(it):
    """[(a, b, [brolls])] em tempo do ARQUIVO de áudio do item"""
    P = it["palavras"]; u0, u1 = it["uso"]; C = []
    for r in REGRAS:
        if r["ag"] != it["ag"] or (r.get("so_take") and it["tipo"] != "take"): continue
        k = achar(P, r["kw"])
        if k is None: continue
        a = P[k]["ini"] - 0.08
        if r.get("recua") and it["tipo"] == "voz": a = u0       # frase começa antes da palavra-chave
        if r.get("recua_ate"):
            j = None
            for jj in range(k - 1, max(-1, k - 15), -1):
                if achar(P, r["recua_ate"], jj) == jj: j = jj; break
            if j is not None: a = P[j]["ini"] - 0.08
        b = u1
        for f in r.get("ate", []):
            j = achar(P, f, k + 1)
            if j is not None: b = min(b, P[j]["ini"] - 0.08)
        if r.get("dur"):
            nx = [p["ini"] - 0.08 for p in P if p["ini"] - 0.08 >= a + r["dur"]]
            b = min(b, nx[0] if nx else u1)
        if b - a > 0.35: C.append([max(u0, a), b, list(r["br"])])
    C.sort()
    for x, y in zip(C, C[1:]): x[1] = min(x[1], y[0])           # sem sobreposição
    C = [c for c in C if c[1] - c[0] > 0.35]
    if it["tipo"] == "voz":                                    # narração: b-roll do começo ao fim
        if not C: C = [[u0, u1, list(POOL.get(it["ag"], ["mont"]))]]
        C[0][0] = u0; C[-1][1] = u1
        for x, y in zip(C, C[1:]): x[1] = y[0]
    if it["tipo"] == "take":                                   # intervalos ruins indicados pelo agente
        ini_frase = [P[0]["ini"] - 0.08] + [y["ini"] - 0.08 for x, y in zip(P, P[1:]) if re.search(r"[.!?…:;]$", x["w"])]
        for r_ in it.get("ruins", []):
            a, b = r_[0], r_[1]; grave = r_[2] if len(r_) > 2 else True
            if any(c[0] <= a and b <= c[1] for c in C): continue
            enc = [c for c in C if a - 0.05 < c[0] <= b + 0.30 and c[1] >= b]   # cobertura que começa logo depois: puxa para trás
            if enc: enc[0][0] = max(u0, min(enc[0][0], a - 0.06)); continue
            enc = [c for c in C if c[0] <= a and a - 0.30 <= c[1] < b]           # cobertura que acaba logo antes: estica
            if enc: enc[0][1] = b + 0.04; continue
            if not grave: continue
            ws = [p for p in P if p["fim"] > a and p["ini"] < b]
            a2 = max(u0, min([a - 0.25] + [p["ini"] - 0.08 for p in ws]))
            fr = [f for f in ini_frase if f >= b - 0.02]; fr = fr[0] if fr else u1
            nx = [p["ini"] - 0.08 for p in P if p["ini"] - 0.08 >= max(b, a2 + 0.8)]; nx = nx[0] if nx else u1
            fr_ok = [f for f in ini_frase if f >= b - 0.02]
            b2 = fr if (fr_ok and a2 + 0.8 <= fr <= a2 + 2.7) else nx
            viz = [limpa(p["w"]) for p in P if a2 - 1.2 <= p["fim"] <= b + 0.1]
            pool = next((br for kw, br in COBRE_KW if kw in viz), None) or POOL.get(it["ag"], ["mont"])
            pool = [x for x in pool if not any(x in c[2] for c in C)] or pool
            C.append([max(u0, a2), min(u1, b2), pool]); print(f"   [{it['id']}] cobre ruim {a:.2f}-{b:.2f} -> {a2:.2f}-{b2:.2f} {pool}")
        C.sort()
        M_ = []
        for c in C:                                            # coberturas a menos de 1,2 s: junta (sem rosto picado entre elas)
            if M_ and it["tipo"] == "take" and 0.01 < c[0] - M_[-1][1] < 1.0 and c[2][0] not in CHAT and M_[-1][2][0] not in CHAT: M_[-1][1] = max(M_[-1][1], c[1]); M_[-1][2] += [x for x in c[2] if x not in M_[-1][2]]
            else: M_.append(c)
        C = M_
        C.sort()
        for x, y in zip(C, C[1:]):
            if x[1] > y[0]: x[1] = y[0]
    return C


def frases(it):
    """inícios de frase (tempo do arquivo) para o punch-in"""
    P = it["palavras"]; return [y["ini"] - 0.08 for x, y in zip(P, P[1:]) if re.search(r"[.!?…:;]$", x["w"])]


def planos(S, total):
    L = []; z_estado = [0]
    def add(t0, t1, **kw):
        if t1 - t0 > 1e-3: L.append(dict(t0=t0, t1=t1, **kw))
    for it in S:
        T0, Tend, u0, V0 = it["T0"], it["V1"], it["uso"][0], it["V0"]; ab = lambda x: T0 + (x - u0)
        if it["tipo"] == "fixo":
            cur = V0
            if it.get("abre_broll"):                    # oração: troca o padre antigo da v1 pelo b-roll
                d0 = T0 + it["abre_broll"][0]; broll_planos(L, it, V0, d0, it["abre_broll"][1]); cur = d0
            add(cur, Tend, src="video", file=it["video"], vt=u0 + (cur - T0) + it["v_off"], post=it.get("post", False), item=it["id"]); continue
        C = [(ab(a), ab(b), br) for a, b, br in coberturas(it)]
        C = [(V0 if a <= T0 + 1e-6 else a, Tend if abs(b - ab(it["uso"][1])) < 1e-6 or b > Tend else b, br) for a, b, br in C]
        cur = V0
        for a, b, br in C:
            if a > cur: take_plano(L, it, cur, a, z_estado)
            broll_planos(L, it, max(a, cur), b, br); cur = b
        if cur < Tend - 1e-3: take_plano(L, it, cur, Tend, z_estado)
    # funde planos curtos (< 0,4 s) no anterior (mesma fonte contínua quando possível)
    out = []
    for p in L:
        if out and p["t1"] - p["t0"] < 0.4:
            out[-1]["t1"] = p["t1"]; continue
        out.append(p)
    # quadros
    for p in out: p["q0"] = round(p["t0"] * FPS)
    for k, p in enumerate(out): p["n"] = (out[k + 1]["q0"] if k + 1 < len(out) else round(total * FPS)) - p["q0"]
    return [p for p in out if p["n"] > 0]


def take_plano(L, it, a, b, z):
    if it["tipo"] != "take":
        broll_planos(L, it, a, b, POOL.get(it["ag"], ["mont"])); return
    T0, u0 = it["T0"], it["uso"][0]; cortes = [a]
    if it.get("live"):
        for f in frases(it):
            t = T0 + (f - u0)
            if t - cortes[-1] >= 1.0 and b - t >= 1.0: cortes.append(t)
    cortes.append(b)
    for x, y in zip(cortes, cortes[1:]):
        zoom = 1.0
        if it.get("live"): zoom = ZOOM if z[0] % 2 else 1.0; z[0] += 1
        L.append(dict(t0=x, t1=y, src="video", file=it["video"], vt=u0 + (x - T0) + it["v_off"], zoom=zoom, item=it["id"],
                      post=it.get("post", False), live=it.get("live", False), modo=it.get("modo")))


def broll_planos(L, it, a, b, brs):
    D = b - a
    if brs and brs[0] in CHAT:
        L.append(dict(t0=a, t1=b, src="chat", file=str(CHAT[brs[0]]), item=it["id"], broll=brs[0])); return
    pecas = [x for x in brs if x in BR]; ext = [x for x in POOL.get(it["ag"], []) + POOL["padre"] if x not in pecas]
    while sum(BR[x][1] - BR[x][0] for x in pecas) / VEL_MIN < D and ext: pecas.append(ext.pop(0))
    avail = sum(BR[x][1] - BR[x][0] for x in pecas); vel = max(VEL_MIN, min(1.0, avail / D)); t = a
    for x in pecas:
        if t >= b - 1e-3: break
        s0, s1, fl = BR[x]; d = min((s1 - s0) / vel, b - t)
        if b - (t + d) < 0.4: d = b - t                       # sobra pequena: estica a peça atual
        L.append(dict(t0=t, t1=t + d, src="video", file=str(BASE), vt=s0, vel=min(1.0, (s1 - s0) / d) if d > (s1 - s0) else vel,
                      post=fl == "post", item=it["id"], broll=x)); t += d


# ------------------------------------------------------------------ render dos planos
def mascara_banda():
    p = GV / "banda.png"
    m = np.zeros((1280, 720), np.float32); y0, y1 = BANDA; f = 22
    m[:y0] = 1; m[y1:] = 1
    m[y0:y0 + f] = np.linspace(1, 0, f)[:, None]; m[y1 - f:y1] = np.linspace(0, 1, f)[:, None]
    Image.fromarray((m * 255).astype(np.uint8), "L").save(p); return p


def plate():
    p = GV / "plate.png"
    if not p.exists(): run(["ffmpeg", "-v", "error", "-y", "-ss", "20.0", "-i", BASE, "-frames:v", "1", p])
    return p


def tam(f, cache={}):
    if f not in cache:
        o = run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", f]).stdout.split(",")
        cache[f] = (int(o[0]), int(o[1]))
    return cache[f]


def render(p, out):
    n = p["n"]
    if p["src"] == "chat":
        fc = (f"[0:v]scale=1440:2560,zoompan=z='1+0.035*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30,"
              f"trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[v]")
        ins = ["-loop", "1", "-framerate", "30", "-t", f"{n / 30 + 0.3:.3f}", "-i", p["file"]]
    else:
        vel = p.get("vel", 1.0); w, h = tam(p["file"])
        ins = ["-ss", f"{max(0, p['vt']):.3f}", "-t", f"{n / 30 * vel + 0.4:.3f}", "-i", p["file"]]
        v = f"[0:v]setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS}"
        janela = (w, h) != (720, 1280) and (p.get("post") or p.get("modo") == "janela")
        if janela:
            ins += ["-loop", "1", "-framerate", "30", "-t", f"{n / 30 + 0.5:.3f}", "-i", plate()]
            v += f",scale={WIN[2]}:{WIN[3]}:force_original_aspect_ratio=increase:flags=lanczos,crop={WIN[2]}:{WIN[3]}[w];[1:v]fps={FPS}[pl];[pl][w]overlay={WIN[0]}:{WIN[1]}"
        elif (w, h) != (720, 1280):
            v += ",scale=720:1280:force_original_aspect_ratio=increase:flags=lanczos,crop=720:1280"
        z = p.get("zoom", 1.0)
        if z > 1.0 and not p.get("banda"):
            v += f",scale={int(720 * z) // 2 * 2}:{int(1280 * z) // 2 * 2}:flags=lanczos,crop=720:1280:{int(ZC[0] * (z - 1))}:{int(ZC[1] * (z - 1))}"
        elif z > 1.0:
            cw, ch = int(720 / z) // 2 * 2, int(1280 / z) // 2 * 2
            x0 = int(min(max(ZC[0] - ZC[0] / z, 0), 720 - cw)); y0 = int(min(max(ZC[1] - ZC[1] / z, 0), 1280 - ch))
            k = len(ins) // 6 if False else (2 if janela else 1)
            ins += ["-loop", "1", "-framerate", "30", "-t", f"{n / 30 + 0.5:.3f}", "-i", mascara_banda()]
            v += (f",format=yuv420p,split[o][zz];[zz]crop={cw}:{ch}:{x0}:{y0},scale=720:1280:flags=lanczos[zm];"
                  f"[{k}:v]fps={FPS},format=gray[mk];[o][mk]alphamerge[ob];[zm][ob]overlay=0:0:format=auto")
        fc = v + f",format=yuv420p,tpad=stop_mode=clone:stop=3,trim=end_frame={n},setpts=PTS-STARTPTS[v]"   # ≤3 quadros de folga (arredondamento 25->30 fps)
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-frames:v", n, "-r", FPS,
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", "-pix_fmt", "yuv420p", *TAG, "-an", out])
    k = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out]).stdout)
    if k != n: print(f"   !!! {out.name}: {k}/{n} quadros (fonte curta?) -> {p}"); sys.exit(1)


def corpo(PL):
    lista = []
    for k, p in enumerate(PL):
        out = M / f"p_{k:03d}.mp4"; render(p, out); lista.append(out)
        print(f"  [{k + 1}/{len(PL)}] {p['t0']:7.2f} {p['n']:4d}q {p.get('broll') or p['item']} z{p.get('zoom', 1.0)}", flush=True)
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in lista), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "corpo.mp4"])


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)); voz = np.zeros((N, 2), np.float32); amb = np.zeros((N, 2), np.float32)
    for it in S:
        u0, u1 = it["uso"]; a = load(it["audio"], u0, u1 - u0)
        if it["id"] != "PIL": a = fade(a)
        alvo = -15.0
        a *= 10 ** ((alvo - lufs(a)) / 20); s = int(it["T0"] * SR); n = min(len(a), N - s); voz[s:s + n] += a[:n]
    # ambiente de rua (demucs da cena original) sob react e Aurelio/¡Claro!
    def amb_trecho(t0, t1, ss, db):
        if t1 <= t0: return
        q = load(NV, ss, t1 - t0); q = fade(q, 80); q *= 10 ** ((db - lufs(q)) / 20); s = int(t0 * SR); n = min(len(q), N - s); amb[s:s + n] += q[:n]
    pil = next(it for it in S if it["id"] == "PIL")
    if pil["T0"] > 0: amb_trecho(0, pil["T0"] + 0.05, 0.3, -31)
    au = [it for it in S if it["ag"] == "aurelio" or it["id"] == "CLARO"]
    if au: amb_trecho(au[0]["T0"] - 0.1, au[-1]["Tend"] + 0.2, 25.33, -31)
    # trilha (demucs, música do trecho do padre) a -32 LUFS da segmentação até o fim
    seg = next(it for it in S if it["id"] == "SEG"); s0 = int((seg["T0"] - 0.3) * SR); need = N - s0
    bed = load(NV, 40.62)
    while len(bed) < need:
        x = load(NV, 45.0); cf = 2 * SR; w = np.linspace(0, 1, cf)[:, None]
        bed = np.concatenate([bed[:-cf], bed[-cf:] * (1 - w) + x[:cf] * w, x[cf:]])
    bed = bed[:need]; bed[:int(0.6 * SR)] *= np.linspace(0, 1, int(0.6 * SR))[:, None]
    bed *= 10 ** ((-32 - lufs(bed)) / 20); amb[s0:] += bed
    mix = voz + amb; mix[-int(1.0 * SR):] *= np.linspace(1, 0, int(1.0 * SR))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"])
    raw.unlink(); print("audio ok")


# ------------------------------------------------------------------ legenda + gigantes (ASS)
FS, Y, Y_BOARD, Y_CTA, Y_GIG = 64, 932, 1000, 840, 792
MAXP, MAXC = 3, 18
SUB = {"ígnes": "ignes", "véritas": "veritas", "siléntium": "silentium", "gládius": "gladius", "fortitúdo": "fortitudo",
       "custódia": "custodia", "sánctitas": "sanctitas", "spíritus": "spiritus", "triúmfus": "triumphus"}
JUNTAR = [(["novecientos", "dieciocho"], "918"), (["cuatrocientos", "noventa", "y", "siete"], "497"), (["doce"], "12"),
          (["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["ver", "más"], "ver más"), (["don", "aurelio"], "don aurelio")]


def palavras_tl(S):
    out = []
    for it in S:
        u0, u1 = it["uso"]
        for p in it["palavras"]:
            if p["ini"] < u0 - 0.05 or p["ini"] > u1: continue
            w = SUB.get(limpa(p["w"]), limpa(p["w"]))
            if not w: continue
            out.append(dict(w=w, raw=p["w"], ini=it["T0"] + p["ini"] - u0, fim=it["T0"] + p["fim"] - u0,
                            linha=f"{it['id']}:{p.get('linha', '')}", item=it["id"]))
    res, k = [], 0
    while k < len(out):
        for seq, rep in JUNTAR:
            if [x["w"] for x in out[k:k + len(seq)]] == seq and len({x["linha"] for x in out[k:k + len(seq)]}) == 1:
                res.append(dict(out[k], w=rep, fim=out[k + len(seq) - 1]["fim"], raw=out[k + len(seq) - 1]["raw"])); k += len(seq); break
        else: res.append(out[k]); k += 1
    return res


def blocos(W):
    B, cur = [], []
    for w in W:
        cand = cur + [w]; txt = " ".join(x["w"] for x in cand)
        if cur and (len(cand) > MAXP or len(txt) > MAXC or cur[-1]["linha"] != w["linha"] or w["ini"] - cur[-1]["fim"] > 0.6):
            B.append(cur); cand = [w]
        cur = cand
        if re.search(r"[.!?…:;]$", w["raw"]) or (w["raw"].endswith(",") and len(cur) >= 2): B.append(cur); cur = []
    if cur: B.append(cur)
    fix = []
    for b in B:
        if fix and len(b) == 1 and len(fix[-1]) < MAXP and fix[-1][-1]["linha"] == b[0]["linha"] and not re.search(r"[.!?…:;]$", fix[-1][-1]["raw"]) \
                and len(" ".join(x["w"] for x in fix[-1] + b)) <= MAXC and b[0]["ini"] - fix[-1][-1]["fim"] < 0.4:
            fix[-1] = fix[-1] + b
        else: fix.append(b)
    return fix


def ts(t): return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(S, PL, total, cta_t, board):
    W = palavras_tl(S); B = blocos(W); ev = []
    cortes = sorted({p["t0"] for p in PL})
    for i, b in enumerate(B):
        ini = b[0]["ini"] - 0.04; prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total)
        y = Y_CTA if ini >= cta_t - 0.1 else (Y_BOARD if board and board[0] - 0.05 <= ini < board[1] else Y)
        for j, w in enumerate(b):
            a = ini if j == 0 else w["ini"] - 0.04; e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + x["w"] for jj, x in enumerate(b))
            pop = r"\fscx85\fscy85\t(0,80,\fscx104\fscy104)\t(80,140,\fscx100\fscy100)" if j == 0 else ""
            ev.append(f"Dialogue: 1,{ts(a)},{ts(e)},L,,0,0,0,,{{\\an5\\pos(360,{y}){pop}}}{txt}")
    # palavras gigantes (primeira ocorrência de cada; "forma correcta" só depois da segmentação)
    Wl = [dict(p, w=limpa(p["raw"])) for p in W]; feitos = set(); seg_t = next(it["T0"] for it in S if it["id"] == "SEG")
    gig = []
    for frase, txt in GIGANTES:
        if txt in feitos: continue
        de = 0
        if "FORMA" in txt: de = next((k for k, p in enumerate(W) if p["ini"] >= seg_t + 3), 0)
        alvo = [p["w"] for p in W]; seq = frase.split(); k0 = None
        for k in range(de, len(W) - len(seq) + 1):
            if alvo[k:k + len(seq)] == seq or [x["w"] for x in Wl[k:k + len(seq)]] == seq: k0 = k; break
        if k0 is None: continue
        a = W[k0]["ini"] - 0.06; e = max(W[k0 + len(seq) - 1]["fim"] + 0.9, a + 1.4)
        fimf = next((it["Tfala"] for it in S if it["id"] == W[k0]["item"]), e); e = min(e, max(fimf + 0.3, a + 1.2)); feitos.add(txt); gig.append((a, e, txt))
        xg, yg = (575, 640) if any(p["src"] == "chat" and p["t0"] - 0.05 <= a < p["t1"] for p in PL) else (360, Y_GIG)   # print: ao lado do comprovante
        ev.append(f"Dialogue: 2,{ts(a)},{ts(e)},Gig,,0,0,0,,{{\\an5\\pos({xg},{yg})\\fscx55\\fscy55\\t(0,110,\\fscx112\\fscy112)\\t(110,190,\\fscx100\\fscy100)\\fad(0,120)}}{txt}")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins SemiBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,2,5,70,70,0,1
Style: Gig,Poppins ExtraBold,88,&H0054E5FE,&H0054E5FE,&H00100A05,&H96000000,0,0,0,0,100,100,1,0,1,7,4,5,20,20,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    (M / "leg.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    json.dump([dict(ini=round(b[0]["ini"], 3), texto=" ".join(x["w"] for x in b)) for b in B], open(M / "leg_blocos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    return W, gig


# ------------------------------------------------------------------ gráficos novos
def titulo_png():
    p = GV / "titulo.png"; W_, H_ = 720, 1280
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    F = lambda s: ImageFont.truetype(str(G / "Poppins-ExtraBold.ttf"), s)
    tams = []
    for t in TITULO:
        s = 70
        while d.textlength(t, font=F(s)) > 640 and s > 20: s -= 1
        tams.append(s)
    s = min(tams); lh = int(s * 1.12); h = lh * len(TITULO) + 28; y0 = 34
    box = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); ImageDraw.Draw(box).rounded_rectangle([4, y0, W_ - 4, max(y0 + h, 252)], 18, fill=(0, 0, 0, 240))
    sh = box.filter(ImageFilter.GaussianBlur(8)); im.alpha_composite(sh); im.alpha_composite(box)
    d = ImageDraw.Draw(im); cores = [(255, 255, 255, 255), (254, 229, 84, 255), (254, 229, 84, 255)]
    for k, t in enumerate(TITULO):
        d.text((W_ / 2, y0 + 14 + lh * k + lh / 2), t, font=F(s), fill=cores[k], anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    im.save(p); return p


# ------------------------------------------------------------------ vídeo final
def overlays(S, PL, total, cta_t, reza):
    L = []
    def junta(lst, png):
        for a, b in lst:
            if L and L[-1][0] == png and abs(L[-1][2] - a) < 1e-3: L[-1] = (png, L[-1][1], b, "0")
            else: L.append((png, a, b, "0"))
    q = lambda p: (p["q0"] / FPS, (p["q0"] + p["n"]) / FPS)
    junta([q(p) for p in PL if p.get("post")], "header.png")
    junta([q(p) for p in PL if p.get("live")], "live_v2.png")
    L.append(("titulo.png", 0.0, TITULO_T, "0"))
    if reza:
        T0 = reza["T0"]; b0, b1 = T0 + reza["board"][0], T0 + reza["board"][1]
        L.append(("board_titulo.png", b0, b1, "0"))
        PW = [p for p in reza["palavras"] if p.get("linha") == "L09b"]
        Wt = [T0 + p["ini"] for p in PW if limpa(p["w"]) != "y"]
        for k, w in enumerate(Wt):
            ini = w - 0.05; fim = (Wt[k + 1] - 0.05) if k + 1 < len(Wt) else b1
            for j in range(4):
                fa = ini + j / 30; fb = (ini + (j + 1) / 30) if j < 3 else fim
                L.append((f"circ_{k:02d}_{j}.png", fa, fb, "0"))
    if cta_t: L.append(("cta_txt.png", cta_t, total, "-22")); L.append(("cta_setas.png", cta_t, total, "-22+10*sin(2*PI*1.4*t)"))
    return L


def video(L, total):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    def caminho(p): return GV / p if (GV / p).exists() else G / p
    pngs = sorted(set(p for p, *_ in L)) + ["selo.png"]
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    for p in pngs: ins += ["-loop", "1", "-framerate", "30", "-t", f"{total + 1:.3f}", "-i", str(caminho(p))]
    idx = {p: i + 2 for i, p in enumerate(pngs)}; uso = {}
    for p, *_ in L: uso[p] = uso.get(p, 0) + 1
    uso["selo.png"] = 1; fc = []
    for p in pngs:
        n = uso[p]; lab = p.replace(".png", "")
        fc.append(f"[{idx[p]}:v]format=rgba" + ((f",split={n}" + "".join(f"[{lab}_{j}]" for j in range(n))) if n > 1 else f"[{lab}_0]"))
    cont = {}
    def ov(p, a, b, y, ult):
        lab = p.replace(".png", ""); j = cont.get(lab, 0); cont[lab] = j + 1
        if b >= total - 0.02: b = total + 5
        en = f":enable='gte(t,{a - 1 / 60:.4f})*lt(t,{b - 1 / 60:.4f})'" if (a > 0 or b < total) else ""
        out = f"[o{len(fc)}]"; fc.append(f"{ult}[{lab}_{j}]overlay=0:{y}:format=auto{en}{out}"); return out
    fc.append(f"[0:v]setpts=N/({FPS}*TB)[base]"); ult = "[base]"
    for p, a, b, y in L:
        if not p.startswith(("cta", "titulo")): ult = ov(p, a, b, y, ult)
    fc.append(f"{ult}ass=leg.ass:fontsdir=fonts[leg]"); ult = "[leg]"
    for p, a, b, y in L:
        if p.startswith(("cta", "titulo")): ult = ov(p, a, b, y, ult)
    ult = ov("selo.png", 0, total, "0", ult); fc.append(f"{ult}format=yuv420p[v]")
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS,
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{total:.2f} s")


# ------------------------------------------------------------------ narración.txt
def narracion(S, total):
    def mmss(t): return f"{int(t // 60):02d}:{int(t % 60):02d}"
    lin = []
    for it in S:
        u0 = it["uso"][0]; P = [p for p in it["palavras"] if u0 - 0.05 <= p["ini"] <= it["uso"][1]]
        grupos = []
        for p in P:
            ch = p.get("linha", "") if it["id"] in ("PIL", "REZA") else ""
            if not grupos or grupos[-1][0] != ch or (ch != "L09b" and re.search(r"[.!?…:]$", grupos[-1][1][-1]["w"])): grupos.append((ch, [p]))
            else: grupos[-1][1].append(p)
        for ch, g in grupos:
            if it["id"] == "PIL": rot = it["quem_linha"].get(ch, "?")
            else: rot = NOME.get(it["ag"], it["ag"]) + (" (oración)" if it.get("oracao") else "") + (" (voz en off)" if it["tipo"] == "voz" else "")
            fr = " ".join(p["w"] for p in g).replace("novecientos dieciocho", "918").replace("cuatrocientos noventa y siete", "497")
            if it.get("oracao") and "Crux" in fr: fr = "Crux, Lux, Fides, Ignes, Veritas, Silentium, Gladius, Fortitudo, Custodia, Sanctitas, Spiritus y Triumphus."
            lin.append(f"[{mmss(it['T0'] + g[0]['ini'] - u0)}] {rot}: {fr}")
    cab = f"""NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})
Tiempos = momento en que empieza cada frase en el video final.
Personajes ficticios: MUJER (react), AGRESOR, DON AURELIO (vendedor), REPORTERA y SACERDOTE (P. Andrés Molina). Sello "VIDEO FICTICIO" arriba a la derecha durante todo el video.
Voces (ElevenLabs): mujer Karly (sM4f2a6lmttmqTug8V7W) · agresor Richard (Cpm6N9BNC1M75bYS7kO1) · don Aurelio Santiago (VXZKNah1ssrzM8c81OiY) · reportera Gabriela (hHjbwzYZW17oh0p05AKv) · sacerdote Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu).
Versión v2 (enxuta): título de apertura, frase de segmentación nueva (reportera, voz en off), palabras gigantes y CTA corto. "(voz en off)" = narración sobre b-roll, sin rostro.
"""
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


if __name__ == "__main__":
    F = fontes.fontes("--ph" in ARGS)
    print("fontes:", {ag: ("REAL" if F[ag + "_real"] else "placeholder") + f" {len(F[ag])}" for ag in fontes.AGENTES})
    S, total = sequencia(F)
    PL = planos(S, total)
    W_all = palavras_tl(S)
    cta = next((it for it in S if it["ag"] == "padre" and it["tipo"] == "take" and classe_padre(it) == "cta"), None)
    cta_t = None
    if cta:
        k = achar(cta["palavras"], "toca"); cta_t = cta["T0"] + cta["palavras"][k]["ini"] - cta["uso"][0] - 0.1 if k is not None else None
    reza = next(it for it in S if it["id"] == "REZA"); board = (reza["T0"] + reza["board"][0], reza["T0"] + reza["board"][1])
    plano_js = dict(total=total, cta_t=cta_t, itens=[{k: it[k] for k in ("id", "ag", "tipo", "T0", "Tend", "uso", "texto")} for it in S],
                    planos=[{k: v for k, v in p.items()} for p in PL])
    json.dump(plano_js, open(AQ / "timeline_v2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for it in S: print(f"{it['T0']:7.2f}-{it['Tend']:7.2f} {it['id']:6s} {it['ag']:9s} {it['tipo']:5s} {it['texto'][:70]}")
    print("TOTAL", total, "CTA", cta_t)
    for p in PL: print(f"   {p['q0'] / 30:7.2f} +{p['n'] / 30:5.2f} {p.get('broll') or p['item']:8s} vt {p.get('vt', 0):6.2f} vel {p.get('vel', 1):.2f} z {p.get('zoom', 1)} {'POST' if p.get('post') else ''}{'LIVE' if p.get('live') else ''}")
    if "--so-plano" in ARGS: sys.exit()
    import ui_live; pt = next((it["video"] for it in S if it["ag"] == "padre" and it["tipo"] == "take"), None)
    if pt: ui_live.gerar(pt)
    titulo_png(); W, gig = legenda(S, PL, total, cta_t or total + 1, board)
    print("gigantes:", [(round(a, 2), t) for a, e, t in gig])
    if "--so-final" not in ARGS: corpo(PL); audio(S, total)
    video(overlays(S, PL, total, cta_t, reza), total)
    print(narracion(S, total))
