import json, sys, subprocess
from pathlib import Path
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas")); import legenda as LEG
pasta, parte1, fim, saida = map(Path, sys.argv[1:5])
narr = fim.parent / ("narr_fim.mp3")
ali = str(narr.with_suffix("")) + ".alinhamento.json"
pal = LEG.palavras_por_alinhamento(ali, 0)
te = next(a for w, a, *_ in pal if LEG._limpa(w).startswith("env"))
d1 = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(parte1)],capture_output=True,text=True).stdout)
rec = {"saida": str(saida), "estilo": "drop", "corpo": str(fim),
       "hook": {"tipo": "antes", "video": str(parte1)},
       "legenda": {"fonte": f"alinhamento:{ali}", "chaves": ["lymphoria", "compre", "dos", "gratis", "recibir", "noventa"]},
       "selo": {"linhas": ["ENVÍO GRATIS A DOMICILIO", "PAGO CONTRA", "ENTREGA", "¡PAGAS AL RECIBIR!"], "x": 160, "y": 1225, "desde": round(d1 + te, 2)},
       "cta": {"palavra": "toca"}, "limite_mb": 30, "resolucao": "720"}
(pasta / "receita_final.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print(pasta / "receita_final.json")
