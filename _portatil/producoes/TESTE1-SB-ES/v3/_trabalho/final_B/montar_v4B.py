# -*- coding: utf-8 -*-
"""Montagem da v3 (narração fiel ao TESTE1, ROTEIRO_v3.md) -> v3/SB-ES_NOTICIA-AURELIO_v3_FICTICIO.mp4 (+ _narracion.txt, _frames.jpg).
Ordem = ROTEIRO_v3 (B01..P08). Sem título de abertura, sem segmentação, sem palavras gigantes (só setas TOCA «VER MÁS»).
- abertura/entrevista: moldura do post (plate + header) quando o take não é 720x1280;
- padre: SEMPRE com a moldura EN VIVO (live_v2.png), punch-in alternado 100/112 % por frase;
- V01..V09 / O01: b-roll da shotlist (cada plano UMA vez só; validação no fim), prints como imagem com zoom lento;
- intervalos_ruins dos takes: b-roll com 0,25 s de folga antes, cortes nas fronteiras de palavra;
- P06: insert do colar sobre "collar de plata"; setas de P07 até o fim;
- áudio: vozes a -15 LUFS, rua (demucs) sob react/entrevista, trilha triste no B04 -> esperança B05-B06, trilha demucs a -32 LUFS do P01 ao fim.
Uso: python montar_v3.py [--ph] [--so-plano] [--so-final] [--saida x.mp4]"""
import json, re, subprocess, sys, difflib, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
import fontes_v3 as fontes

AQ = Path(__file__).resolve().parent; V3T = AQ.parent; V3 = V3T.parent; RAIZ = V3.parent
V1 = RAIZ / "_trabalho"; V2T = RAIZ / "v2" / "_trabalho"
M = AQ / "mont"; M.mkdir(exist_ok=True); G = V1 / "graficos"; GV = AQ / "graficos"; GV.mkdir(exist_ok=True)
FPS, SR = 30, 48000
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
BASE = V1 / "lama" / "base_limpa.mp4"; NV = V1 / "audio" / "sep" / "htdemucs" / "orig" / "no_vocals.wav"
V1CORPO = V1 / "mont" / "corpo.mp4"
ARGS = sys.argv[1:]
OUT = Path(ARGS[ARGS.index("--saida") + 1]) if "--saida" in ARGS else RAIZ / "v4" / "SB-ES_NOTICIA-AURELIO_B-ORACION-COMPLETA_FICTICIO.mp4"
WIN = (0, 297, 720, 840)          # janela do vídeo dentro da moldura do post
ZOOM = 1.12; ZC = (360, 560)      # punch-in do padre
CAUDA = 0.8; VEL_MIN = 0.80; FOLGA = 0.25
E19_FIX = AQ / "e19fix" / "e19_cuadro_12_palabras_fix.mp4"; BRIGA_CAUDA = V3T / "abertura_v2" / "takes" / "seedance_violenta.mp4"
TRILHA_TRISTE = AQ / "trilha" / "triste_1.mp3"; TRILHA_ESP = AQ / "trilha" / "esperanca_1.mp3"

ORDEM = ["B01", "B02", "B03", "B04", "B05", "B06", "R01", "A01", "AV01", "A01B", "A02", "A03", "R02",
         "PB01", "P01", "V01", "P02", "O01", "P03B", "V02", "V03", "V04", "V05", "P04B", "V06", "V08", "P05B", "V07", "P07B"]   # v4-B
ABERTURA_REP = AQ / "abertura" / "react_reporter_B.mp4"; REP_PAL = V3T / "v4_reporter_pip" / "audio" / "palavras.json"   # r2: REPORTERA em PiP desde 0:00
TX_R00 = "Imágenes impactantes: un vendedor fue atacado en plena calle."
ABERTURA_B = AQ / "abertura" / "react_briga_B.mp4"; OFF_B01 = 0.90          # punch-in 130 % + mulher depois do impacto (abertura/abertura_B.py)
TITULO = ("titulo_gancho.png", 0.0, 3.0)                                       # título do gancho 0-3 s (titulo.py)
FORA_B = {"e06_sb_grimorio", "s19_colar_altar_terciopelo", "s20_colar_manos_rezando", "s16_rosario_manos"}   # livro GRIMORIO / colar / medalha
EXTRA = []          # itens novos (voz A01B, fase 2) -> extras()
FORCAR = {}         # bloco -> [ids de b-roll] (cobertura de voz off sem b-roll próprio)
CTA_BLOCO = "P07B"
COBRE_FIX = {"PB01": [(1.04, 3.42)]}   # PB01: rosto em "No es mala suerte." e "hay algo espiritual detrás."; b-roll só nas 2 pausas com dentes
SPLIT = {"P05": [(6.645, 6.855)], "A01": [(0.48, 0.68)], "A02": [(4.29, 4.41)]}   # r2: B01 sem emenda (abertura violenta = take único)
SPLIT_ZOOM = {"A01", "A02"}       # partes alternam 100/112 % dentro da janela do post (esconde o corte seco)
RUINS_REV = {"A03": ["fim"], "R01": ["fim"], "P07B": ["fim"], "P04B": ["fim"], "P01": [(0.0, 0.20)], "P02": [(0.0, 0.12)], "P03": [(0.0, 0.35)],
             "A02": [(0.0, 0.30)]}
BR_AJUSTE = {"e03_sb_escribiendo": (1 / 30, 0), "e06_sb_grimorio": (1 / 30, 0), "e13_mujer_negra_rezando": (0, 0.07), "e07_pergamino": (0.3, 0)}   # (corta início, corta fim)   # pausa com boca aberta retirada no corte (sem b-roll livre para cobrir)
GAP = dict(B04=0.0, B05=0.0, B06=0.0, R01=0.0, A01=0.25, AV01=0.30, A01B=0.30, A02=0.30, A03=0.22, R02=0.12, PB01=0.40, P01=0.35, O01=0.35, P03B=0.40)
NOME = {"AV01": "DON AURELIO (voz en off)", "A01B": "DON AURELIO (voz en off)", "B01": "REPORTERA (en PiP)", "B02": "AGRESOR", "B03": "DON AURELIO", "R01": "REPORTERA", "R02": "REPORTERA",
        "A": "DON AURELIO", "P": "SACERDOTE (EN VIVO)", "V": "SACERDOTE (voz en off)", "O": "SACERDOTE (oración, voz en off)"}


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:2500]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + (["-t", f"{t:.3f}"] if t else []) + \
          ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < int(0.5 * SR): a = np.concatenate([a, np.zeros((int(0.5 * SR) - len(a), 2), np.float32)])
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    raw.unlink(); l = [x for x in r.stderr.splitlines() if x.strip().startswith("I:")]
    v = float(l[-1].split()[1]); return v if v > -70 else -70.0


def fade(a, ms=12):
    n = min(int(ms / 1000 * SR), len(a) // 2)
    if n: a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a


def salvar(a, out):
    raw = Path(str(out) + ".f32"); raw.write_bytes(np.ascontiguousarray(a, np.float32).tobytes())
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-c:a", "pcm_s16le", out]); raw.unlink()


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def tam(f, cache={}):
    if f not in cache:
        if str(f).lower().endswith((".png", ".jpg", ".jpeg", ".webp")): cache[f] = Image.open(f).size
        else:
            o = run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", f]).stdout.strip().split(",")
            cache[f] = (int(o[0]), int(o[1]))
    return cache[f]


# ------------------------------------------------------------------ roteiro (texto exato da legenda)
def roteiro():
    T = {}
    for l in (AQ / "ROTEIRO_B.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Z]{1,2}\d\d[A-Z]?)\b[^\"]*\"(.+)\"\s*$", l.strip())
        if m: T[m.group(1)] = m.group(2)
    if ABERTURA_REP.exists(): T["B01"] = TX_R00
    return T


def texto_roteiro(P, txt):
    """troca as palavras do manifest pelas do roteiro (mesma contagem -> 1:1; senão alinhamento difflib) mantendo os tempos"""
    if not P or not txt: return P
    R = txt.split()
    if len(R) == len(P): return [dict(p, w=r) for p, r in zip(P, R)]
    a = [limpa(p["w"]) for p in P]; b = [limpa(r) for r in R]; out = []
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal": out += [dict(P[i1 + k], w=R[j1 + k]) for k in range(i2 - i1)]
        elif j2 > j1 and i2 > i1:              # bloco trocado: distribui o texto do roteiro no tempo das palavras do manifest
            t0, t1 = P[i1]["ini"], P[i2 - 1]["fim"]; n = j2 - j1; L = [len(limpa(R[j])) + 1 for j in range(j1, j2)]; s = sum(L); t = t0
            for k, j in enumerate(range(j1, j2)): d = (t1 - t0) * L[k] / s; out.append(dict(w=R[j], ini=round(t, 3), fim=round(t + d, 3))); t += d
        elif j2 > j1:                           # palavra do roteiro sem tempo: encosta na anterior
            t = out[-1]["fim"] if out else P[0]["ini"]
            for j in range(j1, j2): out.append(dict(w=R[j], ini=t, fim=t + 0.01))
    return out


# ------------------------------------------------------------------ itens especiais
def v1json(i): return json.loads((V1 / "voz" / "c" / f"{i}.json").read_text(encoding="utf-8"))


def item_reza():
    """O01: oração exatamente como v1/v2 (L09 + L09b com reverb). Visual: b-roll O01 da shotlist e o quadro das 12 palavras (v1)."""
    T0v, T1v = 66.22, 90.90; d9, d9b = v1json("L09"), v1json("L09b"); o9, o9b = 66.24 - T0v, 82.44 - T0v
    N = int((T1v - T0v) * SR); a = np.zeros((N + SR, 2), np.float32)
    for o, i in ((o9, "L09"), (o9b, "L09b")):
        x = load(V1 / "voz" / "c" / f"{i}.wav"); s = int(o * SR); a[s:s + len(x)] += x[:len(a) - s]
    raw = M / "_r.f32"; raw.write_bytes(a.tobytes())
    rv = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af",
                                       "aecho=0.8:0.55:45|95:0.20|0.10", "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)
    raw.unlink(); wav = M / "REZA.wav"; salvar(rv[:N], wav)
    P = [dict(p, ini=p["ini"] + o9, fim=p["fim"] + o9, linha="L09") for p in d9["palavras"]] + \
        [dict(p, ini=p["ini"] + o9b, fim=p["fim"] + o9b, linha="L09b") for p in d9b["palavras"]]
    return dict(id="REZA", bloco="O01", blocos=["O01"], ag="padre", tipo="voz", video=None, audio=str(wav), v_off=0.0, uso=[0.0, T1v - T0v],
                palavras=P, texto="", ruins=[], dur=T1v - T0v, board=(79.75 - T0v, T1v - T0v), board_vt=79.75, oracao=True, extra={})


# ------------------------------------------------------------------ sequência
def fronteiras(P, u0, u1):
    """instantes de corte permitidos (entre palavras) no tempo do arquivo"""
    F = [max(u0, P[0]["ini"] - 0.08)] if P else [u0]
    for x, y in zip(P, P[1:]):
        g = y["ini"] - x["fim"]; F.append(y["ini"] - 0.08 if g > 0.16 else (x["fim"] + y["ini"]) / 2)
    F.append(u1); return sorted(set(round(f, 3) for f in F if u0 - 1e-6 <= f <= u1 + 1e-6))


def sequencia(F, TX):
    pool = EXTRA + F["abertura"] + F["entrevista"] + F["padre"]; usados = set(); S = []
    for b in ORDEM:
        if any(b in it["blocos"] for it in S): continue
        if b == "O01": S.append(item_reza()); continue
        cand = [it for it in pool if b in it["blocos"] and id(it) not in usados and it["tipo"] in ("take", "voz", "mudo")]
        cand.sort(key=lambda it: (it["blocos"].index(b) != 0, not it.get("v4"), it["tipo"] != "take", it["ordem"]))
        if not cand: print(f"   !!! bloco {b} sem item (pulado)"); continue
        it = dict(cand[0]); usados.add(id(cand[0]))
        txt = " ".join(TX.get(x, "") for x in it["blocos"]).strip()
        if txt and it["palavras"] and not it.get("oracao"): it["palavras"] = texto_roteiro(it["palavras"], txt)
        # ajustes da revisão (quadro 0 com dentes / cauda com boca aberta / mão sobre a medalha)
        P = it["palavras"]
        for r_ in RUINS_REV.get(b, []):
            it["ruins"] = it["ruins"] + [[P[-1]["fim"] + 0.03, it["dur"], True] if r_ == "fim" else list(r_) + [True]]
        # intervalo ruim encostado na borda do trecho usado -> apara o trecho
        R = []
        for r_ in it["ruins"]:
            a, bb = r_[0], r_[1]
            if P and a <= it["uso"][0] + 0.08 and bb <= P[0]["ini"] + 0.02: it["uso"][0] = max(it["uso"][0], bb); it["apara_ini"] = True
            elif P and a <= it["uso"][0] + 0.08 and bb <= P[0]["ini"] + 0.40 and b[0] == "P": it["vmin"] = bb          # quadro 0 ruim: imagem só a partir de bb
            elif P and bb >= it["uso"][1] - 0.08 and a >= P[-1]["fim"] - 0.02: it["uso"][1] = min(it["uso"][1], max(a, P[-1]["fim"] + 0.04)); it["apara_fim"] = True
            else: R.append(r_)
        it["ruins"] = R
        it["post"] = it["ag"] in ("abertura", "entrevista"); it["live"] = it["ag"] == "padre" and it["tipo"] == "take"
        cortes_ = SPLIT.get(b, [])
        if not cortes_: S.append(it); continue
        for k, c in enumerate(cortes_ + [None]):          # pausa ruim retirada (corte seco com troca de zoom)
            parte = dict(it); u = list(it["uso"])
            if k > 0: u[0] = cortes_[k - 1][1]; parte["apara_ini"] = True; parte["gap_fix"] = 0.0; parte["sobra0"] = True; parte.pop("vmin", None)
            if c is not None: u[1] = c[0]; parte["apara_fim"] = True
            if b in SPLIT_ZOOM: parte["zoom_post"] = ZOOM if k % 2 else 1.0
            parte["uso"] = u; parte["ruins"] = [r for r in it["ruins"] if r[0] >= u[0] - 0.01 and r[1] <= u[1] + 0.01]; parte["id"] = f"{it['id']}{'abc'[k]}"
            S.append(parte)
    def sobra(it, lado):
        if it["tipo"] == "voz": return 99.0
        if it["tipo"] == "mudo": return 0.0
        if it.get("sobra0") or (lado == "depois" and it.get("apara_fim") and SPLIT.get(it["bloco"])): return 0.0
        if lado == "antes": return 0.04 if it.get("apara_ini") else (it["uso"][0] - it["vmin"] if "vmin" in it else it["uso"][0] + it["v_off"])
        return 0.04 if it.get("apara_fim") else max(0.0, it["dur"] - it["uso"][1] - it["v_off"])
    t = 0.0
    for k, it in enumerate(S):
        g = it.get("gap_fix", GAP.get(it["bloco"], 0.22)) if k else 0.0
        if k and S[k - 1]["tipo"] != "voz" and it["tipo"] != "voz": g = min(g, sobra(S[k - 1], "depois") + sobra(it, "antes"))
        it["gap"] = g; t += g; it["T0"] = round(t, 3); t += it["uso"][1] - it["uso"][0]; it["Tfala"] = round(t, 3)
    total = round(round((t + min(CAUDA, sobra(S[-1], "depois"))) * FPS) / FPS, 4)
    for k, it in enumerate(S):
        it["V0"] = 0.0 if k == 0 else S[k - 1]["V1"]
        if k + 1 == len(S): it["V1"] = total
        else:
            nx = S[k + 1]
            if it["tipo"] == "voz": it["V1"] = round(it["Tfala"] + (nx["gap"] - min(nx["gap"], sobra(nx, "antes")) if nx["tipo"] != "voz" else nx["gap"] / 2), 4)
            else: it["V1"] = round(it["Tfala"] + min(nx["gap"], sobra(it, "depois")), 4)
    for k, it in enumerate(S): it["prev_tipo"] = S[k - 1]["tipo"] if k else None
    return S, total


def S_prev_take(it): return it.get("prev_tipo") in ("take", "mudo")


# ------------------------------------------------------------------ b-roll (cada plano uma vez só)
class Banco:
    def __init__(self, L): self.L = L; self.usados = []
    def livres(self, bloco, papel=None):
        ok = lambda x: x["id"] not in [u["id"] for u in self.usados]
        dono = [x for x in self.L if ok(x) and bloco in x["blocos"] and (papel is None or papel in x["papel"] or papel in x["desc"].lower() or papel in x["id"].lower())]
        return dono
    def reserva(self):
        return [x for x in self.L if x["id"] not in [u["id"] for u in self.usados] and not x["blocos"]]
    def pegar(self, x, onde): self.usados.append(dict(id=x["id"], onde=onde)); return x


def distribuir(BK, bloco, a, b, cortes, onde, forcar=None):
    """cobre [a,b] (tempo final) com planos do bloco (ou reserva); cortes = fronteiras de palavra permitidas (tempo final)"""
    D = b - a; pecas = list(forcar or BK.livres(bloco))
    if not pecas:
        R = sorted(BK.reserva(), key=lambda x: x["dur"]); ok = [x for x in R if x["dur"] / VEL_MIN >= D]
        pecas = ok[:1] or R[-1:]
    if not pecas: print(f"   !!! sem b-roll livre para {bloco} {a:.2f}-{b:.2f}"); return []
    # quantas peças: todas as do bloco se couberem com >= 1,0 s cada; senão o mínimo que cobre com vel >= 0,8
    n = max(1, min(len(pecas), int(D // 1.0)))
    while sum(p["dur"] for p in pecas[:n]) / VEL_MIN < D and n < len(pecas): n += 1
    pecas = pecas[:n]
    extra = [x for x in BK.reserva() if x["id"] not in [p["id"] for p in pecas]]
    while sum(p["dur"] for p in pecas) / VEL_MIN < D and extra:
        x = extra.pop(0); pecas.append(x)
    # pontos de corte: proporcionais à duração de cada peça, encaixados na fronteira de palavra mais próxima
    tot = sum(p["dur"] for p in pecas); alvo = []; acc = 0.0
    for p in pecas[:-1]: acc += p["dur"]; alvo.append(a + D * acc / tot)
    cs = [a]
    for x in alvo:
        cand = [c for c in cortes if cs[-1] + 0.7 <= c <= b - 0.7]
        cs.append(min(cand, key=lambda c: abs(c - x)) if cand else x)
    cs.append(b); out = []
    for p, t0, t1 in zip(pecas, cs, cs[1:]):
        if t1 - t0 < 0.05: continue
        d = t1 - t0; vel = 1.0 if p["tipo"] == "img" else min(1.0, p["dur"] / d)
        if vel < VEL_MIN - 1e-3: print(f"   aviso: {p['id']} esticado vel {vel:.2f} em {onde}")
        BK.pegar(p, onde); out.append(dict(t0=t0, t1=t1, src="img" if p["tipo"] == "img" else "video", file=p["file"], vt=p["ss"], vel=max(vel, 0.5),
                                           broll=p["id"], item=onde, post=False))
    return out


def cronometrados(BK, bloco):
    return sorted([x for x in BK.livres(bloco) if x.get("tb")], key=lambda x: (x["tb"][0], x["ordem"]))


def timed(BK, bloco, it, a, b, cortes, off=0.0, ancorar=True):
    """planos com tempo do agente de b-roll (t_bloco relativo ao áudio do bloco) -> tempo final; cortes internos encaixados
    na fronteira de palavra mais próxima (<= 0,2 s); ancorar = 1º começa em a e último termina em b"""
    L = cronometrados(BK, bloco)
    if not L: return []
    T0, u0 = it["T0"], it["uso"][0]; tt = [[T0 + x["tb"][0] + off - u0, T0 + x["tb"][1] + off - u0] for x in L]
    if ancorar: tt[0][0] = a; tt[-1][1] = b
    for k in range(1, len(tt)):
        c = tt[k][0]; cand = [f for f in cortes if abs(f - c) <= 0.2]
        if cand and not L[k]["id"].startswith("e19"): c = min(cand, key=lambda f: abs(f - c))
        tt[k][0] = c; tt[k - 1][1] = c
    out = []
    for x, (t0, t1) in zip(L, tt):
        t0, t1 = max(t0, a), min(t1, b)
        if t1 - t0 < 0.05: continue
        d = t1 - t0; vel = 1.0 if x["tipo"] == "img" else min(1.0, x["dur"] / d); quadro = "cuadro" in x["id"] or "12_palabras" in x["id"]
        if quadro: vel = 1.0
        elif vel < VEL_MIN - 1e-3: print(f"   aviso: {x['id']} esticado vel {vel:.2f} em {bloco}")
        BK.pegar(x, bloco); out.append(dict(t0=t0, t1=t1, src="img" if x["tipo"] == "img" else "video", file=x["file"], vt=x["ss"], vel=max(vel, 0.5),
                                         broll=x["id"], item=bloco, post=False, congela=quadro))
    return out


def coberturas(it):
    """[(a, b, papel)] em tempo do ARQUIVO para cobrir intervalos ruins (grave) de um take"""
    if it["bloco"] in COBRE_FIX: return [list(x) for x in COBRE_FIX[it["bloco"]]]
    P = it["palavras"]; u0, u1 = it["uso"]; F = fronteiras(P, u0, u1); C = []
    for a, b, grave in it["ruins"]:
        if not grave or b <= u0 or a >= u1: continue
        a2 = max([f for f in F if f <= a - FOLGA] or [u0]); b2 = min([f for f in F if f >= b] or [u1])
        while b2 - a2 < 0.8:
            nx = [f for f in F if f > b2]
            if not nx: break
            b2 = nx[0]
        v_ini = it.get("vmin", u0)
        if a2 - v_ini < 0.7: a2 = u0                      # rosto por menos de 0,7 s antes da cobertura: começa já no b-roll
        if u1 - b2 < 0.7: b2 = u1
        C.append([a2, b2])
    C.sort(); M_ = []
    for c in C:
        if M_ and c[0] - M_[-1][1] < 2.2: M_[-1][1] = max(M_[-1][1], c[1])
        else: M_.append(c)
    return M_


def frases(it):
    P = it["palavras"]; return [y["ini"] - 0.08 for x, y in zip(P, P[1:]) if re.search(r"[.!?…:;,]$", x["w"])]


def planos(S, total, BK):
    L = []; z = [0]
    for it in S:
        T0, u0, V0, V1_ = it["T0"], it["uso"][0], it["V0"], it["V1"]; ab = lambda x: T0 + (x - u0)
        Pw = [dict(p, ini=ab(p["ini"]), fim=ab(p["fim"])) for p in it["palavras"]]
        cortes = fronteiras(Pw, V0, V1_)
        if it["tipo"] == "voz":
            if cronometrados(BK, it["bloco"]):
                L += timed(BK, it["bloco"], it, V0, V1_, cortes, off=0.02 if it.get("oracao") else 0.0)
                if it.get("oracao") and any("cuadro" in x["broll"] or "12_palabras" in x["broll"] for x in L if x.get("broll")): it["board_burn"] = True
            elif it.get("oracao"):
                b0 = T0 + it["board"][0]
                L += distribuir(BK, "O01", V0, b0, cortes, it["bloco"])
                L.append(dict(t0=b0, t1=V1_, src="video", file=str(V1CORPO), vt=it["board_vt"], item="O01", broll="quadro_12_palabras(v1)", post=False))
            else:
                fz = [x for i_ in FORCAR.get(it["bloco"], []) for x in BK.L if x["id"] == i_ and x["id"] not in [u["id"] for u in BK.usados]]
                got = distribuir(BK, it["bloco"], V0, V1_, cortes, it["bloco"], forcar=fz or None)
                if it["ag"] == "entrevista":
                    for g in got: g["post"] = True
                L += got
            continue
        if it["tipo"] == "mudo":
            L.append(dict(t0=V0, t1=V1_, src="video", file=it["video"], vt=it["v_off"] + u0 - (T0 - V0), item=it["bloco"], post=True,
                          crop_post=it["extra"].get("crop_post", False), broll=None)); continue
        # take: coberturas de intervalos ruins + insert do colar (P06)
        C = [(ab(a), ab(b), None) for a, b in coberturas(it)]
        if it["bloco"] == "P06" and INS_P06:
            p06(L, it, Pw, cortes, BK, z); continue
        if it["bloco"] == "P06" and cronometrados(BK, "P06"):
            cs_ = cronometrados(BK, "P06"); a_ = min(T0 + x["tb"][0] - u0 for x in cs_); b_ = max(T0 + x["tb"][1] - u0 for x in cs_)
            C.append((min(cortes, key=lambda f: abs(f - a_)), min(cortes, key=lambda f: abs(f - b_)), "colar_t"))
        elif it["bloco"] == "P06":
            k = next((j for j, p in enumerate(Pw) if limpa(p["w"]) == "collar"), None)
            if k is not None:
                a = max([f for f in cortes if f <= Pw[k]["ini"] - 0.05] or [V0]); bnx = [f for f in cortes if f >= a + 1.6]
                C.append((a, bnx[0] if bnx else min(V1_, a + 1.8), "colar"))
            else: print("   !!! P06 sem a palavra 'collar'")
        C.sort(); cur = V0
        if "vmin" in it:
            cur = max(V0, ab(it["vmin"]))
            if cur - V0 > 0.02 and S_prev_take(it) and not (L and L[-1].get("broll")):            # r2: sem preto -> segura o último quadro do plano anterior até o 1º quadro bom
                L[-1]["congela"] = True; L[-1]["t1"] = cur
            if cur - V0 > 0.02: VIS0[it["bloco"]] = cur
        for a, b, papel in C:
            a = max(a, cur); b = min(b, V1_)
            if a - cur < 0.3: a = cur
            if V1_ - b < 0.3: b = V1_
            if b - a < 0.3: continue
            if a > cur: take_planos(L, it, cur, a, z)
            if papel == "colar_t":
                L += timed(BK, "P06", it, a, b, cortes, ancorar=True)
            elif papel == "colar":
                ins = BK.livres("P06", "colar") or BK.livres("P06")
                L += distribuir(BK, "P06", a, b, cortes, "P06-insert", forcar=ins[:1]) if ins else []
                if not ins: print("   !!! sem insert do colar na shotlist"); take_planos(L, it, a, b, z)
            else:
                got = distribuir(BK, it["bloco"], a, b, cortes, it["bloco"] + "-cobre")
                for g in got: g["post"] = it["post"]
                if got: L += got
                else: take_planos(L, it, a, b, z)
            cur = b
        if cur < V1_ - 1e-3: take_planos(L, it, cur, V1_, z)
    out = []
    for p in L:                                      # funde planos curtos (< 0,3 s) no anterior se for a mesma fonte
        if out and p["t1"] - p["t0"] < 0.3 and out[-1]["file"] == p["file"] and out[-1].get("broll") == p.get("broll"):
            out[-1]["t1"] = p["t1"]; continue
        out.append(p)
    for p in out: p["q0"] = round(p["t0"] * FPS)
    for k, p in enumerate(out): p["n"] = (out[k + 1]["q0"] if k + 1 < len(out) else round(total * FPS)) - p["q0"]
    return [p for p in out if p["n"] > 0]


VIS0 = {}          # r2: bloco -> 1º instante em que o rosto aparece (legenda não entra antes)
INS_P06 = None     # insert do padre (mãos com a medalha) entregue pelo agente do padre


def p06(L, it, Pw, cortes, BK, z):
    """P06: insert das mãos do padre (moldura EN VIVO) em "Y quien obtenga el Grimorio" -> padre com o colar nas mãos
    em "hoy recibirá de" -> insert s19 (colar no altar) "regalo un collar de plata de San Benito," -> s20 (colar nas mãos)
    "el mismo que se usaba en sus oraciones." (cobre as falhas do colar 0,16-1,36 / 3,1-3,4 / 5,3-5,5 / 7,3-7,5 e as bocas abertas)"""
    V0, V1_ = it["V0"], it["V1"]; W = [limpa(p["w"]) for p in Pw]
    def antes(k): return max([f for f in cortes if f <= Pw[k]["ini"] - 0.02] or [V0])
    k_hoy = W.index("hoy"); k_reg = W.index("regalo"); k_el = next(j for j in range(k_reg, len(W)) if W[j] == "el")
    a1, a2, a3 = antes(k_hoy), antes(k_reg), antes(k_el)
    ins = INS_P06
    L.append(dict(t0=V0, t1=a2, src="video", file=ins["video"], vt=0.3, vel=1.0, item="P06", broll="insert_P06_colar_kling(padre)",
                  live=True, zoom=1.0, post=False))
    for nome, t0, t1 in (("s19", a2, a3), ("s20", a3, V1_)):
        x = next((q for q in BK.livres("P06") if q["id"].startswith(nome)), None) or (BK.livres("P06") or BK.reserva())[0]
        L += distribuir(BK, "P06", t0, t1, cortes, "P06-insert", forcar=[x])


def take_planos(L, it, a, b, z):
    T0, u0 = it["T0"], it["uso"][0]; cs = [a]
    if it.get("live"):
        for f in frases(it):
            t = T0 + (f - u0)
            if t - cs[-1] >= 1.0 and b - t >= 1.0: cs.append(t)
    cs.append(b)
    for x, y in zip(cs, cs[1:]):
        zoom = 1.0
        if it.get("live"): zoom = ZOOM if z[0] % 2 else 1.0; z[0] += 1
        elif it.get("zoom_post"): zoom = it["zoom_post"]
        L.append(dict(t0=x, t1=y, src="video", file=it["video"], vt=u0 + (x - T0) + it["v_off"], zoom=zoom, item=it["bloco"],
                      post=it.get("post", False), live=it.get("live", False), full=it["extra"].get("full", False), broll=None))


# ------------------------------------------------------------------ render
def plate():
    p = GV / "plate.png"
    if not p.exists(): run(["ffmpeg", "-v", "error", "-y", "-ss", "20.0", "-i", BASE, "-frames:v", "1", p])
    return p


def render(p, out):
    n = p["n"]
    if p["src"] == "preto":
        fc = f"color=c=black:s=720x1280:r={FPS},trim=end_frame={n},format=yuv420p[v]"; ins = []
    elif p["src"] == "img":
        w, h = tam(p["file"]); sc = "scale=1440:2560:force_original_aspect_ratio=increase,crop=1440:2560" if (w, h) != (720, 1280) else "scale=1440:2560"
        fc = (f"[0:v]{sc},zoompan=z='1+0.035*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30,"
              f"trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[v]")
        ins = ["-loop", "1", "-framerate", "30", "-t", f"{n / 30 + 0.3:.3f}", "-i", p["file"]]
    else:
        vel = p.get("vel", 1.0); w, h = tam(p["file"])
        ins = ["-ss", f"{max(0, p['vt']):.3f}", "-t", f"{n / 30 * vel + 0.4:.3f}", "-i", p["file"]]
        v = f"[0:v]setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS}"
        if p.get("crop_post"): v += f",crop={WIN[2]}:{WIN[3]}:{WIN[0]}:{WIN[1]}"; w, h = WIN[2], WIN[3]
        janela = p.get("post") and not p.get("full") and ((w, h) != (720, 1280) or p.get("broll"))
        if janela:
            ins += ["-loop", "1", "-framerate", "30", "-t", f"{n / 30 + 0.5:.3f}", "-i", plate()]
            zw = p.get("zoom", 1.0); zs = ""
            if zw > 1.0: zs = f",scale={int(WIN[2] * zw) // 2 * 2}:{int(WIN[3] * zw) // 2 * 2}:flags=lanczos,crop={WIN[2]}:{WIN[3]}:{int(WIN[2] / 2 * (zw - 1))}:{int(WIN[3] * 0.4 * (zw - 1))}"
            v += f",scale={WIN[2]}:{WIN[3]}:force_original_aspect_ratio=increase:flags=lanczos,crop={WIN[2]}:{WIN[3]}{zs}[w];[1:v]fps={FPS}[pl];[pl][w]overlay={WIN[0]}:{WIN[1]}"
            p["janela"] = True; p["zoom_janela"] = zw
        elif (w, h) != (720, 1280):
            v += ",scale=720:1280:force_original_aspect_ratio=increase:flags=lanczos,crop=720:1280"
        zz = p.get("zoom", 1.0)
        if zz > 1.0 and not janela:
            v += f",scale={int(720 * zz) // 2 * 2}:{int(1280 * zz) // 2 * 2}:flags=lanczos,crop=720:1280:{int(ZC[0] * (zz - 1))}:{int(ZC[1] * (zz - 1))}"
        fc = v + f",format=yuv420p,tpad=stop_mode=clone:stop={-1 if p.get('congela') else 3},trim=end_frame={n},setpts=PTS-STARTPTS[v]"
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-frames:v", n, "-r", FPS,
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", "-pix_fmt", "yuv420p", *TAG, "-an", out])
    k = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out]).stdout)
    if k != n: print(f"   !!! {out.name}: {k}/{n} quadros (fonte curta?) -> {p}"); sys.exit(1)


def corpo(PL):
    lista = []
    for f in M.glob("p_*.mp4"): f.unlink()
    for k, p in enumerate(PL):
        out = M / f"p_{k:03d}.mp4"; render(p, out); lista.append(out)
        print(f"  [{k + 1}/{len(PL)}] {p['t0']:7.2f} {p['n']:4d}q {p.get('broll') or p['item']} z{p.get('zoom', 1.0)}", flush=True)
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in lista), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "corpo.mp4"])


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)); voz = np.zeros((N, 2), np.float32); amb = np.zeros((N, 2), np.float32)
    for it in S:
        if not it.get("audio") or it["tipo"] == "mudo": continue
        u0, u1 = it["uso"]; a = fade(load(it["audio"], u0, u1 - u0))
        a *= 10 ** ((-15.0 - lufs(a)) / 20); s = int(it["T0"] * SR); n = min(len(a), N - s); voz[s:s + n] += a[:n]
    def pos(a, t0, db=None, fd=80):
        a = fade(a, fd)
        if db is not None: a *= 10 ** ((db - lufs(a)) / 20)
        s = int(t0 * SR); n = min(len(a), N - s); amb[s:s + n] += a[:n]
    by = {b: it for it in S for b in it["blocos"]}
    # trilha triste (B04) -> esperança (B05-B06), ponte para a reportera
    if "B04" in by:
        t4 = by["B04"]["V0"]; t5 = by["B05"]["V0"] if "B05" in by else t4 + 3.0; tR = by["R01"]["T0"] if "R01" in by else t5 + 6
        tri = load(TRILHA_TRISTE); tri *= 10 ** ((-19 - lufs(tri)) / 20)
        nt = min(len(tri), int((t5 - t4 + 0.9) * SR)); tri = tri[:nt].copy(); xf = int(0.9 * SR)
        tri[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]; tri[-xf:] *= np.linspace(1, 0, xf)[:, None]
        pos(tri, t4, None, 1)
        es = load(TRILHA_ESP); es *= 10 ** ((-20 - lufs(es)) / 20)
        ne = min(len(es), int((tR + 2.2 - t5) * SR)); es = es[:ne].copy()
        es[:xf] *= np.linspace(0, 1, xf)[:, None]
        env = np.ones(ne, np.float32); i0 = int((tR - 0.3 - t5) * SR)
        if 0 < i0 < ne: env[i0:] = np.linspace(1, 10 ** (-12 / 20), ne - i0)          # abaixa sob a reportera e some
        es *= env[:, None]; es[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))[:, None]
        pos(es, t5 - 0.0, None, 1)
    # rua (demucs da cena original) sob a entrevista
    ent = [it for it in S if it["ag"] == "entrevista"]
    if ent: t0, t1 = ent[0]["T0"] - 0.1, ent[-1]["V1"] + 0.2; pos(load(NV, 25.33, t1 - t0), t0, -31)
    # trilha (demucs, música do trecho do padre) a -32 LUFS do P01 até o fim
    p1 = next((it for it in S if it["ag"] == "padre"), None)
    if p1:
        s0 = int((p1["V0"] - 0.2) * SR); need = N - s0; bed = load(NV, 40.62)
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


# ------------------------------------------------------------------ legenda (estilo v1)
FS, Y, Y_BOARD, Y_CTA, Y_POST = 64, 932, 1000, 840, 1072
MAXP, MAXC = 3, 18
SUB = {"ígnes": "ignes", "véritas": "veritas", "siléntium": "silentium", "gládius": "gladius", "fortitúdo": "fortitudo",
       "custódia": "custodia", "sánctitas": "sanctitas", "spíritus": "spiritus", "triúmfus": "triumphus"}
JUNTAR = [(["doce"], "12"), (["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["don", "aurelio"], "don aurelio")]


def palavras_tl(S):
    out = []
    for it in S:
        u0, u1 = it["uso"]
        for p in it["palavras"]:
            if p["ini"] < u0 - 0.05 or p["ini"] > u1: continue
            w = SUB.get(limpa(p["w"]), limpa(p["w"]))
            if not w: continue
            out.append(dict(w=w, raw=p["w"], ini=it["T0"] + p["ini"] - u0, fim=it["T0"] + p["fim"] - u0,
                            linha=f"{it['bloco']}:{p.get('linha', '')}", item=it["bloco"]))
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


def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(S, total, cta_t, board):
    W = palavras_tl(S); B = blocos(W); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, VIS0.get(b[0].get("item"), 0.0), 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total)
        y = Y_CTA if ini >= cta_t - 0.1 else (Y_BOARD if board and board[0] - 0.05 <= ini < board[1] else (Y_POST if b[0]["item"][0] in "BRA" else Y))
        for j, w in enumerate(b):
            a = ini if j == 0 else max(ini, w["ini"] - 0.04); e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + x["w"] for jj, x in enumerate(b))
            pop = r"\fscx85\fscy85\t(0,80,\fscx104\fscy104)\t(80,140,\fscx100\fscy100)" if j == 0 else ""
            ev.append(f"Dialogue: 1,{ts(a)},{ts(e)},L,,0,0,0,,{{\\an5\\pos(360,{y}){pop}}}{txt}")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins SemiBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,2,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    (M / "leg.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    json.dump([dict(ini=round(b[0]["ini"], 3), texto=" ".join(x["w"] for x in b)) for b in B], open(M / "leg_blocos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    return W


# ------------------------------------------------------------------ vídeo final
def eh_janela(p):
    if p["src"] != "video" or not p.get("post") or p.get("full"): return False
    w, h = (WIN[2], WIN[3]) if p.get("crop_post") else tam(p["file"])
    return (w, h) != (720, 1280) or bool(p.get("broll"))


def overlays(S, PL, total, cta_t, reza):
    L = []
    for p in PL: p["janela"] = eh_janela(p)
    def junta(lst, png):
        for a, b in lst:
            if L and L[-1][0] == png and abs(L[-1][2] - a) < 1e-3: L[-1] = (png, L[-1][1], b, "0")
            else: L.append((png, a, b, "0"))
    q = lambda p: (p["q0"] / FPS, (p["q0"] + p["n"]) / FPS)
    junta([q(p) for p in PL if p.get("janela") or (p.get("post") and p.get("full"))], "header.png")
    junta([q(p) for p in PL if p.get("live")], "live_v2.png")
    if reza and not reza.get("board_burn"):
        T0 = reza["T0"]; b0, b1 = T0 + reza["board"][0], reza["V1"]
        L.append(("board_titulo.png", b0, b1, "0"))
        PW = [p for p in reza["palavras"] if p.get("linha") == "L09b"]
        Wt = [T0 + p["ini"] for p in PW if limpa(p["w"]) != "y"]
        for k, w in enumerate(Wt):
            ini = w - 0.05; fim = (Wt[k + 1] - 0.05) if k + 1 < len(Wt) else b1
            for j in range(4):
                fa = ini + j / 30; fb = (ini + (j + 1) / 30) if j < 3 else fim
                L.append((f"circ_{k:02d}_{j}.png", fa, fb, "0"))
    L.insert(0, TITULO + ("0",))
    if cta_t is not None: L.append(("cta_txt.png", cta_t, total, "-22")); L.append(("cta_setas.png", cta_t, total, "-37+10*sin(2*PI*1.4*t)"))   # r2: setas 15 px mais altas
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
        if not p.startswith("cta"): ult = ov(p, a, b, y, ult)
    fc.append(f"{ult}ass=leg.ass:fontsdir=fonts[leg]"); ult = "[leg]"
    for p, a, b, y in L:
        if p.startswith("cta"): ult = ov(p, a, b, y, ult)
    ult = ov("selo.png", 0, total, "0", ult); fc.append(f"{ult}format=yuv420p[v]")
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS,
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{total:.2f} s")


def folha(total):
    n = 30; fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    for k in range(n):
        t = (k + 0.5) * total / n
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=360:640", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", f"tile={n}x1", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


def narracion(S, total):
    def mmss(t): return f"{int(t // 60):02d}:{int(t % 60):02d}"
    TX = roteiro(); lin = []
    for it in S:
        for b in it["blocos"]:
            if b not in TX: continue
            P = [p for p in it["palavras"] if limpa(p["w"])]
            t = it["T0"] + (P[0]["ini"] - it["uso"][0] if P else 0)
            if len(it["blocos"]) > 1 and P:                       # bloco dentro de item múltiplo: procura a 1ª palavra do bloco
                w2 = [limpa(x) for x in TX[b].split()[:2]]          # r2: casa as 2 primeiras palavras ("no" aparecia antes no B01)
                k = next((j for j in range(len(P) - 1) if [limpa(P[j]["w"]), limpa(P[j + 1]["w"])] == w2), None)
                if k is not None: t = it["T0"] + P[k]["ini"] - it["uso"][0]
            if any(f"] {b} " in x for x in lin): continue          # item dividido (SPLIT): 1 linha só
            rot = NOME.get(b) or NOME.get(b[0], b)
            lin.append(f"[{mmss(t)}] {b} {rot}: {TX[b]}")
    cab = f"""NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})
Tiempos = momento en que empieza cada frase en el video final. Texto = ROTEIRO_B (versión B: Oración de San Benito Completa -> VSL).
Personajes ficticios: REPORTERA (en PiP desde 0:00 y luego en la calle), AGRESOR, DON AURELIO (vendedor) y SACERDOTE (P. Andrés Molina, siempre dentro de la transmisión EN VIVO).
Sello "VIDEO FICTICIO" arriba a la derecha durante todo el video. "(voz en off)" = narración sobre b-roll, sin rostro.
Voces (ElevenLabs): agresor Richard · don Aurelio Santiago · reportera Gabriela · sacerdote Pa Gabriel.
B04–B06 sin voz (carrito vacío con música triste -> clientes llegando -> fila llena). Título 0–3 s: "LO HUMILLARON EN PLENA CALLE… AL DÍA SIGUIENTE PASÓ ESTO".
CTA único al final (flechas TOCA «VER MÁS» desde P07B hasta el final); nada se dice después del CTA.
"""
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


def antirepeticao(PL, BK):
    """cada plano de b-roll 1x; e nenhum trecho de fonte usado 2x (sobreposição > 0,1 s no mesmo arquivo)"""
    prob = []; ids = {}
    for p in PL:
        if p.get("broll"): ids.setdefault(p["broll"], []).append(round(p["t0"], 2))
    for k, v in ids.items():
        if len(v) > 1: prob.append(f"plano {k} usado {len(v)}x em {v}")
    rng = {}
    for p in PL:
        if p["src"] == "preto": continue
        if p["src"] == "img": a, b = 0, 1
        else: a = p["vt"]; b = a + p["n"] / FPS * p.get("vel", 1.0)
        rng.setdefault(p["file"], []).append((a, b, round(p["t0"], 2)))
    for f, R in rng.items():
        R.sort()
        for x, y in zip(R, R[1:]):
            if y[0] < x[1] - 0.1: prob.append(f"trecho repetido de {Path(f).name}: {x[0]:.2f}-{x[1]:.2f} (em {x[2]}) x {y[0]:.2f}-{y[1]:.2f} (em {y[2]})")
    return ids, prob


# ------------------------------------------------------------------ v4-B: itens novos
V4A = V3T / "v4_assets"


def item_voz(id_, bloco, wav, palavras, ag, texto, extra=None):
    d = fontes.dur(wav)
    return dict(id=id_, bloco=bloco, blocos=[bloco], ag=ag, tipo="voz", video=None, audio=str(wav), v_off=0.0,
                uso=[max(0.0, palavras[0]["ini"] - 0.08), min(d, palavras[-1]["fim"] + 0.15)], palavras=palavras, texto=texto,
                ruins=[], dur=d, ordem=0, extra=extra or {}, v4=True)


def extras(F):
    TX = roteiro()
    # abertura: punch-in + mulher depois do impacto (mesma duração 9,2 s; só a fala B01 anda OFF_B01 s)
    for it in F["abertura"]:
        if it["bloco"] == "B01" and it["tipo"] == "take" and ABERTURA_REP.exists():          # r2: reportera fala desde 0:00 (v4_reporter_pip)
            it["video"] = it["audio"] = str(ABERTURA_REP)
            it["palavras"] = json.loads(REP_PAL.read_text(encoding="utf-8")) + [p for p in it["palavras"] if p["ini"] >= 3.5]
        elif it["bloco"] == "B01" and it["tipo"] == "take" and ABERTURA_B.exists():
            it["video"] = it["audio"] = str(ABERTURA_B)
            it["palavras"] = [dict(p, ini=p["ini"] + OFF_B01, fim=p["fim"] + OFF_B01) if p["ini"] < 3.5 else p for p in it["palavras"]]
    # A01: só "Sí, eso me pasó a mí." no rosto (o resto da fala original citava o Grimorio)
    for it in F["entrevista"]:
        if it["bloco"] == "A01":
            P = it["palavras"]; k = next(j for j, p in enumerate(P) if p["w"].lower().startswith("pero"))
            corte = round((P[k - 1]["fim"] + P[k]["ini"]) / 2, 3)
            it["palavras"] = P[:k]; it["uso"] = [it["uso"][0], corte]; it["ruins"] = [r for r in it["ruins"] if r[0] < corte]
            it["texto"] = TX["A01"]
    # A01B: voz nova (ElevenLabs Santiago, parâmetros do L05) -> voz off sobre b-roll inédito
    vz = AQ / "voz" / "A01B.json"
    if vz.exists():
        j = json.loads(vz.read_text(encoding="utf-8"))
        EXTRA.append(item_voz("A01B_tts", "A01B", AQ / "voz" / "A01B.wav", j["palavras"], "entrevista", TX["A01B"]))
    FORCAR.setdefault("A01B", ["k13_vela_encendiendo", "s24_hombre_rezando_vela"])     # provisório (fase 1); fase 2 troca pelos b-rolls novos
    fase2(F)


def fase2(F):
    """fase 2: v4_assets/manifest.json (falas novas AV01/PB01/P03B/P04B/P05B/P07B + b-rolls de substituição)"""
    mf = V4A / "manifest.json"
    if not mf.exists(): print("   (fase 2: v4_assets/manifest.json ainda não existe)"); return
    raw = json.loads(mf.read_text(encoding="utf-8")); TX = roteiro(); n_ = 0
    L, _ = fontes.carregar("v4", V4A)                              # parser genérico (tempos, ruins, uso)
    por_id = {x["extra"].get("id"): x for x in L}
    for it in raw["itens"]:
        if it.get("tipo") == "broll":
            if it.get("versao") and "B" not in str(it["versao"]): continue
            f = V4A / it["arquivo"]; ss = float(it.get("in", 0.0)); d = float(it.get("out", it.get("duracao"))) - ss
            bl = [it["bloco"]] if it["bloco"] in ORDEM else []
            F["broll"].append(dict(id=Path(it["arquivo"]).stem, file=str(f), ss=ss, dur=d, blocos=bl, desc=it.get("descricao", "")[:120],
                                   tipo="video", papel="", tb=None, ordem=100 + n_, vel=1.0, extra=it)); n_ += 1
            continue
        x = por_id.get(it["id"])
        if x is None or it["bloco"] not in ORDEM: continue
        x = dict(x, bloco=it["bloco"], blocos=[it["bloco"]], v4=True, texto=TX.get(it["bloco"], x["texto"]))
        x["ag"] = "entrevista" if it["bloco"].startswith("A") else "padre"
        EXTRA.append(x)
    # b-roll por bloco (v4-B): n03 recortado sem a capa "Holy Bible" (broll_B/), coberturas temáticas dos takes novos
    F["broll"] = [x for x in F["broll"] if x["id"] != "n03_manos_abren_biblia"]
    F["broll"].append(dict(id="n03_biblia_manos_840", file=str(AQ / "broll_B" / "n03_biblia_manos_840.mp4"), ss=0.0, dur=5.0, blocos=[],
                           desc="manos ancianas pasando páginas (recorte sin la tapa en inglés)", tipo="video", papel="", tb=None, ordem=200, vel=1.0, extra={}))
    BL = {"n05_pareja_rezando_mesa": ["PB01"], "n02_iglesia_vacia_amanecer": ["P04B"], "n04_agua_bendita": ["P05B"], "k12_abuela_alegria": ["P07B"]}
    for x in F["broll"]:
        if x["id"] in BL: x["blocos"] = BL[x["id"]]
    for x in F["broll"]:
        if x["id"] == "n01_aurelio_cierra_carrito": x["dur"] = 2.5          # toldo some de forma abrupta em ~2,5-3,0 s
    n06 = AQ / "broll_B" / "n06_persianas_cerradas.mp4"
    if n06.exists():
        F["broll"].append(dict(id=n06.stem, file=str(n06), ss=0.0, dur=fontes.dur(n06), blocos=[], desc="hombre de espaldas ante persianas de metal cerradas",
                               tipo="video", papel="", tb=None, ordem=201, vel=1.0, extra={}))
    k14 = next((x for x in F["broll"] if x["id"] == "k14_amanecer_valle"), None)      # revisor: São Bento do e04 usa medalha em corrente
    for x in F["broll"]:
        if x["id"] == "e04_sb_acantilado" and k14:
            x.update(id="k14_amanecer_valle(no lugar do e04)", file=k14["file"], ss=0.0, dur=k14["dur"]); F["broll"].remove(k14); break
    FORCAR["AV01"] = ["s15_calendario_7_dias", "n01_aurelio_cierra_carrito", "n06_persianas_cerradas"]
    FORCAR["A01B"] = ["n03_biblia_manos_840", "k13_vela_encendiendo", "s24_hombre_rezando_vela"]
    print("   fase 2:", [x["bloco"] + ":" + x["tipo"] for x in EXTRA], "| b-roll novo:", [x["id"] for x in F["broll"] if x["ordem"] >= 100])


if __name__ == "__main__":
    F = fontes.fontes("--ph" in ARGS)
    print("fontes:", {ag: ("REAL" if F[ag + "_real"] else "placeholder") + f" {len(F[ag])}" for ag in fontes.AGENTES})
    INS_P06 = None                                              # v4-B: sem P06 / sem colar
    F["broll"] = [x for x in F["broll"] if x["id"] not in FORA_B]
    extras(F)
    for x in F["broll"]:
        if x["id"] in BR_AJUSTE: c0, c1 = BR_AJUSTE[x["id"]]; x["ss"] += c0; x["dur"] -= c0 + c1
        if x["id"].startswith("e19") and E19_FIX.exists(): x["file"] = str(E19_FIX)          # r2: placas "Crux"/"Silentium"
    # r2: cutaway do R01 ("atacado por un cliente") = cauda sem fala do take da briga (9,2 s em diante), no lugar da vela k13
    if BRIGA_CAUDA.exists():
        pass                                                                          # v4-B: vela k13 volta como reserva (cobre voz off)
        F["broll"].append(dict(id="briga_cauda_R01", file=str(BRIGA_CAUDA), ss=9.2, dur=0.84, blocos=["R01"], desc="carrinho destruído depois do ataque",
                               tipo="video", papel="", tb=None, ordem=-1, vel=1.0, extra={}))
    TX = roteiro(); S, total = sequencia(F, TX); BK = Banco(F["broll"])
    PL = planos(S, total, BK)
    p7 = next((it for it in S if it["bloco"] == CTA_BLOCO), None)         or ([it for it in S if it.get("live")] or [None])[-1]
    cta_t = (p7["V0"]) if p7 else None
    if p7:                                                      # r2: cta no quadro real do corte para o P07
        q7 = [p for p in PL if p["item"] == p7["bloco"] and p["src"] != "preto"]
        if q7: cta_t = round(min(p["q0"] for p in q7) / FPS, 4)
    reza = next((it for it in S if it.get("oracao")), None); board = (reza["T0"] + reza["board"][0], reza["V1"]) if reza else None
    qb = [p for p in PL if p.get("broll") and ("cuadro" in p["broll"] or "12_palabras" in p["broll"])]
    if qb: board = (qb[0]["t0"], qb[0]["t1"])
    ids, prob = antirepeticao(PL, BK)
    js = dict(total=total, cta_t=cta_t, itens=[{k: it.get(k) for k in ("id", "bloco", "blocos", "ag", "tipo", "T0", "V0", "V1", "uso", "texto", "video", "audio")} for it in S],
              planos=PL, broll_usados=BK.usados, broll_nao_usados=[x["id"] for x in BK.L if x["id"] not in ids], repeticoes=prob)
    json.dump(js, open(AQ / "timeline_B.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for it in S: print(f"{it['V0']:7.2f}-{it['V1']:7.2f} {it['bloco']} {it['id']:14s} {it['tipo']:5s} {' '.join(p['w'] for p in it['palavras'])[:70]}")
    print("TOTAL", total, "CTA", cta_t)
    for p in PL: print(f"   {p['q0'] / 30:7.2f} +{p['n'] / 30:5.2f} {str(p.get('broll') or p['item']):26s} vt {p.get('vt', 0):6.2f} vel {p.get('vel', 1):.2f} z {p.get('zoom', 1)} {'POST' if p.get('post') else ''}{'LIVE' if p.get('live') else ''}")
    print("REPETIÇÕES:", prob or "nenhuma"); print("b-roll não usado:", js["broll_nao_usados"])
    if "--so-plano" in ARGS: sys.exit()
    import ui_live; pt = next((it["video"] for it in S if it["ag"] == "padre" and it["tipo"] == "take"), None)
    if pt: ui_live.gerar(pt)
    legenda(S, total, cta_t if cta_t is not None else total + 1, board)
    if "--so-final" not in ARGS: corpo(PL); audio(S, total)
    video(overlays(S, PL, total, cta_t, reza), total)
    print(narracion(S, total)); folha(total)
