# -*- coding: utf-8 -*-
"""Lote 3: prepara as entradas do HeyGen.
Para cada trecho: in/v_<id>.mp4 = video do ORIGINAL (orig_ini-orig_fim) com o AUDIO ES original, ambos esticados pelo
mesmo fator (setpts + atempo), N quadros exatos (N = round(novo_fim*30) - round(novo_ini*30)); pulpito = recorte do
rosto 360x480 ampliado 2x. base/<id>.mp4 = mesmo video sem recorte e sem audio (fundo para colar a boca).
in/a_<id>.mp3 = narracao DE de novo_ini a novo_fim (mesmos quadros).
Uso: python prep.py [id ...]"""
import json, subprocess, sys
from pathlib import Path

W = Path(__file__).resolve().parent
T = W.parents[1]
SRC = r"C:\Users\PICHAU\Downloads\Lead 2.mp4"
NARR = T / "voz" / "narracao_de_completa.wav"
L = json.load(open(T / "voz" / "lotes.json", encoding="utf-8"))
SEC = json.load(open(T / "voz" / "timeline_de.json", encoding="utf-8"))["secoes_video"]
CROP_PULPITO = (200, 0, 360, 480)   # x, y, w, h -> 720x960
COR = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]


def pecas(t):
    """[(o0, o1, fator)] dividindo o trecho nas fronteiras das secoes de video."""
    if not isinstance(t["fator"], list):
        return [(t["orig_ini"], t["orig_fim"], t["fator"])]
    out = []
    for s in SEC:
        a, b = max(t["orig_ini"], s["src_ini"]), min(t["orig_fim"], s["src_fim"])
        if b - a > 1e-3:
            out.append((a, b, s["fator"]))
    return out


def preparar(t):
    i = t["id"]
    n = round(t["novo_fim"] * 30) - round(t["novo_ini"] * 30)
    pc = pecas(t)
    fc, vs, as_ = [], [], []
    for k, (a, b, f) in enumerate(pc):
        fc.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)*{f}[v{k}]")
        fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={1/f:.6f}[a{k}]")
        vs.append(f"[v{k}]"); as_.append(f"[a{k}]")
    fc.append("".join(vs) + f"concat=n={len(pc)}:v=1:a=0,fps=30,tpad=stop_mode=clone:stop_duration=1,trim=end_frame={n},setpts=N/30/TB[vb]")
    fc.append("".join(as_) + f"concat=n={len(pc)}:v=0:a=1,apad,atrim=end={n/30:.4f}[ab]")
    fc.append("[vb]split[vx][vy]")
    pul = t["cena"] == "padre_pulpito"
    if pul:
        x, y, w, h = CROP_PULPITO
        fc.append(f"[vx]crop={w}:{h}:{x}:{y},scale=720:960:flags=lanczos[vin]")
    else:
        fc.append("[vx]null[vin]")
    (W / "in").mkdir(exist_ok=True); (W / "base").mkdir(exist_ok=True)
    enc = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", *COR, "-threads", "4"]
    # -ss antes do -i desloca os tempos: ajusta os trims para o tempo relativo
    off = max(0, t["orig_ini"] - 2)
    fc2 = ";".join(fc)
    for (a, b, f) in pc:
        fc2 = fc2.replace(f"trim={a}:{b}", f"trim={a - off:.4f}:{b - off:.4f}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{off:.3f}", "-i", SRC, "-filter_complex", fc2,
                    "-map", "[vin]", "-map", "[ab]", *enc, "-c:a", "aac", "-b:a", "192k", str(W / "in" / f"v_{i}.mp4"),
                    "-map", "[vy]", *enc, "-an", str(W / "base" / f"{i}.mp4")], check=True)
    q0 = round(t["novo_ini"] * 30)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(NARR), "-af",
                    f"atrim={q0/30:.4f}:{(q0+n)/30:.4f},asetpts=PTS-STARTPTS", "-ac", "1", "-ar", "44100",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(W / "in" / f"a_{i}.mp3")], check=True)
    nq = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v",
                                      "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(W / "in" / f"v_{i}.mp4")]))
    print(i, t["cena"], "pecas", len(pc), "quadros", nq, "esperado", n, flush=True)
    return {"id": i, "n": n, "q0": q0, "pulpito": pul, "pecas": pc}


if __name__ == "__main__":
    so = set(sys.argv[1:])
    ts = [t for t in L["trechos"] if t["lote"] == 3 and (not so or t["id"] in so)]
    info = {}
    p = W / "prep.json"
    if p.exists():
        info = json.load(open(p, encoding="utf-8"))
    for t in ts:
        info[t["id"]] = preparar(t)
        json.dump(info, open(p, "w", encoding="utf-8"), indent=1)
