# -*- coding: utf-8 -*-
"""Pacote ENXUTO DCD7781: gera overlays novos e as receitas (cfg_enx/*.json) das 6 execucoes.
Copia de trabalho (enxuto/edicao) - nao toca em DEWALT-ADS/edicao nem entregas.
  python gerar_enx.py            -> ov/ (titulos novos) + cfg_enx/<nome>.json + cfg_enx/_plano.json
Depois: python rodar_enx.py"""
import json
import subprocess
from pathlib import Path

from PIL import Image

import gerar_overlays as GO

D = Path(r"C:\Users\PICHAU\Downloads\DEWALT-ADS")
ENX = D / "enxuto"
ED = ENX / "edicao"
CFG = ED / "cfg_enx"
AUD = ED / "_audio"
OV = ED / "ov"
BANCO = D / "banco"
PECAS = ENX / "pecas"
VOZ = ENX / "voz"
R = json.load(open(D / "roteiros" / "roteiros.json", encoding="utf-8"))
REL = json.load(open(VOZ / "_trabalho" / "relatorio_voz.json", encoding="utf-8"))
CTA_DUR, CAUDA = 3.3, 0.8
GO.OUT = OV   # garante que os overlays novos saem na copia

CHAVES = ["dewalt", "percutor", "atornillador", "maleta", "cargador", "carbones", "brushless", "led", "recién",
          "chile", "maestro", "maestros", "madera", "metal", "muro", "taladro", "liviano", "kit", "martillo", "concreto",
          "torque", "tornillo", "gatillo", "eficiencia", "justo", "perforar", "atornillar", "problema", "baterías"]
JUNTAR = [["Pre", "Black", "Friday"], ["dos", "baterías"], ["sin", "carbones"], ["luz", "LED"], ["quince", "posiciones"],
          ["ajuste", "rápido"], ["dos", "velocidades"], ["indicador", "de", "carga"], ["todo", "Chile"],
          ["pagas", "recién"], ["pega", "pesada"], ["un", "solo", "kit"], ["velocidad", "variable"],
          ["broca", "de", "concreto"], ["rincones", "oscuros"], ["amperes", "hora"], ["no", "se", "para"],
          ["menos", "mantención"], ["sin", "pelear"], ["veinte", "volts"], ["la", "pega"]]

# ---------------------------------------------------------------- corpos novos (takes por frase + titulo de frase)
CORPOS = {
    "corpo_c2": {
        "audio": VOZ / "corpo_c2.mp3",
        "takes": [["led_01"], ["anel_06", "anel_02"], ["furando_concreto_01"], ["furando_madeira_02", "furando_madeira_01"],
                  ["lateral_brushless_01", "motor_02"], ["bateria_02", "bateria_03", "kit_completo_03"], ["kit_completo_06", "maleta_04"],
                  ["kit_completo_02", "kit_completo_04"]],
        "titulos": {1: "MODO PERCUTOR", 3: "MADERA Y METAL", 5: "2 BATERÍAS 2Ah + CARGADOR + MALETA",
                    7: "PRE BLACK FRIDAY · PAGAS AL RECIBIR"},
    },
    "corpo_c7": {
        "audio": VOZ / "corpo_c7.mp3",
        "takes": [["anel_01"], ["parafusando_madeira_01"], ["seletor_velocidade_01", "furando_madeira_02"], ["gatilho_01", "gatilho_02"],
                  ["motor_01", "lateral_brushless_01"], ["led_04"], ["bateria_04", "kit_completo_05"],
                  ["kit_completo_02", "kit_completo_04"]],
        "titulos": {0: "15 POSICIONES DE TORQUE", 2: "HASTA 1.750 RPM", 4: "MOTOR SIN CARBONES",
                    7: "PRE BLACK FRIDAY · PAGAS AL RECIBIR"},
    },
}


def corpo_pega():
    """corpo 'pega pesada' do outro workflow (roteiros.json corpo_2 + voz com realce _nv copiada)"""
    c = [x for x in R["corpos"] if x["id"] == "corpo_2"][0]
    tit = {i: s["titulo_tela"] for i, s in enumerate(c["segmentos"]) if s.get("titulo_tela")}
    return {"audio": AUD / "corpo_2_nv.wav", "takes": [[t.replace(".mp4", "") for t in s["takes"]] for s in c["segmentos"]],
            "titulos": tit, "segs": [(s["ini"], s["fim"]) for s in c["segmentos"]], "fala_fim": c["fala_fim"]}


def info_corpo(cid):
    if cid == "corpo_2":
        return corpo_pega()
    c = dict(CORPOS[cid])
    nv = AUD / f"{cid}_nv.wav"
    if nv.exists():
        c["audio"] = nv
    r = REL[cid]
    c["segs"] = [(s["inicio"], s["fim"]) for s in r["segmentos"]]
    c["fala_fim"] = r["fala_fim"]
    return c


# ---------------------------------------------------------------- ganchos
TXT_GANCHO = {   # legenda modo roteiro (alinhamento CTC sobre o audio do proprio gancho)
    "G_C1_obra": "Maestro, con dos baterías la pega no se para.",
    "G_C2_casa": "¿Tu taladro no le entra al muro? El problema no eres tú.",
    "G_C1_ferrevolt": "Maestros: dos baterías, una trabajando y la otra cargando. Así no se para la pega.",
    "G_C7_ferrevolt": "Maestros, si se les pasa el tornillo, es porque no tienen esto.",
}
DUR_GANCHO = {"G_C1_obra": 6.0, "G_C2_casa": 5.9, "G_C1_ferrevolt": 4.9, "G_C7_ferrevolt": 3.4}
LEG_Y_ROSTO = 1480
# AUDITORIA 10/10: a fala do gancho IA comecava tarde (obra 3,3 s; casa 1,4 s) -> corta o inicio parado
GANCHO_DE = {"G_C1_obra": 2.6, "G_C2_casa": 0.9}   # legenda mais baixa nos ganchos com rosto (nao cobre a boca)

EXECUCOES = {
    "C2_casaIA": {"gancho": ("peca", "G_C2_casa"), "corpo": "corpo_c2"},
    "C2_muroReal": {"gancho": ("real", "gancho_muro", [("furando_concreto_01", 1.0)], "tit_muro.png"), "corpo": "corpo_c2",
                    "trocas": {2: ["anel_04"]}},   # nao repetir furando_concreto_01 (ja abre o video)
    "C7_ferrevolt": {"gancho": ("peca", "G_C7_ferrevolt"), "corpo": "corpo_c7"},
    "C7_anelReal": {"gancho": ("real", "gancho_anel", [("anel_03", None)], "tit_anel.png"), "corpo": "corpo_c7",
                    "sem_titulo": [0]},           # o titulo do gancho ja e '15 POSICIONES DE TORQUE'
    "C1_obraIA": {"gancho": ("peca", "G_C1_obra"), "corpo": "corpo_2"},
    "C1_ferrevolt": {"gancho": ("peca", "G_C1_ferrevolt"), "corpo": "corpo_2"},
}


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                          str(p)]).decode().strip())


TAKE_DUR = {p.stem: dur(p) for p in BANCO.glob("*.mp4")}
# fim com flash/transicao do AD original (medido quadro a quadro): usar so ate antes dele
CORTE_FIM = ({"anel_04": 81 / 30, "bateria_02": 81 / 30, "motor_02": 40 / 30})
TAKE_DUR.update(CORTE_FIM)   # AUDITORIA 10/10: com vel<1 o flash ainda entrava -> video_ate no segmento


def fala_fim_el(p):
    a = json.load(open(p, encoding="utf-8"))
    return max(e for c, e in zip(a["characters"], a["character_end_times_seconds"]) if c.strip())


def overlays():
    OV.mkdir(exist_ok=True)
    GO.titulo_gancho("muro", ["¿TU TALADRO", "NO ENTRA AL MURO?"], None, y=150, px=84)
    GO.titulo_gancho("anel", ["15 POSICIONES", "DE TORQUE"], None, y=150, px=96)
    Image.new("RGBA", (GO.W, GO.H), (0, 0, 0, 0)).save(OV / "tit_vazio.png")
    for c in CORPOS.values():
        for t in c["titulos"].values():
            if not (OV / f"tt_{GO.slug(t)}.png").exists():
                GO.titulo_frase(t)
    for t in corpo_pega()["titulos"].values():
        assert (OV / f"tt_{GO.slug(t)}.png").exists(), t


def base_cfg(nome, titulo, cta_dur, pop):
    return {"saida": str(ED / "_montado" / f"{nome}.mp4"), "overlays": str(OV), "sfx": str(ED / "sfx"), "titulo": titulo,
            "cta": {"png": "cta_final.png", "dur": round(cta_dur, 3)}, "banner": True, "sticker": True,
            "selo": {"em": "sempre", "png": "selo_bf.png", "x": "W-w-10", "y": 10}, "whoosh": True, "pop": pop,
            "legenda": {"modo": "roteiro", "textos": dict(TXT_GANCHO), "y": 1060, "chaves": CHAVES, "juntar": JUNTAR},
            "loudnorm": -15, "limite_mb": 30, "segmentos": [], "extras": []}


def execucao(nome, e):
    segs = []
    g = e["gancho"]
    if g[0] == "peca":
        gd = DUR_GANCHO[g[1]]
        tr = GANCHO_DE.get(g[1], 0.0)
        segs.append({"video": str(PECAS / f"{g[1]}.mp4"), "de": tr, "tipo": "outro", "zoom": 1.0, "snap": False,
                     "audio": str(AUD / f"{g[1]}.wav"), "audio_de": tr, "audio_ate": gd, "sticker": False,
                     "legenda_y": LEG_Y_ROSTO})
        titulo = {"png": "tit_vazio.png", "dur": round(gd - tr, 3), "com_legenda": True}   # banner/selo so depois do gancho
        pop = False
    else:
        _, gid, takes, tpng = g
        ga = VOZ / f"{gid}.mp3"
        gd = round((fala_fim_el(VOZ / f"{gid}.alinhamento.json") + 0.2) * 30) / 30
        tot = sum(TAKE_DUR[t] for t, _ in takes)
        a0 = 0.0
        for k, (t, v) in enumerate(takes):
            v = v or round(max(0.7, min(1.0, tot / gd)), 3)
            d = gd - a0 if k == len(takes) - 1 else round(TAKE_DUR[t] / v * 30) / 30
            segs.append({"video": str(BANCO / f"{t}.mp4"), "tipo": "broll", "zoom": 1.0, "snap": False, "vel": v,
                         "audio": str(ga), "audio_de": round(a0, 4), "audio_ate": round(a0 + d, 4), "sticker": False})
            a0 += d
        titulo = {"png": tpng, "dur": gd, "com_legenda": True}
        pop = True
    t_gancho = round(sum((s["audio_ate"] - s["audio_de"]) for s in segs) * 30) / 30

    c = info_corpo(e["corpo"])
    cs = c["segs"]
    fim_corpo = round((c["fala_fim"] + CAUDA) * 30) / 30
    trocas = e.get("trocas", {})
    extras, pos, alertas = [], t_gancho, []
    for i, (ini_s, _) in enumerate(cs):
        ini = 0.0 if i == 0 else ini_s - 0.1
        fim = cs[i + 1][0] - 0.1 if i + 1 < len(cs) else fim_corpo
        L = fim - ini
        takes = trocas.get(i, c["takes"][i])
        tot = sum(TAKE_DUR[t] for t in takes)
        vel = 1.0 if tot >= L else max(0.7, tot / L)
        if tot / L < 0.7:
            alertas.append(f"{nome} frase {i}: takes {tot:.2f}s para {L:.2f}s (congela {L - tot / 0.7:.2f}s)")
        ds = [TAKE_DUR[t] / vel for t in takes]
        a = ini
        for k, (t, dd) in enumerate(zip(takes, ds)):
            d = fim - a if k == len(takes) - 1 else min(dd, L * dd / sum(ds))
            d = round(d * 30) / 30
            segs.append({"video": str(BANCO / f"{t}.mp4"), "tipo": "broll",
                         "zoom": 1.06 if (i % 2 == 1 and k == 0) else 1.0,   # punch-in alternado por frase
                         "snap": k == 0,                                      # snap (+8% -> 0) no 1o take de cada frase
                         "vel": round(vel, 3), "audio": str(c["audio"]), "audio_de": round(a, 4),
                         "audio_ate": round(a + d, 4), "sticker": i == len(cs) - 1,
                         **({"video_ate": round(CORTE_FIM[t], 4)} if t in CORTE_FIM else {})})
            a += d
        tt = c["titulos"].get(i)
        if tt and i not in e.get("sem_titulo", []):
            extras.append({"png": str(OV / f"tt_{GO.slug(tt)}.png"), "de": round(pos, 3), "ate": round(pos + L, 3)})
        pos += L
    total = pos
    cta_ini = t_gancho + cs[-1][0]
    cta_dur = min(CTA_DUR, total - (cta_ini + 1.5))
    cfg = base_cfg(nome, titulo, cta_dur, pop)
    cfg["segmentos"] = segs
    cfg["extras"] = extras
    return cfg, {"total": round(total, 3), "gancho": t_gancho, "cta": round(cta_dur, 3), "alertas": alertas}


if __name__ == "__main__":
    overlays()
    CFG.mkdir(exist_ok=True)
    (ED / "_montado").mkdir(exist_ok=True)
    plano = {}
    for nome, e in EXECUCOES.items():
        cfg, info = execucao(nome, e)
        json.dump(cfg, open(CFG / f"{nome}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        plano[nome] = info
    json.dump(plano, open(CFG / "_plano.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(plano, ensure_ascii=False, indent=1))
