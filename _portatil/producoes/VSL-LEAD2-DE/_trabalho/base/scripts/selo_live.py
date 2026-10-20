# -*- coding: utf-8 -*-
"""Troca a pilula 'EN VIVO' por 'LIVE' (mesma pilula vermelha, posicao e altura de letra). Ponto vermelho e contador intactos.
Uso: python selo_live.py entrada.mp4 saida.mp4   |  python selo_live.py --teste quadro.png saida.png"""
import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
W, H = 720, 960; X0, Y0, X1, Y1 = 95, 29, 245, 67; COR = (205, 13, 31)  # RGB
S = 4
def overlay(COR=COR):
    w, h = (X1 - X0) * S, (Y1 - Y0) * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=tuple(int(c * 0.8) for c in COR) + (255,))
    d.rounded_rectangle([S, S, w - 1 - S, h - 1 - S], radius=h // 2 - S, fill=tuple(COR) + (255,))
    fn = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24 * S)
    bb = d.textbbox((0, 0), "LIVE", font=fn); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((w - tw) / 2 - bb[0], (h - th) / 2 - bb[1]), "LIVE", font=fn, fill=(255, 255, 255, 255))
    im = im.resize((X1 - X0, Y1 - Y0), Image.LANCZOS)
    a = cv2.GaussianBlur(np.array(im).astype(np.float32), (0, 0), 0.6); bgr = a[..., [2, 1, 0]]; al = a[..., 3:4] / 255.0
    return bgr, al
OV, AL = overlay(); _cor = [None]
def cor_da_pilula(f):
    r = f[33:63, 100:240].reshape(-1, 3).astype(int); m = (r[:, 2] > 150) & (r[:, 1] < 100) & (r[:, 0] < 100)
    return tuple(int(x) for x in np.median(r[m], 0)[::-1]) if m.sum() > 200 else None
def presenca(f):
    r = f[31:65, 100:240].astype(int); red = (r[..., 2] > 150) & (r[..., 1] < 100) & (r[..., 0] < 100)
    return float(np.clip((red.mean() - 0.25) / 0.35, 0, 1))
def aplicar(f):
    p = presenca(f)
    if p <= 0: return f, p
    global OV, AL
    c = cor_da_pilula(f)
    if c is not None and (_cor[0] is None or max(abs(a - b) for a, b in zip(c, _cor[0])) > 6): _cor[0] = c; OV, AL = overlay(c)
    roi = f[Y0:Y1, X0:X1].astype(np.float32); a = AL * p
    f = f.copy(); f[Y0:Y1, X0:X1] = np.clip(OV * a + roi * (1 - a), 0, 255).astype(np.uint8); return f, p
if __name__ == "__main__":
    if sys.argv[1] == "--teste":
        f = cv2.imread(sys.argv[2]); g, p = aplicar(f); print("presenca", p)
        cv2.imwrite(sys.argv[3], cv2.resize(np.vstack([f[0:80, 0:300], g[0:80, 0:300]]), None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)); sys.exit()
    ent, sai = sys.argv[1], sys.argv[2]
    ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
    ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", ent, "-vf", "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
        "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-an",
        *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, sai], stdin=subprocess.PIPE)
    n = 0; com = 0
    while True:
        b = rd.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        f = np.frombuffer(b, np.uint8).reshape(H, W, 3); g, p = aplicar(f); com += p > 0; n += 1
        wr.stdin.write(np.ascontiguousarray(g).tobytes())
        if n % 9000 == 0: print(f"[{n}/76899]", flush=True)
    wr.stdin.close(); wr.wait(); print("ok", n, "quadros; com selo:", com)
