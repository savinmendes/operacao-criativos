# -*- coding: utf-8 -*-
"""Fase 2 da versão A: lê v3/_trabalho/v4_assets/manifest.json e injeta nas fontes da montagem:
- PB01 (padre EN VIVO, take HeyGen)  -> F["padre"]  (moldura EN VIVO + punch-in como os outros P);
- AV01 (voz off do Aurelio)          -> F["entrevista"] (tipo voz);
- b-roll inédito do AV01             -> F["broll"] com blocos ["AV01"] (usado uma vez só, dentro da janela do post).
Itens da versão B (P03B/P04B/P05B/P07B e b-rolls de substituição) são ignorados."""
import json, re
from pathlib import Path
import fontes_v3 as fontes

SO_B = re.compile(r"\b(P03B|P04B|P05B|P07B)\b|vers[aã]o[\"' :_-]*B\b|\bsubstitui", re.I)


def tag(x):
    s = json.dumps(x, ensure_ascii=False)
    has_av, has_pb = "AV01" in s.upper(), "PB01" in s.upper()
    if has_av and not has_pb: return "AV01"
    if has_pb and not has_av: return "PB01"
    if has_av and has_pb:          # decide pelo campo de bloco/id
        k = " ".join(str(x.get(c, "")) for c in ("bloco", "blocos", "id", "arquivo", "file")).upper()
        return "AV01" if "AV01" in k else "PB01" if "PB01" in k else None
    return None


def carregar(F, mf):
    pasta = Path(mf).parent; L, raw = fontes.carregar("v4", pasta); log = []
    for x in L:
        t = tag(x["extra"])
        if t is None or (SO_B.search(json.dumps(x["extra"], ensure_ascii=False)) and t is None): log.append(f"ignorado {x['id']}"); continue
        if t == "PB01":
            if x["tipo"] != "take": log.append(f"PB01 não é take ({x['tipo']}): {x['id']} ignorado"); continue
            F["padre"].append(dict(x, bloco="PB01", blocos=["PB01"], ag="padre")); log.append(f"PB01 take {Path(x['video']).name} uso {x['uso']}")
        elif t == "AV01" and x["tipo"] == "voz":
            F["entrevista"].append(dict(x, bloco="AV01", blocos=["AV01"], ag="entrevista")); log.append(f"AV01 voz {Path(x['audio']).name} uso {x['uso']}")
        elif t == "AV01":            # b-roll (mudo) ou take com áudio -> b-roll (a voz vem do item de voz)
            ex = x["extra"]; ss = float(fontes._g(ex, "in", "ss", "ini_uso", default=0.0))
            F["broll"].append(dict(id=f"v4_{Path(x['video']).stem}", file=x["video"], ss=ss, dur=x["dur"] - ss, blocos=["AV01"],
                                   desc=str(fontes._g(ex, "descricao", "desc", "texto", default=""))[:120], tipo="video", papel="",
                                   tb=None, ordem=-1, vel=1.0, extra=ex))
            log.append(f"AV01 b-roll {Path(x['video']).name} {x['dur']:.2f}s")
    # imagem como b-roll do AV01 (carregar() trata imagem como áudio -> não entra; procura direto no manifest)
    for it in fontes._itens(raw):
        arq = fontes._g(it, "arquivo", "file", "imagem", "png")
        if isinstance(arq, str) and re.search(r"\.(png|jpe?g|webp)$", arq, re.I) and tag(it) == "AV01":
            p = Path(arq); p = p if p.is_absolute() else pasta / p
            F["broll"].append(dict(id=f"v4_{p.stem}", file=str(p), ss=0.0, dur=6.0, blocos=["AV01"], desc="", tipo="img", papel="print",
                                   tb=None, ordem=-1, vel=1.0, extra=it)); log.append(f"AV01 imagem {p.name}")
    print("v4_assets:", *log, sep="\n   ")
