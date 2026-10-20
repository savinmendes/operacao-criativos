# -*- coding: utf-8 -*-
"""Prepara as entradas HeyGen do LOTE 1.  Uso: python prep.py [id ...]
Para cada trecho: quadros do ORIGINAL remapeados quadro a quadro para a timeline nova (mesmo mapeamento das
secoes_video da timeline_de.json), audio ES original esticado pelo mesmo fator (atempo), audio DE da narracao.
Gera em ../work/<id>/: orig.mp4 (quadro inteiro 720x960, timeline nova, sem audio), in.mp4 (recorte do rosto
ampliado + audio ES), de.mp3, es.wav, info.json. Trecho < 3,2 s: padding com o ultimo quadro (descartado depois).
Cor: leitura e gravacao bt601/tv fixas (etiqueta bt709 so no bitstream)."""
import sys, json, subprocess, math
from pathlib import Path
import numpy as np, cv2

AQ = Path(__file__).resolve().parent.parent
TR = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho")
SRC = r"C:\Users\PICHAU\Downloads\Lead 2.mp4"
NARR = TR / "voz" / "narracao_de_completa.wav"
W, H, FPS = 720, 960, 30
MIN_DUR = 3.2
ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
TL = json.load(open(TR / "voz" / "timeline_de.json", encoding="utf-8"))
SEC = TL["secoes_video"]
LOT = json.load(open(TR / "voz" / "lotes.json", encoding="utf-8"))
EXCLUIR = {f"L{i:03d}" for i in range(1, 22)}  # apresentador de batina branca: pendente de decisao da pessoa


def src_de(t):
    for s in SEC:
        if s["novo_ini"] - 1e-6 <= t < s["novo_fim"] + 1e-6:
            return s["src_ini"] + (t - s["novo_ini"]) / s["fator"]
    raise ValueError(t)


def pecas(a, b):
    out = []
    for s in SEC:
        lo, hi = max(a, s["novo_ini"]), min(b, s["novo_fim"])
        if hi - lo > 0.002:
            out.append((s["src_ini"] + (lo - s["novo_ini"]) / s["fator"], s["src_ini"] + (hi - s["novo_ini"]) / s["fator"], s["fator"]))
    return out


def ler(t0, n):
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-i", SRC, "-frames:v", str(n), "-vf",
                           "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
                           "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    fr = []; t = W * H * 3
    while len(fr) < n:
        b = pr.stdout.read(t)
        if len(b) < t: break
        fr.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    pr.stdout.close(); pr.wait()
    return fr


def gravar(frames, path, w, h, audio=None):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-"]
    if audio: cmd += ["-i", str(audio)]
    cmd += [*ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG]
    cmd += (["-c:a", "aac", "-b:a", "192k", "-shortest"] if audio else ["-an"]) + [str(path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in frames: p.stdin.write(np.ascontiguousarray(f).tobytes())
    p.stdin.close(); assert p.wait() == 0, path


_det = None
def detector():
    global _det
    if _det is None:
        import mediapipe as mp
        from mediapipe.tasks.python import vision, BaseOptions
        _det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(Path.home() / ".cache" / "kit-edicao" / "face_landmarker.task")),
            num_faces=3, min_face_detection_confidence=0.3))
    return _det


def rostos(fr):
    import mediapipe as mp
    rgb = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
    r = detector().detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
    out = []
    for lm in r.face_landmarks:
        p = np.array([[q.x * W, q.y * H] for q in lm])
        out.append(p)
    return out


def preparar(t):
    tid = t["id"]; D = AQ / "work" / tid; D.mkdir(parents=True, exist_ok=True)
    q0, q1 = round(t["novo_ini"] * FPS), round(t["novo_fim"] * FPS); N = q1 - q0
    idx = [int(math.floor(src_de((q0 + k + 0.5) / FPS) * FPS)) for k in range(N)]
    i0, i1 = min(idx), max(idx)
    raw = ler(i0 / FPS, i1 - i0 + 1)
    frames = [raw[min(i - i0, len(raw) - 1)] for i in idx]
    # rosto: amostra a cada 3 quadros, maior rosto
    caixas, bocas = [], {}
    for k in range(0, N, 3):
        fs = rostos(frames[k])
        if not fs: continue
        p = max(fs, key=lambda p: np.ptp(p[:, 0]))
        caixas.append([p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()])
    if not caixas:
        print(tid, "SEM ROSTO"); json.dump({"id": tid, "erro": "sem_rosto"}, open(D / "info.json", "w")); return
    C = np.array(caixas)
    x0, y0, x1, y1 = np.percentile(C[:, 0], 3), np.percentile(C[:, 1], 3), np.percentile(C[:, 2], 97), np.percentile(C[:, 3], 97)
    fw, fh = np.median(C[:, 2] - C[:, 0]), np.median(C[:, 3] - C[:, 1])
    cw = max(360.0, (x1 - x0) * 2.2, (y1 - y0) * 1.7 * 0.75)
    cw = min(cw, W); ch = cw * 4 / 3
    if ch > H: ch = H; cw = H * 0.75
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 0.05 * fh
    if cw >= W - 1:
        crop = [0, 0, W, H]
    else:
        cxx = int(round(min(max(cx - cw / 2, 0), W - cw))); cyy = int(round(min(max(cy - ch / 2, 0), H - ch)))
        crop = [cxx, cyy, int(round(cw)), int(round(ch))]
    cx0, cy0, cw_, ch_ = crop
    ins = [cv2.resize(f[cy0:cy0 + ch_, cx0:cx0 + cw_], (W, H), interpolation=cv2.INTER_LANCZOS4) if crop != [0, 0, W, H] else f for f in frames]
    Np = max(N, int(math.ceil(MIN_DUR * FPS)))
    ins += [ins[-1]] * (Np - N)
    dur, durp = N / FPS, Np / FPS
    # audio ES (original) esticado pelo mesmo fator, por peca
    pcs = pecas(q0 / FPS, q1 / FPS)
    fc, lab = [], []
    for j, (a, b, f) in enumerate(pcs):
        fc.append(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,atempo={1 / f:.6f}[p{j}]"); lab.append(f"[p{j}]")
    fc.append("".join(lab) + f"concat=n={len(lab)}:v=0:a=1,apad,atrim=0:{durp:.4f},aresample=48000[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(fc), "-map", "[a]", "-ac", "2", str(D / "es.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(NARR), "-af",
                    f"atrim={q0 / FPS:.4f}:{q1 / FPS:.4f},asetpts=PTS-STARTPTS,apad,atrim=0:{durp:.4f}", "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(D / "de.mp3")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(NARR), "-af",
                    f"atrim={q0 / FPS:.4f}:{q1 / FPS:.4f},asetpts=PTS-STARTPTS", "-ac", "1", str(D / "de_real.wav")], check=True)
    gravar(frames, D / "orig.mp4", W, H)
    gravar(ins, D / "in.mp4", W, H, D / "es.wav")
    info = {"id": tid, "q0": q0, "q1": q1, "n": N, "n_pad": Np, "crop": crop, "rosto_px": [float(fw), float(fh)],
            "escala": W / crop[2], "pecas": pcs, "cena": t["cena"], "falante": t["falante"]}
    json.dump(info, open(D / "info.json", "w"), indent=1)
    print(tid, t["cena"], f"N={N} pad={Np - N}", "crop", crop, f"rosto {fw:.0f}x{fh:.0f}", (D / "in.mp4").stat().st_size)


if __name__ == "__main__":
    so = set(sys.argv[1:])
    for t in LOT["trechos"]:
        if t["lote"] != 1 or t["id"] in EXCLUIR: continue
        if so and t["id"] not in so: continue
        preparar(t)
