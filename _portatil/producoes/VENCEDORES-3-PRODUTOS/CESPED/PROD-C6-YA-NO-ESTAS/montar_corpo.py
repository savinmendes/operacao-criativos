# -*- coding: utf-8 -*-
"""Monta o corpo do AD CÉSPED C6 «Ya no estás pa' esto» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Adaptado do montar_corpo.py do P1 (El Maestro). Saída: corpo.mp4 e corpo.alinhamento.json."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU = P / "takes", P / "audio"
BANCO = Path(r"C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\BANCO")
V1, V2 = BANCO / "V1_720.mp4", BANCO / "V2_limpo_13-46.mp4"
SELO = BANCO / "overlay_selo_cesped.png"
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


# tempos da fala da persona (takes/V2_persona.mp4, whisper) — preenchidos após a transcrição
PERSONA = json.load(open(T / "_persona.json", encoding="utf-8"))
PSS, PT, PW = PERSONA["ss"], PERSONA["t"], PERSONA["palavras"]

segs, t = [], 0.0
# 1 gancho: filho fala (voz nativa do Seedance), pai encara
G = 4.2
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", 0, G, None)], [(T / "V1_gancho.mp4", 0, 0, G)], G, SELO))
ali_palavras([("Papá,", 0.4, 0.76), ("deja", 0.76, 0.96), ("que", 0.96, 1.1), ("contratemos", 1.1, 1.6), ("a", 1.6, 1.76), ("alguien…", 1.76, 2.0),
              ("ya", 2.42, 2.78), ("no", 2.78, 2.9), ("estás", 2.9, 3.04), ("pa'", 3.04, 3.24), ("esto.", 3.26, 3.46)], t); t += G
# 2 persona: pai em selfie, voz Salvatore por STS no tempo original
segs.append(bloco("02_persona", [(T / "V2_persona.mp4", PSS, PT, None)], [(AU / "V2_persona_salvatore.mp3", PSS, 0, PT)], PT, SELO))
ali_palavras([(w, a - PSS, b - PSS) for w, a, b in PW], t); t += PT
# 3 antes/depois real (V1 0-5,5) + «Hasta que probé esta.»
segs.append(bloco("03_antes", [(V1, 0, 5.5, None)], [(AU / "L3_antes.mp3", 0, 0.3, None)], 5.5))
ali_tts(AU / "L3_antes.alinhamento.json", t + 0.3); t += 5.5
# 4 mecanismo (C par: começa pelo V1); nenhum trecho repete
M = [(V1, 11.3, 3.6, None),   # borda da calçada (orilladora/bordeadora)
     (V1, 6.2, 4.0, None),    # rodas (una sola mano)
     (V2, 22.8, 0.7, None),   # kit na mesa (cuchilla de metal); só 22,8-23,5 (fantasma LaMa em 23,6-23,9)
     (V1, 18.5, 3.35, None),   # faixas no mato alto (hilos)
     (V1, 16.6, 1.2, None),   # POV do gatilho (inalámbrica)
     (V1, 24.5, 2.6, None)]   # gramado lateral (dos baterías); V2 27-30 tem resto de legenda do LaMa
MD = round(sum(p[2] for p in M), 2)
segs.append(bloco("04_mecanismo", M, [(AU / "L4_mecanismo.mp3", 0, 0.1, None)], MD))
ali_tts(AU / "L4_mecanismo.alinhamento.json", t + 0.1); t += MD
# 5 virada: pai de braços cruzados (voz Salvatore por STS)
VSS, VT = 1.0, 3.2
segs.append(bloco("05_virada", [(T / "V3_virada.mp4", VSS, VT, None)], [(AU / "V3_virada_salvatore.mp3", VSS, 0, VT)], VT, SELO))
ali_palavras([(w, a - VSS, b - VSS) for w, a, b in
              [("¿Quién", 2.14, 2.56), ("no", 2.56, 2.62), ("estaba", 2.62, 2.88), ("pa'", 2.88, 3.06), ("esto?", 3.06, 3.3)]], t); t += VT
# 6 CTA: pai com o produto original (still com zoom lento)
CD = 7.0
cta = P / "cenas" / "S6_cta.png"
segs.append(bloco("06_cta", [(cta, 0, CD, "zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30,split[ca][cb];[ca]boxblur=24:2,eq=brightness=-0.06[cbg];[cb]scale=590:1050[cfg];[cbg][cfg]overlay=65:110")],
                  [(AU / "L6_cta.mp3", 0, 0.25, None)], CD, SELO))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.25); t += CD

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print("".join(ALI["characters"]))
