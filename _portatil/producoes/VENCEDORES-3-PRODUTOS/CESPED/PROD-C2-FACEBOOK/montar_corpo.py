# -*- coding: utf-8 -*-
"""Monta o corpo do AD CÉSPED C2 «Expuesto en Facebook» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Adaptado do montar_corpo.py do P1 (perfumes). Saída: corpo.mp4 e corpo.alinhamento.json."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU, CE = P / "takes", P / "audio", P / "cenas"
BANCO = P.parent / "BANCO"
V1, V2 = BANCO / "V1_720.mp4", BANCO / "V2_limpo_13-46.mp4"
SELO = BANCO / "overlay_selo_cesped.png"
WK = P / "_seg"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
ZOOM = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
# (os tempos do gancho/persona saem do QA dos takes: ver _tr_takes.json)
G = json.load(open(P / "_tempos.json", encoding="utf-8"))


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur, overlay=None):
    """partes: [(arquivo, ss, t, vf_extra, selo?)]  audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None)]"""
    ins, fc = [], []
    for i, (f, ss, t, vx, _s) in enumerate(partes):
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t), "-i", str(f)]
        fc.append(f"[{i}:v]{BASE}{(',' + vx) if vx else ''},trim=duration={t},setpts=PTS-STARTPTS[v{i}]")
    n = len(partes); k = n
    # selo só nas partes marcadas (cenas de IA)
    for i, (f, ss, t, vx, s) in enumerate(partes):
        if s:
            ins += ["-loop", "1", "-t", str(t), "-i", str(SELO)]
            fc.append(f"[v{i}][{k}:v]overlay=0:0:shortest=1,trim=duration={t},setpts=PTS-STARTPTS[w{i}]"); k += 1
        else:
            fc.append(f"[v{i}]null[w{i}]")
    fc.append("".join(f"[w{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]")
    al = []
    for j, (f, ss, atraso, d) in enumerate(audios):
        ins += (["-ss", str(ss)] + (["-t", str(d)] if d else []) + ["-i", str(f)])
        ms = int(atraso * 1000)
        fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms}[a{j}]"); al.append(f"[a{j}]"); k += 1
    ins += ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    fc.append("".join(al) + f"[{k}:a]amix=inputs={len(al) + 1}:normalize=0:duration=longest,atrim=duration={dur}[ao]")
    out = WK / f"{nome}.mp4"
    run([*ins, "-filter_complex", ";".join(fc), "-map", "[vc]", "-map", "[ao]", "-t", str(dur), *ENC, str(out)])
    return out


ALI = {"characters": [], "character_start_times_seconds": [], "character_end_times_seconds": []}


def ali_palavras(pal, t0):
    for i, (w, a, b) in enumerate(pal):
        s = w + " "
        step = (b - a) / max(len(w), 1)
        for c_i, ch in enumerate(s):
            ALI["characters"].append(ch)
            st = t0 + a + min(c_i, len(w)) * step
            ALI["character_start_times_seconds"].append(round(st, 3))
            ALI["character_end_times_seconds"].append(round(st + step, 3))


def ali_tts(arq, t0):
    d = json.load(open(arq, encoding="utf-8"))
    for ch, a, b in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
        ALI["characters"].append(ch); ALI["character_start_times_seconds"].append(round(t0 + a, 3))
        ALI["character_end_times_seconds"].append(round(t0 + b, 3))
    ALI["characters"].append(" "); ALI["character_start_times_seconds"].append(ALI["character_end_times_seconds"][-1])
    ALI["character_end_times_seconds"].append(ALI["character_end_times_seconds"][-1])


segs, t = [], 0.0
# 1 gancho: tela do post (zoom) + take Seedance com a fala (voz Eduardo por STS); jump cut na pausa longa do «…»
g = G["gancho"]; tela = g["tela"]; (a1, b1), (a2, b2) = g["cortes"]
segs.append(bloco("01_gancho", [(CE / "T1_post_gancho.png", 0, tela, ZOOM, False),
                                (T / "V1_gancho.mp4", a1, b1 - a1, None, True), (T / "V1_gancho.mp4", a2, b2 - a2, None, True)],
                  [(AU / "v1_eduardo.mp3", a1, tela, b1 - a1), (AU / "v1_eduardo.mp3", a2, tela + b1 - a1, b2 - a2)],
                  tela + (b1 - a1) + (b2 - a2)))
def _gt(x): return tela + (x - a1 if x <= b1 else (b1 - a1) + x - a2)
ali_palavras([(w, _gt(a), _gt(b)) for w, a, b in g["pal"]], t); t += tela + (b1 - a1) + (b2 - a2)
# 2 persona: selfie Seedance (voz Eduardo por STS, mesmo tempo)
p = G["persona"]
segs.append(bloco("02_persona", [(T / "V2_persona.mp4", p["ss"], p["dur"], None, True)],
                  [(AU / "v2_eduardo.mp3", p["ss"], 0, p["dur"])], p["dur"]))
ali_palavras([(w, a - p["ss"], b - p["ss"]) for w, a, b in p["pal"]], t); t += p["dur"]
# 3 antes/depois real (V1 0–5,5) + «Hasta que probé esta.»
segs.append(bloco("03_antes", [(V1, 0, 5.4, "setpts=PTS/1.25", False)], [(AU / "L3_antes.mp3", 0, 0.3, None)], 4.32))
ali_tts(AU / "L3_antes.alinhamento.json", t + 0.3); t += 4.32
# 4 mecanismo (C par: começa pelo V1) — cortes nas palavras da narração
m = [(V1, 10.8, 4.7, None, False),   # borda: cortapasto, orilladora y bordeadora en uno
     (V1, 6.1, 3.5, None, False),    # rodas: una sola mano
     (V1, 18.2, 4.6, None, False),   # faixas no mato alto: cuchilla de metal / hilos
     (V2, 1.4, 1.7, None, False),    # deck (V2 7,6–9,2 e 3,2–3,6 têm fantasma do LaMa)
     (V1, 25.0, 0.5, None, False),   # gramado lateral (trecho do V1 ainda não usado)
     (V2, 22.8, 0.7, None, False),   # kit na mesa: dos baterías (pula o fantasma 23,6–23,9)
     (V2, 24.0, 0.9, None, False)]   # kit, quadros limpos
dm = round(sum(x[2] for x in m), 2)
segs.append(bloco("04_mecanismo", m, [(AU / "L4_mecanismo.mp3", 0, 0.1, None)], dm))
ali_tts(AU / "L4_mecanismo.alinhamento.json", t + 0.1); t += dm
# 5 virada: Kling (sorri olhando o celular) + tela do post antes/depois com os comentários + Kling
v = G["virada"]
segs.append(bloco("05_virada", [(T / "V3_virada.mp4", v["a"][0], v["a"][1], None, True),
                                (CE / "T2_post_virada.png", 0, v["tela"], ZOOM, False),
                                (T / "V3_virada.mp4", v["b"][0], v["b"][1], None, True)],
                  [], v["a"][1] + v["tela"] + v["b"][1]))
t += v["a"][1] + v["tela"] + v["b"][1]
# 6 CTA: persona com o produto original (still com zoom lento) + narração
cta_d = 8.1
segs.append(bloco("06_cta", [(CE / "S6_cta.png", 0, cta_d, ZOOM, True)], [(AU / "L6_cta.mp3", 0, 0.2, None)], cta_d))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.2); t += cta_d

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print("".join(ALI["characters"]))
