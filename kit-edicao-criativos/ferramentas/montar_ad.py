# -*- coding: utf-8 -*-
"""Monta um criativo inteiro a partir de uma receita JSON (hook + corpo + legenda + overlays + CTA)
e já finaliza (≤30 MB) e revisa (decodificação + folha de frames).

  python montar_ad.py receita.json

Receita (todas as chaves são opcionais, exceto "saida" e "corpo" OU "narracao"+"takes"):
{
  "saida": "AD 08 - DESM-H09-GRAMA.mp4",
  "estilo": "drop",                      // "drop" (Poppins, legenda y=1060) ou "sb" (Anton, y=1480 + faixa de topo)
  "corpo": "corpo.mp4",                  // vídeo com a narração/fala
  "narracao": "narr.mp3",                // OU: narração + takes -> monta o corpo com b-roll sem repetir
  "takes": ["t1.mp4", "t2.mp4"],
  "cortar_pausas": true,                 // tira silêncios longos do corpo
  "hook": {"tipo": "imagem", "video": "hook.mp4", "ate": 4.5},           // cobre a imagem do início; som do corpo segue
  // "hook": {"tipo": "imagem", "trechos": [["X04.mp4",0.9,1.6],["X02.mp4",1.2,2.7]], "vel": 1.3},
  // "hook": {"tipo": "antes", "video": "hook_avatar.mp4"},              // avatar HeyGen com fala própria, antes do corpo
  "trilha": "musica.mp3",                // trilha baixa (-29 LUFS) com ducking
  "legenda": {"fonte": "transcrever", "idioma": "es", "chaves": ["árboles","pasto"], "desde": 0},
  //          fonte: "transcrever" | "alinhamento:narr.alinhamento.json" | "texto:frases.txt" | "nenhuma"
  "manchete": {"texto": "¡CORTA HASTA ÁRBOLES! 😱", "y": 140, "ate": 4.5, "px": 64},
  "faixa_sb": true,                      // faixa "Un último aviso" (padrão no estilo sb)
  "selo": {"linhas": ["SIN BENCINA · 100% ELÉCTRICA","PAGO CONTRA","ENTREGA","¡PAGAS AL RECIBIR!"], "x": 160, "y": 1225},
  "cta": {"palavra": "toca"},            // setas entram nessa palavra (2ª metade do vídeo) ... ou {"inicio": 22.5}
  "formato": "9:16",                     // "9:16" (padrão) | "4:5" | "1:1"
  "resolucao": "1080",                   // "720" | "1080" = largura: 9:16 720x1280/1080x1920, 4:5 720x900/1080x1350,
                                         //                              1:1 720x720/1080x1080
  "limite_mb": 30
}
Posições (legenda.y, manchete.y, selo.x/y, cta.x/y, faixa_sb {"y"}) são px do quadro BASE de 1080 de largura do
formato (1080x1920 / 1080x1350 / 1080x1080), mesmo com "resolucao": "720" (as camadas são reduzidas na saída).
Em vez do px absoluto dá para usar "y_rel" (0–1 da altura do quadro): ex. "selo": {..., "y_rel": 0.2}.
Sem posição, vale o padrão do formato (comum.layout_padrao; no 9:16 os de sempre). selo/cta aceitam "escala"
(padrão 1 no 9:16, 0,85 no 4:5, 0,75 no 1:1).
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from comum import (W, H, FPS, FORMATO_PADRAO, run, dur, tmpdir, preparar_fontsdir, vf_vertical, tem_audio,  # noqa: E402
                   dimensoes, resolucao, layout_padrao, resolver_y)
import audio as AUD  # noqa: E402
import legenda as LEG  # noqa: E402
import overlays as OV  # noqa: E402
import video as VID  # noqa: E402
import finalizar as FIN  # noqa: E402

ENC = ["-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]


def _norm(entrada, saida, w: int = W, h: int = H):
    """Quadro w x h (padrão 1080x1920)/30 fps + áudio 48k estéreo -15 LUFS (para concatenar sem problema)."""
    af = ["-af", "loudnorm=I=-15:TP=-1.5:LRA=11"] if tem_audio(entrada) else []
    extra = [] if af else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest"]
    run(["ffmpeg", "-i", entrada, *extra, "-vf", vf_vertical(w, h), *af, *ENC, saida])
    return saida


def formato_da_receita(rec: dict) -> tuple[str, tuple[int, int], tuple[int, int]]:
    """(formato, (W, H) do quadro base de 1080 de largura, (w, h) da entrega conforme "resolucao")."""
    formato = rec.get("formato") or FORMATO_PADRAO
    return formato, dimensoes(formato, W), resolucao(rec.get("resolucao", "1080"), formato)


def camadas(rec: dict, wk: Path, estilo: str, total: float, pal: list, pal_leg: list,
            ins: list, fc: list, ult: str, idx: int):
    """Acrescenta em `ins`/`fc` as camadas da receita (legenda ASS, faixa SB, manchete, selo, setas de CTA),
    posicionadas no quadro BASE do formato (1080 de largura). Devolve (último rótulo, próximo índice, t_cta).
    Posições: chave absoluta em px do quadro base (ex.: "y") ou "<chave>_rel" (0–1 da altura); sem nenhuma,
    o padrão do formato (comum.layout_padrao; no 9:16 são os valores de sempre)."""
    formato, (Wb, Hb), _ = formato_da_receita(rec)
    L = layout_padrao(formato, estilo)
    preparar_fontsdir(wk)
    if pal_leg:
        lg = rec.get("legenda") or {}
        LEG.gera_ass(pal_leg, str(wk / "leg.ass"), estilo, set(lg.get("chaves", [])),
                     resolver_y(lg, "y", Hb, L["legenda_y"]), total, play_res=(Wb, Hb))
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
        fs = rec["faixa_sb"] if isinstance(rec.get("faixa_sb"), dict) else {}
        camada(OV.faixa_sb(str(wk / "faixa.png")), 0, resolver_y(fs, "y", Hb, L["faixa_y"]))
    if rec.get("manchete"):
        m = rec["manchete"]
        ate = m.get("ate")
        my = resolver_y(m, "y", Hb, L["manchete_y"])
        _avisa_fora("manchete", my, 0, Hb, formato)
        camada(OV.manchete(m["texto"], str(wk / "manchete.png"), m.get("px", 64)), 0,
               my, f"lt(t,{ate})" if ate else None)
    if rec.get("selo"):
        s = rec["selo"]
        esc = s.get("escala", L["selo_escala"])
        x_pad = L["selo_x"] if esc == L["selo_escala"] else int(round((Wb - 760 * esc) / 2))
        # escala trocada na receita: o padrão encolhe/sobe para o selo continuar dentro do quadro
        sy = resolver_y(s, "y", Hb, L["selo_y"] if esc == L["selo_escala"] else min(L["selo_y"], int(Hb - 360 * esc)))
        _avisa_fora("selo", sy, 360 * esc, Hb, formato)
        camada(OV.selo(s["linhas"], str(wk / "selo.png"), escala=esc), s.get("x", x_pad),
               sy, f"gte(t,{s['desde']})" if s.get("desde") else None)

    cta = rec.get("cta")
    t_cta = None
    if cta:
        if "inicio" in cta:
            t_cta = float(cta["inicio"])
        else:
            alvo = LEG._limpa(cta.get("palavra", "toca"))
            cand = [p for p in pal if LEG._limpa(p[0]).startswith(alvo) and p[1] >= total * 0.5]
            t_cta = cand[-1][1] if cand else max(0, total - 4)
            if not cand:
                print(f"aviso: palavra '{alvo}' não achada; setas nos últimos 4 s")
        esc = cta.get("escala", L["cta_escala"])
        seta = OV.seta(str(wk / "seta.png"), escala=esc)
        x_pad = L["cta_x"] if esc == L["cta_escala"] else [int(round(x + 97 - 97 * esc)) for x in (300, 610)]
        y = resolver_y(cta, "y", Hb, L["cta_y"] if esc == L["cta_escala"]     # seta 194 + oscilação 20 (x escala)
                       else min(L["cta_y"], int(Hb * 0.96 - 214 * esc)))
        _avisa_fora("cta", y - 20 * esc, 214 * esc + 20 * esc, Hb, formato)
        for x in cta.get("x", x_pad):
            ins.extend(["-i", seta])
            fc.append(f"{ult}[{idx}:v]overlay={x}:'{y}+{20 * esc:g}*sin(3*PI*t)'"
                      f":enable='gte(t,{t_cta:.2f})'[o{idx}]")
            ult = f"[o{idx}]"
            idx += 1
    return ult, idx, t_cta


def _avisa_fora(nome: str, y: float, altura: float, Hb: int, formato: str):
    """Avisa (não corta) quando a camada sai do quadro base — típico de y absoluto do 9:16 reaproveitado em 4:5/1:1."""
    if y < 0 or y + altura > Hb:
        print(f"aviso: {nome} em y={y:.0f}..{y + altura:.0f} sai do quadro 1080x{Hb} ({formato}); "
              f"use px desse quadro ou {nome}.y_rel")


def montar(rec: dict, base_dir: Path):
    P = lambda p: str((base_dir / p).resolve()) if p and not Path(p).is_absolute() else p  # noqa: E731
    wk = tmpdir("ad_")
    estilo = rec.get("estilo", "drop")
    saida = P(rec["saida"])
    _, (Wb, Hb), entrega = formato_da_receita(rec)

    # 1) corpo
    if rec.get("corpo"):
        corpo = _norm(P(rec["corpo"]), str(wk / "corpo.mp4"), Wb, Hb)
    else:
        corpo = VID.takes(P(rec["narracao"]), [P(t) for t in rec["takes"]], str(wk / "corpo.mp4"), w=Wb, h=Hb)
    if rec.get("cortar_pausas"):
        corpo = AUD.cortar_pausas(corpo, str(wk / "corpo_sp.mp4"))

    # 2) hook
    h = rec.get("hook") or {}
    deslocamento = 0.0
    if h.get("tipo", "imagem") == "imagem" and (h.get("video") or h.get("trechos")):
        hv = P(h["video"]) if h.get("video") else VID.montagem([(P(a), b, c) for a, b, c in h["trechos"]],
                                                                str(wk / "hook.mp4"), h.get("vel", 1.0), w=Wb, h=Hb)
        corpo = VID.hook(corpo, hv, str(wk / "com_hook.mp4"), h.get("ate"), w=Wb, h=Hb)
    elif h.get("tipo") == "antes":
        hk = _norm(P(h["video"]), str(wk / "hook_n.mp4"), Wb, Hb)
        deslocamento = dur(hk)
        corpo = VID.concat([hk, _norm(corpo, str(wk / "corpo_n.mp4"), Wb, Hb)], str(wk / "hook_corpo.mp4"))

    # 3) áudio com trilha
    if rec.get("trilha"):
        mixw = AUD.mix(corpo, P(rec["trilha"]), str(wk / "mix.wav"), dur(corpo))
        run(["ffmpeg", "-i", corpo, "-i", mixw, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "160k", wk / "com_trilha.mp4"])
        corpo = str(wk / "com_trilha.mp4")
    total = dur(corpo)

    # 4) palavras (legenda + tempo do CTA)
    lg = rec.get("legenda", {"fonte": "transcrever"})
    fonte = lg.get("fonte", "transcrever")
    pal = []
    if fonte == "transcrever":
        pal = LEG.palavras_por_whisper(corpo, lg.get("idioma", "es"), lg.get("modelo", "small"))
    elif fonte.startswith("alinhamento:"):
        pal = LEG.palavras_por_alinhamento(P(fonte.split(":", 1)[1]), deslocamento)
    elif fonte.startswith("texto:"):
        frases = [l.strip() for l in open(P(fonte.split(":", 1)[1]), encoding="utf-8") if l.strip()]
        pal = LEG.palavras_por_texto(frases, corpo)
    pal_leg = [p for p in pal if p[1] >= lg.get("desde", 0)]

    # 5) camadas (legenda, faixa, manchete, selo, setas) no quadro base do formato
    ins, fc = [], []
    ult, n, t_cta = camadas(rec, wk, estilo, total, pal, pal_leg, ins, fc, "[0:v]", 1)

    bruto = wk / "bruto.mp4"
    if fc:
        shutil.copy2(corpo, wk / "in.mp4")
        run(["ffmpeg", "-i", "in.mp4", *ins, "-filter_complex", ";".join(fc), "-map", ult, "-map", "0:a?",
             *ENC[:10], "-c:a", "copy", "bruto.mp4"], cwd=wk)
    else:
        shutil.copy2(corpo, bruto)

    # 6) entrega
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    FIN.encode(str(bruto), saida, rec.get("limite_mb", 30), tamanho=entrega)
    tempos = [1.0, total * 0.5] + ([t_cta + 0.5] if t_cta else []) + [-0.8]
    FIN.revisar(saida, str(Path(saida).with_suffix("")) + "_frames.jpg", tempos, entrega)
    print(f"CTA em {t_cta:.2f}s" if t_cta else "sem CTA")
    return saida


def main():
    args = [a for a in sys.argv[1:] if a != "--classico"]
    if len(args) != 1:
        print(__doc__)
        sys.exit(1)
    rec_path = Path(args[0]).resolve()
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    if "--classico" not in sys.argv:
        import montar_ad_rapido as RAP  # uma passada só (~0,6–0,7x a duração) quando a receita permite
        if RAP.elegivel(rec):
            return RAP.montar(rec, rec_path.parent)
    montar(rec, rec_path.parent)


if __name__ == "__main__":
    main()
