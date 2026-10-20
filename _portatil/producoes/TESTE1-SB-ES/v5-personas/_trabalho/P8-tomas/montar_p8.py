# -*- coding: utf-8 -*-
"""SB-ES v5 "Humillación" — P8 DON TOMÁS (dulces en el bus) -> v5-personas/SB-ES_HUMILLACION_P8-TOMAS_FICTICIO.mp4
Estrutura (BRIEFING_PERSONAS.md): reportera PiP sobre a briga (Seedance, take único) -> virada sem fala (Kling/imagem, trilha
triste -> esperança) -> reportera R01 -> Tomás (HeyGen + voz off sobre b-roll inédito) -> reportera CTA (setas até o fim).
Toda a janela do post (720x840) é montada quadro a quadro com a matriz bt601 fixa (comum3) e codificada UMA vez; a passada
final só põe a janela sobre a moldura (plate + header), legenda ASS, título, CTA e selo.
Uso: python montar_p8.py [--so-plano]"""
import json, re, subprocess, sys, difflib
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG

AQ = Path(__file__).resolve().parent; RAIZ = AQ.parents[2]; V5 = AQ.parents[1]
M = AQ / "mont"; M.mkdir(exist_ok=True); W = AQ / "w"
G = RAIZ / "_trabalho" / "graficos"; GB = RAIZ / "v3" / "_trabalho" / "final_B"
OUT = V5 / "SB-ES_HUMILLACION_P8-TOMAS_FICTICIO.mp4"
FPS, SR, WW, WH = 30, 48000, 720, 840
WIN_Y = 297
CFG = json.loads((AQ / "cfg.json").read_text(encoding="utf-8"))
TX = CFG["texto"]                      # texto exato do roteiro por bloco
PIP = CFG.get("pip", dict(x=0, y=300, w=304, h=540, xc=284, lado="esq"))


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:2000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=0.0, t=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}"] + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    if len(a) < SR // 2: a = np.concatenate([a, np.zeros((SR // 2 - len(a), 2), np.float32)])
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    raw.unlink(); v = float([x for x in r.stderr.splitlines() if x.strip().startswith("I:")][-1].split()[1]); return max(v, -70.0)


def norm(a, alvo): return a * 10 ** ((alvo - lufs(a)) / 20)


def fade(a, i=0.01, o=0.01):
    ni, no = int(i * SR), int(o * SR)
    if ni: a[:ni] *= np.linspace(0, 1, ni)[:, None]
    if no: a[-no:] *= np.linspace(1, 0, no)[:, None]
    return a


def dims(p):
    o = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", p]).stdout
    return tuple(int(x) for x in o.strip().split(","))


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def texto_roteiro(P, txt):
    """troca as palavras (whisper/alinhamento) pelas do roteiro mantendo os tempos"""
    R = txt.split()
    if len(R) == len(P): return [dict(p, w=r) for p, r in zip(P, R)]
    a = [limpa(p["w"]) for p in P]; b = [limpa(r) for r in R]; out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal": out += [dict(P[i1 + k], w=R[j1 + k]) for k in range(i2 - i1)]
        elif j2 > j1 and i2 > i1:
            t0, t1 = P[i1]["ini"], P[i2 - 1]["fim"]; L = [len(limpa(R[j])) + 1 for j in range(j1, j2)]; s = sum(L); t = t0
            for k, j in enumerate(range(j1, j2)): d = (t1 - t0) * L[k] / s; out.append(dict(w=R[j], ini=round(t, 3), fim=round(t + d, 3))); t += d
        elif j2 > j1:
            t = out[-1]["fim"] if out else P[0]["ini"]
            for j in range(j1, j2): out.append(dict(w=R[j], ini=t, fim=t + 0.01))
    return out


# ------------------------------------------------------------------ quadros da janela
def cover(f, cy=0.5, cx=0.5, z=1.0):
    """BGR qualquer -> 720x840 (cover), recorte em cx/cy, zoom extra z (centrado no recorte)"""
    h, w = f.shape[:2]; s = max(WW / w, WH / h) * z
    sw, sh = max(WW, round(w * s)), max(WH, round(h * s))
    g = cv2.resize(f, (sw, sh), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LANCZOS4)
    x0 = int(round((sw - WW) * cx)); y0 = int(round((sh - WH) * cy))
    return g[y0:y0 + WH, x0:x0 + WW]


def ler_video(p, ss, n, cy=0.5, cx=0.5, z0=1.0, z1=1.0):
    """n quadros a 30 fps a partir de ss (s); a fonte é reamostrada a 30 fps pelo ffmpeg (sem mexer na cor: comum3 lê bt601)"""
    w, h = dims(p); tmp = M / (Path(p).stem + f"_{ss:.2f}_30.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", p, "-vf", f"fps={FPS}", "-frames:v", n + 2, "-an",
         "-c:v", "libx264", "-crf", "8", "-preset", "fast", tmp])
    fr = list(quadros(tmp, 0, n, w, h))
    tmp.unlink(missing_ok=True)                 # disco cheio: o temporário não é reaproveitado
    if len(fr) < n: print(f"   !!! {Path(p).name}: só {len(fr)}/{n} quadros a partir de {ss:.2f}"); fr += [fr[-1]] * (n - len(fr))
    return [cover(f, cy, cx, z0 + (z1 - z0) * k / max(1, n - 1)) for k, f in enumerate(fr)]


def ler_img(p, n, cy=0.5, cx=0.5, z0=1.0, z1=1.06):
    f = cv2.imread(str(p), cv2.IMREAD_COLOR)
    return [cover(f, cy, cx, z0 + (z1 - z0) * k / max(1, n - 1)) for k in range(n)]


def alfa(f):          # chroma verde + despill (compor_reporter.py)
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def zoom_ponto(f, z, c):
    cw, ch = WW / z, WH / z; x0 = min(max(c[0] - cw / 2, 0), WW - cw); y0 = min(max(c[1] - ch / 2, 0), WH - ch)
    Mx = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]])
    return cv2.warpAffine(f, Mx, (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


# ------------------------------------------------------------------ segmentos
def plano():
    """lista de segmentos com tempo final (T0), duração (n quadros), palavras (tempo final) e áudio"""
    S = []; t = 0.0
    for sg in CFG["segmentos"]:
        s = dict(sg)
        if s["tipo"] == "abertura":
            d = s["dur"]
        elif s.get("voz"):
            j = json.loads((AQ / s["voz"]).with_suffix(".json").read_text(encoding="utf-8"))
            vs = s.get("ss", 0.0) if s["tipo"] == "video" else 0.0
            s["palavras"] = [dict(p, ini=p["ini"] - vs, fim=p["fim"] - vs) for p in texto_roteiro(j["palavras"], TX[s["bloco"]])]
            d = j["dur"] - s.get("corta_fim", 0.0) - vs
        else:
            d = s["dur"]
        s["n"] = int(round(d * FPS)); s["T0"] = round(t, 4); t += s["n"] / FPS; S.append(s)
    return S, round(t, 4)


def quadros_seg(s):
    n = s["n"]; tp = s["tipo"]
    if tp == "abertura": return abertura(s)
    if tp == "img": return ler_img(AQ / s["src"], n, s.get("cy", 0.5), s.get("cx", 0.5), *s.get("zoom", [1.0, 1.06]))
    return ler_video(AQ / s["src"], s.get("ss", 0.0), n, s.get("cy", 0.5), s.get("cx", 0.5), *s.get("zoom", [1.0, 1.0]))


def abertura(s):
    n = s["n"]; fr = ler_video(AQ / s["src"], s.get("ss", 0.0), n, s.get("cy", 0.5), s.get("cx", 0.5))
    z, zc, za = s["punch"]["z"], s["punch"]["c"], s["punch"]["ate"]
    t30 = M / "pip30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", AQ / s["pip"], "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    pw, ph = dims(t30)
    tk = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(t30, 0, None, pw, ph)]
    NP = min(len(tk), int(round(s["pip_ate"] * FPS))); NF = 4; out = []
    x0, y0, w, h = PIP["x"], PIP["y"], PIP["w"], PIP["h"]
    for q, o in enumerate(fr):
        if q < round(za * FPS): o = zoom_ponto(o, z, zc)
        if q < NP:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            hh = min(h, WH - y0); A[y0:y0 + hh, x0:x0 + w] = a[:hh]; F[y0:y0 + hh, x0:x0 + w] = fg[:hh]
            if PIP.get("lado") == "dir": A[:, :PIP["xc"]] = 0
            else: A[:, PIP["xc"]:] = 0
            if q >= NP - NF: A *= 1 - (q - (NP - NF) + 1) / (NF + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    return out


def janela(S, total):
    N = int(round(total * FPS)); out = M / "janela.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-frames:v", str(N), str(out)], stdin=subprocess.PIPE)
    k = 0
    for s in S:
        fr = quadros_seg(s)
        for f in fr[:s["n"]]: ff.stdin.write(np.ascontiguousarray(f).tobytes()); k += 1
        print(f"  {s['id']:6s} {s['T0']:6.2f}s {s['n']}q", flush=True)
    ff.stdin.close(); ff.wait(); print("janela", k, "/", N)


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)) + SR; mix = np.zeros((N, 2), np.float32)
    def pos(a, t0):
        s0 = int(round(t0 * SR)); m = min(len(a), N - s0); mix[s0:s0 + m] += a[:m]
    for s in S:
        if s["tipo"] == "abertura":
            d = s["n"] / FPS; a = norm(load(AQ / s.get("audio_src", s["src"]), s.get("ss", 0.0), d), s.get("lufs", -16))
            t = np.arange(len(a)) / SR; da = s["pip_fala_fim"] + 0.05
            a *= (10 ** (np.interp(t, [0, da, da + 0.3, 1e9], [s.get("duck_db", -5)] * 2 + [0, 0]) / 20)).astype(np.float32)[:, None]
            pos(fade(a, 0.01, 0.25), s["T0"])
            v = norm(load(AQ / s["pip_voz"]), -15); pos(fade(v), s["T0"])
        elif s.get("voz"):
            v = norm(load(AQ / s["voz"]), -15); vs = s.get("ss", 0.0) if s["tipo"] == "video" else 0.0
            v = v[int(vs * SR):int((vs + s["n"] / FPS) * SR)]; pos(fade(v, 0.01, 0.04), s["T0"])
    by = {s["id"]: s for s in S}
    # trilha triste na virada -> esperança, abaixando sob a reportera
    tr = CFG["trilha"]; t4 = by[tr["triste_em"]]["T0"]; t5 = by[tr["esperanca_em"]]["T0"]; tR = by[tr["abaixa_em"]]["T0"]
    tri = norm(load(GB / "trilha" / "triste_1.mp3"), -19); nt = min(len(tri), int((t5 - t4 + 0.9) * SR)); tri = tri[:nt].copy()
    xf = int(0.9 * SR); tri[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]; tri[-xf:] *= np.linspace(1, 0, xf)[:, None]; pos(tri, t4)
    es = norm(load(GB / "trilha" / "esperanca_1.mp3"), -20); ne = min(len(es), int((tR + 2.4 - t5) * SR)); es = es[:ne].copy()
    es[:xf] *= np.linspace(0, 1, xf)[:, None]; env = np.ones(ne, np.float32); i0 = int((tR - 0.2 - t5) * SR)
    if 0 < i0 < ne: env[i0:] = np.linspace(1, 10 ** (-12 / 20), ne - i0)
    es *= env[:, None]; es[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))[:, None]; pos(es, t5)
    # ambiente de rua (ElevenLabs SFX) sob as cenas na calçada
    rua = norm(load(AQ / "voz" / "rua.mp3"), CFG.get("rua_lufs", -33))
    for s in S:
        if s.get("rua"):
            d = s["n"] / FPS; k = int(d * SR); off = int((s["T0"] * 7.3) % 12 * SR)
            seg = np.concatenate([rua, rua])[off:off + k].copy(); pos(fade(seg, 0.15, 0.15), s["T0"])
    mix = mix[:int(round(total * SR))]; mix[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"])
    raw.unlink(); print("audio ok")


# ------------------------------------------------------------------ legenda (estilo v4)
FS, Y_POST, Y_CTA = 64, 1072, 840
MAXP, MAXC = 3, 18
JUNTAR = [(["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["don", "tomás"], "don tomás"), (["juan", "méndez"], "juan méndez")]


def palavras_tl(S):
    out = []
    for s in S:
        for p in s.get("palavras", []):
            w = limpa(p["w"])
            if w: out.append(dict(w=w, raw=p["w"], ini=s["T0"] + p["ini"], fim=s["T0"] + p["fim"], linha=p.get("linha", s["id"]), seg_fim=s["T0"] + s["n"] / FPS))
    res, k = [], 0
    while k < len(out):
        for seq, rep in JUNTAR:
            if [x["w"] for x in out[k:k + len(seq)]] == seq:
                res.append(dict(out[k], w=rep, fim=out[k + len(seq) - 1]["fim"], raw=out[k + len(seq) - 1]["raw"])); k += len(seq); break
        else: res.append(out[k]); k += 1
    return res


def blocos(Wd):
    B, cur = [], []
    for w in Wd:
        cand = cur + [w]; txt = " ".join(x["w"] for x in cand)
        if cur and (len(cand) > MAXP or len(txt) > MAXC or cur[-1]["linha"] != w["linha"] or w["ini"] - cur[-1]["fim"] > 0.6):
            B.append(cur); cand = [w]
        cur = cand
        if re.search(r"[.!?…:;]$", w["raw"]) or (w["raw"].endswith(",") and len(cur) >= 2): B.append(cur); cur = []
    if cur: B.append(cur)
    return B


def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(S, total, cta_t):
    B = blocos(palavras_tl(S)); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total, b[-1]["seg_fim"] if b[-1]["linha"] in ("TOMAS_B",) else total); y = Y_CTA if ini >= cta_t - 0.1 else Y_POST
        for j, w in enumerate(b):
            a = ini if j == 0 else max(ini, w["ini"] - 0.04); e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + x["w"] for jj, x in enumerate(b))
            pop = r"\fscx85\fscy85\t(0,80,\fscx104\fscy104)\t(80,140,\fscx100\fscy100)" if j == 0 else ""
            ev.append(f"Dialogue: 1,{ts(a)},{ts(e)},L,,0,0,0,,{{\\an5\\pos(360,{y}){pop}}}{txt}")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins SemiBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,2,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    (M / "leg.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    json.dump([dict(ini=round(b[0]["ini"], 3), texto=" ".join(x["w"] for x in b)) for b in B], open(M / "leg_blocos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)


# ------------------------------------------------------------------ final
def video(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    T = 0.0; ti = CFG.get("titulo_ate", 3.0)
    ins = ["-loop", "1", "-framerate", "30", "-t", f"{total + 1:.3f}", "-i", GB / "graficos" / "plate.png",
           "-i", "janela.mp4", "-i", "mix.wav"]
    pngs = [G / "header.png", AQ / "graficos" / "titulo_gancho.png", G / "cta_txt.png", G / "cta_setas.png", G / "selo.png"]
    for p in pngs: ins += ["-loop", "1", "-framerate", "30", "-t", f"{total + 1:.3f}", "-i", p]
    fc = [f"[0:v]fps={FPS},format=yuv420p[pl]", f"[1:v]setpts=N/({FPS}*TB)[jw]", f"[pl][jw]overlay=0:{WIN_Y}:format=auto:shortest=0[a0]",
          "[3:v]format=rgba[h]", "[4:v]format=rgba[ti]", "[5:v]format=rgba[ct]", "[6:v]format=rgba[cs]", "[7:v]format=rgba[se]",
          "[a0][h]overlay=0:0:format=auto[a1]",
          f"[a1][ti]overlay=0:0:format=auto:enable='lt(t,{ti:.3f})'[a2]",
          "[a2]ass=leg.ass:fontsdir=fonts[a3]",
          f"[a3][ct]overlay=0:-22:format=auto:enable='gte(t,{cta_t - 1 / 60:.4f})'[a4]",
          f"[a4][cs]overlay=0:'-37+10*sin(2*PI*1.4*t)':format=auto:enable='gte(t,{cta_t - 1 / 60:.4f})'[a5]",
          "[a5][se]overlay=0:0:format=auto,format=yuv420p[v]"]
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    run(["ffmpeg", "-v", "error", "-y", "-reinit_filter", "0", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "2:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS,
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{total:.2f}s")


def folha(total):
    fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    n = 30
    for k in range(n):
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(k + 0.5) * total / n:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=240:427", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", "tile=10x3", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


def narracion(S, total):
    def mmss(t): return f"{int(t // 60):02d}:{int(t % 60):02d}"
    lin = []
    for s in S:
        for b, quem in s.get("falas", []):
            P = [p for p in s.get("palavras", []) if p.get("linha", s["id"]) == b] or s.get("palavras", [])
            t = s["T0"] + (P[0]["ini"] if P else 0); lin.append(f"[{mmss(t)}] {quem}: {TX[b]}")
        if s.get("nota"): lin.append(f"[{mmss(s['T0'])}] ({s['nota']})")
    cab = f"""NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})
Lote "Humillación" (v5 personas), P8 · DON TOMÁS (vendedor de dulces en el bus). Personajes ficticios: REPORTERA, CHOFER, DON TOMÁS.
Sello "VIDEO FICTICIO" arriba a la derecha y moldura de post "Fe en Noticias" durante todo el video. "(voz en off)" = narración sobre b-roll, sin rostro.
Voces: reportera Gabriela (ElevenLabs hHjbwzYZW17oh0p05AKv) · chofer y don Tomás en la pelea = audio nativo del Seedance · don Tomás en la entrevista = ElevenLabs "Oscar G - Calm & Tranquil" (sJYGLUA6m2su09XOMEb8, acento colombiano).
Título 0–3 s: "LO ECHARON DEL BUS POR SU FE… / AL DÍA SIGUIENTE PASÓ ESTO". CTA único al final (flechas TOCA «VER MÁS» desde el CTA hasta el último cuadro).
"""
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


if __name__ == "__main__":
    S, total = plano()
    # palavras da abertura: R00 (alinhamento ElevenLabs) + falas do Seedance (whisper do take)
    for s in S:
        if s["tipo"] == "abertura":
            r0 = json.loads((AQ / s["pip_voz"]).with_suffix(".json").read_text(encoding="utf-8"))["palavras"]
            P = [dict(p, linha="R00") for p in texto_roteiro(r0, TX["R00"])]
            wh = json.loads((AQ / s["whisper"]).read_text(encoding="utf-8")); ss = s.get("ss", 0.0)
            for b in ("CHOFER", "TOMAS_B"):
                a, e = s["janelas"][b]; Pw = [dict(w=x["w"], ini=x["ini"] - ss, fim=x["fim"] - ss) for x in wh if a <= x["ini"] < e]
                P += [dict(p, linha=b) for p in texto_roteiro(Pw, TX[b])]
            s["palavras"] = P
    cta = next(s for s in S if s["id"] == "CTA"); cta_t = cta["T0"]
    for s in S: print(f"{s['T0']:7.2f} +{s['n'] / FPS:5.2f} {s['id']:6s} {s['tipo']:8s} {s.get('src', '')}")
    print("TOTAL", total, "CTA", cta_t)
    json.dump(dict(total=total, cta_t=cta_t, segmentos=S), open(AQ / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--so-plano" in sys.argv: sys.exit()
    legenda(S, total, cta_t)
    if "--so-final" not in sys.argv: janela(S, total); audio(S, total)
    video(total, cta_t); print(narracion(S, total)); folha(total)
