# -*- coding: utf-8 -*-
"""Renderiza cada cena do plano a partir da base limpa -> mont/cena_KK.mp4 (n quadros exatos, sem áudio).
Uso: python render_cenas.py [k ...]"""
import sys, subprocess, json
from pathlib import Path
import plano
AQ = Path(__file__).resolve().parent; M = AQ / "mont"; M.mkdir(exist_ok=True)
BASE = AQ / "lama" / "base_limpa.mp4"
TAG = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
POST = (0, 297, 720, 838)      # área do vídeo dentro da moldura do post (zoom só aqui)
CENTRO_ZOOM = {"aurA": (430, 420), "aurB": (430, 420)}   # centro do zoom (px no quadro)

def cmd_cena(c, out):
    ins, fc, labs = [], [], []
    for j, p in enumerate(c["pecas"]):
        dur = p["n"] / 30 * c["vel"] + 0.25
        ins += ["-ss", f"{p['a']:.3f}", "-t", f"{dur:.3f}", "-i", str(BASE)]
        v = f"[{j}:v]setpts=(PTS-STARTPTS)/{c['vel']},fps=30"
        if p["zoom"] > 1.0:
            x, y, w, h = POST; z = p["zoom"]; cx, cy = CENTRO_ZOOM.get(p["nome"], (360, 700))
            cw, ch = int(w / z) // 2 * 2, int(h / z) // 2 * 2
            x0 = int(min(max(cx - cw / 2, x), x + w - cw)); y0 = int(min(max(cy - ch / 2, y), y + h - ch))
            v += f",split[b{j}][z{j}];[z{j}]crop={cw}:{ch}:{x0}:{y0},scale={w}:{h}:flags=lanczos[zz{j}];[b{j}][zz{j}]overlay={x}:{y}"
        v += f",trim=end_frame={p['n']},setpts=PTS-STARTPTS[v{j}]"
        fc.append(v); labs.append(f"[v{j}]")
    fc.append("".join(labs) + f"concat=n={len(labs)}:v=1:a=0,format=yuv420p[v]")
    return ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-frames:v", str(c["n"]),
            "-r", "30", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *TAG, str(out)]

if __name__ == "__main__":
    S = plano.segmentos(); ks = [int(x) for x in sys.argv[1:]] or range(len(S))
    for k in ks:
        c = S[k]
        if c.get("chat"): continue
        out = M / f"cena_{k:02d}.mp4"
        r = subprocess.run(cmd_cena(c, out), capture_output=True, text=True)
        if r.returncode: print(k, r.stderr[-1500:]); sys.exit(1)
        n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout)
        print(f"[{k+1}/{len(S)}] cena {k:02d} {c['desc']}: {n}/{c['n']} quadros{'' if n == c['n'] else '  !!!'}", flush=True)
    json.dump(S, open(M / "segmentos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
