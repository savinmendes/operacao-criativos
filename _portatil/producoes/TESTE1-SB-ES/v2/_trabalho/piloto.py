# -*- coding: utf-8 -*-
"""Monta o PILOTO v2 (react atual + briga Seedance + reportera HeyGen) com moldura do post, legenda ES palavra a palavra
e selo VIDEO FICTICIO -> .../PILOTO_briga-reportera.mp4.  Config em piloto.json (cortes e palavras dos takes).
Uso: python piloto.py"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
AQ = Path(__file__).resolve().parent; V1 = AQ.parent.parent / "_trabalho"; OUT = AQ.parent / "PILOTO_briga-reportera.mp4"
M = AQ / "mont"; M.mkdir(exist_ok=True); G = V1 / "graficos"
FPS, SR = 30, 48000
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
WIN = (0, 297, 720, 840)          # janela de vídeo dentro da moldura do post
BASE = V1 / "lama" / "base_limpa.mp4"; NV = V1 / "audio" / "sep" / "htdemucs" / "orig" / "no_vocals.wav"
ATUAL = AQ.parent.parent / "SB-ES_NOTICIA-AURELIO_FICTICIO.mp4"
C = json.loads((AQ / "piloto.json").read_text(encoding="utf-8"))


def run(c, **kw):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode: print(" ".join(map(str, c))[:1500]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def load(p, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + (["-t", f"{t:.3f}"] if t else []) + \
          ["-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    raw.unlink(); l = [x for x in r.stderr.splitlines() if x.strip().startswith("I:")]
    return float(l[-1].split()[1])


def fade(a, ms=25):
    n = min(int(ms / 1000 * SR), len(a) // 2)
    if n: a[:n] *= np.linspace(0, 1, n)[:, None]; a[-n:] *= np.linspace(1, 0, n)[:, None]
    return a


# ---------------- linha do tempo (quadros)
NR = 82                                        # react = cena_00_ls atual (0-2,733 s)
B0, B1 = C["briga"]["ini"], C["briga"]["fim"]; NB = round((B1 - B0) * FPS)
R0, R1 = C["rep"]["ini"], C["rep"]["fim"]; NRP = round((R1 - R0) * FPS)
TB = NR / FPS; TRp = (NR + NB) / FPS; TOTAL = (NR + NB + NRP) / FPS
INS = C["rep"].get("insertos", [])            # [ini, fim, ss_base]: b-roll da base_limpa sobre a reportera (tempo do take)


def janela(src, ss, n, cx=None):
    """vídeo do take recortado em cover na janela 720x840; cx = centro x do recorte (fração da largura do take)"""
    xs = "" if cx is None else f":'min(max(iw*{cx}-{WIN[2] / 2},0),iw-{WIN[2]})':0"
    return f"[{src}]trim=start={ss:.3f},setpts=PTS-STARTPTS,fps={FPS},scale={WIN[2]}:{WIN[3]}:force_original_aspect_ratio=increase:flags=lanczos," \
           f"crop={WIN[2]}:{WIN[3]}{xs},trim=end_frame={n},setpts=PTS-STARTPTS"


def video_corpo():
    plate = M / "plate.png"
    run(["ffmpeg", "-v", "error", "-y", "-ss", "20.0", "-i", BASE, "-frames:v", "1", plate])
    ins = ["-i", V1 / "mont" / "cena_00_ls.mp4", "-i", AQ / C["briga"]["arquivo"], "-loop", "1", "-framerate", str(FPS), "-i", plate]
    fc = [f"[0:v]fps={FPS},trim=end_frame={NR},setpts=PTS-STARTPTS,format=yuv420p[r]",
          janela("1:v", B0, NB, C["briga"].get("cx")) + "[w0]"]
    # peças da reportera: take HeyGen intercalado com insertos (cortes em quadros da linha do tempo)
    marcas = [(R0, None)]
    for a, b, ss in INS: marcas += [(a, ss), (b, None)]
    marcas.append((R1, "fim")); labs = ["[w0]"]; q = lambda t: round((t - R0) * FPS)
    for k in range(len(marcas) - 1):
        (t0, ss), (t1, _) = marcas[k], marcas[k + 1]; n = q(t1) - q(t0); j = len(ins) // 2 - 0  # índice do próximo input
        idx = 3 + k
        if ss is None:
            ins += ["-i", AQ / C["rep"]["arquivo"]]; fc.append(janela(f"{idx}:v", t0, n) + f"[w{k + 1}]")
        else:
            ins += ["-ss", f"{ss:.3f}", "-t", "6", "-i", BASE]
            fc.append(f"[{idx}:v]fps={FPS},crop={WIN[2]}:{WIN[3]}:{WIN[0]}:{WIN[1]},trim=end_frame={n},setpts=PTS-STARTPTS[w{k + 1}]")
        labs.append(f"[w{k + 1}]")
    fc.append("".join(labs) + f"concat=n={len(labs)}:v=1:a=0[win]")
    fc.append(f"[2:v]fps={FPS},trim=end_frame={NB + NRP},setpts=PTS-STARTPTS,format=yuv420p[pl]")
    fc.append(f"[pl][win]overlay={WIN[0]}:{WIN[1]}:format=auto,format=yuv420p[nw]")
    fc.append("[r][nw]concat=n=2:v=1:a=0,format=yuv420p[v]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-frames:v", NR + NB + NRP,
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *TAG, M / "corpo.mp4"])


def audio():
    N = int(round(TOTAL * SR)); mix = np.zeros((N, 2), np.float32)
    # react: áudio do vídeo atual (voz L01 + ambiente já mixados)
    a = fade(load(ATUAL, 0, NR / FPS)); mix[:len(a)] += a[:N]
    # briga: áudio nativo do Seedance
    b = fade(load(AQ / C["briga"]["arquivo"], B0, B1 - B0))
    for g0, g1, db in C["briga"].get("ganhos", []):   # realce de trechos (ex.: fala do vendedor mais baixa)
        i0, i1 = int((g0 - B0) * SR), int((g1 - B0) * SR); n = int(0.06 * SR); env = np.ones(i1 - i0, np.float32) * 10 ** (db / 20)
        env[:n] = np.linspace(1, env[n], n); env[-n:] = np.linspace(env[n], 1, n); b[i0:i1] *= env[:, None]
    b *= 10 ** ((C["briga"].get("lufs", -15) - lufs(b)) / 20)
    s = int(TB * SR); mix[s:s + len(b)] += b[:N - s]
    # reportera: voz do HeyGen + ambiente demucs da cena original
    r = fade(load(AQ / C["rep"]["arquivo"], R0, R1 - R0)); r *= 10 ** ((-15 - lufs(r)) / 20)
    amb = fade(load(NV, 19.30, R1 - R0), 80); amb *= 10 ** ((-31 - lufs(amb)) / 20)
    s = int(TRp * SR); n = min(len(r), N - s); mix[s:s + n] += r[:n]; n = min(len(amb), N - s); mix[s:s + n] += amb[:n]
    mix[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", "2", "-i", raw, "-af", af, "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", M / "mix.wav"])
    raw.unlink()


# ---------------- legenda (mesmo estilo do v1: legenda.py)
FS, Y, MAXP, MAXC = 64, 932, 3, 18
JUNTAR = [(["don", "aurelio"], "don aurelio")]
def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"]", "", w).lower()


def palavras():
    out = []
    def add(lista, t0, linha):
        for p in lista: out.append(dict(w=limpa(p["w"]), raw=p["w"], ini=t0 + p["ini"], fim=t0 + p["fim"], linha=linha))
    add(json.loads((V1 / "voz" / "c" / "L01.json").read_text(encoding="utf-8"))["palavras"], 0.0, "L01")
    for k, fala in enumerate(C["briga"]["palavras"]): add(fala, TB - B0, f"B{k}")
    add(json.loads((V1 / "voz" / "c" / "L04.json").read_text(encoding="utf-8"))["palavras"], TRp + C["rep"]["voz_offset"] - R0, "L04")
    out = [p for p in out if p["w"] and p["ini"] < TOTAL]
    res, k = [], 0
    while k < len(out):
        for seq, rep in JUNTAR:
            if [x["w"] for x in out[k:k + len(seq)]] == seq:
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


def ts(t): return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def legenda():
    B = blocos(palavras()); ev = []
    for i, b in enumerate(B):
        ini = b[0]["ini"] - 0.04; prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else TOTAL
        fim = min(prox, b[-1]["fim"] + 0.45, TOTAL, *[c - 0.02 for c in (TB, TRp) if c > b[-1]["fim"]])   # some no corte de cena
        for j, w in enumerate(b):
            a = ini if j == 0 else w["ini"] - 0.04; e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + x["w"] for jj, x in enumerate(b))
            pop = r"\fscx85\fscy85\t(0,80,\fscx104\fscy104)\t(80,140,\fscx100\fscy100)" if j == 0 else ""
            ev.append(f"Dialogue: 0,{ts(a)},{ts(e)},L,,0,0,0,,{{\\an5\\pos(360,{Y}){pop}}}{txt}")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins SemiBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,2,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    (M / "leg.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    for b in B: print(f"  {b[0]['ini']:6.2f} {' '.join(x['w'] for x in b)}")


def final():
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    fc = (f"[0:v]setpts=N/({FPS}*TB)[b];[2:v]format=rgba[h];[3:v]format=rgba[s];"
          f"[b][h]overlay=0:0:format=auto:enable='gte(t,{NR / FPS - 1 / 60:.4f})'[o1];[o1]ass=leg.ass:fontsdir=fonts[o2];"
          f"[o2][s]overlay=0:0:format=auto,format=yuv420p[v]")
    # react (0-2,73 s) já veio do v1 com header? cena_00_ls não tem header -> header em todo o vídeo
    fc = fc.replace(f":enable='gte(t,{NR / FPS - 1 / 60:.4f})'", "")
    run(["ffmpeg", "-v", "error", "-y", "-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav",
         "-loop", "1", "-framerate", FPS, "-t", f"{TOTAL + 1:.3f}", "-i", G / "header.png",
         "-loop", "1", "-framerate", FPS, "-t", f"{TOTAL + 1:.3f}", "-i", G / "selo.png",
         "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high",
         "-pix_fmt", "yuv420p", *TAG, "-r", FPS, "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
         "-t", f"{TOTAL:.3f}", OUT], cwd=M)
    print("ok", OUT, f"{TOTAL:.2f} s")


if __name__ == "__main__":
    print(f"react 0-{TB:.2f} | briga {TB:.2f}-{TRp:.2f} | reportera {TRp:.2f}-{TOTAL:.2f}")
    video_corpo(); audio(); legenda(); final()
