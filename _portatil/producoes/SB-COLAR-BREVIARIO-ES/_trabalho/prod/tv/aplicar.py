import cv2, numpy as np, subprocess, warnings, sys; warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
sys.path.insert(0, ".")
from comum3 import quadros, ENC_VF, ENC_TAG
Q0, Q1, REF = 645, 698, 670
es = cv2.imread("tv/es670.png").astype(np.float32); m = np.load("tv/mask670.npy").astype(np.float32)
m = cv2.GaussianBlur(cv2.dilate(m, np.ones((9, 9), np.uint8)), (0, 0), 3)
lama = SimpleLama(); s = 4
def g(f): return cv2.cvtColor(cv2.resize(f, (270, 480), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
fr = list(quadros("base_sem_legenda.mp4", Q0, Q1 - Q0, 1080, 1920)); T = g(fr[REF - Q0])
im = np.zeros((480, 270), np.uint8); im[0:30] = 1; im[175:475] = 1
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","1080x1920","-r","30","-i","-",*ENC_VF,
    "-threads","3","-c:v","libx264","-crf","12","-preset","medium",*ENC_TAG,"-an","tv/tv_trecho.mp4"], stdin=subprocess.PIPE)
Wp = np.eye(2, 3, dtype=np.float32); chk = []
for k in range(REF - Q0, -1, -1), range(REF - Q0, len(fr)):
    pass
W = {}
for ordem in (range(REF - Q0, -1, -1), range(REF - Q0, len(fr))):
    w = np.eye(2, 3, dtype=np.float32)
    for k in ordem:
        try: _, w = cv2.findTransformECC(T, g(fr[k]), w, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-5), im, 5)
        except cv2.error: print("ecc falhou", k + Q0)
        W[k] = w.copy()
for k, f in enumerate(fr):
    M = W[k].copy(); M[:, 2] *= s
    pe = cv2.warpAffine(es, M, (1080, 1920), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    pm = cv2.warpAffine(m, M, (1080, 1920))[..., None]
    o = f.astype(np.float32) * (1 - pm) + pe * pm
    # caixa borrada da legenda antiga (1330-1445 x 215-830 no quadro 670)
    bm = np.zeros((1920, 1080), np.uint8); bm[1295:1485, 80:930] = 255
    o = np.clip(o, 0, 255).astype(np.uint8)
    r = lama(Image.fromarray(cv2.cvtColor(o, cv2.COLOR_BGR2RGB)), Image.fromarray(bm))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:1920, :1080]
    a = (cv2.GaussianBlur(bm.astype(np.float32) / 255, (0, 0), 3))[..., None]
    o = np.clip(r * a + o * (1 - a), 0, 255).astype(np.uint8)
    ff.stdin.write(o.tobytes())
    if k % 10 == 0: cv2.imwrite(f"tv/chk_{k + Q0}.jpg", cv2.resize(o, (360, 640)))
ff.stdin.close(); ff.wait(); print("ok", len(fr), {k + Q0: np.round(W[k][:, 2] * s, 1).tolist() for k in (0, len(fr) - 1)})
