# -*- coding: utf-8 -*-
"""Monta o corpo do AD «El Feriante» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Saída: corpo.mp4 e corpo.alinhamento.json (formato ElevenLabs: characters + start/end)."""
import json, subprocess, os
from pathlib import Path

P = Path(__file__).parent
T, AU = P / "takes", P / "audio"
UB = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PROD1-EL-MAESTRO\unbox")  # compartilhado, só leitura
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
    n = len(partes)
    for i, (f, ss, t, vx, sl) in enumerate(partes):
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t), "-i", str(f)]
    k = n
    for i, (f, ss, t, vx, sl) in enumerate(partes):
        pos = ("," + vx) if vx else ""
        fc.append(f"[{i}:v]{BASE}{pos},trim=duration={t},setpts=PTS-STARTPTS[p{i}]")
        if sl:
            ins += ["-i", str(SELO)]
            fc.append(f"[p{i}][{k}:v]overlay=0:0:shortest=0:eof_action=repeat[v{i}]"); k += 1
        else:
            fc.append(f"[p{i}]null[v{i}]")
    fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]")
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
C = P / "cenas"
ZOOM = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
# 1 gancho (fala nativa da casera), começa em 0,6 s do take
G0, GD = 0.6, 3.7
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", G0, GD, None, True)], [(T / "V1_gancho.mp4", G0, 0, GD)], GD))
wg = [("¡Casero!", 2.36, 2.88), ("¿Qué", 2.96, 3.22), ("perfume", 3.22, 3.66), ("es", 3.66, 3.84), ("ese?", 3.84, 4.08)]
ali_palavras([(w, a - G0, b - G0) for w, a, b in wg], t); t += GD
# 2 selfie (voz Alejandro Duran por STS, mesmo tempo)
SD = 4.8
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", 0, SD, None, True)], [(AU / "v2_alejandro.mp3", 0, 0, SD)], SD))
w2 = [("Soy", 0.0, 0.42), ("feriante…", 0.42, 0.98), ("y", 0.98, 1.26), ("ahora", 1.26, 1.9), ("vendo", 1.9, 2.26), ("más", 2.26, 2.42),
      ("por", 2.42, 2.66), ("el", 2.66, 2.82), ("aroma", 2.82, 3.06), ("que", 3.06, 3.7), ("por", 3.7, 3.86), ("las", 3.86, 4.02), ("paltas.", 4.02, 4.54)]
ali_palavras(w2, t); t += SD
# 3 oferta: close nos frascos da imagem do CTA (zoom lento) + TTS
OD = 2.6
segs.append(bloco("03_oferta", [(C / "S7_cta.png", 0, OD, "crop=520:924:130:390,scale=720:1280," + ZOOM, True)],
                  [(AU / "L4_oferta.mp3", 0, 0.1, None)], OD))
ali_tts(AU / "L4_oferta.alinhamento.json", t + 0.1); t += OD
# 4 dia: Kling feira + Armaf
segs.append(bloco("04_dia", [(T / "V3_dia.mp4", 0, 4.2, None, True), (UB / "armaf_limpo.mp4", 0, 2.0, None, False)],
                  [(AU / "L5_dia.mp3", 0, 0.15, None)], 6.2))
ali_tts(AU / "L5_dia.alinhamento.json", t + 0.15); t += 6.2
# 5 noite: Asad + Kling dançando na sala
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.0, None, False), (T / "V4_noite.mp4", 0, 4.6, None, True)],
                  [(AU / "L6_noche.mp3", 0, 0.15, None)], 6.6))
ali_tts(AU / "L6_noche.alinhamento.json", t + 0.15); t += 6.6
# 6 fim de semana: asado (imagem com zoom) + 9PM
segs.append(bloco("06_finde", [(C / "S6_finde.png", 0, 2.0, ZOOM, True), (UB / "9pm_limpo.mp4", 0, 2.4, None, False)],
                  [(AU / "L7_finde.mp3", 0, 0.1, None)], 4.4))
ali_tts(AU / "L7_finde.alinhamento.json", t + 0.1); t += 4.4
# 7 CTA: feriante com o pack no caixote de tomates
segs.append(bloco("07_cta", [(C / "S7_cta.png", 0, 4.7, ZOOM, True)], [(AU / "L8_cta.mp3", 0, 0.2, None)], 4.7))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 4.7

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
