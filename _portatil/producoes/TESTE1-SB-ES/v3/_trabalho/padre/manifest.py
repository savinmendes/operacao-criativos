# -*- coding: utf-8 -*-
import json, subprocess
from pathlib import Path
AQ = Path(__file__).resolve().parent
I = json.load(open(AQ / "audio" / "itens.json", encoding="utf-8"))
VID = {"P01": "1e2081ac15985647d6c812fad96a8f97", "P02": "99207ebfbcf89e77b1a7e8192aac696b", "P03": "ea6606c47a280fc70567e04ecdf86614",
       "P04": "5fd990589b712a4f0b1ab1e7fb33e70c", "P05": "0d7beeaa7d43b900c3be225f322f7f55", "P06": "b5b197a15d9b4896a2a7a58ac8961d09",
       "P07": "0a1d43428c77697663107e2256b95ed2", "P08": "4de058bead0ea4055a1cdfc2aeb097b9"}
NOTAS = {"P03": {3.02: "boca aberta na pausa (antecipa 'del Grimorio')"},
         "P04": {0.91: "dentes à mostra na pausa depois de 'atención:'", 3.33: "dentes à mostra na pausa"},
         "P05": {1.75: "boca aberta/dentes na pausa", 6.62: "boca aberta na pausa"},
         "P06": {3.03: "boca aberta na pausa", 5.85: "boca aberta/dentes na pausa"}}
INI_RUIM = {"P03", "P06", "P07", "P08", "P05"}  # quadro 0 já com boca aberta / olhos fechando
EXTRA = {"P06": [dict(ini=0.16, fim=1.36, motivo="COLAR: mão passa na frente e encobre/funde com a medalha", grave=True),
                 dict(ini=3.1, fim=3.4, motivo="COLAR: mão cobre a medalha, corrente salta", grave=True),
                 dict(ini=5.3, fim=5.5, motivo="COLAR: medalha fica translúcida/fantasma", grave=True),
                 dict(ini=7.3, fim=7.5, motivo="COLAR: medalha translúcida/escura", grave=True),
                 dict(ini=0.0, fim=8.16, motivo="COLAR: mãos mexem o take inteiro (inquietas); rosto OK. Usar enquadramento só do rosto (cortar acima de y≈700 no quadro 720x1280) ou cobrir com insert_P06_colar_kling.mp4", grave=False)]}
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
CUSTO_HG = 2.9  # créditos/s 720p (medido na v2)
out = {"personagem": "P. Andrés Molina (sacerdote da live)", "voz": "Zkg9LlmGNlBWLgWjzTnu (Pa Gabriel) est 0.5 / estilo 0.25 / vel 1.06, eleven_multilingual_v2",
       "imagens": {"base": "img/padre_gpt.png (cópia da v2, aprovada)", "P06": "img/padre_colar_gpt.png (GPT Image 2 1k, US$ 0,273)",
                   "insert": "img/maos_colar_close.png"},
       "formato_takes": "720x1280, 25 fps, H.264 da HeyGen copiado sem recodificar (sem etiqueta de cor), áudio = wav recortado do ElevenLabs (AAC 48 kHz). Sem moldura EN VIVO (a montagem aplica).",
       "nota": "tempos em s relativos ao início de cada arquivo; palavras = alinhamento ElevenLabs remapeado após encurtar pausas. Números: V03 diz 'novecientos dieciocho', V05 'cuatrocientos noventa y siete' (legenda pode usar 918/497). O01 não está aqui: reaproveitar _trabalho/voz L09 + L09b da v1.",
       "itens": []}
for k, it in I.items():
    av = it["avatar"]; arq = f"take_{k}.mp4" if av else it["arquivo"]; d = round(dur(AQ / arq), 3)
    ruins = []
    if av:
        p0 = it["pausas"][0][1]
        ruins.append(dict(ini=0.0, fim=max(p0, 0.1) if k in INI_RUIM else p0,
                          motivo="quadro 0 já com boca aberta/olhos fechando (entrada do HeyGen)" if k in INI_RUIM else "início antes da 1ª palavra", grave=k in INI_RUIM))
        for a, b in it["pausas"][1:-1]:
            m = next((v for x, v in NOTAS.get(k, {}).items() if abs(x - a) < 0.1), None)
            ruins.append(dict(ini=a, fim=b, motivo=m or "pausa interna encurtada (≤0,25 s): avatar pode articular", grave=bool(m)))
        ruins.append(dict(ini=it["pausas"][-1][0], fim=d, motivo="cauda após a última palavra (boca fechada, ok)", grave=False))
        ruins += EXTRA.get(k, [])
    wf = AQ / "qa" / f"{k}_{'take' if av else 'wav'}_whisper.json"
    w = json.load(open(wf, encoding="utf-8"))
    out["itens"].append(dict(id=k, bloco=k, tipo="take_avatar" if av else "narracao_off", arquivo=arq, texto=it["texto"], duracao=d,
                             fps=25 if av else None, palavras=it["palavras"], intervalos_ruins=ruins,
                             heygen_video_id=VID.get(k), creditos_heygen_est=round(d * CUSTO_HG, 1) if av else 0,
                             custo_tts_usd=round(len(it.get("tts") or it["texto"]) / 1000 * 0.165, 4),
                             whisper=w["whisper"], whisper_ok=not w["dif"] or k == "V09",
                             whisper_obs="'siete' transcrito como '7' (só normalização)" if k == "V09" else None))
out["itens"].append(dict(id="P06_insert", bloco="P06", tipo="insert_sem_fala", arquivo="insert_P06_colar_kling.mp4",
                         texto=None, duracao=round(dur(AQ / "insert_P06_colar_kling.mp4"), 3) if (AQ / "insert_P06_colar_kling.mp4").exists() else None,
                         nota="close das mãos do padre segurando a medalha; Kling 2.5 Turbo Pro i2v 5 s; cobrir intervalos COLAR do take_P06", intervalos_ruins=[]))
json.dump(out, open(AQ / "manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for x in out["itens"]: print(x["id"], x["arquivo"], x["duracao"], len(x["intervalos_ruins"]))
