# -*- coding: utf-8 -*-
"""AD 08: monta ../base_lipsync.mp4 (30 fps, bt709/tv) a partir da base sem legenda/seta:
- quadros 0-285 (cena das serpentes, rosto de perfil pequeno): cobertos com o recorte (110,560,380,676) = mãos e serpentes,
  sem nenhum rosto (o HeyGen não pega perfil e a boca falaria PT);
- trechos s02-s16: saída do HeyGen reamostrada p/ o nº exato de quadros e colada só na boca/queixo (colar.py);
- clarão 286-292 refeito como fusão 285->293 com luz branca (tira legenda PT lavada e boca PT);
- emendas sem corte de câmera: crossfade de 2 quadros; até o quadro FIM."""
import json, subprocess, sys, cv2, numpy as np
from pathlib import Path
import colar as C
import fechar as Fe
FECHAR = set()   # testado no s02: o fechar.py deixou o queixo borrado (fantasma) na pausa de 18,2 s -> não usado
AQ = Path(__file__).parent; AD = AQ.parent
cfg = json.loads((AD / "segmentos.json").read_text()); segs = cfg["segmentos"]
plano = json.loads((AQ / "plano.json").read_text()) if (AQ / "plano.json").exists() else {}
FIM = int(sys.argv[1])
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
base = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4"))
ob = [base.read()[1] for _ in range(FIM)]; todos = [f.copy() for f in ob]
cb = cfg["cobrir"]["s01"]; (q0, q1), (x, y, w, h) = cb["quadros"], cb["recorte"]
for q in range(q0, q1 + 1): todos[q] = cv2.resize(ob[q][y:y+h, x:x+w], (720, 1280), interpolation=cv2.INTER_LANCZOS4)
for s in segs:
    nome, a, n = s["nome"], s["quadro_ini"], s["n"]
    g = C.ler(AQ / plano.get(nome, f"out/ls_{nome}.mp4")); g = C.reamostrar(g[:n] if s["pad"] else g, n)
    col = C.colador(nome)
    for k in range(n):
        if a + k < FIM: todos[a + k] = col(todos[a + k], g, k)
    if nome in FECHAR:
        lg = []; tr = Fe.fechar([todos[a + k] for k in range(n)], a, lg)
        for k in range(n): todos[a + k] = tr[k]
        print("  fechar:", lg)
    print(nome, len(g), "quadros com rosto trocado (boca do vizinho):", sorted(C.colar.ruins), flush=True)
# clarão de transição (quadros 286-292): no original tem legenda PT lavada e a boca dela já falando PT.
# Refeito como fusão do último quadro coberto (285) para o 1º quadro com lipsync (293), com o mesmo clarão branco.
A, B = q1, segs[0]["quadro_ini"]
for q in range(A + 1, B):
    t = (q - A) / (B - A); luz = np.sin(np.pi * t) * 150
    todos[q] = np.clip(todos[A].astype(np.float32) * (1 - t) + todos[B].astype(np.float32) * t + luz, 0, 255).astype(np.uint8)
log = []
for s in segs[1:]:
    a = s["quadro_ini"]
    if a >= FIM or a == 0: continue
    corte = np.abs(ob[a - 1].astype(np.float32) - ob[a]).mean() > 10
    if not corte:
        L, R = todos[a - 1].astype(np.float32), todos[a].astype(np.float32)
        todos[a - 1] = np.clip(L * 2 / 3 + R / 3, 0, 255).astype(np.uint8); todos[a] = np.clip(L / 3 + R * 2 / 3, 0, 255).astype(np.uint8)
    log.append(f"{s['nome']} q{a}: {'corte' if corte else 'crossfade 2q'}")
for f in todos: ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait(); print("\n".join(log)); print("ok", len(todos))
