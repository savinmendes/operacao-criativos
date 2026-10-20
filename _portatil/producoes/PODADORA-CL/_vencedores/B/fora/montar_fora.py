# -*- coding: utf-8 -*-
"""Corpo B (ORILLA) - ganchos "fora da caixa" H1-H5 com takes IA (Flora: Nano Banana 2 + MiniMax H3 Max).
Monta o visual do gancho (720x1280, 30 fps) a partir dos takes e roda gerar_variacao.py montar
(mesma emenda/volume do montar_ganchos.py do B).   python montar_fora.py [H1 H2 ...]
"""
import json
import os
import subprocess
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
B = D.parent
SRC = str((B.parent / "vencedor1.mp4").resolve())
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
OUT = B.parent.parent / "VENCEDORES" / "FORA"
W, H, FPS = 720, 1280, 30
CORTE = 2.1
VOZ_LUFS = -14.3

# codigo: (texto na tela, slug, lead da fala, [(take, ini, fim)])
G = {
    "H1": ("ORILLA PERFECTA", "LA-ORILLA-IMPOSIBLE", 0.45, [("H1a", 0.0, 4.2)]),
    "H2": ("LA DIFERENCIA 😮", "VISTA-DE-DRON", 0.45, [("H2a", 0.0, 4.2)]),
    "H3": ("SIN CABLES", "SIN-CABLES", 0.35, [("H3b", 0.0, 4.3)]),
    "H4": ("2 BATERÍAS 🔋", "CAMBIO-DE-BATERIA", 0.30, [("H4a", 0.0, 2.8), ("H1a", 1.0, 2.5)]),
    "H5": ("LIVIANA Y CON RUEDAS", "MAMA-TAMBIEN-PUEDE", 0.45, [("H5a", 0.0, 4.2)]),
}
ENC = ["-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", "-an"]


def run(cmd):
    subprocess.run([str(c) for c in cmd], check=True, capture_output=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def lufs(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def visual(nome, segs):
    T = D / "trab" / nome
    T.mkdir(parents=True, exist_ok=True)
    partes, nq = [], 0
    for k, (take, ini, fim) in enumerate(segs):
        n = round((fim - ini) * FPS)
        o = T / f"s{k}.mp4"
        run(["ffmpeg", "-y", "-ss", f"{ini:.3f}", "-i", D / "takes" / f"{take}.mp4", "-frames:v", n, "-vf",
             f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1", *ENC, o])
        partes.append(o)
        nq += n
    ins = [x for p in partes for x in ("-i", p)]
    fc = "".join(f"[{i}:v]" for i in range(len(partes))) + f"concat=n={len(partes)}:v=1:a=0[v]"
    out = T / "visual.mp4"
    run(["ffmpeg", "-y", *ins, "-filter_complex", fc, "-map", "[v]", *ENC, out])
    return out, nq


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bed = B / "bed.wav"
    for nome in sys.argv[1:] or list(G):
        txt, slug, lead, segs = G[nome]
        vis, nq = visual(nome, segs)
        Hd = nq / FPS
        fala = D / "voz" / f"{nome}.mp3"
        df = dur(fala)
        assert lead + df <= Hd + 1e-3, f"{nome}: fala {df:.2f}s não cabe em {Hd:.2f}s"
        ganho = round(VOZ_LUFS - lufs(fala), 2)
        T = D / "trab" / nome
        json.dump({"video": str(vis), "tomadas": []}, open(T / "banco_g.json", "w", encoding="utf-8"))
        cfg = {
            "saida": str(OUT / f"{nome} - {slug}-B-ES-CL.mp4"),
            "resolucao": "720", "limite_mb": 30, "trab": str(T / "gv"),
            "bancos": {"g": str(T / "banco_g.json")},
            "gancho": {"trecho": ["g", 0, round(Hd, 4)], "fala": str(fala), "lead": lead, "cauda": 0.0,
                       "caixa_fixa": {"linhas": [txt], "px": 64, "cy": 240, "de": 0, "ate": round(Hd + 1, 3)},
                       "fundo": str(bed), "fundo_vol": 1.0},
            "corpo": {"video": SRC, "corte": CORTE, "ganho_db": ganho},
        }
        cp = T / f"{nome}.json"
        json.dump(cfg, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[{nome}] gancho {Hd:.3f}s ({nq} q) | fala {df:.2f}s lead {lead} | ganho {ganho:+.2f} dB", flush=True)
        r = subprocess.run([sys.executable, str(KIT / "ferramentas" / "gerar_variacao.py"), "montar", str(cp)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(KIT),
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        print(r.stdout[-600:], r.stderr[-1500:] if r.returncode else "", flush=True)


if __name__ == "__main__":
    main()
