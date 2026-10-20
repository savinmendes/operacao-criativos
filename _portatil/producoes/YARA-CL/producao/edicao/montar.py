# -*- coding: utf-8 -*-
"""Montador de AD 9:16 720x1280 30 fps (python + ffmpeg, local, sem custo).

Uso:
  python montar.py config.json [--sem-legenda] [--manter-tmp]

config.json (caminhos relativos = relativos ao proprio JSON):
{
  "saida": "AD 01 - YARA-KIT3-BF-ES-CL-A.mp4",
  "overlays": ".",                    # pasta com titulo_abertura.png, banner_topo.png, sticker_kit.png, selo_bf.png, cta_final.png
  "sfx": "sfx",                       # pasta com whoosh.wav e pop.wav
  "segmentos": [
    {"video": "T1.mp4", "tipo": "consultora"},                                  # audio do proprio video
    {"video": "b_yara.mp4", "tipo": "broll", "audio": "N_yara.mp3"},            # dura o audio (video cortado / congelado)
    {"video": "T3.mp4", "tipo": "consultora", "zoom": "in", "de": 0.2, "ate": 3.1},
    ...
  ],
  "titulo": {"png": "titulo_abertura.png", "dur": 1.5},      # null = sem titulo
  "cta":    {"png": "cta_final.png", "dur": 2.5},            # null = sem tela final
  "banner": true, "sticker": true,
  "selo": {"em": "broll"},                                   # "broll" | "consultora" | "sempre" | null
  "whoosh": true, "pop": true,
  "legenda": {"modo": "roteiro",       # PADRAO: alinhamento forcado do texto do roteiro no audio limpo de cada segmento
              "textos": "textos_legenda.json",   # {nome_do_audio_sem_ext: "texto exato"}; N_*.mp3 usam o .alinhamento.json
              "y": 1060, "chaves": [...], "juntar": [["día", "a", "día"]]},
  # modo "whisper" (antigo, so compatibilidade): {"modo": "whisper", "modelo": "small", "corrigir": [...], "fundir": [...],
  #   "inicio": [["^orquídea", 5.84]]} -> whisper sobre a voz montada (errava o tempo em ate ~1 s; ver _legenda_sinc/)
  "loudnorm": -15, "limite_mb": 30
}

Segmento: video (obrigatorio); audio (opcional: arquivo de audio OU video, com audio_de/audio_ate; sem ele usa o audio do
video em de/ate); dur (opcional: forca a duracao); tipo "consultora" | "broll" | "outro";
zoom: "in" (100->112% animado) | "out" (112->100%) | numero (fixo, ex. 1.12) | null (auto: nos segmentos de consultora
alterna 100% / 112% fixo; broll 100%); centro [x, y] relativo do zoom (padrao consultora [0.5, 0.42], rosto acima);
legenda_y (opcional: centro da legenda neste segmento, px do quadro 1080x1920; o bloco nunca atravessa o corte);
snap (zoom rapido +8% -> 0 em 0,2 s no inicio do corte; padrao true p/ consultora, false p/ broll - o B-roll ja vem com snap);
png (opcional: overlay 720x1280 so durante o segmento, ex. rotulo grande no gancho).

O que faz:
 1. Normaliza cada segmento (720x1280, 30 fps, yuv420p, etiqueta bt709/tv SEM converter a matriz; audio 48 kHz estereo
    com duracao = n_quadros/30 exatos) -> evita a armadilha de concat com metadados diferentes.
 2. Concatena (todos com os mesmos parametros) e aplica numa passada: titulo (1,5 s, entra com pop) + pop sonoro,
    banner fixo (fora do titulo e do CTA), sticker no rodape nos trechos de B-roll, selo opcional, CTA nos ultimos N s,
    legenda palavra a palavra (alinhamento forcado do roteiro + legenda.py do kit; branca, contorno preto, 1 palavra-chave amarela),
    whoosh em cada corte, loudnorm.
 3. Confere: decodificacao, duracao do audio decodificado = duracao do video, tamanho <= limite (reencoda se passar).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KIT_FERR = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
sys.path.insert(0, str(KIT_FERR))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # alinhar_roteiro.py

W, H, FPS, SR = 720, 1280, 30, 48000
TAGS = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
COR = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
CHAVES_PADRAO = ["yara", "moi", "elixir", "gratis", "tres", "dos", "2", "3", "recibir", "black", "friday", "liquidación",
                 "envío", "pide", "intenso", "femenino", "elegante", "noche", "cita"]
CORRIGIR_PADRAO = [
    [r"^(iara|llara|yarra|lara|yára|jara|yarah)([.,!?¡¿]*)$", r"Yara\2"],
    [r"^(mua|muá|moa|moí|mwa|moá)([.,!?¡¿]*)$", r"Moi\2"],
    [r"^(el[ií]xir|elisir|elíxir|elixír)([.,!?¡¿]*)$", r"Elixir\2"],
]


def sh(args, cwd=None):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg falhou:\n" + " ".join(map(str, args))[:600] + "\n" + r.stderr[-2500:])
    return r.stdout


def dur(p) -> float:
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).strip())


def tem_audio(p) -> bool:
    return bool(sh(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", p]).strip())


def dur_audio_decodificado(p) -> float:
    """soma real das amostras decodificadas (pega salto de pts / audio curto)"""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a:0", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                       capture_output=True)
    return len(r.stdout) / 2 / SR


# ---------------------------------------------------------------- 1. normalizar segmentos
def zoom_expr(z0, z1, n, snap):
    base = f"({z0}+({z1}-{z0})*on/{max(1, n)})"
    if snap:
        base += f"*(1+0.08*pow(max(0\\,1-on/6)\\,2))"
    return base


def duracao_segmento(s, raiz):
    """(n_quadros, duracao = n/30) do segmento na montagem"""
    if s.get("dur"):
        d = float(s["dur"])
    elif s.get("audio"):
        a = (raiz / s["audio"]).resolve()
        ad0, ad1 = float(s.get("audio_de", 0)), s.get("audio_ate")
        d = (float(ad1) if ad1 is not None else dur(a)) - ad0
    else:
        v = (raiz / s["video"]).resolve()
        d = (float(s["ate"]) if s.get("ate") is not None else dur(v)) - float(s.get("de", 0))
    n = max(1, round(d * FPS))
    return n, n / FPS


def normalizar(i, s, raiz, tmp, cont_consultora):
    v = (raiz / s["video"]).resolve()
    tipo = s.get("tipo", "outro")
    de = float(s.get("de", 0))
    n, d = duracao_segmento(s, raiz)

    # zoom
    z = s.get("zoom")
    if z == "in":
        z0, z1 = 1.0, 1.12
    elif z == "out":
        z0, z1 = 1.12, 1.0
    elif isinstance(z, (int, float)):
        z0 = z1 = float(z)
    elif tipo == "consultora":
        z0 = z1 = (1.12 if cont_consultora % 2 == 1 else 1.0)
    else:
        z0 = z1 = 1.0
    snap = s.get("snap", tipo == "consultora")
    cx, cy = s.get("centro", [0.5, 0.42] if tipo == "consultora" else [0.5, 0.5])

    vf = [f"fps={FPS}", f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={W}:{H}", "setsar=1",
          f"tpad=stop_mode=clone:stop_duration={d + 1}"]
    if z0 != 1.0 or z1 != 1.0 or snap:
        vf += ["scale=1440:2560:flags=lanczos",
               f"zoompan=z='{zoom_expr(z0, z1, n, snap)}':d=1:fps={FPS}:s={W}x{H}:"
               f"x='max(0\\,min(iw-iw/zoom\\,iw*{cx}-iw/zoom/2))':y='max(0\\,min(ih-ih/zoom\\,ih*{cy}-ih/zoom/2))'"]
    vf += ["format=yuv420p", TAGS]
    pv = tmp / f"seg{i:02d}.mp4"
    sh(["ffmpeg", "-v", "error", "-y", "-ss", de, "-i", v, "-an", "-vf", ",".join(vf), "-frames:v", n, "-r", FPS,
        "-c:v", "libx264", "-crf", 14, "-preset", "fast", "-g", FPS, *COR, pv])

    # audio: exatamente n/30 s, 48 kHz estereo
    pa = tmp / f"seg{i:02d}.wav"
    af = f"aresample={SR},aformat=sample_fmts=s16:channel_layouts=stereo,apad,atrim=0:{d:.6f},asetpts=N/SR/TB"
    if s.get("audio"):
        a = (raiz / s["audio"]).resolve()
        sh(["ffmpeg", "-v", "error", "-y", "-ss", s.get("audio_de", 0), "-i", a, "-vn", "-af", af, "-ar", SR, "-ac", 2, pa])
    elif tem_audio(v):
        sh(["ffmpeg", "-v", "error", "-y", "-ss", de, "-i", v, "-vn", "-af", af, "-ar", SR, "-ac", 2, pa])
    else:
        sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo", "-t", f"{d:.6f}", pa])
    return {"video": pv, "audio": pa, "dur": d, "n": n, "tipo": tipo, "zoom": [z0, z1], "snap": snap}


# ---------------------------------------------------------------- 2. legenda
def _juntar_nomes(junt, cfg_leg, kit_leg):
    """"Yara Moi"/"Yara Elixir" e as sequencias de "juntar" viram 1 bloco (espaco duro); tempo = 1a palavra"""
    out = []
    for w in junt:
        if out and out[-1][0].rstrip(".,!?:").lower() == "yara" and w[0].rstrip(".,!?:").lower() in ("moi", "elixir") \
                and not out[-1][0].endswith((".", ",", ":", "!", "?")):
            p = out.pop()
            out.append((p[0] + kit_leg.NBSP + w[0], p[1], w[2]))
        else:
            out.append(w)
    for seq in cfg_leg.get("juntar", []):
        alvo = [x.lower() for x in seq]
        i, novo = 0, []
        while i < len(out):
            cand = [x[0].rstrip(".,!?").lower() for x in out[i:i + len(alvo)]]
            if cand == alvo:
                bloco = out[i:i + len(alvo)]
                novo.append((kit_leg.NBSP.join(x[0] for x in bloco), bloco[0][1], bloco[-1][2]))
                i += len(alvo)
            else:
                novo.append(out[i])
                i += 1
        out = novo
    return out


def _snap(t):
    """inicio do evento logo antes do quadro mais proximo (t = k/30): a legenda aparece no quadro k (erro <= 1/2 quadro)"""
    return max(0.0, round(t * FPS) / FPS - 0.012)


def legenda_roteiro(cfg, raiz, faixas, t_ini, t_fim, destino, faixas_y=None, sidecar=None):
    """Legenda por ALINHAMENTO FORCADO do texto do roteiro, segmento a segmento, sobre o audio limpo de cada fala
    (ElevenLabs .alinhamento.json quando existir; senao CTC wav2vec2). Nada de whisper sobre a voz montada.
    - palavra que comeca durante o titulo (t < t_ini) nao aparece; a seguinte entra no seu tempo exato (sem atraso);
    - os blocos sao formados DENTRO de cada segmento (nunca atravessam um corte, nada some no corte)."""
    import legenda as kit_leg
    import alinhar_roteiro as ar
    cfg_leg = cfg.get("legenda") or {}
    tx = cfg_leg.get("textos", str(Path(__file__).resolve().parent / "textos_legenda.json"))
    textos = json.load(open((raiz / tx).resolve(), encoding="utf-8")) if isinstance(tx, str) else tx
    pal = ar.palavras_timeline(cfg["segmentos"], raiz, faixas, textos)
    chaves = set(cfg_leg.get("chaves", CHAVES_PADRAO))
    chaves |= {kit_leg.NBSP.join(seq) for seq in cfg_leg.get("juntar", [])}
    chaves |= {f"yara{kit_leg.NBSP}moi", f"yara{kit_leg.NBSP}elixir"}
    # grupos de segmentos com fala CONTINUA (mesmo audio, audio_de = audio_ate do anterior, mesma legenda_y):
    # o bloco pode atravessar esse corte (a frase continua), senao fecha no corte
    segs = cfg["segmentos"]
    grupos = []
    for i, s in enumerate(segs):
        if grupos and i > 0:
            p = segs[i - 1]
            cont = (s.get("audio") and s.get("audio") == p.get("audio") and p.get("audio_ate") is not None
                    and abs(float(s.get("audio_de", 0)) - float(p["audio_ate"])) < 0.02
                    and s.get("legenda_y") == p.get("legenda_y"))
            if cont:
                grupos[-1].append(i)
                continue
        grupos.append([i])
    if faixas_y:
        faixas_y = [(faixas[g[0]][0], faixas[g[-1]][1], segs[g[0]].get("legenda_y")) for g in grupos]
    linhas, cab, vis = [], None, []
    for gi, gr in enumerate(grupos):
        i, a, b = gi, faixas[gr[0]][0], faixas[gr[-1]][1]
        g = [(w, s0, s1) for w, s0, s1, k in pal if k in gr and s0 >= t_ini - 0.02 and s0 < t_fim - 0.05]
        if not g:
            continue
        g = [(w, max(s0, t_ini), s1) for w, s0, s1 in g]
        g = _juntar_nomes(g, cfg_leg, kit_leg)
        vis += [(w, s0, s1, i) for w, s0, s1 in g]
        g = [(w, _snap(s0), s1) for w, s0, s1 in g]
        tmp_ass = Path(str(destino) + f".seg{i}")
        kit_leg.gera_ass(g, str(tmp_ass), estilo=cfg_leg.get("estilo", "drop"), chaves=chaves,
                         y=cfg_leg.get("y", 1060), fim_total=min(b, t_fim))
        txt = tmp_ass.read_text(encoding="utf-8").splitlines()
        tmp_ass.unlink()
        k = txt.index("[Events]") + 2
        cab = cab or txt[:k]
        linhas += [ln for ln in txt[k:] if ln.startswith("Dialogue:")]
    Path(destino).write_text("\n".join((cab or []) + linhas) + "\n", encoding="utf-8")
    if faixas_y:
        _ajustar_por_segmento(destino, faixas_y)
    if sidecar:   # copia do .ass + palavras (para medir a sincronia depois)
        Path(sidecar).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(destino, str(sidecar) + ".ass")
        json.dump({"titulo_ate": t_ini, "cta_desde": t_fim, "palavras_visiveis": vis,
                   "faixas": [list(f) for f in faixas]},
                  open(str(sidecar) + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    return [w[0] for w in vis]


def legenda(voz_wav, cfg_leg, t_ini, t_fim, destino, faixas_y=None):
    """modo "whisper" (antigo): faster-whisper sobre a voz montada + corrigir/fundir/juntar/inicio"""
    import legenda as kit_leg  # legenda.py do kit
    pal = kit_leg.palavras_por_whisper(str(voz_wav), cfg_leg.get("idioma", "es"), cfg_leg.get("modelo", "small"))
    corr = CORRIGIR_PADRAO + cfg_leg.get("corrigir", [])
    out = []
    for w, a, b in pal:
        for rx, tr in corr:
            w = re.sub(rx, tr, w, flags=re.I)
        if a < t_ini - 0.05 or a >= t_fim:   # o titulo cobre a fala inicial; o CTA final tem texto proprio
            continue
        out.append((w, max(a, t_ini), min(b, t_fim)))
    # fundir pares que o whisper quebrou (ex. "el" + "Íxir," -> "Elixir,"): [["regex1", "regex2", "troca (grupos da 2a)"]]
    for r1, r2, tr in cfg_leg.get("fundir", []):
        j, novo = 0, []
        while j < len(out):
            if j + 1 < len(out) and re.match(r1, out[j][0], re.I) and re.match(r2, out[j + 1][0], re.I):
                novo.append((re.sub(r2, tr, out[j + 1][0], flags=re.I), out[j][1], out[j + 1][2]))
                j += 2
            else:
                novo.append(out[j])
                j += 1
        out = novo
    # "Yara Moi"/"Yara Elixir" juntos no mesmo bloco (espaco duro)
    junt = []
    for w in out:
        if junt and junt[-1][0].rstrip(".,!?").lower() == "yara" and w[0].rstrip(".,!?").lower() in ("moi", "elixir"):
            p = junt.pop()
            junt.append((p[0] + kit_leg.NBSP + w[0], p[1], w[2]))
        else:
            junt.append(w)
    # "juntar": [["día", "a", "día"], ...] -> sequencias de palavras viram 1 bloco (espaco duro), p/ chave de varias palavras
    for seq in cfg_leg.get("juntar", []):
        alvo = [x.lower() for x in seq]
        i, novo = 0, []
        while i < len(junt):
            cand = [x[0].rstrip(".,!?").lower() for x in junt[i:i + len(alvo)]]
            if cand == alvo:
                bloco = junt[i:i + len(alvo)]
                novo.append((kit_leg.NBSP.join(x[0] for x in bloco), bloco[0][1], bloco[-1][2]))
                i += len(alvo)
            else:
                novo.append(junt[i])
                i += 1
        junt = novo
    # "inicio": [["regex", t], ...] -> forca o inicio de uma palavra (whisper atrasa a 1a palavra apos silencio)
    for rx, t0 in cfg_leg.get("inicio", []):
        junt = [(w, float(t0), b) if re.search(rx, w, re.I) else (w, a, b) for w, a, b in junt]
    chaves = set(cfg_leg.get("chaves", CHAVES_PADRAO))
    chaves |= {kit_leg.NBSP.join(seq) for seq in cfg_leg.get("juntar", [])}
    chaves |= {f"yara{kit_leg.NBSP}moi", f"yara{kit_leg.NBSP}elixir"}  # nome composto inteiro em amarelo
    kit_leg.gera_ass(junt, str(destino), estilo=cfg_leg.get("estilo", "drop"), chaves=chaves,
                     y=cfg_leg.get("y", 1060), fim_total=t_fim)
    if faixas_y:
        _ajustar_por_segmento(destino, faixas_y)
    return [w[0] for w in junt]


def _ts_s(ts):
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def _ajustar_por_segmento(ass, faixas_y):
    """faixas_y = [(ini, fim, y|None), ...] por segmento: o bloco nao atravessa o corte (termina no fim do segmento)
    e usa o "legenda_y" do segmento (posicao no quadro base 1080x1920), quando houver."""
    linhas = Path(ass).read_text(encoding="utf-8").splitlines()
    out = []
    for ln in linhas:
        if ln.startswith("Dialogue:"):
            campos = ln.split(",", 9)
            a, b = _ts_s(campos[1]), _ts_s(campos[2])
            for ini, fim, y in faixas_y:
                if ini - 0.02 <= a < fim:
                    if b > fim - 0.02:   # termina 1 centesimo ANTES do 1o quadro do segmento seguinte
                        fe = int((fim - 0.01) * 100) / 100
                        campos[2] = f"{int(fe // 3600)}:{int(fe % 3600 // 60):02d}:{fe % 60:05.2f}"
                    if y is not None:
                        campos[9] = re.sub(r"\\pos\((\d+),\d+\)", lambda m: "\\pos(" + m.group(1) + "," + str(int(y)) + ")",
                                           campos[9])
                    break
            ln = ",".join(campos)
        out.append(ln)
    Path(ass).write_text("\n".join(out) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- 3. montagem final
def montar(cfg_path, sem_legenda=False, manter_tmp=False):
    cfg_path = Path(cfg_path).resolve()
    raiz = cfg_path.parent
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    ov = (raiz / cfg.get("overlays", ".")).resolve()
    sfx = (raiz / cfg.get("sfx", "sfx")).resolve()
    saida = (raiz / cfg["saida"]).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="montar_"))
    print("tmp:", tmp)

    segs, cc = [], 0
    for i, s in enumerate(cfg["segmentos"]):
        r = normalizar(i, s, raiz, tmp, cc)
        if r["tipo"] == "consultora" and s.get("zoom") is None:
            cc += 1
        segs.append(r)
        print(f"[{i + 1}/{len(cfg['segmentos'])}] {Path(s['video']).name}: {r['dur']:.2f} s, {r['tipo']}, zoom {r['zoom']}")

    # tempos
    t, cortes, faixas = 0.0, [], []
    for r in segs:
        faixas.append((t, t + r["dur"], r["tipo"]))
        t += r["dur"]
        cortes.append(t)
    total = t
    cortes = cortes[:-1]
    tit = cfg.get("titulo", {"png": "titulo_abertura.png", "dur": 1.5})
    cta = cfg.get("cta", {"png": "cta_final.png", "dur": 2.5})
    t_tit = float(tit["dur"]) if tit else 0.0
    t_cta = total - float(cta["dur"]) if cta else total

    # concat (mesmos parametros em tudo)
    lst = tmp / "lista.txt"
    lst.write_text("".join(f"file '{r['video'].as_posix()}'\n" for r in segs), encoding="utf-8")
    corpo = tmp / "corpo.mp4"
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", corpo])
    voz = tmp / "voz.wav"
    ins = sum([["-i", r["audio"]] for r in segs], [])
    sh(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
        "".join(f"[{i}:a]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[a]", "-map", "[a]", voz])

    # legenda
    ass_ok = False
    wk = tmp / "wk"
    wk.mkdir()
    if cfg.get("legenda") is not False and not sem_legenda:
        from comum import preparar_fontsdir
        preparar_fontsdir(wk)
        fy = [(a, b, s.get("legenda_y")) for (a, b, _), s in zip(faixas, cfg["segmentos"])]
        if (cfg.get("legenda") or {}).get("modo", "roteiro") == "roteiro":
            sc = Path(__file__).resolve().parent / "_legenda_sinc" / "saidas" / saida.stem
            palavras = legenda_roteiro(cfg, raiz, faixas, t_tit, t_cta, wk / "leg.ass", fy, sidecar=sc)
        else:
            palavras = legenda(voz, cfg.get("legenda") or {}, t_tit, t_cta, wk / "leg.ass", fy)
        print("legenda:", " ".join(palavras))
        ass_ok = True

    # ---- filtergraph
    inputs = [corpo]
    def add(p):
        inputs.append(p)
        return len(inputs) - 1

    def png(nome):
        return (ov / nome).resolve()

    fc = []
    ovfmt = "format=rgba,scale=out_color_matrix=bt709:out_range=tv,format=yuva420p"
    cur = "[0:v]"
    k = 0

    def overlay(idx, x, y, enable, extra=""):
        nonlocal cur, k
        fc.append(f"[{idx}:v]{ovfmt}{extra}[o{k}]")
        fc.append(f"{cur}[o{k}]overlay=x={x}:y={y}:enable='{enable}':eval=frame[v{k}]")
        cur = f"[v{k}]"
        k += 1

    def entre(lista):
        # -10 ms: o quadro do corte (t = k/30 em float) cai no segmento certo, sem 1 quadro de overlay atrasado
        return "+".join(f"between(t\\,{a - 0.01:.3f}\\,{b - 0.01:.3f})" for a, b in lista) or "0"

    # sticker/selo nunca embaixo do titulo de abertura (gancho com B-roll logo no inicio)
    broll = [(max(a, t_tit), min(b, t_cta)) for a, b, tp in faixas if tp == "broll" and a < t_cta and b > t_tit]
    consult = [(max(a, t_tit), min(b, t_cta)) for a, b, tp in faixas if tp == "consultora" and b > t_tit and a < t_cta]
    # "sticker": true no segmento poe o sticker tambem em segmentos que nao sao B-roll (false tira de um B-roll)
    stk = [(max(a, t_tit), min(b, t_cta)) for (a, b, tp), sg in zip(faixas, cfg["segmentos"])
           if sg.get("sticker", tp == "broll") and a < t_cta and b > t_tit]
    if cfg.get("sticker", True) and stk:
        i_ = add(png("sticker_kit.png"))
        overlay(i_, "(W-w)/2", "H-h-40", entre(stk))
    selo = cfg.get("selo")
    if selo:
        quando = {"broll": broll, "consultora": consult, "sempre": [(t_tit, t_cta)]}[selo.get("em", "broll")]
        i_ = add(png(selo.get("png", "selo_bf.png")))
        overlay(i_, selo.get("x", "W-w-16"), selo.get("y", 130), entre(quando))
    if cfg.get("banner", True):
        i_ = add(png("banner_topo.png"))
        overlay(i_, 16, 16, entre([(t_tit, t_cta)]))
    # legenda antes do CTA/titulo (o .ass ja respeita t_tit..t_cta)
    if ass_ok:
        fc.append(f"{cur}ass=leg.ass:fontsdir=fonts[vl]")
        cur = "[vl]"
    # "png" por segmento: overlay de tela cheia (720x1280) so durante aquele segmento (ex. rotulo grande no gancho)
    for (a, b, _), sg in zip(faixas, cfg["segmentos"]):
        if sg.get("png"):
            i_ = add((raiz / sg["png"]).resolve())
            overlay(i_, 0, 0, entre([(a, b)]))
    if tit:
        i_ = add(png(tit["png"]))
        # pop de entrada: 85% -> 106% -> 100% em 0,15 s
        sc = "if(lt(t\\,0.09)\\,0.85+0.21*t/0.09\\,if(lt(t\\,0.15)\\,1.06-0.06*(t-0.09)/0.06\\,1))"
        fc.append(f"[{i_}:v]loop=loop=-1:size=1:start=0,fps={FPS},trim=duration={t_tit + 0.1},{ovfmt},"
                  f"scale=w='{W}*{sc}':h='{H}*{sc}':eval=frame[tt]")
        fc.append(f"{cur}[tt]overlay=x=(W-w)/2:y=(H-h)/2:enable='lt(t\\,{t_tit:.3f})':eval=frame:eof_action=pass[vt]")
        cur = "[vt]"
    if cta:
        i_ = add(png(cta["png"]))
        fc.append(f"[{i_}:v]loop=loop=-1:size=1:start=0,fps={FPS},trim=duration={total + 1},{ovfmt},"
                  f"fade=t=in:st={t_cta:.3f}:d=0.2:alpha=1[cc]")
        fc.append(f"{cur}[cc]overlay=0:0:enable='gte(t\\,{t_cta:.3f})':shortest=1[vc]")
        cur = "[vc]"
    fc.append(f"{cur}format=yuv420p,{TAGS}[vout]")

    # audio: voz + whoosh nos cortes + pop no titulo -> loudnorm
    ia = add(voz)
    mix = [f"[{ia}:a]"]
    if cfg.get("whoosh", True) and cortes:
        iw = add(sfx / "whoosh.wav")
        fc.append(f"[{iw}:a]asplit={len(cortes)}" + "".join(f"[w{j}]" for j in range(len(cortes))))
        for j, c in enumerate(cortes):
            ms = max(0, int((c - 0.15) * 1000))     # pico do whoosh no corte
            fc.append(f"[w{j}]volume=0.45,adelay={ms}|{ms}[wd{j}]")
            mix.append(f"[wd{j}]")
    if cfg.get("pop", True) and tit:
        ip = add(sfx / "pop.wav")
        fc.append(f"[{ip}:a]volume=0.6,adelay=30|30[pp]")
        mix.append("[pp]")
    lufs = cfg.get("loudnorm", -15)
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:duration=first:normalize=0,"
              f"loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample={SR},apad,atrim=0:{total:.6f},asetpts=N/SR/TB[aout]")

    # copia o .ass/fonts para wk e roda la (caminho sem 'C:' no filtro ass)
    args = sum([["-i", str(p)] for p in inputs], [])
    graph = ";".join(fc)
    (tmp / "filtro.txt").write_text(graph, encoding="utf-8")

    def encode(extra):
        sh(["ffmpeg", "-v", "error", "-y", *args, "-/filter_complex", str(tmp / "filtro.txt"),
            "-map", "[vout]", "-map", "[aout]", "-r", FPS, "-t", f"{total:.6f}",
            "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", *extra, *COR,
            "-c:a", "aac", "-b:a", "128k", "-ar", SR, "-ac", 2, "-movflags", "+faststart", str(saida)], cwd=wk)

    saida.parent.mkdir(parents=True, exist_ok=True)
    encode(["-crf", 20, "-preset", "medium", "-maxrate", "6M", "-bufsize", "12M"])
    lim = float(cfg.get("limite_mb", 30))
    mb = saida.stat().st_size / 1e6
    if mb > lim:
        kbps = int((lim * 8e3 * 0.95) / total - 128)
        print(f"{mb:.1f} MB > {lim} MB: reencodando a {kbps} kb/s")
        encode(["-b:v", f"{kbps}k", "-maxrate", f"{kbps}k", "-bufsize", f"{2 * kbps}k", "-preset", "medium"])
        mb = saida.stat().st_size / 1e6

    # ---- conferencias
    erros = subprocess.run(["ffmpeg", "-v", "error", "-i", str(saida), "-f", "null", "-"], capture_output=True, text=True).stderr.strip()
    dv = float(sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                   "stream=nb_read_frames", "-of", "csv=p=0", saida]).strip().strip(",")) / FPS
    da = dur_audio_decodificado(saida)
    rel = {"saida": str(saida), "duracao_video_s": round(dv, 3), "duracao_audio_decodificado_s": round(da, 3),
           "diferenca_s": round(da - dv, 3), "mb": round(mb, 2), "cortes_s": [round(c, 3) for c in cortes],
           "titulo_ate_s": t_tit, "cta_desde_s": round(t_cta, 3), "decodificacao": erros or "ok"}
    print(json.dumps(rel, ensure_ascii=False, indent=1))
    if abs(da - dv) > 0.1:
        print("ATENCAO: audio decodificado difere do video em", round(da - dv, 3), "s")
    if erros:
        print("ATENCAO: erros de decodificacao")

    # quadros de prova: 1 por segmento + titulo + CTA
    marcas = [0.5] + [(a + b) / 2 for a, b, _ in faixas] + [total - 0.5]
    prova = saida.with_name(saida.stem + "_prova.jpg")
    sel = "+".join(f"eq(n\\,{int(m * FPS)})" for m in marcas)
    sh(["ffmpeg", "-v", "error", "-y", "-i", saida, "-vf", f"select='{sel}',scale=240:426,tile={len(marcas)}x1",
        "-frames:v", 1, "-fps_mode", "passthrough", prova])
    print("prova:", prova)
    if not manter_tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    return rel


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--sem-legenda", action="store_true")
    ap.add_argument("--manter-tmp", action="store_true")
    a = ap.parse_args()
    montar(a.config, a.sem_legenda, a.manter_tmp)
