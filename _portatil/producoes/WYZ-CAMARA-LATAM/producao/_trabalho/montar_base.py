# -*- coding: utf-8 -*-
"""Base de um AD Wyze (EN -> ES LATAM), Grupo A:
- faixa opaca (alpha 252) sobre a legenda em inglês + caixa de título em espanhol;
- fundo sem voz (demucs) + narração nova, frase a frase, posicionada no tempo das cenas;
- estende o fim com quadro congelado se a fala passar do vídeo; corta o fim se sobrar;
- gera alinhamento.json deslocado para a legenda do kit.
  python montar_base.py adNN/base.json"""
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
FB = str(KIT / "fonts" / "Poppins-Bold.ttf")
EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"
W, H = 720, 1280
cfg_path = Path(sys.argv[1]).resolve()
R = json.load(open(cfg_path, encoding="utf-8"))
T = cfg_path.parent


def run(cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def eh_emoji(ch):
    return ord(ch) > 0x2000 and ch not in "…–—“”‘’¡¿"


def caixa_titulo(spec, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FB, spec["px"])
    fe = ImageFont.truetype(EMOJI, spec["px"])
    larg = lambda s: sum(d.textlength(c, font=fe if eh_emoji(c) else f) for c in s)  # noqa: E731
    lh = int(spec["px"] * 1.3)
    ws = [larg(l) for l in spec["linhas"]]
    bw = max(max(ws) + 48, spec.get("cobrir_w", 0))
    bh = max(lh * len(spec["linhas"]) + 30, spec.get("cobrir_h", 0))
    cx, cy = W // 2, spec["cy"]
    x0, y0 = cx - bw / 2, cy - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=18, fill=(255, 255, 255, 255))
    ty = cy - lh * len(spec["linhas"]) / 2 + 2
    for l, w in zip(spec["linhas"], ws):
        x = cx - w / 2
        for c in l:
            if eh_emoji(c):
                d.text((x, ty + int(spec["px"] * 0.05)), c, font=fe, embedded_color=True)
                x += d.textlength(c, font=fe)
            else:
                d.text((x, ty), c, font=f, fill=(0, 0, 0, 255))
                x += d.textlength(c, font=f)
        ty += lh
    img.save(destino)


def faixa(y0, y1, destino, g=18):
    """Faixa preta quase opaca (alpha 252) de y0 a y1, com borda suave de g px fora dela."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(max(0, y0 - g), min(H, y1 + g)):
        if y0 <= y < y1:
            a = 252
        elif y < y0:
            a = int(252 * (y - (y0 - g)) / g)
        else:
            a = int(252 * ((y1 + g) - y) / g)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img.save(destino)


# ---- narração frase a frase ----
al = json.load(open(T / R["narr"].replace(".mp3", ".alinhamento.json"), encoding="utf-8"))
al = al.get("alignment") or al
ch, cs, ce = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
txt = "".join(ch)
frases = []
for m in re.finditer(r"[^.!?]+[.!?]?", txt):
    if not m.group().strip():
        continue
    a, b = m.start(), m.end() - 1
    while txt[a] in " \n":
        a += 1
    while txt[b] in " .!?\n" and b > a:
        b -= 1
    frases.append((a, m.end(), cs[a], ce[b]))
offs = R["offsets"]
assert len(offs) == len(frases), f"{len(frases)} frases x {len(offs)} offsets"
novo_s, novo_e = list(cs), list(ce)
for (a, b, s, e), o in zip(frases, offs):
    for i in range(a, b):
        novo_s[i] = round(cs[i] - s + o, 3)
        novo_e[i] = round(ce[i] - s + o, 3)
# caracteres fora de frases (quebras de linha) herdam o tempo do anterior
json.dump({"characters": ch, "character_start_times_seconds": novo_s, "character_end_times_seconds": novo_e},
          open(T / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)
fim_fala = max(e - s + o for (_, _, s, e), o in zip(frases, offs))
total = R.get("total") or round(fim_fala + R.get("cauda", 1.0), 2)

# ---- overlays ----
faixa(*R["faixa"], T / "faixa.png")
camadas = [(T / "faixa.png", 0, 9999)]
if R.get("titulo"):
    caixa_titulo(R["titulo"], T / "titulo.png")
    camadas.append((T / "titulo.png", 0, R["titulo"]["ate"]))

# ---- render ----
cortes = R.get("cortes") or [[0, dur(R["video"])]]
vdur = sum(b - a for a, b in cortes)
ext = max(0.0, total - vdur + 0.05)
ins = ["-i", R["video"], "-i", R["fundo"], "-i", T / R["narr"]]
fc = []
for k, (a, b) in enumerate(cortes):
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[c{k}]")
    fc.append(f"[1:a]aresample=48000,atrim={a}:{b},asetpts=PTS-STARTPTS[f{k}]")
fc.append("".join(f"[c{k}][f{k}]" for k in range(len(cortes))) + f"concat=n={len(cortes)}:v=1:a=1[vcat][fcat]")
ult = "[vcat]"
for k, dz in enumerate(R.get("desfocar", [])):   # {"de","ate","caixa":[x0,y0,x1,y1]} no tempo já cortado
    x0, y0, x1, y1 = dz["caixa"]
    fc.append(f"{ult}split[db{k}][dc{k}]")
    fc.append(f"[dc{k}]crop={x1 - x0}:{y1 - y0}:{x0}:{y0},gblur=sigma=14:steps=3[dr{k}]")
    fc.append(f"[db{k}][dr{k}]overlay={x0}:{y0}:enable='between(t,{dz['de']},{dz['ate']})'[dz{k}]")
    ult = f"[dz{k}]"
fc.append(f"{ult}tpad=stop_mode=clone:stop_duration={ext:.3f},trim=0:{total:.3f},setpts=PTS-STARTPTS[v0]")
for k, (png, de, ate) in enumerate(camadas):
    ins += ["-i", png]
    fc.append(f"[v{k}][{3 + k}:v]overlay=0:0:enable='between(t,{de},{ate})'[v{k + 1}]")
vk = f"v{len(camadas)}"
fc.append(f"[fcat]apad,atrim=0:{total:.3f},volume={R.get('fundo_vol', 1.0)},"
          f"afade=t=out:st={total - 0.35:.3f}:d=0.35[bg]")
partes = []
for k, ((a, b, s, e), o) in enumerate(zip(frases, offs)):
    ini = max(0.0, s - 0.04)
    d_ms = int(max(0.0, o - (s - ini)) * 1000)
    fc.append(f"[2:a]atrim={ini:.3f}:{e + 0.15:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
              f"afade=t=out:st={e + 0.10 - ini:.3f}:d=0.05,adelay={d_ms}|{d_ms}[n{k}]")
    partes.append(f"[n{k}]")
fc.append("".join(partes) + f"amix=inputs={len(partes)}:normalize=0:duration=longest[nv]")
fc.append("[bg][nv]amix=inputs=2:duration=first:normalize=0[a]")
saida = T / "corpo.mp4"
run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", f"[{vk}]", "-map", "[a]",
     "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p", "-r", "30",
     "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", saida])
print(f"ok {saida} | {dur(saida):.2f}s | fala termina em {fim_fala:.2f}s | vídeo original {vdur:.2f}s "
      f"(congelado no fim: {max(0, total - vdur):.2f}s)")
for (a, b, s, e), o in zip(frases, offs):
    print(f"  {o:6.2f}-{e - s + o:6.2f}  {txt[a:b]}")
