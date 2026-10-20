# -*- coding: utf-8 -*-
"""Monta o corpo do AD «El Mecánico» (720x1280, 30 fps) + alinhamento combinado para a legenda.
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


ZP = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
segs, t = [], 0.0
# 1 gancho (fala nativa da cliente)
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", 0, 4.8, None)], [(T / "V1_gancho.mp4", 0, 0, 4.8)], 4.8, SELO))
ali_palavras([("¿Y", 0.7, 1.3), ("mi", 1.3, 1.46), ("auto?", 1.46, 1.76), ("Ya", 1.76, 2.5), ("no", 2.5, 2.62), ("importa…", 2.62, 2.92),
              ("¿qué", 3.9, 4.12), ("te", 4.12, 4.26), ("echaste?", 4.26, 4.64)], t); t += 4.8
# 2 selfie (voz Richard por STS, mesmo tempo)
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", 0, 4.7, None)], [(AU / "v2_richard.mp3", 0, 0, 4.7)], 4.7, SELO))
ali_palavras([("Soy", 0.0, 0.54), ("mecánico…", 0.54, 1.08), ("y", 1.08, 1.32), ("ahora", 1.32, 2.0), ("las", 2.0, 2.16), ("clientas", 2.16, 2.62),
              ("vienen", 2.62, 2.84), ("aunque", 2.84, 3.4), ("el", 3.4, 3.6), ("auto", 3.6, 3.84), ("no", 3.84, 4.02), ("tenga", 4.02, 4.28), ("nada.", 4.28, 4.48)], t); t += 4.7
# 3 oferta: close nos frascos da imagem do CTA (zoom lento) + TTS
segs.append(bloco("03_oferta", [(C / "S6_cta.png", 0, 2.3, "split[oa][ob];[oa]boxblur=20:2,eq=brightness=-0.08[obg];[ob]crop=720:620:0:600[ofg];[obg][ofg]overlay=0:330," + ZP + "|SELO")],
                  [(AU / "L4_oferta.mp3", 0, 0.1, None)], 2.3))
ali_tts(AU / "L4_oferta.alinhamento.json", t + 0.1); t += 2.3
# 4 dia: debaixo do capô + Armaf
segs.append(bloco("04_dia", [(T / "V3_dia.mp4", 0, 4.6, "|SELO"), (UB / "armaf_limpo.mp4", 0, 1.6, None)],
                  [(AU / "L5_dia.mp3", 0, 0.15, None)], 6.2))
ali_tts(AU / "L5_dia.alinhamento.json", t + 0.15); t += 6.2
# 5 noite: Asad + polola
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.0, None), (T / "V4_noite.mp4", 0, 4.4, "|SELO")],
                  [(AU / "L6_noche.mp3", 0, 0.15, None)], 6.4))
ali_tts(AU / "L6_noche.alinhamento.json", t + 0.15); t += 6.4
# 6 fim de semana: carrete (still com zoom) + 9PM
segs.append(bloco("06_finde", [(C / "S5_finde.png", 0, 1.8, ZP + "|SELO"), (UB / "9pm_limpo.mp4", 0, 2.4, None)],
                  [(AU / "L7_finde.mp3", 0, 0.05, None)], 4.2))
ali_tts(AU / "L7_finde.alinhamento.json", t + 0.05); t += 4.2
# 7 CTA: pack sobre o capô (still com zoom lento)
ZC = "zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3':d=1:s=720x1280:fps=30"
segs.append(bloco("07_cta", [(C / "S6_cta.png", 0, 4.8, ZC)], [(AU / "L8_cta.mp3", 0, 0.2, None)], 4.8, SELO))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 4.8

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
# corrige a grafia dos nomes de marca no alinhamento das narrações TTS ("Nine PM" -> "9PM")
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
