# -*- coding: utf-8 -*-
"""base_visual_es.mp4 = base_sem_legenda.mp4 + correções de pixel (mesmos quadros, mesmo tempo, áudio original):
  1) arroba da live "padre.paulo_" -> "padre.pablo_" (troca só o u por b, em todo quadro em que a moldura aparece)
  2) cartão das 12 palavras com as traduções em espanhol (1452–1810)
  3) desfoque do texto PT legível: página do livro (1332–1451), livro aberto embaixo do padre (1844–2032),
     print de WhatsApp (2991–3147), livro na mesa (3280–3395)
Leitura bt709/tv e gravação com a matriz inversa bt709/tv (pixel não tocado volta igual)."""
import sys, json, subprocess, time, numpy as np, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
AQ = Path(__file__).resolve().parent.parent; T = AQ / "_tmp"
sys.path.insert(0, str(Path(__file__).parent)); import cartao
ORIG = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
BASE = str(AQ / "base_sem_legenda.mp4"); SAIDA = str(AQ / "base_visual_es.mp4")
W, H = 720, 1280; N = 4645
def leitor(p, rng):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-i", p, "-vf", f"scale=in_color_matrix=bt709:in_range={rng}:flags=accurate_rnd+full_chroma_int,format=bgr24",
                             "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
# ---------- arroba ----------
ref = cv2.imread(str(T / "g_63.png"))           # quadro 1890 (fundo escuro): molde do texto
mn = ref.min(2)
TX = np.zeros((H, W), np.uint8); TX[55:90, 186:298] = (mn[55:90, 186:298] > 150)   # "padre.pa"
ANEL = cv2.dilate(TX, np.ones((7, 7), np.uint8)) & ~cv2.dilate(TX, np.ones((3, 3), np.uint8))
TXb, ANb = TX.astype(bool), ANEL.astype(bool)
SC_REF = float(mn[TXb].mean() - mn[ANb].mean())
U = np.zeros((H, W), np.uint8); U[58:83, 299:316] = (mn[58:83, 299:316] > 110)
U = cv2.dilate(U, np.ones((3, 3), np.uint8))
fb = ImageFont.truetype(r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf", 26); fb.set_variation_by_name("SemiBold")
fb2 = ImageFont.truetype(r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf", 52); fb2.set_variation_by_name("SemiBold")
Lb = Image.new("L", (W * 2, H * 2), 0); db = ImageDraw.Draw(Lb); bb = db.textbbox((0, 0), "b", font=fb2, anchor="ls")
db.text((2 * 300 - bb[0], 2 * 78 + 1), "b", font=fb2, anchor="ls", fill=255)
LB = np.array(Lb.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
LB = np.clip(cv2.GaussianBlur(LB, (0, 0), 0.45) * 1.3, 0, 1)[..., None]
COR_TXT = np.array([245, 245, 245], np.float32)
def arroba(f):
    m = f.min(2).astype(np.float32)
    sc = float(m[TXb].mean() - m[ANb].mean())
    a = float(np.clip(sc / (0.3 * SC_REF), 0, 1))
    if a < 0.25: return f, 0.0
    x0, y0, x1, y1 = 290, 50, 326, 90
    pat = f[y0:y1, x0:x1].copy()
    inp = cv2.inpaint(pat, U[y0:y1, x0:x1], 3, cv2.INPAINT_TELEA)
    out = f.astype(np.float32)
    um = U[y0:y1, x0:x1].astype(np.float32)[..., None] * a
    out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - um) + inp.astype(np.float32) * um
    cor = np.median(f[TXb], 0).astype(np.float32)        # cor real do texto neste quadro
    out = out * (1 - LB * a) + cor[None, None] * (LB * a)
    return np.clip(out, 0, 255).astype(np.uint8), a
# ---------- desfoques ----------
def papel(f, ymin=112, area=8000, close=41, lim=135):
    mn_ = f.min(2).astype(int); mx_ = f.max(2).astype(int)
    m = ((mn_ > lim) & ((mx_ - mn_) < 60)).astype(np.uint8); m[:ymin] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close, close)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m); k = np.zeros_like(m)
    for j in range(1, n):
        if st[j, 4] >= area: k[lab == j] = 1
    if k.any():
        cs, _ = cv2.findContours(k, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        k = np.zeros_like(k); cv2.drawContours(k, [cv2.convexHull(c) for c in cs], -1, 1, -1)
        k = cv2.dilate(k, np.ones((15, 15), np.uint8))
    return k
def desfocar(f, mask, sig):
    if not mask.any(): return f
    a = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 6)[..., None]; a = np.maximum(a, mask[..., None])
    bl = cv2.GaussianBlur(f, (0, 0), sig)
    return np.clip(bl * a + f * (1 - a), 0, 255).astype(np.uint8)
TOPO = np.zeros((H, W), np.uint8); TOPO[108:, :] = 1
REGRAS = [(1332, 1451, "tudo", 11, {}), (1844, 2032, "papel", 9, {"ymin": 690}), (2991, 3147, "papel", 10, {}), (3280, 3395, "papel", 9, {"ymin": 420, "lim": 95})]
# ---------- laço ----------
pb, po = leitor(BASE, "tv"), leitor(ORIG, "full")
tmp = SAIDA.replace(".mp4", "_v.mp4")
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
    "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
    "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709",
    "-color_trc", "bt709", tmp], stdin=subprocess.PIPE)
S = W * H * 3; ult = None; log = {"arroba": [], "papel": {}}; t0 = time.time()
for i in range(N):
    b1, b2 = pb.stdout.read(S), po.stdout.read(S)
    if len(b1) < S or len(b2) < S: break
    f = np.frombuffer(b1, np.uint8).reshape(H, W, 3).copy(); o = np.frombuffer(b2, np.uint8).reshape(H, W, 3)
    f, ult = cartao.aplicar(i, f, o, ult)
    for a, b, modo, sig, kw in REGRAS:
        if a <= i <= b:
            mk = TOPO if modo == "tudo" else papel(o, **kw)
            if modo == "papel" and mk.any(): log["papel"].setdefault(f"{a}-{b}", 0); log["papel"][f"{a}-{b}"] += 1
            f = desfocar(f, mk, sig)
    f, al = arroba(f)
    if al > 0: log["arroba"].append(i)
    enc.stdin.write(f.tobytes())
    if (i + 1) % 300 == 0: el = time.time() - t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s", flush=True)
enc.stdin.close(); enc.wait()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", ORIG, "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", SAIDA], check=True)
Path(tmp).unlink()
ar = log["arroba"]; seg = []
for k in ar:
    if seg and k - seg[-1][1] <= 2: seg[-1][1] = k
    else: seg.append([k, k])
log["arroba"] = seg
json.dump(log, open(T / "compor_log.json", "w"), indent=1); print("ok", SAIDA, seg)
