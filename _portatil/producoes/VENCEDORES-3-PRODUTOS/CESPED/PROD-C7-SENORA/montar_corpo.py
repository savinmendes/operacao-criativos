# -*- coding: utf-8 -*-
"""Monta o corpo do AD CÉSPED C7 «La Señora Avergonzada» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Adaptado do montar_corpo.py do P1 (El Maestro). Saída: corpo.mp4 e corpo.alinhamento.json."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU = P / "takes", P / "audio"
BK = Path(r"C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\BANCO")
V1, V2 = BK / "V1_720.mp4", BK / "V2_limpo_13-46.mp4"
SELO = BK / "overlay_selo_cesped.png"
WK = P / "_seg"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
ZOOM_TOPO = "zoompan=z='1+0.0005*on':x='iw/2-(iw/zoom/2)':y='0':d=1:s=720x1280:fps=30"
ZOOM = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur, overlay=None):
    """partes: [(arquivo, ss, t, vf_extra)]  audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None)]"""
    ins, fc = [], []
    for i, (f, ss, t, vx) in enumerate(partes):
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t), "-i", str(f)]
        fc.append(f"[{i}:v]{BASE}{(',' + vx) if vx else ''},trim=duration={t},setpts=PTS-STARTPTS[v{i}]")
    n = len(partes)
    fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]")
    k = n
    if overlay:
        ins += ["-i", str(overlay)]; fc.append(f"[vc][{k}:v]overlay=0:0[vo]"); k += 1; vout = "[vo]"
    else:
        vout = "[vc]"
    al = []
    for j, (f, ss, atraso, d) in enumerate(audios):
        ins += (["-ss", str(ss)] + (["-t", str(d)] if d else []) + ["-i", str(f)])
        ms = int(atraso * 1000)
        fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms}[a{j}]"); al.append(f"[a{j}]"); k += 1
    ins += ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    fc.append("".join(al) + f"[{k}:a]amix=inputs={len(al) + 1}:normalize=0:duration=longest,atrim=duration={dur}[ao]")
    out = WK / f"{nome}.mp4"
    run([*ins, "-filter_complex", ";".join(fc), "-map", vout, "-map", "[ao]", "-t", str(dur), *ENC, str(out)])
    return out


ALI = {"characters": [], "character_start_times_seconds": [], "character_end_times_seconds": []}


def ali_palavras(pal, t0):
    """pal: [(texto, ini, fim)] em tempo do bloco"""
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


CFG = json.load(open(P / "cortes.json", encoding="utf-8"))   # cortes dos takes Seedance (após a transcrição)
segs, t = [], 0.0
# 1 gancho: esposa cochichando ao telefone (fala nativa)
g = CFG["gancho"]
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", g["ss"], g["dur"], None)], [(T / "V1_gancho.mp4", g["ss"], 0, g["dur"])], g["dur"], SELO))
ali_palavras([(w, a - g["ss"], b - g["ss"]) for w, a, b in g["pal"]], t); t += g["dur"]
# 2 persona: selfie do marido (voz Louis por STS, mesmo tempo)
s2 = CFG["selfie"]
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", s2["ss"], s2["dur"], None)], [(AU / "v2_louis.mp3", s2["ss"], 0, s2["dur"])], s2["dur"], SELO))
ali_palavras([(w, a - s2["ss"], b - s2["ss"]) for w, a, b in s2["pal"]], t); t += s2["dur"]
# 3 antes/depois real (V1 0-5) + «Hasta que probé esta.»
segs.append(bloco("03_antes", [(V1, 0, 5.0, None)], [(AU / "L3_hasta.mp3", 0, 0.15, None)], 5.0))
ali_tts(AU / "L3_hasta.alinhamento.json", t + 0.15); t += 5.0
# 4 mecanismo: começa pelo V2 (C ímpar), sem repetir trecho
partes4 = [(V2, 1.2, 1.3, None), (V1, 6.05, 3.85, None), (V1, 11.1, 3.0, None), (V1, 18.3, 3.3, None), (V2, 22.8, 0.7, None), (V2, 24.0, 0.9, None)]
d4 = round(sum(p[2] for p in partes4), 2)
segs.append(bloco("04_mecanismo", partes4, [(AU / "L4_mecanismo.mp3", 0, 0.05, None)], d4))
ali_tts(AU / "L4_mecanismo.alinhamento.json", t + 0.05); t += d4
# 5 virada: esposa feliz ao telefone (fala nativa) + família no jardim (still com zoom lento)
v = CFG["virada"]
segs.append(bloco("05a_virada", [(T / "V3_virada.mp4", v["ss"], v["dur"], None)], [(T / "V3_virada.mp4", v["ss"], 0, v["dur"])], v["dur"], SELO))
ali_palavras([(w, a - v["ss"], b - v["ss"]) for w, a, b in v["pal"]], t); t += v["dur"]
segs.append(bloco("05b_familia", [(P / "cenas" / "S5_familia.png", 0, 2.4, ZOOM)], [], 2.4, SELO)); t += 2.4
# 6 CTA: marido com o produto original (still com zoom lento) + narração
segs.append(bloco("06_cta", [(P / "cenas" / "S6_cta.png", 0, 7.3, ZOOM_TOPO)], [(AU / "L6_cta.mp3", 0, 0.2, None)], 7.3, SELO))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.2); t += 7.3

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print("".join(ALI["characters"]))
