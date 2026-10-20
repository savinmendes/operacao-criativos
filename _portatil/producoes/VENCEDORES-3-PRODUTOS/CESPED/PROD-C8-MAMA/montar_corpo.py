# -*- coding: utf-8 -*-
"""Monta o corpo do AD CÉSPED C8 «La casa de mi mamá» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Adaptado do montar_corpo.py do P1 (El Maestro). Saída: corpo.mp4 e corpo.alinhamento.json."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU, C = P / "takes", P / "audio", P / "cenas"
B = Path(r"C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\BANCO")
V1, V2 = B / "V1_720.mp4", B / "V2_limpo_13-46.mp4"
SELO = B / "overlay_selo_cesped.png"
WK = P / "_seg"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
ZOOM = "zoompan=z='1+0.0004*on':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.2':d=1:s=720x1280:fps=30"


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur, overlay=None):
    """partes: [(arquivo, ss, t, vf_extra)]  audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None, vol)]"""
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
    for j, (f, ss, atraso, d, vol) in enumerate(audios):
        ins += (["-ss", str(ss)] + (["-t", str(d)] if d else []) + ["-i", str(f)])
        ms = int(atraso * 1000)
        fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[a{j}]"); al.append(f"[a{j}]"); k += 1
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


CFG = json.load(open(P / "cortes.json", encoding="utf-8"))  # tempos dos takes IA (definidos após o whisper)
segs, t = [], 0.0
# 1 gancho: mãe com vergonha (fala nativa do Seedance)
g = CFG["gancho"]
segs.append(bloco("01_gancho", [(T / "V_gancho.mp4", g["ss"], g["dur"], None)], [(T / "V_gancho.mp4", g["ss"], 0, g["dur"], 1.0)], g["dur"], SELO))
ali_palavras([(w, a - g["ss"], b - g["ss"]) for w, a, b in g["palavras"]], t); t += g["dur"]
# 2 persona: selfie do filho (voz BRAULIO por STS, mesmo tempo)
s = CFG["selfie"]
segs.append(bloco("02_selfie", [(T / "V_selfie.mp4", s["ss"], s["dur"], None)], [(AU / "selfie_braulio.mp3", s["ss"], 0, s["dur"], 1.5)], s["dur"], SELO))
ali_palavras([(w, a - s["ss"], b - s["ss"]) for w, a, b in s["palavras"]], t); t += s["dur"]
# 3 antes/depois real (V1 0–5 s) + «Hasta que probé esta.»
segs.append(bloco("03_antes", [(V1, 0, 5.0, None)], [(AU / "L3_antes.mp3", 0, 0.25, None, 1.0)], 5.0))
ali_tts(AU / "L3_antes.alinhamento.json", t + 0.25); t += 5.0
# 4 mecanismo real (C par: começa pelo V1)
mec = [(V1, 11.3, 3.0, None), (V1, 6.2, 3.0, None), (V1, 18.6, 3.6, None), (V1, 24.4, 1.4, None), (V2, 22.8, 0.7, None), (V2, 24.0, 0.9, None)]
segs.append(bloco("04_mecanismo", mec, [(AU / "L4_mecanismo.mp3", 0, 0.1, None, 1.0)], 12.6))
ali_tts(AU / "L4_mecanismo.alinhamento.json", t + 0.1); t += 12.6
# 5 virada: mãe toma chá no jardim cortado (Kling, sem fala)
v = CFG["virada"]
segs.append(bloco("05_virada", [(T / "V_virada.mp4", v["ss"], v["dur"], None)], [], v["dur"], SELO))
t += v["dur"]
# 6 CTA: filho com o produto original (still com zoom lento) + narração
segs.append(bloco("06_cta", [(C / "S6_cta.png", 0, 7.6, ZOOM)], [(AU / "L6_cta.mp3", 0, 0.2, None, 1.0)], 7.6, SELO))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.2); t += 7.6

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{x.as_posix()}'\n" for x in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print("".join(ALI["characters"]))
