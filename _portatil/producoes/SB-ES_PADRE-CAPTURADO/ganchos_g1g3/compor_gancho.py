# -*- coding: utf-8 -*-
"""Monta um gancho no layout do gancho do v4 (720x1280): faixa preta de topo com título amarelo (Open Sans),
vídeo na janela y 248-1165, legenda em caixa palavra a palavra (maiúsculas, palavra falada amarela) na faixa de baixo,
selo VIDEO FICTICIO por cima de tudo. Cor lida/gravada com matriz bt601 fixa (lição do lote Oración).
uso: python compor_gancho.py cfg.json
cfg: {"video": take.mp4, "ss": 0.0, "dur": 7.5, "src_y": 0.5 (centro da janela no take, 0-1), "zoom": 1.0,
      "audio": mix.wav, "palavras": [{"w","ini","fim"}], "titulo": ["L1","L2"], "out": gancho.mp4}"""
import sys, json, re, subprocess
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 720, 1280, 30
JY0, JY1 = 248, 1165                     # janela do vídeo (igual ao gancho do v4)
OS = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
SELO = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\visual\overlays\selo_ficticio_mini_es.png"
ENC_VF = "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
def fonte(sz, peso):
    f = ImageFont.truetype(OS, sz); f.set_variation_by_name(peso); return f
F_T = fonte(42, "Regular"); F_L = fonte(46, "SemiBold")
SELO_OPAC = 0.10                 # pedido da pessoa (19/10): selo com 90% de transparência
AMARELO_T = (188, 202, 20, 255); AMARELO_L = (244, 242, 23, 255)

def titulo_png(linhas):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    L = Image.new("L", (W, H), 0); dl = ImageDraw.Draw(L)
    f = F_T
    while max(f.getlength(l) for l in linhas) > 680: f = fonte(f.size - 1, "Regular")
    bases = [184, 230] if len(linhas) == 2 else [207]
    for l, b in zip(linhas, bases): dl.text((W // 2, b), l, font=f, anchor="ms", fill=255)
    L = L.filter(ImageFilter.GaussianBlur(0.4))
    im.alpha_composite(Image.composite(Image.new("RGBA", (W, H), AMARELO_T), Image.new("RGBA", (W, H), (0, 0, 0, 0)), L))
    return im

def blocos(pal):
    out, cur = [], []
    for p in pal:
        cur.append(p); txt = " ".join(x["w"] for x in cur)
        if len(cur) >= 3 or len(txt) >= 16 or re.search(r"[,.:;!?]$", p["w"]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out

class Legenda:
    def __init__(self, pal, dur):
        bs = blocos(pal); self.bl = []
        for i, b in enumerate(bs):
            prox = bs[i + 1][0]["ini"] if i + 1 < len(bs) else dur
            fim = min(prox, b[-1]["fim"] + 0.6) if i + 1 < len(bs) else dur
            ws = [(re.sub(r"[,.:;!?¡¿]+", "", x["w"]).upper(), x["ini"]) for x in b]
            self.bl.append((b[0]["ini"], fim, ws))
    def em(self, t):
        for k, (a, z, ws) in enumerate(self.bl):
            if a <= t < z:
                at = max([i for i, (_, wi) in enumerate(ws) if wi <= t] or [0])
                return self.img(k, at)
        return None
    @lru_cache(maxsize=64)
    def img(self, k, at):
        ws = [w for w, _ in self.bl[k][2]]
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        esp = F_L.getlength(" "); lg = [F_L.getlength(w) for w in ws]; tot = sum(lg) + esp * (len(ws) - 1)
        base = 1226; x = W / 2 - tot / 2
        d.rounded_rectangle((int(x - 24), base - 36 - 15, int(x + tot + 24), base + 13 + 11), 18, fill=(14, 14, 14, 252))
        for i, (w, L) in enumerate(zip(ws, lg)):
            d.text((x, base), w, font=F_L, anchor="ls", fill=AMARELO_L if i == at else (255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
            x += L + esp
        return im

def quadros(p, ss, n, zoom, w=W, h=H):
    # take 9:16 qualquer -> 720x1280 (cover) * zoom, lido em bt601/tv fixo
    vf = (f"scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,"
          f"scale={int(w*zoom)}:{int(h*zoom)}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},fps={FPS},format=rgb24")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", p, "-vf", vf, "-frames:v", str(n), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    t = w * h * 3; last = None
    for _ in range(n):
        b = pr.stdout.read(t)
        if len(b) < t: yield last; continue   # take curto: segura o último (não deve acontecer; avisa no fim)
        last = np.frombuffer(b, np.uint8).reshape(h, w, 3); yield last
    pr.stdout.close(); pr.wait()

def main(cfg):
    dur = cfg["dur"]; n = int(round(dur * FPS))
    tit = titulo_png(cfg["titulo"]); selo = Image.open(SELO).convert("RGBA"); selo.putalpha(selo.getchannel("A").point(lambda a: round(a * SELO_OPAC)))
    leg = Legenda(cfg["palavras"], dur)
    jh = JY1 - JY0; cy = cfg.get("src_y", 0.5)
    y0s = int(np.clip(cy * H - jh / 2, 0, H - jh))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", cfg["audio"], "-map", "0:v", "-map", "1:a", "-vf", ENC_VF, "-c:v", "libx264", "-profile:v", "high", "-crf", "17",
                            "-preset", "slow", *ENC_TAG, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{dur:.3f}",
                            "-movflags", "+faststart", cfg["out"]], stdin=subprocess.PIPE)
    curto = 0
    janela = cfg.get("modo") == "janela"   # take não-9:16 (ex.: 3:4) preenche direto a janela 720x917
    for i, fr in enumerate(quadros(cfg["video"], cfg.get("ss", 0.0), n, cfg.get("zoom", 1.0), W, jh if janela else H)):
        if fr is None: raise SystemExit("take sem quadros")
        can = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        can.paste(Image.fromarray(fr if janela else fr[y0s:y0s + jh]).convert("RGBA"), (0, JY0))
        can.alpha_composite(tit)
        l = leg.em(i / FPS)
        if l is not None: can.alpha_composite(l)
        can.alpha_composite(selo)
        enc.stdin.write(np.asarray(can.convert("RGB")).tobytes())
    enc.stdin.close(); enc.wait()
    print("ok", cfg["out"], n, "quadros")

if __name__ == "__main__":
    main(json.load(open(sys.argv[1], encoding="utf-8")))
