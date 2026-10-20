# -*- coding: utf-8 -*-
import json
from pathlib import Path
AQ = Path(__file__).resolve().parent
P = json.loads((AQ / "audio" / "partes.json").read_text(encoding="utf-8"))
T = {
 "A01": ("take_A01_aurelio.mp4", "9527992a8338dacc159280485cdf8a1f", "imagens/aurelio_colar_v1.png",
         [[0.0, 0.12, "dentes/boca entreaberta antes da 1a palavra (leve)"], [8.38, 8.70, "boca aberta com dentes na pausa apos 'Benito' (cobrir)"]]),
 "A02": ("take_A02_aurelio.mp4", "f4707338fd05af49942b6b86ee5b076b", "imagens/aurelio_colar_v1.png",
         [[0.0, 0.10, "boca aberta antes de falar (leve)"], [4.28, 4.42, "dentes na pausa apos 'clientes.' (leve)"]]),
 "A03": ("take_A03_aurelio.mp4", "2a239e92393737ca10aaceb432d06703", "imagens/aurelio_colar_v1.png", []),
 "R01": ("take_R01_reportera.mp4", "117982fe57a17b9d828bc339ba360272", "../../../v2/_trabalho/imagens/reportera_gpt.png",
         [[0.0, 0.12, "sorriso com dentes antes de falar (leve)"], [3.34, 3.62, "boca muito aberta com dentes na pausa apos 'cliente,' (cobrir)"],
          [5.18, 5.34, "sorriso com dentes na pausa apos 'viral,' (leve)"]]),
 "R02": ("take_R02_reportera_claro.mp4", "1b24b2b946ab3444851a9da038e333f2", "../../../v2/_trabalho/imagens/reportera_gpt.png", []),
}
bloco = {"A01": "A01", "A02": "A02", "A03": "A03", "R01": "R01", "R02": "R02"}
takes = []
for i, (arq, vid, img, ruins) in T.items():
    q = json.loads((AQ / "qa" / f"{i}_whisper.json").read_text(encoding="utf-8")); p = P[i]
    takes.append(dict(id=i, bloco=bloco[i], arquivo=arq, personagem="Don Aurelio" if i[0] == "A" else "Reportera", texto=p["texto"],
        dur=q["dur_video"], dur_audio=q["dur_audio"], fps=q["fps"], resolucao=q["res"], heygen_video_id=vid, imagem=img,
        audio_enviado=p["arquivo"], pausas_removidas_fonte=p["pausas_removidas"], palavras=p["palavras"],
        whisper=q["whisper"], whisper_diferencas=q["diferencas"], palavras_whisper=[{k: w[k] for k in ("w", "ini", "fim")} for w in q["palavras_whisper"]],
        intervalos_ruins=[dict(ini=a, fim=b, motivo=m) for a, b, m in ruins],
        custo=dict(heygen_creditos_estim=round(q["dur_audio"] * 2.9, 1), elevenlabs_usd=round(len(p["texto"]) / 1000 * 0.165, 4))))
M = dict(
 parte="v3 entrevista: Don Aurelio (A01-A03) + Reportera (R01-R02)",
 heygen="create_video_from_image (Avatar IV), 720p, 4:5 -> 720x900, 25 fps, expressiveness low, audio wav enviado como asset",
 nota_tempo="audio do take == audio enviado; 'palavras' = alinhamento ElevenLabs remapeado apos encurtar pausas (>0,25 s -> 0,25 s); 'palavras_whisper' = faster-whisper small no take",
 vozes=dict(aurelio="Santiago VXZKNah1ssrzM8c81OiY est 0.45 estilo 0.3 vel 1.06", reportera="Gabriela hHjbwzYZW17oh0p05AKv R01 est 0.5/0.2/1.08, R02 0.4/0.4/1.05"),
 imagens=dict(aurelio=dict(arquivo="imagens/aurelio_colar_v1.png", base="v2/_trabalho/aurelio/imagens/aurelio_gpt.png", referencia="v3/_trabalho/ref/colar_san_benito_ref.png",
                          modelo="Flora is2i-gpt-image-2 (GPT Image 2) 1k 4:5 high", run_id="run_m17a611w924bf4ct9r157rq9598g8w5x", custo_usd=0.273,
                          nota="colar no peito na abertura da gola, medalha redonda prata com cruz e anel de letras, corrente de elos; enquadramento ligeiramente mais fechado que a v2"),
              reportera=dict(arquivo="v2/_trabalho/imagens/reportera_gpt.png", custo_usd=0)),
 custos=dict(flora_usd=0.273, elevenlabs_usd=0.076, heygen_creditos_estim=round(sum(t["custo"]["heygen_creditos_estim"] for t in takes), 1),
             heygen_nota="estimativa 2,9 cr/s (720p); saldo 6927 -> 6875 logo apos os jobs (cobranca pode aparecer depois e outros agentes usam a mesma conta)"),
 takes=takes)
(AQ / "manifest.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")
print([(t["id"], t["dur"], t["custo"]["heygen_creditos_estim"]) for t in takes], M["custos"])
