# -*- coding: utf-8 -*-
"""Variações gancho × corpo a partir de vídeos já prontos: banco de tomadas (scdet) + gancho novo (fala + cenas do
banco com margem nas bordas, sem repetir cena contínua + caixas de texto) + corpo (AD pronto a partir de um corte,
ou corpo novo montado do banco sobre uma narração).

1) Banco de tomadas de cada vídeo-fonte (scdet, grupos de cena contínua, folha de contato e transcrição por palavra):
     python gerar_variacao.py banco "AD 20 - X.mp4" --saida fontes/20/banco.json [--ate 90] [--idioma es] [--sem-whisper]
2) Música sem voz de um trecho (demucs local, grátis), para o fundo do gancho emendar sem pulo no corpo:
     python gerar_variacao.py fundo "AD 20 - X.mp4" --ate 10.933 --saida fontes/20/bed.wav
3) Montar a variação descrita num config JSON (ver exemplos/variacao_exemplo.json):
     python gerar_variacao.py montar var01.json [--semente 7] [--montar-ad]

Config (caminhos relativos à pasta do JSON):
{
 "saida": "VARIACOES/VAR 01 - G1 x AD20.mp4",
 "resolucao": "720",                                   // "720" (720x1280) ou "1080"
 "limite_mb": 30,
 "bancos": {"20": "fontes/20/banco.json", "25": "fontes/25/banco.json"},   // nome -> banco (ele guarda o vídeo-fonte)
 "fundos": {"1": "sep/orig_01/no_vocals.wav"},         // opcional: música sem voz alinhada a cada fonte (modo B)
 "gancho": {
   "fala": "voz/20_G1.mp3",                            // narração do gancho (+ .alinhamento.json do tts_elevenlabs)
   "texto": "...", "voz": "voice_id",                  // se "fala" não existir e houver texto+voz, gera por TTS (pago)
   "lead": 0.12, "cauda": 0.30,                        // silêncio antes/depois da fala
   "pool": [["20", 0, 10.9], ["25", 0, 7.9]],          // tomadas candidatas [banco, de, até] (1ª janela = preferida)
   // OU "trecho": ["1", 0.133, 4.2]                   // trecho fixo de uma fonte (gancho do próprio vídeo)
   "tomada": [1.5, 2.5],                               // duração sorteada de cada tomada
   "caixas": {"cy": 866, "min_w": 540, "min_h": 100, "px": 46},     // caixa branca por frase (cobre legenda queimada)
   // OU "caixa_fixa": {"linhas": ["..."], "px": 29, "cy": 235, "de": 0, "ate": 3, "negrito": true}
   "fundo": "fontes/20/bed.wav",                       // música: últimos s de um wav (modo A) | {"fonte": "1"} mesmo
   "fundo_vol": 1.0                                    //   trecho da fonte (com "trecho") | null = sem música
 },
 "corpo": {"video": "AD 20 - X.mp4", "corte": 10.933, "ganho_db": null},    // modo A: AD pronto a partir do corte
 // modo B: corpo novo = narração + tomadas do banco (+ fundo musical de uma fonte a partir de um instante)
 // "corpo": {"narracao": "voz/corpo_B.mp3", "pool": [["1", 0, 999], ["2", 12, 999]], "tomada": [3.0, 4.3],
 //           "fundo": ["3", 3.3], "fundo_vol": 1.6, "abertura": [["1", 44, 50]], "fechamento": [["3", 40, 44]],
 //           "excluir": [["2", 12.6, 19.7]], "cauda": 0.8},
 "faixa": {"linhas": ["Solo con fines demostrativos."], "topo": 1150},      // aviso opaco no rodapé (opcional)
 "receita": {"estilo": "drop", "legenda": {"chaves": [...]}, "selo": {...}, "cta": {...}}   // modo B: p/ montar_ad.py
}
Saída: modo A grava o arquivo final (finalizar.py: limite de MB + folha de frames). Modo B grava corpo.mp4,
alinhamento.json e receita_final.json na pasta de trabalho (trab/<config>/) e, com --montar-ad, roda o montar_ad.py.
Em ambos, info.json guarda as tomadas sorteadas e a semente (para reproduzir).
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from comum import COR, FONTS, FPS, dur, emoji_font, resolucao, run  # noqa: E402

FB, FM = str(FONTS / "Poppins-Bold.ttf"), str(FONTS / "Poppins-Medium.ttf")
MARGEM = (0.15, 0.20)   # corte do scdet não é exato: margem no início/fim de cada tomada


# ================================================================= banco
def cortes_scdet(video: str, ate: float | None, limiar: float = 10.0) -> list[float]:
    cmd = ["ffmpeg", "-hide_banner"] + (["-t", str(ate)] if ate else []) + \
          ["-i", video, "-an", "-vf", f"scdet=threshold={limiar},metadata=print", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [float(l.split("lavfi.scd.time:")[1]) for l in r.stderr.splitlines() if "lavfi.scd.time:" in l]


def banco(a):
    video = str(Path(a.video).resolve())
    saida = Path(a.saida) if a.saida else Path(video).with_suffix("").with_name(Path(video).stem + "_banco.json")
    saida.parent.mkdir(parents=True, exist_ok=True)
    fim = min(a.ate, dur(video)) if a.ate else dur(video)
    cortes = [0.0] + [c for c in cortes_scdet(video, a.ate, a.limiar) if c < fim] + [fim]
    cap = cv2.VideoCapture(video)

    def quadro(t):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, im = cap.read()
        return cv2.resize(im, (90, 160)) if ok else None

    def hist(im):
        h = cv2.calcHist([cv2.cvtColor(im, cv2.COLOR_BGR2HSV)], [0, 1], None, [30, 32], [0, 180, 0, 256])
        return cv2.normalize(h, h).flatten()

    tomadas, g, q_ant = [], 0, None
    for i in range(len(cortes) - 1):
        ini, fm = cortes[i], cortes[i + 1]
        if fm - ini < 0.1:
            continue
        q0, q1 = quadro(ini + 0.1), quadro(max(ini + 0.1, fm - 0.15))
        t = {"ini": round(ini, 3), "fim": round(fm, 3), "dur": round(fm - ini, 3)}
        if tomadas and q0 is not None and q_ant is not None:
            c = float(cv2.compareHist(hist(q_ant), hist(q0), cv2.HISTCMP_CORREL))
            t["sim_ant"] = round(c, 3)
            if c < a.sim:   # fim da anterior parecido com início desta = mesma cena contínua (mesmo grupo)
                g += 1
        t["grupo"] = g
        tomadas.append(t)
        q_ant = q1
    out = {"video": video, "ate": round(fim, 3), "tomadas": tomadas}
    print(f"{len(tomadas)} tomadas, {g + 1} grupos em {Path(video).name} (até {fim:.1f}s)")

    if a.folha:
        subprocess.run([sys.executable, str(Path(__file__).parent / "folhas_contato.py"), "--cada", "1", "--de", "0",
                        "--ate", str(fim), "--saida", str(saida.parent / "folha"), video], check=True, capture_output=True)
    if not a.sem_whisper:
        from faster_whisper import WhisperModel
        wav = saida.parent / "_banco_tmp.wav"
        run(["ffmpeg", "-t", str(fim), "-i", video, "-ac", "1", "-ar", "16000", wav])
        m = WhisperModel(a.modelo, device="cpu", compute_type="int8", cpu_threads=4)
        segs, _ = m.transcribe(str(wav), language=a.idioma, word_timestamps=True, vad_filter=False)
        out["palavras"] = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in (s.words or [])]
        wav.unlink(missing_ok=True)
        print(" ".join(f"{w}[{t0:.1f}]" for w, t0, _ in out["palavras"][:60]))
    json.dump(out, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("banco:", saida)


# ================================================================= fundo (demucs)
def fundo(a):
    saida = Path(a.saida).resolve()
    saida.parent.mkdir(parents=True, exist_ok=True)
    tmp = saida.parent / "_pre_demucs"
    tmp.mkdir(exist_ok=True)
    pre = tmp / "pre.wav"
    corte = ["-t", f"{a.ate:.3f}"] if a.ate else []
    run(["ffmpeg", *(["-ss", f"{a.de:.3f}"] if a.de else []), *corte, "-i", a.video, "-vn", "-ac", "2", "-ar", "44100", pre])
    env = dict(os.environ, OMP_NUM_THREADS="4", MKL_NUM_THREADS="4")
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals", "-n", "htdemucs", "-o", str(tmp), str(pre)],
                   check=True, env=env)
    (tmp / "htdemucs" / "pre" / "no_vocals.wav").replace(saida)
    print("fundo sem voz:", saida)


# ================================================================= utilidades de montagem
def lufs(f, ss=None, t=None) -> float:
    cmd = ["ffmpeg", "-hide_banner", "-nostats"] + (["-ss", str(ss)] if ss is not None else []) + \
          (["-t", str(t)] if t is not None else []) + ["-i", str(f), "-vn", "-af", "ebur128", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])


def alinhamento(mp3: Path) -> dict:
    al = json.load(open(str(mp3.with_suffix("")) + ".alinhamento.json", encoding="utf-8"))
    return al.get("alignment") or al.get("normalized_alignment") or al


def frases_do_alinhamento(al: dict) -> list[tuple[str, float]]:
    """[(frase, início em s), ...] separando em . ? !"""
    out, buf, ini = [], "", None
    for ch, t0 in zip(al["characters"], al["character_start_times_seconds"]):
        if ini is None and ch.strip():
            ini = t0
        buf += ch
        if ch in ".?!" and buf.strip():
            out.append((buf.strip(), ini))
            buf, ini = "", None
    if buf.strip():
        out.append((buf.strip(), ini or 0.0))
    return out


def e_emoji(ch: str) -> bool:
    return ord(ch) > 0x2000 and ch not in "…–—“”‘’¡¿"


def caixa_texto(linhas, destino, W, H, cy, px=46, min_w=0, min_h=0, negrito=True, maxw=None):
    """Caixa branca arredondada (estilo TikTok) centrada em cy, texto preto, emoji colorido; quebra linhas longas."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FB if negrito else FM, px)
    ef = emoji_font()
    fe = ImageFont.truetype(str(ef), px) if ef else f
    larg = lambda s: sum(d.textlength(c, font=fe if e_emoji(c) else f) for c in s)  # noqa: E731
    maxw = maxw or W * 0.86
    quebradas = []
    for l in linhas:
        cur = ""
        for w in l.split():
            tst = (cur + " " + w).strip()
            if larg(tst) > maxw and cur:
                quebradas.append(cur)
                cur = w
            else:
                cur = tst
        quebradas.append(cur)
    lh = int(px * 1.3)
    ws = [larg(l) for l in quebradas]
    bw = max(max(ws) + 44, min_w)
    bh = max(lh * len(ws) + 26, min_h)
    x0, y0 = W / 2 - bw / 2, cy - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=16, fill=(255, 255, 255, 255))
    ty = cy - lh * len(ws) / 2 + 4
    for l, w in zip(quebradas, ws):
        x = W / 2 - w / 2
        for c in l:
            if e_emoji(c) and ef:
                d.text((x, ty + int(px * 0.05)), c, font=fe, embedded_color=True)
                x += d.textlength(c, font=fe)
            else:
                d.text((x, ty), c, font=f, fill=(0, 0, 0, 255))
                x += d.textlength(c, font=f)
        ty += lh
    img.save(destino)
    return str(destino)


def faixa_aviso(linhas, destino, W, H, topo, px=19):
    """Faixa escura quase opaca (alpha 252) do `topo` até o rodapé, com o aviso em texto pequeno."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    g = 40
    for y in range(topo - g, H):
        a = 252 if y >= topo else int(252 * (y - (topo - g)) / g)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    f = ImageFont.truetype(FM, px)
    lh = int(px * 1.32)
    y = topo + (H - topo - lh * len(linhas)) / 2
    for l in linhas:
        d.text(((W - d.textlength(l, font=f)) / 2, y), l, font=f, fill=(235, 235, 235, 255))
        y += lh
    img.save(destino)
    return str(destino)


def tomadas_em(bancos: dict, janelas, min_dur=0.9):
    """Tomadas do banco inteiramente dentro das janelas [nome, de, até], já com margem nas bordas."""
    out = []
    for nome, de, ate in janelas:
        if nome not in bancos:
            raise SystemExit(f"banco '{nome}' não está em \"bancos\"")
        for k, t in enumerate(bancos[nome]["tomadas"]):
            if t["ini"] < de - 0.01 or t["fim"] > ate + 0.01:
                continue
            a0, a1 = t["ini"] + MARGEM[0], t["fim"] - MARGEM[1]
            if a1 - a0 >= min_dur:
                out.append({"src": nome, "a0": round(a0, 3), "a1": round(a1, 3), "grupo": f"{nome}:{t['grupo']}", "k": k})
    return out


def dentro(t, janelas) -> bool:
    return any(t["src"] == n and t["a0"] >= de - 0.2 and t["a1"] <= ate + 0.2 for n, de, ate in janelas)


def escolher(cands, alvo, tmin, tmax, rnd, usados, ult, evitar_src=True, sobra_min=0.8, l_min=0.8):
    """Preenche `alvo` s com tomadas de `cands` (ordem dada), sem repetir grupo e evitando fonte seguida.
    Devolve (segs, falta)."""
    segs, falta = [], alvo
    for c in cands:
        if falta <= 0.01:
            break
        if c["grupo"] in usados or c["grupo"] == ult["grupo"] or (evitar_src and c["src"] == ult["src"] and
                                                                  any(x["src"] != c["src"] for x in cands if x["grupo"] not in usados)):
            continue
        disp = c["a1"] - c["a0"]
        L = min(disp, rnd.uniform(tmin, tmax))
        if falta - L < sobra_min:      # não deixar sobra curta: absorve na tomada atual se couber
            L = falta if falta <= disp else min(disp, falta - sobra_min)
        L = round(min(L, falta) * FPS) / FPS
        if L < l_min - 1e-6:
            continue
        a0 = c["a0"] + (disp - L) / 2
        segs.append({"src": c["src"], "ini": round(a0, 3), "dur": round(L, 4)})
        usados.add(c["grupo"])
        ult["grupo"], ult["src"] = c["grupo"], c["src"]
        falta = round(falta - L, 4)
    return segs, falta


def cortar_segs(segs, bancos, T, W, H, prefixo) -> Path:
    """Corta cada tomada (quadros exatos) e concatena em <T>/<prefixo>_v.mp4 (sem áudio)."""
    lista = []
    for k, s in enumerate(segs):
        o = T / f"{prefixo}{k:02d}.mp4"
        n = int(round(s["dur"] * FPS))
        run(["ffmpeg", "-ss", f"{s['ini']:.3f}", "-i", bancos[s["src"]]["video"], "-an", "-frames:v", n,
             "-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1",
             "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
        lista.append(f"file '{o.as_posix()}'")
    lst = T / f"{prefixo}lista.txt"
    lst.write_text("\n".join(lista), encoding="utf-8")
    out = T / f"{prefixo}_v.mp4"
    run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])
    return out


# ================================================================= montar
def montar(a):
    cfg_path = Path(a.config).resolve()
    R = json.load(open(cfg_path, encoding="utf-8"))
    D = cfg_path.parent
    P = lambda p: str((D / p).resolve()) if p and not Path(p).is_absolute() else p  # noqa: E731
    seed = a.semente if a.semente is not None else R.get("semente", 7)
    rnd = random.Random(seed)
    W, H = resolucao(R.get("resolucao", "720"))
    T = Path(P(R.get("trab") or f"trab/{cfg_path.stem}"))
    T.mkdir(parents=True, exist_ok=True)
    bancos = {}
    for nome, bp in R.get("bancos", {}).items():
        b = json.load(open(P(bp), encoding="utf-8"))
        if not Path(b["video"]).exists():
            raise SystemExit(f"vídeo do banco '{nome}' não existe: {b['video']}")
        bancos[nome] = b
    fundos = {k: P(v) for k, v in R.get("fundos", {}).items()}
    G, C = R["gancho"], R["corpo"]
    modo_a = "video" in C
    info = {"config": str(cfg_path), "semente": seed, "modo": "A" if modo_a else "B"}

    # ---------- 1) fala do gancho
    fala = Path(P(G["fala"])) if G.get("fala") else None
    if fala and not fala.exists():
        if not (G.get("texto") and G.get("voz")):
            raise SystemExit(f"fala do gancho não existe: {fala} (dê texto+voz para gerar por TTS)")
        import tts_elevenlabs as TTS
        print(f"TTS ElevenLabs: {len(G['texto'])} caracteres (~US$ {len(G['texto']) / 1000 * 0.165:.3f}) -> {fala.name}")
        fala.parent.mkdir(parents=True, exist_ok=True)
        TTS.gerar(G["texto"], str(fala), voz=G["voz"])
    lead, cauda = G.get("lead", 0.12), G.get("cauda", 0.30)
    d_fala = dur(fala) if fala else 0.0
    al_fala = alinhamento(fala) if fala else None

    # ---------- 2) tomadas do gancho
    if G.get("trecho"):
        src, g_ini, g_fim = G["trecho"]
        Hd = max(g_fim - g_ini, (lead + d_fala + cauda) if fala else 0.0)
        Hd = round(Hd * FPS) / FPS
        segs_g = [{"src": src, "ini": round(g_ini, 3), "dur": Hd}]
        t_fala = lead
    else:
        Hd = round((lead + d_fala + cauda) * FPS) / FPS
        pools = [tomadas_em(bancos, [j]) for j in G["pool"]]
        for p in pools:
            rnd.shuffle(p)
        cand = pools[0] + [x for p in pools[1:] for x in p] if pools else []
        tmin, tmax = G.get("tomada", [1.5, 2.5])
        segs_g, falta = escolher(cand, Hd, tmin, tmax, rnd, set(), {"grupo": None, "src": None}, evitar_src=False)
        if falta > 0.01:
            raise SystemExit(f"banco insuficiente para o gancho ({falta:.2f}s faltando)")
        t_fala = lead
    gancho_v = cortar_segs(segs_g, bancos, T, W, H, "g")
    info["gancho"] = {"Hd": Hd, "fala_s": round(d_fala, 2), "tomadas": segs_g}

    # ---------- 3) caixas de texto do gancho
    ovs = []   # (png, de, ate)
    if G.get("caixas") and al_fala:
        cx = G["caixas"]
        frases = frases_do_alinhamento(al_fala)
        for k, (txt, t0) in enumerate(frases):
            de = 0 if k == 0 else round(t_fala + t0 - 0.05, 3)
            ate = Hd + 1 if k == len(frases) - 1 else round(t_fala + frases[k + 1][1] - 0.05, 3)
            png = caixa_texto([txt], T / f"cx{k}.png", W, H, cx["cy"], cx.get("px", 46), cx.get("min_w", 0),
                              cx.get("min_h", 0), cx.get("negrito", True))
            ovs.append((png, de, ate))
        info["gancho"]["frases"] = frases
    if G.get("caixa_fixa"):
        cf = G["caixa_fixa"]
        png = caixa_texto(cf["linhas"], T / "caixa_fixa.png", W, H, cf["cy"], cf.get("px", 29), cf.get("cobrir_w", 0),
                          cf.get("cobrir_h", 0), cf.get("negrito", True))
        ovs.append((png, cf.get("de", 0), cf.get("ate", Hd)))

    # ---------- 4) áudio do gancho (música + fala)
    fg = G.get("fundo")
    gvol = G.get("fundo_vol", 1.0)
    fbg_in, fbg_fc = [], None
    if isinstance(fg, dict) and fg.get("fonte"):
        if not G.get("trecho"):
            raise SystemExit('gancho.fundo {"fonte": ...} só vale com "trecho"')
        fbg_in = ["-i", fundos[fg["fonte"]]]
        fbg_fc = f"[1:a]atrim={g_ini:.3f}:{g_ini + Hd:.3f},asetpts=PTS-STARTPTS,volume={gvol},aresample=48000[bg]"
    elif isinstance(fg, str):
        bed = P(fg)
        bdur = dur(bed)
        fbg_in = ["-i", bed]
        if bdur >= Hd:     # últimos Hd s da música: emenda contínua com o corpo (modo A)
            fbg_fc = f"[1:a]atrim={bdur - Hd:.3f}:{bdur:.3f},asetpts=PTS-STARTPTS,volume={gvol},aresample=48000[bg]"
        else:
            extra = Hd - bdur + 0.3
            fbg_fc = (f"[1:a]asplit[b1][b2];[b1]atrim=0:{extra:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={extra - 0.3:.3f}:d=0.3[e];"
                      f"[b2]afade=t=in:d=0.3[m];[e][m]acrossfade=d=0.3[bgx];[bgx]atrim=0:{Hd:.3f},volume={gvol},aresample=48000[bg]")
    if fbg_fc is None:
        fbg_fc = f"anullsrc=r=48000:cl=stereo,atrim=0:{Hd:.3f}[bg]"
    ganho = 0.0
    if fala:
        if modo_a:
            corpo_I = C.get("lufs") or lufs(P(C["video"]), C["corte"], 30)
            ganho = C["ganho_db"] if C.get("ganho_db") is not None else corpo_I - lufs(fala) - 0.5
        n_fala = 1 + (1 if fbg_in else 0)
        fala_in = ["-i", str(fala)]
        ffala = (f"[{n_fala}:a]aresample=48000,aformat=channel_layouts=stereo,volume={ganho:.2f}dB,"
                 f"adelay={int(t_fala * 1000)}|{int(t_fala * 1000)}[nv]")
        fmix = f"[bg][nv]amix=inputs=2:duration=first:normalize=0,aresample=48000,atrim=0:{Hd:.3f}[ga]"
    else:
        fala_in, ffala, fmix = [], None, f"[bg]atrim=0:{Hd:.3f}[ga]"
    ins = ["-i", str(gancho_v), *fbg_in, *fala_in]
    fc = [fbg_fc] + ([ffala] if ffala else []) + [fmix]
    n_in = 1 + (1 if fbg_in else 0) + (1 if fala_in else 0)
    vin = "[0:v]"
    for k, (png, de, ate) in enumerate(ovs):
        ins += ["-loop", "1", "-t", f"{Hd:.3f}", "-i", png]
        fc.append(f"{vin}[{n_in + k}:v]overlay=0:0:enable='between(t,{de},{ate})'[o{k}]")
        vin = f"[o{k}]"
    n_in += len(ovs)
    fc.append(f"{vin}fps={FPS},format=yuv420p,setsar=1[gv]")
    gancho_av = T / "gancho.mp4"
    run(["ffmpeg", *ins, "-filter_complex", ";".join(fc), "-map", "[gv]", "-map", "[ga]", "-t", f"{Hd:.3f}",
         "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", gancho_av])
    info["gancho"]["ganho_db"] = round(ganho, 2)

    # ---------- 5) corpo
    faixa_png = None
    if R.get("faixa"):
        faixa_png = faixa_aviso(R["faixa"]["linhas"], T / "faixa.png", W, H, R["faixa"].get("topo", int(H * 0.9)),
                                R["faixa"].get("px", 19))

    if modo_a:
        fonte = P(C["video"])
        corte = float(C["corte"])
        DF = dur(fonte)
        # corta o silêncio da cauda do AD (deixa no máx. 0,6 s)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{max(0, DF - 8):.2f}", "-i", fonte, "-vn", "-af",
                            "silencedetect=noise=-45dB:d=0.6", "-f", "null", "-"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace").stderr
        ss = [float(l.split("silence_start:")[1]) for l in r.splitlines() if "silence_start" in l]
        es = [float(l.split("silence_end:")[1].split("|")[0]) for l in r.splitlines() if "silence_end" in l]
        fim_corpo = DF
        if ss and (len(es) < len(ss) or es[-1] > 8 - 0.1):
            fim_corpo = max(0, DF - 8) + ss[-1] + 0.6
        fc = [f"[0:v]fps={FPS},scale={W}:{H},setsar=1,format=yuv420p[gv]",
              f"[1:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,format=yuv420p[cv]",
              "[0:a]aresample=48000,aformat=channel_layouts=stereo[ga]",
              "[1:a]aresample=48000,aformat=channel_layouts=stereo[ca]",
              "[gv][ga][cv][ca]concat=n=2:v=1:a=1[v0][a]"]
        ins = ["-i", str(gancho_av), "-ss", f"{corte:.3f}", "-t", f"{fim_corpo - corte:.3f}", "-i", fonte]
        vk = "[v0]"
        if faixa_png:
            ins += ["-i", faixa_png]
            fc.append("[v0][2:v]overlay=0:0[v1]")
            vk = "[v1]"
        bruto = T / "bruto.mp4"
        run(["ffmpeg", *ins, "-filter_complex", ";".join(fc), "-map", vk, "-map", "[a]",
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", bruto])
        import finalizar as FIN
        saida = Path(P(R["saida"]))
        saida.parent.mkdir(parents=True, exist_ok=True)
        # entrega: bitrate pelo limite de MB (finalizar.encode é só 1080p; aqui respeita a resolução do config)
        v_kbps, _ = FIN.bitrate_alvo(dur(bruto), R.get("limite_mb", 30),
                                     piso=FIN.QUALIDADE_MIN_720_KBPS if W == 720 else None)
        run(["ffmpeg", "-i", bruto, "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1",
             "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
             "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps * 1.5)}k", "-bufsize", f"{v_kbps * 2}k",
             "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida])
        FIN.revisar(str(saida), str(saida.with_name(saida.stem + "_frames.jpg")), esperado=(W, H))
        info.update({"corpo": {"video": fonte, "corte": corte, "fim": round(fim_corpo, 3)}, "saida": str(saida)})
        json.dump(info, open(T / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"ok | gancho {Hd:.2f}s ({len(segs_g)} tomadas, ganho {ganho:+.1f} dB) | total {dur(saida):.1f}s | {saida}")
        return

    # ---------- modo B: corpo novo = narração + tomadas do banco
    narr = Path(P(C["narracao"]))
    al_c = alinhamento(narr)
    d_narr = dur(narr)
    # narração completa (fala do gancho + pausa + narração do corpo) e alinhamento emendado
    al = {"characters": [], "character_start_times_seconds": [], "character_end_times_seconds": []}
    cursor = 0.0
    narr_full = T / "narr.wav"
    if fala:
        for k in al:
            al[k] += al_fala[k]
        cursor = d_fala + 0.3
        al["characters"].append(" ")
        al["character_start_times_seconds"].append(cursor - 0.3)
        al["character_end_times_seconds"].append(cursor - 0.3)
        run(["ffmpeg", "-i", fala, "-i", narr, "-filter_complex",
             "[0:a]aresample=48000,aformat=channel_layouts=mono,apad=pad_dur=0.3[x];[1:a]aresample=48000,aformat=channel_layouts=mono[y];"
             "[x][y]concat=n=2:v=0:a=1", narr_full])
        t_narr = t_fala
    else:
        run(["ffmpeg", "-i", narr, "-ar", "48000", "-ac", "1", narr_full])
        t_narr = Hd
    al["characters"] += al_c["characters"]
    al["character_start_times_seconds"] += [t + cursor for t in al_c["character_start_times_seconds"]]
    al["character_end_times_seconds"] += [t + cursor for t in al_c["character_end_times_seconds"]]
    for k in ("character_start_times_seconds", "character_end_times_seconds"):
        al[k] = [round(t + t_narr, 3) for t in al[k]]
    json.dump(al, open(T / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    d_full = dur(narr_full)
    total = t_narr + d_full + C.get("cauda", 0.8)
    alvo = total - Hd

    usados, ult = set(), {"grupo": None, "src": segs_g[-1]["src"]}
    for s in segs_g:   # tomadas do gancho não voltam no corpo
        for c in tomadas_em(bancos, [[s["src"], s["ini"] - 1, s["ini"] + s["dur"] + 1]]):
            usados.add(c["grupo"])
    tmin, tmax = C.get("tomada", [3.0, 4.3])
    segs_c = []
    if C.get("abertura"):
        ab = [c for c in tomadas_em(bancos, C["abertura"]) if c["src"] != ult["src"]] or tomadas_em(bancos, C["abertura"])
        c = rnd.choice(ab)
        L = min(c["a1"] - c["a0"], 4.5)
        a0 = c["a0"] + (c["a1"] - c["a0"] - L) / 2
        segs_c.append({"src": c["src"], "ini": round(a0, 3), "dur": round(L * FPS) / FPS})
        usados.add(c["grupo"])
        ult = {"grupo": c["grupo"], "src": c["src"]}
        alvo -= segs_c[-1]["dur"]
    fech = tomadas_em(bancos, C["fechamento"]) if C.get("fechamento") else []
    reserva = 3.5 if fech else 0.0
    meio = [c for c in tomadas_em(bancos, C["pool"])
            if not dentro(c, C.get("excluir", [])) and not dentro(c, C.get("abertura", [])) and not dentro(c, C.get("fechamento", []))]
    rnd.shuffle(meio)
    segs_m, falta = escolher(meio, alvo - reserva, tmin, tmax, rnd, usados, ult, evitar_src=True, sobra_min=1.3, l_min=1.3)
    segs_c += segs_m
    alvo = falta + reserva
    if fech:
        rnd.shuffle(fech)
        c = next((x for x in fech if x["src"] != ult["src"]), fech[0])
        L = max(1.5, min(c["a1"] - c["a0"], alvo))
        a0 = c["a0"] + max(0, (c["a1"] - c["a0"]) - L)
        segs_c.append({"src": c["src"], "ini": round(a0, 3), "dur": round(L * FPS) / FPS})
    elif falta > 0.5:
        print(f"aviso: banco insuficiente, corpo {falta:.1f}s mais curto que a narração")
    corpo_v = cortar_segs(segs_c, bancos, T, W, H, "c")
    dv_c = dur(corpo_v)
    info["corpo"] = {"narracao": str(narr), "tomadas": segs_c, "t_narr": t_narr, "dur": round(dv_c, 3)}

    # áudio do corpo: cama contínua da fonte + narração
    fb = C.get("fundo")
    ins = ["-i", str(gancho_av), "-i", str(corpo_v), "-i", str(narr_full)]
    fc = [f"[1:v]fps={FPS},setsar=1,format=yuv420p[cv]"]
    if fb:
        ins += ["-i", fundos[fb[0]]]
        fc.append(f"[3:a]atrim=start={fb[1]},asetpts=PTS-STARTPTS,aloop=loop=3:size=2e9,atrim=0:{dv_c + 0.5:.3f},"
                  f"volume={C.get('fundo_vol', 1.6)},afade=t=in:d=0.4,aresample=48000,aformat=channel_layouts=stereo[cb]")
    else:
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{dv_c:.3f}[cb]")
    fc += ["[0:a]aresample=48000,aformat=channel_layouts=stereo[ga]",
           "[ga][cb]concat=n=2:v=0:a=1[bgm]",
           f"[2:a]adelay={int(t_narr * 1000)}|{int(t_narr * 1000)},aresample=48000,aformat=channel_layouts=stereo[nv]",
           "[bgm][nv]amix=inputs=2:duration=first:normalize=0[a]",
           "[0:v][cv]concat=n=2:v=1:a=0[v0]"]
    vk = "[v0]"
    if faixa_png:
        ins += ["-i", faixa_png]
        fc.append(f"[v0][{4 if fb else 3}:v]overlay=0:0[v1]")
        vk = "[v1]"
    corpo = T / "corpo.mp4"
    run(["ffmpeg", *ins, "-filter_complex", ";".join(fc), "-map", vk, "-map", "[a]", "-t", f"{Hd + dv_c:.3f}",
         "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", corpo])

    rec = {"saida": P(R["saida"]), "estilo": "drop", "corpo": str(corpo), "resolucao": str(R.get("resolucao", "720")),
           "limite_mb": R.get("limite_mb", 30), "legenda": {"fonte": "alinhamento:" + str(T / "alinhamento.json")}}
    for k, v in (R.get("receita") or {}).items():
        if k == "legenda":
            rec["legenda"].update(v)
        else:
            rec[k] = v
    json.dump(rec, open(T / "receita_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    info["saida"] = str(T / "corpo.mp4")
    json.dump(info, open(T / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ok | gancho {Hd:.2f}s ({len(segs_g)} tomadas) + corpo {dv_c:.1f}s ({len(segs_c)} tomadas) | "
          f"narração {t_narr:.2f}-{t_narr + d_full:.2f}s | {corpo}")
    print(f"receita: {T / 'receita_final.json'}  ->  python montar_ad.py \"{T / 'receita_final.json'}\"")
    if a.montar_ad:
        import montar_ad as MA
        import montar_ad_rapido as RAP
        if RAP.elegivel(rec):   # caminho de 1 passada (respeita "resolucao")
            RAP.montar(rec, T)
        else:
            MA.montar(rec, T)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("banco", help="banco de tomadas (scdet) + transcrição por palavra")
    b.add_argument("video")
    b.add_argument("--saida", help="banco.json (padrão: <video>_banco.json)")
    b.add_argument("--ate", type=float, default=None, help="só os primeiros N s")
    b.add_argument("--limiar", type=float, default=10.0, help="scdet threshold")
    b.add_argument("--sim", type=float, default=0.70, help="similaridade (histograma) abaixo da qual começa outro grupo")
    b.add_argument("--idioma", default="es")
    b.add_argument("--modelo", default="small")
    b.add_argument("--sem-whisper", action="store_true")
    b.add_argument("--folha", action="store_true", help="gera folha de contato 1 q/s ao lado do banco")
    b.set_defaults(fn=banco)
    f = sub.add_parser("fundo", help="música sem voz (demucs) de um trecho do vídeo")
    f.add_argument("video")
    f.add_argument("--saida", required=True)
    f.add_argument("--de", type=float, default=0.0)
    f.add_argument("--ate", type=float, default=None)
    f.set_defaults(fn=fundo)
    m = sub.add_parser("montar", help="monta a variação do config JSON")
    m.add_argument("config")
    m.add_argument("--semente", type=int, default=None)
    m.add_argument("--montar-ad", action="store_true", help="modo B: já roda o montar_ad.py com a receita gerada")
    m.set_defaults(fn=montar)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
