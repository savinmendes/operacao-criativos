# -*- coding: utf-8 -*-
"""Prepara o corpo de um criativo traduzido (vídeo em outro idioma -> narração nova), antes do montar_ad.py:
- recorta os trechos mantidos do original (cortes) e emenda;
- cobre a legenda queimada com faixa preta opaca (largura toda, borda em degradê) e/ou caixas opacas;
- cobre o título do topo / caixa de gancho com caixa branca nova com o texto traduzido (emoji colorido);
- faixa de aviso no rodapé com texto pequeno (aviso traduzido);
- desfoca regiões (rosto de terceiro, data na tela) com caixas/elipses por chave de tempo, interpoladas;
- troca o áudio: fundo sem voz (demucs no_vocals) + narração nova (inteira com atempo, por frases com offsets ou
  por blocos de caracteres) e grava alinhamento.json ajustado para a legenda do kit;
- congela o último quadro se a narração passar do vídeo (para caber o CTA).

  python preparar_corpo_traducao.py prep.json [--saida corpo.mp4]

prep.json (caminhos relativos à pasta do JSON; tempos em s; coordenadas em px da SAÍDA):
{
 "video": "original_01.mp4", "resolucao": "720",
 "cortes": [[0.133, 30.0], [41.0, 52.0]],          // trechos mantidos (tempo do ORIGINAL); omitido = inteiro
 "fundo": "sep/htdemucs/orig_01/no_vocals.wav",     // música sem voz alinhada ao original (null = sem fundo)
 "fundo_vol": 1.0,                                  // multiplicador do fundo
 "narr": "narr.mp3",                                // + narr.alinhamento.json (tts_elevenlabs.py)
 "narr_inicio": 0.3, "atempo": 1.0,                 // modo inteira: começa em narr_inicio, velocidade atempo
 "offsets": [0.1, 2.3, 6.2],                        // OU modo frases: início de cada frase (. ! ?) no tempo do corpo
 "blocos": [[0, 0.2], [135, 9.1]],                  // OU modo blocos: [índice do 1º caractere, instante]
 "narr_vol": 1.0,
 "trocas": [["Uais", "Marca"]],                     // correções de texto no alinhamento (mesmo tempo)
 "faixas": [{"y": [576, 696], "de": 0, "ate": 9999, "grad": 18}],          // faixa preta opaca, largura toda
 "caixas": [{"rect": [40, 900, 680, 1000], "cor": [0, 0, 0], "raio": 14, "de": 0, "ate": 9999}],
 "titulos": [{"linhas": ["¿Esta cámara sigue a las personas? 👀"], "px": 29, "cy": 235, "de": 0, "ate": 3,
              "cobrir_w": 0, "cobrir_h": 0, "negrito": true}],             // caixa branca com texto novo
 "aviso": {"linhas": ["Solo con fines demostrativos."], "topo": 1150, "px": 19},
 "desfocar": [{"de": 17.8, "ate": 21.97, "tipo": "blur", "forca": 61, "forma": "caixa",
               "chaves": [[17.8, 250, 50, 440, 240], [18.3, 290, 100, 480, 290]]}],
               // tipo blur|preto; forma caixa|elipse; chaves [t, x0, y0, x1, y1] interpoladas (tempo do corpo)
 "fim": {"folga": 0.5, "max_total": null},          // total = max(vídeo, fim da fala + folga), limitado a max_total
 "saida": "corpo.mp4"
}
Saída: corpo.mp4 (+ alinhamento.json ao lado) pronto para a receita do montar_ad.py
("legenda": {"fonte": "alinhamento:alinhamento.json"}).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from comum import COR, FONTS, FPS, dur, emoji_font, resolucao, run  # noqa: E402

FB, FM = str(FONTS / "Poppins-Bold.ttf"), str(FONTS / "Poppins-Medium.ttf")
ALFA = 255   # faixa/caixa opaca (só a borda tem degradê): abaixo de 250 o texto original aparece por baixo


def e_emoji(ch: str) -> bool:
    return ord(ch) > 0x2000 and ch not in "…–—“”‘’¡¿"


def png_faixa(y0, y1, W, H, destino, grad=18, cor=(0, 0, 0)):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(max(0, y0 - grad), min(H, y1 + grad)):
        if y0 <= y < y1:
            a = ALFA
        elif y < y0:
            a = int(ALFA * (y - (y0 - grad)) / grad)
        else:
            a = int(ALFA * ((y1 + grad) - y) / grad)
        d.line([(0, y), (W, y)], fill=tuple(cor) + (a,))
    img.save(destino)
    return str(destino)


def png_caixa(rect, W, H, destino, cor=(0, 0, 0), raio=14):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle(rect, radius=raio, fill=tuple(cor) + (ALFA,))
    img.save(destino)
    return str(destino)


def png_titulo(spec, W, H, destino):
    """Caixa branca arredondada (estilo TikTok) centrada em cy com o texto novo; cobre pelo menos cobrir_w x cobrir_h."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    px = spec.get("px", 29)
    f = ImageFont.truetype(FB if spec.get("negrito", True) else FM, px)
    ef = emoji_font()
    fe = ImageFont.truetype(str(ef), px) if ef else f
    larg = lambda s: sum(d.textlength(c, font=fe if e_emoji(c) else f) for c in s)  # noqa: E731
    linhas = spec["linhas"]
    lh = int(px * 1.3)
    ws = [larg(l) for l in linhas]
    bw = max(max(ws) + 44, spec.get("cobrir_w", 0))
    bh = max(lh * len(linhas) + 26, spec.get("cobrir_h", 0))
    cx, cy = spec.get("cx", W // 2), spec["cy"]
    x0, y0 = cx - bw / 2, cy - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=16, fill=(255, 255, 255, 255))
    ty = cy - lh * len(linhas) / 2 + 4
    for l, w in zip(linhas, ws):
        x = cx - w / 2
        for c in l:
            if e_emoji(c) and ef:
                d.text((x, ty + int(px * 0.05)), c, font=fe, embedded_color=True)
                x += d.textlength(c, font=fe)
            else:
                d.text((x, ty), c, font=f, fill=(0, 0, 0, 255))
                x += d.textlength(c, font=f)
        ty += lh
    img.save(destino)
    return str(destino)


def png_aviso(spec, W, H, destino):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    topo, g = spec.get("topo", int(H * 0.9)), 40
    for y in range(topo - g, H):
        a = ALFA if y >= topo else int(ALFA * (y - (topo - g)) / g)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    px = spec.get("px", 19)
    f = ImageFont.truetype(FM, px)
    lh = int(px * 1.32)
    y = topo + (H - topo - lh * len(spec["linhas"])) / 2
    for l in spec["linhas"]:
        d.text(((W - d.textlength(l, font=f)) / 2, y), l, font=f, fill=(235, 235, 235, 255))
        y += lh
    img.save(destino)
    return str(destino)


# ----------------------------------------------------------------- narração
def frases(txt: str):
    """[(a, b)] índices de caracteres de cada frase (. ! ?), sem espaços nas pontas."""
    out = []
    for m in re.finditer(r"[^.!?]+[.!?]*", txt):
        if not m.group().strip():
            continue
        a, b = m.start(), m.end() - 1
        while txt[a] in " \n":
            a += 1
        while b > a and txt[b] in " \n":
            b -= 1
        out.append((a, b + 1))
    return out


def preparar_narracao(R, D, T) -> tuple[Path, dict, float]:
    """Devolve (wav posicionado mono 48k, alinhamento ajustado, fim da fala em s)."""
    src = D / R["narr"]
    al = json.load(open(str(src.with_suffix("")) + ".alinhamento.json", encoding="utf-8"))
    al = al.get("alignment") or al.get("normalized_alignment") or al
    C, S, E = list(al["characters"]), list(al["character_start_times_seconds"]), list(al["character_end_times_seconds"])
    wav = T / "narr_pos.wav"
    vol = R.get("narr_vol", 1.0)
    if R.get("offsets"):
        fr = frases("".join(C))
        offs = R["offsets"]
        if len(offs) != len(fr):
            raise SystemExit(f"narração tem {len(fr)} frases e offsets tem {len(offs)} valores:\n"
                             + "\n".join(f"  {k + 1}. {''.join(C)[a:b]}" for k, (a, b) in enumerate(fr)))
        fc, partes = [], []
        nS, nE = list(S), list(E)
        for k, ((a, b), o) in enumerate(zip(fr, offs)):
            s, e = S[a], E[b - 1]
            ini = max(0.0, s - 0.04)
            d_ms = int(max(0.0, o - (s - ini)) * 1000)
            fc.append(f"[0:a]atrim={ini:.3f}:{e + 0.15:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
                      f"afade=t=out:st={e + 0.10 - ini:.3f}:d=0.05,adelay={d_ms}|{d_ms}[n{k}]")
            partes.append(f"[n{k}]")
            for i in range(a, b):
                nS[i], nE[i] = round(S[i] - s + o, 3), round(E[i] - s + o, 3)
        fc.append("".join(partes) + f"amix=inputs={len(partes)}:normalize=0:duration=longest,volume={vol}[a]")
        run(["ffmpeg", "-i", src, "-filter_complex", ";".join(fc), "-map", "[a]", "-ac", "1", "-ar", "48000", wav])
        S, E = nS, nE
    elif R.get("blocos"):
        bl, n = R["blocos"], len(S)
        fc, nS, nE = [], list(S), list(E)
        for k, (ci, dst) in enumerate(bl):
            cj = bl[k + 1][0] if k + 1 < len(bl) else n
            a = max(0.0, S[ci] - 0.04)
            b = (S[cj] - 0.04) if cj < n else E[-1] + 0.05
            fc.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,adelay={int(dst * 1000)}|{int(dst * 1000)}[b{k}]")
            off = dst - a
            for i in range(ci, cj):
                nS[i], nE[i] = round(S[i] + off, 3), round(E[i] + off, 3)
        fc.append("".join(f"[b{k}]" for k in range(len(bl))) + f"amix=inputs={len(bl)}:normalize=0,aresample=48000,volume={vol}[a]")
        run(["ffmpeg", "-i", src, "-filter_complex", ";".join(fc), "-map", "[a]", "-ac", "1", wav])
        S, E = nS, nE
    else:
        at, t0 = R.get("atempo", 1.0), R.get("narr_inicio", 0.3)
        run(["ffmpeg", "-i", src, "-af", f"atempo={at},aresample=48000,adelay={int(t0 * 1000)}|{int(t0 * 1000)},volume={vol}",
             "-ac", "1", wav])
        S = [round(t / at + t0, 3) for t in S]
        E = [round(t / at + t0, 3) for t in E]
    # correções de texto (mesmo tempo, texto novo)
    txt = "".join(C)
    for velho, novo in R.get("trocas", []):
        while (p := txt.find(velho)) >= 0:
            a, b = S[p], E[p + len(velho) - 1]
            n = len(novo)
            C = C[:p] + list(novo) + C[p + len(velho):]
            S = S[:p] + [round(a + (b - a) * i / n, 3) for i in range(n)] + S[p + len(velho):]
            E = E[:p] + [round(a + (b - a) * (i + 1) / n, 3) for i in range(n)] + E[p + len(velho):]
            txt = "".join(C)
    al2 = {"characters": C, "character_start_times_seconds": S, "character_end_times_seconds": E}
    fim = max(e for c, e in zip(C, E) if c.strip())
    return wav, al2, fim


# ----------------------------------------------------------------- desfoque por chaves
def caixa_em(chaves, t):
    if t <= chaves[0][0]:
        return chaves[0][1:]
    if t >= chaves[-1][0]:
        return chaves[-1][1:]
    for a, b in zip(chaves, chaves[1:]):
        if a[0] <= t <= b[0]:
            f = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 0
            return [a[i] + f * (b[i] - a[i]) for i in range(1, 5)]
    return chaves[-1][1:]


def desfocar(entrada: Path, saida: Path, ops: list, W: int, H: int):
    cap = cv2.VideoCapture(str(entrada))
    fps = cap.get(cv2.CAP_PROP_FPS) or FPS
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", f"{fps}", "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                           "-pix_fmt", "yuv420p", *COR, str(saida)], stdin=subprocess.PIPE)
    i = n = 0
    while True:
        ok, im = cap.read()
        if not ok:
            break
        t = i / fps
        ativos = [op for op in ops if op["de"] <= t <= op["ate"]]
        if ativos:
            mask = np.zeros((H, W), np.float32)
            preto = np.zeros((H, W), np.float32)
            for op in ativos:
                x0, y0, x1, y1 = [int(round(v)) for v in caixa_em(sorted(op["chaves"]), t)]
                x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
                if x1 <= x0 or y1 <= y0:
                    continue
                alvo = preto if op.get("tipo") == "preto" else mask
                if op.get("forma") == "elipse":
                    cv2.ellipse(alvo, ((x0 + x1) // 2, (y0 + y1) // 2), ((x1 - x0) // 2, (y1 - y0) // 2), 0, 0, 360, 1, -1)
                else:
                    alvo[y0:y1, x0:x1] = 1
            if mask.any():
                k = max(op.get("forca", 61) for op in ativos) | 1
                m = cv2.GaussianBlur(mask, (31, 31), 0)[..., None]
                b = cv2.GaussianBlur(cv2.GaussianBlur(im, (k, k), 0), (k, k), 0)
                im = (b * m + im * (1 - m)).astype(np.uint8)
            if preto.any():
                m = cv2.GaussianBlur(preto, (7, 7), 0)[..., None]
                im = (im * (1 - m)).astype(np.uint8)
            n += 1
        ff.stdin.write(im.tobytes())
        i += 1
    ff.stdin.close()
    ff.wait()
    return n


# ----------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--saida", default=None)
    ap.add_argument("--crf", type=int, default=16)
    a = ap.parse_args()
    cfg = Path(a.config).resolve()
    R = json.load(open(cfg, encoding="utf-8"))
    D = cfg.parent
    P = lambda p: str((D / p).resolve()) if p and not Path(p).is_absolute() else p  # noqa: E731
    W, H = resolucao(R.get("resolucao", "720"))
    saida = Path(a.saida).resolve() if a.saida else Path(P(R.get("saida", "corpo.mp4")))
    T = saida.parent / "_prep"
    T.mkdir(parents=True, exist_ok=True)

    video = P(R["video"])
    cortes = R.get("cortes") or [[0, dur(video)]]
    vdur = sum(b - a for a, b in cortes)
    narr, al2, fim_fala = preparar_narracao(R, D, T)
    json.dump(al2, open(saida.with_name("alinhamento.json"), "w", encoding="utf-8"), ensure_ascii=False)
    fim = R.get("fim") or {}
    total = max(vdur, fim_fala + fim.get("folga", 0.5))
    if fim.get("max_total"):
        total = min(total, fim["max_total"])
    pad = max(0.0, total - vdur + 0.05)

    # camadas
    camadas = []   # (png, de, ate)
    for k, fx in enumerate(R.get("faixas", [])):
        camadas.append((png_faixa(fx["y"][0], fx["y"][1], W, H, T / f"faixa{k}.png", fx.get("grad", 18), fx.get("cor", (0, 0, 0))),
                        fx.get("de", 0), fx.get("ate", 9999)))
    for k, cx in enumerate(R.get("caixas", [])):
        camadas.append((png_caixa(cx["rect"], W, H, T / f"caixa{k}.png", cx.get("cor", (0, 0, 0)), cx.get("raio", 14)),
                        cx.get("de", 0), cx.get("ate", 9999)))
    for k, tt in enumerate(R.get("titulos", [])):
        camadas.append((png_titulo(tt, W, H, T / f"titulo{k}.png"), tt.get("de", 0), tt.get("ate", 9999)))
    if R.get("aviso"):
        camadas.append((png_aviso(R["aviso"], W, H, T / "aviso.png"), 0, 9999))

    # vídeo: cortes + concat + congelamento do fim
    vf = []
    for k, (a0, b0) in enumerate(cortes):
        vf.append(f"[0:v]trim={a0}:{b0},setpts=PTS-STARTPTS[c{k}]")
    vf.append("".join(f"[c{k}]" for k in range(len(cortes))) + f"concat=n={len(cortes)}:v=1:a=0[vcat]")
    vf.append(f"[vcat]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},setsar=1,"
              f"tpad=stop_mode=clone:stop_duration={pad:.3f},trim=0:{total:.3f},setpts=PTS-STARTPTS[v0]")
    ins = ["-i", video]
    if R.get("desfocar"):
        mudo = T / "imagens.mp4"
        run(["ffmpeg", *ins, "-filter_complex", ";".join(vf), "-map", "[v0]", "-an", "-c:v", "libx264", "-crf", "14",
             "-preset", "medium", "-pix_fmt", "yuv420p", *COR, mudo])
        mudo2 = T / "imagens_desfocado.mp4"
        n = desfocar(mudo, mudo2, R["desfocar"], W, H)
        print(f"desfoque: {n} quadros tratados")
        ins = ["-i", str(mudo2)]
        vf = ["[0:v]setpts=PTS-STARTPTS[v0]"]
    vk = "[v0]"
    n_in = 1
    for k, (png, de, ate) in enumerate(camadas):
        ins += ["-i", png]
        vf.append(f"{vk}[{n_in}:v]overlay=0:0:enable='between(t,{de},{ate})'[o{k}]")
        vk = f"[o{k}]"
        n_in += 1

    # áudio: fundo (mesmos cortes) + narração
    af = []
    ins += ["-i", str(narr)]
    i_narr = n_in
    n_in += 1
    if R.get("fundo"):
        ins += ["-i", P(R["fundo"])]
        for k, (a0, b0) in enumerate(cortes):
            af.append(f"[{n_in}:a]aresample=48000,atrim={a0}:{b0},asetpts=PTS-STARTPTS[f{k}]")
        af.append("".join(f"[f{k}]" for k in range(len(cortes))) + f"concat=n={len(cortes)}:v=0:a=1[fcat]")
        af.append(f"[fcat]volume={R.get('fundo_vol', 1.0)},apad,atrim=0:{total:.3f},afade=t=out:st={max(0, total - 0.35):.3f}:d=0.35[bg]")
        af.append(f"[{i_narr}:a]aresample=48000,apad,atrim=0:{total:.3f}[nv]")
        af.append("[bg][nv]amix=inputs=2:duration=first:normalize=0,aformat=channel_layouts=stereo[a]")
    else:
        af.append(f"[{i_narr}:a]aresample=48000,apad,atrim=0:{total:.3f},aformat=channel_layouts=stereo[a]")

    run(["ffmpeg", *ins, "-filter_complex", ";".join(vf + af), "-map", vk, "-map", "[a]", "-t", f"{total:.3f}",
         "-c:v", "libx264", "-crf", str(a.crf), "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), *COR,
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", saida])
    print(f"ok {saida} | {dur(saida):.2f}s | vídeo {vdur:.2f}s + congelado {max(0.0, total - vdur):.2f}s | "
          f"fala termina em {fim_fala:.2f}s | alinhamento: {saida.with_name('alinhamento.json').name}")


if __name__ == "__main__":
    main()
