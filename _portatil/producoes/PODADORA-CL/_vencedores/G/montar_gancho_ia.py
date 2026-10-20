# -*- coding: utf-8 -*-
"""Criativos "fora da caixa" G1-G5: gancho com takes IA (Flora: Nano Banana 2 + MiniMax H3 Max) + corpo A (AD 04) intacto.
  python montar_gancho_ia.py G1 [G2 ...]   (sem argumento = todos)
Baseado em _vencedores/A/montar_gancho.py: mesma emenda (corte 9,0 s), mesma faixa do aviso, mesma caixa e legenda,
música do próprio AD 04 nos Hd s antes do corte, fala igualada ao LUFS da voz do corpo."""
import json
import sys
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
from comum import COR, FPS, dur, preparar_fontsdir, run  # noqa: E402
import finalizar as FIN  # noqa: E402
import legenda as LEG  # noqa: E402
from gerar_variacao import caixa_texto, lufs  # noqa: E402

BASE = Path(r"C:\Users\PICHAU\Downloads\PODADORA-CL")
G_DIR = BASE / "_vencedores" / "G"
TAKES = G_DIR / "takes"
AD04 = BASE / "AD 04 - PODADORA-INALAMBRICA-DEVOLVER-ES-CL.mp4"
FAIXA = BASE / "_trabalho" / "04" / "faixa.png"
OUT = BASE / "VENCEDORES" / "FORA"
CORTE = 9.0
W, H = 720, 1280
LEAD, CAUDA, MIN_H = 0.12, 0.35, 4.0
CAIXA = dict(cy=470, px=46, min_w=520, min_h=84)

# tomadas: (arquivo em takes/, início no clipe, duração | None = completa até Hd)
G = {
    "G1": dict(nome="SELVA", texto=["DE SELVA A JARDÍN 🌿"], tomadas=[("G1a.mp4", 0.3, 1.7), ("G1b.mp4", 0.4, None)],
               chaves=["selva", "esto"]),
    "G2": dict(nome="DOMINGO-LIBRE", texto=["DOMINGO LIBRE ☕"], tomadas=[("G2.mp4", 0.0, None)],
               chaves=["domingo", "ahora"]),
    "G3": dict(nome="UNA-MANO", texto=["CON UNA MANO ✋"], tomadas=[("G3.mp4", 0.0, None)],
               chaves=["mano", "fácil"]),
    "G4": dict(nome="LLUVIA-DE-PASTO", texto=["MIRA CÓMO CORTA"], tomadas=[("G4.mp4", 0.2, None)],
               chaves=["corta", "alto"]),
    "G5": dict(nome="CAJA-EN-LA-PUERTA", texto=["PAGAS AL RECIBIR 📦"], tomadas=[("G5a.mp4", 0.2, 1.8), ("G5b.mp4", 0.3, None)],
               chaves=["internet", "llegó"]),
}


def fim_fala(al_path):
    al = json.load(open(al_path, encoding="utf-8"))
    al = al.get("alignment") or al.get("normalized_alignment") or al
    return max(e for c, e in zip(al["characters"], al["character_end_times_seconds"]) if c.strip())


def montar(cod):
    g = G[cod]
    T = G_DIR / "trab" / cod
    T.mkdir(parents=True, exist_ok=True)
    fala = G_DIR / "voz" / f"{cod}.mp3"
    alj = G_DIR / "voz" / f"{cod}.alinhamento.json"
    Hd = round(max(MIN_H, LEAD + fim_fala(alj) + CAUDA) * FPS) / FPS
    if Hd > CORTE:
        raise SystemExit("gancho maior que o trecho de música antes do corte")
    caixa = caixa_texto(g["texto"], T / "caixa.png", W, H, CAIXA["cy"], g.get("px", CAIXA["px"]), CAIXA["min_w"], CAIXA["min_h"], True)

    fixos = sum(t[2] for t in g["tomadas"] if t[2])
    segs, lista = [], []
    for k, (arq, ini, d) in enumerate(g["tomadas"]):
        if d is None:
            d = round((Hd - fixos) * FPS) / FPS
        src = TAKES / arq
        if ini + d > dur(src) + 0.01:
            raise SystemExit(f"{arq}: trecho {ini}+{d} passa do fim do clipe ({dur(src):.2f})")
        segs.append((arq, ini, d))
        o = T / f"t{k}.mp4"
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},setsar=1"
        run(["ffmpeg", "-ss", f"{ini:.3f}", "-i", src, "-an", "-frames:v", int(round(d * FPS)), "-vf", vf,
             "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
        lista.append(f"file '{o.as_posix()}'")
    (T / "lista.txt").write_text("\n".join(lista), encoding="utf-8")
    run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", T / "lista.txt", "-c", "copy", T / "g_v.mp4"])

    pal = LEG.palavras_por_alinhamento(str(alj), LEAD)
    preparar_fontsdir(T)
    LEG.gera_ass(pal, str(T / "leg.ass"), "drop", set(g["chaves"]), None, Hd)

    corpo_I = lufs(AD04, CORTE, 30)
    ganho = corpo_I - lufs(fala) - 0.5
    fc = [f"[1:a]atrim={CORTE - Hd:.4f}:{CORTE:.4f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[bg]",
          f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume={ganho:.2f}dB,adelay={int(LEAD * 1000)}|{int(LEAD * 1000)}[nv]",
          f"[bg][nv]amix=inputs=2:duration=first:normalize=0,atrim=0:{Hd:.4f}[ga]",
          "[0:v][3:v]overlay=0:0[v1]", "[v1][4:v]overlay=0:0[v2]",
          "[v2]ass=leg.ass:fontsdir=fonts,format=yuv420p,setsar=1[gv]"]
    run(["ffmpeg", "-i", T / "g_v.mp4", "-i", AD04, "-i", fala, "-loop", "1", "-t", f"{Hd:.3f}", "-i", FAIXA,
         "-loop", "1", "-t", f"{Hd:.3f}", "-i", caixa, "-filter_complex", ";".join(fc), "-map", "[gv]", "-map", "[ga]",
         "-t", f"{Hd:.4f}", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
         "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "gancho.mov"], cwd=T)

    DF = dur(AD04)
    total = Hd + DF - CORTE
    v_kbps, _ = FIN.bitrate_alvo(total, 30, piso=FIN.QUALIDADE_MIN_720_KBPS)
    OUT.mkdir(parents=True, exist_ok=True)
    saida = OUT / f"{cod} - {g['nome']}-A-ES-CL.mp4"
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
            "mb": round(saida.stat().st_size / 1e6, 1), "kbps": v_kbps, "texto": g["texto"]}
    json.dump(info, open(T / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ok {cod} | gancho {Hd:.2f}s {segs} | total {info['total_s']}s | {info['mb']} MB | {saida.name}")


if __name__ == "__main__":
    for c in (sys.argv[1:] or list(G)):
        montar(c)
