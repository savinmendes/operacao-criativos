# -*- coding: utf-8 -*-
"""Lote C: tira o xadrez de pixels sob o labio (perfil, w04) em 35,27-35,40 e 35,63-35,87 s, sem credito.
O mesmo defeito aparece mais fraco em todo o plano de perfil do w04 (quadros 1003-1138; corte de camera em 1139): em cada quadro do w04, janela na boca da mulher
(faces_13.jsonl do revisor, rosto mais a esquerda); mascara = excesso de resposta ao kernel de xadrez (final - base_sem_legenda),
so corrige se a mascara tiver >= 50 px;
inpaint TELEA + borda suave (gauss 2 px). Le e grava com a conversao exata do comum3 (sem desvio de cor).
Grava out/xadrez_patch.mp4 (so os quadros corrigidos, sem perda) e o ../corpo_ad13.mp4 = base_lipsync (yuv direto, como antes) + patch, com o audio copiado do corpo anterior
(../_antes_cor/corpo_ad13.mp4). A base_lipsync.mp4 fica a mesma da v3."""
import subprocess, cv2, numpy as np
from pathlib import Path
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).parent; AD = AQ.parent
K = np.array([[1, -1], [-1, 1]], float); Q0, Q1 = 1003, 1139; THR = 3.0; NMIN = 50
import json
ROWS = {json.loads(l)["q"]: json.loads(l)["faces"] for l in open(AD.parent / "revisao" / "loteC" / "faces_13.jsonl")}
def janela(i):
    fs = ROWS.get(i)
    if not fs: return 400, 520, 220, 340
    fc = min(fs, key=lambda x: x["cx"]); cx, cy, L = fc["cx"], fc["cy"], fc["L"]
    return int(cy - 0.4 * L), int(cy + 0.9 * L), int(cx - 0.7 * L), int(cx + 0.7 * L)
# guarda do indice de pausa: nos quadros de PAUSA da voz ES do w04 so aceita a correcao se a abertura da boca
# (mediapipe no recorte do rosto que o revisar_ad --lipsync usa) nao aumentar
import sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
DET = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=1))
ROSTO = (85, 285, 283, 260)
def abertura(f):
    x, y, w, h = ROSTO; c = np.ascontiguousarray(cv2.cvtColor(f[y:y + h, x:x + w], cv2.COLOR_BGR2RGB))
    r = DET.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=c))
    return cl._abertura(np.array([(q.x * w, q.y * h) for q in r.face_landmarks[0]])) if r.face_landmarks else np.nan
FAL = cl.mascara_fala(cl.envelope(cl.ler_audio(str(AQ / "rev" / "es_w04.mp3")), 16000, 30, 1307 - 1003))
TOL = 0.0
def pausa(i): return 1003 <= i < 1307 and not FAL[i - 1003]
def resp(f): return np.abs(cv2.filter2D(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(float), -1, K))
def consertar(f, b, Y0, Y1, X0, X1):
    c = f[Y0:Y1, X0:X1].copy(); rb = cv2.blur(resp(b[Y0:Y1, X0:X1]), (5, 5)); rf = cv2.blur(resp(c), (5, 5))
    m = cv2.morphologyEx(((rf - rb) > THR).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)); n = int(m.sum())
    if n < NMIN: return f, 0
    m = cv2.dilate(m, np.ones((3, 3), np.uint8)); inp = cv2.inpaint(c, m * 255, 4, cv2.INPAINT_TELEA)
    w = np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2.0)[..., None] * 1.5, 0, 1)
    o = f.copy(); o[Y0:Y1, X0:X1] = np.clip(inp * w + c * (1 - w), 0, 255).astype(np.uint8); return o, n
src = AD / "_antes_cor" / "base_lipsync.mp4"; n = int(cv2.VideoCapture(str(src)).get(7))
PATCH = AQ / "out" / "xadrez_patch.mp4"   # so os quadros Q0..Q1-1 corrigidos, sem perda (qp 0), conversao exata
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",*ENC_VF,
    "-c:v","libx264","-qp","0","-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,str(PATCH)], stdin=subprocess.PIPE)
bs = quadros(AD / "base_sem_legenda.mp4"); sheet = []; nfix = 0; ult = None
for i, f in enumerate(quadros(src, 0, Q1)):
    b = next(bs)
    if Q0 <= i < Q1:
        jn = janela(i); g, k = consertar(f, b, *jn)
        if k and pausa(i):
            a0, a1 = abertura(f), abertura(g)
            print(f"  pausa q{i}: {k} px, abertura {a0:.3f} -> {a1:.3f}", "MANTIDO SEM CORRECAO" if a1 > a0 + TOL else "")
            if a1 > a0 + TOL and ult is not None:
                # quadro vizinho limpo: na mancha (mascara dilatada, borda suave) usa o quadro anterior ja corrigido
                Y0, Y1, X0, X1 = jn; c = f[Y0:Y1, X0:X1]
                m = cv2.morphologyEx(((cv2.blur(resp(c), (5, 5)) - cv2.blur(resp(b[Y0:Y1, X0:X1]), (5, 5))) > THR).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
                w = np.clip(cv2.GaussianBlur(cv2.dilate(m, np.ones((7, 7), np.uint8)).astype(np.float32), (0, 0), 2.5)[..., None] * 1.5, 0, 1)
                g2 = f.copy(); g2[Y0:Y1, X0:X1] = np.clip(ult[Y0:Y1, X0:X1] * w + c * (1 - w), 0, 255).astype(np.uint8); a2 = abertura(g2)
                print(f"    vizinho q{i-1}: abertura {a2:.3f}", "ok" if a2 <= a0 + TOL else "MANTIDO SEM CORRECAO")
                g = g2 if a2 <= a0 + TOL else f; k = k if a2 <= a0 + TOL else 0
            elif a1 > a0 + TOL: g, k = f, 0
        f = g; nfix += k > 0; ult = f
        if i in (1015, 1022, 1038, 1039, 1046, 1059, 1060, 1072, 1104, 1108, 1111, 1114): sheet.append(cv2.resize(f[jn[0]:jn[1], jn[2]:jn[3]], (240, 220)))
        ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait()
# corpo = base_lipsync (yuv direto, como antes) com o patch por cima so em Q0..Q1-1; mesmos parametros do corpo anterior (crf 14, medium, 4 threads)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(src),"-i",str(PATCH),"-i",str(AD / "_antes_cor" / "corpo_ad13.mp4"),"-filter_complex",
    f"[1:v]setpts=PTS+{Q0}/30/TB[p];[0:v][p]overlay=eof_action=pass:enable='between(n,{Q0},{Q1-1})'[v]","-map","[v]","-map","2:a",
    "-frames:v","3594","-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",
    "-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-c:a","copy",str(AD / "corpo_ad13.mp4")], check=True)
while len(sheet) % 6: sheet.append(np.zeros_like(sheet[0]))
cv2.imwrite(str(AQ / "chk_xadrez_fix.jpg"), np.vstack([np.hstack(sheet[i:i + 6]) for i in range(0, len(sheet), 6)]))
print("ok", n, "quadros corrigidos", nfix)
