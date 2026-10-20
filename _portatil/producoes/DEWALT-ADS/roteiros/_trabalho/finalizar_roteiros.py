# -*- coding: utf-8 -*-
"""Junta fonte.json + tempos reais da voz (relatorio_voz.json) -> ../roteiros.json e ../roteiros.md"""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
F = json.loads((AQUI / "fonte.json").read_text(encoding="utf-8"))
REL = json.loads((RAIZ / "voz" / "_trabalho" / "relatorio_voz.json").read_text(encoding="utf-8"))
WH = json.loads((RAIZ / "voz" / "_trabalho" / "whisper_check.json").read_text(encoding="utf-8"))
IDX = {t["arquivo"]: t for t in json.loads((RAIZ / "banco" / "indice.json").read_text(encoding="utf-8"))["takes"]}
ORIGW = json.loads((RAIZ / "voz" / "_trabalho" / "palavras_originais.json").read_text(encoding="utf-8"))

comum = {
    "produto": "DeWalt DCD7781D2-B2 · kit taladro percutor/atornillador 20V MAX brushless + 2 baterías 2Ah + cargador + maleta",
    "mercado": "COD Chile · español chileno", "tema": "Pre Black Friday (sin precio, sin escasez inventada)",
    "cta": "Pídelo hoy y pagas recién cuando te llegue.",
    "ficha": str(RAIZ / "ficha_dcd7781.json"),
    "regras": ["Nada de preço/desconto em valor", "Sem 65 Nm, 29.750 gpm, 0-500 rpm, capacidade de furo em mm",
               "'17% más eficiente' só com 'que un motor con carbones, según DeWalt'",
               "Legenda pelo roteiro (texto) com o alinhamento do TTS; música -32 LUFS", "Velocidade TTS <= 1,1x"],
    "pendencias": ["Confirmar com o fornecedor que o kit é o D2-B2 (2 baterias + maleta dura), não o D1 com bolsa de lona.",
                   "Base 37: cobrir os números '38mm'/'13mm' dos cards de perfuração (capacidade sem fonte oficial).",
                   "Ouvir a pronúncia de 'DeWalt' (whisper ouviu 'de Walt'/'de wall', aceito como 'de-uólt')."],
}


def orig_span(ad, a, b):
    ws = [w for w in ORIGW.get(ad, []) if a is not None and a - 0.1 <= w[0] < b - 0.05]
    return (round(ws[0][0], 2), round(ws[-1][1], 2)) if ws else (None, None)


out = {"comum": comum, "voz_maestro": F["voz_maestro"], "traducoes": [], "corpos": [], "ganchos": []}
for t in F["traducoes"]:
    r = REL[t["id"]]
    segs = []
    for s, rs in zip(t["segmentos"], r["segmentos"]):
        oa, ob = orig_span(t["ad_origem"], s["orig_ini"], s["orig_fim"])
        d = {"texto": s["texto"], "titulo_tela": s.get("titulo"), "amarelo": s["amarelo"],
             "ini": rs["inicio"], "fim": rs["fim"], "dur": rs["dur"],
             "orig_fala": [oa, ob] if oa is not None else None}
        if oa is not None:
            d["razao_vs_original"] = round(rs["dur"] / (ob - oa), 2)
        if s.get("extensao"):
            d["extensao_fim_congelado"] = True
        if s.get("take_visual"):
            d["visual"] = s["take_visual"]
        segs.append(d)
    out["traducoes"].append({"id": t["id"], "nome": t["nome"], "base": str(RAIZ / t["base"]), "duracao_base": t["duracao_base"],
                             "voz": t["voz"], "audio": str(RAIZ / "voz" / f"{t['id']}.mp3"),
                             "alinhamento": str(RAIZ / "voz" / f"{t['id']}.alinhamento.json"),
                             "duracao_audio": r["duracao"], "fala_fim": r["fala_fim"],
                             "observacoes": t["observacoes"], "segmentos": segs})
for c in F["corpos"]:
    r = REL[c["id"]]
    segs = []
    for s, rs in zip(c["segmentos"], r["segmentos"]):
        tk = sum(IDX[x]["duracao_s"] for x in s["takes"])
        d = {"texto": s["texto"], "takes": s["takes"], "takes_dur": round(tk, 2), "amarelo": s["amarelo"],
             "ini": rs["inicio"], "fim": rs["fim"], "dur": rs["dur"]}
        if s.get("titulo"):
            d["titulo_tela"] = s["titulo"]
        if s.get("rodape"):
            d["rodape"] = s["rodape"]
        if tk < rs["dur"]:
            d["atencao"] = "takes mais curtos que a frase: esticar o último take (slow 0,85x) ou somar outro take da mesma ação"
        segs.append(d)
    out["corpos"].append({"id": c["id"], "nome": c["nome"], "voz": c["voz"], "audio": str(RAIZ / "voz" / f"{c['id']}.mp3"),
                          "alinhamento": str(RAIZ / "voz" / f"{c['id']}.alinhamento.json"),
                          "duracao_audio": r["duracao"], "fala_fim": r["fala_fim"], "segmentos": segs})
for g in F["ganchos"]:
    r = REL[g["id"]]
    d = {k: g[k] for k in ("id", "inspiracao", "texto", "titulo", "amarelo", "take", "por_que_take", "par_sugerido") if k in g}
    d["palavras"] = len(g["texto"].split())
    d.update({"voz": F["voz_maestro"], "audio": str(RAIZ / "voz" / f"{g['id']}.mp3"),
              "alinhamento": str(RAIZ / "voz" / f"{g['id']}.alinhamento.json"), "fala_s": r["fala_fim"],
              "take_dur": IDX[g["take"]]["duracao_s"]})
    if g.get("nota"):
        d["nota"] = g["nota"]
    out["ganchos"].append(d)

(AQUI.parent / "roteiros.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------- markdown ----------
L = ["# Roteiros DCD7781 · COD Chile · Pre Black Friday", "",
     f"- **Produto:** {comum['produto']}", f"- **Tema:** {comum['tema']}", f"- **CTA:** \"{comum['cta']}\"",
     f"- **Voz maestro (corpos, ganchos e AD 38):** {F['voz_maestro']['nome']} · `{F['voz_maestro']['id']}`",
     "- **Áudios:** `voz/<id>.mp3` + `voz/<id>.alinhamento.json` (formato ElevenLabs, tempos já no tempo do vídeo base)",
     "- Palavras em **negrito** = amarelo na legenda.", "", "## Pendências", ""]
L += [f"- {p}" for p in comum["pendencias"]] + [""]


def amar(txt, ws):
    for w in sorted(ws, key=len, reverse=True):
        i = txt.lower().find(w.lower())
        if i >= 0 and "**" not in txt[max(0, i - 2):i + len(w) + 2]:
            txt = txt[:i] + "**" + txt[i:i + len(w)] + "**" + txt[i + len(w):]
    return txt


L += ["## A) Traduções", ""]
for t in out["traducoes"]:
    L += [f"### {t['nome']}", "", f"- Base: `{t['base']}` ({t['duracao_base']} s) · voz: {t['voz']['nome']} `{t['voz']['id']}`",
          f"- Áudio: {t['duracao_audio']} s (fala até {t['fala_fim']} s)"]
    L += [f"- {o}" for o in t["observacoes"]]
    L += ["", "| Tempo | Fala (ES-CL) | Título na tela | Original (fala) | Razão |", "|---|---|---|---|---|"]
    for s in t["segmentos"]:
        o = f"{s['orig_fala'][0]}–{s['orig_fala'][1]}" if s.get("orig_fala") else ("extensão (fim congelado)" if s.get("extensao_fim_congelado") else "—")
        L.append(f"| {s['ini']:.2f}–{s['fim']:.2f} | {amar(s['texto'], s['amarelo'])} | {s.get('titulo_tela') or ''} | {o} | {s.get('razao_vs_original', '')} |")
    L.append("")
L += ["## B) Corpos novos (banco de takes)", ""]
for c in out["corpos"]:
    L += [f"### {c['nome']}", "", f"- Voz: {c['voz']['nome']} `{c['voz']['id']}` · áudio {c['duracao_audio']} s", "",
          "| Tempo | Fala | Take(s) do banco | Título |", "|---|---|---|---|"]
    for s in c["segmentos"]:
        tit = (s.get("titulo_tela") or "") + (f" · rodapé: {s['rodape']}" if s.get("rodape") else "")
        at = " (!)" if s.get("atencao") else ""
        L.append(f"| {s['ini']:.2f}–{s['fim']:.2f} | {amar(s['texto'], s['amarelo'])} | {', '.join(s['takes'])} ({s['takes_dur']} s){at} | {tit} |")
    L.append("")
L += ["(!) = take(s) mais curto(s) que a frase: esticar o último take (0,85x) ou somar outro take da mesma ação.", "",
      "## C) Ganchos (voz maestro)", "", "| Gancho | Fala | Título grande | Take de abertura | Fala (s) | Par sugerido |", "|---|---|---|---|---|---|"]
for g in out["ganchos"]:
    L.append(f"| {g['id']} ({g['inspiracao']}) | {amar(g['texto'], g['amarelo'])} ({g['palavras']} palavras) | {g['titulo']} | "
             f"{g['take']}: {g['por_que_take']} | {g['fala_s']} | {g['par_sugerido']} |")
L += [""] + [f"- {g['id']}: {g['nota']}" for g in out["ganchos"] if g.get("nota")]
L += ["", "## Conferência da voz", "",
      "- Whisper medium (es) em todos os áudios: sem palavra errada. As diferenças que sobraram são de fronteira entre frases ou grafia ('2x3' = 'dos por tres', 'Preblack').",
      "- Regravados: gancho 2 ('débil'), gancho 3, gancho 4 ('Pre'), gancho 5 ('Dos'), corpo 1 ('DeWalt', 'luz LED'), corpo 2 ('DeWalt dice', 'pagas'), AD 37 ('en la mano', 'revoluciones'), AD 21 e AD 38 ('DeWalt').",
      "- Todas as vozes em velocidade 1,0x (gancho 5 em 1,08x)."]
(AQUI.parent / "roteiros.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("ok")
