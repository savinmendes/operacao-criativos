# -*- coding: utf-8 -*-
"""Monta um corpo 9:16 intercalando clipes de avatar (HeyGen com lipsync da narração inteira) e takes do vídeo
original SEM o rosto/legenda: tela cheia recortada (P), tela dividida avatar em cima + recorte embaixo (S) ou um
clipe pronto (T). O áudio é a narração.

  python montar_corpo_avatar.py plano.json [--saida corpo.mp4] [--placeholder] [--resolucao 720]

plano.json (caminhos relativos à pasta do plano; tempos em s; coords do original em px do ORIGINAL,
"faixa"/"av_y" etc. em px da SAÍDA):
{
 "original": "../originais/01.mp4",
 "avatar": "av.mp4",                 // vídeo do avatar (lipsync da narração inteira, mesmo tempo da narração)
 "avatar_img": "avatar.webp",        // foto parada usada com --placeholder (antes do HeyGen ficar pronto)
 "narr": "narr.mp3",                 // narração: vira o áudio do corpo (normalizada a -15 LUFS)
 "cauda": 0.5,                       // s de avatar congelado depois do fim da fala
 "resolucao": "720",                 // 720 (720x1280) ou 1080
 "A_zoom": 1.0625, "A_shift": 70,    // zoom e deslocamento vertical do avatar (sobe o rosto; legenda não cobre a boca)
 "P": {"x": 132, "y": 470, "w": 456, "faixa": [575, 680], "desfocar": [x0, y0, x1, y1]},
       // take cheio: recorte 9:16 do original (largura w a partir de x,y) + faixa opaca na saída (cobre legenda)
       // + desfoque opcional de uma região do original (rosto de terceiro, tela) antes do recorte
 "S": {"av_y": 60, "av_h": 835, "src_y": 530, "src_h": 420, "src_x": null, "desfocar": null},
       // dividida: avatar (recorte av_y..av_y+av_h) em cima + recorte do original (src_y, src_h) embaixo
 "segs": [["A", 0, 4.6], ["P", 4.6, 6.85, 5.6], ["S", 6.85, 9.0, 3.0, 0.9], ["T", 9.0, 12.0, "b1.mp4", 0, 1.0]]
       // tipo, ini, fim (tempo do corpo); P/S: src_ini [, vel [, {sobrescreve P/S só aqui}]]; T: arquivo [, ini, vel]
       // o último segmento vai até o fim (fala + cauda)
}
Todas as partes saem com os mesmos metadados de cor (bt709/tv) e a emenda é RECODIFICADA (nada de -c copy):
partes com tags diferentes faziam o ffmpeg reconfigurar o filtergraph no montar_ad e perder overlays e áudio.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import COR, FPS, dur, resolucao, run  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plano")
    ap.add_argument("--saida", help="padrão: corpo.mp4 (ou corpo_placeholder.mp4) ao lado do plano")
    ap.add_argument("--placeholder", action="store_true", help="usa avatar_img parado no lugar do vídeo do avatar")
    ap.add_argument("--resolucao", default=None, help="720 ou 1080 (padrão: do plano, senão 720)")
    ap.add_argument("--crf", type=int, default=16)
    a = ap.parse_args()

    PL = Path(a.plano).resolve()
    D = PL.parent
    R = json.load(open(PL, encoding="utf-8"))
    P = lambda p: str((D / p).resolve()) if p and not Path(p).is_absolute() else p  # noqa: E731
    W, H = resolucao(a.resolucao or R.get("resolucao", "720"))
    PH = a.placeholder
    TMP = D / "segs"
    TMP.mkdir(exist_ok=True)
    ENC = ["-c:v", "libx264", "-crf", str(a.crf), "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), *COR]

    narr = P(R["narr"])
    total = dur(narr) + R.get("cauda", 0.5)
    segs = [list(s) for s in R["segs"]]
    segs[-1][2] = total   # último segmento vai até o fim (cauda)
    original = P(R.get("original"))

    if PH:
        av_in = ["-loop", "1", "-framerate", str(FPS), "-i", P(R["avatar_img"])]
    else:
        av_in = ["-i", P(R["avatar"])]
    av_base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS}"

    def desfoque(spec):
        """Filtro que desfoca uma caixa do original antes do recorte (coords do original)."""
        if not spec or not spec.get("desfocar"):
            return "[0:v]"
        bx0, by0, bx1, by1 = spec["desfocar"]
        return (f"[0:v]split[db][dc];[dc]crop={bx1 - bx0}:{by1 - by0}:{bx0}:{by0},gblur=sigma=6[bl];"
                f"[db][bl]overlay={bx0}:{by0}[dz];[dz]")

    lista = []
    for k, s in enumerate(segs):
        tipo, ini, fim = s[0], float(s[1]), float(s[2])
        d = fim - ini
        out = TMP / f"s{k:02d}.mp4"
        if tipo == "A":
            ss = ["-ss", f"{ini:.3f}"] if not PH else []
            z = R.get("A_zoom", 1.0)
            vfa = av_base if z == 1.0 else (
                f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                f"scale={round(W * z / 2) * 2}:{round(H * z / 2) * 2},crop={W}:{H}:(iw-{W})/2:{R.get('A_shift', 0)},"
                f"setsar=1,fps={FPS}")
            vfa += ",tpad=stop_mode=clone:stop_duration=3"   # avatar acaba junto com a fala: congela na cauda
            run(["ffmpeg", *ss, *av_in, "-vf", vfa, "-t", f"{d:.3f}", "-an", *ENC, out])
        elif tipo in ("P", "S"):
            src0 = float(s[3])
            vel = float(s[4]) if len(s) > 4 and s[4] is not None else 1.0
            extra = s[5] if len(s) > 5 and isinstance(s[5], dict) else {}
            need = d * vel + 0.1
            p = {**R[tipo], **extra}
            if tipo == "P":
                h = round(p["w"] * 16 / 9)
                y = min(p["y"], R.get("original_h", 1280) - h)
                vf = (f"{desfoque(p)}setpts=(PTS-STARTPTS)/{vel},crop={p['w']}:{h}:{p['x']}:{y},"
                      f"scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}")
                if p.get("faixa"):
                    vf += (f"[v0];[v0]drawbox=x=0:y={p['faixa'][0]}:w={W}:h={p['faixa'][1] - p['faixa'][0]}:"
                           f"color=black@0.99:t=fill[v]")
                else:
                    vf += "[v]"
                run(["ffmpeg", "-ss", f"{src0:.3f}", "-t", f"{need:.3f}", "-i", original,
                     "-filter_complex", vf, "-map", "[v]", "-t", f"{d:.3f}", "-an", *ENC, out])
            else:
                ah = p["av_h"]
                sh = H - ah
                sw = round(W * p["src_h"] / sh)          # recorte do original com a proporção da metade de baixo
                sx = p.get("src_x")
                if sx is None:
                    sx = (R.get("original_w", 720) - sw) // 2
                ss = ["-ss", f"{ini:.3f}"] if not PH else []
                fc = (f"[0:v]{av_base},crop={W}:{ah}:0:{p['av_y']}[top];"
                      f"{desfoque(p).replace('[0:v]', '[1:v]')}setpts=(PTS-STARTPTS)/{vel},"
                      f"crop={sw}:{p['src_h']}:{sx}:{p['src_y']},scale={W}:{sh}:flags=lanczos,setsar=1,fps={FPS}[bot];"
                      f"[top][bot]vstack[v]")
                run(["ffmpeg", *ss, *av_in, "-ss", f"{src0:.3f}", "-t", f"{need:.3f}", "-i", original,
                     "-filter_complex", fc, "-map", "[v]", "-t", f"{d:.3f}", "-an", *ENC, out])
        elif tipo == "T":
            clipe = P(s[3])
            t0 = float(s[4]) if len(s) > 4 and s[4] is not None else 0.0
            vel = float(s[5]) if len(s) > 5 and s[5] is not None else 1.0
            vf = (f"setpts=(PTS-STARTPTS)/{vel},{av_base},tpad=stop_mode=clone:stop_duration={d:.3f}")
            run(["ffmpeg", "-ss", f"{t0:.3f}", "-i", clipe, "-vf", vf, "-t", f"{d:.3f}", "-an", *ENC, out])
        else:
            raise SystemExit(f"tipo de segmento desconhecido: {tipo}")
        lista.append(out)
        print(f"[{k + 1}/{len(segs)}] {tipo} {ini:.2f}-{fim:.2f}", flush=True)

    txt = TMP / "lista.txt"
    txt.write_text("".join(f"file '{p.as_posix()}'\n" for p in lista), encoding="utf-8")
    saida = Path(a.saida).resolve() if a.saida else D / ("corpo_placeholder.mp4" if PH else "corpo.mp4")
    run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", txt, "-i", narr, "-filter_complex",
         f"[0:v]fps={FPS},setsar=1,format=yuv420p[v];[1:a]loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,"
         f"apad=whole_dur={total:.3f}[a]", "-map", "[v]", "-map", "[a]", *ENC,
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", saida])
    print(f"ok {saida} | {dur(saida):.2f}s (fala {dur(narr):.2f}s) | {W}x{H}")


if __name__ == "__main__":
    main()
