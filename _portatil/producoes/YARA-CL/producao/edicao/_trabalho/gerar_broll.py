# -*- coding: utf-8 -*-
"""B-roll das narracoes (b_yara/b_moi/b_elixir.mp4, 720x1280 30 fps, sem audio, 7 s) a partir do banco de takes reais.
So ffmpeg (sem cv2: nao ha leitura/regravacao em RGB, a matriz bt709/tv das fontes e mantida e etiquetada).
Cada take: recorte opcional (caixa relativa, p/ close de detalhe ou p/ tirar legenda queimada) ->
zoom z0->z1 ao longo do take (punch-in animado ou fixo) + "snap" de zoom rapido nos 0,2 s iniciais do corte.
Uso: python gerar_broll.py [edl_broll.json]"""
import json, subprocess, sys
from pathlib import Path

ED = Path(r"C:\Users\PICHAU\Downloads\YARA-CL\producao\edicao")
BANCO = Path(r"C:\Users\PICHAU\Downloads\YARA-CL\banco")
FPS, W, H = 30, 720, 1280
COR = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
SNAP, SNAP_T = 0.10, 0.20


def take_vf(t):
    dur = t["dur"]
    vf = []
    if t.get("caixa"):                      # [x, y, w, h] relativos (0-1) do quadro 720x1280
        x, y, w, h = t["caixa"]
        vf.append(f"crop=iw*{w}:ih*{h}:iw*{x}:ih*{y}")
    # sobe a resolucao interna p/ o zoompan nao "tremer" por arredondamento
    vf.append("scale=1440:2560:flags=lanczos,setsar=1")
    z0, z1 = t.get("z0", 1.0), t.get("z1", t.get("z0", 1.0))
    n = max(1, round(dur * FPS))
    z = (rf"({z0}+({z1}-{z0})*on/{n})*(1+{SNAP}*pow(max(0\,1-on/{SNAP_T * FPS})\,2))")
    cx, cy = t.get("centro", [0.5, 0.5])
    vf.append(f"zoompan=z='{z}':d=1:fps={FPS}:s={W}x{H}:"
              rf"x='max(0\,min(iw-iw/zoom\,iw*{cx}-iw/zoom/2))':y='max(0\,min(ih-ih/zoom\,ih*{cy}-ih/zoom/2))'")
    vf.append("format=yuv420p")
    return ",".join(vf)


def render(nome, takes, total):
    tmp = ED / "_trabalho" / "broll_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    partes = []
    for i, t in enumerate(takes):
        p = tmp / f"{nome}_{i:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t.get("ini", 0)), "-t", str(t["dur"] + 0.1),
                        "-i", str(BANCO / t["take"]), "-an", "-vf", take_vf(t), "-frames:v", str(round(t["dur"] * FPS)),
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-r", str(FPS), *COR, str(p)], check=True)
        partes.append(p)
    lista = tmp / f"{nome}_lista.txt"
    lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes), encoding="utf-8")
    out = ED / f"{nome}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-an",
                    "-vf", f"fps={FPS},trim=duration={total},setpts=PTS-STARTPTS,format=yuv420p",
                    "-c:v", "libx264", "-crf", "17", "-preset", "medium", *COR, str(out)], check=True)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                       capture_output=True, text=True).stdout.strip()
    print(nome, "->", out.name, d, "s")


if __name__ == "__main__":
    edl = json.load(open(sys.argv[1] if len(sys.argv) > 1 else ED / "edl_broll.json", encoding="utf-8"))
    for nome, seq in edl["sequencias"].items():
        render(nome, seq["takes"], edl.get("duracao", 7.0))
