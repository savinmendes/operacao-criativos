# -*- coding: utf-8 -*-
"""Grimório V2 + colar: insere a frase nova após "São Bento" (2:05,73), foto do colar, print segurado,
legenda nova no estilo original (Open Sans 53, branca, sombra) e selo VÍDEO FICTÍCIO. Original intocado."""
import json, subprocess, numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
AQ = Path(__file__).resolve().parent
ORIG = AQ.parent.parent / "GRIMORIO V2.mp4"
SAIDA = AQ.parent.parent / "GRIMORIO V2 - COLAR (VIDEO FICTICIO).mp4"
FPS = 30
FA = 3772            # 1º quadro removido do padre (A = 125,7333 s; silêncio entre "Bento" e "disponível")
FP = 3779            # 1º quadro do print do perfil (corte original)
NCOL, NHOLD = 74, 34 # colar 2,467 s + print segurado 1,133 s  (= 108 quadros no lugar de 7)
A = FA / FPS
S = (NCOL + NHOLD - (FP - FA)) / FPS   # 101 quadros = 3,3667 s de atraso
PRE = 0.10
G = AQ / "graficos"; G.mkdir(exist_ok=True)

# ---------------- áudio ----------------
sr = 44100
mix, _ = librosa.load(AQ / "audio_orig.wav", sr=sr, mono=False)
nov, _ = librosa.load(AQ / "demucs/htdemucs/audio_orig/no_vocals.wav", sr=sr, mono=False)
voc, _ = librosa.load(AQ / "demucs/htdemucs/audio_orig/vocals.wav", sr=sr, mono=True)
ins, _ = librosa.load(AQ / "tts/ins3.mp3", sr=sr, mono=True)
ins = ins[: int(3.08 * sr)]
fo = int(0.03 * sr); ins[-fo:] *= np.linspace(1, 0, fo); ins[: int(0.004 * sr)] *= np.linspace(0, 1, int(0.004 * sr))
med = pyln.Meter(sr)
l_ref = med.integrated_loudness(voc[int(100 * sr): int(133 * sr)])
l_ins = med.integrated_loudness(ins)
ins = ins * 10 ** ((l_ref - l_ins) / 20)
print(f"LUFS voz original {l_ref:.1f} | frase nova {l_ins:.1f} -> ajustada {med.integrated_loudness(ins):.1f}")
iA, nS = int(round(A * sr)), int(round(S * sr))
X = nov[:, iA: iA + nS].copy()
v = np.zeros(nS); p = int(PRE * sr); v[p: p + len(ins)] = ins
X += v[None, :]
# costuras: 20 ms na entrada, 60 ms na saída (sai já na mistura original de A-60ms..A)
c1 = int(0.02 * sr); w = np.linspace(0, 1, c1)
X[:, :c1] = mix[:, iA: iA + c1] * (1 - w) + X[:, :c1] * w
c2 = int(0.06 * sr); w = np.sin(np.linspace(0, np.pi / 2, c2)) ** 2
X[:, -c2:] = X[:, -c2:] * (1 - w) + mix[:, iA - c2: iA] * w
out = np.concatenate([mix[:, :iA], X, mix[:, iA:]], axis=1)
sf.write(AQ / "audio_novo.wav", out.T, sr, subtype="PCM_16")
print("áudio", out.shape[1] / sr, "s; pico", np.abs(out).max())

# ---------------- gráficos ----------------
prt = Image.open(AQ / "q/print_f3779.png").convert("RGB")
prod = Image.open(AQ / "colar/img2.jpg").convert("RGB")
(G / "colar").mkdir(exist_ok=True)
for i in range(NCOL):
    z = 1.0 + 0.05 * i / (NCOL - 1)
    s = int(round(720 * z)); im = Image.new("RGB", (720, 1280), (0, 0, 0))
    pr = prod.resize((s, s), Image.LANCZOS); im.paste(pr, ((720 - s) // 2, 470 - s // 2))
    im.paste(ImageChops.lighter(im.crop((0, 0, 720, 148)), prt.crop((0, 0, 720, 148))), (0, 0))
    im.save(G / "colar" / f"c{i:03d}.png")
f = ImageFont.truetype(str(AQ / "fonts/OpenSans.ttf"), 53); f.set_variation_by_name("Regular")
CHUNKS = [("junto com o colar", 0.0, 1.157), ("da medalha de", 1.157, 1.90), ("São Bento", 1.90, 2.465), ("de presente", 2.465, S)]
for k, (t, a, b) in enumerate(CHUNKS):
    sh = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.text((361, 821), t, font=f, anchor="ms", fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(2.2))
    d = ImageDraw.Draw(sh); d.text((360, 819), t, font=f, anchor="ms", fill=(255, 255, 255, 255))
    sh.save(G / f"leg{k}.png")
json.dump({"A": A, "S": S, "chunks": CHUNKS}, open(AQ / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------- vídeo ----------------
IN709 = "scale=in_color_matrix=bt709:in_range=full:out_range=full:flags=accurate_rnd+full_chroma_int+bitexact,format=gbrp"
fc = [f"[0:v]split=3[a][b][c]",
      f"[a]trim=end_frame={FA},setpts=PTS-STARTPTS,{IN709}[v1]",
      f"[1:v]fps={FPS},setpts=PTS-STARTPTS,format=gbrp[v2]",
      f"[b]trim=start_frame={FP}:end_frame={FP+1},setpts=PTS-STARTPTS,loop={NHOLD-1}:1:0,setpts=N/{FPS}/TB,{IN709}[v3]",
      f"[c]trim=start_frame={FP},setpts=PTS-STARTPTS,{IN709}[v4]",
      f"[v1][v2][v3][v4]concat=n=4:v=1:a=0[cat]"]
last = "cat"
for k, (t, a, b) in enumerate(CHUNKS):
    fc.append(f"[{3+k}:v]format=gbrap[l{k}]")
    fc.append(f"[{last}][l{k}]overlay=0:0:format=gbrp:shortest=1:enable='between(t,{A+a:.4f},{A+b-0.001:.4f})'[o{k}]"); last = f"o{k}"
fc.append(f"[2:v]format=gbrap[selo]")
fc.append(f"[{last}][selo]overlay=0:0:format=gbrp:shortest=1,scale=in_range=full:out_color_matrix=bt709:out_range=full:flags=accurate_rnd+full_chroma_int+bitexact,format=yuvj420p[vout]")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(ORIG), "-framerate", str(FPS), "-i", str(G / "colar/c%03d.png"),
       "-loop", "1", "-t", "170", "-i", str(G / "selo_ficticio_mini_pt.png")]
for k in range(len(CHUNKS)): cmd += ["-loop", "1", "-t", "170", "-i", str(G / f"leg{k}.png")]
cmd += ["-i", str(AQ / "audio_novo.wav"), "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", f"{3+len(CHUNKS)}:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuvj420p",
        "-color_range", "pc", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-r", str(FPS), "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-movflags", "+faststart", str(SAIDA)]
# -shortest com entradas em loop: limita pelo áudio; o vídeo acaba antes (154,83+S) -> ver abaixo
subprocess.run(cmd, check=True)
print("ok", SAIDA)
