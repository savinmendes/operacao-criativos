# -*- coding: utf-8 -*-
"""Monta o corpo do AD «F3 Entrevista en la calle» (720x1280, 30 fps) + alinhamento combinado para a legenda.
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
TM = json.load(open(P / "_tempos.json", encoding="utf-8"))  # cortes e palavras dos takes (QA whisper)
segs, t = [], 0.0
# 1 gancho: Kling (entrevistador de costas oferecendo o microfone) + pergunta do Richard
G = TM["gancho"]
segs.append(bloco("01_gancho", [(T / "V_gancho.mp4", G["ss"], G["dur"], None)], [(AU / "L1_gancho.mp3", 0, 0.25, None)], G["dur"], SELO))
ali_tts(AU / "L1_gancho.alinhamento.json", t + 0.25); t += G["dur"]
# 2-4 reações (fala nativa Seedance) + unboxing + nome do perfume (Richard)
UBX = {"M1": ("armaf_limpo.mp4", "L2_armaf"), "M2": ("asad_limpo.mp4", "L3_asad"), "M3": ("9pm_limpo.mp4", "L4_9pm")}
for i, m in enumerate(["M1", "M2", "M3"]):
    r = TM[m]
    segs.append(bloco(f"0{2 + 2 * i}_{m}", [(T / f"V_{m}.mp4", r["ss"], r["dur"], None)], [(T / f"V_{m}.mp4", r["ss"], 0, r["dur"])], r["dur"], SELO))
    ali_palavras([(w, a - r["ss"], b - r["ss"]) for w, a, b in r["pal"]], t); t += r["dur"]
    ub, nar = UBX[m]
    ud = ffdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(AU / f"{nar}.mp3")], capture_output=True, text=True).stdout)
    dur = round(max(ud + 0.35, 2.0), 2)
    segs.append(bloco(f"0{3 + 2 * i}_{m}_ub", [(UB / ub, 0, dur, "tpad=stop_mode=clone:stop_duration=2")], [(AU / f"{nar}.mp3", 0, 0.1, None)], dur))
    ali_tts(AU / f"{nar}.alinhamento.json", t + 0.1); t += dur
# 8 fechamento: close nos frascos (CTA) sobre fundo desfocado + «te llevas los tres al precio de uno»
segs.append(bloco("08_cierre", [(C / "S6_cta.png", 0, 3.2, "split[oa][ob];[oa]boxblur=20:2,eq=brightness=-0.08[obg];[ob]crop=540:330:90:730,scale=720:440[ofg];[obg][ofg]overlay=0:770," + ZP + "|SELO")],
                  [(AU / "L5_cierre.mp3", 0, 0.15, None)], 3.2))
ali_tts(AU / "L5_cierre.alinhamento.json", t + 0.15); t += 3.2
# 9 CTA: entrevistador com o pack (zoom lento)
ZC = "zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.3':d=1:s=720x1280:fps=30"
segs.append(bloco("09_cta", [(C / "S6_cta.png", 0, 4.2, ZC)], [(AU / "L6_cta.mp3", 0, 0.2, None)], 4.2, SELO))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.2); t += 4.2

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
txt = "".join(ALI["characters"])
for velho, novo in [("Nine PM", "9PM"), ("veinticuatro", "24")]:
    i = txt.find(velho)
    if i >= 0:
        n = len(velho)
        s0, e0 = ALI["character_start_times_seconds"][i], ALI["character_end_times_seconds"][i + n - 1]
        ALI["characters"][i:i + n] = list(novo)
        ALI["character_start_times_seconds"][i:i + n] = [s0] * len(novo)
        ALI["character_end_times_seconds"][i:i + n] = [e0] * len(novo)
        txt = "".join(ALI["characters"])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print(txt)
