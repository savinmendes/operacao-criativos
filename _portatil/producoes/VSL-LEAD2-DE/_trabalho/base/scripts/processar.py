# -*- coding: utf-8 -*-
"""Base sem legenda por blocos de 5 min (9000 quadros). Retomavel: pula blocos prontos (blocos/bXX.mp4 + .ok).
Uso: _vg python scripts/processar.py"""
import sys, os, json, time, subprocess, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import numpy as np, cv2
from simple_lama_inpainting import SimpleLama
from limpar import preparar, inpaint, corrigir_fill
SRC = r"C:\Users\PICHAU\Downloads\Lead 2.mp4"; N = 76899; BL = 9000; PASSO = 6; W, H = 720, 960
PAINEL = r"C:\Users\PICHAU\Downloads\Produtividade com ia\painel\painel.py"
os.makedirs("blocos", exist_ok=True)
ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
def ocr():
    while True:
        try: return {int(k): v for k, v in json.load(open("ocr_boxes.json")).items()}
        except Exception: time.sleep(5)
import bisect
_K = []
def caixas(D, i):
    if len(_K) != len(D): _K[:] = sorted(D)
    j = bisect.bisect_right(_K, i) - 1
    a = _K[j] if j >= 0 else None; b = _K[j + 1] if j + 1 < len(_K) else None
    if a == i: return D[a]
    return (D[a] if a is not None else []) + (D[b] if b is not None else [])
def painel(k, n, txt):
    subprocess.run([sys.executable if False else "python", PAINEL, "etapa", "vsl-de-base", "VSL DE: base sem legenda (LaMa)", "--texto", txt, "--k", str(k), "--n", str(n)], capture_output=True)
lama = SimpleLama(); nb = (N + BL - 1) // BL; T0 = time.time(); feitos = 0
for bi in range(nb):
    out = f"blocos/b{bi:02d}.mp4"
    if os.path.exists(out + ".ok"): continue
    q0, q1 = bi * BL, min(N, (bi + 1) * BL)
    D = ocr()
    while max(D) < q1 - 1 and max(D) < N - 12:   # espera o OCR cobrir o bloco
        time.sleep(30); D = ocr()
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{q0/30:.4f}", "-i", SRC, "-frames:v", str(q1 - q0), "-vf",
        "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24", "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-an",
        *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "fast", *ENC_TAG, out], stdin=subprocess.PIPE)
    t0 = time.time(); prev = None; ema = None; pm = None; log = []
    for i in range(q0, q1):
        b = rd.stdout.read(W * H * 3)
        if len(b) < W * H * 3: print("quadro faltando", i); break
        f = np.frombuffer(b, np.uint8).reshape(H, W, 3).copy()
        g = cv2.resize(f, (90, 120)).astype(np.float32)
        corte = prev is not None and np.abs(g - prev).mean() > 20; prev = g
        bx = caixas(D, i)
        if not bx: ema = None; wr.stdin.write(f.tobytes()); continue
        try: u, mk, modos = preparar(f, bx)
        except Exception as e:
            u = f; mk = np.zeros((H, W), np.uint8); modos = ["erro:" + str(e)[:60]]
            for x0, y0, x1, y1 in bx: mk[max(0, y0 - 10):y1 + 10, max(0, x0 - 10):x1 + 10] = 1
        o = inpaint(lama, u, mk)
        if ema is not None and not corte and pm is not None:
            both = (mk > 0) & (pm > 0)
            o = o.copy(); o[both] = np.clip(0.7 * o[both] + 0.3 * ema[both], 0, 255).astype(np.uint8)
        ema = o; pm = mk
        if i % 300 == 0: log.append([i, modos])
        wr.stdin.write(np.ascontiguousarray(o).tobytes())
        k = i - q0 + 1
        if k % 900 == 0:
            el = time.time() - t0; tot = time.time() - T0; feitos_q = feitos * BL + k
            rest_q = (N - q0 - k) + 0; fps = feitos_q / tot
            msg = f"bloco {bi+1}/{nb} [{k}/{q1-q0}] | total {100*(q0+k)//N}% | {fps:.1f} q/s | falta ~{rest_q/fps/60:.0f} min"
            print(msg, flush=True); painel(bi, nb, msg)
    rd.stdout.close(); rd.wait(); wr.stdin.close(); wr.wait()
    json.dump(log, open(out + ".log.json", "w"))
    open(out + ".ok", "w").write(f"{q1-q0} {time.time()-t0:.0f}s telea_quadros={corrigir_fill.quadros}")
    feitos += 1; print("ok bloco", bi, round(time.time() - t0), "s", flush=True)
print("FIM", round(time.time() - T0), "s")
