# -*- coding: utf-8 -*-
"""Lote 3: todas as famílias refeitas com os 5 mais vendidos (ranking da loja: Vittorio, Dominante, Milano, Opulent, Maretti)."""
import os

import gerar_lote as g1
import gerar_lote2 as g2

SAIDA = os.path.join(g1.BASE, "lote3-vencedores")
V = ["vittorio", "pelvini-dominante", "pelvini-milano", "pelvini-opulent", "pelvini-maretti-1"]
N = {h: g2.nome_curto(h) for h in V}
PARES = [("vittorio", "pelvini-milano"), ("pelvini-dominante", "pelvini-opulent"), ("pelvini-milano", "pelvini-maretti-1"),
         ("pelvini-opulent", "vittorio"), ("pelvini-maretti-1", "pelvini-dominante")]
CORES = [(242, 107, 29), (246, 197, 49), (225, 48, 48), (242, 107, 29), (246, 197, 49)]
VIDA = ["vittorio_5.jpg", "pelvini-milano_5.jpg"]
ESTUDIO = ["vittorio_6.jpg", "pelvini-dominante_5.jpg", "pelvini-dominante_6.jpg", "pelvini-dominante_4.jpg"]


def plano():
    p = []
    add = lambda fam, nome, fn, *a: p.append((fam, nome, fn, a))
    for (a, b), cor in zip(PARES, CORES):
        add("bogo-saturado", f"C1_P2_bogo-saturado_{N[a]}-{N[b]}", g2.f_bogo_saturado, a, b, cor)
        add("bogo-caixa", f"C1_P2_bogo-caixa_{N[a]}-{N[b]}", g1.t_bogo_caixa, a, b)
    for h in V:
        add("vs-designer", f"C2_P1_vs-designer_{N[h]}", g2.f_vs_designer, h)
        add("is-name-worth", f"C2_P1_is-name-worth_{N[h]}", g2.f_is_name_worth, h)
        add("ancora-10k", f"C2_P1_ancora-10k_{N[h]}", g1.t_ancora, h)
        add("generico-x-nos", f"C3_P3_generico-x-nos_{N[h]}", g1.t_genericoxnos, h)
        add("garantia-90d", f"C4_P3_garantia-90d_{N[h]}", g1.t_garantia, h)
        add("poster", f"C7_P1_poster_{N[h]}", g2.f_poster, h, "316L STEEL  ·  BUY 1 GET 1 FREE")
        add("postit", f"C8_P2_postit-produto_{N[h]}", g2.f_postit, h, ["2nd watch\nFREE\nends tonight", "BUY 1\nGET 1\nFREE", "no code\nneeded :)", "looks like\n$10K\n(it's not)", "90 days\nto love it\nor return it"][V.index(h)], True)
        pk = g2.packs_de(h)
        if len(pk) >= 2:
            add("cores", f"C7_P1_cores_{N[h]}", g2.f_cores, h, pk[:6])
        outras = [k for k in g2.CLASS["estudio"] + g2.CLASS["pulso"] + pk[1:] if k.startswith(h + "_")]
        if outras:
            add("detalhes", f"C3_P3_detalhes_{N[h]}", g2.f_detalhes, h, (outras * 3)[:3])
        add("catalogo", f"C9_todas_catalogo-bogo_{N[h]}", g1.t_catalogo, h)
    tweets = {"vittorio": "Unpopular opinion: you don't need to spend $5,000 to look like you did.",
              "pelvini-dominante": "Two-tone. Chronograph. Second one free. You're welcome.",
              "pelvini-milano": "The green dial everyone keeps asking about is back in stock.",
              "pelvini-opulent": "Buy one watch. Get a second one free. That's it. That's the tweet.",
              "pelvini-maretti-1": "Quiet luxury doesn't need a logo on the dial."}
    for h, t in tweets.items():
        add("tweet", f"C2_P1_tweet_{N[h]}", g2.f_tweet, h, t)
    for a, b, la, lb, t in [("vittorio", "pelvini-dominante", "CLASSIC", "BOLD", "Which one are you?"),
                            ("pelvini-milano", "pelvini-opulent", "GREEN", "BLUE", "Green or blue?"),
                            ("pelvini-maretti-1", "pelvini-milano", "GREY", "GREEN", "Which one are you?"),
                            ("pelvini-dominante", "pelvini-opulent", "CHRONO", "CLEAN", "Which one are you?")]:
        add("qual-voce", f"C7_P1_qual-voce_{la.lower()}-{lb.lower()}", g2.f_qual_voce, a, b, la, lb, t)
    add("ranking", "C2_P1_ranking_top5", g2.f_ranking, ["vittorio", "pelvini-dominante", "pelvini-milano", "pelvini-opulent"], "Our 4 best-selling watches right now")
    add("maleta", "C8_P2_maleta_bestsellers", g2.f_maleta, V * 3, "OUR BEST SELLERS. 2ND FREE.")
    add("his-hers", "C1_P2_his-hers_vittorio-clovera", g1.t_his_hers, "vittorio", "pelvini-clovera")
    add("his-hers", "C1_P2_his-hers_milano-serafina", g1.t_his_hers, "pelvini-milano", "pelvini-serafina")
    add("his-hers", "C1_P2_his-hers_opulent-lunetta", g1.t_his_hers, "pelvini-opulent", "pelvini-lunetta")
    add("imessage", "C1_P2_imessage_pai-dominante", g2.f_imessage, "pelvini-dominante",
        [("eu", "Dad, did the package arrive?"), ("img", ""), ("ela", "It's beautiful. You shouldn't have"), ("eu", "It was buy 1 get 1. Mine matches yours")])
    add("imessage", "C1_P2_imessage_irmao-milano", g2.f_imessage, "pelvini-milano",
        [("eu", "Happy birthday bro. Check the door"), ("img", ""), ("ela", "No way. That green dial??"), ("eu", "Got one for me too. Second was free")])
    for f in VIDA:
        b = f[:-4]
        h = b.rsplit("_", 1)[0]
        add("split", f"C7_P1_split_{b}", g2.f_split, f, h)
        add("pulso-frase", f"C2_P1_pulso-frase_{b}", g2.f_pulso_frase, f, "The watch people ask about." if "vittorio" in f else "Looks expensive. Isn't.")
        add("vida-bogo", f"C1_P2_vida-bogo_{b}", g2.f_vida_bogo, f)
        add("postit", f"C8_P2_postit_{b}", g2.f_postit, f, "2nd watch\nFREE\nends tonight" if "vittorio" in f else "one for you\none for them")
    for f in ESTUDIO:
        add("estudio", f"C7_P1_estudio_{f[:-4]}", g2.f_estudio, f)
    return p


if __name__ == "__main__":
    feitos, erros = [], []
    for fam, nome, fn, args in plano():
        os.makedirs(os.path.join(SAIDA, fam), exist_ok=True)
        fmts = ["1x1"] if fam == "catalogo" else list(g1.FORMATOS)
        for fmt in fmts:
            out = os.path.join(SAIDA, fam, f"{nome}_{fmt}.jpg")
            try:
                fn(fmt, *args).convert("RGB").save(out, quality=92)
                feitos.append(out)
            except Exception as e:
                erros.append(f"{nome} {fmt}: {e.__class__.__name__}: {e}")
    print(len(feitos), "imagens |", len(erros), "erros")
    for e in erros:
        print("  ", e)
    q = sorted(f for f in feitos if f.endswith("_1x1.jpg"))
    for i in range(0, len(q), 48):
        g2.folha(q[i:i + 48], os.path.join(SAIDA, f"_revisao_1x1_{i // 48 + 1:02d}.jpg"))
