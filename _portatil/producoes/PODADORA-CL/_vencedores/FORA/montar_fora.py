# -*- coding: utf-8 -*-
"""Criativos "fora da caixa" F3 (esquete da vizinha, corpo A) e F5 (presente pro pai, corpo B).
  python montar_fora.py F3 [F5]   (sem argumento = os dois)
Gancho: clipes de avatar HeyGen (photo avatar com lipsync do áudio ElevenLabs) + takes reais do próprio vencedor,
legenda drop da fala, faixa do aviso só nos takes do original_04 (corpo A), música/ambiente do próprio vencedor
imediatamente antes do corte (emenda contínua). Corpo: vencedor a partir do corte, sem alteração (só recodificação)."""
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
F = BASE / "_vencedores" / "FORA"
OUT = BASE / "VENCEDORES" / "FORA"
W, H = 720, 1280
PAD = 0.15        # silêncio colocado antes da fala no áudio enviado ao HeyGen (o clipe começa 0,15 s antes da voz)

ORIG04 = BASE / "original_04.mp4"
AD04 = BASE / "AD 04 - PODADORA-INALAMBRICA-DEVOLVER-ES-CL.mp4"
FAIXA04 = BASE / "_trabalho" / "04" / "faixa.png"
V1 = BASE / "_vencedores" / "vencedor1.mp4"
BED_B = F / "bed_F5.wav"   # no_vocals do vencedor1: 21,45–22,25 s (take das rodas) + 0–2,1 s (emenda no corpo)

# segmento: ("av", nome, fala|None) | ("src", arquivo, ini, n_quadros, faixa?) ; None em ini = termina no corte
G = {
    "F3": dict(nome="VECINA-SAPA-A", corpo=AD04, corte=9.0, lado="A",
               segs=[("av", "F3_vizinha"), ("av", "F3_dono"), ("src", ORIG04, 27.6, 36, True), ("src", ORIG04, None, 30, True)],
               chaves=["carísimo", "diez"], caixa=None,
               cenas="avatar vizinha na cerca (HeyGen) → avatar dono com a máquina (HeyGen) → close da máquina cortando o mato alto "
                     "(original_04 27,6–28,8 s, só pernas) → câmera da porta cortando o mato (original_04 8,0–9,0 s, emenda contínua no corpo)"),
    "F5": dict(nome="REGALO-PAPA-B", corpo=V1, corte=2.1, lado="B",
               segs=[("av", "F5_senhor"), ("src", V1, 21.45, 24, False), ("src", V1, None, 63, False)],
               chaves=["liviana", "ruedas"], caixa=dict(linhas=["EL REGALO PARA PAPÁ 🎁"], cy=135, px=48),
               cenas="avatar senhor segurando a máquina (HeyGen, imagem base Flora a partir da foto do kit) → máquina com rodas vindo "
                     "em direção à câmera (vencedor1 21,45–22,25 s) → corredor com o mato alto (vencedor1 0,0–2,1 s, emenda contínua no corpo)"),
}
VOZ_LUFS_B = -14.3


def montar(cod):
    g = G[cod]
    T = F / "trab" / cod
    T.mkdir(parents=True, exist_ok=True)
    corte = g["corte"]
    # ---- partes do vídeo (quadros exatos, 30 fps, 720x1280)
    partes, falas, t, faixa_jan = [], [], 0.0, []
    for k, s in enumerate(g["segs"]):
        o = T / f"p{k}.mp4"
        if s[0] == "av":
            av = F / "av" / f"{s[1]}.mp4"
            n = int(round(dur(av) * FPS)) - 1
            run(["ffmpeg", "-i", av, "-an", "-vf", f"fps={FPS},scale={W}:{H},setsar=1", "-frames:v", n,
                 "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
            falas.append((F / "voz" / f"{s[1]}.mp3", F / "voz" / f"{s[1]}.alinhamento.json", t + PAD))
        else:
            _, src, ini, n, fx = s
            if ini is None:
                ini = round(corte - n / FPS, 4)
            run(["ffmpeg", "-ss", f"{ini:.3f}", "-i", src, "-an", "-frames:v", n, "-vf", f"fps={FPS},scale={W}:{H},setsar=1",
                 "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
            if fx:
                faixa_jan.append((round(max(0, t - 0.02), 4), round(t + n / FPS, 4)))
        nq = int(round(dur(o) * FPS))
        partes.append((o, nq, s))
        t += nq / FPS
    Hd = round(t * FPS) / FPS
    if g["lado"] == "A" and Hd > corte:
        raise SystemExit("gancho maior que o trecho de música antes do corte")
    ins = [x for p in partes for x in ("-i", p[0])]
    fc = "".join(f"[{i}:v]" for i in range(len(partes))) + f"concat=n={len(partes)}:v=1:a=0[v]"
    run(["ffmpeg", *ins, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-crf", "12", "-preset", "fast",
         "-pix_fmt", "yuv420p", *COR, T / "g_v.mp4"])

    # ---- legenda (falas emendadas)
    pal = []
    for mp3, alj, t0 in falas:
        pal += LEG.palavras_por_alinhamento(str(alj), t0)
    preparar_fontsdir(T)
    LEG.gera_ass(pal, str(T / "leg.ass"), "drop", set(g["chaves"]), None, Hd)

    # ---- áudio: fundo do próprio vencedor antes do corte + falas no nível da voz do corpo
    if g["lado"] == "A":
        alvo = lufs(AD04, corte, 30) - 0.5
        bg = [f"[1:a]atrim={corte - Hd:.4f}:{corte:.4f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[bg]"]
        a_in = ["-i", AD04]
    else:
        alvo = VOZ_LUFS_B
        bd = dur(BED_B)
        bg = [f"[1:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int((Hd - bd) * 1000)}|{int((Hd - bd) * 1000)},"
              f"apad=whole_dur={Hd:.4f}[bg]"]
        a_in = ["-i", BED_B]
    fc, ganhos = list(bg), []
    for i, (mp3, _, t0) in enumerate(falas):
        gdb = alvo - lufs(mp3)
        ganhos.append(round(gdb, 2))
        a_in += ["-i", mp3]
        fc.append(f"[{2 + i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gdb:.2f}dB,"
                  f"adelay={int(t0 * 1000)}|{int(t0 * 1000)}[f{i}]")
    nf = len(falas)
    fc.append("[bg]" + "".join(f"[f{i}]" for i in range(nf)) + f"amix=inputs={nf + 1}:duration=first:normalize=0,atrim=0:{Hd:.4f}[ga]")
    v_in, vk, n_in = [], "[0:v]", 2 + nf
    if faixa_jan:
        v_in += ["-loop", "1", "-t", f"{Hd:.3f}", "-i", FAIXA04]
        en = "+".join(f"between(t,{a},{b})" for a, b in faixa_jan)
        fc.append(f"{vk}[{n_in}:v]overlay=0:0:enable='{en}'[vf]")
        vk, n_in = "[vf]", n_in + 1
    if g["caixa"]:
        c = g["caixa"]
        png = caixa_texto(c["linhas"], T / "caixa.png", W, H, c["cy"], c["px"], 0, 0, True, maxw=W - 40)
        v_in += ["-loop", "1", "-t", f"{Hd:.3f}", "-i", png]
        fc.append(f"{vk}[{n_in}:v]overlay=0:0[vc]")
        vk, n_in = "[vc]", n_in + 1
    fc.append(f"{vk}ass=leg.ass:fontsdir=fonts,format=yuv420p,setsar=1[gv]")
    run(["ffmpeg", "-i", T / "g_v.mp4", *a_in, *v_in, "-filter_complex", ";".join(fc), "-map", "[gv]", "-map", "[ga]",
         "-t", f"{Hd:.4f}", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
         "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "gancho.mov"], cwd=T)

    # ---- gancho + corpo do vencedor a partir do corte (sem alteração), entrega <= 30 MB
    corpo = g["corpo"]
    total = Hd + dur(corpo) - corte
    v_kbps, _ = FIN.bitrate_alvo(total, 30, piso=FIN.QUALIDADE_MIN_720_KBPS)
    OUT.mkdir(parents=True, exist_ok=True)
    saida = OUT / f"{cod} - {g['nome']}-ES-CL.mp4"
    fc = ["[0:v]fps=30,setsar=1,format=yuv420p[v0]",
          f"[1:v]fps=30,scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[v1]",
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0]", "[1:a]aresample=48000,aformat=channel_layouts=stereo[a1]",
          "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"]
    run(["ffmpeg", "-i", T / "gancho.mov", "-ss", f"{corte:.3f}", "-i", corpo, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-pix_fmt", "yuv420p", *COR,
         "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps * 1.5)}k", "-bufsize", f"{v_kbps * 2}k",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida])
    FIN.revisar(str(saida), str(saida.with_name(saida.stem + "_frames.jpg")), esperado=(W, H))
    info = {"cod": cod, "saida": str(saida), "gancho_s": Hd, "partes": [(str(p[0].name), p[1]) for p in partes],
            "falas": [(str(m.name), round(t0, 3), round(dur(m), 3)) for m, _, t0 in falas], "ganhos_db": ganhos,
            "corte": corte, "total_s": round(dur(saida), 2), "mb": round(saida.stat().st_size / 1e6, 1), "kbps": v_kbps,
            "cenas": g["cenas"]}
    json.dump(info, open(T / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ok {cod} | gancho {Hd:.2f}s | total {info['total_s']}s | {info['mb']} MB | {saida.name}")


if __name__ == "__main__":
    for c in (sys.argv[1:] or list(G)):
        montar(c)
