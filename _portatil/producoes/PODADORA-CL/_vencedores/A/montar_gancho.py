# -*- coding: utf-8 -*-
"""Vencedor A (AD 04 DEVOLVER): gancho novo + corpo/CTA do AD 04 intactos a partir do corte.
  python montar_gancho.py A1 [A2 ...]   (sem argumento = todos)
Gancho: tomadas do original_04 (sem rosto falando) + faixa do aviso do AD 04 + caixa grande + legenda da fala
(mesmo estilo drop do kit) + música do próprio AD 04 imediatamente antes do corte (emenda contínua).
Corpo: AD 04 a partir de CORTE (início da 1ª frase "Quien inventó esto…"), sem nenhuma alteração além da recodificação."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
from comum import COR, FPS, dur, preparar_fontsdir, run  # noqa: E402
import finalizar as FIN  # noqa: E402
import legenda as LEG  # noqa: E402
from gerar_variacao import caixa_texto, lufs  # noqa: E402

BASE = Path(r"C:\Users\PICHAU\Downloads\PODADORA-CL")
A = BASE / "_vencedores" / "A"
ORIG = BASE / "original_04.mp4"
AD04 = BASE / "AD 04 - PODADORA-INALAMBRICA-DEVOLVER-ES-CL.mp4"
FAIXA = BASE / "_trabalho" / "04" / "faixa.png"
OUT = BASE / "VENCEDORES"
CORTE = 9.0          # fim do gancho original (câmera da porta sem fala) = início de "Quien inventó esto…" (9,046 s)
W, H = 720, 1280
LEAD, CAUDA = 0.12, 0.35
CAIXA = dict(cy=470, px=46, min_w=520, min_h=84)   # cobre a caixa em inglês do original (cy 470, 484x52, até ~6,6 s)

# tomadas: (início, duração) no original_04 | None = completar a duração até terminar no CORTE (emenda contínua)
G = {
    "A1": dict(nome="ESPOSO", texto=["¿DEVOLVERLA? NI LOCA 😅"], tomadas=[(1.0, 1.4), None],
               chaves=["devolviera", "soltar"],
               cenas="câmera da porta: caixa chegando (1,0–2,4 s) → máquina cortando o mato alto (câmera da porta, termina em 9,0 s e emenda no corpo)"),
    "A2": dict(nome="OTRA-COMPRA", texto=["OTRA COMPRA MÁS… 🙄"], tomadas=[(0.3, None)], zoom=(1.0, 1.2, 360, 880), px=38,
               chaves=["internet", "equivoqué"],
               cenas="câmera da porta: caixa chegando e sendo aberta (0,3 s em diante) com zoom lento na caixa"),
    "A3": dict(nome="UNA-PASADA", texto=["UNA SOLA PASADA"], tomadas=[(27.6, 2.0), None],
               chaves=["pasada", "rodilla"],
               cenas="close do mato alto sumindo sob a máquina (27,6–29,6 s, só pernas) → câmera da porta cortando o mato (termina em 9,0 s)"),
    "A4": dict(nome="INALAMBRICO", texto=["SIN CABLES. SIN BENCINA."], tomadas=[(35.85, 1.4), (24.6, None)],
               chaves=["inalámbrico"],
               cenas="mesa com as 2 baterias 21V e as rodas (35,85–37,25 s, só mão) → máquina com rodas cortando sem cabo (24,6 s em diante, só pernas)"),
    "A5": dict(nome="JARDINERO", texto=["ADIÓS JARDINERO"], tomadas=[(21.35, 2.5), (24.6, None)],
               chaves=["jardinero", "minutos"],
               cenas="corte no caminho de pedra junto ao canteiro (21,35–23,85 s, só pernas) → corte ao lado do canteiro de plantas (24,6 s em diante, só pernas)"),
    "A6": dict(nome="LLEGO-AYER", texto=["LLEGÓ AYER 📦"], tomadas=[(1.0, 1.4), (11.9, None)],
               chaves=["ayer", "patio"],
               cenas="câmera da porta: caixa chegando (1,0–2,4 s) → câmera da porta com o gramado já cortado (11,9 s em diante)"),
}


def fim_fala(al_path):
    al = json.load(open(al_path, encoding="utf-8"))
    al = al.get("alignment") or al.get("normalized_alignment") or al
    return max(e for c, e in zip(al["characters"], al["character_end_times_seconds"]) if c.strip())


def montar(cod):
    g = G[cod]
    T = A / "trab" / cod
    T.mkdir(parents=True, exist_ok=True)
    fala = A / "voz" / f"{cod}.mp3"
    alj = A / "voz" / f"{cod}.alinhamento.json"
    Hd = round((LEAD + fim_fala(alj) + CAUDA) * FPS) / FPS
    if Hd > CORTE:
        raise SystemExit("gancho maior que o trecho de música antes do corte")

    caixa = caixa_texto(g["texto"], T / "caixa.png", W, H, CAIXA["cy"], g.get("px", CAIXA["px"]), CAIXA["min_w"], CAIXA["min_h"], True)

    # ---- tomadas (quadros exatos)
    fixos = sum(d for t in g["tomadas"] if t and t[1] for d in [t[1]])
    segs = []
    for t in g["tomadas"]:
        if t is None:                              # termina exatamente no CORTE (mesma tomada contínua do corpo)
            d = round((Hd - fixos) * FPS) / FPS
            segs.append((round(CORTE - d, 4), d))
        elif t[1] is None:
            segs.append((t[0], round((Hd - fixos) * FPS) / FPS))
        else:
            segs.append(t)
    lista = []
    for k, (ini, d) in enumerate(segs):
        o = T / f"t{k}.mp4"
        vf = f"fps={FPS},scale={W}:{H},setsar=1"
        if g.get("zoom") and k == 0:
            z0, z1, cx, cy = g["zoom"]
            n = int(round(d * FPS))
            # zoom lento e contínuo, mantendo o ponto (cx, cy) fixo: escala por quadro + recorte 720x1280
            z = f"({z0}+({z1}-{z0})*n/{n})"
            vf = (f"fps={FPS},scale=w='2*trunc({W}*{z}/2)':h='2*trunc({H}*{z}/2)':eval=frame:flags=lanczos,"
                  f"crop={W}:{H}:x='max(0,min(iw-{W},{cx}*iw/{W}-{cx}))':y='max(0,min(ih-{H},{cy}*ih/{H}-{cy}))',setsar=1")
        if g.get("zoom") and k == 0:
            # com zoom, a caixa entra ANTES do zoom (cobre o texto em inglês, que também se move com o zoom)
            run(["ffmpeg", "-ss", f"{ini:.3f}", "-i", ORIG, "-loop", "1", "-i", caixa, "-an", "-frames:v", int(round(d * FPS)),
                 "-filter_complex", f"[0:v]fps={FPS},scale={W}:{H}[b];[b][1:v]overlay=0:0:shortest=1,{vf.split(',', 1)[1]}",
                 "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
            lista.append(f"file '{o.as_posix()}'")
            continue
        run(["ffmpeg", "-ss", f"{ini:.3f}", "-i", ORIG, "-an", "-frames:v", int(round(d * FPS)), "-vf", vf,
             "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
        lista.append(f"file '{o.as_posix()}'")
    (T / "lista.txt").write_text("\n".join(lista), encoding="utf-8")
    run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", T / "lista.txt", "-c", "copy", T / "g_v.mp4"])

    # ---- legenda da fala
    pal = LEG.palavras_por_alinhamento(str(alj), LEAD)
    preparar_fontsdir(T)
    LEG.gera_ass(pal, str(T / "leg.ass"), "drop", set(g["chaves"]), None, Hd)

    # ---- áudio: música do AD 04 nos Hd s antes do corte (só música ali) + fala com o nível da voz do corpo
    corpo_I = lufs(AD04, CORTE, 30)
    ganho = corpo_I - lufs(fala) - 0.5
    fc = [f"[1:a]atrim={CORTE - Hd:.4f}:{CORTE:.4f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[bg]",
          f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume={ganho:.2f}dB,adelay={int(LEAD * 1000)}|{int(LEAD * 1000)}[nv]",
          f"[bg][nv]amix=inputs=2:duration=first:normalize=0,atrim=0:{Hd:.4f}[ga]",
          "[0:v][3:v]overlay=0:0[v1]", "[v1][4:v]overlay=0:0[v2]" if not g.get("zoom") else "[v1]null[v2]",
          "[v2]ass=leg.ass:fontsdir=fonts,format=yuv420p,setsar=1[gv]"]
    run(["ffmpeg", "-i", T / "g_v.mp4", "-i", AD04, "-i", fala, "-loop", "1", "-t", f"{Hd:.3f}", "-i", FAIXA,
         "-loop", "1", "-t", f"{Hd:.3f}", "-i", caixa, "-filter_complex", ";".join(fc), "-map", "[gv]", "-map", "[ga]",
         "-t", f"{Hd:.4f}", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
         "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "gancho.mov"], cwd=T)

    # ---- gancho + AD 04 a partir do corte (mesmos 30 fps / 720x1280 / bt709), entrega <= 30 MB
    DF = dur(AD04)
    total = Hd + DF - CORTE
    v_kbps, _ = FIN.bitrate_alvo(total, 30, piso=FIN.QUALIDADE_MIN_720_KBPS)
    saida = OUT / f"{cod} - DEVOLVER-{g['nome']}-ES-CL.mp4"
    fc = ["[0:v]fps=30,setsar=1,format=yuv420p[v0]", "[1:v]fps=30,setsar=1,format=yuv420p[v1]",
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0]", "[1:a]aresample=48000,aformat=channel_layouts=stereo[a1]",
          "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"]
    run(["ffmpeg", "-i", T / "gancho.mov", "-ss", f"{CORTE:.3f}", "-i", AD04, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-pix_fmt", "yuv420p", *COR,
         "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps * 1.5)}k", "-bufsize", f"{v_kbps * 2}k",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida])
    FIN.revisar(str(saida), str(saida.with_name(saida.stem + "_frames.jpg")), esperado=(W, H))
    info = {"cod": cod, "saida": str(saida), "gancho_s": Hd, "fala_s": round(dur(fala), 3), "tomadas": segs,
            "corte_ad04": CORTE, "total_s": round(dur(saida), 2), "ganho_fala_db": round(ganho, 2),
            "mb": round(saida.stat().st_size / 1e6, 1), "kbps": v_kbps, "cenas": g["cenas"], "texto": g["texto"]}
    json.dump(info, open(T / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ok {cod} | gancho {Hd:.2f}s {segs} | total {info['total_s']}s | {info['mb']} MB | {saida.name}")


if __name__ == "__main__":
    for c in (sys.argv[1:] or list(G)):
        montar(c)
