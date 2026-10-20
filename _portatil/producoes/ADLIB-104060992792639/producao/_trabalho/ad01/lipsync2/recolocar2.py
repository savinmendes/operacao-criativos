# -*- coding: utf-8 -*-
"""Recoloca os trechos na base limpa, sem congelar quadros:
- trechos refeitos (plano.json: lista de partes recortadas, cada uma com quadros esperados) -> colar.colar (so a boca/rosto);
- trechos mantidos -> ../lipsync/ls_sNN.mp4 como no recolocar.py antigo (parte de cima, transicao y 760-800);
- toda saida e reamostrada no tempo para o numero exato de quadros (interpolacao, nao repete o ultimo);
- emendas entre trechos SEM corte de camera: crossfade de 2 quadros (ultimo de A e primeiro de B).
Saida: ../base_lipsync.mp4 (a antiga fica como ../base_lipsync_v1.mp4)."""
import json, subprocess, cv2, numpy as np
from pathlib import Path
import colar as C, fechar as Fe
AQ = Path(__file__).parent; AD = AQ.parent
seg = json.loads((AD / "segmentos.json").read_text())["segmentos"]
plano = json.loads((AQ / "plano.json").read_text())   # {"s05": [["out/ls_s05.mp4", 350], ...], ...}
w = np.zeros((1280, 1, 1), np.float32); w[800:] = 1; w[760:800, 0, 0] = np.linspace(0, 1, 40)
base = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4"))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
def quadros_seg(s, bases):
    n = s["quadro_fim"] - s["quadro_ini"] + 1
    if s["nome"] in plano and not s["nome"].startswith("_"):
        gs = []
        for p, k in plano[s["nome"]]: gs += C.reamostrar(C.ler(AQ / p), k)
        assert len(gs) == n, (s["nome"], len(gs), n)
        return [C.colar(b, g) for b, g in zip(bases, gs)], "novo"
    gs = C.reamostrar(C.ler(AD / "lipsync" / f"ls_{s['nome']}.mp4"), n)
    out = []
    for b, g in zip(bases, gs):
        if g.shape != b.shape: g = cv2.resize(g, (720, 1280), interpolation=cv2.INTER_LANCZOS4)
        out.append(np.clip(g * (1 - w) + b * w, 0, 255).astype(np.uint8))
    return out, "antigo"
i = 0; prev = None; log = []
for s in seg:
    a, b = s["quadro_ini"], s["quadro_fim"]
    if i < a and prev is not None:
        for f in prev[0]: ff.stdin.write(f.tobytes())
        prev = None
    while i < a:
        ok, f = base.read(); ff.stdin.write(f.tobytes()); i += 1
    bases = []
    for _ in range(a, b + 1):
        ok, f = base.read(); bases.append(f); i += 1
    fr, tipo = quadros_seg(s, bases)
    if s["nome"] in plano.get("_fechar", []):
        lg = []; fr = Fe.fechar(fr, a, lg); tipo += " +fechar " + "; ".join(lg)
    if prev is not None:
        corte = np.abs(prev[1].astype(np.float32) - bases[0]).mean() > 10   # base: ultimo de A x primeiro de B
        if not corte and prev[2] == a - 1:
            L, R = prev[0][-1].astype(np.float32), fr[0].astype(np.float32)
            prev[0][-1] = np.clip(L * 2 / 3 + R / 3, 0, 255).astype(np.uint8)
            fr[0] = np.clip(L / 3 + R * 2 / 3, 0, 255).astype(np.uint8)
        log.append(f"{s['nome']} q{a}: {'corte' if corte else 'crossfade 2q'}")
        for f in prev[0]: ff.stdin.write(f.tobytes())

    prev = (fr, bases[-1], b); print(s["nome"], tipo, len(fr), flush=True)
if prev is not None:
    for f in prev[0]: ff.stdin.write(f.tobytes())
while True:
    ok, f = base.read()
    if not ok: break
    ff.stdin.write(f.tobytes()); i += 1
ff.stdin.close(); ff.wait()
print("\n".join(log)); print("ok quadros", i)
