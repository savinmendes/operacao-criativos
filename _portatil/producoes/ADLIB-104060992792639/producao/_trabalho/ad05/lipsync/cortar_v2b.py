"""Blocos extras de lipsync (v2): recorte justo no rosto, escalado a 720x1280, vídeo com ÁUDIO PT original, espanhol separado.
cl = Clara 'Toma, papá' (tomada 119-161, completada até 3 s com quadro congelado); mz = marido de perfil (212-286), recorte 4x."""
import json, subprocess
from pathlib import Path
L = Path(__file__).parent; AD = L.parent; FPS = 24
NOVOS = [dict(id="cl2", quem="clara", a=119, b=161, crop=(180,100,360,640), pad=3.0),
         ]
for k in NOVOS:
    t0, t1 = k["a"]/FPS, k["b"]/FPS; dur = t1-t0; pad = max(0, k.get("pad", 0)-dur)
    x,y,w,h = k["crop"]
    vf = f"trim=start_frame={k['a']}:end_frame={k['b']},setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos"
    if pad: vf += f",tpad=stop_mode=clone:stop_duration={pad:.3f}"
    af = f"atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB" + (f",apad=pad_dur={pad:.3f}" if pad else "")
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"base_sem_legenda.mp4"),"-i",str(AD/"_audio/orig_novo.wav"),
        "-filter_complex",f"[0:v]{vf}[v];[1:a]{af}[a]","-map","[v]","-map","[a]","-r","24","-c:v","libx264","-crf","14","-preset","slow",
        "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","44100",str(L/f"pt_{k['id']}.mp4")],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/f"narr_{k['quem']}.wav"),"-af",af,"-c:a","libmp3lame","-b:a","192k",str(L/f"es_{k['id']}.mp3")],check=True)
    k["dur"] = round(dur+pad,3)
B = [b for b in json.load(open(L/"blocos.json",encoding="utf-8")) if b["id"] not in ("cl2",)] + NOVOS
json.dump(B, open(L/"blocos.json","w",encoding="utf-8"), indent=1)
for k in NOVOS: print(k["id"], k["dur"], (L/f"pt_{k['id']}.mp4").stat().st_size, (L/f"es_{k['id']}.mp3").stat().st_size)
