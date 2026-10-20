# -*- coding: utf-8 -*-
"""Base de um AD Wyze (EN -> ES LATAM), Grupo A (ad04/ad05):
- faixa opaca (alpha 255) cobrindo a legenda queimada em inglês;
- áudio: fundo sem voz (demucs no_vocals) + narração nova ElevenLabs;
  narração inteira com atempo  OU  em blocos (frases) posicionados no tempo das cenas;
- congelamento opcional do último quadro (cauda) para a fala caber;
- alinhamento ajustado para a legenda do kit.
  python preparar_wyze.py adNN/prep.json"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 720, 1280
cfg_path = Path(sys.argv[1]).resolve()
R = json.load(open(cfg_path, encoding="utf-8"))
T = cfg_path.parent


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def faixa(y0, y1, destino, grad=24):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(max(0, y0 - grad), min(H, y1 + grad)):
        if y0 <= y < y1:
            a = 255
        elif y < y0:
            a = int(255 * (y - (y0 - grad)) / grad)
        else:
            a = int(255 * ((y1 + grad) - y) / grad)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img.save(destino)


# 1) faixa
fx = R["faixa"]
faixa(fx[0], fx[1], T / "faixa.png")

# 2) narração + alinhamento
al = json.load(open(T / R["narr"].replace(".mp3", ".alinhamento.json"), encoding="utf-8"))
al = al.get("alignment") or al
S, E = al["character_start_times_seconds"], al["character_end_times_seconds"]
narr_src = T / R["narr"]
narr = T / "narr_pos.wav"
if "blocos" in R:
    # blocos: [[char_ini, destino_s], ...] — cada bloco vai do char_ini até o char_ini do próximo
    bl = R["blocos"]
    n = len(S)
    filtros, ins, novS, novE = [], [], list(S), list(E)
    for k, (ci, dst) in enumerate(bl):
        cj = bl[k + 1][0] if k + 1 < len(bl) else n
        a = max(0.0, S[ci] - 0.04)
        b = (S[cj] - 0.04) if cj < n else E[-1] + 0.05
        filtros.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,adelay={int(dst * 1000)}|{int(dst * 1000)}[b{k}]")
        off = dst - a
        for i in range(ci, cj):
            novS[i] = round(S[i] + off, 3)
            novE[i] = round(E[i] + off, 3)
    filtros.append("".join(f"[b{k}]" for k in range(len(bl))) + f"amix=inputs={len(bl)}:normalize=0,aresample=48000[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", narr_src, "-filter_complex", ";".join(filtros), "-map", "[a]",
                    "-ac", "1", narr], check=True)
    al["character_start_times_seconds"], al["character_end_times_seconds"] = novS, novE
else:
    at = R.get("atempo", 1.0)
    t0 = R.get("narr_inicio", 0.15)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", narr_src, "-af",
                    f"atempo={at},aresample=48000,adelay={int(t0 * 1000)}|{int(t0 * 1000)}", "-ac", "1", narr], check=True)
    for k in ("character_start_times_seconds", "character_end_times_seconds"):
        al[k] = [round(t / at + t0, 3) for t in al[k]]
json.dump(al, open(T / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
fim_narr = al["character_end_times_seconds"][-1]

# 3) render
vid = R["video"]
cauda = R.get("cauda_congelada", 0.0)
total = dur(vid) + cauda
fundo = T / "sep" / "htdemucs" / "orig" / "no_vocals.wav"
vf = f"[0:v]setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={cauda:.3f}[v0];[v0][3:v]overlay=0:0[v]"
fc = [vf,
      f"[1:a]volume={R.get('fundo_vol', 0.5)},aresample=48000,apad[bg]",
      "[2:a]aresample=48000,apad[nv]",
      f"[bg][nv]amix=inputs=2:normalize=0,atrim=0:{total:.3f}[a]"]
saida = T / "corpo.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", fundo, "-i", narr, "-i", T / "faixa.png",
                "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", saida], check=True)
print(f"ok {saida} | {dur(saida):.2f}s | narração termina em {fim_narr:.2f}s")
