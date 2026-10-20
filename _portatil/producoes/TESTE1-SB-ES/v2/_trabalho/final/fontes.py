# -*- coding: utf-8 -*-
"""Fontes da montagem v2: lê os manifest.json dos agentes (react / aurelio / padre) e normaliza cada item para
  {id, ag, tipo: "take"|"voz", video, audio, v_off, uso:[ini,fim], palavras:[{w,ini,fim}], texto, ruins:[[a,b]], dur}
(tempos em segundos no ARQUIVO de áudio; video_t = audio_t + v_off).
Sem manifest -> placeholders feitos da v1 (python fontes.py --placeholder gera os arquivos em final/ph/).
Não escreve nas pastas dos agentes."""
import json, re, subprocess, sys
from pathlib import Path
AQ = Path(__file__).resolve().parent; V2T = AQ.parent; V1 = V2T.parent.parent / "_trabalho"
PH = AQ / "ph"; AGENTES = ("react", "aurelio", "padre")


def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(" ".join(map(str, c))[:800]); print(r.stderr[-1500:]); sys.exit(1)
    return r


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout.strip())


def tem_video(p):
    return bool(run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=index", "-of", "csv=p=0", p]).stdout.strip())


# ---------------------------------------------------------------- normalização de manifest (nomes de chave tolerantes)
def _g(d, *ks, default=None):
    for k in ks:
        if isinstance(d, dict) and k in d and d[k] is not None: return d[k]
    return default


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
        if isinstance(x, dict): a = _g(x, "ini", "start", "de", "a"); b = _g(x, "fim", "end", "ate", "b")
        else: a, b = x[0], x[1]
        g = x.get("grave", True) if isinstance(x, dict) else True
        if a is not None and b is not None and float(b) > float(a): out.append([float(a), float(b), bool(g)])
    return out


def _itens(raw):
    if isinstance(raw, list): return raw
    if any(k in raw for k in ("arquivo", "file", "video", "mp4")): return [raw]          # manifest de 1 item só
    L = None
    for k in ("itens", "items", "takes", "clips", "falas", "segmentos", "trechos"):
        if isinstance(raw.get(k), list): L = list(raw[k]); break
    if L is None: L = [v | {"id": k} for k, v in raw.items() if isinstance(v, dict) and any(x in v for x in ("arquivo", "file", "video"))]
    for k2 in ("narracoes", "narrações", "narracao", "narração", "audio_separado", "audios_separados", "vozes", "wavs", "audios", "narr"):
        v = raw.get(k2)
        if isinstance(v, dict): v = [v]
        if isinstance(v, list): L += [dict(x, tipo=x.get("tipo", "voz"), id=x.get("id", f"{k2}{i}")) for i, x in enumerate(v) if isinstance(x, dict)]
    return L


def carregar(ag, pasta=None):
    pasta = Path(pasta or V2T / ag); mf = pasta / "manifest.json"
    raw = json.loads(mf.read_text(encoding="utf-8")); res = []
    for n, it in enumerate(_itens(raw)):
        arq = _g(it, "arquivo", "file", "video", "mp4", "path", "saida", "wav", "audio")
        if not arq: continue
        arq = Path(arq); arq = arq if arq.is_absolute() else pasta / arq
        if not arq.exists(): print(f"[{ag}] AVISO: arquivo não existe: {arq}"); continue
        aud = _g(it, "audio_arquivo", "wav", "audio")
        aud = Path(aud) if isinstance(aud, str) and re.search(r"\.(wav|mp3|m4a|aac|flac)$", aud, re.I) else arq
        aud = aud if aud.is_absolute() else pasta / aud
        if not aud.exists(): aud = arq
        tipo = str(_g(it, "tipo", "type", "kind", default="")).lower()
        vid = tem_video(arq) if arq.suffix.lower() in (".mp4", ".mov", ".mkv", ".webm") else False
        tipo = "take" if (vid and not tipo.startswith(("voz", "narr", "audio", "wav", "off"))) else "voz"
        d = dur(aud)
        P = _palavras(_g(it, "palavras", "words", "tempos", "tempos_palavras", "word_timings", "alinhamento"))
        uso = _g(it, "uso_s", "trecho_uso")
        R = _intervalos(_g(it, "ruins", "intervalos_ruins", "cobrir", "bad", "ruim", "cobrir_broll"))
        if isinstance(uso, list) and len(uso) == 2 and all(isinstance(x, (int, float)) for x in uso): uso = [float(uso[0]), float(uso[1])]
        elif _g(it, "quadros") and tipo == "take": uso = [0.0, min(d, float(_g(it, "quadros")) / float(_g(it, "fps", default=30)))]
        elif P: uso = [max(0.0, P[0]["ini"] - (0.10 if tipo == "take" else 0.08)), min(d, P[-1]["fim"] + (0.25 if tipo == "take" else 0.15))]
        else: uso = [0.0, d]
        # intervalo ruim encostado na borda do trecho usado -> apara o trecho em vez de cobrir
        apara_ini = apara_fim = False
        for r_ in list(R):
            a, b = r_[0], r_[1]
            if a <= uso[0] + 0.06 and b < (P[0]["fim"] if P else b + 1): uso[0] = max(uso[0], b - 0.02); R.remove(r_); apara_ini = True
            elif b >= uso[1] - 0.06 and P and a > P[-1]["ini"]: uso[1] = min(uso[1], a + 0.02); R.remove(r_); apara_fim = True
        res.append(dict(id=str(_g(it, "id", "nome", "name", default=f"{ag}{n}")), ag=ag, tipo=tipo,
                        video=str(arq) if tipo == "take" else None, audio=str(aud), v_off=float(_g(it, "v_off", "offset_video", default=0.0)),
                        uso=uso, palavras=P, texto=str(_g(it, "texto", "text", "fala", default=" ".join(p["w"] for p in P))),
                        ruins=R,
                        dur=d, ordem=n, modo=_g(it, "modo", "layout"), apara_ini=apara_ini, apara_fim=apara_fim))
    ordem = _g(raw, "ordem_montagem", "ordem", "order") if isinstance(raw, dict) else None
    if isinstance(ordem, list) and ordem:
        def pos(it):
            nome = Path(it["video"] or it["audio"]).name
            for k, o in enumerate(ordem):
                if nome in str(o) or str(o).split()[0] == it["id"]: return k
            return 999 + it["ordem"]
        res.sort(key=pos)
    return res


# ---------------------------------------------------------------- placeholders da v1 (para testar a pipeline)
def _v1(i):
    return json.loads((V1 / "voz" / "c" / f"{i}.json").read_text(encoding="utf-8"))


def _corte(i, de, ate):
    """palavras da fala v1 i, do índice de (inclusive) ao ate (exclusive)"""
    d = _v1(i); P = d["palavras"][de:ate]; return d, P


PLANO_PH = {   # (agente, id, tipo, fala v1, palavra ini, palavra fim excl.)
    "react": [("R1", "take", "L01", 0, None)],
    "aurelio": [("A1", "take", "L05", 0, 25), ("A1v", "voz", "L05", 25, 32), ("A2", "take", "L05", 32, None), ("A3", "take", "L06", 0, None)],
    "padre": [("P1", "take", "L08", 0, 20), ("P2", "take", "L08", 20, 32), ("P2v", "voz", "L08", 32, 45), ("P3", "take", "L08", 45, None),
              ("P4", "take", "L10", 0, 20), ("P5", "take", "L10", 20, 36), ("P5v", "voz", "L10", 36, 85), ("P6", "take", "L12", 0, 37)],
}


def placeholder():
    import importlib.util
    sp = importlib.util.spec_from_file_location("plano_v1", V1 / "plano.py"); pl = importlib.util.module_from_spec(sp)
    sys.path.insert(0, str(V1)); sp.loader.exec_module(pl)
    for ag, L in PLANO_PH.items():
        pasta = PH / ag; pasta.mkdir(parents=True, exist_ok=True); itens = []
        for nome, tipo, fala, a, b in L:
            d = _v1(fala); P = d["palavras"][a:b]; ini = max(0, P[0]["ini"] - 0.25); fim = min(d["dur"], P[-1]["fim"] + 0.3)
            T = pl.LIN[fala]["T0"]
            wav = pasta / f"{nome}.wav"
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-t", f"{fim - ini:.3f}", "-i", V1 / "voz" / "c" / f"{fala}.wav", wav])
            arq = wav
            if tipo == "take":
                arq = pasta / f"{nome}.mp4"
                src = V1 / "mont" / "cena_00_ls.mp4" if ag == "react" else V1 / "mont" / "corpo.mp4"
                ss = ini if ag == "react" else T + ini
                run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{fim - ini:.3f}", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a",
                     "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", arq])
            W = [dict(w=p["w"], ini=round(p["ini"] - ini, 3), fim=round(p["fim"] - ini, 3)) for p in P]
            it = dict(id=nome, tipo=tipo, arquivo=arq.name, texto=" ".join(p["w"] for p in P), palavras=W)
            if nome == "P1": it["ruins"] = [[1.0, 1.6]]      # testa a cobertura automática
            itens.append(it)
        (pasta / "manifest.json").write_text(json.dumps(dict(itens=itens), ensure_ascii=False, indent=1), encoding="utf-8")
        print(ag, len(itens), "itens placeholder")


def fontes(usar_ph=False):
    """{ag: [itens]}; usa o manifest real do agente quando existe, senão o placeholder"""
    out = {}
    for ag in AGENTES:
        real = V2T / ag / "manifest.json"
        if real.exists() and not usar_ph: out[ag] = carregar(ag); out[ag + "_real"] = True
        elif (PH / ag / "manifest.json").exists(): out[ag] = carregar(ag, PH / ag); out[ag + "_real"] = False
        else: out[ag] = []; out[ag + "_real"] = False
    return out


if __name__ == "__main__":
    if "--placeholder" in sys.argv: placeholder()
    F = fontes("--ph" in sys.argv)
    for ag in AGENTES:
        print(f"== {ag} ({'REAL' if F[ag + '_real'] else 'placeholder'})")
        for it in F[ag]:
            print(f"  {it['id']:6s} {it['tipo']:4s} uso {it['uso'][0]:.2f}-{it['uso'][1]:.2f} ruins {it['ruins']} | {it['texto'][:90]}")
