# -*- coding: utf-8 -*-
"""Monta o corpo do AD C9 «El Ratón» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Adaptado de KIT-HOMBRE-3EN1/PROD1-EL-MAESTRO/montar_corpo.py."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU, CE = P / "takes", P / "audio", P / "cenas"
B = Path(r"C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\BANCO")
V1, V2 = B / "V1_720.mp4", B / "V2_limpo_13-46.mp4"
SELO = B / "overlay_selo_cesped.png"
WK = P / "_seg"; WK.mkdir(exist_ok=True)
CFG = json.load(open(P / "cortes.json", encoding="utf-8"))
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur, overlay=None):
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
    for w, a, b in pal:
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
# 1 gancho: take Seedance (vídeo + ambiente nativo) com a fala trocada pela voz STS (Andrea), mesmo tempo
g = CFG["gancho"]
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", g["ss"], g["dur"], None)],
                  [(AU / "v1_andrea.mp3", g["ss"], 0, g["dur"])], g["dur"], SELO))
ali_palavras([(w, a - g["ss"], b - g["ss"]) for w, a, b in g["palavras"]], t); t += g["dur"]
# 2 persona: selfie Seedance + voz STS
s = CFG["selfie"]
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", s["ss"], s["dur"], None)],
                  [(AU / "v2_andrea.mp3", s["ss"], 0, s["dur"])], s["dur"], SELO))
ali_palavras([(w, a - s["ss"], b - s["ss"]) for w, a, b in s["palavras"]], t); t += s["dur"]
# 3 antes/depois real (V1 0–5,5) + «Hasta que probé esta.»
segs.append(bloco("03_antes_despues", [(V1, 0.5, 4.5, None)], [(AU / "L3_hasta.mp3", 0, 0.25, None)], 4.5))
ali_tts(AU / "L3_hasta.alinhamento.json", t + 0.25); t += 4.5
# 4 mecanismo (C ímpar começa pelo V2): deck (V2) → rodas no gramado (V1 6,1–9,6; o V2 7,5–11 tinha texto fantasma do LaMa) → close cuchilla → kit
m_d = 13.1
segs.append(bloco("04_mecanismo", [(V2, 1.4, 1.7, None), (V2, 4.6, 1.6, None), (V1, 6.1, 3.5, None), (V2, 13.5, 3.3, None),
                                   (V1, 24.0, 1.4, None), (V2, 22.8, 0.7, None), (V2, 24.0, 0.9, None)],
                  [(AU / "L4_mecanismo.mp3", 0, 0.2, None)], m_d))
ali_tts(AU / "L4_mecanismo.alinhamento.json", t + 0.2); t += m_d
# 5 virada: Kling (filhos descalços no pasto baixo), sem fala
vd = CFG["virada"]["dur"]
segs.append(bloco("05_virada", [(T / "V5_virada.mp4", CFG["virada"]["ss"], vd, None)], [], vd, SELO))
t += vd
# 6 CTA: imagem com o produto original reduzida a 86% no topo, sobre a própria imagem desfocada (espaço p/ legenda e setas) + zoom lento
cta_d = 7.1
vf_cta = ("split[a][b];[a]boxblur=25:2[bg];[b]scale=576:1024,"
          "zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=576x1024:fps=30[fg];"
          "[bg][fg]overlay=72:100")
segs.append(bloco("06_cta", [(CE / "S6_cta.png", 0, cta_d, vf_cta)], [(AU / "L6_cta.mp3", 0, 0.25, None)], cta_d, SELO))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.25); t += cta_d

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{x.as_posix()}'\n" for x in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print("".join(ALI["characters"]))
