# -*- coding: utf-8 -*-
"""Base de um AD Wyze (EN -> ES LATAM), adaptado do preparar_corpo.py da Podadora:
- cobre a legenda em inglês com caixa opaca (alpha 252) e o título do topo com caixa nova em espanhol;
- troca o áudio: fundo sem voz (demucs) + narração nova, com atempo opcional;
- congela o último quadro se a narração passar do fim do vídeo;
- gera o alinhamento deslocado/escalado para a legenda do kit.
  python preparar_corpo_wyze.py adNN/prep.json"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
FB = str(KIT / "fonts" / "Poppins-Bold.ttf")
W, H = 720, 1280
CFG = Path(sys.argv[1]).resolve()
R = json.load(open(CFG, encoding="utf-8"))
T = CFG.parent


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def caixa(spec, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(spec["rect"], radius=spec.get("raio", 14), fill=tuple(spec.get("cor", [0, 0, 0])) + (252,))
    img.save(destino)


def titulo(spec, destino):
    """Caixa branca opaca cobrindo o título original inteiro, com o texto novo em preto."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FB, spec["px"])
    d.rounded_rectangle(spec["rect"], radius=14, fill=(255, 255, 255, 255))
    x0, y0, x1, y1 = spec["rect"]
    lh = int(spec["px"] * 1.3)
    ty = (y0 + y1) / 2 - lh * len(spec["linhas"]) / 2
    for l in spec["linhas"]:
        w = d.textlength(l, font=f)
        d.text(((x0 + x1) / 2 - w / 2, ty), l, font=f, fill=(0, 0, 0, 255))
        ty += lh
    img.save(destino)


camadas = []
for i, c in enumerate(R.get("caixas", [])):
    caixa(c, T / f"caixa{i}.png")
    camadas.append((T / f"caixa{i}.png", c.get("de", 0), c.get("ate", 9999)))
if R.get("titulo"):
    titulo(R["titulo"], T / "titulo.png")
    camadas.append((T / "titulo.png", R["titulo"].get("de", 0), R["titulo"].get("ate", 9999)))

# narração com atempo + alinhamento escalado/deslocado
at = R.get("atempo", 1.0)
t0 = R["narr_inicio"]
narr = T / "narr.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", T / R["narr"], "-af", f"atempo={at},aresample=48000", "-ac", "1",
                narr], check=True)
al = json.load(open(T / R["narr"].replace(".mp3", ".alinhamento.json"), encoding="utf-8"))
a2 = al.get("alignment") or al
for k in ("character_start_times_seconds", "character_end_times_seconds"):
    a2[k] = [round(t / at + t0, 3) for t in a2[k]]
json.dump(a2, open(T / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)

video = R["video"]
corte = R.get("corte_inicio", 0.0)
dv = dur(video) - corte
fim_narr = t0 + dur(narr)
total = max(dv, fim_narr + R.get("folga_fim", 0.5))
total = min(total, R.get("max_total", 999))
pad = max(0.0, total - dv)

ins = ["-ss", f"{corte:.4f}", "-i", video, "-ss", f"{corte:.4f}", "-i", R["fundo"], "-i", narr]
fc = [f"[0:v]setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration={pad:.3f}[v0]"]
for k, (png, de, ate) in enumerate(camadas):
    ins += ["-i", png]
    fc.append(f"[v{k}][{3 + k}:v]overlay=0:0:enable='between(t,{de},{ate})'[v{k + 1}]")
vk = f"v{len(camadas)}"
fc.append(f"[1:a]volume={R.get('fundo_vol', 1.0)},aresample=48000,apad[bg]")
fc.append(f"[2:a]adelay={int(t0 * 1000)}|{int(t0 * 1000)},volume=1.0,apad[nv]")
fc.append(f"[bg][nv]amix=inputs=2:duration=longest:normalize=0,atrim=0:{total:.3f}[a]")
saida = T / "corpo.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", *ins, "-filter_complex", ";".join(fc),
                "-map", f"[{vk}]", "-map", "[a]", "-t", f"{total:.3f}",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", saida], check=True)
print(f"ok {saida} | {dur(saida):.2f}s | vídeo {dv:.2f}s + congelado {pad:.2f}s | narração termina em {fim_narr:.2f}s")
