# -*- coding: utf-8 -*-
"""v2 (padre Juan Méndez = avatar novo HeyGen a partir do rosto da página). Tempos locais do SEGMENTO (já com o lead).
A = janelas com o avatar (cortes em fronteiras de palavra); B = b-roll do banco cobrindo pausas/trechos."""
from pathlib import Path
T = Path(__file__).resolve().parent
BR = Path(r"C:\Users\PICHAU\Downloads\SB-BANCO-BROLL")
LEAD = 0.10
LINHAS = {"jm1": 10.68 + 0.30, "jm_previa": 10.96 + 0.30, "jm2": 6.04 + 0.25, "jm_monjes": 7.66 + 0.25, "jm_mec": 11.80 + 0.20, "jm3": 10.59 + 0.50}
def L(x): return round(LEAD + x, 3)
# (ini, fim, tipo, ref)  tipo: av (avatar) | broll
PARTES = {
 "jm1": [(0, L(3.50), "av"), (L(3.50), L(5.08), "broll", "oracion/oracion_08_hombre-arrodillado-iglesia.mp4"),
         (L(5.08), L(7.30), "broll", "problema/problema_02_maos-contando-moedas.mp4"), (L(7.30), L(9.43), "broll", "problema/problema_10_porta-aco-cadeado.mp4"),
         (L(9.43), L(LINHAS["jm1"]), "av")],
 "jm_previa": [(0, L(1.66), "av"), (L(1.66), L(3.73), "broll", "sagrado/sagrado_08_manuscrito-iluminado-vela.mp4"),
               (L(3.73), L(6.96), "broll", "sagrado/sagrado_25_cruz-pedra-topo-montanha.mp4"), (L(6.96), L(9.27), "broll", "sagrado/sagrado_29_ceu-dramatico-raios-colinas.mp4"),
               (L(9.27), L(LINHAS["jm_previa"]), "av")],
 "jm2": [(0, L(LINHAS["jm2"]), "av")],
 "jm_monjes": [(0, L(2.00), "broll", "sagrado/sagrado_03_dois-monges-claustro-costas.mp4"), (L(2.00), L(4.18), "broll", "sagrado/sagrado_07_maos-folheando-manuscrito.mp4"),
               (L(4.18), L(LINHAS["jm_monjes"]), "av")],
 "jm_mec": [(0, L(3.59), "av"), (L(3.59), L(5.48), "broll", "oracion/oracion_15_anciano-manos-biblia-vela.mp4"),
            (L(5.48), L(8.66), "av"), (L(8.66), L(LINHAS["jm_mec"]), "broll", "sagrado/sagrado_31_mao-celular-live-borrao.mp4")],
 "jm3": [(0, L(3.00), "av"), (L(3.00), L(6.02), "broll", "oracion/oracion_30_capilla-noche-velas.mp4"), (L(6.02), L(LINHAS["jm3"]), "av")],
}
def fim(n): return L(LINHAS[n])
PRE, GAP, POS = 0.25, 0.45, 0.40     # silêncio no áudio do HeyGen: início, entre janelas, fim
def mapa(n):
    """[(ini_seg, fim_seg, ini_no_video_heygen)] das janelas de avatar"""
    out = []; t = PRE
    for p in PARTES[n]:
        if p[2] != "av": continue
        out.append((p[0], p[1], t)); t += (p[1] - p[0]) + GAP
    return out, t - GAP + POS
