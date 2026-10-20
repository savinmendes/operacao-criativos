"""Corta os blocos de lipsync da base_sem_legenda.mp4 (24 fps, tempo novo).
Cada bloco: pt_<id>.mp4 (vídeo + ÁUDIO ORIGINAL PT do trecho) e es_<id>.mp3 (fala em espanhol do personagem).
Blocos com 'crop' são recortes (rosto em plano aberto), escalados para 720x1280; 'pad' congela o último quadro até N s."""
import json, subprocess
from pathlib import Path
L = Path(__file__).parent; AD = L.parent; FPS = 24
BLOCOS = [
 dict(id="c1", quem="clara", a=0, b=75),
 dict(id="m1", quem="marido", a=87, b=120, pad=3.0),
 dict(id="m2", quem="marido", a=212, b=286, crop=(360,400,360,640)),
 dict(id="c2", quem="clara", a=286, b=430), dict(id="c3", quem="clara", a=430, b=653),
 dict(id="m3", quem="marido", a=653, b=883), dict(id="m4", quem="marido", a=883, b=1133), dict(id="m5", quem="marido", a=1133, b=1271),
 dict(id="d1", quem="desatadora", a=1302, b=1474), dict(id="d2", quem="desatadora", a=1474, b=1712),
 dict(id="d3", quem="desatadora", a=1712, b=1992), dict(id="d4", quem="desatadora", a=1992, b=2150), dict(id="d5", quem="desatadora", a=2150, b=2298)]
for k in BLOCOS:
    t0, t1 = k["a"]/FPS, k["b"]/FPS; dur = t1-t0; pad = max(0, k.get("pad", 0)-dur)
    vf = f"trim=start_frame={k['a']}:end_frame={k['b']},setpts=PTS-STARTPTS"
    if "crop" in k:
        x,y,w,h = k["crop"]; vf += f",crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos"
    if pad: vf += f",tpad=stop_mode=clone:stop_duration={pad:.3f}"
    af = f"atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB" + (f",apad=pad_dur={pad:.3f}" if pad else "")
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"base_sem_legenda.mp4"),"-i",str(AD/"_audio/orig_novo.wav"),
        "-filter_complex",f"[0:v]{vf}[v];[1:a]{af}[a]","-map","[v]","-map","[a]","-r","24","-c:v","libx264","-crf","14","-preset","slow",
        "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","44100",str(L/f"pt_{k['id']}.mp4")],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/f"narr_{k['quem']}.wav"),"-af",af,"-c:a","libmp3lame","-b:a","192k",str(L/f"es_{k['id']}.mp3")],check=True)
    k["dur"] = round(dur+pad,3)
json.dump(BLOCOS, open(L/"blocos.json","w",encoding="utf-8"), indent=1)
for k in BLOCOS: print(k["id"], k["a"], k["b"], k["dur"], (L/f"pt_{k['id']}.mp4").stat().st_size, (L/f"es_{k['id']}.mp3").stat().st_size)
