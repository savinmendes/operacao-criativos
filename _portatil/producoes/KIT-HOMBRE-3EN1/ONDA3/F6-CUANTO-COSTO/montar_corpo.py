# -*- coding: utf-8 -*-
"""Monta o corpo do AD F6 «¿Cuánto te costó?» (720x1280, 30 fps) + alinhamento combinado para a legenda.
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
# 1 gancho: amigo cheira e fala (voz nativa do Seedance)
G0 = 0.6
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", G0, 4.0, None)], [(T / "V1_gancho.mp4", G0, 0, 4.0)], 4.0, SELO))
ali_palavras([(w, a - G0, b - G0) for w, a, b in [("¡Hueón!", 1.3, 1.74), ("¿Qué", 1.74, 1.96), ("te", 1.96, 2.06), ("echaste?", 2.06, 2.42),
              ("Eso", 2.78, 3.22), ("debe", 3.22, 3.42), ("haber", 3.42, 3.56), ("salido", 3.56, 3.94), ("carísimo.", 3.94, 4.4)]], t); t += 4.0
# 2 ele ri e conta (voz Santiago por STS, mesmo tempo)
R0 = 0.45
segs.append(bloco("02_ri", [(T / "V2_ri.mp4", R0, 4.55, None)], [(AU / "v2_santiago.mp3", R0, 0, 4.55)], 4.55, SELO))
ali_palavras([(w, a - R0, b - R0) for w, a, b in [("Si", 0.88, 1.64), ("supieran…", 1.64, 2.18), ("son", 2.18, 3.0), ("tres,", 3.0, 3.34),
              ("y", 3.34, 3.84), ("los", 3.84, 3.96), ("pagué", 3.96, 4.24), ("cuando", 4.24, 4.4), ("llegaron.", 4.4, 4.78)]], t); t += 4.55
# 3 oferta: close nos frascos da imagem do CTA sobre o fundo desfocado + TTS
segs.append(bloco("03_oferta", [(C / "S5_cta.png", 0, 3.0, "split[oa][ob];[oa]boxblur=20:2,eq=brightness=-0.08[obg];[ob]crop=420:300:120:460,scale=720:514[ofg];[obg][ofg]overlay=0:383," + ZP + "|SELO")],
                  [(AU / "L3_oferta.mp3", 0, 0.1, None)], 3.0))
ali_tts(AU / "L3_oferta.alinhamento.json", t + 0.1); t += 3.0
# 4 Armaf: amigos cheirando (início do Kling) + unboxing Armaf
segs.append(bloco("04_armaf", [(T / "V4_cheiram.mp4", 0, 1.4, "|SELO"), (UB / "armaf_limpo.mp4", 0, 2.2, "setpts=1.1*PTS")],
                  [(AU / "L4_armaf.mp3", 0, 0.12, None)], 3.6))
ali_tts(AU / "L4_armaf.alinhamento.json", t + 0.12); t += 3.6
# 5 Asad: unboxing Asad + continuação do Kling (corta antes de os rostos mudarem)
segs.append(bloco("05_asad", [(UB / "asad_limpo.mp4", 0, 3.0, "setpts=1.364*PTS"), (T / "V4_cheiram.mp4", 1.4, 1.5, "|SELO")],
                  [(AU / "L5_asad.mp3", 0, 0.1, None)], 4.5))
ali_tts(AU / "L5_asad.alinhamento.json", t + 0.1); t += 4.5
# 6 9PM: unboxing 9PM levemente desacelerado
segs.append(bloco("06_9pm", [(UB / "9pm_limpo.mp4", 0, 4.9, "setpts=1.23*PTS")], [(AU / "L6_9pm.mp3", 0, 0.08, None)], 4.9))
ali_tts(AU / "L6_9pm.alinhamento.json", t + 0.08); t += 4.9
# 7 virada (amigos pedindo pelo celular) + CTA com o pack (still com zoom lento)
ZC = "zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.45':d=1:s=720x1280:fps=30"
segs.append(bloco("07_cta", [(T / "V3_celulares.mp4", 0, 3.3, "|SELO"), (C / "S5_cta.png", 0, 3.0, ZC + "|SELO")],
                  [(AU / "L8_cta.mp3", 0, 0.2, None)], 6.3))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 6.3

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
