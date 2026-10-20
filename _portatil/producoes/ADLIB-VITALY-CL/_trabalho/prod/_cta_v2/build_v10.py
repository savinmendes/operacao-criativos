# -*- coding: utf-8 -*-
"""V10 CTA v2: o fim é a criadora falando ("Oye, si lo has tenido en el carrito... hoy es tu día").
Sai a caixa cinza "Toca el botón de abajo / Comprar ahora" + selo grande. O rosto entra com zoom 1,22x
(o rodapé "vitaly-chile.com" do original fica fora do quadro), e "hoy es el día, hoy es tu día" passa em off sobre
um take Lymphoria. Legenda palavra a palavra só no fim, selo pequeno e setas."""
import json, subprocess, sys
from pathlib import Path
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
AQUI = Path(__file__).parent
V10 = AQUI.parent / "V10"
A = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
T_ROD, T_HOY, T_FIM = 70.967, 74.80, 77.0
TAKE = A / "ad14/flora/t4_edit.mp4"
wk = AQUI / "V10"; (wk / "out").mkdir(parents=True, exist_ok=True)
corpo = wk / "corpo_v10.mp4"
fc = (f"[0:v]trim=0:{T_ROD},setpts=PTS-STARTPTS,scale=720:1280,fps=30,format=yuv420p,setsar=1[a];"
      f"[1:v]trim={T_ROD}:{T_HOY},setpts=PTS-STARTPTS,crop=iw*0.82:ih*0.82:iw*0.09:0,scale=720:1280,fps=30,format=yuv420p,setsar=1[b];"
      f"[2:v]trim=0.2:{0.2 + T_FIM - T_HOY:.3f},setpts=PTS-STARTPTS,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,format=yuv420p,setsar=1[c];"
      f"[a][b][c]concat=n=3:v=1:a=0[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V10 / "corpo_av.mp4"), "-i", str(V10 / "orig.mp4"), "-i", str(TAKE),
                "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-t", f"{T_FIM:.3f}",
                "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(corpo)], check=True)
rec = {"saida": str(wk / "out" / "V10 - LYMPHORIA-CARRITO-MENOPAUSIA.mp4"), "estilo": "drop", "corpo": str(corpo),
       "legenda": {"fonte": "transcrever", "idioma": "es", "desde": T_ROD - 0.05, "chaves": ["carrito", "hoy"]},
       "selo": {"linhas": ["", "PAGO CONTRA", "ENTREGA", ""], "escala": 0.55, "x": 331, "y": 1330, "desde": T_ROD},
       "cta": {"inicio": T_HOY - 0.3}, "limite_mb": 30, "resolucao": "720"}
(wk / "receita_cta2.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
subprocess.run([sys.executable, str(KIT / "ferramentas" / "montar_ad.py"), str(wk / "receita_cta2.json")], check=True)
json.dump({"corte": T_ROD, "takes": [str(TAKE)], "narr": "fala original da criadora"}, open(wk / "info.json", "w"), indent=1)
