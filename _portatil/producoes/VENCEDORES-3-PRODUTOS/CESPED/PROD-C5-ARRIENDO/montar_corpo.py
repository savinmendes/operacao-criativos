# -*- coding: utf-8 -*-
"""Monta o corpo do AD CÉSPED C5 «Nadie arrienda» (720x1280, 30 fps) + alinhamento combinado para a legenda.
Saída: corpo.mp4 e corpo.alinhamento.json (formato ElevenLabs: characters + start/end)."""
import json, subprocess, os
from pathlib import Path

P = Path(__file__).parent
T, AU, C = P / "takes", P / "audio", P / "cenas"
BK = Path("C:/Users/PICHAU/Downloads/VENCEDORES-3-PRODUTOS/CESPED/BANCO")
SELO = BK / "overlay_selo_cesped.png"
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



# narração do mecanismo acelerada 1,1x (cabe nos takes) + alinhamento reescalado
VEL = 1.1
L4R = AU / "L4_mecanismo_r.mp3"
run(["-i", str(AU / "L4_mecanismo.mp3"), "-af", f"atempo={VEL}", str(L4R)])
_d = json.load(open(AU / "L4_mecanismo.alinhamento.json", encoding="utf-8"))
for k in ("character_start_times_seconds", "character_end_times_seconds"):
    _d[k] = [x / VEL for x in _d[k]]
json.dump(_d, open(AU / "L4_mecanismo_r.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)

ZS = "zoompan=z='1+0.0005*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"
V1, V2 = BK / "V1_720.mp4", BK / "V2_limpo_13-46.mp4"
segs, t = [], 0.0
# 1 gancho: corretor (voz nativa do Seedance), cortado após «arrendar»
segs.append(bloco("01_gancho", [(T / "V1_gancho.mp4", 0, 3.3, None)], [(T / "V1_gancho.mp4", 0, 0, 3.3)], 3.3, SELO))
ali_palavras([("Señora,", 0.48, 0.82), ("con", 0.82, 0.98), ("ese", 0.98, 1.16), ("pasto", 1.16, 1.56), ("nadie", 1.56, 1.7), ("la", 1.7, 1.9),
              ("va", 1.9, 2.0), ("a", 2.0, 2.14), ("arrendar.", 2.14, 2.52)], t); t += 3.3
# 2 persona: selfie (voz Isa por STS, mesmo tempo)
segs.append(bloco("02_persona", [(T / "V2_persona.mp4", 0, 4.7, None)], [(AU / "v2_isa.mp3", 0, 0, 4.7)], 4.7, SELO))
ali_palavras([("Tres", 0.08, 0.56), ("meses", 0.56, 0.76), ("con", 0.76, 1.02), ("la", 1.02, 1.12), ("casa", 1.12, 1.34), ("vacía…", 1.34, 1.96),
              ("y", 2.8, 3.04), ("yo", 3.04, 3.2), ("pensando", 3.2, 3.58), ("que", 3.58, 3.82), ("era", 3.82, 3.94), ("el", 3.94, 4.04), ("precio.", 4.04, 4.36)], t); t += 4.7
# 3 antes/depois real (V1 0–5,5)
segs.append(bloco("03_antes_depois", [(V1, 0, 5.5, None)], [(AU / "L3_probe.mp3", 0, 0.25, None)], 5.5))
ali_tts(AU / "L3_probe.alinhamento.json", t + 0.25); t += 5.5
# 4 mecanismo: começa pelo V2 (C ímpar); nenhum trecho repete; V2 só em trechos conferidos a 0,1 s sem fantasma da LaMa (4,6–6,6; 22,8–23,45; 24,05–24,8)
segs.append(bloco("04_mecanismo", [(V2, 4.6, 2.0, None), (V1, 11.3, 1.35, None), (V1, 6.6, 4.15, None), (V1, 18.4, 3.7, None),
                                   (V1, 24.0, 1.0, None), (V2, 22.8, 0.65, None), (V2, 24.05, 0.75, None)],
                  [(L4R, 0, 0.1, None)], 13.6))
ali_tts(AU / "L4_mecanismo_r.alinhamento.json", t + 0.1); t += 13.6
# 5 virada: casal jovem aperta a mão dela (Kling) + «Arrendada en una semana.»
segs.append(bloco("05_virada", [(T / "V5_virada.mp4", 0, 4.0, "|SELO")], [(AU / "L5_virada.mp3", 0, 1.2, None)], 4.0))
ali_tts(AU / "L5_virada.alinhamento.json", t + 1.2); t += 4.0
# 6 CTA: imagem a 80% no topo sobre fundo desfocado (produto acima da legenda, setas abaixo)
segs.append(bloco("06_cta", [(C / "S6_cta.png", 0, 6.7, "split[ca][cb];[ca]boxblur=20:2,eq=brightness=-0.1[cbg];[cb]scale=576:1024[cfg];[cbg][cfg]overlay=72:-20," + ZS)],
                  [(AU / "L6_cta.mp3", 0, 0.2, None)], 6.7, SELO))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.2); t += 6.7

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print("".join(ALI["characters"]))
