# -*- coding: utf-8 -*-
import json, subprocess
from pathlib import Path
AQ = Path(__file__).resolve().parent
I = json.load(open(AQ / "audio" / "itens.json", encoding="utf-8"))
VID = {"PB01": "77f5a7a9d7607469be3326745377f73d", "P03B": "47e492ad0d331e8ef7c3190270cabf0a", "P04B": "c3a5336e48244f42d6538b77bdc649a0",
       "P05B": "6ae51a64a62dab5d887ee38be168e8c7", "P07B": "19355b2d96dd824123ce6dfe8457402b"}
# QA visual (qa/<id>_pausas.jpg): pausa com dentes/boca aberta = grave
NOTAS = {"PB01": {1.08: "dentes à mostra na pausa depois de 'suerte.'", 3.05: "dentes à mostra / olhos semicerrados na pausa"},
         "P04B": {0.92: "dentes à mostra na pausa depois de 'atención:'"},
         "P05B": {4.84: "dentes à mostra na pausa"},
         "P07B": {3.01: "dentes à mostra na pausa"}}
INI = {"PB01": "quadro 0 com olhos fechados e lábios em bico (entrada do HeyGen)", "P03B": "quadro 0 já com boca aberta/dentes",
       "P07B": "quadro 0 com olhos fechados e lábios em bico (entrada do HeyGen)"}
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
CUSTO_HG = 2.9
out = {"nota": "tempos em s relativos ao início de cada arquivo; palavras = alinhamento ElevenLabs remapeado após encurtar pausas (sacerdote ≤0,25 s; AV01 voz off pausas naturais ≤0,45 s).",
       "padre": {"voz": "Zkg9LlmGNlBWLgWjzTnu (Pa Gabriel) est 0.5 / estilo 0.25 / vel 1.06, eleven_multilingual_v2", "imagem": "img/padre_gpt.png (mesma de v3/_trabalho/padre)",
                 "formato_takes": "720x1280, 25 fps, H.264 da HeyGen copiado sem recodificar (sem etiqueta de cor, igual aos takes atuais), áudio = wav recortado (AAC 48 kHz). Sem moldura EN VIVO.",
                 "heygen": "Avatar IV (create_video_from_image) 720p, 9:16, expressiveness low, áudio enviado como asset"},
       "aurelio_voz": "VXZKNah1ssrzM8c81OiY (Santiago) est 0.45 / estilo 0.3 / vel 1.06 (falas.json v1 L05)",
       "itens": []}
for k, it in I.items():
    av = it["avatar"]; arq = f"take_{k}.mp4" if av else it["arquivo"]; d = round(dur(AQ / arq), 3)
    ruins = []
    if av:
        p0 = it["pausas"][0][1]
        ruins.append(dict(ini=0.0, fim=max(p0, 0.12) if k in INI else p0, motivo=INI.get(k, "início antes da 1ª palavra"), grave=k in INI))
        for a, b in it["pausas"][1:-1]:
            m = next((v for x, v in NOTAS.get(k, {}).items() if abs(x - a) < 0.1), None)
            ruins.append(dict(ini=a, fim=b, motivo=m or "pausa interna encurtada (≤0,25 s): boca fechada no QA, ok", grave=bool(m)))
        ruins.append(dict(ini=it["pausas"][-1][0], fim=d, motivo="cauda após a última palavra (boca fechada, ok)", grave=False))
    wt = AQ / "qa" / f"{k}_take_whisper.json"; ww = AQ / "qa" / f"{k}_wav_whisper.json"
    w = json.load(open(wt if wt.exists() else ww, encoding="utf-8"))
    out["itens"].append(dict(id=k, bloco=k, tipo="take_avatar" if av else "narracao_off", arquivo=arq, texto=it["texto"], duracao=d,
                             fps=25 if av else None, palavras=it["palavras"], intervalos_ruins=ruins,
                             heygen_video_id=VID.get(k), creditos_heygen_est=round(d * CUSTO_HG, 1) if av else 0,
                             custo_tts_usd=round(len(it["texto"]) / 1000 * 0.165, 4),
                             whisper=w["whisper"], whisper_ok=(not w["dif"]) or k == "P03B", whisper_dif=w["dif"] or None, whisper_obs="'doce' transcrito como '12' (só normalização)" if k == "P03B" else None))
B = json.load(open(AQ / "broll" / "broll.json", encoding="utf-8"))
for b in B:
    p = AQ / b["arquivo"]
    b["duracao"] = round(dur(p), 3) if p.exists() else None
    b.setdefault("fps", 30); b.setdefault("intervalos_ruins", [])
    out["itens"].append(b)
json.dump(out, open(AQ / "manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for x in out["itens"]: print(x["id"], x["arquivo"], x["duracao"], len(x["intervalos_ruins"]), x.get("whisper_ok"))
