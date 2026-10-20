# -*- coding: utf-8 -*-
"""Monta o corpo do AD CÉSPED C10 «El Jardinero Fantasma» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Adaptado do montar_corpo.py dos perfumes (P1/P10). Saída: corpo.mp4 e corpo.alinhamento.json."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU, C = P / "takes", P / "audio", P / "cenas"
BANCO = Path(r"C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\BANCO")
V1, V2 = BANCO / "V1_720.mp4", BANCO / "V2_limpo_13-46.mp4"
SELO = BANCO / "overlay_selo_cesped.png"
WK = P / "_seg"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
TK = json.load(open(P / "tempos.json", encoding="utf-8"))  # tempos medidos nos takes (whisper)


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur, overlay=None):
    """partes: [(arquivo, ss, t, vf_extra)]; vf_extra pode terminar em '|SELO' (selo só naquela parte)
    e pode conter '@TELA=<png>' (cartão de celular sobreposto, 470 px de largura, no alto).
    audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None)]"""
    ins, fc, extra = [], [], []
    for i, (f, ss, t, vx) in enumerate(partes):
        if str(f).endswith(".png"):
            ins += ["-loop", "1", "-t", str(t), "-i", str(f)]
        else:
            ins += ["-ss", str(ss), "-t", str(t), "-i", str(f)]
        vx = vx or ""
        sel = vx.endswith("|SELO")
        if sel: vx = vx[:-5]
        tela = None
        if "@TELA=" in vx:
            vx, tela = vx.split("@TELA=")
        extra.append((i, t, sel, tela))
        fc.append(f"[{i}:v]{BASE}{(',' + vx.strip(',')) if vx.strip(',') else ''},trim=duration={t},setpts=PTS-STARTPTS[r{i}]")
    n, k = len(partes), len(partes)
    for i, t, sel, tela in extra:
        cur = f"r{i}"
        if tela:
            ins += ["-loop", "1", "-t", str(t), "-i", str(tela)]
            fc.append(f"[{k}:v]scale=470:-1,fps=30[tl{i}];[{cur}][tl{i}]overlay=125:130:shortest=1[t{i}]"); cur = f"t{i}"; k += 1
        if sel:
            ins += ["-loop", "1", "-t", str(t), "-i", str(SELO)]
            fc.append(f"[{cur}][{k}:v]overlay=0:0:shortest=1[s{i}]"); cur = f"s{i}"; k += 1
        fc.append(f"[{cur}]null[v{i}]")
    fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]")
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


def zp(v=0.0012):
    return f"zoompan=z='1+{v}*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"


FUNDO = "boxblur=18:2,eq=brightness=-0.12,"
segs, t = [], 0.0

# 1 GANCHO: 3 mensagens iguais chegando (tela por código sobre a cena desfocada) + «¿Otra vez?» (Seedance, voz STS)
g = TK["gancho"]  # {"ss": início do corte no take, "dur": duração, "pal": [[w,a,b] em tempo do take]}
tg = [0.6, 0.6, 0.9]; TG = sum(tg)
segs.append(bloco("01_gancho", [
    (C / "S1_gancho.png", 0, tg[0], FUNDO + zp(0.0008) + "@TELA=" + str(C / "tela_g1.png") + "|SELO"),
    (C / "S1_gancho.png", 0, tg[1], FUNDO + zp(0.0008) + "@TELA=" + str(C / "tela_g2.png") + "|SELO"),
    (C / "S1_gancho.png", 0, tg[2], FUNDO + zp(0.0008) + "@TELA=" + str(C / "tela_g3.png") + "|SELO"),
    (T / "V1_gancho.mp4", g["ss"], g["dur"], "|SELO")],
    [(AU / "gancho_jc.mp3", g["ss"], TG, g["dur"])], TG + g["dur"]))
ali_palavras([(w, a - g["ss"] + TG, b - g["ss"] + TG) for w, a, b in g["pal"]], t); t += TG + g["dur"]
FIM_GANCHO = t

# 2 PERSONA: selfie (Seedance, voz STS)
s = TK["selfie"]
segs.append(bloco("02_selfie", [(T / "V2_selfie.mp4", s["ss"], s["dur"], "|SELO")],
                  [(AU / "selfie_jc.mp3", s["ss"], 0, s["dur"])], s["dur"]))
ali_palavras([(w, a - s["ss"], b - s["ss"]) for w, a, b in s["pal"]], t); t += s["dur"]

# 3 ANTES/DEPOIS real (V1 0–5) + «Hasta que probé esta.»
segs.append(bloco("03_antes_depois", [(V1, 0, 5.0, None)], [(AU / "L3_probe_c.mp3", 0, 0.25, None)], 5.0))
ali_tts(AU / "L3_probe.alinhamento_c.json", t + 0.25); t += 5.0

# 4 MECANISMO real (C par começa pelo V1): borda → rodas → mato alto → kit (baterias)
M = TK["mecanismo"]  # cortes [ini, fim] no tempo da narração
d1, d2, d3 = M[0], M[1] - M[0], M[2] - M[1]
dm = TK["mec_dur"]; d4 = dm - M[2]
segs.append(bloco("04_mecanismo", [(V1, 11.3, d1, None), (V1, 6.2, d2, None), (V1, 18.0, d3, None), (V2, 22.8, 0.7, None), (V2, 24.0, 0.9, None), (V1, 24.5, d4 - 1.6, None)],
                  [(AU / "L4_mecanismo_c.mp3", 0, 0.1, None)], dm))
ali_tts(AU / "L4_mecanismo.alinhamento_c.json", t + 0.1); t += dm

# 5 VIRADA: Kling (ele digita) → tela com a resposta + narração da resposta → Kling (sorriso)
k1, k2 = TK["kling"]
segs.append(bloco("05_virada", [
    (T / "V3_virada.mp4", 0, k1, "|SELO"),
    (C / "S5_virada.png", 0, 2.75, FUNDO + zp(0.0008) + "@TELA=" + str(C / "tela_v.png") + "|SELO"),
    (T / "V3_virada.mp4", k2, 1.4, "|SELO")],
    [(AU / "L5_virada_c.mp3", 0, k1 + 0.15, None)], k1 + 2.75 + 1.4))
ali_tts(AU / "L5_virada.alinhamento_c.json", t + k1 + 0.15); t += k1 + 2.75 + 1.4

# 6 CTA: ele com o produto original (still com zoom lento) + narração CTA
segs.append(bloco("06_cta", [(C / "S6_cta.png", 0, 6.1, zp(0.0006))], [(AU / "L6_cta_c.mp3", 0, 0.2, None)], 6.1, SELO))
ali_tts(AU / "L6_cta.alinhamento_c.json", t + 0.2); t += 6.1

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{x.as_posix()}'\n" for x in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
txt = "".join(ALI["characters"])
# «90» na legenda (o TTS diz «noventa días»; o alinhamento mantém o texto escrito)
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2), "fim do gancho", round(FIM_GANCHO, 2)); print(txt)
