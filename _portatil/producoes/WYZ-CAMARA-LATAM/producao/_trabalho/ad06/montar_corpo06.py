# -*- coding: utf-8 -*-
"""AD 06 (esquete vizinhos) reconstruido: avatares HeyGen (vecina/vecino) + takes sem rosto do original.
Gera corpo.mp4 (720x1280, 30 fps) + alinhamento.json (legenda) e linha_tempo.json."""
import json
import subprocess
from pathlib import Path

T = Path(__file__).resolve().parent
ORIG = T.parents[2] / "originais" / "06.mp4"
FUNDO = T.parent / "sep_0609" / "htdemucs" / "orig06" / "no_vocals.wav"
TTS = T / "tts"
OFF = json.load(open(TTS / "offsets.json"))
GAP = 0.25
ORDEM = ["F1", "M1", "M2", "F2", "M3", "M4", "M5", "F3", "M6", "F4", "M7"]
BROLL = {  # trechos do original sem rosto (s)
    "M2": [(12.8, 15.5), (16.0, 18.5)],
    "M4": [(25.8, 28.8), (29.8, 32.2)],
    "M5": [(33.8, 36.0), (39.7, 41.2)],
    "M6": [(41.3, 43.3)],
}
CROP = "crop=574:1020:73:0,scale=720:1280:flags=lanczos,setsar=1,fps=30"
BLUR_FONE = (12.8, 15.5, 180, 540, 320, 170)  # rostos dos atores na tela do celular: t0,t1,x,y,w,h


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def ff(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", *map(str, args)], check=True)


partes = T / "partes"
partes.mkdir(exist_ok=True)
t = 0.15
linha = []
for i, k in enumerate(ORDEM):
    d = dur(TTS / f"{k}.mp3")
    L = d + (GAP if i < len(ORDEM) - 1 else 0.7)
    out = partes / f"{i:02d}_{k}.mp4"
    if k in BROLL:
        segs = BROLL[k]
        tot = sum(b - a for a, b in segs)
        vel = min(1.0, tot / L)  # se faltar take, desacelera levemente (>=0.8)
        assert vel >= 0.8, (k, vel)
        ins, fc = [], []
        for j, (a, b) in enumerate(segs):
            ins += ["-ss", f"{a}", "-t", f"{b - a}", "-i", ORIG]
            extra = ""
            if (a, b) == (12.8, 15.5):
                x0, y0, w, h = BLUR_FONE[2:]
                extra = (f",split[s{j}a][s{j}b];[s{j}b]crop={w}:{h}:{x0}:{y0},boxblur=18:2[s{j}c];"
                         f"[s{j}a][s{j}c]overlay={x0}:{y0}")
            fc.append(f"[{j}:v]setpts=PTS-STARTPTS{extra},{CROP}[c{j}]")
        fc.append("".join(f"[c{j}]" for j in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,setpts=PTS/{vel:.4f},"
                  f"trim=duration={L:.3f},setpts=PTS-STARTPTS[v]")
        ff([*ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16",
            "-pix_fmt", "yuv420p", "-r", "30", out])
        fonte = "broll"
    else:
        av = T / ("vecina.mp4" if k.startswith("F") else "vecino.mp4")
        a = max(0.0, OFF[k] - 0.15)
        ff(["-ss", f"{a:.3f}", "-t", f"{L:.3f}", "-i", av, "-vf", "scale=720:1280:flags=lanczos,setsar=1,fps=30",
            "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out])
        fonte = av.name
    linha.append({"k": k, "inicio": round(t, 3), "dur_fala": round(d, 3), "dur_cena": round(L, 3), "fonte": fonte})
    t += L

# video concat
lst = partes / "lista.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in sorted(partes.glob("*.mp4"))), encoding="utf-8")
ff(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", T / "video_mudo.mp4"])
total = dur(T / "video_mudo.mp4")

# audio: falas nas posicoes + fundo baixo
ins2 = ["-i", T / "video_mudo.mp4", "-i", FUNDO]
fc2 = [f"[1:a]atrim=0:{total:.3f},volume=0.45,aresample=48000[bg]"]
for j, it in enumerate(linha):
    ins2 += ["-i", TTS / f"{it['k']}.mp3"]
    ms = int(it["inicio"] * 1000)
    fc2.append(f"[{j + 2}:a]aresample=48000,adelay={ms}|{ms}[f{j}]")
fc2.append("[bg]" + "".join(f"[f{j}]" for j in range(len(linha))) +
           f"amix=inputs={len(linha) + 1}:normalize=0:duration=first[a]")
ff([*ins2, "-filter_complex", ";".join(fc2), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
    "-b:a", "192k", "-t", f"{total:.3f}", T / "corpo.mp4"])

# alinhamento combinado
C, S, E = [], [], []
for it in linha:
    al = json.load(open(TTS / f"{it['k']}.alinhamento.json", encoding="utf-8"))
    al = al.get("alignment") or al
    if C:
        C.append(" ")
        S.append(S[-1] if S else 0)
        E.append(E[-1] if E else 0)
    C += al["characters"]
    S += [round(x + it["inicio"], 3) for x in al["character_start_times_seconds"]]
    E += [round(x + it["inicio"], 3) for x in al["character_end_times_seconds"]]
json.dump({"characters": C, "character_start_times_seconds": S, "character_end_times_seconds": E},
          open(T / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(linha, open(T / "linha_tempo.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
av_s = sum(it["dur_cena"] for it in linha if it["fonte"] != "broll")
print(f"ok corpo.mp4 {total:.2f}s | avatar {av_s:.1f}s ({100 * av_s / total:.0f}%)")
for it in linha:
    print(it)
