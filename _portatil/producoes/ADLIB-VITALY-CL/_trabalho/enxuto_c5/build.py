# -*- coding: utf-8 -*-
"""C5 do lote enxuto Lymphoria (COD Chile): monta o corpo (takes/fotos/avatar) + áudio e chama o montar_ad.py.
  python build.py a|b
"""
import json, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).parent
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
A = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
U = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod")
BED = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\variacoes\fontes")
FONTS = Path(r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\_trabalho\prod\IMGS\fonts")
OUT = Path(r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\LYMPHORIA-ENXUTO")
IMG = AQUI / "img"
W, H, FPS = 1080, 1920, 30
PRE = {"P2_frasco_miel.mp4": {"pre": "crop=579:1030:141:250"}}   # tira a emenda do topo da foto


def sh(*a):
    subprocess.run([str(x) for x in a], check=True)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout.split()[0])


def fix_alinhamento(src, dst):
    """Linforia (grafia fonética do TTS) -> Lymphoria na legenda, redistribuindo os tempos do trecho."""
    al = json.load(open(src, encoding="utf-8"))
    C, S, E = list(al["characters"]), list(al["character_start_times_seconds"]), list(al["character_end_times_seconds"])
    txt = "".join(C)
    i = txt.find("Linforia")
    while i >= 0:
        s0, s1 = S[i], E[i + 7]
        novo = "Lymphoria"
        n = len(novo)
        C[i:i + 8] = list(novo)
        S[i:i + 8] = [s0 + (s1 - s0) * k / n for k in range(n)]
        E[i:i + 8] = [s0 + (s1 - s0) * (k + 1) / n for k in range(n)]
        txt = "".join(C)
        i = txt.find("Linforia")
    json.dump({"characters": C, "character_start_times_seconds": S, "character_end_times_seconds": E},
              open(dst, "w", encoding="utf-8"), ensure_ascii=False)


def seg(src, d, out, kind="take", zoom=(1.0, 1.10), crop=None, ss=None, pre=None):
    """Clipe 1080x1920, 30 fps, sem áudio, duração exata d.
    take: corta do meio (ou ss) e desacelera até 0,5x se faltar; foto: zoom lento (ken burns); avatar: trecho ss..ss+d com zoom fixo."""
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
    if kind == "foto":
        im = Image.open(src).convert("RGB")
        if crop:
            im = im.crop(crop)
        tw = int(W * 1.25)
        im = im.resize((tw, int(tw * im.height / im.width)), Image.LANCZOS)
        tmp = out.with_suffix(".png")
        im.save(tmp)
        nf = int(round(d * FPS))
        z0, z1 = zoom
        vf = (f"scale={W*2}:-2,zoompan=z='{z0}+({z1}-{z0})*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
              f"d={nf}:s={W}x{H}:fps={FPS},setsar=1")
        sh("ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", tmp, "-vf", vf, "-frames:v", nf, "-an",
           "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-r", FPS, "-threads", "3",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out)
        return out
    if kind == "avatar":
        z = zoom[0]
        vf = (f"trim={ss:.3f}:{ss + d:.3f},setpts=PTS-STARTPTS,"
              f"scale={int(W*z)}:{int(H*z)}:flags=lanczos,crop={W}:{H}:(iw-{W})/2:{int((H*z-H)*0.25)},fps={FPS},setsar=1")
        sh("ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-an", "-t", f"{d:.3f}",
           "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-r", FPS, "-threads", "3",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out)
        return out
    dt = dur(src)
    if dt >= d + 0.1:
        st = ss if ss is not None else (dt - d) / 2
        f = f"trim={st:.3f}:{st + d:.3f},setpts=PTS-STARTPTS"
    else:
        fat = min(d / (dt - 0.05), 2.0)
        f = f"setpts={fat:.4f}*(PTS-STARTPTS),tpad=stop_mode=clone:stop_duration={d:.3f},trim=0:{d:.3f},setpts=PTS-STARTPTS"
    if pre:
        f = f"{f},{pre}"
    sh("ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"{f},{base},fps={FPS},format=yuv420p", "-an", "-t", f"{d:.3f}",
       "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-r", FPS, "-threads", "3",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out)
    return out


def titulo_png(dst):
    """Texto grande 'PAGAS AL RECIBIR' (caixa verde da marca, RECIBIR em amarelo) + linha menor."""
    f1 = ImageFont.truetype(str(FONTS / "Poppins-Black.ttf"), 150)
    f2 = ImageFont.truetype(str(FONTS / "Poppins-Bold.ttf"), 50)
    l1, l2, l3 = "PAGAS AL", "RECIBIR", "envío gratis a todo Chile"
    im = Image.new("RGBA", (W, 640), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((70, 10, W - 70, 600), 46, fill=(25, 74, 52, 245), outline=(255, 255, 255, 255), width=6)
    for txt, f, y, cor in ((l1, f1, 40, (255, 255, 255)), (l2, f1, 215, (255, 214, 0)), (l3, f2, 455, (255, 255, 255))):
        w = d.textlength(txt, font=f)
        d.text(((W - w) / 2, y), txt, font=f, fill=cor)
    d.line((250, 435, W - 250, 435), fill=(255, 255, 255, 180), width=3)
    im.save(dst)
    return dst


def audio(narr, bed, D, out):
    sh("ffmpeg", "-v", "error", "-y", "-i", narr, "-stream_loop", "-1", "-i", bed, "-filter_complex",
       f"[0:a]aresample=48000,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={D:.3f}[v];"
       f"[1:a]atrim=0:{D + 0.5:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
       f"loudnorm=I=-32:TP=-9:LRA=11,aresample=48000,afade=t=in:d=0.3,afade=t=out:st={D - 0.6:.3f}:d=0.6[m];"
       f"[v][m]amix=inputs=2:duration=first:normalize=0,atrim=0:{D:.3f}[a]",
       "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", out)
    return out


def corpo(segs, narr, bed, wk, overlay=None):
    clips = []
    for k, s in enumerate(segs):
        clips.append(seg(*s["a"], out=wk / f"s{k:02d}.mp4", **s.get("kw", {})))
    D = sum(dur(c) for c in clips)
    lst = wk / "lista.txt"
    lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    vid = wk / "video.mp4"
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid)
    aud = audio(narr, bed, D, wk / "mix.wav")
    out = wk / "corpo.mp4"
    if overlay:
        png, t0, t1 = overlay
        fc = f"[0:v][2:v]overlay=0:{png[1]}:enable='between(t,{t0},{t1})',format=yuv420p[v]"
        sh("ffmpeg", "-v", "error", "-y", "-i", vid, "-i", aud, "-i", png[0], "-filter_complex", fc,
           "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "-r", FPS, "-threads", "3",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", out)
    else:
        sh("ffmpeg", "-v", "error", "-y", "-i", vid, "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", out)
    return out, D


def spans(cortes, total):
    """[(t0,t1)] a partir dos pontos de corte."""
    pts = [0.0] + cortes + [total]
    return [(round(pts[i], 3), round(pts[i + 1], 3)) for i in range(len(pts) - 1)]


def build_a():
    wk = AQUI / "a"
    av = wk / "heygen.mp4"
    narr = wk / "narr.mp3"
    total = dur(narr) + 0.6
    cortes = [3.6, 7.4, 9.5, 11.6, 15.2, 18.1, 22.0, 24.95, 27.5, 31.1, 33.9, 36.6, 39.8]
    sp = spans(cortes, total)
    plano = ["AV1", "AV2", "AV1", A / "ad10/flora/t1_edit.mp4", "AV2", ("foto", IMG / "v1.png"), "AV1", "AV2",
             U / "V1_gotero_hierbas.mp4", U / "P2_frasco_miel.mp4", "AV1", "AV2", ("foto", IMG / "v2.png"),
             A / "ad22/flora/t1_edit.mp4"]
    segs = []
    for (t0, t1), p in zip(sp, plano):
        d = t1 - t0
        if p == "AV1":
            segs.append({"a": (av, d), "kw": {"kind": "avatar", "ss": t0, "zoom": (1.0,)}})
        elif p == "AV2":
            segs.append({"a": (av, d), "kw": {"kind": "avatar", "ss": t0, "zoom": (1.18,)}})
        elif isinstance(p, tuple):
            segs.append({"a": (p[1], d), "kw": {"kind": "foto"}})
        else:
            segs.append({"a": (p, d), "kw": PRE.get(p.name, {})})
    c, D = corpo(segs, narr, BED / "05" / "bed_no_vocals.wav", wk)
    fix_alinhamento(wk / "narr.alinhamento.json", wk / "leg.alinhamento.json")
    t_oferta = 36.6
    rec = {"saida": str(OUT / "LYM-CL_C5_desconfiada-online_avatar-ugc_a.mp4"), "estilo": "drop", "corpo": str(c),
           "legenda": {"fonte": f"alinhamento:{wk / 'leg.alinhamento.json'}",
                       "chaves": ["lymphoria", "gratis", "recibir", "tarjeta", "miel", "noventa", "dos", "nada"]},
           "manchete": {"texto": "¿Te da miedo comprar por internet? 😰", "ate": 3.6},
           "selo": {"linhas": ["", "PAGO CONTRA", "ENTREGA", ""], "escala": 0.55, "x": 331, "y": 1330, "desde": t_oferta},
           "cta": {"palavra": "toca"}, "limite_mb": 30, "resolucao": "720"}
    return rec, wk


def build_b():
    wk = AQUI / "b"
    narr = wk / "narr.mp3"
    total = dur(narr) + 0.6
    cortes = [2.7, 4.2, 6.3, 8.6, 11.6, 13.9, 15.9, 18.7, 21.4, 24.4, 27.3, 29.3]
    sp = spans(cortes, total)
    c5 = (300, 0, 1556, 2234)   # recorte 9:16 da foto da caja (2 frascos)
    plano = [("foto", IMG / "v1.png", None, (1.0, 1.12)), A / "ad11/flora/t3_edit.mp4", A / "ad22/flora/t1_edit.mp4",
             A / "ad01/flora/t2_edit.mp4", ("foto", IMG / "v2.png", None, (1.04, 1.16)), A / "ad19/flora/t1_edit.mp4",
             U / "V1_gotero_hierbas.mp4", A / "ad19/flora/t3_edit.mp4", U / "P2_frasco_miel.mp4",
             A / "ad14/flora2/t6_edit.mp4", A / "ad10/flora/t1_edit.mp4", ("foto", IMG / "c5.png", c5, (1.0, 1.1)),
             A / "ad14/flora/t3_edit.mp4"]
    segs = []
    for (t0, t1), p in zip(sp, plano):
        d = t1 - t0
        if isinstance(p, tuple):
            segs.append({"a": (p[1], d), "kw": {"kind": "foto", "crop": p[2], "zoom": p[3]}})
        else:
            segs.append({"a": (p, d), "kw": PRE.get(p.name, {})})
    png = titulo_png(wk / "titulo.png")
    c, D = corpo(segs, narr, BED / "30" / "bed_no_vocals.wav", wk, overlay=((png, 150), 0, 11.6))
    fix_alinhamento(wk / "narr.alinhamento.json", wk / "leg.alinhamento.json")
    rec = {"saida": str(OUT / "LYM-CL_C5_desconfiada-online_montaje-pagas-al-recibir_b.mp4"), "estilo": "drop",
           "corpo": str(c),
           "legenda": {"fonte": f"alinhamento:{wk / 'leg.alinhamento.json'}",
                       "chaves": ["lymphoria", "gratis", "recibir", "pagas", "miel", "noventa", "dos", "hierbas", "hinchazón"]},
           "selo": {"linhas": ["", "PAGO CONTRA", "ENTREGA", ""], "escala": 0.55, "x": 331, "y": 1330, "desde": 24.4},
           "cta": {"palavra": "toca"}, "limite_mb": 30, "resolucao": "720"}
    return rec, wk


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    rec, wk = {"a": build_a, "b": build_b}[sys.argv[1]]()
    (wk / "receita.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    subprocess.run([sys.executable, str(KIT / "ferramentas" / "montar_ad.py"), str(wk / "receita.json")],
                   check=True, env=env, cwd=str(KIT))
    print("OK", rec["saida"])
