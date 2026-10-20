# -*- coding: utf-8 -*-
"""Gera as receitas (montar.py) das 7 produções da onda 2 + textos_legenda.json. Caminhos relativos a esta pasta."""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
T, V, BR, BANCO, OV = "../takes/", "../voz/", "../../edicao/", "../../../banco/", "../overlays/"
SAIDA = "../../../entregas/ONDA2/sem-musica/"

TEXTOS = {
    "C2_T1_gancho_vz": "¿No sabes cuál perfume árabe elegir? Te recomiendo uno para cada momento del día y la habrá para cada momento del día.",
    "C2_T2_cta_vz": "¿Para qué elegir? Por Black Friday pagas dos y te llevas los tres. Y pagas cuando te llega.",
    "C4_T1_natalie_vz": "Oye, ¿qué perfume traes? Huele demasiado rico.",
    "C4_T2_aline_vz": "¡Son árabes! Tengo tres, uno para cada día. Los pedí por Black Friday: pagué dos y me llegaron tres.",
    "C5_T1_gancho_vzfix": "Si te echas perfume y te frotas las muñecas, ¿lo estás haciendo mal? o estás haciéndolas melo",
    "C5_T2_dicas_vzfix": "Al frotarlo rompes el aroma. Aplícalo en el pulso: muñecas, cuello y detrás de las orejas, y deja que se seque solo.",
    "C5_T3_cta_vz": "Estos tres Yara vienen en kit por Black Friday: pagas dos y te llevas tres, y pagas al recibir.",
    "C7_T1_gancho_vz": "Me preguntaron cuánto pagué por este perfume… y cuando les dije, no me creyeron.",
    "C7_T2_cta_vz": "Vienen tres en un kit. Por Black Friday pagas dos y te llevas los tres, y pagas al recibir.",
    "silencio": "",
}


def take(nome, de, ate, audio=None, **kw):
    a = audio or f"{nome}_vz.wav"
    s = {"video": T + f"{nome}.mp4", "tipo": "consultora", "de": de, "ate": ate,
         "audio": T + a, "audio_de": de, "audio_ate": ate}
    s.update(kw)
    return s


def broll(video, audio, de=None, ate=None, **kw):
    s = {"video": video, "tipo": "broll", "audio": audio}
    if de is not None:
        s["audio_de"], s["audio_ate"] = de, ate
    s.update(kw)
    return s


def base(nome, titulo, segs, sticker=True, cta=True, selo=True):
    return {"saida": SAIDA + f"{nome}.mp4", "overlays": BR, "sfx": BR + "sfx",
            "titulo": {"png": "../onda2/overlays/" + titulo, "dur": 1.5} if titulo else None,  # relativo a overlays
            "cta": {"png": "cta_final.png", "dur": 1.8} if cta else None,
            "banner": True, "sticker": sticker, "selo": {"em": "broll"} if selo else None, "whoosh": True, "pop": True,
            "legenda": {"modo": "roteiro", "textos": "textos_legenda.json", "y": 1060},
            "loudnorm": -15, "limite_mb": 30, "segmentos": segs}


KIT = T + "C3_T1_kit.mp4"
R = {}
R["C2_uno-para-cada-momento"] = base("C2_yara-kit3_uno-para-cada-momento_es-cl", "titulo_C2.png", [
    take("C2_T1_gancho", 0.03, 2.9),
    take("C2_T1_gancho", 2.9, 6.25, zoom="in"),
    broll(BR + "b_yara.mp4", V + "C2_N_dia.mp3", de=0.35),
    broll(BR + "b_moi.mp4", V + "C2_N_cita.mp3", png=BR + "volume/rotulo_moi.png"),
    broll(BR + "b_elixir.mp4", V + "C2_N_noche.mp3"),
    take("C2_T2_cta", 0.03, 3.15),
    take("C2_T2_cta", 3.15, 9.05, zoom="in"),
], selo=False)
R["C3_1-2-gratis"] = base("C3_yara-kit3_1-2-gratis_es-cl", None, [
    broll(KIT, V + "C3_N.mp3", 0.0, 0.64, png=OV + "C3_n1.png", dur=0.64),
    broll(KIT, V + "C3_N.mp3", 0.64, 1.09, png=OV + "C3_n2.png", dur=0.45),
    broll(KIT, V + "C3_N.mp3", 1.09, 2.68, png=OV + "C3_n3.png", dur=1.59),
    broll(BANCO + "yara_04.mp4", V + "C3_N.mp3", 2.68, 4.34),
    broll(BR + "b_elixir.mp4", V + "C3_N.mp3", 4.34, 7.57),
], selo=False)
R["C4_que-perfume-traes"] = base("C4_yara-kit3_que-perfume-traes_es-cl", "titulo_C4.png", [
    take("C4_T1_natalie", 0.4, 4.95),
    take("C4_T2_aline", 0.0, 4.45),
    take("C4_T2_aline", 4.45, 9.03, zoom="in"),
    broll(KIT, V + "C4_N_cta.mp3"),
])
R["C5_lo-estas-aplicando-mal"] = base("C5_yara-kit3_lo-estas-aplicando-mal_es-cl", "titulo_C5.png", [
    take("C5_T1_gancho", 0.0, 2.45, audio="C5_T1_gancho_vzfix.wav"),
    take("C5_T1_gancho", 2.45, 5.6, audio="C5_T1_gancho_vzfix.wav", zoom="in"),
    take("C5_T2_dicas", 0.0, 2.6, audio="C5_T2_dicas_vzfix.wav"),
    take("C5_T2_dicas", 2.6, 5.85, audio="C5_T2_dicas_vzfix.wav"),
    take("C5_T2_dicas", 5.85, 10.05, audio="C5_T2_dicas_vzfix.wav"),
    broll(BR + "b_yara.mp4", V + "C5_N_momento.mp3", 0.0, 3.75),
    broll(BR + "b_elixir.mp4", V + "C5_N_momento.mp3", 3.75, 5.67),
    take("C5_T3_cta", 0.0, 4.5),
    take("C5_T3_cta", 4.5, 9.05, zoom="in"),
])
R["C6_regalo-navidad"] = base("C6_yara-kit3_regalo-navidad_es-cl", "titulo_C6.png", [
    {"video": T + "C6_T1_reacao.mp4", "tipo": "outro", "de": 0.0, "ate": 2.14, "audio": V + "C6_N_gancho.mp3"},
    {"video": T + "C6_T1_reacao.mp4", "tipo": "broll", "de": 2.0, "audio": V + "C6_N_corpo.mp3",
     "audio_de": 0.0, "audio_ate": 4.35},
    broll(KIT, V + "C6_N_corpo.mp3", 4.35, 9.33),
])
R["C7_cuanto-pague"] = base("C7_yara-kit3_cuanto-pague_es-cl", "titulo_C7.png", [
    take("C7_T1_gancho", 0.0, 4.5),
    take("C7_T1_gancho", 4.5, 9.05, zoom="in"),
    broll(KIT, V + "C7_N_meio.mp3"),
    take("C7_T2_cta", 0.0, 4.0),
    take("C7_T2_cta", 4.0, 8.05, zoom="in"),
])
SIL = "silencio.wav"
c1 = []
for i, (v, d) in enumerate([(BANCO + "yara_09.mp4", 2.8), (BANCO + "moi_08.mp4", 2.8), (BANCO + "elixir_07.mp4", 2.8),
                            (KIT, 2.6), (KIT, 3.0)], 1):
    s = {"video": v, "tipo": "broll", "audio": SIL, "audio_de": 0, "audio_ate": d, "dur": d, "png": OV + f"C1_t{i}.png"}
    if i == 5:
        s["de"] = 2.0
    if i == 2:
        s["de"] = 0.8
    c1.append(s)
R["C1_hueles-a"] = base("C1_yara-kit3_hueles-a_es-cl", None, c1, sticker=False, selo=False)

if __name__ == "__main__":
    (AQUI / "textos_legenda.json").write_text(json.dumps(TEXTOS, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, cfg in R.items():
        (AQUI / f"{k}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(sorted(R))
