# -*- coding: utf-8 -*-
"""Monta SB-ES_MEDALLA_FICTICIO.mp4 (1080x1920, 30 fps).
Linha do tempo de saída T: narração original t, com uma pausa G=2,7 s inserida em t=11,75 (salão cheio sem fala).
Etapas: 1) partes de vídeo (yuv direto, sem passar por RGB: cor dos takes preservada) -> mont/seg_XX.mp4
        2) concat (mesmos parâmetros) -> mont/corpo.mp4
        3) áudio: voz (reza com reverb leve) + pausa + trilha própria com swell -> loudnorm -14 LUFS / -1,5 dBTP
        4) legenda (legenda_final.py) + overlays (selo sempre, título gancho, cartões do latim, CTA) -> final
Rodar em _trabalho:  python montar_final.py [--so-audio] [--so-final]
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

AQ = Path(__file__).resolve().parent
M = AQ / "mont"; M.mkdir(exist_ok=True)
BR = Path(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS")
GR = AQ / "graficos"; AV = AQ / "avatar"; TK = AQ / "takes"
SAIDA = M / "master.mp4"  # depois: finalizar.py -> ../SB-ES_MEDALLA_FICTICIO.mp4
FPS = 30
C, G = 11.75, 2.70
TOTAL_NARR = 118.72
TOTAL = round((TOTAL_NARR + G) * FPS) / FPS          # 121.42
SAC0 = 36.03 + G                                     # 38.73: início do sacerdote em T
SELF0 = 11.75 + G                                    # 14.45: início da selfie em T
CTA_T = 113.24 + G                                   # 115.94 ("Toca el botón")

SAC_PARTES = [(0.0, 30.78, AV / "sac_p1_final.mp4"), (30.78, 56.34, AV / "sac_p2_final.mp4"),
              (56.34, 99.0, AV / "sac_p3_final.mp4")]
SELFIE = AV / "com_selfie_final.mp4"
ROSTO_SELF = (576, 830)
ROSTO_SAC = (558, 650)


def S(t):
    return t + (G if t >= C else 0.0)


def brv(n):
    return next(p for p in BR.glob(f"SB-BRV-{n} *KLING25.mp4") if "REPROV" not in p.name)


# (T_ini, T_fim, tipo, args)
SEG = [
    (0.0, 6.30, "take", dict(src=TK / "salao_vazio.mp4", ss=0.0, vel=0.80, interp=True)),
    (6.30, C, "take", dict(src=TK / "salao_vazio.mp4", ss=0.0, vel=0.925, zoom=1.8, centro=(560, 860), interp=True)),
    (C, SELF0, "take", dict(src=TK / "salao_cheio.mp4", ss=0.6, vel=1.0)),
    (SELF0, S(15.50), "selfie", dict(zoom=1.0)),
    (S(15.50), S(19.70), "selfie", dict(zoom=1.13)),
    (S(19.70), S(22.30), "take", dict(src=brv(19), ss=1.2, vel=1.0)),
    (S(22.30), S(28.30), "selfie", dict(zoom=1.0)),
    (S(28.30), S(31.00), "selfie", dict(zoom=1.13)),
    (S(31.00), SAC0, "take", dict(src=TK / "salao_cheio_v2.mp4", ss=0.0, vel=1.0)),
    (SAC0, S(40.45), "sac", dict(zoom=1.0)),
    (S(40.45), S(43.40), "sac", dict(zoom=1.12)),
    (S(43.40), S(47.90), "take", dict(src=TK / "medalla.mp4", ss=0.3, vel=1.0)),
    (S(47.90), S(52.35), "sac", dict(zoom=1.0)),
    (S(52.35), S(56.30), "take", dict(src=brv(14), ss=0.5, vel=1.0)),
    (S(56.30), S(61.15), "take", dict(src=brv(35), ss=0.1, vel=1.0)),
    (S(61.15), S(65.00), "sac", dict(zoom=1.12)),
    (S(65.00), S(69.20), "take", dict(src=brv(26), ss=0.4, vel=1.0)),
    (S(69.20), S(72.70), "sac", dict(zoom=1.0)),
    (S(72.70), S(77.00), "take", dict(src=brv(32), ss=0.4, vel=1.0)),
    (S(77.00), S(81.80), "sac", dict(zoom=1.12)),
    (S(81.80), S(85.60), "sac", dict(zoom=1.0)),
    (S(85.60), S(89.00), "take", dict(src=brv(31), ss=0.8, vel=1.0)),
    (S(89.00), S(92.50), "take", dict(src=brv(44), ss=0.8, vel=1.0)),
    (S(92.50), S(95.35), "sac", dict(zoom=1.0)),
    (S(95.35), S(98.50), "sac", dict(zoom=1.12)),
    (S(98.50), S(101.00), "sac", dict(zoom=1.0)),
    (S(101.00), S(104.00), "take", dict(src=brv(55), ss=0.8, vel=1.0)),
    (S(104.00), S(108.30), "sac", dict(zoom=1.12)),
    (S(108.30), S(110.80), "take", dict(src=brv(50), ss=1.0, vel=1.0)),
    (S(110.80), S(113.10), "sac", dict(zoom=1.0)),
    (S(113.10), TOTAL, "sac", dict(zoom=1.12)),
]

# cartões do latim (T_ini, T_fim, png, y)
CARTOES = [
    (S(43.40), S(47.90), "latim_01.png", 110),
    (S(47.90), S(52.35), "latim_02.png", 110),
    (S(52.35), S(56.30), "latim_03.png", 110),
    (S(56.30), S(61.15), "latim_04.png", 110),
    (S(61.15), S(65.00), "latim_05.png", 110),
    (S(65.00), S(69.20), "latim_lista_6.png", 0),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(" ".join(map(str, cmd))[:3000]); print(r.stderr[-3000:]); sys.exit(1)
    return r


def nfr(a, b):
    return round(b * FPS) - round(a * FPS)


def crop_zoom(z, centro, W=1080, H=1920):
    if z <= 1.0:
        return ""
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    x = int(min(max(centro[0] - cw / 2, 0), W - cw)); y = int(min(max(centro[1] - ch / 2, 0), H - ch))
    return f"crop={cw}:{ch}:{x}:{y},"


def render(i, a, b, tipo, kw):
    out = M / f"seg_{i:02d}.mp4"
    n = nfr(a, b)
    base = "scale=1080:1920:flags=lanczos,setsar=1"
    moldura = False
    if tipo == "take":
        vel = kw.get("vel", 1.0)
        dur_src = n / FPS * vel + 0.2
        tempo = f"setpts=(PTS-STARTPTS)/{vel},"
        fr = "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if kw.get("interp") else "fps=30,"
        vf = tempo + fr + crop_zoom(kw.get("zoom", 1.0), kw.get("centro", (540, 960))) + base
        inp = ["-ss", f"{kw['ss']:.3f}", "-t", f"{dur_src:.3f}", "-i", str(kw["src"])]
    elif tipo == "selfie":
        loc = a - SELF0
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SELF) + base
        inp = ["-ss", f"{loc:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(SELFIE)]
    else:  # sac
        loc = a - SAC0
        fim = b - SAC0
        parte = next(p for p in SAC_PARTES if p[0] <= loc + 1e-6 < p[1])
        assert fim <= parte[1] + 0.05 or parte is SAC_PARTES[-1], (i, loc, fim, parte)
        vf = "fps=30," + crop_zoom(kw["zoom"], ROSTO_SAC) + base
        inp = ["-ss", f"{loc - parte[0]:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", str(parte[2])]
        moldura = True
    vf += ",tpad=stop_mode=clone:stop_duration=2"
    if moldura:
        cmd = ["ffmpeg", "-v", "error", "-y", *inp, "-i", str(GR / "moldura_envivo.png"), "-filter_complex",
               f"[0:v]{vf}[b];[1:v]format=rgba[m];[b][m]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]"]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", *inp, "-vf", vf + ",format=yuv420p"]
    cmd += ["-frames:v", str(n), "-an", "-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "12",
            "-pix_fmt", "yuv420p", "-x264-params", "keyint=60",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", str(out)]
    run(cmd)
    return out, n


def audio():
    SR = 48000

    def load(p, af=None):
        cmd = ["ffmpeg", "-v", "error", "-i", str(p)] + (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
        return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()

    voz = load(AQ / "voz" / "narracao_completa.mp3")
    reza = load(AQ / "voz" / "narracao_completa.mp3", f"atrim=0:{C},aecho=0.8:0.5:45|95:0.22|0.12")
    nC = int(C * SR)
    reza = reza[:nC]
    out_v = np.concatenate([reza, np.zeros((int(G * SR), 2), np.float32), voz[nC:]])
    n = int(TOTAL * SR)
    out_v = np.pad(out_v, ((0, max(0, n - len(out_v))), (0, 0)))[:n]
    tr = load(AQ / "audio" / "trilha.wav")
    tr = np.pad(tr, ((0, max(0, n - len(tr))), (0, 0)))[:n]
    t = np.arange(n) / SR
    # envelope da trilha (dB): base 0 (= -32 LUFS); sobe +9 dB no salão cheio; leve +3 dB no CTA
    db = np.zeros(n)
    sw = (t >= C - 0.6) & (t < SELF0 + 0.8)
    x = np.clip(np.minimum((t - (C - 0.6)) / 0.9, (SELF0 + 0.8 - t) / 1.2), 0, 1)
    db[sw] = 9 * x[sw]
    db += 3 * np.clip((t - CTA_T) / 1.5, 0, 1)
    mix = out_v + tr * (10 ** (db / 20))[:, None]
    raw = M / "mix.f32"; raw.write_bytes(mix.astype(np.float32).tobytes())
    # loudnorm 2 passadas (linear)
    r = run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af",
             "loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-2.5:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']},"
          f"alimiter=limit=0.74:level=false,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", af,
         "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", str(M / "mix.wav")])
    raw.unlink()
    print("audio ok", js["input_i"], "->", "-14")


def final():
    run([sys.executable, str(AQ / "legenda_final.py")])
    fonts = M / "fonts"
    if not fonts.exists():
        fonts.mkdir()
        for f in (AQ / "fonts").glob("*.ttf"):
            (fonts / f.name).write_bytes(f.read_bytes())
    ins = ["-reinit_filter", "0", "-i", "corpo.mp4", "-i", "mix.wav"]
    pngs = [("selo_ficticio.png", 0, TOTAL, 0), ("titulo_gancho.png", 0, 6.30, 0)] + \
           [(p, a, b, y) for a, b, p, y in CARTOES] + [("cta_vermas.png", CTA_T, TOTAL, 0)]
    fc = []; ult = "[0:v]"
    for k, (p, a, b, y) in enumerate(pngs):
        ins += ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL + 1:.3f}", "-i", str(GR / p)]
        idx = k + 2
        fc.append(f"[{idx}:v]format=rgba[p{k}]")
    # legenda antes dos gráficos (CTA e selo por cima)
    fc.append(f"{ult}ass=leg_final.ass:fontsdir=fonts[l]"); ult = "[l]"
    ordem = list(range(1, len(pngs))) + [0]  # selo por último
    for j, k in enumerate(ordem):
        p, a, b, y = pngs[k]
        en = "" if (a <= 0 and b >= TOTAL) else f":enable='between(t,{a:.3f},{b - 0.001:.3f})'"
        fc.append(f"{ult}[p{k}]overlay=0:{y}:format=auto{en}[o{j}]"); ult = f"[o{j}]"
    fc.append(f"{ult}format=yuv420p[v]")
    cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "1:a", "-af", "apad",
           "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-r", "30", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
           "-t", f"{TOTAL:.3f}", str(SAIDA)]
    r = subprocess.run(cmd, cwd=M, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-3000:]); sys.exit(1)
    print("final ok", SAIDA)


if __name__ == "__main__":
    so_audio = "--so-audio" in sys.argv
    so_final = "--so-final" in sys.argv
    json.dump([dict(i=i, ini=round(a, 3), fim=round(b, 3), tipo=t, **{k: str(v) for k, v in kw.items()})
               for i, (a, b, t, kw) in enumerate(SEG)], open(M / "mapa_cenas.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    if not so_audio and not so_final:
        # checa continuidade
        for (a, b, *_), (c, *_) in zip(SEG, SEG[1:]):
            assert abs(b - c) < 1e-6, (b, c)
        lista = []
        tot = 0
        for i, (a, b, t, kw) in enumerate(SEG):
            out, n = render(i, a, b, t, kw); lista.append(out); tot += n
            print(f"[{i + 1}/{len(SEG)}] {t:6s} {a:7.2f}-{b:7.2f} {n} quadros", flush=True)
        assert tot == round(TOTAL * FPS), (tot, TOTAL * FPS)
        (M / "lista.txt").write_text("".join(f"file '{p.name}'\n" for p in lista), encoding="utf-8")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(M / "lista.txt"), "-c", "copy", str(M / "corpo.mp4")])
    if not so_final:
        audio()
    if not so_audio:
        final()
