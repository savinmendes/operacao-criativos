# -*- coding: utf-8 -*-
"""F6 - Kit "explodido" 3D (corpo B).
Gancho 4,0 s: take IA (Flora: Nano Banana 2 a partir da foto do kit + MiniMax H3 i2v, push-in com as peças ao redor),
narração "Mira todo lo que trae la caja…" (voz clonada da narradora B) e caixa "TODO ESTO EN LA CAJA 📦".
Depois o vencedor1 intacto a partir de 2,100 s, pelo mesmo caminho do montar_ganchos.py do B (gerar_variacao.py montar)."""
import json
import os
import subprocess
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
B = D.parent / "B"
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
SRC = str((D.parent / "vencedor1.mp4").resolve())
CLIP = D / "takes" / "F6_kit_v1.mp4"
FALA = D / "voz" / "F6.mp3"
T = D / "trab" / "F6"
CORTE, VOZ_LUFS, LEAD, FPS = 2.1, -14.3, 0.50, 30
NQ = 120                      # 4,0 s de gancho
TEXTO = "TODO ESTO EN LA CAJA 📦"


def run(cmd):
    subprocess.run([str(c) for c in cmd], check=True, capture_output=True)


def lufs(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def main():
    T.mkdir(parents=True, exist_ok=True)
    vis = T / "visual.mp4"
    # 768x1344 (4:7) -> 720x1280 (9:16): escala para cobrir e corta 5 px de cada lado
    run(["ffmpeg", "-y", "-i", CLIP, "-an", "-frames:v", NQ, "-vf",
         f"fps={FPS},scale=-2:1280:flags=lanczos,crop=720:1280,setsar=1",
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", vis])
    Hd = NQ / FPS
    ganho = round(VOZ_LUFS - lufs(FALA), 2)
    json.dump({"video": str(vis), "tomadas": []}, open(T / "banco_g.json", "w", encoding="utf-8"))
    cfg = {
        "saida": str(D.parent.parent / "VENCEDORES" / "FORA" / "F6 - KIT-EXPLODIDO-B-ES-CL.mp4"),
        "resolucao": "720", "limite_mb": 30, "trab": str(T / "gv"),
        "bancos": {"g": str(T / "banco_g.json")},
        "gancho": {"trecho": ["g", 0, round(Hd, 4)], "fala": str(FALA), "lead": LEAD, "cauda": 0.0,
                   "caixa_fixa": {"linhas": ["TODO ESTO", "EN LA CAJA 📦"], "px": 60, "cy": 170, "de": 0, "ate": round(Hd + 1, 3)},
                   "fundo": str(B / "bed.wav"), "fundo_vol": 1.0},
        "corpo": {"video": SRC, "corte": CORTE, "ganho_db": ganho},
    }
    cp = T / "F6.json"
    json.dump(cfg, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[F6] gancho {Hd:.3f}s | ganho {ganho:+.2f} dB", flush=True)
    r = subprocess.run([sys.executable, str(KIT / "ferramentas" / "gerar_variacao.py"), "montar", str(cp)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(KIT),
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    print(r.stdout[-800:], r.stderr[-1500:] if r.returncode else "", flush=True)


if __name__ == "__main__":
    main()
