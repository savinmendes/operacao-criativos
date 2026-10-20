# -*- coding: utf-8 -*-
"""Monta o corpo do AD «El Chofer de Micro» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Adaptado do montar_corpo.py do P1 (El Maestro). Diferença: o selo entra por PARTE (só nas cenas de IA),
porque o unboxing já vem com selo e rodapé.
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
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
ZOOM = "zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur):
    """partes: [(arquivo, ss, t, vf_extra, selo)]  audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None)]"""
    ins, fc, k = [], [], 0
    rot = []
    for i, (f, ss, t, vx, selo) in enumerate(partes):
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t), "-i", str(f)]
        fc.append(f"[{k}:v]{BASE}{(',' + vx) if vx else ''},trim=duration={t},setpts=PTS-STARTPTS[v{i}]"); k += 1
        if selo:
            ins += ["-loop", "1", "-t", str(t), "-i", str(SELO)]
            fc.append(f"[v{i}][{k}:v]overlay=0:0:shortest=1,format=yuv420p[s{i}]"); k += 1
            rot.append(f"[s{i}]")
        else:
            rot.append(f"[v{i}]")
    fc.append("".join(rot) + f"concat=n={len(partes)}:v=1:a=0[vc]")
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
    """pal: [(texto, ini, fim)] em tempo do bloco"""
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


G = json.load(open(P / "gancho_corte.json", encoding="utf-8"))  # {"ss":..,"dur":..,"palavras":[[w,a,b],...]} em tempo do take
segs, t = [], 0.0
# 1 gancho: passageiras cheiram o chofer (fala nativa da mulher)
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", G["ss"], G["dur"], None, True)], [(T / "V1_gancho.mp4", G["ss"], 0, G["dur"])], G["dur"]))
ali_palavras([(w, a - G["ss"], b - G["ss"]) for w, a, b in G["palavras"]], t); t += G["dur"]
# 2 selfie na cabine (voz Mario por STS, mesmo tempo do take)
SD = 4.9
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", 0, SD, None, True)], [(AU / "v2_mario.mp3", 0, 0, SD)], SD))
w2 = [("Soy", 0.0, 0.44), ("chofer", 0.44, 0.92), ("de", 0.92, 1.04), ("micro…", 1.04, 1.28), ("y", 1.28, 1.68), ("ahora", 1.68, 2.78),
      ("nadie", 2.78, 3.12), ("se", 3.12, 3.3), ("quiere", 3.3, 3.5), ("bajar", 3.5, 3.92), ("en", 3.92, 4.0), ("su", 4.0, 4.12), ("paradero.", 4.12, 4.64)]
ali_palavras(w2, t); t += SD
# 3 oferta: close nos frascos da imagem do CTA (zoom lento) + narração
segs.append(bloco("03_oferta", [(C / "S7_cta.png", 0, 2.4, "crop=468:832:166:448,scale=720:1280," + ZOOM, True)],
                  [(AU / "L4_oferta.mp3", 0, 0.1, None)], 2.4))
ali_tts(AU / "L4_oferta.alinhamento.json", t + 0.1); t += 2.4
# 4 dia: passageiras sorriem pelo retrovisor (Kling, para-brisa congelado = micro parada) + Armaf
segs.append(bloco("04_dia", [(T / "V4_dia_fixo.mp4", 0, 4.6, None, True), (UB / "armaf_limpo.mp4", 0, 1.8, None, False)],
                  [(AU / "L5_dia.mp3", 0, 0.15, None)], 6.4))
ali_tts(AU / "L5_dia.alinhamento.json", t + 0.15); t += 6.4
# 5 noite: Asad + esposa o abraça na cozinha
segs.append(bloco("05_noche", [(UB / "asad_limpo.mp4", 0, 2.0, None, False), (T / "V5_noche.mp4", 0, 4.4, None, True)],
                  [(AU / "L6_noche.mp3", 0, 0.15, None)], 6.4))
ali_tts(AU / "L6_noche.alinhamento.json", t + 0.15); t += 6.4
# 6 fim de semana: foto no bar de bairro (zoom lento) + 9PM
segs.append(bloco("06_finde", [(C / "S6_finde.png", 0, 1.8, ZOOM, True), (UB / "9pm_limpo.mp4", 0.5, 2.4, None, False)],
                  [(AU / "L7_finde.mp3", 0, 0.05, None)], 4.2))
ali_tts(AU / "L7_finde.alinhamento.json", t + 0.05); t += 4.2
# 7 CTA: chofer com o pack no painel da micro (zoom lento)
segs.append(bloco("07_cta", [(C / "S7_cta.png", 0, 4.2, ZOOM, True)], [(AU / "L8_cta.mp3", 0, 0.2, None)], 4.2))
ali_tts(AU / "L8_cta.alinhamento.json", t + 0.2); t += 4.2

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
# grafia da marca no alinhamento das narrações TTS ("Nine PM" -> "9PM")
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
