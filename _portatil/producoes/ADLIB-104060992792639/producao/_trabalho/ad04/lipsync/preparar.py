# -*- coding: utf-8 -*-
"""Entrada do HeyGen por trecho: recorte 9:16 (só o rosto de quem fala) da base_sem_legenda.mp4, escalado p/ 720x1280,
com o ÁUDIO ORIGINAL PT do trecho; e o ES (narr_<quem>.wav) do mesmo intervalo como mp3.
Trechos < MIN s: completados com o último quadro (tpad) e o áudio com silêncio; só os n quadros reais são usados depois.
Uso: python preparar.py [nomes...]  -> in/pt_<n>.mp4, in/es_<n>.mp3, in/orig_<n>.mp4 (trecho da base 720x1280 com PT, p/ medir)"""
import sys, json, subprocess
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent; (AQ/"in").mkdir(exist_ok=True)
cfg = json.loads((AQ/"segs.json").read_text()); FPS = cfg["fps"]; MIN = 3.2
SRC = str((AD/cfg["src"]).resolve()); BASE = str(AD/"base_sem_legenda.mp4")
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
sel = set(sys.argv[1:])
for s in cfg["segs"]:
    if sel and s["n"] not in sel: continue
    a, b = s["a"], s["b"]; t0, t1 = a/FPS, b/FPS; d = t1-t0; pad = max(0, MIN-d)
    if "track" in s:   # recorte que segue o rosto (caixas por quadro em boxes_<n>.json, geradas por rastrear.py)
        tmpv = AQ/"in"/f"_trk_{s['n']}.mp4"; subprocess.run([sys.executable, str(AQ/"rastrear.py"), s["n"], str(tmpv)], check=True)
        vin, vf = str(tmpv), "setsar=1"
    else:
        x, y, w, h = s["crop"]; vin = BASE
        vf = f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos,setsar=1"
    if pad: vf += f",tpad=stop_mode=clone:stop_duration={pad:.3f}"
    af = f"atrim={t0:.4f}:{t1:.4f},asetpts=PTS-STARTPTS" + (f",apad=pad_dur={pad:.3f}" if pad else "")
    subprocess.run(["ffmpeg","-v","error","-y","-threads","4","-i",vin,"-i",SRC,"-filter_complex",f"[0:v]{vf}[v];[1:a]{af}[a]",
        "-map","[v]","-map","[a]","-r",str(FPS),"-c:v","libx264","-crf","14","-preset","slow","-pix_fmt","yuv420p",*COR,
        "-c:a","aac","-b:a","192k","-ar","44100",str(AQ/"in"/f"pt_{s['n']}.mp4")], check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/f"narr_{s['quem']}.wav"),"-af",af,"-ac","1","-c:a","libmp3lame","-b:a","192k",
        str(AQ/"in"/f"es_{s['n']}.mp3")], check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-threads","4","-i",BASE,"-i",SRC,"-filter_complex",
        f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v];[1:a]atrim={t0:.4f}:{t1:.4f},asetpts=PTS-STARTPTS[a]",
        "-map","[v]","-map","[a]","-r",str(FPS),"-c:v","libx264","-crf","14","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
        str(AQ/"in"/f"orig_{s['n']}.mp4")], check=True)
    print(s["n"], round(d,2), "pad", round(pad,2), (AQ/"in"/f"pt_{s['n']}.mp4").stat().st_size, (AQ/"in"/f"es_{s['n']}.mp3").stat().st_size)
