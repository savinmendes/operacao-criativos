# -*- coding: utf-8 -*-
"""CTA v2 (clean) do lote Lymphoria ES-CL: parte 1 intacta + fim novo com takes Lymphoria variados,
mesma voz (narração antiga encurtada, sem preço), legenda, selo pequeno amarelo e setas vermelhas.
  python build_cta.py V01 [V05 ...]      -> _cta_v2/VNN/out/<nome>.mp4 (não toca nos finais)"""
import json, subprocess, sys
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import legenda as LEG  # noqa: E402

AQUI = Path(__file__).parent
P = AQUI.parent
VID = Path(r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\VIDEOS")
FIN = Path(r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\LYMPHORIA-ES-CL")
A = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
U = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho\ugc\prod")

NARR = {  # mp3 + trechos mantidos (s) — cortes nas pausas entre frases
    "chilena": (P / "_fim_V14-V22-V25-V30" / "narr_fim.mp3", [(0, 5.92), (7.95, 10.356)]),
    "carolina": (P / "_fim" / "narr_fim.mp3", [(0, 1.29), (4.97, 9.47), (11.36, 14.071)]),
    "v09": (P / "V09" / "narr_fim.mp3", [(0, 1.63), (6.39, 8.15), (9.56, 11.64), (14.07, 16.904)]),
    "v12": (P / "V12" / "narr_fim.mp3", [(0, 5.745), (9.91, 12.027)], 0.25),
}
NOV = lambda n: str(VID / n)
CFG = {
    "V01": dict(nome="V01 - LYMPHORIA-TE-TRANSFORMA", p1=P / "V01/corte_up.mp4", narr="carolina",
                mus=(NOV("01 - Vitaly - 1215399127142396.mp4"), 9.63),
                takes=[U / "V1_gotero_hierbas.mp4", A / "ad14/flora/t3_edit.mp4", U / "P1_kit3.mp4"]),
    "V05": dict(nome="V05 - LYMPHORIA-POV-10MIL-PASOS", p1=P / "V05/rotulo.mp4", narr="carolina",
                mus=(NOV("05 - Vitaly - 2347337989106455.mp4"), 12.57),
                takes=[A / "ad19/flora/t1_edit.mp4", U / "V3_frasco_mesa.mp4", A / "ad11/flora/t3_edit.mp4"]),
    "V09": dict(nome="V09 - LYMPHORIA-TE-PASO-EL-DATO", p1=AQUI / "V09/parte1.mp4", narr="v09", mus=None,
                takes=[A / "ad16/flora/t2_edit.mp4", A / "ad14/flora2/t6_edit.mp4", A / "ad11/flora/t2_edit.mp4"]),
    "V12": dict(nome="V12 - LYMPHORIA-RUTINA-30-SEGUNDOS", p1=P / "V12/parte1_norm.mp4", narr="v12",
                mus=(str(next((P / "V12/sep").rglob("no_vocals.wav"))), 64.47),
                takes=[A / "ad19/flora/t3_edit.mp4", A / "ad11/flora/t4_edit.mp4", U / "P2_frasco_miel.mp4"]),
    "V14": dict(nome="V14 - LYMPHORIA-DEJAR-AZUCAR", p1=P / "V14/parte1_norm.mp4", narr="chilena",
                mus=(NOV("14 - Vitaly - 2081726192565218.mp4"), 10.37),
                takes=[A / "ad22/flora/t1_edit.mp4", U / "V2_frasco_cocina.mp4", U / "P1_kit3.mp4"]),
    "V19": dict(nome="V19 - LYMPHORIA-ANTES-DESPUES", p1=P / "V19/parte1_norm.mp4", narr="v12",
                mus=(NOV("19 - Vitaly - 881380110992207.mp4"), 19.33), suav=True,
                takes=[A / "ad13/flora/t5_edit.mp4", U / "V1_gotero_hierbas.mp4", A / "ad14/flora/t4_edit.mp4"]),
    "V22": dict(nome="V22 - LYMPHORIA-POV-DRENAR", p1=P / "V22/parte1_norm.mp4", narr="chilena",
                mus=(NOV("22 - Vitaly - 1512195570083814.mp4"), 15.37),
                takes=[A / "ad03/flora/t2_edit.mp4", A / "ad19/flora/t1_edit.mp4", A / "ad22/flora/t1_edit.mp4"]),
    "V25": dict(nome="V25 - LYMPHORIA-HINCHAZON-ENERGIA", p1=P / "V25/parte1_norm.mp4", narr="chilena",
                mus=(NOV("25 - Vitaly - 714399068325247.mp4"), 10.567),
                takes=[A / "ad13/flora/t4_edit.mp4", A / "ad14/flora/t3_edit.mp4", U / "P1_kit3.mp4"]),
    "V30": dict(nome="V30 - LYMPHORIA-ANTES-AHORA", p1=P / "V30/parte1_norm.mp4", narr="chilena",
                mus=(NOV("30 - Vitaly - 917426547905012.mp4"), 9.30),
                takes=[A / "ad14/flora/t2_edit.mp4", A / "ad19/flora/t3_edit.mp4", A / "ad03/flora/t2_edit.mp4"]),
}
EXTRA = AQUI / "cfg_extra.json"   # V10/V26 (entram quando o outro agente terminar)
if EXTRA.exists():
    for k, v in json.loads(EXTRA.read_text(encoding="utf-8")).items():
        v["p1"] = Path(v["p1"]); v["takes"] = [Path(t) for t in v["takes"]]
        if v.get("mus"): v["mus"] = tuple(v["mus"])
        if v.get("narr_custom"): NARR[k] = (Path(v["narr_custom"][0]), [tuple(s) for s in v["narr_custom"][1]], *v["narr_custom"][2:]); v["narr"] = k
        CFG[k] = v


def sh(*a): subprocess.run([str(x) for x in a], check=True)
def dur(f, s=None):
    cmd = ["ffprobe", "-v", "error"] + (["-select_streams", s] if s else []) + \
          ["-show_entries", "format=duration" if not s else "stream=duration", "-of", "csv=p=0", str(f)]
    return float(subprocess.run(cmd, capture_output=True, text=True).stdout.split()[0])


GAP = 0.06


def narracao(chave, wk):
    mp3, segs, *g = NARR[chave]
    GAP = g[0] if g else 0.06
    ali = json.load(open(str(mp3.with_suffix("")) + ".alinhamento.json", encoding="utf-8"))
    al = ali.get("alignment") or ali.get("normalized_alignment") or ali
    C, S, E = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    fc, labs, oc, os_, oe, off = [], [], [], [], [], 0.0
    for i, (a, b) in enumerate(segs):
        d = b - a
        fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.01,"
                  f"afade=t=out:st={d - 0.012:.3f}:d=0.012,apad=pad_dur={GAP}[s{i}]")
        labs.append(f"[s{i}]")
        if oc and oc[-1] != " ":
            oc.append(" "); os_.append(off - GAP / 2); oe.append(off - GAP / 2)
        for c, s, e in zip(C, S, E):
            if a - 1e-3 <= s < b:
                oc.append(c); os_.append(s - a + off); oe.append(min(e, b) - a + off)
        off += d + GAP
    fc.append("".join(labs) + f"concat=n={len(segs)}:v=0:a=1[o]")
    out = wk / "narr.wav"
    sh("ffmpeg", "-v", "error", "-y", "-i", mp3, "-filter_complex", ";".join(fc), "-map", "[o]", "-ac", "1", out)
    alj = wk / "narr.alinhamento.json"
    alj.write_text(json.dumps({"characters": oc, "character_start_times_seconds": os_,
                               "character_end_times_seconds": oe}, ensure_ascii=False), encoding="utf-8")
    return out, alj


def corpo_fim(cfg, narr, wk):
    D = dur(narr) + 0.7
    n = len(cfg["takes"]); seg = D / n
    ins, fc = [], []
    for k, t in enumerate(cfg["takes"]):
        dt = dur(t)
        if dt >= seg + 0.1:
            st = (dt - seg) / 2; f = f"trim={st:.3f}:{st + seg:.3f},setpts=PTS-STARTPTS"
        else:
            fat = min(seg / (dt - 0.05), 1.35)
            f = f"setpts={fat:.4f}*(PTS-STARTPTS),tpad=stop_mode=clone:stop_duration={seg:.3f},trim=0:{seg:.3f},setpts=PTS-STARTPTS"
        ins += ["-i", t]
        fc.append(f"[{k}:v]{f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p[v{k}]")
    fc.append("".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0[v]")
    na = n
    ins += ["-i", narr]
    fc.append(f"[{na}:a]aresample=48000,loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={D:.3f}[voz]")
    if cfg.get("mus"):
        src, t0 = cfg["mus"]
        mw = wk / "mus.wav"
        sh("ffmpeg", "-v", "error", "-y", "-stream_loop", "4", "-i", src, "-vn", "-ss", f"{t0:.3f}", "-t", f"{D + 1:.3f}",
           "-ar", "48000", "-ac", "2", mw)
        ins += ["-i", mw]
        fc.append(f"[{na + 1}:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                  f"loudnorm=I=-32:TP=-9:LRA=11,aresample=48000,afade=t=in:d=0.3,afade=t=out:st={D - 0.5:.3f}:d=0.5[mus]")
        fc.append("[voz][mus]amix=inputs=2:duration=first:normalize=0,atrim=0:%.3f[a]" % D)
    else:
        fc.append("[voz]atrim=0:%.3f[a]" % D)
    out = wk / "corpo_fim.mp4"
    sh("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{D:.3f}",
       "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", out)
    return out


def montar(v):
    cfg = CFG[v]
    wk = AQUI / v; wk.mkdir(exist_ok=True); (wk / "out").mkdir(exist_ok=True)
    narr, alj = narracao(cfg["narr"], wk)
    corpo = corpo_fim(cfg, narr, wk)
    d1 = dur(cfg["p1"], "v:0")
    pal = LEG.palavras_por_alinhamento(str(alj), 0)
    tp = next(a for w, a, *_ in pal if LEG._limpa(w).startswith("pagas"))
    saida = wk / "out" / (cfg["nome"] + ".mp4")
    rec = {"saida": str(saida), "estilo": "drop", "corpo": str(corpo),
           "hook": {"tipo": "antes", "video": str(cfg["p1"])},
           "legenda": {"fonte": f"alinhamento:{alj}", "chaves": ["lymphoria", "compre", "dos", "gratis", "recibir"]},
           "selo": {"linhas": ["", "PAGO CONTRA", "ENTREGA", ""], "escala": 0.55, "x": 331, "y": 1330,
                    "desde": round(d1 + tp, 2)},
           "cta": {"palavra": cfg.get("cta", "toca")}, "limite_mb": 30, "resolucao": "720"}
    (wk / "receita_cta2.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    sh(sys.executable, KIT / "ferramentas" / "montar_ad.py", wk / "receita_cta2.json")
    json.dump({"corte": d1, "fim_dur": dur(corpo), "takes": [str(t) for t in cfg["takes"]], "narr": cfg["narr"]},
              open(wk / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("OK", v, saida)


if __name__ == "__main__":
    for v in sys.argv[1:]:
        montar(v)
