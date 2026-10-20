# -*- coding: utf-8 -*-
"""Gera as receitas (cfg/*.json) dos 14 videos DCD7781 a partir de roteiros/roteiros.json e prepara os audios das traducoes.
  python gerar_configs.py            -> cfg/TR21.json ... cfg/G5_C2.json + _audio/
Depois: python rodar_lote.py (montar.py + mixar_cama.py)."""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

D = Path(r"C:\Users\PICHAU\Downloads\DEWALT-ADS")
ED = D / "edicao"
CFG = ED / "cfg"
AUD = ED / "_audio"
BANCO = D / "banco"
VOZ = D / "voz"
ENT = D / "entregas"
OV = ED / "ov"
R = json.load(open(D / "roteiros" / "roteiros.json", encoding="utf-8"))
SR = 48000
CTA_DUR = 3.3          # cartao final (s)
CAUDA = 0.8            # depois da ultima palavra
FUNDO_REL = -16.0      # fundo demucs (versao fundo-original) = voz - 16 LU

from gerar_overlays import slug  # noqa: E402

CHAVES = ["dewalt", "percutor", "atornillador", "maleta", "cargador", "carbones", "brushless", "led", "recién",
          "chile", "bueno", "bonito", "barato", "débil", "incluido", "maestro", "madera", "metal", "muro", "modo",
          "taladro", "versatilidad", "potencia", "fuerza", "liviano", "kit"]
JUNTAR = [["Pre", "Black", "Friday"], ["dos", "baterías"], ["sin", "carbones"], ["luz", "LED"], ["quince", "posiciones"],
          ["ajuste", "rápido"], ["dos", "velocidades"], ["indicador", "de", "carga"], ["todo", "Chile"],
          ["pagas", "recién"], ["pega", "pesada"], ["taladro", "débil"], ["todo", "incluido"], ["un", "solo", "kit"],
          ["sin", "cables"], ["en", "segundos"], ["harto", "tiempo"], ["bien", "apretado"], ["la", "obra"]]


def voz_de(iid):
    """voz com realce das palavras finais baixas (fix_voz.py), se existir; senao a original"""
    nv = AUD / f"{iid}_nv.wav"
    return nv if nv.exists() else VOZ / f"{iid}.mp3"


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                          str(p)]).decode().strip())


def dec(p, n=None):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)
    if n is not None:
        x = np.pad(x, ((0, max(0, n - len(x))), (0, 0)))[:n]
    return x


def base_cfg(saida, titulo, cta_dur, legenda_y=1060):
    return {"saida": str(saida), "overlays": str(OV), "sfx": str(ED / "sfx"), "titulo": titulo,
            "cta": {"png": "cta_final.png", "dur": round(cta_dur, 3)}, "banner": True, "sticker": True,
            "selo": {"em": "sempre", "png": "selo_bf.png", "x": "W-w-10", "y": 10}, "whoosh": True, "pop": True,
            "legenda": {"modo": "roteiro", "textos": {}, "y": legenda_y, "chaves": CHAVES, "juntar": JUNTAR},
            "loudnorm": -15, "limite_mb": 30, "segmentos": [], "extras": []}


# ------------------------------------------------------------------ traducoes
COBRE37 = [("cobre37_madera.png", 51.78, 55.30), ("cobre37_metal.png", 55.30, 58.27), ("cobre37_muro.png", 58.27, 60.47)]


def traducao(t):
    n = t["id"].split("_")[1]
    base = Path(t["base"])
    segs = t["segmentos"]
    fala_fim = t["fala_fim"]
    total = round((fala_fim + CAUDA) * 30) / 30
    cta_ini = segs[-1]["ini"]
    cta_dur = min(CTA_DUR, total - (cta_ini + 1.5))
    # audios: voz (so a voz) e voz + fundo demucs
    AUD.mkdir(exist_ok=True)
    N = int(round(total * SR))
    voz = dec(voz_de(t["id"]), N)
    fundo = dec(D / "base_limpa" / "audio" / f"{n}_no_vocals.wav")
    nb = min(len(fundo), N)
    f2 = np.zeros((N, 2)); f2[:nb] = fundo[:nb]
    fo = int(0.8 * SR)
    f2[max(0, nb - fo):nb] *= np.linspace(1, 0, nb - max(0, nb - fo))[:, None]   # fundo acaba com fade (quadro congelado)
    m = pyln.Meter(SR)
    lv, lf = m.integrated_loudness(voz), m.integrated_loudness(f2[:nb])
    f2 *= 10 ** ((lv + FUNDO_REL - lf) / 20)
    out = {}
    for tag, x in (("voz", voz), ("fundo", voz + f2)):
        w = AUD / f"{t['id']}_{tag}.wav"
        sf.write(w, x.astype(np.float32), SR, subtype="FLOAT")
        shutil.copy(VOZ / f"{t['id']}.alinhamento.json", w.with_suffix(".alinhamento.json"))
        out[tag] = w
    cfgs = {}
    for tag in ("voz", "fundo"):
        c = base_cfg(ED / "_montado" / f"TR{n}_{tag}.mp4", None, cta_dur)
        c["sticker"] = False
        c["whoosh"] = False
        c["segmentos"] = [{"video": str(base), "tipo": "outro", "zoom": 1.0, "snap": False, "audio": str(out[tag]),
                           "dur": total, **({"video_ate": 71.4} if n == "37" else {})}]   # 37: preto a partir de 71,47 s
        for i, s in enumerate(segs):
            tt = s.get("titulo_tela")
            if not tt:
                continue
            if n == "37" and tt in ("MADERA", "METAL", "MURO Y CONCRETO (MODO PERCUTOR)"):
                continue
            fim = segs[i + 1]["ini"] if i + 1 < len(segs) else total
            png = OV / f"tt_{slug(tt)}.png"
            assert png.exists(), png
            c["extras"].append({"png": str(png), "de": s["ini"], "ate": fim})
        if n == "37":
            c["extras"] += [{"png": str(OV / p), "de": a, "ate": b} for p, a, b in COBRE37]
        cfgs[tag] = c
    return f"TR{n}", cfgs, {"total": total, "cta": cta_dur}


# ------------------------------------------------------------------ ganchos x corpos
# janela util de cada take: sem os 2 primeiros e os 2 ultimos quadros (o 1o quadro de varios takes e da cena anterior)
# e, quando ha salto de camera no fim (scdet), ate antes dele
CAP = {"kit_completo_02": 1.7, "maleta_02": 1.95, "anel_04": 2.7, "anel_03": 2.5, "mandril_01": 2.15, "bateria_01": 2.55,
       "anel_05": 1.65, "motor_02": 1.33, "maleta_01": 0.88}
DE0 = 2 / 30
TAKE_FIM = {p.stem: min(dur(p) - DE0, CAP.get(p.stem, 99)) for p in BANCO.glob("*.mp4")}
TAKE_DUR = {k: v - DE0 for k, v in TAKE_FIM.items()}
GANCHO_TAKES = {   # (take, vel)
    "gancho_1_3b": [("led_01", 1.0)],
    "gancho_2_debil": [("furando_concreto_01", 1.0)],
    "gancho_3_pega": [("furando_madeira_01", 0.55)],
    "gancho_4_bf": [("maleta_01", 1.0), ("kit_completo_03", 0.8)],
    "gancho_5_kit": [("kit_completo_08", 0.86)],
}
# trocas de take no corpo para nao repetir o take/plano do gancho: {(g, corpo): {indice_frase: [takes]}}
TROCAS = {
    ("g1", "corpo_1"): {11: ["led_02"]},
    ("g2", "corpo_1"): {8: ["anel_04"]},
    ("g3", "corpo_1"): {7: ["furando_madeira_02"]},
    ("g4", "corpo_1"): {1: ["maleta_02", "maleta_04"]},
}
TITULO_FRASE_CORPO = {"HASTA 1.750 RPM": "tt_hasta-1-750-rpm.png", "17% MÁS EFICIENTE*": "tt_17-mas-eficiente.png",
                      "PRE BLACK FRIDAY · PAGAS AL RECIBIR": "tt_pre-black-friday-pagas-al-recibir.png"}


def fala_fim_el(p):
    a = json.load(open(p, encoding="utf-8"))
    return max(e for c, e in zip(a["characters"], a["character_end_times_seconds"]) if c.strip())


def combinacao(gi, g, corpo):
    gid = f"g{gi}"
    cid = corpo["id"]
    nome = f"G{gi}_C{cid[-1]}"
    c = None
    gaudio = voz_de(g["id"])
    gd = round((fala_fim_el(g["alinhamento"]) + 0.2) * 30) / 30
    segs = []
    # gancho
    takes = GANCHO_TAKES[g["id"]]
    disp = [TAKE_DUR[t] / v for t, v in takes]
    a0 = 0.0
    for k, ((t, v), dd) in enumerate(zip(takes, disp)):
        d = gd - a0 if k == len(takes) - 1 else min(dd, gd * dd / sum(disp))
        d = round(d * 30) / 30
        segs.append({"video": str(BANCO / f"{t}.mp4"), "tipo": "broll", "zoom": 1.0, "snap": False, "vel": v, "de": round(DE0, 4), "video_ate": round(TAKE_FIM[t], 4),
                     "audio": str(gaudio), "audio_de": round(a0, 4), "audio_ate": round(a0 + d, 4), "sticker": False,
                     "whoosh": k == 0})
        a0 += d
    t_gancho = a0
    # corpo
    cs = corpo["segmentos"]
    fala_fim = corpo["fala_fim"]
    fim_corpo = round((fala_fim + CAUDA) * 30) / 30
    trocas = TROCAS.get((gid, cid), {})
    extras = []
    pos = t_gancho
    for i, s in enumerate(cs):
        ini = 0.0 if i == 0 else s["ini"] - 0.1          # corte no silencio antes da 1a palavra
        fim = cs[i + 1]["ini"] - 0.1 if i + 1 < len(cs) else fim_corpo
        L = fim - ini
        takes = [x.replace(".mp4", "") for x in s["takes"]]
        takes = trocas.get(i, takes)
        if cid == "corpo_1" and i == 2:   # kit_completo_05 tem saltos de camera (scdet): trocado por taladro_01
            takes = ["kit_completo_09", "taladro_01"]
        tot = sum(TAKE_DUR[t] for t in takes)
        vel = 1.0 if tot >= L else max(0.7, tot / L)
        ds = [TAKE_DUR[t] / vel for t in takes]
        a = ini
        for k, (t, dd) in enumerate(zip(takes, ds)):
            if k == len(takes) - 1:
                d = fim - a
            else:
                d = min(dd, L * dd / sum(ds))
            d = round(d * 30) / 30
            segs.append({"video": str(BANCO / f"{t}.mp4"), "tipo": "broll", "zoom": 1.0, "snap": False,
                         "vel": round(vel, 3), "de": round(DE0, 4), "video_ate": round(TAKE_FIM[t], 4),
                         "audio": str(voz_de(cid)), "audio_de": round(a, 4),
                         "audio_ate": round(a + d, 4), "sticker": i == len(cs) - 1, "whoosh": k == 0})
            a += d
        tt = s.get("titulo_tela")
        if tt:
            extras.append({"png": str(OV / TITULO_FRASE_CORPO[tt]), "de": round(pos, 3), "ate": round(pos + L, 3)})
        pos += L
    total = pos
    cta_ini = t_gancho + cs[-1]["ini"]
    cta_dur = min(CTA_DUR, total - (cta_ini + 1.5))
    titulo = {"png": f"tit_{gid}.png", "dur": round(t_gancho, 3), "com_legenda": True}
    cfgs = {}
    for tag in ("voz",):
        c = base_cfg(ED / "_montado" / f"{nome}_{tag}.mp4", titulo, cta_dur)
        c["segmentos"] = segs
        c["extras"] = extras
        cfgs[tag] = c
    return nome, cfgs, {"total": round(total, 3), "cta": cta_dur, "tit": round(t_gancho, 3)}


if __name__ == "__main__":
    CFG.mkdir(exist_ok=True)
    (ED / "_montado").mkdir(exist_ok=True)
    plano = {}
    for t in R["traducoes"]:
        nome, cfgs, info = traducao(t)
        for tag, c in cfgs.items():
            json.dump(c, open(CFG / f"{nome}_{tag}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        plano[nome] = info
    for gi, g in enumerate(R["ganchos"], 1):
        for corpo in R["corpos"]:
            nome, cfgs, info = combinacao(gi, g, corpo)
            for tag, c in cfgs.items():
                json.dump(c, open(CFG / f"{nome}_{tag}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            plano[nome] = info
    json.dump(plano, open(CFG / "_plano.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(plano, indent=0))
