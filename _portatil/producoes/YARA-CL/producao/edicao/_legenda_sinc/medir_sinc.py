# -*- coding: utf-8 -*-
"""Mede a sincronia legenda x fala.
  python medir_sinc.py cfg.json --antigo -o x.json  -> recria o .ass do modo whisper antigo (mesmo codigo) e mede
  python medir_sinc.py cfg.json --ass X.ass         -> mede um .ass (ex.: sidecar da montagem nova)
  [--video final.mp4] confere nos QUADROS do video queimado se cada evento aparece no quadro esperado.
Referencia da fala: alinhamento forcado CTC (wav2vec2) do texto do roteiro no audio limpo de cada segmento
+ onset por energia (independente do alinhador) nas palavras que comecam depois de uma pausa.
Erro = (1o quadro em que o bloco aparece) - (inicio da 1a palavra do bloco na fala).
"""
import argparse, json, re, subprocess, sys, tempfile, difflib
from pathlib import Path
import numpy as np

ED = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ED))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import montar as M
import alinhar_roteiro as ar
from energia import regioes


NUM = {"2": "dos", "3": "tres", "1": "uno"}


def ts(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def eventos(ass):
    ev = []
    for ln in Path(ass).read_text(encoding="utf-8").splitlines():
        if ln.startswith("Dialogue:"):
            c = ln.split(",", 9)
            y = re.search(r"\\pos\(\d+,(\d+)\)", c[9])
            txt = re.sub(r"\{[^}]*\}", "", c[9]).replace("\u00a0", " ")
            ev.append({"ini": ts(c[1]), "fim": ts(c[2]), "txt": txt,
                       "pal": [ar.norm_tok(NUM.get(w.strip(".,!?"), w)) for w in txt.split() if ar.norm_tok(NUM.get(w.strip(".,!?"), w))],
                       "y": int(y.group(1)) if y else 1060})
    return ev


def preparar(cfg_path):
    cfg_path = Path(cfg_path).resolve()
    raiz = cfg_path.parent
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    t, faixas = 0.0, []
    for s in cfg["segmentos"]:
        n, d = M.duracao_segmento(s, raiz)
        faixas.append((t, t + d, s.get("tipo", "outro")))
        t += d
    tit = cfg.get("titulo", {"png": "x", "dur": 1.5})
    cta = cfg.get("cta", {"dur": 2.5})
    return cfg, raiz, faixas, (float(tit["dur"]) if tit else 0.0), (t - float(cta["dur"]) if cta else t), t


def ass_antigo(cfg, raiz, faixas, t_tit, t_cta, destino):
    tmp = Path(tempfile.mkdtemp(prefix="medir_"))
    wavs = []
    for i, (s, (a, b, _)) in enumerate(zip(cfg["segmentos"], faixas)):
        d = b - a
        pa = tmp / f"s{i}.wav"
        af = f"aresample={M.SR},aformat=sample_fmts=s16:channel_layouts=stereo,apad,atrim=0:{d:.6f},asetpts=N/SR/TB"
        src = (raiz / (s.get("audio") or s["video"])).resolve()
        ss = s.get("audio_de", 0) if s.get("audio") else s.get("de", 0)
        M.sh(["ffmpeg", "-v", "error", "-y", "-ss", ss, "-i", src, "-vn", "-af", af, "-ar", M.SR, "-ac", 2, pa])
        wavs.append(pa)
    voz = tmp / "voz.wav"
    M.sh(["ffmpeg", "-v", "error", "-y", *sum([["-i", w] for w in wavs], []), "-filter_complex",
          "".join(f"[{i}:a]" for i in range(len(wavs))) + f"concat=n={len(wavs)}:v=0:a=1[a]", "-map", "[a]", voz])
    fy = [(a, b, s.get("legenda_y")) for (a, b, _), s in zip(faixas, cfg["segmentos"])]
    M.legenda(voz, dict(cfg.get("legenda") or {}), t_tit, t_cta, destino, fy)
    return destino


def onsets_energia(cfg, raiz, faixas):
    """inicios de fala (apos pausa) por energia no audio limpo de cada segmento, na linha do tempo"""
    out, cache = [], {}
    for s, (a, b, _) in zip(cfg["segmentos"], faixas):
        src = (raiz / (s.get("audio") or s["video"])).resolve()
        a0 = float(s.get("audio_de", 0) if s.get("audio") else s.get("de", 0))
        if src not in cache:
            cache[src] = regioes(str(src))
        for r0, r1 in cache[src]:
            if a0 <= r0 < a0 + (b - a):
                out.append(a + r0 - a0)
    return out


def quadros_banda(video, ys, t_max):
    """por quadro: quantos pixels claros (texto da legenda) mudaram na banda da legenda"""
    res = {}
    for y in set(ys):
        yc = int(y * 1280 / 1920)
        h = 150
        y0 = max(0, min(1280 - h, yc - h // 2))
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-t", f"{t_max:.2f}", "-vf",
                            f"crop=720:{h}:0:{y0},format=gray", "-f", "rawvideo", "-"], capture_output=True)
        f = np.frombuffer(r.stdout, np.uint8).reshape(-1, h, 720)
        claro = (f > 215).reshape(len(f), -1)
        res[y] = np.r_[0, (claro[1:] != claro[:-1]).sum(1)]
    return res


def medir(cfg_path, ass, video=None, rotulo=""):
    cfg, raiz, faixas, t_tit, t_cta, total = preparar(cfg_path)
    textos = json.load(open(ED / "textos_legenda.json", encoding="utf-8"))
    ref = ar.palavras_timeline(cfg["segmentos"], raiz, faixas, textos, metodo="ctc")
    ons = onsets_energia(cfg, raiz, faixas)
    ev = eventos(ass)
    linhas, errs, errs_en, usados = [], [], [], set()
    for e in ev:
        if not e["pal"]:
            continue
        w0 = e["pal"][0]
        cand = [(abs(r[1] - e["ini"]), j) for j, r in enumerate(ref)
                if j not in usados and abs(r[1] - e["ini"]) < 2.5 and
                (ar.norm_tok(r[0]) == w0 or difflib.SequenceMatcher(a=ar.norm_tok(r[0]), b=w0).ratio() >= 0.6)]
        k = int(np.ceil(e["ini"] * 30 - 1e-6))   # 1o quadro em que o bloco aparece
        if not cand:
            linhas.append({"legenda": e["txt"], "leg_t": round(k / 30, 3), "fala_t": None, "erro_ms": None,
                           "obs": "texto sem correspondencia na fala"})
            continue
        _, j = min(cand)
        usados.add(j)
        r = ref[j]
        err = (k / 30 - r[1]) * 1000
        e_en = None
        if j == 0 or r[1] - ref[j - 1][2] > 0.12:   # so palavra depois de pausa (onset de energia confiavel)
            en = [o for o in ons if abs(o - r[1]) < 0.25]
            if en:
                o = min(en, key=lambda o: abs(o - r[1]))
                e_en = round((k / 30 - o) * 1000)
                errs_en.append(e_en)
        errs.append(err)
        linhas.append({"legenda": e["txt"], "leg_t": round(k / 30, 3), "palavra": r[0], "fala_t": r[1],
                       "erro_ms": round(err), "erro_energia_ms": e_en})
    sem = sum(1 for l in linhas if l["erro_ms"] is None)
    # palavras faladas (fora do titulo/CTA) que nao estao na tela enquanto sao faladas
    faltando = []
    for r in ref:
        if r[1] < t_tit + 0.02 or r[1] >= t_cta - 0.05:
            continue
        nt = ar.norm_tok(r[0])
        ok = any(e["ini"] - 0.12 <= r[1] < e["fim"] + 0.05 and any(nt == p or nt in p for p in e["pal"]) for e in ev)
        if not ok:
            faltando.append((r[0], r[1]))
    quad = None
    if video:
        sinais = quadros_banda(video, [e["y"] for e in ev], t_cta + 0.5)
        hit, tot, falhas = 0, 0, []
        for e in ev:
            k = int(np.ceil(e["ini"] * 30 - 1e-6))
            d = sinais[e["y"]]
            if k >= len(d) or k < 1:
                continue
            tot += 1
            viz = d[max(1, k - 3):k + 4]
            if d[k] >= 150:   # o texto do bloco muda exatamente neste quadro
                hit += 1
            else:
                falhas.append((e["txt"], round(k / 30, 2), int(d[k]), int(viz.argmax()) + max(1, k - 3) - k))
        quad = {"eventos_conferidos": tot, "aparecem_no_quadro_esperado": hit, "falhas": falhas[:10]}
    a = np.abs(errs) if errs else np.array([0.0])
    return {"rotulo": rotulo, "cfg": str(cfg_path), "titulo_ate": t_tit, "cta_desde": round(t_cta, 3),
            "blocos_medidos": len(errs), "blocos_texto_errado": sem,
            "erro_medio_abs_ms": round(float(a.mean())), "erro_max_abs_ms": round(float(a.max())),
            "pct_dentro_100ms": round(100 * float((a <= 100).mean()), 1),
            "erro_energia_max_abs_ms": (max(abs(x) for x in errs_en) if errs_en else None), "n_energia": len(errs_en),
            "faladas_sem_legenda": faltando, "quadros": quad, "linhas": linhas}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cfg")
    ap.add_argument("--antigo", action="store_true")
    ap.add_argument("--ass")
    ap.add_argument("--video")
    ap.add_argument("--rotulo", default="")
    ap.add_argument("-o")
    a = ap.parse_args()
    ass = a.ass
    if a.antigo:
        cfg, raiz, faixas, t_tit, t_cta, total = preparar(a.cfg)
        ass = str(Path(a.o).with_suffix(".ass")) if a.o else "antigo.ass"
        ass_antigo(cfg, raiz, faixas, t_tit, t_cta, ass)
    r = medir(a.cfg, ass, a.video, a.rotulo)
    if a.o:
        json.dump(r, open(a.o, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in r.items() if k not in ("linhas",)}, ensure_ascii=False))
    for l in r["linhas"]:
        if l["erro_ms"] is None or abs(l["erro_ms"]) > 100:
            print("  ", l)
