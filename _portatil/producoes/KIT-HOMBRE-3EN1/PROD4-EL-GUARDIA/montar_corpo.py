# -*- coding: utf-8 -*-
"""Monta o corpo do AD «El Guardia» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Adaptado do P1 (El Maestro). Selo aplicado só nas partes de IA (o unboxing já vem com selo).
Saída: corpo.mp4 e corpo.alinhamento.json (formato ElevenLabs: characters + start/end)."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU, C = P / "takes", P / "audio", P / "cenas"
UB = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\PROD1-EL-MAESTRO\unbox")  # só leitura
SELO = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\LOTE-15-10\_trabalho\A\overlay_selo.png")  # só leitura
WK = P / "_seg"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1"
ZOOM = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur):
    """partes: [(arquivo, ss, t, cadeia_vf|None, selo)]  audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None)]"""
    ins, fc = [], []
    for f, ss, t, vf, _ in partes:
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-framerate", "30", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t), "-i", str(f)]
    k = len(partes)
    ins += ["-loop", "1", "-framerate", "30", "-i", str(SELO)]; ks = k; k += 1
    n = len(partes)
    sel = [i for i, p in enumerate(partes) if p[4]]
    if len(sel) > 1:
        fc.append(f"[{ks}:v]split={len(sel)}" + "".join(f"[sx{i}]" for i in sel))
    for i, (f, ss, t, vf, selo) in enumerate(partes):
        cadeia = vf if vf else BASE + ",fps=30"
        fc.append(f"[{i}:v]{cadeia},trim=duration={t},setpts=PTS-STARTPTS[p{i}]")
        if selo:
            src = f"[sx{i}]" if len(sel) > 1 else f"[{ks}:v]"
            fc.append(f"{src}trim=duration={t},setpts=PTS-STARTPTS[s{i}]")
            fc.append(f"[p{i}][s{i}]overlay=0:0:shortest=1,format=yuv420p[v{i}]")
        else:
            fc.append(f"[p{i}]format=yuv420p[v{i}]")
    fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]")
    al = []
    for j, (f, ss, atraso, d) in enumerate(audios):
        ins += (["-ss", str(ss)] + (["-t", str(d)] if d else []) + ["-i", str(f)])
        ms = int(atraso * 1000)
        fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms}[a{j}]"); al.append(f"[a{j}]"); k += 1
    ins += ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    fc.append("".join(al) + f"[{k}:a]amix=inputs={len(al) + 1}:normalize=0:duration=longest,atrim=duration={dur}[ao]")
    out = WK / f"{nome}.mp4"
    run([*ins, "-filter_complex", ";".join(fc), "-map", "[vc]", "-map", "[ao]", "-t", str(dur), *ENC, str(out)])
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


IMG_ZOOM = BASE + "," + ZOOM
OFERTA = "crop=540:960:90:300,scale=720:1280,setsar=1," + ZOOM  # close nos 3 frascos da imagem do CTA

segs, t = [], 0.0
# 1 gancho (fala nativa da mulher)
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", 0, 3.7, None, True)], [(T / "V1_gancho.mp4", 0, 0, 3.7)], 3.7))
ali_palavras([("¡Revísame", 1.96, 2.52), ("a", 2.54, 2.6), ("mí,", 2.62, 2.76), ("mejor!", 3.02, 3.34)], t); t += 3.7
# 2 selfie (voz Diego por STS, mesmo tempo)
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", 0, 4.9, None, True)], [(AU / "v2_diego.mp3", 0, 0, 4.9)], 4.9))
w2 = [("Soy", 0.0, 0.42), ("guardia", 0.42, 0.86), ("de", 0.86, 0.9), ("mall…", 0.9, 1.14), ("y", 1.14, 1.74), ("ahora", 1.74, 2.38),
      ("las", 2.38, 2.6), ("clientas", 2.6, 3.12), ("pasan", 3.12, 3.54), ("dos", 3.54, 3.68), ("veces", 3.68, 3.9),
      ("por", 3.9, 4.18), ("la", 4.18, 4.28), ("entrada.", 4.28, 4.54)]
ali_palavras(w2, t); t += 4.9
# 3 oferta
segs.append(bloco("03_oferta", [(C / "S7_cta.png", 0, 2.5, OFERTA, True)], [(AU / "L4_oferta.mp3", 0, 0.1, None)], 2.5))
ali_tts(AU / "L4_oferta.alinhamento.json", t + 0.1); t += 2.5
# 4 dia: ronda no mall (Kling) + Armaf
segs.append(bloco("04_dia", [(T / "V3_dia.mp4", 0, 5.0, None, True), (UB / "armaf_limpo.mp4", 0, 1.6, None, False)],
                  [(AU / "L5_dia.mp3", 0, 0.15, None)], 6.6))
ali_tts(AU / "L5_dia.alinhamento.json", t + 0.15); t += 6.6
# 5 noite: Asad + esposa (Kling)
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.0, None, False), (T / "V4_noite.mp4", 0, 5.0, None, True)],
                  [(AU / "L6_noche.mp3", 0, 0.15, None)], 7.0))
ali_tts(AU / "L6_noche.alinhamento.json", t + 0.15); t += 7.0
# 6 fim de semana: cumbia (imagem com zoom) + 9PM
segs.append(bloco("06_finde", [(C / "S6_finde.png", 0, 2.0, IMG_ZOOM, True), (UB / "9pm_limpo.mp4", 0, 2.6, None, False)],
                  [(AU / "L7_finde.mp3", 0, 0.05, None)], 4.6))
ali_tts(AU / "L7_finde.alinhamento.json", t + 0.05); t += 4.6
# 7 CTA: guarita com o pack (zoom lento)
segs.append(bloco("07_cta", [(C / "S7_cta.png", 0, 4.6, IMG_ZOOM, True)], [(AU / "L8_cta.mp3", 0, 0.2, None)], 4.6))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 4.6

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
# "Nine PM" -> "9PM" no alinhamento
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
