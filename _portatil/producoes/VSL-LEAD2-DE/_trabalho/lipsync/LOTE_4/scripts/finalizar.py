# -*- coding: utf-8 -*-
"""Pos-processamento do LOTE 4. Uso: python finalizar.py jobs.json [ids...]
jobs.json: {"L224": {"job_id": "...", "url": "..."}}. Baixa out/raw_<id>.mp4, gera LOTE_4/<id>.mp4 (so video, N quadros
da timeline nova, leitura/gravacao com matriz bt601/tv fixa), mede com checar_lipsync.py e grava relatorio.json."""
import sys, json, subprocess, re, os
from pathlib import Path
import numpy as np, cv2

L = Path(__file__).resolve().parents[1]
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
SRC = r"C:\Users\PICHAU\Downloads\Lead 2.mp4"
ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
COR = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]


def quadros(p, w, h):
    """Quadros em YUV 4:4:4 (sem conversao de matriz: os valores Y/U/V saem iguais aos do arquivo)."""
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(p), "-vf", "format=yuv444p", "-fps_mode", "passthrough",
                           "-f", "rawvideo", "-pix_fmt", "yuv444p", "-"], stdout=subprocess.PIPE)
    t = w * h * 3
    while True:
        b = pr.stdout.read(t)
        if len(b) < t:
            break
        yield np.frombuffer(b, np.uint8).reshape(3, h, w).transpose(1, 2, 0).copy()
    pr.stdout.close(); pr.wait()


def yuv2rgb(f):
    """So para o detector de rosto (aproximacao bt601 tv)."""
    y = f[..., 0].astype(np.float32) - 16; u = f[..., 1].astype(np.float32) - 128; v = f[..., 2].astype(np.float32) - 128
    r = 1.164 * y + 1.596 * v; g = 1.164 * y - 0.392 * u - 0.813 * v; b = 1.164 * y + 2.017 * u
    return np.clip(np.stack([r, g, b], -1), 0, 255).astype(np.uint8)


def nq(p):
    return int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries",
                                        "stream=nb_read_frames", "-of", "csv=p=0", str(p)]))


def tam(p):
    s = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                                 "-of", "csv=p=0", str(p)]).decode().strip().split(",")
    return int(s[0]), int(s[1])


def enc(frames_iter, out, n):
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv444p", "-s", "720x960", "-r", "30",
                           "-i", "-", "-vf", "format=yuv420p", "-frames:v", str(n), "-c:v", "libx264", "-crf", "14",
                           "-preset", "medium", *ENC_TAG, "-an", str(out)], stdin=subprocess.PIPE)
    k = 0; last = None
    for f in frames_iter:
        if k >= n:
            break
        pr.stdin.write(np.ascontiguousarray(f.transpose(2, 0, 1)).tobytes()); last = f; k += 1
    while k < n and last is not None:
        pr.stdin.write(np.ascontiguousarray(last.transpose(2, 0, 1)).tobytes()); k += 1
    pr.stdin.close(); pr.wait()
    return k


def transcodar(raw, out, n):
    """Saida inteira do HeyGen: so recodifica (YUV intacto), N quadros, sem audio, etiqueta bt709/tv."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-vf", "tpad=stop_mode=clone:stop=10", "-frames:v", str(n),
                    "-an", "-sn", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", *ENC_TAG,
                    str(out)], check=True)


def orig_esticado(t, out):
    f = t["fator"]; a0, a1 = t["orig_ini"], t["orig_fim"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a0:.3f}", "-t", f"{a1 - a0 + 0.5:.3f}", "-i", SRC, "-vf",
                    f"setpts=(PTS-STARTPTS)*{f},fps=30,tpad=stop_mode=clone:stop=10", "-frames:v", str(t["N"]), "-an",
                    "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, str(out)], check=True)


def colar_crop(t, raw, out):
    """Trecho de rosto pequeno: base = original esticado (N quadros). Nos envN primeiros quadros cola so boca+queixo do
    recorte 2x devolvido pelo HeyGen (reduzido de volta, elipse suave, cor ajustada pelo anel em volta da boca)."""
    import mediapipe as mp
    from mediapipe.tasks import python as mpp
    from mediapipe.tasks.python import vision
    base = L / "out" / f"orig_{t['id']}.mp4"
    if not base.exists():
        orig_esticado(t, base)
    x, y, w, h = t["crop"]
    g = list(quadros(raw, 2 * w, 2 * h)); B = list(quadros(base, 720, 960))
    mod = str(Path.home() / ".cache" / "kit-edicao" / "face_landmarker.task")
    det = vision.FaceLandmarker.create_from_options(
        vision.FaceLandmarkerOptions(base_options=mpp.BaseOptions(model_asset_path=mod), num_faces=1))
    pts = []
    for k in range(min(len(g), t["envN"])):
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(yuv2rgb(g[k]))))
        if r.face_landmarks:
            p = r.face_landmarks[0]; H, W = g[k].shape[:2]
            pts.append(((p[13].x + p[14].x) / 2 * W, (p[13].y + p[14].y) / 2 * H,
                        abs(p[454].x - p[234].x) * W, abs(p[152].y - p[10].y) * H))
        else:
            pts.append(None)
    ok = np.array([q for q in pts if q is not None]); med = np.median(ok, 0)
    frames = []
    for k in range(t["N"]):
        b = B[min(k, len(B) - 1)].astype(np.float32)
        if k < t["envN"] and k < len(g):
            mx, my = (pts[k] or med)[:2]; fw, fh = med[2], med[3]
            m = np.zeros((2 * h, 2 * w), np.float32)
            cv2.ellipse(m, (int(mx), int(my + 0.06 * fh)), (int(0.30 * fw), int(0.24 * fh)), 0, 0, 360, 1.0, -1)
            m = cv2.GaussianBlur(m, (0, 0), max(3, 0.06 * fw))
            gs = cv2.resize(g[k], (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
            ms = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA)[..., None]
            reg = b[y:y + h, x:x + w]
            ring = (ms[..., 0] > 0.02) & (ms[..., 0] < 0.5)
            if ring.sum() > 50:
                gs = gs + (reg[ring].mean(0) - gs[ring].mean(0))
            b[y:y + h, x:x + w] = gs * ms + reg * (1 - ms)
        frames.append(np.clip(b, 0, 255).astype(np.uint8))
    enc(iter(frames), out, t["N"])


def checar(out, t):
    de = L / "in" / f"de_{t['id']}.mp3"
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    if t["crop"]:
        cmd = [str(L / "out" / f"orig_{t['id']}.mp4"), "--sem-audio-original"]
    else:
        cmd = [str(L / "in" / f"es_{t['id']}.mp4")]
    r = subprocess.run([sys.executable, str(L / "scripts" / "medir.py"), str(out), str(de), *cmd],
                       capture_output=True, text=True, env=env, encoding="utf-8", errors="replace")
    linha = [l for l in r.stdout.splitlines() if l.startswith("{")]
    return json.loads(linha[-1]) if linha else {"status": "ERRO", "motivo": r.stderr[-400:]}


def luma(p, k=10):
    fr = []
    for i, f in enumerate(quadros(p, *tam(p))):
        if i % 30 == 0:
            fr.append(f[..., 0].mean())
        if len(fr) >= k:
            break
    return float(np.mean(fr))


def main():
    jobs = json.load(open(sys.argv[1])); so = set(sys.argv[2:])
    P = {t["id"]: t for t in json.load(open(L / "plano.json", encoding="utf-8"))}
    (L / "out").mkdir(exist_ok=True); R = L / "relatorio.json"
    rel = {r["id"]: r for r in json.load(open(R, encoding="utf-8"))} if R.exists() else {}
    for i, j in jobs.items():
        if so and i not in so:
            continue
        t = P[i]; raw = L / "out" / f"raw_{i}.mp4"
        if i in rel and (L / f"{i}.mp4").exists():
            continue
        if not raw.exists() or raw.stat().st_size == 0:
            tmp = raw.with_suffix(".tmp")
            code = subprocess.run(["curl", "-s", "-L", "-o", str(tmp), "-w", "%{http_code}", j["url"]], capture_output=True, text=True).stdout
            ok = code == "200" and subprocess.run(["ffprobe", "-v", "error", str(tmp)], capture_output=True).returncode == 0
            if not ok:
                tmp.unlink(missing_ok=True); continue
            tmp.replace(raw)
        out = L / f"{i}.mp4"
        if t["crop"]:
            colar_crop(t, raw, out)
        else:
            assert tam(raw) == (720, 960), tam(raw)
            transcodar(raw, out, t["N"])
        n = nq(out); m = checar(out, t)
        idx = m.get("indice"); curto = idx is None and m.get("indice_curto") is not None
        ix = idx if idx is not None else m.get("indice_curto")
        mudou = m.get("mudou")
        if mudou is not None and mudou < 0.30:
            st = "usar_broll"
        elif ix is None:
            st = "aviso"
        else:
            st = "ok" if ix <= 0.6 else ("aviso" if (curto or ix <= 0.75) else "usar_broll")
        obs = []
        if t["crop"]:
            obs.append("pulpito: rosto pequeno -> recorte 2x + colagem de boca/queixo so em 0-%.2fs do trecho; depois a mao "
                       "cobre o rosto (sinal da cruz) e entra b-roll (crucifixo/estatua), sem lipsync ali" % (t["envN"] / 30))
        if curto:
            obs.append("voz DE sem pausa >= 8 quadros: indice medido em pausas curtas (>= 4 quadros, %s q); acima de 0,6 vira aviso (boca entreaberta em pausa de 0,1-0,2 s e natural), conferir a olho" % m.get("n_pausa_curto"))
        elif ix is None:
            obs.append("sem pausa nem curta na voz DE: indice nao calculado (corr. boca x DE %.2f, x ES %s)" % (
                m.get("corr_novo") or 0, "%.2f" % m["corr_original"] if m.get("corr_original") is not None else "-"))
        o = L / "out" / f"orig_{i}.mp4"
        d_l = luma(out) - (luma(o) if t["crop"] else luma(L / "in" / f"es_{i}.mp4"))
        rel[i] = {"id": i, "job_id": j["job_id"], "indice": None if ix is None else round(ix, 3),
                  "indice_tipo": "oficial" if idx is not None else ("pausas_curtas" if curto else None),
                  "status": st, "veredito_kit": m.get("status"), "mudou": None if mudou is None else round(mudou, 2),
                  "corr_novo": m.get("corr_novo"), "corr_original": m.get("corr_original"),
                  "quadros": n, "esperado": t["N"], "dif_luma": round(d_l, 2), "obs": "; ".join(obs)}
        ver = m.get("status")
        print(i, n, t["N"], rel[i]["indice"], rel[i]["indice_tipo"], ver, rel[i]["mudou"], st, rel[i]["dif_luma"], flush=True)
        json.dump(sorted(rel.values(), key=lambda r: r["id"]), open(R, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


main()
