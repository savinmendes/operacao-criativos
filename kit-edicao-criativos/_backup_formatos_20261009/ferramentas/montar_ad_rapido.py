# -*- coding: utf-8 -*-
"""Versão rápida do montar_ad.py: UMA passada de ffmpeg (encaixe + volume + legenda + selo + setas + compressão
final ≤ limite MB), em vez de 3 recodificações. Mesma receita JSON do montar_ad.py.

Cobre receitas com: corpo, hook {"tipo":"antes"} (opcional), legenda, manchete, faixa_sb, selo, cta, limite_mb,
resolucao ("720" -> entrega 720x1280; padrão "1080" -> 1080x1920).
Receitas com cortar_pausas, trilha ou hook do tipo "imagem" -> usa o montar_ad.py clássico automaticamente.

  python montar_ad_rapido.py receita.json
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import W, H, FPS, run, dur, tmpdir, preparar_fontsdir, tem_audio, mb  # noqa: E402
import legenda as LEG  # noqa: E402
import overlays as OV  # noqa: E402
import finalizar as FIN  # noqa: E402
import montar_ad as CLASSICO  # noqa: E402


def elegivel(rec: dict) -> bool:
    h = rec.get("hook") or {}
    return (rec.get("corpo") and not rec.get("cortar_pausas") and not rec.get("trilha")
            and h.get("tipo", "antes") == "antes")


def montar(rec: dict, base_dir: Path):
    if not elegivel(rec):
        print("receita fora do caminho rápido -> montar_ad clássico")
        return CLASSICO.montar(rec, base_dir)
    t0 = time.time()
    P = lambda p: str((base_dir / p).resolve()) if p and not Path(p).is_absolute() else p  # noqa: E731
    wk = tmpdir("adr_")
    estilo = rec.get("estilo", "drop")
    saida = P(rec["saida"])
    partes = []
    h = rec.get("hook") or {}
    if h.get("video"):
        partes.append(P(h["video"]))
    partes.append(P(rec["corpo"]))
    durs = [dur(p) for p in partes]
    deslocamento = durs[0] if len(partes) == 2 else 0.0
    total = sum(durs)

    # palavras (legenda + CTA) — só do corpo, deslocadas pela duração da parte 1
    lg = rec.get("legenda", {"fonte": "nenhuma"})
    fonte = lg.get("fonte", "nenhuma")
    pal = []
    if fonte.startswith("alinhamento:"):
        pal = LEG.palavras_por_alinhamento(P(fonte.split(":", 1)[1]), deslocamento)
    elif fonte == "transcrever":
        pal = [(w, a + deslocamento, b + deslocamento) for w, a, b in
               LEG.palavras_por_whisper(partes[-1], lg.get("idioma", "es"), lg.get("modelo", "small"))]
    elif fonte.startswith("texto:"):
        frases = [l.strip() for l in open(P(fonte.split(":", 1)[1]), encoding="utf-8") if l.strip()]
        pal = [(w, a + deslocamento, b + deslocamento) for w, a, b in LEG.palavras_por_texto(frases, partes[-1])]
    lh = rec.get("legenda_hook")   # legenda também na parte 1 (ex.: vídeo dublado, sem legenda queimada)
    if lh and len(partes) == 2:
        ph = LEG.palavras_por_whisper(partes[0], lh.get("idioma", "es"), lh.get("modelo", "small"))
        # junta elisões que o whisper separa ("l" + "'appunto" -> "l'appunto") e aplica correções
        # opcionais {"corrigir": [[regex, troca], ...]} (ex.: nome de marca mal transcrito)
        junt = []
        for w, a, b in ph:
            if junt and w.startswith("'") and re.fullmatch(
                    r"(l|d|c|s|m|t|v|n|un|dell|nell|sull|dall|all|quell|quest)", junt[-1][0], re.I):
                w0, a0, _ = junt.pop()
                w, a = w0 + w, a0
            junt.append((w, a, b))
        for rx, troca in lh.get("corrigir", []):
            junt = [(re.sub(rx, troca, w, flags=re.I), a, b) for w, a, b in junt]
        pal = junt + pal
    pal_leg = [p for p in pal if p[1] >= lg.get("desde", 0)]

    ins, fc = [], []
    for k, p in enumerate(partes):
        # -reinit_filter 0: se os metadados de cor mudarem no meio do corpo (ex.: concat -c copy de takes
        # HeyGen + vídeo original), o ffmpeg refaz o filtergraph e perde as entradas PNG (setas/manchete)
        # e o que estava bufferizado (loudnorm ~3 s de áudio). Desligado, o scale lida com a mudança.
        ins += ["-reinit_filter", "0", "-i", p]
    n = len(partes)
    for k, p in enumerate(partes):
        fc.append(f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
                  f"fps={FPS},setsar=1[v{k}]")
        if tem_audio(p):
            fc.append(f"[{k}:a]loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a{k}]")
        else:
            fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{durs[k]:.3f}[a{k}]")
    fc.append("".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    ult, idx = "[vc]", n

    preparar_fontsdir(wk)
    if pal_leg:
        LEG.gera_ass(pal_leg, str(wk / "leg.ass"), estilo, set(lg.get("chaves", [])), lg.get("y"), total)
        fc.append(f"{ult}ass=leg.ass:fontsdir=fonts[l]")
        ult = "[l]"

    def camada(png, x, y, enable=None):
        nonlocal ult, idx
        ins.extend(["-i", png])
        en = f":enable='{enable}'" if enable else ""
        fc.append(f"{ult}[{idx}:v]overlay={x}:{y}{en}[o{idx}]")
        ult = f"[o{idx}]"
        idx += 1

    if rec.get("faixa_sb", estilo == "sb"):
        camada(OV.faixa_sb(str(wk / "faixa.png")), 0, 150)
    if rec.get("manchete"):
        m = rec["manchete"]
        camada(OV.manchete(m["texto"], str(wk / "manchete.png"), m.get("px", 64)), 0, m.get("y", 140),
               f"lt(t,{m['ate']})" if m.get("ate") else None)
    if rec.get("selo"):
        s = rec["selo"]
        camada(OV.selo(s["linhas"], str(wk / "selo.png")), s.get("x", 160), s.get("y", 1225),
               f"gte(t,{s['desde']})" if s.get("desde") else None)
    t_cta = None
    cta = rec.get("cta")
    if cta:
        if "inicio" in cta:
            t_cta = float(cta["inicio"])
        else:
            alvo = LEG._limpa(cta.get("palavra", "toca"))
            cand = [p for p in pal if LEG._limpa(p[0]).startswith(alvo) and p[1] >= total * 0.5]
            t_cta = cand[-1][1] if cand else max(0, total - 4)
        seta = OV.seta(str(wk / "seta.png"))
        for x in cta.get("x", [300, 610]):
            ins.extend(["-i", seta])
            fc.append(f"{ult}[{idx}:v]overlay={x}:'{cta.get('y', 1630)}+20*sin(3*PI*t)'"
                      f":enable='gte(t,{t_cta:.2f})'[o{idx}]")
            ult = f"[o{idx}]"
            idx += 1

    r720 = str(rec.get("resolucao", "1080")) == "720"
    esperado = (720, 1280) if r720 else (W, H)
    if r720:   # camadas foram posicionadas em 1080x1920; reduz só na saída
        fc.append(f"{ult}scale=720:1280:flags=lanczos[res]")
        ult = "[res]"
    limite = rec.get("limite_mb", 30)
    v_kbps, cabe = FIN.bitrate_alvo(total, limite, piso=FIN.QUALIDADE_MIN_720_KBPS if r720 else None)
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", *ins, "-filter_complex", ";".join(fc), "-map", ult, "-map", "[ac]",
         "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps * 1.5)}k", "-bufsize", f"{v_kbps * 2}k",
         "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", saida], cwd=wk)
    if cabe and mb(saida) > limite:      # raro: refaz pelo finalizar com folga
        FIN.encode(saida, saida.replace(".mp4", "_tmp.mp4"), limite * 0.85)
        Path(saida.replace(".mp4", "_tmp.mp4")).replace(saida)
    tempos = [1.0, total * 0.5] + ([t_cta + 0.5] if t_cta else []) + [-0.8]
    FIN.revisar(saida, str(Path(saida).with_suffix("")) + "_frames.jpg", tempos, esperado)
    print(f"CTA em {t_cta:.2f}s" if t_cta else "sem CTA")
    print(f"montagem rápida: {time.time() - t0:.0f}s para {total:.0f}s de vídeo ({(time.time() - t0) / total:.2f}x)")
    return saida


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    rec_path = Path(sys.argv[1]).resolve()
    montar(json.loads(rec_path.read_text(encoding="utf-8")), rec_path.parent)


if __name__ == "__main__":
    main()
