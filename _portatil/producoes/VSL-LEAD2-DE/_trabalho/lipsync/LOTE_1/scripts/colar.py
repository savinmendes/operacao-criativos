# -*- coding: utf-8 -*-
"""Cola boca+queixo da saida HeyGen de volta no quadro original e mede.  Uso: python colar.py id [id ...]
Entrada: ../work/<id>/{orig.mp4,in.mp4,out.mp4,info.json,de_real.wav,es.wav}
Saida: ../<id>.mp4 (so video, 720x960, N quadros = timeline nova) e ../work/<id>/chk.txt (checar_lipsync)."""
import sys, json, subprocess, re
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, str(Path(__file__).parent))
from prep import W, H, FPS, ENC_VF, ENC_TAG, gravar, rostos, AQ

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")


def quadros(p, w=W, h=H):
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(p), "-vf",
                           f"scale={w}:{h}:in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int+lanczos,format=bgr24",
                           "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    fr = []; t = w * h * 3
    while True:
        b = pr.stdout.read(t)
        if len(b) < t: break
        fr.append(np.frombuffer(b, np.uint8).reshape(h, w, 3))
    pr.stdout.close(); pr.wait(); return fr


def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    if 0 < n - m <= 2: return fr + [fr[-1]] * (n - m)  # entrada perdeu o ultimo quadro no -shortest: repete o ultimo
    if 0 < m - n <= 2: return fr[:n]
    return [fr[min(m - 1, int(round(i * (m - 1) / max(1, n - 1))))] for i in range(n)]


def colar(tid):
    D = AQ / "work" / tid; I = json.load(open(D / "info.json"))
    N, Np = I["n"], I["n_pad"]; x0, y0, cw, ch = I["crop"]
    orig = quadros(D / "orig.mp4"); inp = quadros(D / "in.mp4"); out = quadros(D / "out.mp4")
    nota = f"out {len(out)} q (esperado {Np})"
    out = reamostrar(out, Np)[:N]; inp = reamostrar(inp, Np)[:N]; orig = orig[:N]
    # pontos do rosto no original (a cada quadro), suavizados
    P = []; ult = None
    for f in orig:
        fs = rostos(f)
        if fs:
            p = max(fs, key=lambda p: np.ptp(p[:, 0])); ult = p
        P.append(ult)
    prim = next((p for p in P if p is not None), None)
    if prim is None: raise SystemExit(f"{tid}: sem rosto")
    P = [p if p is not None else prim for p in P]
    G = []
    for p in P:
        mx, my = (p[13] + p[14])[0] / 2, (p[13] + p[14])[1] / 2
        fw = np.linalg.norm(p[454] - p[234]); fh = np.linalg.norm(p[152] - p[10]); chin = p[152][1]
        G.append([mx, my, fw, fh, chin])
    G = np.array(G); K = 5
    Gs = np.array([G[max(0, i - K // 2):i + K // 2 + 1].mean(0) for i in range(len(G))])
    # correcao de cor: diferenca media saida x entrada fora da boca (no espaco do recorte)
    s = W / cw
    dv = []
    for k in range(0, N, max(1, N // 10)):
        mx, my, fw, fh, chin = Gs[k]
        m = np.ones((H, W), bool)
        cxm, cym = (mx - x0) * s, (my - y0) * s
        cv2.ellipse(m.view(np.uint8), (int(cxm), int(cym + 0.1 * fh * s)), (int(0.6 * fw * s), int(0.55 * fh * s)), 0, 0, 360, 0, -1)
        dv.append((inp[k].astype(np.float32) - out[k].astype(np.float32))[m].mean(0))
    dv = np.mean(dv, 0)
    res = []
    for k in range(N):
        mx, my, fw, fh, chin = Gs[k]
        g = np.clip(out[k].astype(np.float32) + dv, 0, 255)
        Mx = np.float32([[cw / W, 0, x0], [0, ch / H, y0]])
        full = cv2.warpAffine(g, Mx, (W, H), flags=cv2.INTER_AREA if cw < W else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        m = np.zeros((H, W), np.float32)
        cyc = (my + chin) / 2
        cv2.ellipse(m, (int(mx), int(cyc)), (int(0.36 * fw), int(max(0.30 * fh, (chin - my) * 0.5 + 0.12 * fh))), 0, 0, 360, 1.0, -1)
        m = cv2.GaussianBlur(m, (0, 0), max(3, 0.06 * fw))[..., None]
        res.append(np.clip(full * m + orig[k].astype(np.float32) * (1 - m), 0, 255).astype(np.uint8))
    gravar(res, AQ / f"{tid}.mp4", W, H)
    # conferencia
    full = D / "full.mp4"; ori = D / "orig_es.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQ / f"{tid}.mp4"), "-i", str(D / "de_real.wav"), "-c:v", "copy", "-c:a", "aac", "-shortest", str(full)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(D / "orig.mp4"), "-i", str(D / "es.wav"), "-c:v", "copy", "-c:a", "aac", "-shortest", str(ori)], check=True)
    f0 = Gs[N // 2]; rx = int(max(0, f0[0] - f0[2] * 0.8)); ry = int(max(0, f0[1] - f0[3] * 0.9))
    rosto = f"{rx},{ry},{int(f0[2] * 1.6)},{int(f0[3] * 1.5)}"
    r = subprocess.run([sys.executable, str(KIT / "checar_lipsync.py"), str(full), "--audio-novo", str(D / "de_real.wav"),
                        "--original", str(ori), "--audio-original", str(D / "es.wav"), "--rosto", rosto],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    txt = r.stdout + "\n" + nota + f"\ncor dv={dv.round(2).tolist()}\n"
    (D / "chk.txt").write_text(txt, encoding="utf-8")
    m = re.search(r"[íi]ndice de pausa[^0-9\-]*([0-9]+[.,][0-9]+)", txt, re.I)
    idx = float(m.group(1).replace(",", ".")) if m else None
    ver = "APROVADO" if "APROVADO" in txt else ("REPROVADO" if "REPROVADO" in txt else ("AVISO" if "AVISO" in txt else "?"))
    med = "quadro_inteiro"
    if ver != "APROVADO":  # rosto pequeno no quadro: mede tambem no recorte ampliado (saida HeyGen x entrada)
        r2 = subprocess.run([sys.executable, str(KIT / "checar_lipsync.py"), str(D / "out.mp4"), "--audio-novo", str(D / "de.mp3"),
                             "--original", str(D / "in.mp4")], capture_output=True, text=True, encoding="utf-8", errors="replace",
                            env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
        t2 = r2.stdout
        (D / "chk_recorte.txt").write_text(t2, encoding="utf-8")
        m2 = re.search(r"[íi]ndice de pausa[^0-9\-]*([0-9]+[.,][0-9]+)", t2, re.I)
        i2 = float(m2.group(1).replace(",", ".")) if m2 else None
        v2 = "APROVADO" if "APROVADO" in t2 else ("REPROVADO" if "REPROVADO" in t2 else ("AVISO" if "AVISO" in t2 else "?"))
        ordem = {"APROVADO": 0, "AVISO": 1, "REPROVADO": 2, "?": 3}
        if ordem[v2] < ordem[ver]: ver, idx, med = v2, i2, "recorte"
    print(tid, ver, idx, med, nota, "dv", dv.round(1))
    return {"indice": idx, "veredito": ver, "medida": med, "nota": nota}


if __name__ == "__main__":
    R = {}
    for t in sys.argv[1:]:
        try: R[t] = colar(t)
        except Exception as e: print(t, "ERRO", e); R[t] = {"erro": str(e)}
    json.dump(R, open(AQ / "_tmp" / f"colar_{sys.argv[1]}_{len(sys.argv) - 1}.json", "w"), indent=1)
