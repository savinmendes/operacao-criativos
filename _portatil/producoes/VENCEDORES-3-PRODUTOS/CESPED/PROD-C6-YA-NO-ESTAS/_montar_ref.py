# -*- coding: utf-8 -*-
"""Monta o corpo do AD «El Maestro» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Saída: corpo.mp4 e corpo.alinhamento.json (formato ElevenLabs: characters + start/end)."""
import json, subprocess, os
from pathlib import Path

P = Path(__file__).parent
T, AU, UB = P / "takes", P / "audio", P / "unbox"
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


segs, t = [], 0.0
# 1 gancho (fala nativa da mulher)
segs.append(bloco("01_gancho", [(T / "V1_gancho1.mp4", 0, 3.9, None)], [(T / "V1_gancho1.mp4", 0, 0, 3.9)], 3.9, SELO))
ali_palavras([("¡Oye,", 1.38, 2.06), ("ven", 2.06, 2.24), ("acá!", 2.24, 2.52), ("¿Qué", 2.52, 3.16), ("te", 3.16, 3.28), ("echaste?", 3.28, 3.68)], t); t += 3.9
# 2 selfie (voz Luis por STS, mesmo tempo)
segs.append(bloco("02_selfie", [(T / "V3_selfie.mp4", 1.3, 5.0, None)], [(AU / "v3_luis.mp3", 1.3, 0, 5.0)], 5.0, SELO))
w3 = [("Soy", 1.60, 2.0), ("maestro", 2.02, 2.44), ("de", 2.44, 2.52), ("la", 2.52, 2.58), ("construcción…", 2.58, 3.14), ("y", 3.16, 3.7),
      ("desde", 3.70, 3.9), ("que", 3.90, 4.06), ("uso", 4.08, 4.24), ("estos", 4.26, 4.38), ("perfumes,", 4.38, 4.9), ("no", 4.92, 5.22),
      ("me", 5.22, 5.32), ("dejan", 5.32, 5.54), ("tranquilo.", 5.54, 6.02)]
ali_palavras([(w, a - 1.3, b - 1.3) for w, a, b in w3], t); t += 5.0
# 3 oferta: close nos frascos (boca fora do quadro) + narração TTS
segs.append(bloco("03_oferta", [(T / "V4_oferta.mp4", 0.4, 2.3, "crop=514:914:103:366,scale=720:1280")],
                  [(AU / "L4_oferta.mp3", 0, 0.1, None)], 2.3, SELO))
ali_tts(AU / "L4_oferta.alinhamento.json", t + 0.1); t += 2.3
# 4 dia: ponto de ônibus + Armaf
segs.append(bloco("04_dia", [(T / "V5_dia.mp4", 0, 5.0, None), (UB / "armaf_limpo.mp4", 0, 1.6, None)],
                  [(AU / "L5_dia.mp3", 0, 0.15, None)], 6.6))
ali_tts(AU / "L5_dia.alinhamento.json", t + 0.15); t += 6.6
# 5 noite: Asad + esposa
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.0, None), (T / "V6_noite1.mp4", 0, 5.0, None)],
                  [(AU / "L6_noche.mp3", 0, 0.15, None)], 7.0))
ali_tts(AU / "L6_noche.alinhamento.json", t + 0.15); t += 7.0
# 6 bar: pergunta da mulher (nativa)
segs.append(bloco("06_bar", [(T / "V8_bar1.mp4", 2.3, 2.1, None)], [(T / "V8_bar1.mp4", 2.3, 0, 2.1)], 2.1, SELO))
ali_palavras([("¿Qué", 0.44, 0.8), ("perfume", 0.8, 1.08), ("es", 1.08, 1.24), ("ese?", 1.24, 1.4)], t); t += 2.1
# 7 fim de semana: 9PM
segs.append(bloco("07_finde", [(UB / "9pm_limpo.mp4", 0, 4.0, None)], [(AU / "L7_finde.mp3", 0, 0.05, None)], 4.0))
ali_tts(AU / "L7_finde.alinhamento.json", t + 0.05); t += 4.0
# 8 CTA: Maestro com o pack (still com zoom lento) + rodapé
cta = P / "cenas" / "S3_oferta_1.png"
segs.append(bloco("08_cta", [(cta, 0, 4.2, "zoompan=z='1+0.0015*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30")],
                  [(AU / "L8_cta.mp3", 0, 0.2, None)], 4.2, SELO))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 4.2

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
