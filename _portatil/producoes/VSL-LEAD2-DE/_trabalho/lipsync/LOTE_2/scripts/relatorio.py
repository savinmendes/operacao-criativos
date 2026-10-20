# -*- coding: utf-8 -*-
import json, re
from pathlib import Path
R = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\lipsync\LOTE_2")
P = json.load(open(R / "plano.json")); f = json.load(open(R / "_tmp" / "fin.json", encoding="utf-8"))
e = json.load(open(R / "_tmp" / "ext.json", encoding="utf-8")); b = json.load(open(R / "batch.json"))
BROLL_VISUAL = {}  # nenhum override: reprovados do checador vao para b-roll
NOTAS = {
 "L100": "pausa interna 8,68-9,09 s (6 q): indice no trecho 1,05, com as bordas 0,60; a olho a boca fecha. Se quiser 100% seguro, jump cut em 8,68 s.",
 "L119": "ultimo quadro (173) ja e o plano seguinte (corte da fonte 1 quadro antes da borda); indice 0,80 com 17 q de pausa.",
 "L091": "comeca dentro de uma fusao (crossfade) do original; boca articula a olho, mas sem pausa e corr. com o DE 0,14.",
 "L103": "termina dentro de uma fusao do original; boca articula a olho, sem pausa, corr. DE 0,15 < corr. ES 0,39.",
 "L110": "1o job falhou (No speaker is detected); reenvio r1 ok mas boca nao segue o DE (corr. 0,03 x ES 0,36, sem pausa). Termina dentro de uma fusao do original.",
 "L139": "checador no trecho: REPROVADO por correlacao (0,11 = ES 0,11, sem pausa); com as bordas: AVISO; a olho a boca articula. Conferir na montagem.",
 "L125": "trecho de 2,27 s enviado com padding de quadro congelado ate 3 s; saida cortada nos 68 quadros.",
}
def g(t, p):
    m = re.search(p, t or ""); return m.group(1) if m else None
out = []
for x in P:
    i = x["id"]; a = f.get(i, {}); c = e.get(i, {})
    if "checar" not in a:
        out.append({"id": i, "job_id": b["jobs"][i], "indice": None, "status": "pendente", "obs": a.get("erro", "sem saida do HeyGen")}); continue
    vs = [v for v in (a.get("checar"), c.get("checar")) if v]
    idx = [v for v in (a.get("indice"), c.get("indice")) if v is not None]
    if c.get("checar") == "APROVADO" or (a.get("checar") == "APROVADO" and c.get("checar") != "REPROVADO"):
        st = "ok"
    elif (c.get("checar") or a.get("checar")) == "REPROVADO" or (a.get("checar") == "REPROVADO" and not c):
        st = "usar_broll"
    else:
        st = "aviso"
    ind = c.get("indice") if c.get("indice") is not None else a.get("indice")
    obs = []
    if ind is None: obs.append("sem pausa >= 8 quadros na voz DE (nem nas bordas): indice nao calculavel; boca mudou %s%%, corr. DE %s x ES %s" % (g(a["log"], r"mudou em (\d+)%"), g(a["log"], r"corr. novo ([-0-9.]+)"), g(a["log"], r"corr. original ([-0-9.]+)")))
    if a.get("indice") is not None and c.get("indice") is not None and abs(a["indice"] - c["indice"]) > 0.05:
        obs.append(f"indice no trecho {a['indice']} / com 0,6 s dos vizinhos {c['indice']}")
    if i in NOTAS: obs.append(NOTAS[i])
    if a.get("nota"): obs.append(a["nota"])
    out.append({"id": i, "cena": x["cena"], "job_id": b["jobs"][i], "indice": ind, "status": st,
                "checar_trecho": a.get("checar"), "checar_com_bordas": c.get("checar"), "quadros": a.get("n_quadros"),
                "obs": " | ".join(obs)})
rel = {"lote": 2, "ids": "L084-L153", "batch_id": b["batch_id"], "reenvios": b["reenvios"],
       "criterio": "checar_lipsync.py do kit no recorte enviado (saida HeyGen x entrada ES esticada, audio DE) e, nos planos medios, de novo com 0,6 s dos vizinhos (as pausas DE ficam nas bordas dos cortes). ok = indice <= 0,6; aviso = sem pausa mensuravel ou 0,6-0,9 com poucos quadros; usar_broll = REPROVADO.",
       "saida": "<id>.mp4 = so video 720x960 30 fps, N quadros da timeline nova; YUV sem conversao, etiqueta bt709/tv via h264_metadata; pulpito = boca+queixo do recorte 2x colados (elipse suave).",
       "trechos": out}
json.dump(rel, open(R / "relatorio.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(t["status"] for t in out)); print([t["id"] for t in out if t["status"] == "usar_broll"])
