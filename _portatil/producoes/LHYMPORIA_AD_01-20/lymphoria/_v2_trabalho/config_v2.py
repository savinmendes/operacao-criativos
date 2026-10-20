# -*- coding: utf-8 -*-
"""Como cada AD do lote antigo Lymphoria foi montado (levantado em 05/10/2026 a partir de
_trabalho/processar_ad.py, rNN.json, logs log_r*.txt, trechos.json, receita_final.json e do histórico
de comandos da sessão que produziu o lote). Usado por encaixar_v2.py e montar_v2.py.

Para cada AD:
  base      = vídeo onde os takes foram encaixados (substituir_trechos)
  hook_old  = parte 1 que entrou no AD entregue (o áudio dela é reaproveitado sem mexer)
  refazer   = takes com o defeito: clipe usado no trechos.json -> (take original, edit Kling, --dur)
  etapas    = passos de vídeo depois do encaixe, na mesma ordem (blur / texto). Etapas de áudio
              (trocar_trecho_audio) não mexem no vídeo (-c:v copy) -> o áudio vem pronto do hook_old.
  remendo   = take encaixado depois na parte1 já pronta (remendar_ad.py)
  classico  = AD montado com o montar_ad.py clássico (antes do caminho rápido existir)
"""
import json
from pathlib import Path

LOTE = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria")
OLD = LOTE / "_trabalho"
V2 = LOTE / "_v2_trabalho"
SAIDA = LOTE / "_v2_corrigidos"
KIT = V2 / "kit" / "ferramentas"


def _receita(n):
    return json.load(open(OLD / f"r{n}.json", encoding="utf-8-sig"))


def _etapas_receita(r):
    """processar_ad.py: blur (todos) -> textos (todos) -> áudios."""
    et = [("blur", b) for b in r.get("blur", [])]
    et += [("texto", t) for t in r.get("textos", [])]
    return et


def _dur(q):
    return f"{q / 30:.3f}"     # igual ao processar_ad.py


def _de_receita(n, flag):
    r = _receita(n)
    ref = {}
    for t in r["takes"]:
        nome = Path(t["orig"]).stem
        if nome in flag:
            ref[f"flora/{nome}_final.mp4"] = (t["orig"], f"flora/{nome}_edit.mp4", _dur(t["quadros"]))
    return dict(saida=r["saida"], base="base.mp4", hook_old="parte1.mp4", refazer=ref,
                etapas=_etapas_receita(r), remendo=None, classico=False)


ADS = {
    # ---- defeito visível (letras/marcas do rótulo antigo) ----
    "ad01": dict(  # trechos: t1 (loop do original, sem Kling: fica) + t3 (Kling). t2 nunca entrou no AD.
        saida="AD 01 - LYMPHORIA-ESPOSA-ES-LATAM.mp4", base="base.mp4", hook_old="parte1.mp4",
        refazer={"flora/t3_final.mp4": ("flora/t3.mp4", "flora/t3_edit.mp4", "2.37")},
        etapas=[("texto", {"de": 241, "ate": 250, "ref": 246.0, "caixa": "95,992,625,1042",
                           "texto": "cuatro plantas. Lymphoria.", "px": 39, "contorno": 0,
                           "fonte": "Poppins-Medium.ttf"})],
        remendo=None, classico=False),
    "ad09": _de_receita("09", {"t1", "t2"}),
    "ad11": _de_receita("11", {"t1", "t2", "t3", "t4", "t5"}),
    "ad16": _de_receita("16", {"t2", "t3"}),
    "ad03": dict(  # takes refeitos com o 2º edit Kling (t*_edit2.mp4)
        saida="AD 03 - LYMPHORIA-ESQUELETO-30DIAS-ES-LATAM.mp4", base="base.mp4", hook_old="parte1.mp4",
        refazer={"flora/t1_final.mp4": ("flora/t1.mp4", "flora/t1_edit2.mp4", "5.4"),
                 "flora/t2_final.mp4": ("flora/t2.mp4", "flora/t2_edit2.mp4", "5.067")},
        etapas=[("texto", {"de": 2.15, "ate": 2.97, "caixa": "200,955,520,1045", "texto": "Lymphoria",
                           "maiusc": True, "px": 60, "contorno": 4, "fonte": "Poppins-Bold.ttf"})],
        remendo=None, classico=False),
    "ad14": dict(_de_receita("14", {"t1", "t2", "t3", "t4", "t5"}),
                 remendo={"clipe": "flora2/t6_final.mp4", "orig": "flora2/t6.mp4", "edit": "flora2/t6_edit.mp4",
                          "dur": _dur(38), "inicio": 382.167, "quadros": 38}),
    # ---- manchas brancas ----
    "ad02": _de_receita("02", {"t1", "t2", "t3"}),
    "ad04": dict(  # AD do 1º dia: base = parte1_up.mp4, sem etapas depois, montado pelo montar_ad clássico
        saida="AD 04 - LYMPHORIA-ESQUELETO-CERVEZA-ES-LATAM.mp4", base="parte1_up.mp4",
        hook_old="parte1_lymphoria.mp4",
        refazer={"flora/take1_final.mp4": ("flora/take1.mp4", "flora/take1_edit.mp4", None),
                 "flora/take34_final.mp4": ("flora/take34.mp4", "flora/take34_edit.mp4", None),
                 "flora/take67_final.mp4": ("flora/take67.mp4", "flora/take67_edit.mp4", "2.233"),
                 "flora/r4_final.mp4": ("flora/r4.mp4", "flora/r4_edit.mp4", "1.166"),
                 "flora/r5_final.mp4": ("flora/r5.mp4", "flora/r5_edit.mp4", "1.333")},
        etapas=[], remendo=None, classico=True),
    "ad10": dict(
        saida="AD 10 - LYMPHORIA-MATRIMONIO-ES-LATAM.mp4", base="base.mp4", hook_old="parte1.mp4",
        refazer={"flora/t1_final.mp4": ("flora/t1.mp4", "flora/t1_edit2.mp4", "1.37"),
                 "flora/t3_final.mp4": ("flora/t3.mp4", "flora/t3_edit.mp4", "2.5")},
        etapas=[("texto", {"de": 282, "ate": 288, "ref": 285.2, "caixa": "220,1052,500,1104", "texto": "Lymphoria.",
                           "px": 44, "contorno": 2, "fonte": "Poppins-Medium.ttf"}),
                ("texto", {"de": 375, "ate": 380, "ref": 377.6, "caixa": "220,1052,500,1104", "texto": "Lymphoria.",
                           "px": 44, "contorno": 2, "fonte": "Poppins-Medium.ttf"})],
        remendo={"clipe": "flora2/t4p_final.mp4", "orig": "flora2/t4p.mp4", "edit": "flora2/t4p_edit.mp4",
                 "dur": _dur(69), "inicio": 285.3, "quadros": 69},
        classico=False),
    "ad12": _de_receita("12", {"t1", "t2"}),
    "ad13": _de_receita("13", {"t1", "t2", "t4", "t5"}),
    "ad19": _de_receita("19", {"t1", "t2", "t3", "t4"}),  # t2: fora da lista da auditoria, mas com mancha branca grande (ver RELATORIO)
    "ad22": _de_receita("22", {"t2"}),
}

# takes que entram no AD mas não estavam na lista da auditoria (conferidos à parte, ver encaixar_v2.py)
NAO_LISTADOS = {
    "ad10": {"flora/t2_final.mp4": ("flora/t2.mp4", "flora/t2_edit.mp4", "3.06")},
    "ad13": {"flora/t3_final.mp4": ("flora/t3.mp4", "flora/t3_edit.mp4", _dur(118))},
    "ad16": {"flora/t1_final.mp4": ("flora/t1.mp4", "flora/t1_edit.mp4", _dur(69))},
    "ad22": {"flora/t1_final.mp4": ("flora/t1.mp4", "flora/t1_edit.mp4", _dur(113))},
    "ad04": {"flora/r2_final.mp4": ("flora/r2.mp4", "flora/r2_edit.mp4", "2.6"),
             "flora/r7_final.mp4": ("flora/r7.mp4", "flora/r7_edit.mp4", "0.533")},
}

ORDEM = ["ad01", "ad09", "ad11", "ad16", "ad03", "ad14", "ad02", "ad04", "ad10", "ad12", "ad13", "ad19", "ad22"]
