# -*- coding: utf-8 -*-
"""P3 CARMEN — montagem do SB-ES "Humillación" (v5-personas) -> v5-personas/SB-ES_HUMILLACION_P3-CARMEN_FICTICIO.mp4
Estrutura (BRIEFING_PERSONAS.md): abertura Seedance (take único) + reportera em PiP (chroma) + zoom 130 % + título;
virada sem fala (Kling: mãos/terço -> sentada + senhora -> abraço) com trilha triste -> esperança; reportera R01 (HeyGen);
Carmen entrevistada (HeyGen, 5 jobs, cortes secos com zoom 100/112 %); reportera CTA com setas até o fim.
Tudo dentro da moldura do post (janela 720x840 em y=297). Selo VIDEO FICTICIO o vídeo todo. Legenda palavra a palavra pelo roteiro.
Config: cfg.json. Uso: python montar.py [--so-plano]"""
import json, re, subprocess, sys, difflib
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG

AQ = Path(__file__).resolve().parent; T = AQ / "takes"; V = AQ / "voz"; GR = AQ / "graficos"; M = AQ / "mont"; M.mkdir(exist_ok=True)
RAIZ = AQ.parents[2]; G1 = RAIZ / "_trabalho" / "graficos"; TRI = RAIZ / "v3" / "_trabalho" / "final_B" / "trilha"
OUT = AQ.parents[1] / "SB-ES_HUMILLACION_P3-CARMEN_FICTICIO.mp4"
C = json.loads((AQ / "cfg.json").read_text(encoding="utf-8"))
FPS, SR, WW, WH, WY = 30, 48000, 720, 840, 297
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
ROT = {"R00": "Imágenes impactantes: una empleada fue echada a la calle… por su fe.",
       "B02": "¡Ladrona! ¿Rezas tanto? ¡Que tu Dios te consiga otro trabajo!",
       "B03": "Señora, yo nunca le robé nada. Por el amor de Dios, créame.",
       "R01": "A los pocos días, Carmen tenía tres familias queriendo contratarla.",
       "C1": "Esa noche pensé en mis hijos y no sabía cómo decirles que me habían echado… y encima acusada de ladrona. Una amiga me mandó la transmisión del padre Juan Méndez.",
       "C2": "La hice esa misma noche, como él enseña. Al día siguiente, me llamaron para un trabajo nuevo, con gente que me trata como familia.",
       "P1": "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche.",
       "P2": "Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito…",
       "P3": "y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?",
       "CTA": "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo."}


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


def fade(a, ms=15):
    n = min(int(ms / 1000 * SR), len(a) // 2)
    if n: a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a


def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"“”]", "", w).lower()


def roteirizar(P, txt):
    """troca as palavras (whisper/alinhamento) pelas do roteiro mantendo os tempos"""
    R = txt.split()
    if len(R) == len(P): return [dict(p, w=r) for p, r in zip(P, R)]
    a = [limpa(p["w"]) for p in P]; b = [limpa(r) for r in R]; out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal": out += [dict(P[i1 + k], w=R[j1 + k]) for k in range(i2 - i1)]
        elif j2 > j1 and i2 > i1:
            t0, t1 = P[i1]["ini"], P[i2 - 1]["fim"]; L = [len(limpa(R[j])) + 1 for j in range(j1, j2)]; s = sum(L); t = t0
            for k, j in enumerate(range(j1, j2)): d = (t1 - t0) * L[k] / s; out.append(dict(w=R[j], ini=t, fim=t + d)); t += d
        elif j2 > j1:
            t = out[-1]["fim"] if out else P[0]["ini"]
            for j in range(j1, j2): out.append(dict(w=R[j], ini=t, fim=t + 0.01))
    return out


def alfa(f):           # chroma verde + despill (igual compor_reporter.py)
    x = f.astype(np.float32); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    a = 1 - np.clip((g - np.maximum(r, b) - 18) / (70 - 18), 0, 1)
    a = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 0.9)
    lim = np.maximum(r, b) + 4; x[..., 1] = np.where(g > lim, lim, g)
    return x, a


def enc(frames, out):
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{WW}x{WH}", "-r", str(FPS), "-i", "-",
                           *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", *ENC_TAG,
                           "-frames:v", str(len(frames)), str(out)], stdin=subprocess.PIPE)
    for f in frames: ff.stdin.write(f.tobytes())
    ff.stdin.close(); ff.wait()


def cover(src, ini, n, zoom=1.0, cx=0.5, cy=0.5, vel=1.0):
    """trecho [ini, ini + n/30*vel] do take -> n quadros 720x840 (cover + zoom opcional)"""
    o = M / f"seg_{src.stem}_{ini:.2f}_{n}_{zoom}.mp4"
    zs = ""
    if zoom > 1.0:
        zw, zh = int(WW * zoom) // 2 * 2, int(WH * zoom) // 2 * 2
        zs = f",scale={zw}:{zh}:flags=lanczos,crop={WW}:{WH}:{int((zw - WW) * cx)}:{int((zh - WH) * cy)}"
    vf = (f"setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS},scale={WW}:{WH}:force_original_aspect_ratio=increase:flags=lanczos,"
          f"crop={WW}:{WH}:(iw-{WW})*{cx}:(ih-{WH})*{cy}{zs},format=yuv420p,tpad=stop_mode=clone:stop=3,trim=end_frame={n},setpts=PTS-STARTPTS")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-t", f"{n / FPS * vel + 0.5:.3f}", "-i", src, "-vf", vf, "-frames:v", n, "-r", FPS,
         "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", "-pix_fmt", "yuv420p", *TAG, o])
    return o


def PRE(): return C["pre"]["quadros"] if C.get("pre") else 0


def palavras_json(i):
    return json.loads((V / f"{i}.json").read_text(encoding="utf-8"))["palavras"]


# ------------------------------------------------------------------ plano
def plano():
    S = []; t = 0.0
    b = C["briga"]; nb = round((b["fim"] - b["ini"]) * FPS) + PRE()
    S.append(dict(id="briga", n=nb, T0=0.0)); t = nb / FPS
    for k in ("maos", "sentada", "abraco"):
        v = C["virada"][k]; n = round(v["dur"] * FPS); S.append(dict(id=k, n=n, T0=t, src=T / v["arquivo"], ini=v["ini"], cx=v.get("cx", 0.5), cy=v.get("cy", 0.5),
                                                                      zoom=v.get("zoom", 1.0), vel=v.get("vel", 1.0))); t += n / FPS
    for k, z in C["falas"]:
        P = palavras_json(k); a = max(C.get("cabeca_min", 0.08), P[0]["ini"] - C.get("cabeca", 0.10)); e = P[-1]["fim"] + C.get("cauda", 0.10)
        if k == "CTA": e = P[-1]["fim"] + C.get("cauda_cta", 0.9)
        n = round((e - a) * FPS); S.append(dict(id=k, n=n, T0=t, src=T / f"hg_{k}.mp4", ini=a, zoom=z, voz=V / f"{k}.wav", P=P,
                                                cx=0.5, cy=C.get("cy_carmen", 0.35) if k[0] in "CP" and k != "CTA" else C.get("cy_rep", 0.3)))
        t += n / FPS
    if C.get("final"):        # plano final sem fala (setas do CTA continuam até o último quadro)
        v = C["final"]; n = round(v["dur"] * FPS); S.append(dict(id="final", n=n, T0=t, src=T / v["arquivo"], ini=v["ini"], cx=0.5, cy=0.5)); t += n / FPS
    total = round(t * FPS) / FPS
    return S, total


# ------------------------------------------------------------------ abertura (python: zoom + PiP chroma)
def abertura(seg):
    b = C["briga"]; src = T / b["arquivo"]; P = PRE(); n = seg["n"] - P
    def jan(arq, ini, k, nome, vel=1.0):
        o = M / nome
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", arq, "-vf",
             f"setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS},scale={WW}:{WH}:force_original_aspect_ratio=increase:flags=lanczos,crop={WW}:{WH}:(iw-{WW})*{b.get('cx', 0.5)}:(ih-{WH})*{b.get('cy', 0.5)}",
             "-frames:v", k, "-an", "-c:v", "libx264", "-crf", "8", "-preset", "fast", o])
        return list(quadros(o, 0, k, WW, WH))
    fr = jan(src, b["ini"], n, "briga_840.mp4")
    if P:          # pré-roll Kling (termina no quadro 0 do Seedance): últimos P quadros, fundidos nos J últimos
        pr = C["pre"]; pf = jan(T / pr["arquivo"], pr["ini"], P, "pre_840.mp4", pr.get("vel", 1.0)); J = pr.get("fundir", 4)
        for k in range(J):
            a_ = (k + 1) / (J + 1); i = P - J + k; pf[i] = cv2.addWeighted(pf[i], 1 - a_, fr[0], a_, 0)
        fr = pf + fr
    t30 = M / "pip30.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", T / "hg_R00_pip.mp4", "-vf", f"fps={FPS}", "-c:v", "libx264", "-crf", "8", "-preset", "fast", "-an", t30])
    tk = [cv2.resize(f, (304, 540), interpolation=cv2.INTER_AREA) for f in quadros(t30)]
    NP = min(len(tk), round(C["pip_ate"] * FPS)); NF = 4; Z = C.get("zoom", 1.30); ZC = C.get("zoom_c", [360, 420]); ZATE = round(C.get("zoom_ate", 2.0) * FPS); ZDE = round(C.get("zoom_de", 0.0) * FPS)
    out = []
    for q, o in enumerate(fr):
        if ZDE <= q < ZATE:
            Z = C.get("zoom", 1.30); k_ = ZATE - q
            if k_ <= 6: Z = 1 + (Z - 1) * (k_ - 1) / 6          # volta suave nos últimos 6 quadros
            cw, ch = WW / Z, WH / Z; x0 = min(max(ZC[0] - cw / 2, 0), WW - cw); y0 = min(max(ZC[1] - ch / 2, 0), WH - ch)
            o = cv2.warpAffine(o, np.float32([[Z, 0, -x0 * Z], [0, Z, -y0 * Z]]), (WW, WH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
        if q < NP:
            fg, a = alfa(tk[q]); A = np.zeros((WH, WW), np.float32); F = np.zeros((WH, WW, 3), np.float32)
            A[300:840, 0:304] = a[:540]; F[300:840, 0:304] = fg[:540]; A[:, 284:] = 0
            if q >= NP - NF: A *= 1 - (q - (NP - NF) + 1) / (NF + 1)
            o = np.clip(F * A[..., None] + o.astype(np.float32) * (1 - A[..., None]), 0, 255).astype(np.uint8)
        out.append(o)
    o = M / "seg_abertura.mp4"; enc(out, o); return o


# ------------------------------------------------------------------ áudio
def audio(S, total):
    N = int(round(total * SR)); mix = np.zeros((N, 2), np.float32)
    def pos(a, t0):
        s = int(round(t0 * SR)); n = min(len(a), N - s)
        if n > 0: mix[s:s + n] += a[:n]
    b = C["briga"]; nb = S[0]["n"] / FPS
    off = PRE() / FPS; nat = load(T / b["arquivo"], b["ini"], nb - off) if not (C.get("sts") and (AQ / "sts" / "briga_audio_sts.wav").exists())         else load(AQ / "sts" / "briga_audio_sts.wav", b["ini"], nb - off)
    g = 10 ** ((-16 - lufs(nat)) / 20); nat = nat * g
    if off:       # ambiente do pré-roll = fundo (demucs) do próprio take
        amb = load(AQ / "sts" / "htdemucs" / "briga2" / "no_vocals.wav", C["pre"].get("amb_ss", 0.0), off + 0.3) * g
        f_ = int(0.3 * SR); amb[-f_:] *= np.linspace(1, 0, f_)[:, None]; pos(amb, 0.0)
    r0 = palavras_json("R00"); da = r0[-1]["fim"] + 0.05 - off; t = np.arange(len(nat)) / SR
    nat *= (10 ** (np.interp(t, [0, max(da, 0.01), max(da, 0.01) + 0.3, 1e9], [-5, -5, 0, 0]) / 20)).astype(np.float32)[:, None]
    f_ = int(0.03 * SR); nat[:f_] *= np.linspace(0, 1, f_)[:, None]
    k = int(0.25 * SR); nat[-k:] *= np.linspace(1, 0, k)[:, None]; pos(nat, off)
    pos(norm(load(V / "R00.wav"), -15), 0.0)
    by = {s["id"]: s for s in S}
    # trilha triste (mãos + sentada) -> esperança (senhora chega + abraço), abaixa sob a reportera
    t4 = by["maos"]["T0"]; t5 = by["sentada"]["T0"] + C.get("esperanca_em", 1.6); tR = by["R01"]["T0"]; xf = int(0.9 * SR)
    tri = norm(load(TRI / "triste_1.mp3"), -19); nt = min(len(tri), int((t5 - t4 + 0.9) * SR)); tri = tri[:nt].copy()
    tri[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]; tri[-xf:] *= np.linspace(1, 0, xf)[:, None]; pos(tri, t4 - 0.15)
    es = norm(load(TRI / "esperanca_1.mp3"), -20); ne = min(len(es), int((tR + 2.2 - t5) * SR)); es = es[:ne].copy(); es[:xf] *= np.linspace(0, 1, xf)[:, None]
    env = np.ones(ne, np.float32); i0 = int((tR - 0.3 - t5) * SR)
    if 0 < i0 < ne: env[i0:] = np.linspace(1, 10 ** (-12 / 20), ne - i0)
    es *= env[:, None]; es[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))[:, None]; pos(es, t5)
    # vozes HeyGen (mesmo trecho do vídeo)
    for s in S:
        if "voz" not in s: continue
        a = fade(load(s["voz"], s["ini"], s["n"] / FPS)); pos(norm(a, -15), s["T0"])
    # rua residencial sob reportera/entrevista
    t0 = tR - 0.1; rua = load(AQ / "trilha" / "rua_residencial.mp3"); need = int((total - t0) * SR)
    while len(rua) < need: rua = np.concatenate([rua, rua])
    rua = norm(rua[:need].copy(), -33); rua[:int(0.4 * SR)] *= np.linspace(0, 1, int(0.4 * SR))[:, None]; pos(rua, t0)
    k = int(0.5 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{total:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"]); raw.unlink()


# ------------------------------------------------------------------ legenda (estilo v4)
FS, Y_POST, Y_CTA, MAXP, MAXC = 64, 1072, 840, 3, 18
JUNTAR = [(["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["juan", "méndez"], "juan méndez")]


def palavras_tl(S):
    W = []
    for p in palavras_json("R00"): W.append(dict(p, linha="R00"))
    sb = json.loads((T / "whisper_briga.json").read_text(encoding="utf-8"))
    for lin in ("B02", "B03"):
        P = roteirizar([p for p in sb if p["linha"] == lin], ROT[lin])
        o_ = PRE() / FPS - C["briga"]["ini"]
        W += [dict(p, linha=lin, ini=p["ini"] + o_, fim=p["fim"] + o_) for p in P]
    for s in S:
        if "P" not in s: continue
        P = roteirizar(s["P"], ROT[s["id"]])
        W += [dict(w=p["w"], ini=s["T0"] + p["ini"] - s["ini"], fim=s["T0"] + p["fim"] - s["ini"], linha=s["id"], t0s=s["T0"] + 1 / FPS) for p in P]
    out = []
    for p in W:
        w = limpa(p["w"])
        if w: out.append(dict(p, raw=p["w"], w=w))
    res, k = [], 0
    while k < len(out):
        for seq, rep in JUNTAR:
            if [x["w"] for x in out[k:k + len(seq)]] == seq and len({x["linha"] for x in out[k:k + len(seq)]}) == 1:
                res.append(dict(out[k], w=rep, fim=out[k + len(seq) - 1]["fim"], raw=out[k + len(seq) - 1]["raw"])); k += len(seq); break
        else: res.append(out[k]); k += 1
    return res


def blocos(W):
    B, cur = [], []
    for w in W:
        cand = cur + [w]; txt = " ".join(x["w"] for x in cand)
        if cur and (len(cand) > MAXP or len(txt) > MAXC or cur[-1]["linha"] != w["linha"] or w["ini"] - cur[-1]["fim"] > 0.6):
            B.append(cur); cand = [w]
        cur = cand
        if re.search(r"[.!?…:;]$", w["raw"]) or (w["raw"].endswith(",") and len(cur) >= 2): B.append(cur); cur = []
    if cur: B.append(cur)
    fix = []
    for b in B:
        if fix and len(b) == 1 and len(fix[-1]) < MAXP and fix[-1][-1]["linha"] == b[0]["linha"] and not re.search(r"[.!?…:;]$", fix[-1][-1]["raw"]) \
                and len(" ".join(x["w"] for x in fix[-1] + b)) <= MAXC and b[0]["ini"] - fix[-1][-1]["fim"] < 0.4:
            fix[-1] = fix[-1] + b
        else: fix.append(b)
    return fix


def ts(t): t = max(0.0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda(S, total, cta_t):
    W = palavras_tl(S); B = blocos(W); ev = []
    for i, b in enumerate(B):
        ini = max(b[0]["ini"] - 0.04, b[0].get("t0s", 0.0), 0.0); prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else total
        fim = min(prox, b[-1]["fim"] + 0.45, total); y = Y_CTA if ini >= cta_t - 0.1 else Y_POST
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
    return W


# ------------------------------------------------------------------ vídeo final
def video(total, cta_t):
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G1.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    L = lambda p: ["-loop", "1", "-framerate", str(FPS), "-t", f"{total + 1:.3f}", "-i", str(GR / p)]
    ins = ["-reinit_filter", "0", "-i", "janela.mp4", "-i", "mix.wav", *L("plate.png"), *L("header.png"), *L("titulo_gancho.png"), *L("cta_txt.png"), *L("cta_setas.png"), *L("selo.png")]
    a = cta_t - 1 / 60
    fc = [f"[2:v]fps={FPS},format=yuv420p[pl]", f"[0:v]setpts=N/({FPS}*TB)[jn]", f"[pl][jn]overlay=0:{WY}:format=auto[b0]",
          "[3:v]format=rgba[hd]", "[b0][hd]overlay=0:0:format=auto[b1]",
          "[4:v]format=rgba[tt]", f"[b1][tt]overlay=0:0:format=auto:enable='lt(t,{C.get('titulo_ate', 3.0):.3f})'[b2]",
          "[b2]ass=leg.ass:fontsdir=fonts[b3]",
          "[5:v]format=rgba[ct]", f"[b3][ct]overlay=0:-22:format=auto:enable='gte(t,{a:.4f})'[b4]",
          "[6:v]format=rgba[cs]", f"[b4][cs]overlay=0:'-37+10*sin(2*PI*1.4*t)':format=auto:enable='gte(t,{a:.4f})'[b5]",
          "[7:v]format=rgba[se]", "[b5][se]overlay=0:0:format=auto,format=yuv420p[v]"]
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", FPS,
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{total:.2f} s")


def folha(total):
    n = 30; fr = M / "_fr"; fr.mkdir(exist_ok=True)
    for f in fr.glob("*.png"): f.unlink()
    for k in range(n):
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(k + 0.5) * total / n:.3f}", "-i", OUT, "-frames:v", "1", "-vf", "scale=360:640", fr / f"{k:02d}.png"])
    run(["ffmpeg", "-v", "error", "-y", "-i", fr / "%02d.png", "-vf", f"tile={n}x1", "-frames:v", "1", "-q:v", "3", OUT.with_name(OUT.stem + "_frames.jpg")])


NOME = {"R00": "REPORTERA (en PiP)", "B02": "PATRONA", "B03": "CARMEN", "R01": "REPORTERA", "C1": "CARMEN", "C2": "CARMEN", "P1": "CARMEN",
        "P2": "CARMEN", "P3": "CARMEN", "CTA": "REPORTERA"}


def narracion(W, S, total):
    mm = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"; lin = []; vistos = set()
    for w in W:
        if w["linha"] in vistos: continue
        vistos.add(w["linha"]); lin.append(f"[{mm(w['ini'])}] {NOME[w['linha']]}: {ROT[w['linha']]}")
        if w["linha"] == "B03":
            by = {s["id"]: s for s in S}
            lin.append(f"[{mm(by['maos']['T0'])}] (sin voz: Carmen junta el rosario del suelo, música triste -> sentada sola en la acera -> una señora se acerca -> recibida con un abrazo en una casa nueva)")
    cab = f"""NARRACIÓN COMPLETA — {OUT.name} ({int(total // 60)}:{int(total % 60):02d})
Tiempos = momento en que empieza cada frase en el video final.
Personajes ficticios: REPORTERA (en PiP desde 0:00 y luego en la calle), PATRONA, CARMEN (empleada doméstica).
Sello "VIDEO FICTICIO" arriba a la derecha durante todo el video. Moldura de post "Fe en Noticias / Trabajador es humillado y algo impactante sucede" todo el video.
Voces: reportera Gabriela (ElevenLabs) · Carmen Alisson (ElevenLabs) en la entrevista · patrona y Carmen en la pelea = audio nativo del take (Seedance){' convertido con speech-to-speech: patrona voz Karly, Carmen voz Alisson; "¿Rezas" y "créame" re-grabados en TTS con la misma voz' if C.get('sts') else ''}.
Título 0–3 s: "LA HUMILLARON POR SU FE… / A LOS POCOS DÍAS PASÓ ESTO". CTA único al final (flechas TOCA «VER MÁS» desde el CTA hasta el final); nada se dice después del CTA.
"""
    p = OUT.with_name(OUT.stem + "_narracion.txt"); p.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8"); return p


if __name__ == "__main__":
    S, total = plano(); by = {s["id"]: s for s in S}; cta_t = by["CTA"]["T0"]
    for s in S: print(f"{s['T0']:7.2f} +{s['n'] / FPS:5.2f} {s['id']:8s} z{s.get('zoom', 1)}")
    print("TOTAL", total, "CTA", cta_t)
    if "--so-plano" in sys.argv: sys.exit()
    segs = [abertura(S[0])]
    for s in S[1:]: segs.append(cover(s["src"], s["ini"], s["n"], s.get("zoom", 1.0), s.get("cx", 0.5), s.get("cy", 0.5), s.get("vel", 1.0)))
    (M / "lista.txt").write_text("".join(f"file '{x.name}'\n" for x in segs), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", M / "lista.txt", "-c", "copy", M / "janela.mp4"])
    k = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", M / "janela.mp4"]).stdout)
    print("janela", k, "quadros; esperado", round(total * FPS))
    audio(S, total); W = legenda(S, total, cta_t); video(total, cta_t); print(narracion(W, S, total)); folha(total)
    json.dump(dict(total=total, cta_t=cta_t, segs=[{k: (str(v) if isinstance(v, Path) else v) for k, v in s.items() if k != "P"} for s in S]),
              open(AQ / "timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
