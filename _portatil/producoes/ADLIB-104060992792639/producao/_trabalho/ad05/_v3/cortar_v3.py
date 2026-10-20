# -*- coding: utf-8 -*-
"""v3: blocos de lipsync refeitos. Vídeo de entrada com o ÁUDIO PT original; espanhol (só a voz do personagem) separado.
Desatadora: entrada recortada só no rosto dela (sem a família) 288x512 em (0,150), escala 2,5x. m1: recorte no marido.
Marido m3-m5: quadro inteiro (rosto único), trechos <= 8 s sem atravessar corte (cortes em q893 e q1129).
Saída: in/pt_<id>.mp4, in/es_<id>.mp3, blocos_v3.json"""
import json, subprocess
from pathlib import Path
V = Path(__file__).parent; AD = V.parent; FPS = 24
CR_D = (0, 150, 288, 512)
BLOCOS = [
 dict(id="m1", quem="marido", a=87, b=119, crop=(30, 0, 450, 800), pad=3.0),
 dict(id="m3a", quem="marido", a=653, b=739), dict(id="m3b", quem="marido", a=739, b=893),
 dict(id="m4a", quem="marido", a=893, b=1025), dict(id="m4b", quem="marido", a=1025, b=1129),
 dict(id="m5", quem="marido", a=1129, b=1271),
 dict(id="d1", quem="desatadora", a=1302, b=1474, crop=CR_D),
 dict(id="d2a", quem="desatadora", a=1474, b=1573, crop=CR_D),
 dict(id="d2b", quem="desatadora", a=1573, b=1712, crop=CR_D)]
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
for k in BLOCOS:
    t0, t1 = k["a"]/FPS, k["b"]/FPS; dur = t1-t0; pad = max(0, k.get("pad", 0)-dur)
    vf = f"trim=start_frame={k['a']}:end_frame={k['b']},setpts=PTS-STARTPTS"
    if "crop" in k:
        x,y,w,h = k["crop"]; vf += f",crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos"
    if pad: vf += f",tpad=stop_mode=clone:stop_duration={pad:.3f}"
    af = f"atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB" + (f",apad=pad_dur={pad:.3f}" if pad else "")
    subprocess.run(["ffmpeg","-v","error","-y","-threads","4","-i",str(AD/"base_sem_legenda_lama.mp4"),"-i",str(AD/"_audio/orig_novo.wav"),
        "-filter_complex",f"[0:v]{vf}[v];[1:a]{af}[a]","-map","[v]","-map","[a]","-r","24","-c:v","libx264","-crf","14","-preset","slow",
        "-pix_fmt","yuv420p",*COR,"-c:a","aac","-b:a","192k","-ar","44100",str(V/"in"/f"pt_{k['id']}.mp4")],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/f"narr_{k['quem']}.wav"),"-af",af,"-c:a","libmp3lame","-b:a","192k",str(V/"in"/f"es_{k['id']}.mp3")],check=True)
    k["dur"] = round(dur+pad,3)
json.dump(BLOCOS, open(V/"blocos_v3.json","w",encoding="utf-8"), indent=1)
for k in BLOCOS: print(k["id"], k["a"], k["b"], k["dur"], (V/"in"/f"pt_{k['id']}.mp4").stat().st_size, (V/"in"/f"es_{k['id']}.mp3").stat().st_size)
