# -*- coding: utf-8 -*-
"""Base de um AD Wyze (EN -> ES LATAM), grupo A, para depois passar no montar_ad.py.
  python construir_base.py adNN/base.json
- recorta os trechos (segs) do original, aplica desfoques/caixas pretas (com caixa interpolada no tempo),
  cola a faixa opaca sobre a legenda em inglês;
- narração nova (pausas longas encurtadas) + fundo sem voz (demucs);
- ajusta a velocidade das imagens para casar com a narração (fator único, limitado a [0.75, 1.15]);
- grava alinhamento corrigido (Uáis->Wyze, números) para a legenda do kit."""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

R = json.load(open(sys.argv[1], encoding="utf-8"))
D = Path(sys.argv[1]).resolve().parent
W, H, FPS = 720, 1280, 30


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


# ---------- faixa opaca ----------
def faixa(y0, y1, grad, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(max(0, y0 - grad), min(H, y1 + grad)):
        if y < y0:
            a = int(253 * (y - (y0 - grad)) / grad)
        elif y >= y1:
            a = int(253 * ((y1 + grad) - y) / grad)
        else:
            a = 253
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img.save(destino)
    return np.array(img).astype(np.float32)


band = faixa(R["faixa"][0], R["faixa"][1], R["faixa"][2], D / "faixa.png")
band_a = band[..., 3:4] / 255.0
band_rgb = band[..., :3][..., ::-1]  # BGR


def caixa_em(op, t):
    ks = op["keys"]
    if len(ks) == 1 or t <= ks[0][0]:
        return ks[0][1:]
    if t >= ks[-1][0]:
        return ks[-1][1:]
    for a, b in zip(ks, ks[1:]):
        if a[0] <= t <= b[0]:
            f = (t - a[0]) / (b[0] - a[0])
            return [a[i] + f * (b[i] - a[i]) for i in range(1, 5)]


def aplica(fr, t):
    for op in R.get("ops", []):
        if not (op["de"] <= t <= op["ate"]):
            continue
        x0, y0, x1, y1 = [int(round(v)) for v in caixa_em(op, t)]
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
        if x1 <= x0 or y1 <= y0:
            continue
        if op["tipo"] == "preto":
            fr[y0:y1, x0:x1] = 0
        else:
            roi = fr[y0:y1, x0:x1]
            k = op.get("forca", 31) | 1
            bl = cv2.GaussianBlur(cv2.GaussianBlur(roi, (k, k), 0), (k, k), 0)
            m = np.zeros(roi.shape[:2], np.float32)
            pad = 6
            m[pad:-pad or None, pad:-pad or None] = 1
            m = cv2.GaussianBlur(m, (13, 13), 0)[..., None]
            fr[y0:y1, x0:x1] = (bl * m + roi * (1 - m)).astype(np.uint8)
    fr[:] = (band_rgb * band_a + fr.astype(np.float32) * (1 - band_a)).astype(np.uint8)
    return fr


# ---------- imagens ----------
mudo = D / "imagens.mp4"
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-threads", "4",
                       "-pix_fmt", "yuv420p", str(mudo)], stdin=subprocess.PIPE)
cap = cv2.VideoCapture(R["video"])
src_fps = cap.get(cv2.CAP_PROP_FPS)
n_out = 0
for ini, fim in R["segs"]:
    i0, i1 = int(round(ini * src_fps)), int(round(fim * src_fps))
    cap.set(cv2.CAP_PROP_POS_FRAMES, i0)
    for i in range(i0, i1):
        ok, fr = cap.read()
        if not ok:
            break
        if fr.shape[1] != W or fr.shape[0] != H:
            fr = cv2.resize(fr, (W, H), interpolation=cv2.INTER_LANCZOS4)
        ff.stdin.write(aplica(fr, i / src_fps).tobytes())
        n_out += 1
ff.stdin.close()
ff.wait()
foot = n_out / FPS

# ---------- narração: encurta pausas longas ----------
al = json.load(open(D / R["narr"].replace(".mp3", ".alinhamento.json"), encoding="utf-8"))
al = al.get("alignment") or al
C, S, E = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
wav = D / "narr_full.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(D / R["narr"]), "-ac", "1", "-ar", "48000", str(wav)], check=True)
nd = dur(wav)
# palavras
pal = []
for k, ch in enumerate(C):
    if ch.strip():
        if not pal or C[k - 1] == " ":
            pal.append([k, k])
        else:
            pal[-1][1] = k
maxg, keepg = R.get("pausa_max", 0.38), R.get("pausa_manter", 0.30)
cortes = []   # (ini, fim) de áudio removido
for a, b in zip(pal, pal[1:]):
    g0, g1 = E[a[1]], S[b[0]]
    if g1 - g0 > maxg:
        meio = (g0 + g1) / 2
        rem = (g1 - g0) - keepg
        cortes.append((meio - rem / 2, meio + rem / 2))
fim_fala = E[pal[-1][1]]
manter, t = [], 0.0
for c0, c1 in cortes:
    manter.append((t, c0))
    t = c1
manter.append((t, min(nd, fim_fala + 0.35)))


def remap(x):
    off = 0.0
    for c0, c1 in cortes:
        if x >= c1:
            off += c1 - c0
        elif x > c0:
            return c0 - off
    return x - off


t0 = R.get("narr_inicio", 0.25)
S2 = [round(remap(x) + t0, 3) for x in S]
E2 = [round(remap(x) + t0, 3) for x in E]
sel = "+".join(f"between(t,{a:.4f},{b:.4f})" for a, b in manter)
narr = D / "narr_edit.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af",
                f"aselect='{sel}',asetpts=N/SR/TB,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000", str(narr)], check=True)
narr_dur = dur(narr)

# correções de texto no alinhamento (mesmo tempo, texto novo)
txt = "".join(C)
for velho, novo in R.get("trocas", []):
    while True:
        p = txt.find(velho)
        if p < 0:
            break
        a, b = S2[p], E2[p + len(velho) - 1]
        n = len(novo)
        ns = [round(a + (b - a) * i / n, 3) for i in range(n)]
        ne = [round(a + (b - a) * (i + 1) / n, 3) for i in range(n)]
        C = C[:p] + list(novo) + C[p + len(velho):]
        S2 = S2[:p] + ns + S2[p + len(velho):]
        E2 = E2[:p] + ne + E2[p + len(velho):]
        txt = "".join(C)
json.dump({"characters": C, "character_start_times_seconds": S2, "character_end_times_seconds": E2},
          open(D / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- montagem ----------
total = t0 + narr_dur + R.get("cauda", 0.6)
fator = foot / total            # <1 = câmera lenta
fator = max(0.75, min(1.15, fator))
total = foot / fator
fundo = R["fundo"]
fd = dur(fundo)
atempo = max(0.5, min(2.0, fd / total)) if R.get("fundo_esticar", True) else 1.0
corpo = D / "corpo.mp4"
fc = (f"[0:v]setpts=PTS/{fator:.5f},fps={FPS},trim=0:{total:.3f},setpts=PTS-STARTPTS[v];"
      f"[1:a]atempo={atempo:.4f},loudnorm=I={R.get('fundo_lufs', -28)}:TP=-3:LRA=11,aresample=48000,"
      f"apad,atrim=0:{total:.3f},afade=t=out:st={total - 0.6:.3f}:d=0.6[bg];"
      f"[2:a]adelay={int(t0 * 1000)}|{int(t0 * 1000)},apad[nv];"
      f"[bg][nv]amix=inputs=2:duration=first:normalize=0,aformat=channel_layouts=stereo[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", "-i", str(mudo), "-i", fundo, "-i", str(narr),
                "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                "-threads", "4", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}",
                str(corpo)], check=True)
info = {"imagens_s": round(foot, 2), "narr_s": round(narr_dur, 2), "fator_velocidade": round(fator, 3),
        "fundo_atempo": round(atempo, 3), "total_s": round(dur(corpo), 2), "fim_fala": round(t0 + narr_dur, 2),
        "pausas_cortadas": len(cortes)}
json.dump(info, open(D / "base_info.json", "w"), indent=1)
print(info)
