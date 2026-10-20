# -*- coding: utf-8 -*-
"""Montagem P4 JULIO (SB-ES Humillación v5) -> v5-personas/SB-ES_HUMILLACION_P4-JULIO_FICTICIO.mp4 (+ _frames.jpg, _narracion.txt)
Estrutura (BRIEFING_PERSONAS.md): briga Seedance com a REPORTERA em PiP (0-~5 s) + zoom 130 % + título -> virada sem fala
(mãos/terço, obra parada, homens com plantas, equipe) com trilha triste->esperança -> REPORTERA (R01) -> JULIO entrevistado
(J1, J2 voz off sobre b-roll noturno, J3, P1-P3) -> REPORTERA CTA (setas até o fim). Tudo dentro da moldura do post.
Cor: leitura/gravação bt601/tv fixa (comum3). Uso: python montar.py [--sem-final]"""
import sys, json, re, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG

AQ = Path(__file__).resolve().parent; RAIZ = AQ.parents[2]; V5 = AQ.parents[1]
G = RAIZ / "_trabalho" / "graficos"; PLATE = RAIZ / "v3" / "_trabalho" / "final_B" / "graficos" / "plate.png"
M = AQ / "mont"; M.mkdir(exist_ok=True); T = AQ / "takes"; I = AQ / "img"; VZ = AQ / "voz"; TR = AQ / "trilha"
OUT = V5 / "SB-ES_HUMILLACION_P4-JULIO_FICTICIO.mp4"
FPS, SR = 30, 48000
WY, WW, WH = 297, 720, 840
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
PIP = dict(x=0, y=300, w=304, h=540, xc=284); NFADE = 4
FS, Y_POST, Y_CTA, MAXP, MAXC = 64, 1072, 840, 3, 18

R00 = "Imágenes impactantes: un albañil fue humillado por el dueño de la obra… por su fe."
TXT = {
    "DUENO": "¿No crees en Dios? ¡Que Él te pague entonces!",
    "JULIOB": "Patrón, yo trabajé todo el mes. Por favor, págueme lo que es justo.",
    "R01": "Al día siguiente, a don Julio le ofrecieron la obra más grande de su vida.",
    "J1": "Esa noche volví caminando a casa, con las manos vacías después de un mes de trabajo.",
    "J2": "Ya no sabía qué decirle a mi esposa. Mi hermano me mandó la transmisión del padre Juan Méndez.",
    "J3": "La hice esa misma noche, como él enseña. Al otro día, me llamó un ingeniero que había visto el video.",
    "P1": "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche.",
    "P2": "Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito…",
    "P3": "y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?",
    "R02": "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo.",
}
NOME = {"R00": "REPORTERA (en PiP)", "DUENO": "DUEÑO DE LA OBRA", "JULIOB": "DON JULIO", "R01": "REPORTERA", "J1": "DON JULIO",
        "J2": "DON JULIO (voz en off)", "J3": "DON JULIO", "P1": "DON JULIO", "P2": "DON JULIO", "P3": "DON JULIO", "R02": "REPORTERA"}
CFG = json.loads((AQ / "cfg.json").read_text(encoding="utf-8"))


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
    raw.unlink(); v = float([x for x in r.stderr.splitlines() if x.strip().startswith("I:")][-1].split()[1]); return v if v > -70 else -70.0


def norm(a, alvo): return a * 10 ** ((alvo - lufs(a)) / 20)


def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def tam(p):
    o = run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", p]).stdout.strip().split(",")
    return int(o[0]), int(o[1])


# ------------------------------------------------------------------ janela 720x840
def cobrir(f, cy=0.5, z=1.0, cx=0.5):
    """escala para cobrir 720x840 (com zoom z) e recorta; cy/cx = centro relativo do recorte"""
    h, w = f.shape[:2]; s = max(WW / w, WH / h) * z
    nw, nh = int(round(w * s)), int(round(h * s))
    g = cv2.resize(f, (nw, nh), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LANCZOS4)
    x0 = int(np.clip(cx * nw - WW / 2, 0, nw - WW)); y0 = int(np.clip(cy * nh - WH / 2, 0, nh - WH))
    return g[y0:y0 + WH, x0:x0 + WW]


def alfa(f):
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def to30(p, tag):
    o = M / f"{tag}_30.mp4"
    if not o.exists() or o.stat().st_mtime < Path(p).stat().st_mtime:
        run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", o])
    return o


def frames_seg(s):
    """gera os quadros 720x840 do segmento"""
    n = s["n"]
    if s["tipo"] == "img":
        im = cv2.imread(str(AQ / s["file"])); z0, z1 = s.get("z", (1.0, 1.07))
        for k in range(n):
            yield cobrir(im, s.get("cy", 0.5), z0 + (z1 - z0) * k / max(1, n - 1), s.get("cx", 0.5))
        return
    src = to30(AQ / s["file"], s["id"]); w, h = tam(src); q0 = int(round(s["ini"] * FPS)); k = 0; last = None
    for f in quadros(src, q0, n, w, h):
        last = cobrir(f, s.get("cy", 0.5), s.get("z", 1.0), s.get("cx", 0.5)); yield last; k += 1
    while k < n: yield last; k += 1            # (não deve acontecer: conferido no fim)


def briga(s):
    """take Seedance + zoom 130 % nos 2 primeiros s + PiP da reportera (HeyGen fundo verde)"""
    src = to30(AQ / s["file"], "BRIGA"); w, h = tam(src); n = s["n"]
    pip = [cv2.resize(f, (PIP["w"], PIP["h"]), interpolation=cv2.INTER_AREA) for f in quadros(to30(AQ / CFG["pip"]["file"], "PIP"), 0, None, *tam(to30(AQ / CFG["pip"]["file"], "PIP")))]
    NP = min(len(pip), int(round(CFG["pip"]["ate"] * FPS))); QS = NP - NFADE; Z = s.get("zoom_ini", 1.3); ZQ = int(s.get("zoom_ate", 2.0) * FPS)
    for q, f in enumerate(quadros(src, int(round(s["ini"] * FPS)), n, w, h)):
        o = cobrir(f, s.get("cy", 0.5))
        if q < ZQ:
            cw, ch = WW / Z, WH / Z; zx, zy = s.get("zc", (360, 420))
            x0 = min(max(zx - cw / 2, 0), WW - cw); y0 = min(max(zy - ch / 2, 0), WH - ch)
            o = cv2.warpAffine(o, np.float32([[Z, 0, -x0 * Z], [0, Z, -y0 * Z]]), (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
        if q < NP:
            fg, a = alfa(pip[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            y0, x0, pw, ph = PIP["y"], PIP["x"], PIP["w"], PIP["h"]; hh = min(ph, WH - y0)
            A[y0:y0 + hh, x0:x0 + pw] = a[:hh]; F[y0:y0 + hh, x0:x0 + pw] = fg[:hh]; A[:, PIP["xc"]:] = 0
            if q >= QS: A *= 1 - (q - QS + 1) / (NFADE + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        yield o


def plano():
    S = []; t = 0.0
    for s in CFG["segs"]:
        s = dict(s)
        if s["tipo"] in ("video", "briga"):
            d = s["fim"] - s["ini"]
        elif s["tipo"] == "img":
            d = s["dur"]
        s["n"] = int(round(d * FPS)); s["T0"] = t; t += s["n"] / FPS; S.append(s)
    return S, t


def render_corpo(S, total):
    plate = cv2.imread(str(PLATE)); N = int(round(total * FPS))
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-x264-params", "keyint=60", *ENC_TAG,
                           "-frames:v", str(N), str(M / "corpo.mp4")], stdin=subprocess.PIPE)
    k = 0
    for s in S:
        gen = briga(s) if s["tipo"] == "briga" else frames_seg(s); c = 0
        for f in gen:
            fr = plate.copy(); fr[WY:WY + WH] = f; ff.stdin.write(fr.tobytes()); c += 1; k += 1
        print(f"  {s['id']:7s} T0={s['T0']:6.2f} {c}/{s['n']} q", flush=True)
        if c != s["n"]: print("   !!! quadros faltando", s["id"]); sys.exit(1)
    ff.stdin.close(); ff.wait(); return k


# ------------------------------------------------------------------ áudio
def mix(S, total):
    N = int(round(total * SR)); voz = np.zeros((N, 2), np.float32); bg = np.zeros((N, 2), np.float32)
    def pos(buf, a, t0, fd=0.02):
        n = min(len(a), N - int(t0 * SR)); a = a[:n].copy(); f = int(fd * SR)
        if f and n > 2 * f: a[:f] *= np.linspace(0, 1, f)[:, None]; a[-f:] *= np.linspace(1, 0, f)[:, None]
        s0 = int(round(t0 * SR)); buf[s0:s0 + n] += a
    for s in S:
        d = s["n"] / FPS
        if s["tipo"] == "briga":
            a = norm(load(AQ / s["file"], s["ini"], d), -16); fim = CFG["pip"]["voz_fim"] + 0.05
            tt = np.arange(len(a)) / SR; a *= (10 ** (np.interp(tt, [0, fim, fim + 0.3, 1e9], [-5, -5, 0, 0]) / 20)).astype(np.float32)[:, None]
            k = int(0.15 * SR); a[-k:] *= np.linspace(1, 0, k)[:, None]
            pos(voz, a, s["T0"]); pos(voz, norm(load(VZ / "R00.wav"), -15), s["T0"])
        if s.get("voz"):
            pos(voz, norm(load(VZ / f"{s['voz']}.wav", s.get("voz_ini", 0.0)), -15), s["T0"] + s.get("voz_off", 0.0))
    # trilha da virada: triste (MANOS+PARADA) -> esperança (PLANOS..R01 início)
    tv = {s["id"]: s for s in S}
    tri = norm(load(TR / "triste_1.mp3"), -19); esp = norm(load(TR / "esperanca_1.mp3"), -19)
    t_tri = tv["MANOS"]["T0"]; t_esp = tv["PLANOS"]["T0"] - 0.4
    ntri = int((t_esp + 0.6 - t_tri) * SR); tri = tri[:ntri]; f = int(0.6 * SR); tri[-f:] *= np.linspace(1, 0, f)[:, None]
    pos(bg, tri, t_tri, 0.15)
    fim_esp = tv["R01"]["T0"] + 1.6; ne = int((fim_esp - t_esp) * SR); e = esp[:ne].copy()
    tt = np.arange(len(e)) / SR; dk = tv["R01"]["T0"] - t_esp
    e *= (10 ** (np.interp(tt, [0, 0.4, dk - 0.2, dk + 0.3, 1e9], [-12, 0, 0, -10, -10]) / 20)).astype(np.float32)[:, None]
    f = int(1.0 * SR); e[-f:] *= np.linspace(1, 0, f)[:, None]; pos(bg, e, t_esp, 0.05)
    # ambiente de obra sob a entrevista (exceto o plano noturno)
    amb = norm(load(TR / "amb_obra.mp3"), -32); L = len(amb); xf = int(1.0 * SR)
    for s in S:
        if s.get("amb"):
            a0 = int(s["T0"] * SR); n = s["n"] * SR // FPS; seg = np.zeros((n, 2), np.float32); p = 0
            off = (a0 * 7) % max(1, L - SR)
            while p < n:
                m = min(n - p, L - off); seg[p:p + m] = amb[off:off + m]; p += m; off = 0
            g = int(0.05 * SR); seg[:g] *= np.linspace(0, 1, g)[:, None]; seg[-g:] *= np.linspace(1, 0, g)[:, None]
            bg[a0:a0 + n] += seg[:N - a0]
    m = voz + bg; k = int(0.2 * SR); m[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = M / "mix.f32"; raw.write_bytes(m.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-2:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.8:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.4f}", "-c:a", "pcm_s16le", M / "mix.wav"]); raw.unlink()


# ------------------------------------------------------------------ legenda
def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def com_roteiro(P, txt):
    R = txt.split()
    if len(R) == len(P): return [dict(p, w=r) for p, r in zip(P, R)]
    import difflib
    a = [limpa(p["w"]) for p in P]; b = [limpa(r) for r in R]; out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal": out += [dict(P[i1 + k], w=R[j1 + k]) for k in range(i2 - i1)]
        elif j2 > j1 and i2 > i1:
            t0, t1 = P[i1]["ini"], P[i2 - 1]["fim"]; L = [len(limpa(R[j])) + 1 for j in range(j1, j2)]; sm = sum(L); t = t0
            for k, j in enumerate(range(j1, j2)): d = (t1 - t0) * L[k] / sm; out.append(dict(w=R[j], ini=t, fim=t + d)); t += d
        elif j2 > j1:
            t = out[-1]["fim"] if out else P[0]["ini"]
            for j in range(j1, j2): out.append(dict(w=R[j], ini=t, fim=t + 0.05))
    print("   (alinhamento difflib)", txt[:40]); return out


def palavras(S):
    W = []
    def add(P, txt, t0, lin, cta=False):
        for p in com_roteiro(P, txt): W.append(dict(w=p["w"], ini=t0 + p["ini"], fim=t0 + p["fim"], linha=lin, cta=cta))
    for s in S:
        if s["tipo"] == "briga":
            add(json.loads((VZ / "R00.palavras.json").read_text(encoding="utf-8")), R00, s["T0"], "R00")
            wh = json.loads((T / "whisper_briga.json").read_text(encoding="utf-8"))
            for lin in ("DUENO", "JULIOB"):
                P = [dict(w=x["w"], ini=x["ini"] - s["ini"], fim=x["fim"] - s["ini"]) for x in wh if x["linha"] == lin]
                add(P, TXT[lin], s["T0"], lin)
        if s.get("voz"):
            P = json.loads((VZ / f"{s['voz']}.palavras.json").read_text(encoding="utf-8"))
            P = [dict(p, ini=p["ini"] - s.get("voz_ini", 0.0), fim=p["fim"] - s.get("voz_ini", 0.0)) for p in P]
            add(P, TXT[s["voz"]], s["T0"] + s.get("voz_off", 0.0), s["voz"], s["voz"] == "R02")
    return W


def blocos(W):
    B, cur = [], []
    for w in W:
        cand = cur + [w]; txt = " ".join(limpa(x["w"]) for x in cand)
        if cur and (len(cand) > MAXP or len(txt) > MAXC or cur[-1]["linha"] != w["linha"] or w["ini"] - cur[-1]["fim"] > 0.6):
            B.append(cur); cand = [w]
        cur = cand
        if re.search(r"[.!?…:;]$", w["w"]) or (w["w"].endswith(",") and len(cur) >= 2): B.append(cur); cur = []
    if cur: B.append(cur)
    return B


def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(W, total):
    B = blocos(W); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total); y = Y_CTA if b[0]["cta"] else Y_POST
        for j, w in enumerate(b):
            a = ini if j == 0 else max(ini, w["ini"] - 0.04); e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + limpa(x["w"]) for jj, x in enumerate(b))
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


def final(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    L = [(str(G / "header.png"), 0, None, "0"), (str(AQ / "graficos" / "titulo_gancho.png"), 0, 3.0, "0")]
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    pngs = L + [(str(G / "cta_txt.png"), cta_t, None, "-22"), (str(G / "cta_setas.png"), cta_t, None, "-37+10*sin(2*PI*1.4*t)"), (str(G / "selo.png"), 0, None, "0")]
    for p, *_ in pngs: ins += ["-loop", "1", "-framerate", "30", "-t", f"{total + 1:.3f}", "-i", p]
    fc = [f"[0:v]setpts=N/({FPS}*TB)[b0]"]; ult = "[b0]"
    def ov(i, a, b, y, ult):
        en = ""
        if a > 0 or b is not None: en = f":enable='gte(t,{a - 1 / 60:.4f})" + (f"*lt(t,{b - 1 / 60:.4f})'" if b is not None else "'")
        o = f"[o{i}]"; fc.append(f"{ult}[{i + 2}:v]overlay=0:{y}:format=auto{en}{o}"); return o
    ult = ov(0, *pngs[0][1:], ult); ult = ov(1, *pngs[1][1:], ult)
    fc.append(f"{ult}ass=leg.ass:fontsdir=fonts[lg]"); ult = "[lg]"
    for i in (2, 3, 4): ult = ov(i, *pngs[i][1:], ult)
    fc.append(f"{ult}format=yuv420p[v]"); (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
         "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS, "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
         "-t", f"{total:.3f}", OUT], cwd=M)


def folha(total):
    fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    n = 24
    for k in range(n):
        t = (k + 0.5) * total / n
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=240:427", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", "tile=12x2", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


def narracion(S, W, total):
    def mmss(t): return f"{int(t // 60):02d}:{t % 60:05.2f}"
    lin = {}
    for w in W: lin.setdefault(w["linha"], []).append(w)
    out = [f"SB-ES HUMILLACIÓN — P4 DON JULIO (albañil) — {OUT.name} — {total:.2f} s — VIDEO FICTICIO", ""]
    for k, ws in sorted(lin.items(), key=lambda x: x[1][0]["ini"]):
        out.append(f"[{mmss(ws[0]['ini'])}–{mmss(ws[-1]['fim'])}] {NOME[k]}: " + " ".join(x["w"] for x in ws))
    out += ["", "Planos (sem fala): " + " | ".join(f"{mmss(s['T0'])} {s['id']}" for s in S)]
    OUT.with_name(OUT.stem + "_narracion.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    S, total = plano(); total = round(total, 4)
    print("total", total, "s")
    W = palavras(S); legenda(W, total)
    cta = next(s for s in S if s.get("voz") == "R02")["T0"]
    mix(S, total); render_corpo(S, total); final(total, cta); folha(total); narracion(S, W, total)
    json.dump(dict(total=total, segs=[{k: v for k, v in s.items()} for s in S], cta=cta), open(M / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", OUT, total)


if __name__ == "__main__":
    main()
