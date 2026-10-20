# -*- coding: utf-8 -*-
"""Monta o corpo do AD «El Garzón» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Saída: corpo.mp4 e corpo.alinhamento.json (formato ElevenLabs: characters + start/end)."""
import json, subprocess, os
from pathlib import Path

P = Path(__file__).parent
T, AU = P / "takes", P / "audio"
UB = P.parent / "PROD1-EL-MAESTRO" / "unbox"  # compartilhado, só leitura
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
    for i, pt in enumerate(partes):
        f, ss, t, vx = pt[:4]
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t), "-i", str(f)]
        fc.append(f"[{i}:v]{BASE}{(',' + vx) if vx else ''},trim=duration={t},setpts=PTS-STARTPTS[v{i}]")
    n = len(partes)
    fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]")
    k = n
    sel = [i for i, pt in enumerate(partes) if len(pt) > 4 and pt[4]]
    if sel and not overlay:
        ins += ["-i", str(SELO)]; ks = k; k += 1
        for i in sel:
            fc = [x.replace(f"setpts=PTS-STARTPTS[v{i}]", f"setpts=PTS-STARTPTS[w{i}]") for x in fc]
            fc.insert(-1, f"[w{i}][{ks}:v]overlay=0:0[v{i}]")
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
ZP = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
C = P / "cenas"
# 1 gancho (fala nativa da cliente), a partir de 1.4 s do take
G0, GD = 1.4, 3.65
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", G0, GD, None)], [(T / "V1_gancho.mp4", G0, 0, GD)], GD, SELO))
ali_palavras([(w, a - G0, b - G0) for w, a, b in [("¡Oiga,", 1.70, 2.30), ("garzón!", 2.40, 2.95), ("¿Qué", 3.35, 3.55), ("perfume", 3.55, 3.95),
              ("anda", 3.95, 4.20), ("trayendo?", 4.20, 4.95)]], t); t += GD
# 2 selfie (voz Damián por STS, mesmo tempo; «propina» refeita por TTS da mesma voz)
SD = 5.05
segs.append(bloco("02_selfie", [(T / "V3_selfie.mp4", 0, SD, None)], [(AU / "v3_fix.mp3", 0, 0, SD)], SD, SELO))
ali_palavras([("Soy", 0.0, 0.46), ("garzón", 0.46, 0.88), ("hace", 0.88, 1.06), ("veinte", 1.06, 1.3), ("años…", 1.3, 1.78), ("y", 1.78, 2.14),
              ("nunca", 2.14, 3.0), ("me", 3.0, 3.2), ("habían", 3.2, 3.4), ("dejado", 3.4, 3.84), ("tanta", 3.9, 4.36), ("propina.", 4.38, 4.9)], t); t += SD
# 3 oferta: close nos frascos da imagem do CTA (zoom lento) + TTS
segs.append(bloco("03_oferta", [(C / "S7_cta.png", 0, 2.5, "crop=420:747:132:396,scale=720:1280," + ZP)],
                  [(AU / "L4_oferta.mp3", 0, 0.1, None)], 2.5, SELO))
ali_tts(AU / "L4_oferta.alinhamento.json", t + 0.1); t += 2.5
# 4 dia: Kling (selo) + Armaf (já tem selo); narração acelerada 8%
segs.append(bloco("04_dia", [(T / "V5_dia.mp4", 0, 5.0, None, True), (UB / "armaf_limpo.mp4", 0, 2.0, None)],
                  [(AU / "L5_dia_r.mp3", 0, 0.12, None)], 7.0))
ali_tts(AU / "L5_dia_r.alinhamento.json", t + 0.12); t += 7.0
# 5 noite: Asad + Kling (selo) + esposa
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.2, None), (T / "V6_noite.mp4", 0, 5.0, None, True)],
                  [(AU / "L6_noche.mp3", 0, 0.12, None)], 7.2))
ali_tts(AU / "L6_noche.alinhamento.json", t + 0.12); t += 7.2
# 6 fim de semana: imagem do asado (zoom lento, selo) + 9PM
segs.append(bloco("06_finde", [(C / "S6_finde.png", 0, 1.6, ZP, True), (UB / "9pm_limpo.mp4", 0, 2.6, None)],
                  [(AU / "L7_finde.mp3", 0, 0.08, None)], 4.2))
ali_tts(AU / "L7_finde.alinhamento.json", t + 0.08); t += 4.2
# 7 CTA: garzón com o pack na bandeja (zoom lento)
segs.append(bloco("07_cta", [(C / "S7_cta.png", 0, 5.6, ZP)], [(AU / "L8_cta.mp3", 0, 0.2, None)], 5.6, SELO))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 5.6

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
