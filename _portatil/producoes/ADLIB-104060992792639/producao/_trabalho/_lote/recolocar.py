# -*- coding: utf-8 -*-
"""Recoloca as saidas do HeyGen na base limpa (so a regiao boca/rosto, elipse suave 'cola' = [cx,cy,ax,ay]).
Uso (na pasta adNN): python recolocar.py lipsync/segs.json
- saida de cada trecho: lipsync/out/ls_<nome>.mp4 (ou seg["arquivo"]); se seg["cobrir"] existir o trecho nao e colado.
- descarta o 1o quadro da saida se ele nao bater com a entrada (quadro de outra tomada);
- reamostra no tempo p/ o numero exato de quadros (interpolacao, sem congelar);
- emendas sem corte de camera: crossfade de 3 quadros (so na regiao colada);
- gera base_lipsync.mp4 (bt709/tv) e, por trecho, lipsync/chk/full_<nome>.mp4 (com o ES) e orig_<nome>.mp4 (original + PT)."""
import sys, json, subprocess, cv2, numpy as np
from pathlib import Path
cfg = json.load(open(sys.argv[1], encoding="utf-8")); segs = cfg["segs"]
CHK = Path("lipsync/chk"); CHK.mkdir(parents=True, exist_ok=True)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
def ler(p):
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr
def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / (n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[-1] if j >= m - 1 else (fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0)))
    return out
def cola_em(c, k):
    """cola fixa [cx,cy,ax,ay], None (quadro inteiro) ou chaves [[k,cx,cy,ax,ay],...] interpoladas (k relativo ao trecho)"""
    if c is None or not isinstance(c[0], (list, tuple)): return c
    K = np.array(c, float); return [int(round(np.interp(k, K[:, 0], K[:, j]))) for j in range(1, 5)]
def mascara(c):
    if c is None: return np.ones((1280, 720, 1), np.float32)
    cx, cy, ax, ay = c; m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (cx, cy), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(4, ax * 0.12))[..., None]
def enc(path, fps=30):
    return subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(fps),"-i","-",
        "-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(path)], stdin=subprocess.PIPE)
base = ler(cfg["base"]); N = len(base); out = [f.copy() for f in base]; log = []
for s in segs:
    if s.get("cobrir"): log.append(f"{s['nome']}: coberto, nao colado"); continue
    q0, q1 = s["q0"], s["q1"]; n = q1 - q0 + 1
    p = Path(s.get("arquivo", f"lipsync/out/ls_{s['nome']}.mp4")); g = ler(p)
    entrada = ler(f"lipsync/in/pt_{s['nome']}.mp4")
    d0 = np.abs(cv2.resize(g[0], (180, 320)).astype(np.float32) - cv2.resize(entrada[0], (180, 320))).mean()
    d1 = np.abs(cv2.resize(g[1], (180, 320)).astype(np.float32) - cv2.resize(entrada[1], (180, 320))).mean()
    drop = d0 > 3 * max(d1, 1.5)
    if drop: g = g[1:]
    info = f"{s['nome']}: saida {len(g) + drop} q (entrada {len(entrada)}, esperado {n}){' 1o quadro descartado' if drop else ''} d0={d0:.1f} d1={d1:.1f}"
    g = reamostrar(g, n); fixa = s["cola"] is None or not isinstance(s["cola"][0], (list, tuple)); M = mascara(cola_em(s["cola"], 0))
    for k in range(n):
        if not fixa: M = mascara(cola_em(s["cola"], k))
        gg = g[k]
        if s.get("crop"):
            x, y, w, h = s["crop"]; full = base[q0 + k].copy()
            full[y:y+h, x:x+w] = cv2.resize(gg, (w, h), interpolation=cv2.INTER_AREA); gg = full
        elif gg.shape[:2] != (1280, 720): gg = cv2.resize(gg, (720, 1280), interpolation=cv2.INTER_LANCZOS4)
        out[q0 + k] = np.clip(gg * M + base[q0 + k] * (1 - M), 0, 255).astype(np.uint8)
    log.append(info)
# crossfade nas emendas continuas
for a, b in zip(segs, segs[1:]):
    if a.get("cobrir") or b.get("cobrir") or a["q1"] + 1 != b["q0"]: continue
    q = b["q0"]; corte = np.abs(base[q - 1].astype(np.float32) - base[q]).mean() > 10
    if corte: log.append(f"emenda q{q}: corte de camera"); continue
    M = np.maximum(mascara(cola_em(a["cola"], a["q1"] - a["q0"])), mascara(cola_em(b["cola"], 0)))
    L = [out[q - 2].astype(np.float32), out[q - 1].astype(np.float32)]; R = [out[q].astype(np.float32), out[q + 1].astype(np.float32)]
    # rampa: q-2 (3/4 A), q-1 (1/2), q (1/4 A)... boca A -> boca B
    mix = lambda A, B, w: np.clip((A * w + B * (1 - w)) * M + A * (1 - M), 0, 255).astype(np.uint8)
    out[q - 1] = mix(L[1], R[0], 0.6); out[q] = mix(R[0], L[1], 0.6)
    log.append(f"emenda q{q}: continua, crossfade na boca")
e = enc("base_lipsync.mp4")
for f in out: e.stdin.write(f.tobytes())
e.stdin.close(); e.wait()
orig = cfg["orig"]
for s in segs:
    if s.get("cobrir"): continue
    q0, q1 = s["q0"], s["q1"]; t0, t1 = q0 / 30, (q1 + 1) / 30
    tmp = CHK / f"_v_{s['nome']}.mp4"; e = enc(tmp)
    for f in out[q0:q1 + 1]: e.stdin.write(f.tobytes())
    e.stdin.close(); e.wait()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",cfg["narr"],"-filter_complex",f"[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]",
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac",str(CHK / f"full_{s['nome']}.mp4")],check=True); tmp.unlink()
    # "original" p/ o checar = base limpa (mesma cor/legenda removida) com o audio PT original
    subprocess.run(["ffmpeg","-v","error","-y","-i",cfg["base"],"-i",orig,"-filter_complex",
        r"[0:v]select='between(n\,%d\,%d)',setpts=N/30/TB[v];" % (q0, q1) + f"[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]",
        "-map","[v]","-map","[a]","-r","30","-c:v","libx264","-crf","16","-c:a","aac",str(CHK / f"orig_{s['nome']}.mp4")],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",cfg["narr"],"-af",f"atrim={t0}:{t1},asetpts=PTS-STARTPTS","-ac","1","-c:a","libmp3lame","-b:a","192k",str(CHK / f"es_{s['nome']}.mp3")],check=True)
print("\n".join(log)); print("ok", N, "quadros")
