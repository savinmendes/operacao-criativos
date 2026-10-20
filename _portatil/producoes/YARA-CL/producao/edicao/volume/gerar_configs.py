# -*- coding: utf-8 -*-
"""Gera cfg_H1..H5.json: gancho novo + corpo do AD-C a partir de T3 (Este es Yara) ate o CTA."""
import json, copy
from pathlib import Path
AQUI = Path(__file__).resolve().parent
base = json.load(open(AQUI.parent / "ad_C_final.json", encoding="utf-8"))
corpo = []
for s in base["segmentos"][3:]:
    s = copy.deepcopy(s)
    s["video"] = "../" + s["video"]
    if s.get("audio"):
        s["audio"] = "../" + s["audio"]
    corpo.append(s)
T1, T1A = "../../takes/T1_gancho_v2.mp4", "../../takes/T1_gancho_v2_vz.wav"
T4, T4A = "../../takes/T4_yara_close.mp4", "../../takes/T4_yara_close_vz.wav"
T10, T10A = "../../takes/T10_cta.mp4", "../../takes/T10_cta_vz.wav"
B = "../../../banco/"


def cons(v, a, de, ate, **kw):
    return {"video": v, "tipo": "consultora", "de": de, "ate": ate, "audio": a, "audio_de": de, "audio_ate": ate, **kw}


def bro(take, ini, a_de, a_ate, **kw):
    """take do banco com a VOZ do T1 por cima (snap + leve push-in = movimento no 1o quadro)"""
    d = {"video": B + take, "tipo": "broll", "de": ini, "audio": T1A, "audio_de": a_de, "audio_ate": a_ate,
         "snap": True, "zoom": kw.pop("zoom", "in"), "centro": kw.pop("centro", [0.5, 0.5])}
    d.update(kw)
    return d


T1_RESTO = [cons(T1, T1A, 2.5, 6.05), cons(T1, T1A, 6.05, 10.08)]
ganchos = {
    "H1": dict(titulo=("titulo_abertura.png", 1.5), segs=[cons(T1, T1A, 0.03, 1.30), cons(T1, T1A, 1.30, 2.5)] + T1_RESTO),
    # oferta primeiro: "Pagas dos y te llevas los tres." (punch-in no balcao) -> "Llevate los tres Yara muy por debajo..."
    "H2": dict(titulo=("volume/titulo_H2.png", 1.5), segs=[
        cons(T10, T10A, 0.46, 1.56, zoom=1.35, centro=[0.56, 0.40]),
        cons(T10, T10A, 1.56, 2.66, zoom=1.7, centro=[0.56, 0.36], legenda_y=1450),  # legenda abaixo do rosto no close
        cons(T1, T1A, 2.5, 4.34), cons(T1, T1A, 4.34, 6.05)]),
    # movimento/curiosidade: ela cheira o frasco (antes de falar) -> T1 inteiro
    "H3": dict(titulo=("volume/titulo_H3.png", 1.35), segs=[
        {"video": T4, "tipo": "consultora", "de": 0.25, "ate": 1.60, "audio": T4A, "audio_de": 0.25, "audio_ate": 1.60,
         "zoom": "in", "centro": [0.5, 0.45]},
        cons(T1, T1A, 0.03, 1.30), cons(T1, T1A, 1.30, 2.5)] + T1_RESTO),
    # unboxing: 4 cortes rapidos (<=0,8 s) + mais B-roll, tudo com a voz do T1
    "H4": dict(titulo=("volume/titulo_H4.png", 1.5), segs=[
        bro("yara_03.mp4", 0.3, 0.03, 0.83),
        bro("elixir_09.mp4", 0.4, 0.83, 1.63, centro=[0.5, 0.55]),
        bro("moi_12.mp4", 0.2, 1.63, 2.43),
        bro("yara_05.mp4", 0.5, 2.43, 3.20),
        bro("elixir_02.mp4", 0.3, 3.20, 4.34),
        bro("yara_08.mp4", 0.6, 4.34, 5.08),
        bro("moi_07.mp4", 0.3, 5.08, 6.05),
        bro("elixir_10.mp4", 0.3, 6.05, 7.84),
        bro("yara_09.mp4", 0.5, 7.84, 10.08)]),
    # lista visual: 3 closes com rotulo grande + voz do T1, depois a consultora segue o T1
    "H5": dict(titulo=("volume/titulo_H5.png", 2.47), segs=[
        bro("yara_04.mp4", 1.0, 0.03, 0.853, png="rotulo_yara.png"),
        bro("moi_12.mp4", 0.1, 0.853, 1.677, png="rotulo_moi.png"),
        bro("elixir_10.mp4", 0.2, 1.677, 2.5, png="rotulo_elixir.png")] + T1_RESTO),
}
EXTRA = [[r"^feminino([.,]*)$", r"femenino\1"], [r"^porqu[ií]dea([.,]*)$", r"Orquídea\1"], ["^palas$", "Pagas"], [r"^mullo([.,]*)$", r"Moi\1"], ["^precio$", "precio"], ["^mercado$", "mercado."]]
# H3: o whisper sobre a voz com silencio inicial devolveu o trecho do T1 em MAIUSCULAS -> volta ao normal (sensivel a caixa)
EXTRA_H3 = [[f"(?-i:^{a}$)", b] for a, b in [("LIQUIDACIÓN", "¡Liquidación"), ("TOTAL", "total"), ("POR", "por"), ("BLACK", "Black"),
            ("FRIDAY", "Friday!"), ("LLÉVATE", "Llévate"), ("LOS", "los"), ("TREES", "tres"), ("YAYA", "Yara"), ("MUY", "muy"),
            ("DEBAJO", "debajo"), ("EL", "del"), ("Precio", "precio"), ("Mercado", "mercado.")]]
for h, g in ganchos.items():
    cfg = copy.deepcopy(base)
    cfg["legenda"]["corrigir"] += EXTRA + (EXTRA_H3 if h == "H3" else [])
    cfg["saida"] = f"../../../entregas/volume/YARA-BF_{h}_sem-musica.mp4"
    cfg["overlays"] = ".."
    cfg["sfx"] = "../sfx"
    cfg["titulo"] = {"png": g["titulo"][0], "dur": g["titulo"][1]}
    cfg["segmentos"] = g["segs"] + corpo
    json.dump(cfg, open(AQUI / f"cfg_{h}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(h, len(cfg["segmentos"]), "segmentos")
