# -*- coding: utf-8 -*-
"""Monta o corpo do AD «F7 Primera Cita» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Saída: corpo.mp4 e corpo.alinhamento.json (formato ElevenLabs: characters + start/end)."""
import json, subprocess, os
from pathlib import Path

P = Path(__file__).parent
T, AU, C = P / "takes", P / "audio", P / "cenas"
UB = Path("C:/Users/PICHAU/Downloads/KIT-HOMBRE-3EN1/PROD1-EL-MAESTRO/unbox")
OVA = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\LOTE-15-10\_trabalho\A")
SELO, SELO_ROD = OVA / "overlay_selo.png", OVA / "overlay_selo_rodape.png"
WK = P / "_seg"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur, overlay=None):
    """partes: [(arquivo, ss, t, vf_extra)]  audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None)]"""
    ins, fc, selos = [], [], []
    for i, (f, ss, t, vx) in enumerate(partes):
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t), "-i", str(f)]
        sel = bool(vx) and vx.endswith("|SELO")
        if sel: vx = vx[:-5] or None
        fc.append(f"[{i}:v]{BASE}{(',' + vx) if vx else ''},trim=duration={t},setpts=PTS-STARTPTS[v{i}{'s' if sel else ''}]")
        if sel: selos.append(i)
    n = len(partes)
    for j, i in enumerate(selos):
        ins += ["-loop", "1", "-t", str(partes[i][2]), "-i", str(SELO)]
        fc.append(f"[v{i}s][{n + j}:v]overlay=0:0:shortest=1[v{i}]")
    fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]")
    k = n + len(selos)
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
        s = w + (" " if i < len(pal) - 1 else " ")
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


ZP = "zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
segs, t = [], 0.0
G0 = 0.8  # corta o início parado do gancho
# 1 gancho POV: fala nativa dela
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", G0, 4.25, None)], [(T / "V1_gancho.mp4", G0, 0, 4.25)], 4.25, SELO))
ali_palavras([("Antes", 1.64 - G0, 2.28 - G0), ("de", 2.28 - G0, 2.42 - G0), ("pedir…", 2.42 - G0, 2.9 - G0),
              ("¿qué", 3.86 - G0, 4.0 - G0), ("perfume", 4.0 - G0, 4.32 - G0), ("traes?", 4.32 - G0, 4.8 - G0)], t); t += 4.25
# 2 noche: Asad (unboxing) + ela sentindo o perfume (Kling)
segs.append(bloco("02_noche", [(UB / "asad_limpo.mp4", 0, 2.2, None), (T / "V3_noche.mp4", 0, 3.1, "|SELO")],
                  [(AU / "L2_noche.mp3", 0, 0.1, None)], 5.3))
ali_tts(AU / "L2_noche.alinhamento.json", t + 0.1); t += 5.3
# 3 oferta: os 3 frascos sobre a mesa (zoom lento)
segs.append(bloco("03_oferta", [(C / "S3_cta.png", 0, 2.3, "crop=660:1173:30:60,scale=720:1280," + ZP + "|SELO")],
                  [(AU / "L3_oferta.mp3", 0, 0.1, None)], 2.3))
ali_tts(AU / "L3_oferta.alinhamento.json", t + 0.1); t += 2.3
# 4 resto da semana: Armaf + 9PM
segs.append(bloco("04_semana", [(C / "S3_cta.png", 0, 2.1, ZP + "|SELO"), (UB / "armaf_limpo.mp4", 0, 2.0, None), (UB / "9pm_limpo.mp4", 0, 3.9, None)],
                  [(AU / "L4_semana.mp3", 0, 0.1, None)], 8.0))
ali_tts(AU / "L4_semana.alinhamento.json", t + 0.1); t += 8.0
# 5 virada: POV de mãos dadas na rua
segs.append(bloco("05_virada", [(T / "V5_virada.mp4", 0, 4.0, "|SELO")], [(AU / "L5_virada.mp3", 0, 0.6, None)], 4.0))
ali_tts(AU / "L5_virada.alinhamento.json", t + 0.6); t += 4.0
# 6 CTA: pack sobre a mesa do restaurante
segs.append(bloco("06_cta", [(C / "S3_cta.png", 0, 4.8, ZP)], [(AU / "L6_cta.mp3", 0, 0.2, None)], 4.8, SELO))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.2); t += 4.8

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
txt = "".join(ALI["characters"])
i = txt.find("Nine PM")
if i >= 0:
    s0, e0 = ALI["character_start_times_seconds"][i], ALI["character_end_times_seconds"][i + 6]
    ALI["characters"][i:i + 7] = list("9PM")
    ALI["character_start_times_seconds"][i:i + 7] = [s0, s0, s0]
    ALI["character_end_times_seconds"][i:i + 7] = [e0, e0, e0]
    txt = "".join(ALI["characters"])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print(txt)
