# -*- coding: utf-8 -*-
"""Correcao de cor (REVISAO-LOTE-C) do AD 07: refaz base_sem_legenda + base_lipsync NUMA GERACAO SO, a partir do ORIGINAL
(UNICOS_HD/07.mp4) e das saidas do HeyGen ja baixadas (lipsync/out/ls_sNN.mp4; o s08 = ls_s08g, mesmo arquivo), com a
leitura/gravacao exata do ad13/lipsync3/comum3.py (ffmpeg bt601 + accurate_rnd; conversao inversa exata; etiqueta
bt709/tv so no bitstream).
- Base: quadro do original + SO a area editada pelo LaMa (legenda PT), copiada da base antiga (_antes_cor/base_sem_legenda,
  1 geracao) com a cor reajustada por quadro (afim por canal antiga -> original, medido fora da mascara, faixa y 700-1100).
  Mascara = base_sem_legenda_mask.npy dilatada 19 px. Nenhum LaMa novo.
- Montagem = lipsync/recolocar.py: mesma caixa (segmentos.json), mesma elipse e canto do Jesus (colar.mascara), mesma
  reamostragem (colar.reamostrar), quadros 0-3 = 1o quadro colado do s01, crossfade de 2 q nas emendas sem corte de camera
  (dif. media da base > 10 = corte), ate o quadro 2147.
- Cada trecho do HeyGen leva antes de colar: desvio BGR (mediana) num anel de pele em volta da elipse (fora dela, dentro da
  caixa, fora do canto do Jesus) + ajuste interno (mediana dentro do miolo da elipse) aplicado com o peso da elipse.
Uso (em ad07/lipsync): python recolocar_cor.py  -> ../base_sem_legenda.mp4 (2170 q) e ../base_lipsync.mp4 (2147 q), 24 fps"""
import sys, json, subprocess, numpy as np, cv2
from pathlib import Path
AQ = Path(__file__).resolve().parent; AD = AQ.parent; T = AD.parent; P = T.parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3")); sys.path.insert(0, str(AQ))
from comum3 import quadros, ENC_VF, ENC_TAG
import colar as C
ORIG = P / "UNICOS_HD" / "07.mp4"; VELHA = AD / "_antes_cor" / "base_sem_legenda.mp4"
NB, FIM = 2170, 2147
SEGS = json.loads((AD / "segmentos.json").read_text())["segmentos"]
CANTO = {"s01": None}
MK = np.load(AD / "base_sem_legenda_mask.npy")
FY0, FY1 = 700, 1100
log = []
def base_gen():
    fits = []
    for q, (o, v) in enumerate(zip(quadros(ORIG, 0, NB), quadros(VELHA, 0, NB))):
        m = np.unpackbits(MK[q])[:1280 * 720].reshape(1280, 720)
        if m.any():
            M = cv2.dilate(m, np.ones((19, 19), np.uint8))
            o32 = o[FY0:FY1].astype(np.float32); v32 = v[FY0:FY1].astype(np.float32); Mb = M[FY0:FY1]
            fora = cv2.dilate(Mb, np.ones((41, 41), np.uint8)) == 0; fora[::2] = False; fora[:, ::2] = False
            A = np.zeros((3, 2), np.float32)
            for c in range(3): A[c] = np.polyfit(v32[..., c][fora], o32[..., c][fora], 1)
            fits.append(A)
            vc = v[FY0:FY1].astype(np.float32) * A[:, 0] + A[:, 1]
            w = np.maximum(cv2.GaussianBlur(Mb.astype(np.float32), (0, 0), 3), Mb)[..., None]
            o = o.copy(); o[FY0:FY1] = np.clip(vc * w + o32 * (1 - w), 0, 255).astype(np.uint8)
        yield q, o
    if fits:
        F = np.array(fits); log.append(f"base antiga -> original (faixa LaMa): ganho BGR {F[:, :, 0].mean(0).round(3)}, offset {F[:, :, 1].mean(0).round(2)} ({len(F)} quadros)")
def colar_trecho(nome, bases, g, caixa):
    X0, Y0, W, H = caixa; canto = CANTO.get(nome, (342, 575)); Mf = C.mascara(nome, canto); M = Mf[..., 0]
    x0, y0, x1, y1 = C.ROS[nome]["w"]; fw = x1 - x0
    dentro = M > 0.01
    anel = cv2.dilate(dentro.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.35 * fw) | 1,) * 2)).astype(bool) & ~dentro
    cx = np.zeros_like(anel); cx[Y0 + 3:Y0 + H - 3, X0 + 3:X0 + W - 3] = True; anel &= cx
    if canto: anel[:canto[1] + 6, :canto[0] + 6] = False
    miolo = M > 0.9
    ks = np.linspace(0, len(bases) - 1, 12).astype(int)
    crops = lambda k: cv2.resize(g[k], (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)
    def full(k, extra=0):
        f = bases[k].astype(np.float32).copy(); f[Y0:Y0 + H, X0:X0 + W] = crops(k) + extra; return f
    d0 = np.median(np.array([np.median((bases[k].astype(np.float32) - full(k))[anel], 0) for k in ks]), 0)
    d1 = np.clip(np.median(np.array([np.median((bases[k].astype(np.float32) - full(k, d0))[miolo], 0) for k in ks]), 0), -8, 8)
    Mc = Mf[Y0:Y0 + H, X0:X0 + W]
    out = []
    for k in range(len(bases)):
        f = bases[k].astype(np.float32).copy(); f[Y0:Y0 + H, X0:X0 + W] = crops(k) + d0 + d1 * Mc
        out.append(np.clip(f * Mf + bases[k] * (1 - Mf), 0, 255).astype(np.uint8))
    return out, (d0, d1, int(anel.sum()), int(miolo.sum()))
def enc(path, crf):
    return subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
        *ENC_VF,"-threads","4","-c:v","libx264","-crf",str(crf),"-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(path)], stdin=subprocess.PIPE)
if __name__ == "__main__":
    eb, el = enc(AD / "base_sem_legenda.mp4", 12), enc(AD / "base_lipsync.mp4", 14)
    gen = base_gen(); nl = 0
    def ler_base(n):
        fs = []
        for _ in range(n):
            q, f = next(gen); eb.stdin.write(f.tobytes()); fs.append(f)
        return fs
    def w(fs):
        global nl
        for f in fs: el.stdin.write(f.tobytes()); nl += 1
    a0 = SEGS[0]["quadro_ini"]; ler_base(a0)
    pend = None; pend_base = None
    for si, s in enumerate(SEGS):
        nome, a, n = s["nome"], s["quadro_ini"], s["n"]
        bases = ler_base(n)
        g = list(quadros(AQ / "out" / f"ls_{nome}.mp4")); m0 = len(g); g = C.reamostrar(g[:n] if s["pad"] else g, n)
        out, (d0, d1, na, nm) = colar_trecho(nome, bases, g, s["caixa"])
        log.append(f"{nome}: {m0}->{n} q; desvio anel {d0.round(2)} + interno {d1.round(2)} (anel {na} px, miolo {nm} px)")
        if si == 0:
            w([out[0]] * a0)   # quadros 0-3 = 1o quadro colado do s01
        else:
            corte = np.abs(pend_base.astype(np.float32) - bases[0]).mean() > 10
            dif = np.abs(pend_base.astype(np.float32) - bases[0]).mean()
            if not corte:
                L, R = pend[-1].astype(np.float32), out[0].astype(np.float32)
                pend[-1] = np.clip(L * 2 / 3 + R / 3, 0, 255).astype(np.uint8); out[0] = np.clip(L / 3 + R * 2 / 3, 0, 255).astype(np.uint8)
            log.append(f"  emenda {nome} q{a}: {'corte' if corte else 'crossfade 2q'} (dif {dif:.1f})")
            w(pend)
        pend, pend_base = out, bases[-1]; print(log[-1], flush=True)
    w(pend[:FIM - nl]); el.stdin.close(); el.wait()
    ler_base(NB - (SEGS[-1]["quadro_ini"] + SEGS[-1]["n"])); eb.stdin.close(); eb.wait()
    print("\n".join(log)); print("ok", nl, "quadros lipsync,", NB, "base")
