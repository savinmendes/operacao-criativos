# -*- coding: utf-8 -*-
"""Montagem final: cenas (com lipsync quando existir) -> corpo; audio (vozes + ambiente/trilha demucs);
legenda ES + moldura do post + moldura EN VIVO + titulo/circulos do quadro + selo + CTA -> mont/master.mp4
Uso: python montar.py [--so-audio] [--so-video]"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import plano, vozes
AQ = Path(__file__).resolve().parent; M = AQ / "mont"; G = AQ / "graficos"; SR = 48000
NV = AQ / "audio" / "sep" / "htdemucs" / "orig" / "no_vocals.wav"
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
S = plano.segmentos(); TOTAL = plano.TOTAL


def run(c, **kw):
    r = subprocess.run(c, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode:
        print(" ".join(map(str, c))[:2000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def arquivo(k, c):
    if c.get("chat"): return M / f"cena_chat{c['chat']}.mp4"
    ls = M / f"cena_{k:02d}_ls.mp4"
    return ls if ls.exists() else M / f"cena_{k:02d}.mp4"


def corpo():
    for c in S:
        if c.get("chat"): run([sys.executable, str(G / "chat.py"), str(c["n"]), c["chat"]])
    lista = []
    for k, c in enumerate(S):
        out = M / f"n_{k:02d}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(arquivo(k, c)), "-frames:v", str(c["n"]), "-vf", "fps=30,format=yuv420p",
             "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-x264-params", "keyint=60", *TAG, "-an", str(out)])
        lista.append(out)
    (M / "lista.txt").write_text("".join(f"file '{p.name}'\n" for p in lista), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(M / "lista.txt"), "-c", "copy", str(M / "corpo.mp4")])
    n = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames",
                 "-of", "csv=p=0", str(M / "corpo.mp4")]).stdout)
    print("corpo", n, "quadros (esperado", sum(c["n"] for c in S), ")")


def load(p, af=None, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + (["-t", f"{t:.3f}"] if t else []) + ["-i", str(p)] + \
          (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()


def lufs(a):
    raw = M / "_m.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    raw.unlink(); l = [x for x in r.stderr.splitlines() if x.strip().startswith("I:")]
    return float(l[-1].split()[1])


def audio():
    N = int(TOTAL * SR); T = vozes.trilhas()
    voz = np.zeros((N, 2), np.float32)
    for p, a in T.items():
        if p == "sacerdote":   # reza (L09/L09b) com reverb leve
            a = a.copy(); i0 = int(plano.LIN["L09"]["T0"] * SR); i1 = int((plano.LIN["L09b"]["T0"] + plano.LIN["L09b"]["dur"] + 1.0) * SR)
            raw = M / "_r.f32"; raw.write_bytes(a[i0:i1].tobytes())
            rv = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af",
                                               "aecho=0.8:0.55:45|95:0.20|0.10", "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)
            raw.unlink(); rv = rv[:i1 - i0]; a[i0:i0 + len(rv)] = rv
        voz += a[:N]
    gv = 10 ** ((-15 - lufs(voz)) / 20); voz *= gv
    amb = np.zeros((N, 2), np.float32); fade = int(0.03 * SR)
    T0 = next(c["T"] for c in S if c["desc"].startswith("padre P1"))
    for c in S:
        if c.get("chat") or not c["pecas"] or c["T"] >= T0: continue
        for p in c["pecas"]:
            q = load(NV, ss=p["a"], t=p["n"] / 30 * c["vel"]); s = int(p["q0"] / 30 * SR); n = min(len(q), N - s, int(p["n"] / 30 * SR))
            q = q[:n]; q[:fade] *= np.linspace(0, 1, fade)[:, None]; q[-fade:] *= np.linspace(1, 0, fade)[:, None]; amb[s:s + n] += q
    bed = load(NV, ss=40.62); need = N - int(T0 * SR)
    while len(bed) < need:
        x = load(NV, ss=45.0); cf = 2 * SR; w = np.linspace(0, 1, cf)[:, None]
        bed = np.concatenate([bed[:-cf], bed[-cf:] * (1 - w) + x[:cf] * w, x[cf:]])
    bed = bed[:need]; bed[:int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))[:, None]
    ia = amb[:int(T0 * SR)]
    amb *= 10 ** ((-30 - lufs(ia[np.abs(ia).sum(1) > 0])) / 20)
    bed *= 10 ** ((-32 - lufs(bed)) / 20)
    amb[int(T0 * SR):] += bed
    amb[-int(1.0 * SR):] *= np.linspace(1, 0, int(1.0 * SR))[:, None]
    mix = voz + amb
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af",
             "loudnorm=I=-14:TP=-3:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-3:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.66:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", af, "-t", f"{TOTAL:.3f}",
         "-c:a", "pcm_s16le", str(M / "mix.wav")])
    raw.unlink(); print("audio ok; ganho voz", round(20 * np.log10(gv), 1), "dB")


def overlays():
    L = []
    for c in S:
        a, b = c["q0"] / 30, (c["q0"] + c["n"]) / 30
        if c["pecas"] and all(p["a"] < 40.0 for p in c["pecas"]): L.append(("header.png", a, b, "0"))
        if c["pecas"] and all(p["nome"].startswith("P") for p in c["pecas"]): L.append(("live_ui.png", a, b, "0"))
        if c.get("board"):
            L.append(("board_titulo.png", a, b, "0"))
            PW = plano.LIN["L09b"]["palavras"]
            W = [plano.LIN["L09b"]["T0"] + p["ini"] for p in PW if p["w"].lower() != "y"]
            for k, w in enumerate(W):
                ini = w - 0.05; fim = (W[k + 1] - 0.05) if k + 1 < len(W) else b
                for j in range(4):
                    fa = ini + j / 30; fb = (ini + (j + 1) / 30) if j < 3 else fim
                    L.append((f"circ_{k:02d}_{j}.png", fa, fb, "0"))
    L.append(("cta_txt.png", plano.CTA_T, TOTAL, "0"))
    L.append(("cta_setas.png", plano.CTA_T, TOTAL, "10*sin(2*PI*1.4*t)"))
    return L


def video():
    fonts = M / "fonts"; fonts.mkdir(exist_ok=True)
    for f in G.glob("Poppins-*.ttf"): (fonts / f.name).write_bytes(f.read_bytes())
    L = overlays(); pngs = sorted(set(p for p, *_ in L)) + ["selo.png"]
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    for p in pngs: ins += ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL + 1:.3f}", "-i", str(G / p)]
    idx = {p: i + 2 for i, p in enumerate(pngs)}
    uso = {}
    for p, *_ in L: uso[p] = uso.get(p, 0) + 1
    uso["selo.png"] = 1
    fc = []
    for p in pngs:
        n = uso[p]; lab = p.replace(".png", "")
        fc.append(f"[{idx[p]}:v]format=rgba" + ((f",split={n}" + "".join(f"[{lab}_{j}]" for j in range(n))) if n > 1 else f"[{lab}_0]"))
    cont = {}
    def ov(p, a, b, y, ultimo):
        lab = p.replace(".png", ""); j = cont.get(lab, 0); cont[lab] = j + 1
        if b >= TOTAL - 0.02: b = TOTAL + 5   # ate o ultimo quadro (inclusive o duplicado do finalizar)
        en = f":enable='gte(t,{a - 1 / 60:.4f})*lt(t,{b - 1 / 60:.4f})'" if (a > 0 or b < TOTAL) else ""
        out = f"[o{len(fc)}]"; fc.append(f"{ultimo}[{lab}_{j}]overlay=0:{y}:format=auto{en}{out}"); return out
    fc.append("[0:v]setpts=N/(30*TB)[base]"); ult = "[base]"
    for p, a, b, y in L:
        if not p.startswith("cta"): ult = ov(p, a, b, y, ult)
    fc.append(f"{ult}ass=leg.ass:fontsdir=fonts[leg]"); ult = "[leg]"
    for p, a, b, y in L:
        if p.startswith("cta"): ult = ov(p, a, b, y, ult)
    ult = ov("selo.png", 0, TOTAL, "0", ult)
    fc.append(f"{ult}format=yuv420p[v]")
    (M / "fc.txt").write_text(";\n".join(fc), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-/filter_complex", "fc.txt", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p", *TAG, "-r", "30",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-t", f"{TOTAL:.3f}", "master.mp4"], cwd=M)
    print("master ok", M / "master.mp4")


if __name__ == "__main__":
    if "--so-audio" in sys.argv: audio()
    elif "--so-video" in sys.argv: corpo(); video()
    else: corpo(); audio(); video()
