# -*- coding: utf-8 -*-
"""C2 (Drama "¿estás embarazada?") do lote enxuto Lymphoria CL.
  A = gancho novo (voz clonada da narradora do AD 30) + corpo AD 30 CURTO (de "Verás..." até "Solo puedes drenarlos")
  B = gancho novo (voz clonada do narrador do AD 23) + corpo AD 23 (de "Cuando Gloria me dejó" até "...para siempre")
  Fim CTA v2 (ESTUDO-CTA.md): takes Lymphoria em movimento, legenda, selo pequeno "PAGO CONTRA ENTREGA", setas no "Toca".
  python build.py A|B [etapa: gancho|fim|tudo]"""
import json, subprocess, sys
from pathlib import Path

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import legenda as LEG  # noqa: E402

AQ = Path(__file__).parent
DL = Path(r"C:\Users\PICHAU\Downloads")
D3 = DL / "DRENAGEM-LATAM" / "producao"
U = D3 / "_trabalho" / "ugc" / "prod"
L = DL / "LHYMPORIA AD 01-20" / "lymphoria" / "_trabalho"
AD23 = DL / "APROVADOS E VALIDADOS TIKTOK" / "AD 23 - LYMPHORIA-SUPERMERCADO-ES-LATAM.mp4"
CURTO = D3 / "_trabalho" / "ad30" / "curto_p1c.mp4"          # AD 30 CURTO sem o fim antigo (0-57,67 s)
SAIDA = DL / "ADLIB-VITALY-CL" / "LYMPHORIA-ENXUTO"

CFG = {
    "A": dict(
        nome="LYM-CL_C2_drama-embarazada-suegra_gancho-x-ad30_a",
        voz="x7Q3zqDG9jz6G8aiQCio",
        fonte_hook=D3 / "AD 03 - LYMPHORIA-MEJOR-AMIGA-ES-LATAM.mp4",
        # tomadas escolhidas à mão (folhas de contato), já com margem de 0,15/0,20 s do gerar_variacao
        tomadas=[(11.95, 14.35), (129.6, 132.4), (159.85, 162.7), (171.9, 175.0), (37.0, 40.5), (196.9, 201.75)],
        caixas={"cy": 950, "min_w": 570, "min_h": 120, "px": 44},
        bed=AQ / "fontes/30c/bed.wav",
        corpo=CURTO, corte=29.0,
        narr=(D3 / "_trabalho/ad30/curto/narr_fim.mp3", [(0, 4.90), (9.70, 15.35), (20.35, 23.359)]),
        mus=(CURTO, 29.0, 57.6),
        takes=[L / "ad11/flora/t4_edit.mp4", U / "V1_gotero_hierbas.mp4", U / "V2_frasco_cocina.mp4", U / "P1_kit3.mp4"],
        chaves=["lymphoria", "hierbas", "gratis", "recibir"]),
    "B": dict(
        nome="LYM-CL_C2_drama-de-cuantos-meses-cunado_gancho-x-ad23_b",
        voz="Su8gBKRqNV3hbcg6U1g6",
        fonte_hook=D3 / "AD 24 - LYMPHORIA-HOMBRE-40-ES-LATAM.mp4",
        tomadas=[(90.6, 93.85), (77.5, 80.35), (80.4, 82.75), (87.35, 90.45), (60.8, 63.75), (51.75, 55.5)],
        caixas={"cy": 975, "min_w": 600, "min_h": 130, "px": 44},
        bed=AQ / "fontes/23/bed.wav",
        corpo=None, corte=69.42, fim_corpo=398.06,
        narr=(AQ / "voz/B_fim.mp3", None),
        mus=(AD23, 398.3, 445.0),
        takes=[L / "ad10/flora/t1_edit.mp4", U / "V3_frasco_mesa.mp4", L / "ad03/flora/t2_edit.mp4", L / "ad11/flora/t2_edit.mp4", L / "ad13/flora/t5_edit.mp4", U / "P2_frasco_miel.mp4"],
        chaves=["lymphoria", "miel", "gratis", "recibir"]),
}


def sh(*a, **k): subprocess.run([str(x) for x in a], check=True, **k)
def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout.split()[0])


ENV = dict(__import__("os").environ, PYTHONIOENCODING="utf-8")


def gancho(k, c, wk):
    """Gancho + corpo pelo gerar_variacao.py (modo A) com banco de tomadas escolhidas."""
    banco = {"video": str(c["fonte_hook"]), "tomadas": [
        {"ini": a, "fim": b, "dur": round(b - a, 3), "grupo": i} for i, (a, b) in enumerate(c["tomadas"])]}
    (wk / "banco_hook.json").write_text(json.dumps(banco, ensure_ascii=False, indent=1), encoding="utf-8")
    corpo = c["corpo"]
    if corpo is None:      # AD 23 cortado antes de "así que volvamos a Walmart" (o fim novo entra depois)
        corpo = wk / "corpo_fonte.mp4"
        if not corpo.exists():
            sh("ffmpeg", "-v", "error", "-y", "-i", AD23, "-t", f"{c['fim_corpo']:.3f}", "-vf", "scale=720:1280:flags=lanczos,fps=30",
               "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
               "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
               "-c:a", "aac", "-b:a", "192k", "-ar", "48000", corpo)
    cfg = {"saida": str(wk / "p1_final.mp4"), "trab": str(wk / "var"), "resolucao": "720", "limite_mb": 60, "semente": 7,
           "bancos": {"h": str(wk / "banco_hook.json")},
           "gancho": {"fala": str(AQ / f"voz/{k}_gancho.mp3"), "lead": 0.12, "cauda": 0.30,
                      "pool": [["h", a - 0.01, b + 0.01] for a, b in c["tomadas"]],
                      "tomada": [3.5, 3.5], "caixas": c["caixas"], "fundo": str(c["bed"]), "fundo_vol": 1.0},
           "corpo": {"video": str(corpo), "corte": c["corte"], "ganho_db": None}}
    (wk / "var.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    sh(sys.executable, KIT / "ferramentas/gerar_variacao.py", "montar", wk / "var.json", env=ENV)


def narracao(c, wk):
    mp3, segs = c["narr"]
    ali = json.load(open(str(Path(mp3).with_suffix("")) + ".alinhamento.json", encoding="utf-8"))
    al = ali.get("alignment") or ali.get("normalized_alignment") or ali
    C, S, E = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    if segs is None:
        segs = [(0, dur(mp3))]
    GAP = 0.06
    fc, labs, oc, os_, oe, off = [], [], [], [], [], 0.0
    for i, (a, b) in enumerate(segs):
        d = b - a
        fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.01,"
                  f"afade=t=out:st={d - 0.012:.3f}:d=0.012,apad=pad_dur={GAP}[s{i}]")
        labs.append(f"[s{i}]")
        if oc and oc[-1] != " ":
            oc.append(" "); os_.append(off - GAP / 2); oe.append(off - GAP / 2)
        for ch, s, e in zip(C, S, E):
            if a - 1e-3 <= s < b:
                oc.append(ch); os_.append(s - a + off); oe.append(min(e, b) - a + off)
        off += d + GAP
    fc.append("".join(labs) + f"concat=n={len(segs)}:v=0:a=1[o]")
    out = wk / "narr.wav"
    sh("ffmpeg", "-v", "error", "-y", "-i", mp3, "-filter_complex", ";".join(fc), "-map", "[o]", "-ac", "1", out)
    alj = wk / "narr.alinhamento.json"
    alj.write_text(json.dumps({"characters": oc, "character_start_times_seconds": os_,
                               "character_end_times_seconds": oe}, ensure_ascii=False), encoding="utf-8")
    return out, alj


def musica(c, wk):
    """Música sem voz que continua a do corpo (demucs local)."""
    src, de, ate = c["mus"]
    w = wk / "mus_src.wav"
    if not w.exists():
        sh(sys.executable, KIT / "ferramentas/gerar_variacao.py", "fundo", src, "--de", str(de), "--ate", str(ate - de),
           "--saida", w, env=ENV)
    return w


def corpo_fim(c, narr, mus, wk):
    D = dur(narr) + 0.7
    ds = [dur(t) - 0.05 for t in c["takes"]]
    fat = D / sum(ds)                              # duração de cada take proporcional à dele
    ins, fc = [], []
    for k, (t, dt) in enumerate(zip(c["takes"], ds)):
        seg = dt * fat
        if fat <= 1:
            st = (dt - seg) / 2; f = f"trim={st:.3f}:{st + seg:.3f},setpts=PTS-STARTPTS"
        else:
            f = (f"setpts={min(fat, 1.35):.4f}*(PTS-STARTPTS),tpad=stop_mode=clone:stop_duration={seg:.3f},"
                 f"trim=0:{seg:.3f},setpts=PTS-STARTPTS")
        ins += ["-i", t]
        fc.append(f"[{k}:v]{f},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p[v{k}]")
    n = len(c["takes"])
    fc.append("".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0[v]")
    ins += ["-i", narr, "-stream_loop", "3", "-i", mus]
    fc.append(f"[{n}:a]aresample=48000,loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,aformat=channel_layouts=stereo,"
              f"apad=whole_dur={D:.3f}[voz]")
    fc.append(f"[{n + 1}:a]atrim=0:{D + 0.5:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
              f"loudnorm=I=-32:TP=-9:LRA=11,aresample=48000,afade=t=in:d=0.3,afade=t=out:st={D - 0.5:.3f}:d=0.5[mus]")
    fc.append(f"[voz][mus]amix=inputs=2:duration=first:normalize=0,atrim=0:{D:.3f}[a]")
    out = wk / "corpo_fim.mp4"
    sh("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{D:.3f}",
       "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", out)
    return out


def fim(k, c, wk):
    p1 = wk / "var" / "bruto.mp4"
    narr, alj = narracao(c, wk)
    corpo = corpo_fim(c, narr, musica(c, wk), wk)
    d1 = dur(p1)
    pal = LEG.palavras_por_alinhamento(str(alj), 0)
    tp = next(a for w, a, *_ in pal if LEG._limpa(w).startswith("pagas"))
    SAIDA.mkdir(parents=True, exist_ok=True)
    rec = {"saida": str(SAIDA / (c["nome"] + ".mp4")), "estilo": "drop", "corpo": str(corpo),
           "hook": {"tipo": "antes", "video": str(p1)},
           "legenda": {"fonte": f"alinhamento:{alj}", "chaves": c["chaves"]},
           "selo": {"linhas": ["", "PAGO CONTRA", "ENTREGA", ""], "escala": 0.55, "x": 331, "y": 1330,
                    "desde": round(d1 + tp, 2)},
           "cta": {"palavra": "toca"}, "limite_mb": 30, "resolucao": "720"}
    (wk / "receita.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    sh(sys.executable, KIT / "ferramentas/montar_ad.py", wk / "receita.json", env=ENV)
    json.dump({"p1": str(p1), "p1_dur": d1, "fim_dur": dur(corpo)}, open(wk / "info.json", "w"), indent=1)


if __name__ == "__main__":
    k = sys.argv[1]; et = sys.argv[2] if len(sys.argv) > 2 else "tudo"
    wk = AQ / k; wk.mkdir(exist_ok=True)
    if et in ("gancho", "tudo"):
        gancho(k, CFG[k], wk)
    if et in ("fim", "tudo"):
        fim(k, CFG[k], wk)
