# -*- coding: utf-8 -*-
"""F2 - Duelo bencina vs inalámbrica (corpo A).
Gancho 6,0 s em tela dividida: em cima take IA (Flora, MiniMax H3) do vizinho com cortadora a gasolina que não pega;
embaixo tomadas reais da nossa máquina cortando (original_04). Narração em 2 partes (voz clonada do corpo A),
caixa "¿CUÁL PREFIERES? 👇" na divisória e legenda drop. Depois o AD 04 intacto a partir de 9,0 s (mesma emenda do A)."""
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
D = BASE / "_vencedores" / "FORA_F2F6"
T = D / "trab" / "F2"
ORIG = BASE / "original_04.mp4"
AD04 = BASE / "AD 04 - PODADORA-INALAMBRICA-DEVOLVER-ES-CL.mp4"
TOPO = D / "takes" / "F2_topo_v1.mp4"
FALA = D / "voz" / "F2.mp3"
ALJ = D / "voz" / "F2.alinhamento.json"
OUT = BASE / "VENCEDORES" / "FORA"
CORTE = 9.0
W, H, PH = 720, 1280, 640
HD = 6.0
SPLIT = 1.97              # pausa real (silêncio 1,90-2,04) entre "…bencina…" e "y yo con esta."
P1, P2 = 0.30, 3.30       # início de cada parte no gancho
BAIXO = [(27.6, 69), (24.6, 69), (21.0, 42)]   # (início s, quadros) no original_04 = 180 q = 6,0 s
CROP_Y = 520              # faixa 720x640 do original sem o aviso em inglês do rodapé
TEXTO = "¿CUÁL PREFIERES? 👇"


def main():
    T.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    n = int(round(HD * FPS))
    # ---- painel de cima (IA)
    run(["ffmpeg", "-y", "-i", TOPO, "-an", "-frames:v", n, "-vf",
         f"fps={FPS},scale={W}:{W}:flags=lanczos,crop={W}:{PH}:0:20,setsar=1",
         "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, T / "topo.mp4"])
    # ---- painel de baixo (tomadas reais)
    lista = []
    for k, (ini, q) in enumerate(BAIXO):
        o = T / f"b{k}.mp4"
        run(["ffmpeg", "-y", "-ss", f"{ini:.3f}", "-i", ORIG, "-an", "-frames:v", q, "-vf",
             f"fps={FPS},scale={W}:{H},crop={W}:{PH}:0:{CROP_Y},setsar=1",
             "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", *COR, o])
        lista.append(f"file '{o.as_posix()}'")
    (T / "lista.txt").write_text("\n".join(lista), encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", T / "lista.txt", "-c", "copy", T / "baixo.mp4"])

    # ---- fala em 2 partes + legenda
    run(["ffmpeg", "-y", "-i", FALA, "-af", f"atrim=0:{SPLIT},asetpts=PTS-STARTPTS", T / "f1.wav"])
    run(["ffmpeg", "-y", "-i", FALA, "-af", f"atrim={SPLIT},asetpts=PTS-STARTPTS", T / "f2.wav"])
    pal = [(w, a + (P1 if a < SPLIT else P2 - SPLIT), b + (P1 if a < SPLIT else P2 - SPLIT))
           for w, a, b in LEG.palavras_por_alinhamento(str(ALJ))]
    preparar_fontsdir(T)
    LEG.gera_ass(pal, str(T / "leg.ass"), "drop", {"bencina", "esta"}, 1330, HD)   # y na escala 1080x1920 do .ass (= ~887 px em 1280)
    caixa = caixa_texto([TEXTO], T / "caixa.png", W, H, PH, 50, 0, 0, True)

    corpo_I = lufs(AD04, CORTE, 30)
    ganho = corpo_I - lufs(FALA) - 0.5
    fc = [
        "[0:v][1:v]vstack=inputs=2,drawbox=x=0:y=637:w=720:h=6:color=white@1:t=fill[st]",
        "[st][4:v]overlay=0:0[v1]", "[v1]ass=leg.ass:fontsdir=fonts,format=yuv420p,setsar=1[gv]",
        f"[2:a]atrim={CORTE - HD:.4f}:{CORTE:.4f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[bg]",
        f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume={ganho:.2f}dB,adelay={int(P1 * 1000)}|{int(P1 * 1000)}[n1]",
        f"[5:a]aresample=48000,aformat=channel_layouts=stereo,volume={ganho:.2f}dB,adelay={int(P2 * 1000)}|{int(P2 * 1000)}[n2]",
        f"[bg][n1][n2]amix=inputs=3:duration=first:normalize=0,atrim=0:{HD:.4f}[ga]",
    ]
    run(["ffmpeg", "-y", "-i", "topo.mp4", "-i", "baixo.mp4", "-i", AD04, "-i", "f1.wav",
         "-loop", "1", "-t", f"{HD:.3f}", "-i", caixa, "-i", "f2.wav",
         "-filter_complex", ";".join(fc), "-map", "[gv]", "-map", "[ga]", "-t", f"{HD:.4f}",
         "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", *COR,
         "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "gancho.mov"], cwd=T)

    # ---- gancho + AD 04 a partir do corte (igual ao montar_gancho.py do A)
    total = HD + dur(AD04) - CORTE
    v_kbps, _ = FIN.bitrate_alvo(total, 30, piso=FIN.QUALIDADE_MIN_720_KBPS)
    saida = OUT / "F2 - DUELO-BENCINA-A-ES-CL.mp4"
    fc = ["[0:v]fps=30,setsar=1,format=yuv420p[v0]", "[1:v]fps=30,setsar=1,format=yuv420p[v1]",
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0]", "[1:a]aresample=48000,aformat=channel_layouts=stereo[a1]",
          "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"]
    run(["ffmpeg", "-y", "-i", T / "gancho.mov", "-ss", f"{CORTE:.3f}", "-i", AD04, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-pix_fmt", "yuv420p", *COR,
         "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps * 1.5)}k", "-bufsize", f"{v_kbps * 2}k",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida])
    FIN.revisar(str(saida), str(saida.with_name(saida.stem + "_frames.jpg")), esperado=(W, H))
    info = {"saida": str(saida), "gancho_s": HD, "partes_fala": [P1, P2], "baixo": BAIXO, "ganho_fala_db": round(ganho, 2),
            "total_s": round(dur(saida), 2), "mb": round(saida.stat().st_size / 1e6, 1), "kbps": v_kbps}
    json.dump(info, open(T / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", info)


if __name__ == "__main__":
    main()
