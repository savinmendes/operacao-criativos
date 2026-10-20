# -*- coding: utf-8 -*-
"""Fecha a boca do avatar HeyGen nas pausas da voz (o Avatar IV por foto abre um sorriso com dentes entre as frases,
o que reprova o índice de pausa). Adaptado de ADLIB-.../ad01/lipsync2/fechar.py para 1080x1920:
para cada pausa da voz (>= MINQ quadros abaixo de pico-30 dB) pega, no próprio clipe, o quadro vizinho com a boca
mais fechada, alinha ao rosto atual por pontos estáveis (olhos/nariz) e cola só boca+queixo com borda suave e rampa.
Leitura/gravação com matriz bt601/tv fixa (sem desvio de cor).
Uso:  python fechar_boca.py entrada.mp4 audio.mp3 saida.mp4
"""
import sys, subprocess
from pathlib import Path
import numpy as np, cv2

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
sys.path.insert(0, str(KIT))
sys.argv, ARGS = [sys.argv[0]], sys.argv[1:]
import checar_lipsync as CL  # noqa: E402

HOLD = "--segurar" in ARGS
ARGS = [x for x in ARGS if x != "--segurar"]
ENT, AUD, SAI = ARGS
W, H = 1080, 1920
MINQ, RAMPA, VIZ = 6, 3, 40
ESTAVEIS = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]


def fps_de(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate",
                        "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    a, b = r.split("/"); return float(a) / float(b)


def ler(p):
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", p, "-vf",
                           "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
                           "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    out = []; t = W * H * 3
    while True:
        b = pr.stdout.read(t)
        if len(b) < t: break
        out.append(np.frombuffer(b, np.uint8).reshape(H, W, 3).copy())
    pr.wait(); return out


def mascara(p):
    lab = (p[13] + p[14]) / 2; queixo = p[152]; nariz = p[2]
    c = (lab + queixo) / 2 + np.array([0, 0.08 * np.linalg.norm(queixo - nariz)])
    ax = int(0.62 * np.linalg.norm(p[61] - p[291]) + 24); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 12)
    m = np.zeros((H, W), np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    m[int(queixo[1]) + 6:, :] = 0          # nada abaixo do queixo (gola/colarinho não entram)
    return cv2.GaussianBlur(m, (0, 0), 8)


def main():
    fps = fps_de(ENT)
    fr = ler(ENT); n = len(fr)
    x = CL.ler_audio(AUD); env = CL.envelope(x, 16000, fps, n)
    fala = CL.mascara_fala(env)
    runs, k = [], 0
    while k < n:
        if not fala[k]:
            j = k
            while j < n and not fala[j]: j += 1
            if j - k >= MINQ: runs.append((k, j))
            k = j
        else:
            k += 1
    det = CL.Rastreador()
    P = [None] * n; ab = np.full(n, np.nan)
    need = set()
    for a, b in runs:
        need.update(range(max(0, a - VIZ), min(n, b + VIZ)))
    for k in sorted(need):
        P[k] = det.pontos(fr[k])
        if P[k] is not None: ab[k] = CL._abertura(P[k])
    orig = [f.copy() for f in fr]
    log = []
    QUEIXO = [152, 148, 377, 176, 400]
    TOL = 9.0   # px: erro max. do contorno do queixo entre ref alinhada e quadro atual (evita queixo duplo)
    for a, b in runs:
        viz = [k for k in range(max(0, a - VIZ), min(n, b + VIZ)) if np.isfinite(ab[k])]
        if not viz: continue
        lim = min(0.02, np.nanpercentile(ab[viz], 25))
        cands = [k for k in viz if ab[k] <= lim]
        esc, wts = {}, np.zeros(b - a)
        for k in range(a, b):
            pk = P[k]
            if pk is None: continue
            best = None
            for r in cands:
                M, _ = cv2.estimateAffinePartial2D(P[r][ESTAVEIS].astype(np.float32), pk[ESTAVEIS].astype(np.float32))
                if M is None: continue
                q = P[r][QUEIXO] @ M[:, :2].T + M[:, 2]
                e = float(np.linalg.norm(q - pk[QUEIXO], axis=1).mean())
                if best is None or e < best[0]: best = (e, r, M)
            if best:
                esc[k] = best
        # pausa inteira ou nada (fechar só parte dos quadros pisca a boca)
        if len(esc) < (b - a) or max(e for e, _, _ in esc.values()) > TOL * 1.6:
            # plano B: segura o quadro mais fechado logo antes da pausa (rosto inteiro), com fusão de 2 quadros
            ant = [k for k in range(max(0, a - 8), a + 2) if np.isfinite(ab[k])]
            if HOLD and ant:
                h = min(ant, key=lambda k: ab[k]); base = orig[h].astype(np.float32)
                for k in range(a, b):
                    w = min(1.0, (k - a + 1) / 2, (b - k) / 2)
                    fr[k] = np.clip(base * w + orig[k] * (1 - w), 0, 255).astype(np.uint8)
                log.append(f"pausa {a / fps:.2f}-{b / fps:.2f}s: quadro {h / fps:.2f}s segurado"); continue
            log.append(f"pausa {a / fps:.2f}-{b / fps:.2f}s: mantida (pose não casa)"); continue
        wts[:] = 1.0
        wts = np.convolve(np.pad(wts, 2, mode="edge"), np.ones(5) / 5, mode="valid")
        for i in range(len(wts)):
            wts[i] *= min(1.0, (i + 1) / RAMPA, (b - a - i) / RAMPA)
        feitos = 0
        for k, (e, r, M) in esc.items():
            w = wts[k - a]
            if w <= 0.01: continue
            g = cv2.warpAffine(orig[r], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            ms = mascara(P[k])[..., None] * w
            fr[k] = np.clip(g * ms + fr[k] * (1 - ms), 0, 255).astype(np.uint8); feitos += 1
        log.append(f"pausa {a / fps:.2f}-{b / fps:.2f}s: {feitos}/{b - a} quadros fechados")
    print("\n".join(log)); print(len(runs), "pausas")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", f"{fps}", "-i", "-", "-i", ENT, "-map", "0:v", "-map", "1:a", "-vf",
                            "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
                            "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "copy", SAI], stdin=subprocess.PIPE)
    for f in fr:
        enc.stdin.write(f.tobytes())
    enc.stdin.close(); enc.wait()


main()
