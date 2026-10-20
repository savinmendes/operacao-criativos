# -*- coding: utf-8 -*-
"""Normaliza os b-rolls GERADOS no Flora: takes Kling 2.5 (24 fps -> 30) e stills com Ken Burns."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import norm
BR = Path(__file__).resolve().parents[1]; R = BR / "gerado" / "raw"; I = BR / "gerado" / "img"
# Kling: trecho util (s no take bruto) - corta artefatos vistos na folha (serpente vira fumaça >3 s; fosforo vira chama grande >2 s;
# cadeado some no fim do cofre)
K = {"k01_cofre": (0.15, 3.2), "k02_sb_rostro": (0.0, 5.0), "k03_serpiente": (0.15, 2.85), "k04_altar_incienso": (0.0, 5.0),
     "k05_biblioteca_secreta": (0.0, 5.0), "k06_monjes_claustro": (0.0, 5.0), "k07_abadia_italia": (0.0, 5.0),
     "k08_congreso_adoracion": (0.0, 5.0), "k09_grimorio_paginas": (0.0, 5.0), "k10_ampolleta": (0.0, 5.0),
     "k11_familia_feliz": (0.0, 5.0), "k12_abuela_alegria": (0.0, 5.0), "k13_vela_encendiendo": (0.1, 1.9), "k14_amanecer_valle": (0.0, 5.0)}
RAW = {"k02_sb_rostro": "k02_sb_rosto", "k04_altar_incienso": "k04_altar", "k05_biblioteca_secreta": "k05_biblioteca",
       "k06_monjes_claustro": "k06_monjes", "k07_abadia_italia": "k07_abadia", "k10_ampolleta": "k10_ampulheta",
       "k11_familia_feliz": "k11_familia", "k13_vela_encendiendo": "k13_vela", "k14_amanecer_valle": "k14_amanecer_valle"}
only = sys.argv[1:]
for n, (a, b) in K.items():
    if only and n not in only: continue
    norm.video(R / f"{RAW.get(n, n)}.mp4", BR / f"{n}.mp4", a, b); print(n, b - a)
S = {"s14_reloj_bolsillo": ("g14_reloj.png", 2.5, 1.0, 1.15, .5, .55, .5, .6),
     "s15_calendario_7_dias": ("g15_calendario.png", 2.5, 1.0, 1.12, .45, .45, .4, .4),
     "s16_rosario_manos": ("g16_rosario.png", 2.5, 1.12, 1.0, .5, .5, .5, .55),
     "s17_vitral_luz": ("g17_vitral.png", 2.5, 1.0, 1.12, .5, .4, .5, .5),
     "s18_hombre_cerro_amanecer": ("g18_hombre_cerro.png", 2.5, 1.15, 1.0, .5, .55, .5, .5),
     "s19_colar_altar_terciopelo": ("g19_colar_altar.png", 3.0, 1.0, 1.15, .5, .62, .5, .68),
     "s20_colar_manos_rezando": ("g20_colar_manos.png", 3.0, 1.0, 1.12, .55, .6, .6, .62),
     "s21_biblia_banca": ("g21_biblia_banca.png", 2.5, 1.0, 1.12, .5, .5, .5, .55),
     "s22_mujer_arrodillada_iglesia": ("g22_mujer_arrodillada.png", 3.0, 1.12, 1.0, .5, .5, .5, .5),
     "s24_hombre_rezando_vela": ("g24_hombre_rezando_vela.png", 2.5, 1.0, 1.12, .5, .45, .45, .45)}
for n, (img, d, z0, z1, x0, y0, x1, y1) in S.items():
    if only and n not in only: continue
    if not (I / img).exists(): print("falta", img); continue
    norm.kb(I / img, BR / f"{n}.mp4", d, z0, z1, x0, y0, x1, y1); print(n, d)
