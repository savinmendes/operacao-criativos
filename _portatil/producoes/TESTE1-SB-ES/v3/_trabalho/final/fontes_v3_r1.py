# -*- coding: utf-8 -*-
"""Fontes da montagem v3: lê os manifest.json dos 4 agentes (abertura / entrevista / padre / broll) e normaliza
cada item para {bloco, blocos, ag, tipo: take|voz|mudo, video, audio, v_off, uso, palavras, texto, ruins, dur, extra}
(tempos em s no ARQUIVO de áudio; tempo de vídeo = tempo de áudio + v_off).
Sem manifest real -> placeholder em memória feito da v1/v2 (só para testar a pipeline). Não escreve nas pastas dos agentes."""
import json, re, subprocess, sys
from pathlib import Path
AQ = Path(__file__).resolve().parent; V3T = AQ.parent; RAIZ = V3T.parent.parent
V1 = RAIZ / "_trabalho"; V2T = RAIZ / "v2" / "_trabalho"
AGENTES = ("abertura", "entrevista", "padre", "broll")
BASE = V1 / "lama" / "base_limpa.mp4"; G = V1 / "graficos"
RX = re.compile(r"\b([BRAPVO])(\d{1,2})\b")


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(" ".join(map(str, c))[:800]); print(r.stderr[-1500:]); sys.exit(1)
    return r


def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout.strip())
def tem_video(p): return bool(run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=codec_type", "-of", "csv=p=0", p]).stdout.strip())
def tem_audio(p): return bool(run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "csv=p=0", p]).stdout.strip())


def _g(d, *ks, default=None):
    for k in ks:
        if isinstance(d, dict) and k in d and d[k] is not None: return d[k]
    return default


def blocos_de(x):
    """'B01-B03' / ['B02','B03'] / 'P6' -> ['B01','B02','B03']"""
    s = " ".join(map(str, x)) if isinstance(x, (list, tuple)) else str(x or "")
    s = s.upper(); out = []
    for m in re.finditer(r"\b([BRAPVO])(\d{1,2})\s*[-–a]\s*([BRAPVO])?(\d{1,2})\b", s):
        for n in range(int(m.group(2)), int(m.group(4)) + 1): out.append(f"{m.group(1)}{n:02d}")
    for m in RX.finditer(s): out.append(f"{m.group(1)}{int(m.group(2)):02d}")
    res = []
    for b in out:
        if b not in res: res.append(b)
    return res


def _palavras(lst):
    out = []
    for p in lst or []:
        if isinstance(p, (list, tuple)): w, a, b = p[0], p[1], p[2]
        else: w = _g(p, "w", "word", "palavra", "text", "texto"); a = _g(p, "ini", "start", "inicio", "s"); b = _g(p, "fim", "end", "e")
        if w is None or a is None or b is None: continue
        out.append(dict(w=str(w).strip(), ini=float(a), fim=float(b)))
    return [p for p in out if p["w"]]


def _intervalos(lst):
    out = []
    for x in lst or []:
        if isinstance(x, dict): a = _g(x, "ini", "start", "de", "a"); b = _g(x, "fim", "end", "ate", "b"); g = x.get("grave", "(leve)" not in str(x.get("motivo", "")).lower())
        else: a, b, g = x[0], x[1], True
        if a is not None and b is not None and float(b) > float(a): out.append([float(a), float(b), bool(g)])
    return out


def _itens(raw):
    if isinstance(raw, list): return raw
    for k in ("itens", "items", "takes", "clips", "planos", "shots", "shotlist", "falas", "trechos"):
        if isinstance(raw.get(k), list):
            L = list(raw[k]); break
    else:
        L = [dict(v, id=v.get("id", k)) for k, v in raw.items() if isinstance(v, dict) and any(x in v for x in ("arquivo", "file", "video"))]
    for k2 in ("narracoes", "narrações", "vozes", "audios", "audio_separado", "voz_off", "vo", "insertos", "inserts"):
        v = raw.get(k2)
        if isinstance(v, dict): v = [v]
        if isinstance(v, list): L += [dict(x, _grupo=k2) for x in v if isinstance(x, dict)]
    return L


def carregar(ag, pasta):
    pasta = Path(pasta); raw = json.loads((pasta / "manifest.json").read_text(encoding="utf-8")); res = []
    for n, it in enumerate(_itens(raw)):
        arq = _g(it, "arquivo", "file", "video", "mp4", "path", "saida", "wav", "audio")
        if not arq or not isinstance(arq, str): continue
        arq = Path(arq); arq = arq if arq.is_absolute() else pasta / arq
        if not arq.exists(): print(f"[{ag}] AVISO: arquivo não existe: {arq}"); continue
        aud = _g(it, "audio_arquivo", "audio_wav", "wav", "audio")
        aud = Path(aud) if isinstance(aud, str) and re.search(r"\.(wav|mp3|m4a|aac|flac)$", aud, re.I) else None
        if aud is not None and not aud.is_absolute(): aud = pasta / aud
        if aud is not None and not aud.exists(): aud = None
        ehv = arq.suffix.lower() in (".mp4", ".mov", ".mkv", ".webm") and tem_video(arq)
        tp = str(_g(it, "tipo", "type", "kind", default="")).lower()
        if aud is None and ehv and tem_audio(arq): aud = arq
        if not ehv: aud = arq
        if ehv and (tp.startswith(("mudo", "broll", "b-roll", "insert", "sem")) or aud is None): tipo = "mudo"
        elif ehv: tipo = "take"
        else: tipo = "voz"
        bl = blocos_de(_g(it, "blocos", "bloco", "bloco_roteiro", "roteiro", "id_roteiro", default="")) or blocos_de(_g(it, "id", "nome", default="")) \
            or blocos_de(arq.stem)
        d = dur(arq if ehv else aud)
        P = _palavras(_g(it, "palavras", "words", "tempos", "tempos_palavras", "word_timings", "alinhamento", "palavras_whisper_small_no_arquivo_final"))
        R = _intervalos(_g(it, "intervalos_ruins", "ruins", "cobrir", "bad", "cobrir_broll"))
        uso = _g(it, "uso_s", "trecho_uso", "uso")
        if isinstance(uso, list) and len(uso) == 2 and all(isinstance(x, (int, float)) for x in uso): uso = [float(uso[0]), float(uso[1])]
        elif P:
            fimw = float(_g(it, "fim_ultima_palavra_s", default=P[-1]["fim"]))
            uso = [max(0.0, P[0]["ini"] - (0.10 if tipo == "take" else 0.08)), min(d, fimw + (0.30 if ag == "abertura" else 0.25 if tipo == "take" else 0.15))]
        else: uso = [0.0, d]
        res.append(dict(id=str(_g(it, "id", "nome", default=f"{ag}{n}")), bloco=bl[0] if bl else None, blocos=bl, ag=ag, tipo=tipo,
                        video=str(arq) if ehv else None, audio=str(aud) if aud else None, v_off=float(_g(it, "v_off", default=0.0)),
                        uso=uso, palavras=P, texto=str(_g(it, "texto", "text", "fala", default=" ".join(p["w"] for p in P))),
                        ruins=R, dur=d, ordem=n, extra=it))
    return res, raw


# ---------------------------------------------------------------- shotlist do b-roll
def shotlist(pasta):
    """lista de planos {id, file, ss, dur, blocos, desc, tipo: video|img, papel}"""
    pasta = Path(pasta)
    mf = pasta / "shotlist.json" if (pasta / "shotlist.json").exists() else pasta / "manifest.json"
    raw = json.loads(mf.read_text(encoding="utf-8")); out = []
    L = _itens(raw) if isinstance(raw, (dict, list)) else []
    for n, it in enumerate(L):
        arq = _g(it, "arquivo", "file", "video", "path", "imagem", "png", "saida")
        if not arq or not isinstance(arq, str): continue
        arq = Path(arq); arq = arq if arq.is_absolute() else pasta / arq
        if not arq.exists():
            alt = pasta / arq.name
            if alt.exists(): arq = alt
            else: print(f"[broll] AVISO: não existe {arq}"); continue
        img = arq.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
        ss = float(_g(it, "in", "ss", "ini", "inicio", "corte_ini", default=0.0))
        dd = _g(it, "dur_arquivo", "dur", "duracao", "dur_util", "duração")
        dd = (float(dd) - ss) if dd is not None else (6.0 if img else dur(arq) - ss)
        tb = (_g(it, "t_bloco_ini"), _g(it, "t_bloco_fim"))
        tb = (float(tb[0]), float(tb[1])) if None not in tb else None
        bl = blocos_de(_g(it, "blocos", "bloco", "para", "uso", "bloco_roteiro", default=""))
        out.append(dict(id=str(_g(it, "id", "nome", default=arq.stem)), file=str(arq), ss=ss, dur=float(dd), blocos=bl,
                        desc=str(_g(it, "descricao", "desc", "descrição", "prompt", default=""))[:120], tipo="img" if img else "video",
                        papel=str(_g(it, "papel", "funcao", "função", "tipo", default="")).lower(), tb=tb, ordem=_g(it, "ordem", default=n),
                        vel=float(_g(it, "vel_sugerida", default=1.0)), extra=it))
    return out


# ---------------------------------------------------------------- placeholders (v1/v2) — só para testar
def _v1(i): return json.loads((V1 / "voz" / "c" / f"{i}.json").read_text(encoding="utf-8"))


def ph_abertura():
    import importlib.util
    sp = importlib.util.spec_from_file_location("piloto", V2T / "piloto.py"); pil = importlib.util.module_from_spec(sp); sp.loader.exec_module(pil)
    corpo, mix = V2T / "mont" / "corpo.mp4", V2T / "mont" / "mix.wav"
    P = [dict(w=p["raw"], ini=p["ini"], fim=p["fim"]) for p in pil.palavras() if p["ini"] < pil.TRp]
    B = [dict(id="ph_B0103", bloco="B01", blocos=["B01", "B02", "B03"], ag="abertura", tipo="take", video=str(corpo), audio=str(mix), v_off=0.0,
              uso=[0.0, pil.TRp], palavras=P, texto="", ruins=[], dur=pil.TRp, extra=dict(full=True))]
    for b, (s0, s1) in (("B04", (10.45, 13.30)), ("B05", (13.42, 15.95)), ("B06", (15.95, 19.20))):
        B.append(dict(id="ph_" + b, bloco=b, blocos=[b], ag="abertura", tipo="mudo", video=str(BASE), audio=None, v_off=s0, uso=[0.0, s1 - s0],
                      palavras=[], texto="", ruins=[], dur=s1 - s0, extra=dict(crop_post=True)))
    return B


def ph_entrevista():
    import importlib.util
    sp = importlib.util.spec_from_file_location("piloto", V2T / "piloto.py"); pil = importlib.util.module_from_spec(sp); sp.loader.exec_module(pil)
    corpo, mix = V2T / "mont" / "corpo.mp4", V2T / "mont" / "mix.wav"
    P = [dict(w=p["raw"], ini=p["ini"], fim=p["fim"]) for p in pil.palavras() if p["ini"] >= pil.TRp]
    out = [dict(id="ph_R01", bloco="R01", blocos=["R01"], ag="entrevista", tipo="take", video=str(corpo), audio=str(mix), v_off=0.0,
                uso=[pil.TRp, pil.TOTAL], palavras=P, texto="", ruins=[], dur=pil.TOTAL, extra=dict(full=True))]
    L, _ = carregar("entrevista", V2T / "aurelio")
    for it, b in zip([x for x in L if x["tipo"] == "take"], ("A01", "A02", "A03")): out.append(dict(it, bloco=b, blocos=[b], id="ph_" + b))
    d = _v1("L07"); Pw = d["palavras"]
    out.append(dict(id="ph_R02", bloco="R02", blocos=["R02"], ag="entrevista", tipo="voz", video=None, audio=str(V1 / "voz" / "c" / "L07.wav"), v_off=0.0,
                    uso=[max(0, Pw[0]["ini"] - 0.08), Pw[-1]["fim"] + 0.12], palavras=Pw, texto="¡Claro!", ruins=[], dur=d["dur"], extra={}))
    return out


def ph_padre():
    L, _ = carregar("padre", V2T / "padre"); m = {x["id"]: x for x in L}; out = []
    for b, k in (("P01", "P2"), ("P02", "P3"), ("P03", "P4"), ("P04", "P5"), ("P05", "P6"), ("P06", "P1"),
                 ("V01", "narr_L08_no-quieren"), ("V04", "narr_L10_monjes-congreso"), ("V08", "narr_L11_imagina")):
        if k in m: out.append(dict(m[k], bloco=b, blocos=[b], id="ph_" + b, ag="padre"))
    return out


BR_PH = dict(tecl=(46.75, 47.85), sb_pe=(51.45, 52.25), sb_esc=(52.55, 55.30), sb_mar=(55.36, 58.17), mul1=(58.25, 59.93),
             perg_a=(82.55, 84.30), perg_b=(84.30, 85.57), cruz=(88.82, 89.97), mont=(90.45, 91.55), hrez=(92.40, 93.90),
             praia=(95.86, 97.20), congr=(99.03, 101.17), mrez1=(106.56, 107.70), mrez2=(107.70, 108.80), divid=(132.83, 139.67))
BR_PH_BLOCO = dict(tecl="V01", perg_b="V01", hrez="O01", praia="O01", chat1="V02", perg_a="V03", sb_pe="V04", sb_mar="V04", sb_esc="V04",
                   congr="V05", chat2="V05", divid="V08", mrez1="R02", cruz="", mont="", mul1="", mrez2="")


def ph_broll():
    out = []
    for k, (a, b) in BR_PH.items():
        out.append(dict(id="ph_" + k, file=str(BASE), ss=a, dur=b - a, blocos=blocos_de(BR_PH_BLOCO.get(k, "")), desc=k, tipo="video", papel="", extra={}))
    for k, f in (("chat1", "chat_1.png"), ("chat2", "chat_2.png")):
        out.append(dict(id="ph_" + k, file=str(G / f), ss=0.0, dur=6.0, blocos=blocos_de(BR_PH_BLOCO[k]), desc=k, tipo="img", papel="print", extra={}))
    return out


def fontes(usar_ph=False):
    F = {}
    for ag in AGENTES:
        pasta = V3T / ag; real = (pasta / ("shotlist.json" if ag == "broll" and (pasta / "shotlist.json").exists() else "manifest.json")).exists()
        if real and not usar_ph:
            F[ag] = shotlist(pasta) if ag == "broll" else carregar(ag, pasta)[0]; F[ag + "_real"] = True
        else:
            F[ag] = dict(abertura=ph_abertura, entrevista=ph_entrevista, padre=ph_padre, broll=ph_broll)[ag](); F[ag + "_real"] = False
    return F


if __name__ == "__main__":
    F = fontes("--ph" in sys.argv)
    for ag in AGENTES:
        print(f"== {ag} ({'REAL' if F[ag + '_real'] else 'placeholder'})")
        for it in F[ag]:
            if ag == "broll": print(f"  {it['id']:22s} {it['tipo']:5s} {it['dur']:5.2f}s {it['blocos']} {it['desc'][:60]}")
            else: print(f"  {it['id']:22s} {it['blocos']} {it['tipo']:4s} uso {it['uso'][0]:.2f}-{it['uso'][1]:.2f} ruins {it['ruins']} | {it['texto'][:70]}")
