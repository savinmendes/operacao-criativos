# -*- coding: utf-8 -*-
"""Monta o corpo do AD CÉSPED C3 «El cumpleaños del sábado» (720x1280, 30 fps) + alinhamento combinado.
Adaptado do montar_corpo.py do P10 (perfumes). Saída: corpo.mp4 e corpo.alinhamento.json."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU, C = P / "takes", P / "audio", P / "cenas"
BC = Path("C:/Users/PICHAU/Downloads/VENCEDORES-3-PRODUTOS/CESPED/BANCO")
V1, V2 = BC / "V1_720.mp4", BC / "V2_limpo_13-46.mp4"
SELO = BC / "overlay_selo_cesped.png"
WK = P / "_seg"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur, overlay=None):
    """partes: [(arquivo, ss, t, vf_extra)]  audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None)]"""
    ins, fc = [], []
    for i, (f, ss, t, vx) in enumerate(partes):
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t + 1), "-i", str(f)]
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


CFG = json.load(open(P / "cortes.json", encoding="utf-8"))
segs, t = [], 0.0
# 1 gancho: filha (voz nativa do Seedance)
g = CFG["gancho"]
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", g["ini"], g["dur"], None)], [(T / "V1_gancho.mp4", g["ini"], 0, g["dur"])], g["dur"], SELO))
ali_palavras([(w, a - g["ini"], b - g["ini"]) for w, a, b in g["palavras"]], t); t += g["dur"]
# 2 persona: selfie com a voz do Alberto por STS, mesmo tempo
s = CFG["selfie"]
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", s["ini"], s["dur"], None)], [(AU / "v2_alberto.mp3", s["ini"], 0, s["dur"])], s["dur"], SELO))
ali_palavras([(w, a - s["ini"], b - s["ini"]) for w, a, b in s["palavras"]], t); t += s["dur"]
# 3 antes/depois real (V1 0–5,5 s) + «Hasta que probé esta.»
segs.append(bloco("03_antes", [(V1, 0.2, 4.6, None)], [(AU / "L3_antes_c.mp3", 0, 0.3, None)], 4.6))
ali_tts(AU / "L3_antes.alinhamento_c.json", t + 0.3); t += 4.6
# 4 mecanismo real (C ímpar: começa pelo V2)
segs.append(bloco("04_mecanismo", [(V2, 1.4, 1.7, None),            # deck limpo 1,4–3,1 (fantasmas LaMa em 1,1–1,3 e 3,2–4,0 fora)
                                   (V1, 11.6, 1.6, None),           # borda da calçada: orilladora/bordeadora
                                   (V1, 6.3, 2.8, None),            # rodas: una sola mano
                                   (V1, 18.4, 3.8, None),           # faixas no mato alto: cuchilla de metal (V2 galpão tem fantasma LaMa ~27 s)
                                   (V1, 24.5, 0.8, None),           # gramado lateral: inalámbrica
                                   (V2, 22.8, 0.91, "setpts=1.3*PTS"),  # kit limpo 22,8–23,5
                                   (V2, 24.0, 1.19, "setpts=1.3*PTS")],  # kit limpo 24,0–24,9 (fantasma em 23,6–23,9 fora)
                  [(AU / "L4_mecanismo_c.mp3", 0, 0.1, None)], 12.8))
ali_tts(AU / "L4_mecanismo.alinhamento_c.json", t + 0.1); t += 12.8
# 5 virada: a festa no quintal cortado (Kling, sem fala)
v = CFG["virada"]
segs.append(bloco("05_virada", [(T / "V3_virada.mp4", v["ini"], v["dur"], None)], [], v["dur"], SELO))
t += v["dur"]
# 6 CTA: pai com o produto original (still com zoom lento) + narração
ZC = "zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3':d=1:s=720x1280:fps=30"
segs.append(bloco("06_cta", [(C / "S6_cta.png", 0, 6.5, ZC)], [(AU / "L6_cta_c.mp3", 0, 0.2, None)], 6.5, SELO))
ali_tts(AU / "L6_cta.alinhamento_c.json", t + 0.2); t += 6.5

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{x.as_posix()}'\n" for x in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
txt = "".join(ALI["characters"]); i = txt.find("noventa")
if i >= 0:
    s0, e0 = ALI["character_start_times_seconds"][i], ALI["character_end_times_seconds"][i + 6]
    ALI["characters"][i:i + 7] = list("90"); ALI["character_start_times_seconds"][i:i + 7] = [s0, s0]
    ALI["character_end_times_seconds"][i:i + 7] = [e0, e0]
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print("".join(ALI["characters"]))
