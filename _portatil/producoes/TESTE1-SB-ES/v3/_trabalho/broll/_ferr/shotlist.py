# -*- coding: utf-8 -*-
"""Gera broll/shotlist.json. Tempos dos blocos V* = padre/audio/itens.json (wavs reais vo_V*.wav);
O01 = voz v1 L09 (+0,40 s) + L09b. P06 = audio do take do sacerdote (inserts do colar)."""
import json, subprocess, unicodedata
from pathlib import Path
BR = Path(__file__).resolve().parents[1]; T = BR.parent; RAIZ = T.parents[1]
IT = json.loads((T / "padre" / "audio" / "itens.json").read_text(encoding="utf-8"))
def norm(w): return unicodedata.normalize("NFKD", w.lower()).encode("ascii", "ignore").decode().strip("¿¡.,;:!?… ")
L09 = json.loads((RAIZ / "_trabalho" / "voz" / "c" / "L09.json").read_text(encoding="utf-8"))
L09B = json.loads((RAIZ / "_trabalho" / "voz" / "c" / "L09b.json").read_text(encoding="utf-8"))
GAP_B = 0.40; T0B = round(L09["dur"] + GAP_B, 3)
BLOCOS = {k: dict(dur=IT[k]["dur"], palavras=IT[k]["palavras"]) for k in ["V01", "V02", "V03", "V04", "V05", "V06", "V07", "V08", "V09", "P06"]}
BLOCOS["O01"] = dict(dur=round(T0B + L09B["dur"], 3),
                     palavras=L09["palavras"] + [dict(w=p["w"], ini=round(T0B + p["ini"], 3), fim=round(T0B + p["fim"], 3)) for p in L09B["palavras"]])
ORD = ["V01", "O01", "V02", "V03", "V04", "V05", "V06", "V07", "P06", "V08", "V09"]
def W(b, w, n=1):
    k = 0
    for p in BLOCOS[b]["palavras"]:
        if norm(p["w"]) == norm(w):
            k += 1
            if k == n: return p["ini"]
    raise KeyError((b, w, n))
# (bloco, arquivo, âncora (palavra, n) ou None=início, descrição)
PLANO = [
 ("V01", "e01_teclado", None, "manos tecleando en la oscuridad (quieren borrar/ocultar)"),
 ("V01", "k01_cofre", ("acceso", 1), "mano anciana cierra con candado un cofre antiguo"),
 ("V01", "s17_vitral_luz", ("porque", 1), "vitral con rayos de luz (oración poderosa)"),
 ("O01", "k02_sb_rostro", None, "rostro de San Benito mirando al cielo, luz divina"),
 ("O01", "e02_sb_de_pie", ("guardián", 1), "San Benito de pie en la iglesia"),
 ("O01", "k04_altar_incienso", ("misterios", 1), "altar con libro y medalla, incienso (misterios sagrados)"),
 ("O01", "k03_serpiente", ("que", 1), "serpiente negra retrocede ante la luz"),
 ("O01", "e08_cruz_agua", ("señal", 1), "cruz luminosa sobre el agua"),
 ("O01", "e04_sb_acantilado", ("y", 1), "San Benito en el acantilado ante el mar (rugido del abismo)"),
 ("O01", "e10_hombre_rezando", ("inquebrantable", 1), "hombre rezando en penumbra (fe)"),
 ("O01", "s22_mujer_arrodillada_iglesia", ("invoco", 1), "mujer arrodillada sola en la iglesia"),
 ("O01", "e05_mujer_rezando", ("por", 1), "mujer rezando de perfil"),
 ("O01", "e19_cuadro_12_palabras", ("crux", 1), "cuadro ES 'Las 12 Palabras Sagradas de San Benito'; círculos rojos ya sincronizados al L09b (t=0 del archivo = inicio del L09b)"),
 ("V02", "e16_print_geralda", None, "print WhatsApp Geralda (relatos)"),
 ("V02", "e11_nino_playa", ("todos", 1), "niño arrodillado en la playa al atardecer"),
 ("V03", "e03_sb_escribiendo", None, "San Benito escribiendo la regla"),
 ("V03", "e07_pergamino", ("en", 1), "pergamino antiguo (su regla)"),
 ("V03", "k05_biblioteca_secreta", ("durante", 1), "biblioteca monástica secreta y polvorienta (918 años)"),
 ("V04", "k06_monjes_claustro", None, "monjes benedictinos caminando en claustro italiano"),
 ("V04", "e09_montanas_niebla", ("la", 1), "montañas con niebla (excursión)"),
 ("V04", "k07_abadia_italia", ("que", 1), "abadía en la cima de una montaña de Italia (aérea)"),
 ("V04", "e13_mujer_negra_rezando", ("decidí", 1), "mujer rezando (compartirla con ustedes)"),
 ("V05", "e12_congreso", None, "congreso: público en el auditorio"),
 ("V05", "k08_congreso_adoracion", ("en", 1), "multitud con manos alzadas en el congreso"),
 ("V05", "e17_print_rosa_maria", ("recibí", 1), "print WhatsApp Rosa María + transferencia US$ 13.000"),
 ("V05", "e18_print_carmen", ("relatos", 1), "print WhatsApp Carmen (relato de bendición)"),
 ("V06", "e06_sb_grimorio", None, "San Benito sostiene el libro GRIMORIO SAGRADO Y SECRETO DE SAN BENITO"),
 ("V06", "k09_grimorio_paginas", ("de", 1), "manos pasan las páginas del Grimorio con diagramas/instrucciones"),
 ("V07", "k10_ampolleta", None, "ampolleta (reloj de arena) corriendo"),
 ("V07", "s14_reloj_bolsillo", ("tiempo", 1), "reloj de bolsillo antiguo"),
 ("P06", "s19_colar_altar_terciopelo", ("collar", 1), "INSERT collar San Benito sobre terciopelo en el altar con velas"),
 ("P06", "s20_colar_manos_rezando", ("el", 2), "INSERT collar entre las manos de una persona rezando"),
 ("V08", "e14_deudas", None, "manos sobre cuentas/deudas, hombre angustiado"),
 ("V08", "e15_alivio_paid", ("bienvenida", 1), "luz dorada: alivio, cuentas pagadas"),
 ("V09", "s15_calendario_7_dias", None, "calendario con 7 días tachados y el 8o marcado"),
 ("V09", "k12_abuela_alegria", ("para", 1), "abuela sonriendo con lágrimas de alegría"),
 ("V09", "k11_familia_feliz", ("que", 1), "familia feliz abrazándose"),
]
EXTRAS = [("k13_vela_encendiendo", "vela encendiéndose en iglesia oscura"), ("s16_rosario_manos", "rosario con medalla en manos arrugadas"),
          ("s18_hombre_cerro_amanecer", "hombre arrodillado en el cerro con manos al cielo"), ("s21_biblia_banca", "Biblia abierta con rosario en banca de iglesia"),
          ("k14_amanecer_valle", "amanecer dorado sobre valle con iglesia (time-lapse)"), ("s24_hombre_rezando_vela", "hombre rezando de perfil a la luz de una vela")]
FONTE_E = {"e16": "v1 _trabalho/graficos/chat_1.png", "e17": "v1 _trabalho/graficos/chat_2.png", "e18": "v1 _trabalho/graficos/chat_3.png",
           "e19": "v1 _trabalho/q/board_clean.png + graficos/board_titulo.png + circ_*.png"}
CORTES = {"e01": (46.80, 47.83), "e02": (51.50, 52.75), "e03": (53.30, 55.28), "e04": (55.40, 58.15), "e05": (58.28, 59.75), "e06": (77.95, 80.22),
          "e07": (82.60, 85.55), "e08": (88.85, 89.95), "e09": (90.45, 91.95), "e10": (92.50, 93.88), "e11": (95.88, 97.18), "e12": (99.05, 101.15),
          "e13": (106.58, 108.80), "e14": (132.85, 136.15), "e15": (136.42, 139.65)}
def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
def custo(n):
    if n.startswith("k"): return 0.303, "Flux 2 (US$0,009) + Kling 2.5 Turbo i2v 5 s (US$0,294)"
    if n in ("s19_colar_altar_terciopelo", "s20_colar_manos_rezando"): return 0.263, "GPT Image 2 1k high com a foto real do colar como referência (US$0,263) + Ken Burns local"
    if n.startswith("s"): return 0.009, "Flux 2 (US$0,009) + Ken Burns local"
    return 0.0, "reaproveitado (sem custo)"
def fonte(n):
    if n[:3] in FONTE_E: return FONTE_E[n[:3]]
    if n[0] == "e": a, b = CORTES[n[:3]]; return f"TESTE1 limpo por LaMa (v1 _trabalho/lama/base_limpa.mp4) {a:.2f}-{b:.2f} s"
    return "Flora, projeto 'SB-ES Noticia Aurelio v2' (imagem base em broll/gerado/img, take bruto em broll/gerado/raw)"
out = []; usados = set()
for b in ORD:
    itens = [x for x in PLANO if x[0] == b]
    ini = [0.0 if a is None else max(0.0, round(W(b, *a) - 0.08, 3)) for _, _, a, _ in itens]
    fim = ini[1:] + [round(BLOCOS[b]["dur"] + 0.15, 3)]
    if b == "P06": fim = [ini[1], round(W("P06", "en", 1) - 0.08, 3)]
    for k, ((_, arq, a, desc), t0, t1) in enumerate(zip(itens, ini, fim)):
        assert arq not in usados, arq; usados.add(arq)
        d = round(dur(BR / f"{arq}.mp4"), 3); need = round(t1 - t0, 3)
        vel = round(min(1.0, d / need), 3)
        c, cd = custo(arq)
        out.append({"bloco": b, "ordem": k + 1, "arquivo": f"broll/{arq}.mp4", "t_bloco_ini": t0, "t_bloco_fim": t1,
                    "ancora": a[0] if a else "(início do bloco)", "in": 0.0, "out": round(min(d, need), 3), "dur_arquivo": d, "vel_sugerida": vel,
                    "obs": ("arquivo mais curto que o trecho: câmera lenta na vel_sugerida ou estender o plano vizinho" if vel < 0.999 else ""),
                    "descricao": desc, "origem": "existente" if arq[0] == "e" else "gerado", "fonte": fonte(arq), "custo_usd": c, "custo_detalhe": cd})
for k, (arq, desc) in enumerate(EXTRAS):
    assert arq not in usados, arq; usados.add(arq)
    d = round(dur(BR / f"{arq}.mp4"), 3); c, cd = custo(arq)
    out.append({"bloco": "EXTRA", "ordem": k + 1, "arquivo": f"broll/{arq}.mp4", "t_bloco_ini": None, "t_bloco_fim": None,
                "ancora": "cobertura curta para pausa ruim dos avatares (1-2 s)", "in": 0.0, "out": round(min(d, 2.0), 3), "dur_arquivo": d,
                "vel_sugerida": 1.0, "obs": "usar 1-2 s; cada um só uma vez", "descricao": desc, "origem": "gerado", "fonte": fonte(arq),
                "custo_usd": c, "custo_detalhe": cd})
res = {"regra": "cada arquivo = um plano distinto; usar cada um UMA vez no vídeo (nenhum se repete entre blocos)",
       "tempos": f"t_bloco_ini/fim em s relativos ao início do áudio do bloco (V* = padre/vo_V*.wav via padre/audio/itens.json; O01 = voz v1 L09 com o L09b começando em {T0B} s; P06 = padre/audio/P06.wav). in/out = trecho sugerido do arquivo.",
       "formato": "720x1280, 30 fps, yuv420p, pixels em matriz bt601/tv (etiqueta bt709/tv só no bitstream, convenção comum3.ENC_TAG), sem áudio",
       "o01_l09b_t0": T0B, "planos": out}
(BR / "shotlist.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "planos")
for x in out:
    print(f"{x['bloco']:5s} {x['ordem']} {x['arquivo'][6:]:36s} {str(x['t_bloco_ini']):>6}-{str(x['t_bloco_fim']):6} dur {x['dur_arquivo']:5.2f} vel {x['vel_sugerida']}")
