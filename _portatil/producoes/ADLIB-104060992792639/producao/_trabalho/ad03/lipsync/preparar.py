"""Entradas do lipsync do 03: recorte 360x640 em (170,0) (so o padre; no split = metade de cima), escala 2x -> 720x1280,
com o AUDIO ORIGINAL PT do trecho; ES do mesmo intervalo em es_<nome>.mp3. Fonte: base_sem_legenda.mp4 se existir, senao o original.
Uso: python lipsync/preparar.py [nomes...]"""
import json, subprocess, sys
from pathlib import Path
L=Path(__file__).parent; AD=L.parent
J=json.loads((L/"trechos.json").read_text(encoding="utf-8-sig")); X,Y,W,H=J["recorte"]
src=str(AD/"base_sem_legenda.mp4") if (AD/"base_sem_legenda.mp4").exists() else str(AD/"../../../UNICOS_HD/03.mp4")
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
for nome,a,b in J["trechos"]:
    if len(sys.argv)>1 and nome not in sys.argv[1:]: continue
    t0,t1=a/30,(b+1)/30
    subprocess.run(["ffmpeg","-v","error","-y","-threads","4","-i",src,"-i",str(AD/"../../../UNICOS_HD/03.mp4"),"-filter_complex",
      f"[0:v]trim=start_frame={a}:end_frame={b+1},setpts=PTS-STARTPTS,crop={W}:{H}:{X}:{Y},scale=720:1280:flags=lanczos[v];[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]",
      "-map","[v]","-map","[a]","-c:v","libx264","-crf","12","-preset","slow","-pix_fmt","yuv420p",*COR,"-r","30","-c:a","aac","-b:a","192k",str(L/f"pt_{nome}.mp4")],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"narracao_es.wav"),"-af",f"atrim={t0}:{t1}","-ac","1","-c:a","libmp3lame","-b:a","192k",str(L/f"es_{nome}.mp3")],check=True)
    print(nome, src.split("\\")[-1].split("/")[-1], b-a+1)
