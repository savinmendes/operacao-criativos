# -*- coding: utf-8 -*-
"""Grupo B (rosto do criador) -> corpo 720x1280 com avatar HeyGen + takes do original SEM o rosto.
  python montar_corpo_b.py plano.json [--placeholder]

plano.json:
{
 "original": ".../originais/01.mp4",
 "avatar": "av.mp4",                 # vídeo HeyGen (lipsync da narração inteira, mesmo tempo da narração)
 "avatar_img": "../avatar_masculino.webp",   # usado com --placeholder (antes do HeyGen ficar pronto)
 "narr": "narr.mp3",
 "cauda": 0.5,                       # segundos de avatar depois do fim da fala
 "P": {"x":132,"y":470,"w":456,"faixa":[575,680]},      # take cheio: recorte 9:16 abaixo do rosto + faixa opaca (coords 720p)
 "S": {"av_y":60,"av_h":835,"src_y":530,"src_h":420},   # tela dividida: avatar em cima, recorte do original embaixo
 "segs": [["A",0,4.6], ["P",4.6,6.85,5.6], ["S",6.85,9,3.0,0.9]]   # tipo, ini, fim, [src_ini, [vel]]
}
"""
import json
import subprocess
import sys
from pathlib import Path

PL = Path(sys.argv[1]).resolve()
D = PL.parent
R = json.load(open(PL, encoding="utf-8"))
PH = "--placeholder" in sys.argv
W, H, FPS = 720, 1280, 30
TMP = D / "segs"
TMP.mkdir(exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), "-threads", "4"]


def run(cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


narr = D / R["narr"]
total = dur(narr) + R.get("cauda", 0.5)
segs = [list(s) for s in R["segs"]]
segs[-1][2] = total            # último segmento vai até o fim (cauda)

# entrada do avatar (vídeo real ou a foto parada)
if PH:
    av_in = ["-loop", "1", "-framerate", str(FPS), "-i", str((D / R["avatar_img"]).resolve())]
else:
    av_in = ["-i", str(D / R["avatar"])]
av_base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS}"

lista = []
for k, s in enumerate(segs):
    tipo, a, b = s[0], float(s[1]), float(s[2])
    d = b - a
    out = TMP / f"s{k:02d}.mp4"
    if tipo == "A":
        ss = ["-ss", f"{a:.3f}"] if not PH else []
        z = R.get("A_zoom", 1.0)
        vfa = av_base if z == 1.0 else (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                                        f"scale={round(W * z / 2) * 2}:{round(H * z / 2) * 2},crop={W}:{H}:(iw-{W})/2:{R.get('A_shift', 0)},setsar=1,fps={FPS}")
        vfa += ",tpad=stop_mode=clone:stop_duration=2"      # avatar termina junto com a fala: congela o último quadro na cauda
        run(["ffmpeg", "-v", "error", "-y", *ss, *av_in, "-vf", vfa, "-t", f"{d:.3f}", "-an", *ENC, out])
    else:
        src0 = float(s[3])
        vel = float(s[4]) if len(s) > 4 else 1.0
        need = d * vel + 0.1
        if tipo == "P":
            p = {**R["P"], **(s[5] if len(s) > 5 else {})}
            h = round(p["w"] * 16 / 9)
            y = min(p["y"], 1280 - h)
            vf = f"[0:v]setpts=(PTS-STARTPTS)/{vel},crop={p['w']}:{h}:{p['x']}:{y},scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
            if p.get("faixa"):
                vf += f"[v0];[v0]drawbox=x=0:y={p['faixa'][0]}:w={W}:h={p['faixa'][1] - p['faixa'][0]}:color=black@0.99:t=fill[v]"
            else:
                vf += "[v]"
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{src0:.3f}", "-t", f"{need:.3f}", "-i", R["original"],
                 "-filter_complex", vf, "-map", "[v]", "-t", f"{d:.3f}", "-an", *ENC, out])
        elif tipo == "S":
            p = {**R["S"], **(s[5] if len(s) > 5 else {})}
            ah, sh = p["av_h"], H - p["av_h"]
            # recorte do original com largura cheia, altura src_h, escalado p/ altura sh (zoom leve se precisar)
            sw = round(W * p["src_h"] / sh)
            sx = p.get("src_x", (720 - sw) // 2)
            ss = ["-ss", f"{a:.3f}"] if not PH else []
            fc = (f"[0:v]{av_base},crop={W}:{ah}:0:{p['av_y']}[top];"
                  f"[1:v]setpts=(PTS-STARTPTS)/{vel},crop={sw}:{p['src_h']}:{sx}:{p['src_y']},scale={W}:{sh}:flags=lanczos,setsar=1,fps={FPS}[bot];"
                  f"[top][bot]vstack[v]")
            run(["ffmpeg", "-v", "error", "-y", *ss, *av_in, "-ss", f"{src0:.3f}", "-t", f"{need:.3f}", "-i", R["original"],
                 "-filter_complex", fc, "-map", "[v]", "-t", f"{d:.3f}", "-an", *ENC, out])
    lista.append(out)
    print(f"[{k + 1}/{len(segs)}] {tipo} {a:.2f}-{b:.2f}", flush=True)

txt = TMP / "lista.txt"
txt.write_text("".join(f"file '{p.as_posix()}'\n" for p in lista), encoding="utf-8")
saida = D / ("corpo_placeholder.mp4" if PH else "corpo.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-i", narr,
     "-filter_complex", f"[1:a]aresample=48000,apad=whole_dur={total:.3f}[a]", "-map", "0:v", "-map", "[a]",
     *ENC, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.3f}", saida])
print(f"ok {saida} | {dur(saida):.2f}s (fala {dur(narr):.2f}s)")
