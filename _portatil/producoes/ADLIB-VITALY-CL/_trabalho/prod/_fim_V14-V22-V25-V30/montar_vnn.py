# -*- coding: utf-8 -*-
"""Parte 1 (vídeo tratado) + fim Lymphoria comum (parte2.mp4 + narr_fim) -> montar_ad.py em 720x1280.
  python montar_vnn.py <pasta_trabalho_VNN> <parte1_tratada.mp4> "<saida.mp4>"
Normaliza a parte 1 (30 fps, áudio com a mesma duração do vídeo, fade de 0,25 s no fim da música)."""
import json, subprocess, sys
from pathlib import Path
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
FIM = Path(__file__).parent
pasta, p1, saida = Path(sys.argv[1]).resolve(), str(Path(sys.argv[2]).resolve()), sys.argv[3]
dur = lambda f, s="v": float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", f"{s}:0", "-show_entries",
                        "stream=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
d = dur(p1)
p1n = pasta / "parte1_norm.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "3", "-i", p1, "-t", f"{d:.4f}", "-r", "30",
                "-af", f"apad,atrim=0:{d:.4f},afade=t=out:st={d - 0.25:.3f}:d=0.25,aresample=48000",
                "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                "-c:a", "aac", "-b:a", "192k", "-ac", "2", str(p1n)], check=True)
d1 = dur(str(p1n))
rec = {
    "saida": saida, "estilo": "drop", "corpo": str(FIM / "parte2.mp4"),
    "hook": {"tipo": "antes", "video": str(p1n)},
    "legenda": {"fonte": f"alinhamento:{FIM / 'narr_fim.alinhamento.json'}",
                "chaves": ["lymphoria", "reciba", "gratis", "recibir", "noventa"]},
    "selo": {"linhas": ["ENVÍO GRATIS A DOMICILIO", "PAGO CONTRA", "ENTREGA", "¡PAGAS AL RECIBIR!"],
             "x": 160, "y": 1225, "desde": round(d1 + 3.32, 2)},
    "cta": {"palavra": "toca"}, "limite_mb": 30, "resolucao": "720",
}
(pasta / "receita_final.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
subprocess.run([sys.executable, str(KIT / "ferramentas" / "montar_ad.py"), str(pasta / "receita_final.json")], check=True)
