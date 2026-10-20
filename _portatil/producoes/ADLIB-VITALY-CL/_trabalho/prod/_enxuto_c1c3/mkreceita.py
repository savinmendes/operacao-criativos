# -*- coding: utf-8 -*-
import json, sys, subprocess
from pathlib import Path
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas")); import legenda as LEG
AQ = Path(__file__).parent
OUT = Path(r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\LYMPHORIA-ENXUTO")
CFG = {
 "c1a": ("LYM-CL_C1_trabajadora-de-pie_avatar-ugc_a", "12 HORAS DE PIE"),
 "c1b": ("LYM-CL_C1_trabajadora-de-pie_pov-voz-off_b", "¿Llegas con los tobillos hinchados?"),
 "c3a": ("LYM-CL_C3_jubilada-60_avatar-ugc_a", "¡Volví a usar mi anillo!"),
 "c3b": ("LYM-CL_C3_jubilada-60_testimonio-off_b", "¿Tus anillos ya no entran?"),
}
CH = ["hinchados", "hinchazón", "lymphoria", "natural", "miel", "livianas", "anillos", "anillo", "zapatos", "compre", "dos", "gratis", "recibir"]
for c in sys.argv[1:]:
    nome, man = CFG[c]
    ali = str(AQ / c / "narr.alinhamento.json")
    pal = LEG.palavras_por_alinhamento(ali, 0)
    tp = next(a for w, a, *_ in pal if LEG._limpa(w).startswith("pagas"))
    rec = {"saida": str(OUT / (nome + ".mp4")), "estilo": "drop", "corpo": str(AQ / c / "corpo.mp4"),
           "legenda": {"fonte": f"alinhamento:{ali}", "chaves": CH},
           "manchete": {"texto": man, "y": 150, "ate": 3.0, "px": 78},
           "selo": {"linhas": ["", "PAGO CONTRA", "ENTREGA", ""], "escala": 0.55, "x": 331, "y": 1330, "desde": round(tp, 2)},
           "cta": {"palavra": "toca"}, "limite_mb": 30, "resolucao": "720"}
    (AQ / c / "receita.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(c, "selo desde", round(tp, 2))
