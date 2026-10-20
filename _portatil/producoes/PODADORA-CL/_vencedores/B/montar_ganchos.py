# -*- coding: utf-8 -*-
"""Vencedor B (ORILLA): monta o visual de cada gancho (cenas escolhidas a dedo, quadros exatos, 576x1024 30 fps),
gera banco/config para gerar_variacao.py montar (modo A, trecho fixo = visual pronto) e roda.
  python montar_ganchos.py [B1 B2 ...]
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageFilter

D = Path(__file__).resolve().parent
SRC = str((D.parent / "vencedor1.mp4").resolve())
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
W, H, FPS = 576, 1024, 30
CORTE = 2.1           # fim de "Ya ni se veía la orilla, sigue viendo." (1.92) / início de "Mira," (2.26)
VOZ_LUFS = -14.3      # nível da voz original (stem vocals do demucs)
LEAD = 0.30

# gancho: (texto na tela, nome, [segmentos]) ; segmento = (ini, n_quadros) | ("freeze", t, n) | ("kit", n)
G = {
    "B1": ("YA NI SE VEÍA 😳", "YA-NI-SE-VEIA", [(0.00, 36), (19.50, 33), (22.40, 22)]),
    "B2": ("¿CONTRATASTE A ALGUIEN?", "VECINOS", [(18.40, 51), (22.40, 22), (21.60, 18)]),
    "B3": ("SOLA. EN UNA TARDE.", "SOLA", [(16.45, 50), (32.60, 37)]),
    "B4": ("¿TU PATIO SE VE ASÍ?", "TU-PATIO", [("freeze", 0.0, 30), (0.00, 63)]),
    "B5": ("LA ORILLA PERFECTA", "ORILLA-PERFECTA", [(11.40, 42), (20.00, 66)]),
    "B6": ("VALIÓ LA PENA ✅", "VALIO-LA-PENA", [("kit", 86), (16.45, 24), (21.45, 22), (6.25, 16)]),
}


def run(cmd):
    subprocess.run([str(c) for c in cmd], check=True, capture_output=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def lufs(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


ENC = ["-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", "-an"]


def kit_clip(n, out):
    """Foto do kit: fundo ampliado/desfocado 9:16 + foto inteira no centro com zoom lento (1.00 -> 1.08)."""
    fr = D / "kit_frames"
    fr.mkdir(exist_ok=True)
    im = Image.open(D.parent / "produto_kit.webp").convert("RGB")
    s = H / im.height
    bg = im.resize((int(im.width * s), H), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(28))
    bg = Image.eval(bg, lambda v: int(v * 0.85))
    for k in range(n):
        z = 1.0 + 0.08 * k / max(1, n - 1)
        fw = int(W * 0.98 * z)
        fg = im.resize((fw, int(im.height * fw / im.width)), Image.LANCZOS)
        f = bg.copy()
        f.paste(fg, ((W - fg.width) // 2, int(H * 0.56 - fg.height / 2)))
        f.save(fr / f"{k:04d}.png")
    run(["ffmpeg", "-y", "-framerate", FPS, "-i", fr / "%04d.png", "-frames:v", n, *ENC, out])


def visual(nome, segs):
    T = D / "trab" / nome
    T.mkdir(parents=True, exist_ok=True)
    partes = []
    for k, s in enumerate(segs):
        o = T / f"s{k}.mp4"
        if s[0] == "kit":
            kit_clip(s[1], o)
        elif s[0] == "freeze":
            run(["ffmpeg", "-y", "-ss", f"{s[1]:.3f}", "-i", SRC, "-frames:v", 1, T / "fz.png"])
            run(["ffmpeg", "-y", "-loop", 1, "-framerate", FPS, "-i", T / "fz.png", "-frames:v", s[2],
                 "-vf", f"scale={W}:{H},setsar=1", *ENC, o])
        else:
            run(["ffmpeg", "-y", "-ss", f"{s[0]:.3f}", "-i", SRC, "-frames:v", s[1],
                 "-vf", f"fps={FPS},scale={W}:{H},setsar=1", *ENC, o])
        partes.append(o)
    n = len(partes)
    ins = [x for p in partes for x in ("-i", p)]
    fc = "".join(f"[{i}:v]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    out = T / "visual.mp4"
    run(["ffmpeg", "-y", *ins, "-filter_complex", fc, "-map", "[v]", *ENC, out])
    nq = sum(s[-1] if s[0] in ("kit", "freeze") else s[1] for s in segs)
    return out, nq


def main():
    alvo = sys.argv[1:] or list(G)
    bed = D / "bed.wav"
    if not bed.exists():
        run(["ffmpeg", "-y", "-i", D / "sep/htdemucs/v1/no_vocals.wav", "-t", f"{CORTE:.3f}", bed])
    for nome in alvo:
        txt, slug, segs = G[nome]
        vis, nq = visual(nome, segs)
        Hd = nq / FPS
        fala = D / "voz" / f"{nome}.mp3"
        df = dur(fala)
        assert LEAD + df <= Hd + 1e-3, f"{nome}: fala {df:.2f}s não cabe em {Hd:.2f}s"
        ganho = round(VOZ_LUFS - lufs(fala), 2)
        T = D / "trab" / nome
        json.dump({"video": str(vis), "tomadas": []}, open(T / "banco_g.json", "w", encoding="utf-8"))
        cfg = {
            "saida": str(D.parent.parent / "VENCEDORES" / f"{nome} - ORILLA-{slug}-ES-CL.mp4"),
            "resolucao": "720", "limite_mb": 30, "trab": str(T / "gv"),
            "bancos": {"g": str(T / "banco_g.json")},
            "gancho": {"trecho": ["g", 0, round(Hd, 4)], "fala": str(fala), "lead": LEAD, "cauda": 0.0,
                       "caixa_fixa": {"linhas": [txt], "px": 64, "cy": 240, "de": 0, "ate": round(Hd + 1, 3)},
                       "fundo": str(bed), "fundo_vol": 1.0},
            "corpo": {"video": SRC, "corte": CORTE, "ganho_db": ganho},
        }
        cp = T / f"{nome}.json"
        json.dump(cfg, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[{nome}] gancho {Hd:.3f}s ({nq} q) | fala {df:.2f}s | ganho {ganho:+.2f} dB", flush=True)
        r = subprocess.run([sys.executable, str(KIT / "ferramentas" / "gerar_variacao.py"), "montar", str(cp)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(KIT),
                           env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
        print(r.stdout[-600:], r.stderr[-1500:] if r.returncode else "", flush=True)


if __name__ == "__main__":
    main()
