# -*- coding: utf-8 -*-
import json
from pathlib import Path
AQ = Path(__file__).resolve().parent
P = json.loads((AQ / "audio" / "partes.json").read_text(encoding="utf-8"))
wh = lambda f: json.loads((AQ / "qa" / f).read_text(encoding="utf-8"))
T = {
 "A": dict(arquivo="take_A_L05a.mp4", texto="Sí, me pasó a mí. Y lo peor no fue el golpe… fue llegar a casa y sentir que Dios se había olvidado de mí.",
           whisper="L05a_whisper.json", heygen_id="fce8a54d49eda970ba22e56067724ff3",
           ruins=[[1.56, 1.86, "pausa entre 'mí.' e 'Y': boca aberta parada mostrando dentes (não é sorriso; leve)"]]),
 "B": dict(arquivo="take_B_L05b.mp4", texto="Hasta que aprendí la oración completa de San Benito y la hice después de aquella situación. Al día siguiente, mi carrito se llenó de clientes. No lo podía creer.",
           whisper="L05b_whisper.json", heygen_id="b6a468248b0535e2af943e2b68c093d4",
           ruins=[[0.0, 0.16, "início em silêncio com boca aberta (dentes)"],
                  [3.50, 3.80, "pausa após 'San Benito': boca aberta parada com dentes"],
                  [6.28, 6.60, "pausa após 'situación.': boca aberta parada com dentes"]]),
 "C": dict(arquivo="take_C_L06.mp4", texto="¿Podemos poner aquí la transmisión en vivo que enseña esta oración tan poderosa?",
           whisper="L06_whisper.json", heygen_id="6d8f3e5dd0dad9614ed96223ab6e9a95", ruins=[]),
}
out = {"personagem": "Don Aurelio (entrevista)", "voz": "Santiago VXZKNah1ssrzM8c81OiY (ElevenLabs, ja gerada)",
       "imagem": "imagens/aurelio_gpt.png (GPT Image 2 i2i, 1k, 4:5, 896x1120) a partir de prints/win_25.5.png (base_limpa LaMa, janela 720x840)",
       "heygen": "create_video_from_image (Avatar IV), 720p, 4:5 -> 720x900, 25 fps, expressiveness low, audio enviado como asset (wav)",
       "nota_tempo": "audio do take == audio enviado (mesma duracao); tempos 'palavras' = alinhamento ElevenLabs remapeado apos encurtar pausas; 'palavras_whisper' = faster-whisper small no take",
       "takes": [], "audio_separado": {
           "arquivo": "narr_L05_rezaba.wav", "texto": "Rezaba todos los días y nada cambiaba.", "uso": "narracao sobre b-roll de homem rezando (entre take A e take B)",
           "dur": P["NARR"]["dur"], "palavras": P["NARR"]["palavras"], "palavras_whisper": wh("narr_whisper.json"),
           "corte_fonte_L05": P["NARR"]["corte_fonte"]}}
for k, v in T.items():
    p = P[{"A": "A", "B": "B", "C": "C"}[k]]
    out["takes"].append(dict(id=k, arquivo=v["arquivo"], texto=v["texto"], audio_usado=p["arquivo"], fonte=p["fonte"], corte_fonte=p["corte_fonte"],
        pausas_encurtadas_rel=p["removidos_rel"], dur=p["dur"], fps=25, resolucao="720x900", heygen_video_id=v["heygen_id"],
        palavras=p["palavras"], palavras_whisper=wh(v["whisper"]), pausas_no_audio=p["pausas"],
        intervalos_ruins=[dict(ini=a, fim=b, motivo=m) for a, b, m in v["ruins"]]))
out["ordem_montagem"] = ["take_A_L05a.mp4", "narr_L05_rezaba.wav (b-roll)", "take_B_L05b.mp4", "take_C_L06.mp4 (fala L06, posicao conforme roteiro)"]
(AQ / "manifest.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8"); print("ok")
