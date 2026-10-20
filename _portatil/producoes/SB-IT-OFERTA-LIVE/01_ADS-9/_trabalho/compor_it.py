# Monta o SB-IT-ADS-9: gancho limpo (LaMa) + 11 trechos com lipsync HeyGen + live FR com selo "IN DIRETTA";
# legenda ASS IT, setas vermelhas no CTA (82,1-97,77 s), áudio mix_it.wav. Leitura/gravação bt709 fixa.
import subprocess, numpy as np, cv2, json, sys
W, H, FPS = 720, 1280, 30; TOTAL = 102.866; HK = 2.37; LIVE = 97.7667
C = [2.37, 9.6, 19.4, 29.1, 39.3, 48.0, 58.8, 68.4, 74.1, 81.7, 89.6, 97.7667]
SRC = r"C:\Users\PICHAU\Downloads\1-VIDEOS\ad 9 frances pronto.mp4"
SAIDA = sys.argv[1] if len(sys.argv) > 1 else "bruto_it.mp4"
VF_IN = "scale=720:1280:in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int+lanczos,format=bgr24"
def ler(p, ss=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.4f}", "-i", p] + (["-t", f"{dur:.4f}"] if dur else []) + ["-vf", VF_IN, "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (W * H * 3); return np.frombuffer(raw[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)
def caber(fr, n):   # reamostra p/ exatamente n quadros
    if len(fr) != n: print("aviso: quadros", len(fr), "esperado", n, flush=True)
    return [fr[min(i, len(fr) - 1)] for i in range(n)]
N = int(round(TOTAL * FPS)); nb = lambda t: int(round(t * FPS))
def gerar():
    feitos = 0
    for fr in caber(ler("lama/hook_limpo.mp4", 0, HK + 0.1), nb(HK)): feitos += 1; yield fr
    for k in range(11):
        fr = ler(f"heygen/out/ls_{k:02d}.mp4"); n = nb(C[k + 1]) - nb(C[k]); info.append((k, len(fr), n))
        for q in caber(fr, n): feitos += 1; yield q
        del fr
    for q in caber(ler(SRC, LIVE), N - feitos): yield q
info = []
selo = cv2.imread("selo_diretta.png", cv2.IMREAD_UNCHANGED)
se = cv2.imread("seta_esq.png", cv2.IMREAD_UNCHANGED); sd = cv2.imread("seta_dir.png", cv2.IMREAD_UNCHANGED)
def colar(img, png, x, y):
    h, w = png.shape[:2]; x, y = int(x), int(y)
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
    p = png[y0 - y:y1 - y, x0 - x:x1 - x]; a = p[..., 3:4].astype(np.float32) / 255
    img[y0:y1, x0:x1] = (p[..., :3] * a + img[y0:y1, x0:x1] * (1 - a)).astype(np.uint8)
SETA_INI = 82.1
# 81,2-82,45 s: borrão do LaMa (janela da máscara das setas FR) no decote -> repõe y>=840 com o quadro limpo de 30 s antes
R0, R1 = 81.2, 82.45
REF = ler("lama/base_limpa3.mp4", R0 - 30.0, R1 - R0 + 0.1)
ALR = np.clip((np.arange(H) - 840) / 80.0, 0, 1).astype(np.float32)[:, None, None]
def remendo(img, t):
    s = REF[min(len(REF) - 1, int(round((t - R0) * FPS)))]
    g1 = cv2.cvtColor(img[640:840], cv2.COLOR_BGR2GRAY).astype(np.float32); g2 = cv2.cvtColor(s[640:840], cv2.COLOR_BGR2GRAY).astype(np.float32)
    (dx, dy), _ = cv2.phaseCorrelate(g2, g1)
    s2 = cv2.warpAffine(s, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    return np.clip(s2.astype(np.float32) * ALR + img.astype(np.float32) * (1 - ALR), 0, 255).astype(np.uint8)
# restos de letra FR na borda (x<70 / x>650), que a 1ª máscara não pegou: LaMa só nesses quadros
from PIL import Image
from simple_lama_inpainting import SimpleLama
LAMA = SimpleLama(); n_borda = [0]
def borda(img):
    full = np.zeros((H, W), np.uint8)
    for x0, x1 in [(0, 70), (650, 720)]:
        hsv = cv2.cvtColor(img[830:1240, x0:x1], cv2.COLOR_BGR2HSV)
        m = ((hsv[..., 2] >= 205) & (hsv[..., 1] <= 45)).astype(np.uint8)
        if m.sum() > 40: full[830:1240, x0:x1] = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
    if full.sum() == 0: return img
    ys = np.where(full.any(1))[0]; a0, a1 = max(0, ys.min() - 100), min(H, ys.max() + 100)
    r = LAMA(Image.fromarray(cv2.cvtColor(img[a0:a1], cv2.COLOR_BGR2RGB)), Image.fromarray(full[a0:a1] * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:a1 - a0, :W].astype(np.float32)
    al = np.maximum(cv2.GaussianBlur(full.astype(np.float32), (9, 9), 0), full)[a0:a1, :, None]
    out = img.copy(); out[a0:a1] = np.clip(r * al + img[a0:a1] * (1 - al), 0, 255).astype(np.uint8); n_borda[0] += 1
    return out
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-i", "audio/mix_it.wav", "-filter_complex",
    "[0:v]ass=leg_it.ass:fontsdir=fonts,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]",
    "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-r", str(FPS),
    "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", SAIDA], stdin=subprocess.PIPE)
for i, q in enumerate(gerar()):
    t = i / FPS; img = q.copy()
    if R0 <= t < R1: img = remendo(img, t)
    if HK <= t < LIVE and any(a <= t < b for a, b in [(12.5, 15.5), (52.5, 56.5), (82.5, 86.5)]): img = borda(img)
    if SETA_INI <= t < LIVE:
        b = 14 * abs(np.sin(2 * np.pi * (t - SETA_INI) / 0.6))
        colar(img, se, 40 + b * 0.57, 985 + b * 0.82)
        colar(img, sd, W - 40 - sd.shape[1] - b * 0.57, 985 + b * 0.82)
    if t >= LIVE - 0.02: colar(img, selo, 265, 351)   # cobre tambem o 1o quadro da live (2933 = 97,7667 s)
    enc.stdin.write(np.ascontiguousarray(img).tobytes())
enc.stdin.close(); enc.wait(); print("trechos (k, quadros heygen, esperado):", info); print("borda corrigida em", n_borda[0], "quadros"); print("ok", SAIDA, i + 1, "quadros de", N)
