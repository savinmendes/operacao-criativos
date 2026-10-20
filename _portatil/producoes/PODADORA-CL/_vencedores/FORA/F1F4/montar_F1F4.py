# -*- coding: utf-8 -*-
"""Criativos "fora da caixa" F1 (ASMR) e F4a/F4b/F4c ("respondiendo al comentario") da Podadora COD Chile.
  python montar_F1F4.py [F1 F4a F4b F4c]   (sem argumento = todos)
Só tomadas que já existem (original_03/04, vencedor1). Corpo A = AD 04 a partir de 9,000 s; corpo B = vencedor1 a
partir de 2,100 s escalado para 720x1280. Os dois entram intactos até o fim (só recodificação)."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
from comum import COR, FPS, dur, preparar_fontsdir, run  # noqa: E402
import finalizar as FIN  # noqa: E402
import legenda as LEG  # noqa: E402
from gerar_variacao import lufs  # noqa: E402

BASE = Path(r"C:\Users\PICHAU\Downloads\PODADORA-CL")
D = Path(__file__).resolve().parent
VOZ = D.parent / "voz"
OUT = BASE / "VENCEDORES" / "FORA"
O3, O4 = BASE / "original_03.mp4", BASE / "original_04.mp4"
V1 = BASE / "_vencedores" / "vencedor1.mp4"
AD04 = BASE / "AD 04 - PODADORA-INALAMBRICA-DEVOLVER-ES-CL.mp4"
FAIXA_A = BASE / "_trabalho" / "04" / "faixa.png"       # aviso em espanhol do AD 04 (cobre o aviso em inglês)
BED_B = BASE / "_vencedores" / "B" / "bed.wav"           # no_vocals dos 2,1 s antes do corte do vencedor B
W, H = 720, 1280
FB = str(KIT / "fonts" / "Poppins-Bold.ttf")
FS = str(KIT / "fonts" / "Poppins-SemiBold.ttf")
FM = str(KIT / "fonts" / "Poppins-Medium.ttf")
CORPO = {"A": dict(video=AD04, corte=9.000), "B": dict(video=V1, corte=2.100)}
VOZ_B_LUFS = -14.3   # nível da voz original do vencedor B (relatório B)

# tomada = (fonte, ini, n_quadros, opções) ; opções: "cobre" = zoom 1,10 ancorado no topo (tira o aviso em inglês
# queimado no rodapé dos originais, para o corpo B, que não tem faixa) ; "lento" = câmera lenta 0,5x (n = quadros
# de origem, sai 2n) ; fonte None = termina exatamente no corte do AD 04 (mesma tomada contínua do corpo A)
G = {
    "F1": dict(nome="ASMR", corpo="B", fala=None, som="som_F1.wav",
               tomadas=[(V1, 0.00, 30, ""), (O3, 13.55, 42, "cobre"), (V1, 16.45, 30, ""), (O3, 18.05, 33, "cobre"),
                        (V1, 19.40, 30, ""), (V1, 22.33, 26, "lento")],
               caixas=[(["ANTES ", "e_1f629.png"], 0.0, 2.4), (["10 MIN DESPUÉS ", "e_1f62e-200d-1f4a8.png"], 5.5, 99)],
               cenas="corredor tomado de mato (vencedor1 0,00–1,00) → máquina entrando no mato alto, close (original_03 "
                     "13,55–14,95) → POV cortando mato alto (vencedor1 16,45–17,45) → close no mato alto (original_03 "
                     "18,05–19,15) → faixa sendo aberta no gramado alto (vencedor1 19,40–20,40) → POV da faixa listrada, "
                     "câmera lenta 0,5x (vencedor1 22,33–23,20 → 1,73 s)"),
    "F4a": dict(nome="COMENTARIO-PASTO-ALTO", corpo="B", fala="F4a", pergunta="¿Sirve para pasto alto?",
                chaves=["alto?", "altísimo…"], lead=0.30,
                tomadas=[(V1, 16.36, 55, ""), (V1, 18.40, 50, ""), (V1, 22.31, 27, "")],
                cenas="POV cortando mato alto (vencedor1 16,36–18,19) → faixas abertas no gramado alto (vencedor1 "
                      "18,40–20,07) → POV da faixa listrada pronta (vencedor1 22,31–23,21)"),
    "F4b": dict(nome="COMENTARIO-BATERIA", corpo="A", fala="F4b", pergunta="¿Cuánto dura la batería?",
                chaves=["baterías…", "otra"], lead=0.12,
                tomadas=[(O4, 24.45, 48, ""), (O4, 35.75, 45, ""), (O4, 27.47, 48, ""), (None, 0, 48, "")],
                cenas="máquina com rodas cortando junto às plantas, só pernas (original_04 24,45–26,05) → mesa com as 2 "
                      "baterias 21V, só mão (35,75–37,25) → close das rodas cortando o mato na calçada (27,47–29,07) → "
                      "câmera da porta cortando o mato (7,40–9,00, emenda contínua no corpo)"),
    "F4c": dict(nome="COMENTARIO-PESADA", corpo="A", fala="F4c", pergunta="¿Es pesada?",
                chaves=["ruedas…", "peso."], lead=0.12,
                tomadas=[(O4, 14.00, 37, ""), (O4, 28.80, 30, ""), (O4, 24.45, 73, "")],
                cenas="máquina rodando no gramado junto à escada, só pernas (original_04 14,00–15,23) → close das rodas "
                      "(28,80–29,80) → guiando a máquina com uma mão junto às plantas, só pernas (24,45–26,88)"),
}


# ------------------------------------------------------------------ gráficos
def bolha(pergunta, destino, cy=330):
    """Balão de comentário genérico: avatar cinza + 'Usuario' + só a pergunta (sem curtidas, sem avaliação)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fq, fn = ImageFont.truetype(FB, 48), ImageFont.truetype(FS, 28)
    tmp = ImageDraw.Draw(img)
    av, pad, gap = 90, 26, 20
    maxw = 680 - av - gap - 2 * pad
    linhas, cur = [], ""
    for w in pergunta.split():
        t = (cur + " " + w).strip()
        if tmp.textlength(t, font=fq) > maxw and cur:
            linhas.append(cur)
            cur = w
        else:
            cur = t
    linhas.append(cur)
    tw = max([tmp.textlength(l, font=fq) for l in linhas] + [tmp.textlength("Usuario", font=fn)])
    bw = int(pad * 2 + av + gap + tw)
    bh = int(pad * 2 + 38 + 62 * len(linhas))
    x0, y0 = (W - bw) // 2, cy - bh // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 3, y0 + 6, x0 + bw + 3, y0 + bh + 6], 30, fill=(0, 0, 0, 110))
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 30, fill=(255, 255, 255, 255))
    d.polygon([(x0 + 46, y0 + bh - 2), (x0 + 82, y0 + bh - 2), (x0 + 40, y0 + bh + 26)], fill=(255, 255, 255, 255))
    ax, ay = x0 + pad, y0 + pad
    d.ellipse([ax, ay, ax + av, ay + av], fill=(176, 179, 184, 255))
    d.ellipse([ax + av * 0.33, ay + av * 0.17, ax + av * 0.67, ay + av * 0.51], fill=(240, 240, 242, 255))
    m = Image.new("L", (av, av), 0)
    ImageDraw.Draw(m).ellipse([0, 0, av - 1, av - 1], fill=255)
    corpo = Image.new("RGBA", (av, av), (0, 0, 0, 0))
    ImageDraw.Draw(corpo).ellipse([av * 0.16, av * 0.58, av * 0.84, av * 1.25], fill=(240, 240, 242, 255))
    corpo.putalpha(Image.fromarray(np.minimum(np.array(corpo.split()[3]), np.array(m))))
    img.alpha_composite(corpo, (int(ax), int(ay)))
    d = ImageDraw.Draw(img)
    tx = ax + av + gap
    d.text((tx, y0 + pad - 4), "Usuario", font=fn, fill=(105, 108, 114, 255))
    ty = y0 + pad + 34
    for l in linhas:
        d.text((tx, ty), l, font=fq, fill=(15, 15, 15, 255))
        ty += 62
    img.save(destino)
    return str(destino)


def caixa(partes, destino, cy=240, px=64):
    """Caixa branca do kit (Poppins Bold, preto) com emoji em PNG (Twemoji, CC-BY 4.0; o Pillow local não junta
    a sequência ZWJ de 😮‍💨)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FB, px)
    es = int(px * 1.05)
    larg = sum(es + 4 if p.endswith(".png") else d.textlength(p, font=f) for p in partes)
    bw, bh = larg + 44, int(px * 1.3) + 26
    x0, y0 = W / 2 - bw / 2, cy - bh / 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=16, fill=(255, 255, 255, 255))
    x = x0 + 22
    for p in partes:
        if p.endswith(".png"):
            e = Image.open(D / p).convert("RGBA").resize((es, es), Image.LANCZOS)
            img.alpha_composite(e, (int(x), int(cy - es / 2)))
            x += es + 4
        else:
            d.text((x, cy - px * 0.62), p, font=f, fill=(0, 0, 0, 255))
            x += d.textlength(p, font=f)
    img.save(destino)
    return str(destino)


# ------------------------------------------------------------------ montagem
def tomada(src, ini, n, op, o):
    if src == V1:
        base = f"scale={W}:{H}:flags=lanczos"
    elif "cobre" in op:
        base = f"scale=792:1408:flags=lanczos,crop={W}:{H}:36:0"
    else:
        base = f"scale={W}:{H}"
    if "lento" in op:
        vf = (f"fps={FPS},{base},minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
              f"setpts=2*PTS,fps={FPS},setsar=1")
        run(["ffmpeg", "-ss", f"{ini:.3f}", "-t", f"{n / FPS + 0.2:.3f}", "-i", src, "-an", "-vf", vf,
             "-frames:v", 2 * n, "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
        return 2 * n
    run(["ffmpeg", "-ss", f"{ini:.3f}", "-i", src, "-an", "-frames:v", n, "-vf", f"fps={FPS},{base},setsar=1",
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
    return n


def fim_fala(alj):
    al = json.load(open(alj, encoding="utf-8"))
    return max(e for c, e in zip(al["characters"], al["character_end_times_seconds"]) if c.strip())


def montar(cod):
    g = G[cod]
    T = D / "trab" / cod
    T.mkdir(parents=True, exist_ok=True)
    corpo = CORPO[g["corpo"]]
    nq_total = sum(2 * t[2] if "lento" in t[3] else t[2] for t in g["tomadas"])
    Hd = nq_total / FPS

    # ---- visual
    lista, segs, q = [], [], 0
    for k, (src, ini, n, op) in enumerate(g["tomadas"]):
        o = T / f"t{k}.mp4"
        if src is None:                       # termina no corte do AD 04 (câmera da porta contínua)
            src, ini = O4, round(corpo["corte"] - n / FPS, 4)
        nn = tomada(src, ini, n, op, o)
        segs.append({"fonte": Path(src).name, "ini": ini, "quadros_origem": n, "quadros": nn, "op": op,
                     "de_s": round(q / FPS, 3)})
        q += nn
        lista.append(f"file '{o.as_posix()}'")
    (T / "lista.txt").write_text("\n".join(lista), encoding="utf-8")
    run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", T / "lista.txt", "-c", "copy", T / "g_v.mp4"])

    # ---- overlays (png, de, até)
    ovs = []
    if g["corpo"] == "A":
        ovs.append((str(FAIXA_A), 0, 99))
    if g.get("pergunta"):
        ovs.append((bolha(g["pergunta"], T / "bolha.png"), 0, 99))
    for k, (partes, de, ate) in enumerate(g.get("caixas", [])):
        ovs.append((caixa(partes, T / f"caixa{k}.png"), de, ate))

    # ---- áudio
    ins = ["-i", T / "g_v.mp4"]
    fc = []
    if g["fala"]:
        fala, alj = VOZ / f"{g['fala']}.mp3", VOZ / f"{g['fala']}.alinhamento.json"
        lead = g["lead"]
        assert lead + fim_fala(alj) + 0.2 <= Hd, f"{cod}: fala não cabe no gancho"
        if g["corpo"] == "A":
            ganho = lufs(AD04, corpo["corte"], 30) - lufs(fala) - 0.5
            ins += ["-i", AD04]
            fc.append(f"[1:a]atrim={corpo['corte'] - Hd:.4f}:{corpo['corte']:.4f},asetpts=PTS-STARTPTS,"
                      "aresample=48000,aformat=channel_layouts=stereo[bg]")
        else:
            ganho = VOZ_B_LUFS - lufs(fala)
            bd = dur(BED_B)
            ins += ["-i", BED_B]
            fc.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int((Hd - bd) * 1000)}|"
                      f"{int((Hd - bd) * 1000)},apad,atrim=0:{Hd:.4f}[bg]")
        ins += ["-i", fala]
        fc.append(f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume={ganho:.2f}dB,"
                  f"adelay={int(lead * 1000)}|{int(lead * 1000)}[nv]")
        fc.append(f"[bg][nv]amix=inputs=2:duration=first:normalize=0,apad,atrim=0:{Hd:.4f}[ga]")
        pal = LEG.palavras_por_alinhamento(str(alj), lead)
        preparar_fontsdir(T)
        LEG.gera_ass(pal, str(T / "leg.ass"), "drop", set(g["chaves"]), None, Hd)
        n_in = 3
    else:
        som = D / g["som"]
        ganho = -16.0 - lufs(D / "som_F1_raw.wav")
        run(["ffmpeg", "-i", D / "som_F1_raw.wav", "-af", f"volume={ganho:.2f}dB", "-ar", "48000", som])
        ins += ["-i", som]
        fc.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{Hd:.4f}[ga]")
        n_in = 2
    vin = "[0:v]"
    for k, (png, de, ate) in enumerate(ovs):
        ins += ["-loop", "1", "-t", f"{Hd:.3f}", "-i", png]
        fc.append(f"{vin}[{n_in + k}:v]overlay=0:0:enable='between(t,{de},{ate})'[o{k}]")
        vin = f"[o{k}]"
    fc.append(f"{vin}{'ass=leg.ass:fontsdir=fonts,' if g['fala'] else ''}fps={FPS},format=yuv420p,setsar=1[gv]")
    run(["ffmpeg", *ins, "-filter_complex", ";".join(fc), "-map", "[gv]", "-map", "[ga]", "-t", f"{Hd:.4f}",
         "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
         "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "gancho.mov"], cwd=T)

    # ---- gancho + corpo intacto a partir do corte (até o fim)
    DF = dur(corpo["video"])
    total = Hd + DF - corpo["corte"]
    v_kbps, _ = FIN.bitrate_alvo(total, 30, piso=FIN.QUALIDADE_MIN_720_KBPS)
    saida = OUT / f"{cod} - {g['nome']}-{g['corpo']}-ES-CL.mp4"
    fc = ["[0:v]fps=30,setsar=1,format=yuv420p[v0]",
          f"[1:v]fps=30,scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[v1]",
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0]",
          "[1:a]aresample=48000,aformat=channel_layouts=stereo[a1]",
          "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"]
    run(["ffmpeg", "-i", T / "gancho.mov", "-ss", f"{corpo['corte']:.3f}", "-i", corpo["video"],
         "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-pix_fmt", "yuv420p", *COR,
         "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps * 1.5)}k", "-bufsize", f"{v_kbps * 2}k",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida])
    FIN.revisar(str(saida), str(saida.with_name(saida.stem + "_frames.jpg")), esperado=(W, H))
    info = {"cod": cod, "saida": str(saida), "gancho_s": round(Hd, 3), "tomadas": segs, "corpo": g["corpo"],
            "corte": corpo["corte"], "total_s": round(dur(saida), 2), "ganho_db": round(ganho, 2),
            "mb": round(saida.stat().st_size / 1e6, 1), "kbps": v_kbps, "cenas": g["cenas"]}
    json.dump(info, open(T / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ok {cod} | gancho {Hd:.2f}s | total {info['total_s']}s | {info['mb']} MB | {saida.name}", flush=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for c in (sys.argv[1:] or list(G)):
        montar(c)
