# -*- coding: utf-8 -*-
"""Plano das falas novas. Tempo local da LINHA = inclui o lead (silêncio antes da fala).
JOBS: lipsync HeyGen; 'janela' = trecho da linha (local) que vai no áudio do job, a partir do 1º quadro do vídeo-fonte."""
from pathlib import Path
T = Path(__file__).resolve().parent
GA = Path(r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es")
BASE = GA / "visual" / "base_visual_es.mp4"
AVC = GA / "audio" / "v2" / "av_chora_final.mp4"
BR = Path(r"C:\Users\PICHAU\Downloads\SB-BANCO-BROLL")
LINHAS = {"chora": dict(tts="chora_v2", lead=0.15, fim=0.15 + 5.67 + 0.22),
          "jm1": dict(tts="jm1", lead=0.10, fim=11.08),
          "jm2": dict(tts="jm2", lead=0.15, fim=6.40),
          "jm3": dict(tts="jm3", lead=0.10, fim=11.19)}
JOBS = {
 "chora": dict(linha="chora", src=("avc", 508, 658), crop=None, janela=(0.0, 5.03)),
 "jm1":   dict(linha="jm1", src=("base", 667, 923), crop=[109, 19, 558, 992], janela=[(0.0, 4.55), (9.52, 11.08)]),
 "jm2":   dict(linha="jm2", src=("base", 1832, 2023), crop=[136, 20, 432, 768], janela=(0.0, 6.40)),
 "jm3a":  dict(linha="jm3", src=("base", 2852, 2947), crop=[88, 0, 632, 1124], janela=(0.0, 3.20)),
 "jm3b":  dict(linha="jm3", src=("base", 3600, 3755), crop=[120, 0, 600, 1067], janela=(6.12, 11.19)),
}
# partes visuais de cada linha: (a, b, tipo, ref, t_no_ref) -> mostra ref a partir de t_no_ref
PARTES = {
 "chora": [(0.0, 4.41, "ls", "chora", 0.0), (4.41, LINHAS["chora"]["fim"], "broll", "sagrado/sagrado_34_familia-celular-juntos.mp4", 0.3)],
 "jm1":   [(0.0, 4.55, "ls", "jm1", 0.0), (4.55, 7.38, "broll", "problema/problema_02_maos-contando-moedas.mp4", 0.2),
           (7.38, 9.52, "broll", "problema/problema_10_porta-aco-cadeado.mp4", 0.3), (9.52, 11.08, "ls", "jm1", 4.55)],
 "jm2":   [(0.0, 6.40, "ls", "jm2", 0.0)],
 "jm3":   [(0.0, 3.10, "ls", "jm3a", 0.0), (3.10, 6.12, "broll", "oracion/oracion_30_capilla-noche-velas.mp4", 0.2), (6.12, 11.19, "ls", "jm3b", 0.0)],
}
