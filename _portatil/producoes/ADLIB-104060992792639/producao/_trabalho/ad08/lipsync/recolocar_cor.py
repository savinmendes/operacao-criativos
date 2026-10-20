# -*- coding: utf-8 -*-
"""Correcao de cor (REVISAO-LOTE-C) do AD 08: refaz base_sem_legenda + base_lipsync NUMA GERACAO SO, a partir do ORIGINAL
(UNICOS_HD/08.mp4) e das saidas do HeyGen ja baixadas (lipsync/out = lote A, lipsync_b/out = lote B), com a leitura/gravacao
exata do ad13/lipsync3/comum3.py (ffmpeg bt601 + accurate_rnd; conversao inversa exata; etiqueta bt709/tv so no bitstream).
- Base: quadro do original + SO as areas editadas pelo LaMa (legenda, seta e brilhos), copiadas da base antiga
  (base_sem_legenda.mp4 de 2 geracoes) com a cor reajustada por quadro (ajuste afim por canal, antiga -> original, medido
  fora da mascara). Mascara = base_sem_legenda_mask.npy (legenda+seta, dilatada) + brilhos (q >= 2250, onde a antiga
  ajustada difere do original na caixa x 200-520, y 650-1050). Nenhum LaMa novo.
- Montagem = lipsync/recolocar.py (cobertura do s01, trechos s02-s16 com colar.py, clarao 286-292, crossfade 2 q nas
  emendas sem corte) + lote B (rastreado.py aplicar: f02, f14, f15 por cima, crossfade so na boca nas emendas continuas).
- Cada trecho do HeyGen leva antes de colar o desvio de cor (BGR) medido num anel de pele em volta da elipse (fora dela)
  + um ajuste interno (pele do filtro e do meio do queixo) aplicado com o peso da elipse (0 na borda, 1 no centro).
Uso (em ad08/lipsync): python recolocar_cor.py  -> ../base_sem_legenda.mp4 (2935 q) e ../base_lipsync.mp4 (2921 q), 30 fps"""
import sys, json, subprocess, numpy as np, cv2
from pathlib import Path
AQ = Path(__file__).resolve().parent; AD = AQ.parent; T = AD.parent; P = T.parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros, ENC_VF, ENC_TAG, reamostrar
ORIG = P / "UNICOS_HD" / "08.mp4"; VELHA = AD / "_antes_cor" / "base_sem_legenda.mp4"
NB, FIM = 2935, 2921
cfg = json.loads((AD / "segmentos.json").read_text()); SEGS = cfg["segmentos"]
cb = cfg["cobrir"]["s01"]; (C0, C1), (cx0, cy0, cw, ch) = cb["quadros"], cb["recorte"]
LB = json.loads((AD / "lote_b.json").read_text())["trechos"]   # f02 494-583, f14 2515-2621, f15 2622-2711
MK = np.load(AD / "base_sem_legenda_mask.npy")
BX0, BX1, BY0, BY1 = 200, 520, 650, 1050
log = []
# ---------------- base nova ----------------
def base_gen():
    corte = []; prev = None; fits = []
    for q, (o, v) in enumerate(zip(quadros(ORIG, 0, NB), quadros(VELHA, 0, NB))):
        m = np.unpackbits(MK[q])[:1280 * 720].reshape(1280, 720)
        o32 = o.astype(np.float32); v32 = v.astype(np.float32)
        M = cv2.dilate(m, np.ones((19, 19), np.uint8)) if m.any() else m
        if q >= 2250 or M.any():
            fora = cv2.dilate(M, np.ones((41, 41), np.uint8)) == 0; fora[::2] = False; fora[:, ::2] = False
            A = np.zeros((3, 2), np.float32)
            for c in range(3):
                x, y = v32[..., c][fora], o32[..., c][fora]; A[c] = np.polyfit(x, y, 1)
            vc = v32 * A[:, 0] + A[:, 1]; fits.append(A)
            if q >= 2250:
                d = np.abs(vc[BY0:BY1, BX0:BX1] - o32[BY0:BY1, BX0:BX1]).max(-1) > 12
                d = cv2.morphologyEx(d.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                if d.sum() > 30: M = M.copy(); M[BY0:BY1, BX0:BX1] |= cv2.dilate(d, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
            if M.any():
                w = np.maximum(cv2.GaussianBlur(M.astype(np.float32), (0, 0), 3), M)[..., None]
                o = np.clip(vc * w + o32 * (1 - w), 0, 255).astype(np.uint8)
        dif = 0 if prev is None else np.abs(prev.astype(np.float32) - o).mean()
        prev = o
        yield q, o, dif
    if fits:
        F = np.array(fits); log.append(f"base antiga -> original: ganho BGR {F[:, :, 0].mean(0).round(3)}, offset {F[:, :, 1].mean(0).round(2)} ({len(F)} quadros)")
# ---------------- colagem ----------------
def caixa(Tr, j):
    W = Tr["W"][j] if isinstance(Tr["W"], list) else Tr["W"]; H = Tr["H"][j] if isinstance(Tr["H"], list) else Tr["H"]
    return Tr["X0"][j], Tr["Y0"][j], W, H
def elipse(r, x0, y0, W, H):   # = colar.py / rastreado.colar_q
    fw, fh = r[2] - r[0], r[3] - r[1]; m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int((r[0]+r[2])/2), int(r[1] + 0.68*fh)), (int(0.42*fw + 6), int(0.36*fh + 8)), 0, 0, 360, 1.0, -1)
    m[:y0, :] = 0; m[y0+H:, :] = 0; m[:, :x0] = 0; m[:, x0+W:] = 0
    return cv2.GaussianBlur(m, (0, 0), max(4, fw / 25))[..., None]
def esticar(base, g, x0, y0, W, H):
    full = base.astype(np.float32).copy(); full[y0:y0+H, x0:x0+W] = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA); return full
def desvio(bases, G, Tr, rost, idx):
    """idx(k) -> quadro da saida usado no quadro k (o colar.py troca os 'ruins' pelo vizinho bom)"""
    ks = np.linspace(0, len(bases) - 1, 12).astype(int); d0s = []
    for k in ks:
        x0, y0, W, H = caixa(Tr, idx(k)); r = rost[k]; m = elipse(r, x0, y0, W, H)[..., 0]; dentro = m > 0.01; fw = r[2] - r[0]
        anel = cv2.dilate(dentro.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.5 * fw) | 1,) * 2)).astype(bool) & ~dentro
        cx = np.zeros_like(anel); cx[y0 + 2:y0 + H - 2, x0 + 2:x0 + W - 2] = True; anel &= cx
        if anel.sum() < 50: continue
        d0s.append((bases[k].astype(np.float32) - esticar(bases[k], G[idx(k)], x0, y0, W, H))[anel].mean(0))
    d0 = np.median(np.array(d0s), 0) if d0s else np.zeros(3, np.float32); dis = []
    for k in ks:
        x0, y0, W, H = caixa(Tr, idx(k)); r = rost[k]; fw, fh = r[2] - r[0], r[3] - r[1]; rr = max(3, int(0.05 * fw))
        full = esticar(bases[k], G[idx(k)], x0, y0, W, H) + d0; bb = bases[k].astype(np.float32)
        for fy in (0.655, 0.915):
            x, y = int((r[0] + r[2]) / 2), int(r[1] + fy * fh)
            if y0 <= y - rr and y + rr <= y0 + H: dis.append((bb[y-rr:y+rr, x-rr:x+rr] - full[y-rr:y+rr, x-rr:x+rr]).reshape(-1, 3).mean(0))
    d1 = np.clip(np.median(np.array(dis), 0), -8, 8) if dis else np.zeros(3, np.float32)
    return d0, d1
def colar_trecho(bases, G, Tr, ruins_ok=True):
    n = len(bases); R = np.array(Tr["rosto"], float)
    if ruins_ok:   # = colar.colador: deteccao trocada (Jesus) -> caixa interpolada, boca do quadro bom mais proximo
        cxx = (R[:, 0] + R[:, 2]) / 2; cyy = (R[:, 1] + R[:, 3]) / 2; fw = np.median(R[:, 2] - R[:, 0])
        ruins = set(np.where((np.abs(cxx - np.median(cxx)) > 0.4 * fw) | (np.abs(cyy - np.median(cyy)) > 0.4 * fw))[0].tolist())
        bons = [i for i in range(len(R)) if i not in ruins]
        R = np.array([np.interp(range(len(R)), bons, R[bons, j]) for j in range(4)]).T
        idx = lambda k: k if k not in ruins else min(bons, key=lambda b: abs(b - k))
    else: ruins = set(); idx = lambda k: k
    d0, d1 = desvio(bases, G, Tr, R, idx); out, masks = [], []
    for k in range(n):
        j = idx(k); x0, y0, W, H = caixa(Tr, j); m = elipse(R[k], x0, y0, W, H)
        full = esticar(bases[k], G[j], x0, y0, W, H) + d0 + d1 * m
        out.append(np.clip(full * m + bases[k] * (1 - m), 0, 255).astype(np.uint8))
        if k in (0, n - 1): masks.append(m)
    return out, masks, (d0, d1, sorted(ruins))
def enc(path):
    return subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
        *ENC_VF,"-threads","4","-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(path)], stdin=subprocess.PIPE)
eb, el = enc(AD / "base_sem_legenda.mp4"), enc(AD / "base_lipsync.mp4")
gen = base_gen(); DIF = {}
def ler_base(n):
    fs = []
    for _ in range(n):
        q, f, d = next(gen); DIF[q] = d; eb.stdin.write(f.tobytes()); fs.append(f)
    return fs
def w(fs):
    for f in fs: el.stdin.write(f.tobytes())
# 1) cobertura do s01 (0..285) e clarao (286..292)
cob = [cv2.resize(f[cy0:cy0+ch, cx0:cx0+cw], (720, 1280), interpolation=cv2.INTER_LANCZOS4) for f in ler_base(C1 + 1)]
w(cob[:-1]); ultimo_cob = cob[-1]; del cob
ler_base(SEGS[0]["quadro_ini"] - C1 - 1)
pend = None
for si, s in enumerate(SEGS):
    nome, a, n = s["nome"], s["quadro_ini"], s["n"]
    bases = ler_base(n)
    g = list(quadros(AQ / "out" / f"ls_{nome}.mp4")); m0 = len(g); g = reamostrar(g[:n] if s["pad"] else g, n)
    Tr = json.loads((AQ / "trilhas" / f"{nome}.json").read_text())
    out, masks, (d0, d1, ru) = colar_trecho(bases, g, Tr)
    log.append(f"{nome}: {m0}->{n} q; desvio anel {d0.round(2)} + interno {d1.round(2)}; ruins {ru}")
    # lote B por cima (rastreado.aplicar)
    for t in LB:
        q0, q1 = t["q0"], t["q1"]
        if not (a <= q0 and q1 <= a + n - 1): continue
        nb = q1 - q0 + 1; Tb = json.loads((AD / "lipsync_b" / "trilhas" / f"{t['nome']}.json").read_text())
        gb = list(quadros(AD / "lipsync_b" / "out" / f"ls_{t['nome']}.mp4")); mb = len(gb); gb = reamostrar(gb[:nb] if len(gb) > nb else gb, nb)
        ob, mk, (e0, e1, _) = colar_trecho(bases[q0 - a:q1 - a + 1], gb, Tb, ruins_ok=False)
        out[q0 - a:q1 - a + 1] = ob
        log.append(f"  lote B {t['nome']} q{q0}-{q1}: {mb}->{nb} q; desvio anel {e0.round(2)} + interno {e1.round(2)}")
        for q, M, lado in ((q0, mk[0], "ini"), (q1 + 1, mk[-1], "fim")):
            if q <= a or q > a + n - 1:   # emenda fora do trecho: e emenda de trecho (tratada abaixo) ou fim
                log.append(f"    {lado} q{q}: emenda de trecho"); continue
            if DIF[q] > 10: log.append(f"    {lado} q{q}: corte de câmera"); continue
            L, Rr = out[q - 1 - a].astype(np.float32), out[q - a].astype(np.float32)
            out[q - 1 - a] = np.clip((L * 2/3 + Rr / 3) * M + L * (1 - M), 0, 255).astype(np.uint8)
            out[q - a] = np.clip((L / 3 + Rr * 2/3) * M + Rr * (1 - M), 0, 255).astype(np.uint8)
            log.append(f"    {lado} q{q}: contínua, crossfade 2 q na boca")
    if si == 0:   # clarao refeito: fusao do ultimo quadro coberto (285) p/ o 1o com lipsync (293), luz branca
        A, B = C1, a; fr = [ultimo_cob]
        for q in range(A + 1, B):
            tt = (q - A) / (B - A); luz = np.sin(np.pi * tt) * 150
            fr.append(np.clip(ultimo_cob.astype(np.float32) * (1 - tt) + out[0].astype(np.float32) * tt + luz, 0, 255).astype(np.uint8))
        w(fr)
    else:
        corte = DIF[a] > 10
        if not corte:
            L, Rr = pend[-1].astype(np.float32), out[0].astype(np.float32)
            pend[-1] = np.clip(L * 2 / 3 + Rr / 3, 0, 255).astype(np.uint8); out[0] = np.clip(L / 3 + Rr * 2 / 3, 0, 255).astype(np.uint8)
        log.append(f"  emenda {nome} q{a}: {'corte' if corte else 'crossfade 2q'}")
        w(pend)
    pend = out; print(log[-1], flush=True)
w(pend); el.stdin.close(); el.wait()
ler_base(NB - FIM); eb.stdin.close(); eb.wait()
print("\n".join(log)); print("ok", FIM, "quadros lipsync,", NB, "base")
