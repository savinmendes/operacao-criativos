# -*- coding: utf-8 -*-
"""Pos-processa as saidas do HeyGen. uso: python finalizar.py [id ...]
out/ls_<id>.mp4 -> <id>.mp4 (so video, N quadros = duracao da timeline nova) + checar_lipsync (no recorte enviado).
padre_medio: saida do HeyGen cortada em N quadros. padre_pulpito: boca+queixo do recorte 2x colados no quadro inteiro
(elipse suave, posicao pelos landmarks suavizados, cor ajustada no anel em volta). Leitura/gravacao bt601 fixa."""
import json, subprocess, sys, re, os
from pathlib import Path
import cv2, numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
R = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\lipsync\LOTE_2")
KIT = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\checar_lipsync.py"
ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
def quadros(p, w, h):
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(p), "-vf", "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
        "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    t = w * h * 3; out = []
    while True:
        b = pr.stdout.read(t)
        if len(b) < t: break
        out.append(np.frombuffer(b, np.uint8).reshape(h, w, 3).copy())
    pr.wait(); return out
def nq(p):
    return int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(p)]))
def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    return [fr[min(m - 1, round(i * (m - 1) / max(1, n - 1)))] for i in range(n)]
LM = None
def landmarks(frames):
    global LM
    if LM is None:
        M = str(Path.home() / ".cache" / "kit-edicao" / "face_landmarker.task")
        LM = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=M), num_faces=1))
    pts = []
    for f in frames:
        r = LM.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(f, cv2.COLOR_BGR2RGB)))
        if not r.face_landmarks: pts.append(None); continue
        H, W = f.shape[:2]; L = r.face_landmarks[0]
        P = lambda i: np.array([L[i].x * W, L[i].y * H])
        boca = (P(13) + P(14)) / 2; fw = np.linalg.norm(P(234) - P(454)); fh = np.linalg.norm(P(10) - P(152))
        queixo = P(152)
        pts.append([boca[0], (boca[1] + queixo[1]) / 2, fw, fh])
    ok = [p for p in pts if p is not None]
    if not ok: return None, 0
    falhas = len(pts) - len(ok)
    a = np.array([p if p is not None else [np.nan] * 4 for p in pts], float)
    for c in range(4):
        col = a[:, c]; idx = np.arange(len(col)); g = ~np.isnan(col)
        a[:, c] = np.interp(idx, idx[g], col[g])
    k = 7; ker = np.ones(k) / k
    sm = np.array([np.convolve(np.pad(a[:, c], (k // 2, k // 2), mode="edge"), ker, "valid") for c in range(4)]).T
    return sm, falhas
def checar(i, cfg):
    r = subprocess.run([sys.executable, KIT, str(R / "out" / f"ls_{i}.mp4"), "--audio-novo", str(R / "in" / f"de_{i}.mp3"),
        "--original", str(R / "in" / f"es_{i}.mp4")], capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    txt = r.stdout.strip(); m = re.search(r"índice de pausa ([0-9.]+|-)", txt)
    ind = float(m.group(1)) if m and m.group(1) != "-" else None
    st = re.findall(r"^(APROVADO|AVISO|REPROVADO)", txt, re.M)
    return ind, (st[-1] if st else "ERRO"), txt
def fin(x):
    i, N, NP = x["id"], x["N"], x["NP"]; ls = R / "out" / f"ls_{i}.mp4"; dst = R / f"{i}.mp4"
    nls = nq(ls); nota = []
    if nls != NP: nota.append(f"HeyGen devolveu {nls} quadros (esperado {NP})")
    if x["crop"] is None:
        vf = f"tpad=stop_mode=clone:stop={max(0, N - nls) + 2},trim=end_frame={N},setpts=PTS-STARTPTS"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ls), "-vf", vf, "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
            "-pix_fmt", "yuv420p", *ENC_TAG, str(dst)], check=True)  # YUV intacto; etiqueta so no bitstream
    else:
        cx, cy, cw, ch = x["crop"]
        g = reamostrar(quadros(ls, cw * 2, ch * 2), NP)[:N]
        b = quadros(R / "in" / f"base_{i}.mp4", 720, 960)[:N]
        sm, falhas = landmarks(g)
        if sm is None: raise RuntimeError("sem rosto no recorte")
        if falhas: nota.append(f"rosto nao achado em {falhas} quadros (interpolado)")
        out = []; difs = []
        masks = []
        for k in range(N):
            mx, my, fw, fh = sm[k] / 2  # coords no quadro original (recorte reduzido 0.5x)
            m = np.zeros((960, 720), np.float32)
            cv2.ellipse(m, (int(cx + mx), int(cy + my)), (int(0.42 * fw), int(0.34 * fh)), 0, 0, 360, 1.0, -1)
            m = cv2.GaussianBlur(m, (0, 0), max(2.5, 0.07 * fw))
            masks.append(m)
        # cor: anel em volta da mascara, media (heygen reduzido - base)
        for k in range(0, N, max(1, N // 12)):
            gs = cv2.resize(g[k], (cw, ch), interpolation=cv2.INTER_AREA).astype(np.float32)
            bb = b[k][cy:cy + ch, cx:cx + cw].astype(np.float32); mm = masks[k][cy:cy + ch, cx:cx + cw]
            anel = (mm > 0.02) & (mm < 0.5)
            if anel.sum() > 50: difs.append((bb[anel] - gs[anel]).mean(0))
        dv = np.mean(difs, 0) if difs else np.zeros(3)
        nota.append("ajuste cor BGR %s" % np.round(dv, 1).tolist())
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x960", "-r", "30", "-i", "-",
            *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, str(dst)], stdin=subprocess.PIPE)
        for k in range(N):
            gs = np.clip(cv2.resize(g[k], (cw, ch), interpolation=cv2.INTER_AREA).astype(np.float32) + dv, 0, 255)
            full = b[k].astype(np.float32); full[cy:cy + ch, cx:cx + cw] = gs
            m = masks[k][..., None]
            enc.stdin.write(np.clip(full * m + b[k] * (1 - m), 0, 255).astype(np.uint8).tobytes())
        enc.stdin.close(); enc.wait()
    nf = nq(dst)
    if nf != N: nota.append(f"!! saida com {nf} quadros (esperado {N})")
    ind, st, txt = checar(i, x)
    return {"n_quadros": nf, "indice": ind, "checar": st, "nota": "; ".join(nota), "log": txt}
if __name__ == "__main__":
    plano = json.load(open(R / "plano.json")); so = set(sys.argv[1:])
    RJ = R / "_tmp" / "fin.json"; res = json.load(open(RJ, encoding="utf-8")) if RJ.exists() else {}
    for x in plano:
        if so and x["id"] not in so: continue
        if not (R / "out" / f"ls_{x['id']}.mp4").exists(): continue
        if not so and x["id"] in res: continue
        try: res[x["id"]] = fin(x)
        except Exception as e: res[x["id"]] = {"erro": str(e)}
        print(x["id"], {k: v for k, v in res[x["id"]].items() if k != "log"}, flush=True)
        json.dump(res, open(RJ, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
