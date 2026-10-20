# -*- coding: utf-8 -*-
"""Troca o texto de uma faixa de rótulo (ex.: nome de marca num frasco) quadro a quadro, sem IA.
Apaga o texto antigo preenchendo a faixa com a própria cor de fundo (degradê/brilho preservados) e escreve
o texto novo no mesmo ângulo. O personagem e o resto do quadro não mudam nenhum pixel.

Modos (escolha um):
  --auto    acha a faixa pela cor (--cor) dentro da região de busca (--roi), endireita pelo ângulo, cobre a faixa
            na largura toda do rótulo (cor de fundo coluna a coluna) e suaviza o movimento no tempo.
            Bom para frasco em movimento. (--so-faixa: cobre só a área detectada, sem alargar ao rótulo)
  --seguir  segue a faixa pelas LINHAS (fração de pixels da cor por linha) e preenche linha a linha com a cor
            mediana da própria linha; geometria suavizada por mediana de 7 quadros. Bom para faixa horizontal,
            e com --cor escuro quando a faixa não é colorida.
  --caixa   caixa marcada à mão (chaves por quadro, interpoladas), para planos parados ou quase parados.

  python trocar_rotulo_faixa.py in.mp4 out.mp4 --auto --roi 200,820,400,920 --texto MARCA --de 143.07 --ate 145.67
  python trocar_rotulo_faixa.py in.mp4 out.mp4 --seguir --roi 290,840,452,940 --cor escuro --texto MARCA
  python trocar_rotulo_faixa.py in.mp4 out.mp4 --caixa "0:265,960,455,1010;60:270,965,460,1015" --texto MARCA
  python trocar_rotulo_faixa.py in.mp4 out.mp4 --auto --roi ... --texto MARCA --prev 10   (só salva o quadro 10 tratado)

--roi / --caixa: "x0,y0,x1,y1" fixo ou "q:x0,y0,x1,y1;q:x0,y0,x1,y1;..." com chaves por quadro (q contado a partir
  de --de), interpoladas no meio. Sem --roi no modo --auto/--seguir, procura no quadro inteiro.
--cor: verde | escuro | "h0,s0,v0,h1,s1,v1" (HSV do OpenCV, H de 0 a 179). Padrão: verde.
--de / --ate: só os quadros desse intervalo são tratados; o resto passa inalterado. Áudio copiado.
Saída: mesmo tamanho e fps do original, H.264 crf 14.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from comum import FONTS, POPPINS  # noqa: E402

CORES = {"verde": ((35, 30, 15), (95, 255, 140))}


# ----------------------------------------------------------------- utilidades
def ler_chaves(s: str) -> list[tuple[int, list[float]]]:
    """'x0,y0,x1,y1' ou 'q:x0,y0,x1,y1;q:...' -> [(q, [x0,y0,x1,y1]), ...] ordenado."""
    if ":" in s:
        return sorted((int(q), [float(v) for v in r.split(",")]) for q, r in (c.split(":") for c in s.split(";")))
    return [(0, [float(v) for v in s.split(",")])]


def chave_em(K, n: int) -> list[float]:
    if n <= K[0][0]:
        return list(K[0][1])
    for (q0, r0), (q1, r1) in zip(K, K[1:]):
        if n <= q1:
            t = (n - q0) / max(1, q1 - q0)
            return [u + (v - u) * t for u, v in zip(r0, r1)]
    return list(K[-1][1])


def roi_int(r, W, H) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = [int(round(v)) for v in r]
    return max(0, x0), max(0, y0), min(W, x1), min(H, y1)


def faixa_hsv(cor: str, smax: int, vmax: int):
    if cor == "escuro":
        return (0, 0, 20), (179, smax, vmax)
    if cor in CORES:
        return CORES[cor]
    v = [int(x) for x in cor.split(",")]
    if len(v) != 6:
        raise SystemExit("--cor: use verde, escuro ou 'h0,s0,v0,h1,s1,v1'")
    return tuple(v[:3]), tuple(v[3:])


def fonte_ajustada(caminho: str, texto: str, px: int, larg_max: float) -> ImageFont.FreeTypeFont:
    px = max(6, px)
    f = ImageFont.truetype(caminho, px)
    while f.getlength(texto) > larg_max and px > 6:
        px -= 1
        f = ImageFont.truetype(caminho, px)
    return f


def escrever(bgr: np.ndarray, texto: str, cx: float, cy: float, fnt, cor_rgb, ang: float = 0.0) -> np.ndarray:
    """Escreve `texto` centrado em (cx, cy), girado de `ang` graus (sentido anti-horário), e devolve BGR."""
    bb = fnt.getbbox(texto)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    base = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)).convert("RGBA")
    if abs(ang) < 0.3:
        d = ImageDraw.Draw(base)
        d.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), texto, font=fnt, fill=cor_rgb + (255,))
    else:
        img = Image.new("RGBA", (tw + 8, th + 10), (0, 0, 0, 0))
        ImageDraw.Draw(img).text((4 - bb[0], 5 - bb[1]), texto, font=fnt, fill=cor_rgb + (255,))
        img = img.rotate(ang, expand=True, resample=Image.BICUBIC)
        base.alpha_composite(img, (int(round(cx - img.width / 2)), int(round(cy - img.height / 2))))
    return cv2.cvtColor(np.array(base.convert("RGB")), cv2.COLOR_RGB2BGR)


def preencher_degrade(band: np.ndarray, perc_col: int = 45, perc_lin: int = 40, blur: int = 15) -> np.ndarray:
    """Cor de fundo da faixa: por coluna, média dos pixels mais escuros (o texto é claro), suavizada;
    perfil vertical leve para manter a borda de cima/baixo."""
    band = band.astype(np.float32)
    h, w = band.shape[:2]
    lum = band.mean(axis=2)
    cor = np.zeros((w, 3), np.float32)
    for j in range(w):
        sel = lum[:, j] <= np.percentile(lum[:, j], perc_col)
        cor[j] = band[:, j][sel].mean(axis=0)
    cor = cv2.blur(cor.reshape(1, -1, 3), (blur, 1)).reshape(-1, 3)
    vert = np.array([np.percentile(lum[y], perc_lin) for y in range(h)], np.float32)
    vert = vert / max(1.0, float(np.median(vert)))
    return np.clip(cor[None, :, :] * np.clip(vert, 0.85, 1.15)[:, None, None], 0, 255)


# ----------------------------------------------------------------- modo --auto (band_fix3)
class Auto:
    def __init__(self, a, K, W, H, lo, hi, fnt_path, cor_txt):
        self.a, self.K, self.W, self.H, self.lo, self.hi = a, K, W, H, lo, hi
        self.fnt_path, self.cor_txt = fnt_path, cor_txt
        self.est = None  # cx, cy, w, h, ang, L, R (suavizado)
        self.falhas = 0
        self.sem = 0     # quadros seguidos sem detecção

    def medir(self, f, n):
        a, W, H = self.a, self.W, self.H
        x0, y0, x1, y1 = roi_int(chave_em(self.K, n), W, H) if self.K else (0, 0, W, H)
        roi = f[y0:y1, x0:x1]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        m = cv2.morphologyEx(cv2.inRange(hsv, self.lo, self.hi), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        k, lab, st, _ = cv2.connectedComponentsWithStats(m)
        if k <= 1:
            return None
        i = 1 + int(np.argmax(st[1:, 4]))
        if st[i, 4] < a.min_area:
            return None
        cnt, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hull = cv2.convexHull(max(cnt, key=cv2.contourArea))
        (cx, cy), (rw, rh), ang = cv2.minAreaRect(hull)
        if rw < rh:
            rw, rh = rh, rw
            ang += 90
        if ang > 45:
            ang -= 180
        if ang < -45:
            ang += 180
        L, R = cx - rw / 2, cx + rw / 2
        if not a.so_faixa:
            # endireita e procura o rótulo claro logo abaixo da faixa para cobrir a largura toda
            M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
            rot = cv2.warpAffine(roi, M, (roi.shape[1], roi.shape[0]), flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_REPLICATE)
            ya = int(min(rot.shape[0] - 2, cy + rh / 2 + 2))
            yb = int(min(rot.shape[0] - 1, cy + rh / 2 + max(6, rh * 1.3)))
            if yb > ya:
                hv = cv2.cvtColor(rot[ya:yb], cv2.COLOR_BGR2HSV)
                claro = ((hv[..., 2] > 135) & (hv[..., 1] < 90)).mean(axis=0) > 0.25
                c = int(np.clip(cx, 0, len(claro) - 1))
                gap = max(4, int(rh * 0.5))
                l_ = c
                while l_ > 0 and claro[max(0, l_ - gap):l_].any():
                    l_ -= 1
                r_ = c
                while r_ < len(claro) - 1 and claro[r_ + 1:r_ + 1 + gap].any():
                    r_ += 1
                if (r_ - 1) - (l_ + 1) >= rw * 0.8:
                    L, R = l_ + 1, r_ - 1
        return np.array([cx + x0, cy + y0, rw, rh, ang, L + x0, R + x0], float)

    def tratar(self, f, n):
        medida = self.medir(f, n)
        if medida is None:
            self.falhas += 1
            self.sem += 1
            if self.est is None or self.sem > self.a.max_sem:   # faixa sumiu: não pinta no lugar velho
                self.est = None
                return f
        else:
            self.sem = 0
            self.est = medida if self.est is None else self.a.alfa * medida + (1 - self.a.alfa) * self.est
        cx, cy, rw, rh, ang, L, R = self.est
        W, H = self.W, self.H
        pad = int(rh * 1.5 + (R - L) * 0.2 + 10)
        X0, Y0 = int(max(0, min(L, cx - rw / 2) - pad)), int(max(0, cy - rh / 2 - pad))
        X1, Y1 = int(min(W, max(R, cx + rw / 2) + pad)), int(min(H, cy + rh / 2 + pad))
        if X1 - X0 < 8 or Y1 - Y0 < 4:
            return f
        pat = f[Y0:Y1, X0:X1].copy()
        ccx, ccy = cx - X0, cy - Y0
        M = cv2.getRotationMatrix2D((ccx, ccy), ang, 1.0)
        rp = cv2.warpAffine(pat, M, (pat.shape[1], pat.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        l, r = max(0, int(L - X0 + 2)), min(rp.shape[1], int(R - X0 - 2))
        t, b = max(0, int(round(ccy - rh / 2 + 1.5))), min(rp.shape[0], int(round(ccy + rh / 2 - 1.5)))
        if r - l <= 8 or b - t <= 4:
            return f
        rp[t:b, l:r] = preencher_degrade(rp[t:b, l:r]).astype(np.uint8)
        fnt = fonte_ajustada(self.fnt_path, self.a.texto, int((b - t) * self.a.escala), (r - l) * 0.72)
        rp = escrever(rp, self.a.texto, (l + r) / 2, (t + b) / 2, fnt, self.cor_txt)
        # volta ao ângulo original e cola só a faixa, com borda suave
        mask = np.zeros(rp.shape[:2], np.uint8)
        mask[t:b, l:r] = 255
        Mi = cv2.getRotationMatrix2D((ccx, ccy), -ang, 1.0)
        back = cv2.warpAffine(rp, Mi, (pat.shape[1], pat.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        mb = cv2.warpAffine(mask, Mi, (pat.shape[1], pat.shape[0]), flags=cv2.INTER_LINEAR)
        mb = cv2.GaussianBlur(mb, (3, 3), 0).astype(np.float32)[..., None] / 255
        f[Y0:Y1, X0:X1] = (back * mb + pat * (1 - mb)).astype(np.uint8)
        return f


# ----------------------------------------------------------------- modo --seguir (band_fix2)
class Seguir:
    """Passo 1 (preparar): geometria da faixa em cada quadro do intervalo, suavizada. Passo 2 (tratar)."""

    def __init__(self, a, K, W, H, lo, hi, fnt_path, cor_txt):
        self.a, self.K, self.W, self.H, self.lo, self.hi = a, K, W, H, lo, hi
        self.fnt_path, self.cor_txt = fnt_path, cor_txt
        self.G = None
        self.falhas = 0

    def _mask(self, hsv):
        g = cv2.inRange(hsv, self.lo, self.hi)
        k = self.a.fecho | 1
        return cv2.morphologyEx(g, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8)) > 0

    def _roi(self, n):
        return roi_int(chave_em(self.K, n), self.W, self.H) if self.K else (0, 0, self.W, self.H)

    def preparar(self, cap, i0, i1):
        geo = []
        cap.set(cv2.CAP_PROP_POS_FRAMES, i0)
        for n in range(i1 - i0 + 1):
            ok, f = cap.read()
            if not ok:
                break
            x0, y0, x1, y1 = self._roi(n)
            g = self._mask(cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2HSV))
            rows = np.where(g.mean(axis=1) > self.a.frac)[0]
            if len(rows) == 0:
                geo.append(None)
                continue
            runs, s = [], rows[0]
            for p, q in zip(rows[:-1], rows[1:]):
                if q - p > 3:
                    runs.append((s, p))
                    s = q
            runs.append((s, rows[-1]))
            ya, yb = max(runs, key=lambda r: r[1] - r[0])
            xc = np.where(g[ya:yb + 1].mean(axis=0) > 0.5)[0]
            if len(xc) < 5:
                geo.append(None)
                continue
            geo.append([ya + y0, yb + y0, xc[0] + x0, xc[-1] + x0])
        self.falhas = sum(1 for v in geo if v is None)
        ok_idx = [i for i, v in enumerate(geo) if v]
        if not ok_idx:
            raise SystemExit("--seguir: faixa não encontrada em nenhum quadro (ajuste --roi, --cor, --frac)")
        G = np.array([geo[i] if geo[i] else geo[min(ok_idx, key=lambda j: abs(j - i))] for i in range(len(geo))], float)
        self.G = np.array([np.median(G[max(0, i - 3):i + 4], axis=0) for i in range(len(G))])

    def tratar(self, f, n):
        if self.G is None or n >= len(self.G):
            return f
        x0, y0, x1, y1 = self._roi(n)
        ya, yb, xa, xb = [int(round(v)) for v in self.G[n]]
        ya, yb, xa, xb = ya - y0, yb - y0, xa - x0, xb - x0
        roi = f[y0:y1, x0:x1]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        g = (cv2.inRange(hsv, self.lo, self.hi) > 0) & (hsv[..., 2] < self.a.vfill)
        bloco = roi[max(0, ya):yb + 1, xa:xb + 1][g[max(0, ya):yb + 1, xa:xb + 1]]
        cor_bloco = np.median(bloco, axis=0) if len(bloco) > 3 else None
        ult = None
        for y in range(max(0, ya - 1), min(roi.shape[0], yb + 2)):
            seg, gg = roi[y, xa:xb + 1], g[y, xa:xb + 1]
            if gg.sum() > 3:
                cor = np.median(seg[gg], axis=0)
                ult = cor
            else:
                cor = cor_bloco if cor_bloco is not None else (ult if ult is not None else np.median(seg, axis=0))
            roi[y, xa + 1:xb] = cor.astype(np.uint8)
        fnt = fonte_ajustada(self.fnt_path, self.a.texto, int((yb - ya) * self.a.escala), (xb - xa) * 0.78)
        roi[:] = escrever(roi, self.a.texto, (xa + xb) / 2, (ya + yb) / 2, fnt, self.cor_txt)
        return f


# ----------------------------------------------------------------- modo --caixa (band_box)
class Caixa:
    def __init__(self, a, K, W, H, fnt_path, cor_txt):
        self.a, self.K, self.W, self.H, self.fnt_path, self.cor_txt = a, K, W, H, fnt_path, cor_txt
        self.falhas = 0

    def tratar(self, f, n):
        x0, y0, x1, y1 = chave_em(self.K, n)
        X0, Y0 = max(0, int(x0)), max(0, int(y0))
        X1, Y1 = min(self.W, int(np.ceil(x1))), min(self.H, int(np.ceil(y1)))
        if X1 - X0 < 4 or Y1 - Y0 < 3:
            return f
        band = f[Y0:Y1, X0:X1].astype(np.float32)
        novo = preencher_degrade(band, perc_col=40, perc_lin=35, blur=9)
        msk = np.zeros((Y1 - Y0, X1 - X0), np.float32)
        msk[2:-2, 2:-2] = 1
        msk = cv2.GaussianBlur(msk, (5, 5), 0)[..., None]
        f[Y0:Y1, X0:X1] = np.clip(novo * msk + band * (1 - msk), 0, 255).astype(np.uint8)
        fnt = fonte_ajustada(self.fnt_path, self.a.texto, int((y1 - y0) * self.a.escala), (x1 - x0) * 0.8)
        return escrever(f, self.a.texto, (x0 + x1) / 2, (y0 + y1) / 2, fnt, self.cor_txt)


# ----------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("saida")
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument("--auto", action="store_true")
    modo.add_argument("--seguir", action="store_true")
    modo.add_argument("--caixa", help='caixa fixa "x0,y0,x1,y1" ou com chaves "q:x0,y0,x1,y1;q:..."')
    ap.add_argument("--roi", help="região de busca (--auto/--seguir), fixa ou com chaves por quadro")
    ap.add_argument("--texto", required=True, help="texto novo da faixa")
    ap.add_argument("--fonte", default="Poppins-Bold.ttf", help="arquivo em kit/fonts ou caminho de .ttf")
    ap.add_argument("--cor", default="verde", help="verde | escuro | h0,s0,v0,h1,s1,v1 (HSV OpenCV)")
    ap.add_argument("--cor-texto", default="236,230,212", help="RGB do texto novo")
    ap.add_argument("--de", type=float, default=0.0)
    ap.add_argument("--ate", type=float, default=None)
    ap.add_argument("--escala", type=float, default=0.55, help="altura da fonte = altura da faixa x escala")
    ap.add_argument("--min-area", type=int, default=150, help="--auto: área mínima (px) da faixa detectada")
    ap.add_argument("--alfa", type=float, default=0.5, help="--auto: suavização temporal (1 = sem)")
    ap.add_argument("--so-faixa", action="store_true", help="--auto: cobre só a faixa detectada (não alarga ao rótulo)")
    ap.add_argument("--max-sem", type=int, default=3, help="--auto: quadros seguidos sem faixa antes de parar de pintar")
    ap.add_argument("--frac", type=float, default=0.45, help="--seguir: fração mínima da cor numa linha da faixa")
    ap.add_argument("--fecho", type=int, default=15, help="--seguir: tamanho do fechamento morfológico")
    ap.add_argument("--smax", type=int, default=140, help="--cor escuro: saturação máxima")
    ap.add_argument("--vmax", type=int, default=135, help="--cor escuro: brilho máximo")
    ap.add_argument("--vfill", type=int, default=110, help="--seguir: só pixels com V abaixo disto dão a cor de fundo")
    ap.add_argument("--crf", type=int, default=14)
    ap.add_argument("--prev", type=int, default=None, help="salva só o quadro N (a partir de --de) tratado em <saida>")
    a = ap.parse_args()

    fnt_path = a.fonte if Path(a.fonte).exists() else str(FONTS / a.fonte)
    if not Path(fnt_path).exists():
        fnt_path = str(POPPINS)
    cor_txt = tuple(int(v) for v in a.cor_texto.split(","))
    lo, hi = faixa_hsv(a.cor, a.smax, a.vmax)

    cap = cv2.VideoCapture(a.entrada)
    if not cap.isOpened():
        raise SystemExit(f"não abriu {a.entrada}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W, H = int(cap.get(3)), int(cap.get(4))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    i0 = int(round(a.de * fps))
    i1 = int(round(a.ate * fps)) if a.ate is not None else total - 1
    i1 = min(i1, total - 1)

    K = ler_chaves(a.roi) if a.roi else None
    if a.caixa:
        trat = Caixa(a, ler_chaves(a.caixa), W, H, fnt_path, cor_txt)
    elif a.auto:
        trat = Auto(a, K, W, H, lo, hi, fnt_path, cor_txt)
    else:
        trat = Seguir(a, K, W, H, lo, hi, fnt_path, cor_txt)
        trat.preparar(cv2.VideoCapture(a.entrada), i0, i1)

    if a.prev is not None:
        n = i0 + a.prev
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ok, f = cap.read()
        if not ok:
            raise SystemExit("quadro fora do vídeo")
        if a.auto:  # aquece a suavização com os quadros anteriores
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(i0, n - 5))
            for _ in range(min(5, n - i0)):
                ok2, f2 = cap.read()
                if ok2:
                    trat.tratar(f2, n - 5)
        cv2.imwrite(a.saida, trat.tratar(f, a.prev), [cv2.IMWRITE_JPEG_QUALITY, 92])
        print(f"prev: {a.saida} (quadro {n}, {n / fps:.2f}s)")
        return

    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", f"{fps}", "-i", "-", "-i", a.entrada, "-map", "0:v", "-map", "1:a?",
                           "-c:v", "libx264", "-crf", str(a.crf), "-preset", "medium", "-pix_fmt", "yuv420p",
                           "-c:a", "copy", "-shortest", a.saida], stdin=subprocess.PIPE)
    i = 0
    tratados = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if i0 <= i <= i1:
            f = trat.tratar(f, i - i0)
            tratados += 1
        ff.stdin.write(f.tobytes())
        i += 1
    ff.stdin.close()
    ff.wait()
    if ff.returncode:
        raise SystemExit("ffmpeg falhou ao gravar a saída")
    print(f"ok: {a.saida} | {i} quadros, {tratados} tratados ({i0 / fps:.2f}-{i1 / fps:.2f}s), "
          f"sem faixa em {trat.falhas}")


if __name__ == "__main__":
    main()
