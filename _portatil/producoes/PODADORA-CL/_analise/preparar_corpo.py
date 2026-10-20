# -*- coding: utf-8 -*-
"""Prepara a base de um AD da podadora (EN -> ES Chile):
- corta o início (quadros de capa), queima a caixa de gancho em espanhol e a faixa do aviso em espanhol;
- troca o áudio: fundo sem voz (demucs) + narração nova (voz clonada), com atempo opcional;
- gera o alinhamento deslocado/escalado para a legenda do kit.
  python preparar_corpo.py receita.json"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
FB = str(KIT / "fonts" / "Poppins-Bold.ttf")
FM = str(KIT / "fonts" / "Poppins-Medium.ttf")
EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"
W, H = 720, 1280
R = json.load(open(sys.argv[1], encoding="utf-8"))
P = Path(sys.argv[1]).resolve().parent.parent
T = P / "_trabalho" / R["id"]
T.mkdir(parents=True, exist_ok=True)


def texto_com_emoji(d, xy, txt, font, fill, emoji_px):
    """Desenha texto; caracteres fora do BMP básico (emoji) com a fonte Segoe UI Emoji colorida."""
    x, y = xy
    fe = ImageFont.truetype(EMOJI, emoji_px)
    for ch in txt:
        if ord(ch) > 0x2000 and ch not in "…–—“”‘’¡¿":
            d.text((x, y + int(font.size * 0.05)), ch, font=fe, embedded_color=True)
            x += d.textlength(ch, font=fe)
        else:
            d.text((x, y), ch, font=font, fill=fill)
            x += d.textlength(ch, font=font)


def largura(d, txt, font, emoji_px):
    fe = ImageFont.truetype(EMOJI, emoji_px)
    return sum(d.textlength(ch, font=fe if ord(ch) > 0x2000 and ch not in "…–—“”‘’¡¿" else font) for ch in txt)


def caixa_gancho(spec, destino):
    """Caixa branca arredondada (estilo TikTok) cobrindo a caixa original inteira, texto preto."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FB if spec.get("negrito", True) else FM, spec["px"])
    linhas = spec["linhas"]
    lh = int(spec["px"] * 1.3)
    ws = [largura(d, l, f, spec["px"]) for l in linhas]
    cx = W // 2
    bw = max(max(ws) + 44, spec.get("cobrir_w", 0))
    bh = max(lh * len(linhas) + 26, spec.get("cobrir_h", 0))
    cy = spec["cy"]
    x0, y0 = cx - bw / 2, cy - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=16, fill=(255, 255, 255, 255))
    ty = cy - lh * len(linhas) / 2 + 4
    for l, w in zip(linhas, ws):
        texto_com_emoji(d, (cx - w / 2, ty), l, f, (0, 0, 0, 255), spec["px"])
        ty += lh
    img.save(destino)


def faixa_aviso(linhas, destino, topo=1150):
    """Faixa escura no rodapé cobrindo o aviso em inglês, com o aviso em espanhol (texto pequeno)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    g = 40
    for y in range(topo - g, H):
        a = 252 if y >= topo else int(252 * (y - (topo - g)) / g)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    f = ImageFont.truetype(FM, 19)
    lh = 25
    y = topo + (H - topo - lh * len(linhas)) / 2
    for l in linhas:
        w = d.textlength(l, font=f)
        d.text(((W - w) / 2, y), l, font=f, fill=(235, 235, 235, 255))
        y += lh
    img.save(destino)


# overlays
faixa_aviso(R["aviso"], T / "faixa.png", R.get("faixa_topo", 1150))
camadas = [(T / "faixa.png", 0, 9999)]
if R.get("gancho"):
    caixa_gancho(R["gancho"], T / "gancho.png")
    camadas.append((T / "gancho.png", R["gancho"]["de"], R["gancho"]["ate"]))

# narração com atempo + alinhamento escalado/deslocado
at = R.get("atempo", 1.0)
t0 = R["narr_inicio"]
narr = T / "narr.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", P / "_analise" / R["narr"], "-af",
                f"atempo={at},aresample=48000", "-ac", "1", narr], check=True)
al = json.load(open(P / "_analise" / R["narr"].replace(".mp3", ".alinhamento.json"), encoding="utf-8"))
a2 = al.get("alignment") or al
for k in ("character_start_times_seconds", "character_end_times_seconds"):
    a2[k] = [round(t / at + t0, 3) for t in a2[k]]
json.dump(a2, open(T / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)

# render da base
corte = R.get("corte_inicio", 0.0)
ins = ["-ss", f"{corte:.4f}", "-i", P / R["video"],
       "-ss", f"{corte:.4f}", "-i", P / "_audio" / "sep" / "htdemucs" / R["fundo"] / "no_vocals.wav",
       "-i", narr]
fc = ["[0:v]setpts=PTS-STARTPTS[v0]"]
for k, (png, de, ate) in enumerate(camadas):
    ins += ["-i", png]
    fc.append(f"[v{k}][{3 + k}:v]overlay=0:0:enable='between(t,{de},{ate})'[v{k + 1}]")
vk = f"v{len(camadas)}"
fc.append(f"[1:a]volume={R.get('fundo_vol', 2.0)},aresample=48000[bg]")
fc.append(f"[2:a]adelay={int(t0 * 1000)}|{int(t0 * 1000)},volume=1.0[nv]")
fc.append("[bg][nv]amix=inputs=2:duration=first:normalize=0[a]")
saida = T / "corpo.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", f"[{vk}]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-shortest", saida], check=True)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", saida],
                         capture_output=True, text=True).stdout)
fim_narr = t0 + float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                      narr], capture_output=True, text=True).stdout)
print(f"ok {saida} | {d:.2f}s | narração termina em {fim_narr:.2f}s")
