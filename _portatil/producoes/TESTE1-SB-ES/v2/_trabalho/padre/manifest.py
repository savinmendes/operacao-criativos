# -*- coding: utf-8 -*-
import json, subprocess
from pathlib import Path
AQ = Path(__file__).resolve().parent
I = json.load(open(AQ / "audio" / "itens.json", encoding="utf-8"))
VID = {"P1": "759d2989f258aea8c7b0b41aca36524a", "P2": "4ead3908262e586fe2dfe5224f4068a7", "P3": "2e2bd70a5eb50216dc88b790ea367e40",
       "P4": "84bc39740f12dadba30f6b214c007189", "P5": "647feb0ef2cdb5dfd07788930ac21499", "P6": "6b5e7f5903ff630c57f6915c1f2d6498"}
NOTAS = {"P1": {(1.6, 1.85): "dentes à mostra na pausa (leve)"}, "P5": {(3.74, 3.99): "boca abre antes de 'durante' (antecipa)", (5.67, 5.92): "dentes/sorriso na pausa"},
         "P6": {(5.0, 5.25): "dentes/sorriso na pausa (4,96-5,25)"}}
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
out = {"personagem": "P. Andrés Molina (padre da live)", "imagem": "padre_gpt.png", "voz": "Zkg9LlmGNlBWLgWjzTnu",
       "formato_takes": "720x1280, 25 fps, H.264 sem etiqueta de cor (saída HeyGen copiada sem recodificar), áudio = wav recortado (AAC 48 kHz)",
       "nota": "tempos em s relativos ao início de cada arquivo; palavras = alinhamento ElevenLabs remapeado após encurtar pausas (whisper do take confere o texto)",
       "itens": []}
for k, it in I.items():
    av = it["avatar"]; arq = f"take_{k}.mp4" if av else it["arquivo"]
    ruins = []
    if av:
        d = dur(AQ / arq)
        if it["pausas"][0][1] > 0.04: ruins.append(dict(ini=0.0, fim=it["pausas"][0][1], motivo="início antes da 1ª palavra (boca parada/entrando)"))
        for a, b in it["pausas"][1:-1]:
            m = next((v for (x, y), v in NOTAS.get(k, {}).items() if abs(x - a) < 0.1), None)
            ruins.append(dict(ini=a, fim=b, motivo=m or "pausa interna encurtada (≤0,25 s): avatar pode sorrir/articular; cobrir se aparecer", grave=bool(m)))
        ruins.append(dict(ini=it["pausas"][-1][0], fim=round(d, 3), motivo="cauda após a última palavra"))
    w = json.load(open(AQ / "qa" / f"{k}_whisper.json", encoding="utf-8")) if av else None
    out["itens"].append(dict(id=k, tipo="take_avatar" if av else "narracao_off", arquivo=arq, texto=it["texto"], duracao=round(dur(AQ / arq), 3),
                             fonte_audio=f"_trabalho/voz/{'c/' + it['fonte'] + '.wav' if it['fonte'] != 'P6' else 'TTS novo (padre/audio/P6_tts.mp3)'}",
                             palavras=it["palavras"], intervalos_ruins=ruins, heygen_video_id=VID.get(k),
                             whisper_take=" ".join(x["w"] for x in w) if w else None))
json.dump(out, open(AQ / "manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for x in out["itens"]: print(x["id"], x["arquivo"], x["duracao"], len(x["intervalos_ruins"]))
