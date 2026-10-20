# -*- coding: utf-8 -*-
"""Monta o corpo do AD «F2 Regalo para él» (720x1280, 30 fps) + alinhamento combinado para a legenda.
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
# 1 gancho: selfie dela (Seedance), voz Isa Pro por STS no mesmo tempo
G0 = 0.3
segs.append(bloco("01_selfie", [(T / "V1_selfie.mp4", G0, 4.0, None)], [(AU / "v1_isa.mp3", G0, 0, 4.0)], 4.0, SELO))
ali_palavras([(w, a - G0, b - G0) for w, a, b in [("Mi", 0.64, 0.8), ("marido", 0.8, 1.1), ("usaba", 1.1, 1.46), ("el", 1.46, 1.56), ("mismo", 1.56, 1.86),
              ("perfume", 1.86, 2.3), ("desde", 2.3, 2.74), ("2015…", 2.74, 3.6)]], t); t += 4.0
# 2 compra: ela embrulha o presente (still com zoom) + corte para a caixa
ZB = "crop=504:896:108:384,scale=720:1280,setsar=1,zoompan=z='1.0+0.0010*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
segs.append(bloco("02_compra", [(C / "S2_envolver.png", 0, 3.5, ZP + "|SELO"), (C / "S2_envolver.png", 0, 2.2, ZB + "|SELO")],
                  [(AU / "L2_compra.mp3", 0, 0.1, None)], 5.7))
ali_tts(AU / "L2_compra.alinhamento.json", t + 0.1); t += 5.7
# 3 oferta: close nos frascos da imagem do CTA sobre o fundo desfocado
segs.append(bloco("03_oferta", [(C / "S5_cta.png", 0, 2.3, "split[oa][ob];[oa]boxblur=20:2,eq=brightness=-0.08[obg];[ob]crop=640:440:40:490,scale=720:495[ofg];[obg][ofg]overlay=0:390," + ZP + "|SELO")],
                  [(AU / "L3_oferta.mp3", 0, 0.1, None)], 2.3))
ali_tts(AU / "L3_oferta.alinhamento.json", t + 0.1); t += 2.3
# 4-6 unboxing real com os 3 perfumes
segs.append(bloco("04_armaf", [(UB / "armaf_limpo.mp4", 0, 2.6, "setpts=1.3*PTS")], [(AU / "L4_armaf.mp3", 0, 0.1, None)], 2.6))
ali_tts(AU / "L4_armaf.alinhamento.json", t + 0.1); t += 2.6
segs.append(bloco("05_asad", [(UB / "asad_limpo.mp4", 0, 2.3, "setpts=1.05*PTS")], [(AU / "L5_asad.mp3", 0, 0.05, None)], 2.3))
ali_tts(AU / "L5_asad.alinhamento.json", t + 0.05); t += 2.3
segs.append(bloco("06_9pm", [(UB / "9pm_limpo.mp4", 0, 2.5, None)], [(AU / "L6_9pm.mp3", 0, 0.05, None)], 2.5))
ali_tts(AU / "L6_9pm.alinhamento.json", t + 0.05); t += 2.5
# 7 virada: marido abre o presente e cheira o Asad; ela cheira o pescoço dele (Kling, levemente desacelerado)
segs.append(bloco("07_virada", [(T / "V2_virada.mp4", 0, 4.6, "setpts=1.1*PTS|SELO")], [(AU / "L7_virada.mp3", 0, 2.2, None)], 4.6))
ali_tts(AU / "L7_virada.alinhamento.json", t + 2.2); t += 4.6
# 8 CTA: ela com o pack (still com zoom lento)
ZC = "zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.45':d=1:s=720x1280:fps=30"
segs.append(bloco("08_cta", [(C / "S5_cta.png", 0, 4.3, ZC)], [(AU / "L8_cta.mp3", 0, 0.2, None)], 4.3, SELO))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 4.3

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
