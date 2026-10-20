# -*- coding: utf-8 -*-
"""Monta o corpo do AD CÉSPED C1 «Don Raúl y la denuncia» (720x1280, 30 fps) + alinhamento combinado.
Adaptado de PROD1-EL-MAESTRO/montar_corpo.py. Saída: corpo.mp4 e corpo.alinhamento.json."""
import json, subprocess
from pathlib import Path

P = Path(__file__).parent
T, AU, C = P / "takes", P / "audio", P / "cenas"
B = Path(r"C:\Users\PICHAU\Downloads\VENCEDORES-3-PRODUTOS\CESPED\BANCO")
V1, V2 = B / "V1_720.mp4", B / "V2_limpo_13-46.mp4"
SELO = B / "overlay_selo_cesped.png"
WK = P / "_seg"; WK.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
BASE = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30"
ZOOM = "zoompan=z='1+{v}*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30"


def run(c):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)


def bloco(nome, partes, audios, dur, overlay=None):
    """partes: [(arquivo, ss, t, vf_extra)]  audios: [(arquivo, ss_no_arquivo, atraso_no_bloco, dur|None, af|None)]"""
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
    for j, (f, ss, atraso, d, af) in enumerate(audios):
        ins += (["-ss", str(ss)] + (["-t", str(d)] if d else []) + ["-i", str(f)])
        ms = int(atraso * 1000)
        fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo{(',' + af) if af else ''},adelay={ms}|{ms}[a{j}]")
        al.append(f"[a{j}]"); k += 1
    ins += ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    fc.append("".join(al) + f"[{k}:a]amix=inputs={len(al) + 1}:normalize=0:duration=longest,atrim=duration={dur}[ao]")
    out = WK / f"{nome}.mp4"
    run([*ins, "-filter_complex", ";".join(fc), "-map", vout, "-map", "[ao]", "-t", str(dur), *ENC, str(out)])
    return out


ALI = {"characters": [], "character_start_times_seconds": [], "character_end_times_seconds": []}


def ali_palavras(pal, t0):
    for w, a, b in pal:
        s = w + " "
        step = (b - a) / max(len(w), 1)
        for c_i, ch in enumerate(s):
            st = t0 + a + min(c_i, len(w)) * step
            ALI["characters"].append(ch)
            ALI["character_start_times_seconds"].append(round(st, 3))
            ALI["character_end_times_seconds"].append(round(st + step, 3))


def ali_tts(arq, t0):
    d = json.load(open(arq, encoding="utf-8"))
    for ch, a, b in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
        ALI["characters"].append(ch); ALI["character_start_times_seconds"].append(round(t0 + a, 3))
        ALI["character_end_times_seconds"].append(round(t0 + b, 3))
    ALI["characters"].append(" "); ALI["character_start_times_seconds"].append(ALI["character_end_times_seconds"][-1])
    ALI["character_end_times_seconds"].append(ALI["character_end_times_seconds"][-1])


def gate(trechos):
    """volume 1 só nos trechos de fala (tempo do arquivo de áudio), resto mudo — tira o chiado do STS nas pausas"""
    cond = "+".join(f"between(t,{a},{b})" for a, b in trechos)
    return f"volume='if({cond},1,0)':eval=frame"


SFX = AU / "sfx_msg.mp3"
segs, t = [], 0.0
# 1 GANCHO: tela do grupo (msg 1, msg 2) + Don Raúl em pânico (fala STS Arturo)
G0 = 1.3   # início do take
segs.append(bloco("01_gancho",
    [(C / "T1a.png", 0, 0.9, ZOOM.format(v=0.0008)), (C / "T1b.png", 0, 1.3, ZOOM.format(v=0.0008)),
     (T / "V1_gancho.mp4", G0, 3.6, None)],
    [(SFX, 0, 0.02, None, "volume=0.8"), (SFX, 0, 0.92, None, "volume=0.8"),
     (AU / "v1_arturo.mp3", G0, 2.2, 3.6, gate([(1.85 - G0, 3.1 - G0), (3.7 - G0, 4.75 - G0)]) + ",volume=1.3")],
    5.8, SELO))
ali_palavras([(w, a - G0 + 2.2, b - G0 + 2.2) for w, a, b in
              [("¿Me", 1.98, 2.12), ("van", 2.12, 2.26), ("a", 2.26, 2.36), ("denunciar…", 2.36, 3.0),
               ("por", 3.8, 3.98), ("el", 3.98, 4.1), ("pasto?", 4.1, 4.6)]], t); t += 5.8
# 2 PERSONA: selfie com a máquina a bencina (fala STS Arturo)
PER = json.load(open(P / "persona.json", encoding="utf-8"))   # {"ini","dur","trechos":[[a,b]],"palavras":[[w,a,b]]} (tempo do take)
segs.append(bloco("02_persona", [(T / "V2_persona.mp4", PER["ini"], PER["dur"], None)],
                  [(AU / "v2_arturo.mp3", PER["ini"], 0, PER["dur"], gate([(a - PER["ini"], b - PER["ini"]) for a, b in PER["trechos"]]) + ",volume=1.3")],
                  PER["dur"], SELO))
ali_palavras([(w, a - PER["ini"], b - PER["ini"]) for w, a, b in PER["palavras"]], t); t += PER["dur"]
# 3+4 ANTES/DEPOIS + MECANISMO (takes reais, sem áudio original; C1 ímpar: o mecanismo começa pelo V2)
reais = [(V1, 0.3, 4.0),            # antes/depois: corredor com mato -> faixa limpa
         # V2 (LaMa) tem texto fantasma em vários pontos (6,5–6,9; 8,5–11; 12,3–12,4; 13,2–13,4; 22,8–24; 25,3–25,7):
         # só entra o trecho conferido quadro a quadro (12,5–13,1). C1 ímpar: o mecanismo começa pelo V2.
         (V2, 12.5, 0.6),           # lâmina de metal no mato (V2)
         (V1, 12.0, 0.95),          # borda da calçada ("orilladora y bordeadora")
         (V1, 6.3, 2.0),            # rodas
         (V1, 12.95, 1.8),          # borda da calçada, uma mão
         (V1, 20.5, 2.7),           # faixas no mato alto ("cuchilla de metal")
         (V1, 24.0, 2.2),           # gramado lateral
         (V1, 16.4, 1.8),           # POV do gatilho ("inalámbrica")
         (V1, 26.2, 1.95)]          # gramado lateral, fim           # mato alto perto do galpão
DR = round(sum(d for _, _, d in reais), 2)
segs.append(bloco("03_real", [(f, ss, d, None) for f, ss, d in reais],
                  [(AU / "L3_probe.mp3", 0, 0.4, None, None), (AU / "L4_mecanismo.mp3", 0, 2.0, None, None)], DR))
ali_tts(AU / "L3_probe.alinhamento.json", t + 0.4); ali_tts(AU / "L4_mecanismo.alinhamento.json", t + 2.0); t += DR
# 5 VIRADA: msg da Sra. Marta no grupo + Don Raúl sorrindo no antejardín cortado (Kling, sem fala)
segs.append(bloco("05_virada", [(C / "T5.png", 0, 2.4, ZOOM.format(v=0.0008)), (T / "V5_virada.mp4", 0.5, 3.0, None)],
                  [(SFX, 0, 0.1, None, "volume=0.8")], 5.4, SELO))
t += 5.4
# 6 CTA: Don Raúl com o produto original (still com zoom lento) + narração
segs.append(bloco("06_cta", [(C / "S6_cta.png", 0, 9.1, ZOOM.format(v=0.0006))],
                  [(AU / "L6_cta.mp3", 0, 0.2, None, None)], 9.1, SELO))
ali_tts(AU / "L6_cta.alinhamento.json", t + 0.2); t += 9.1

lst = WK / "lista.txt"
lst.write_text("".join(f"file '{s.as_posix()}'\n" for s in segs), encoding="utf-8")
run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(P / "corpo.mp4")])
json.dump(ALI, open(P / "corpo.alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
print("duração", round(t, 2)); print("".join(ALI["characters"]))
