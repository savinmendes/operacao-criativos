"""Corta os trechos de rosto falando do 01.mp4 (vídeo + ÁUDIO ORIGINAL PT) e o áudio ES correspondente."""
import json, subprocess
SEGS = [(0,251),(252,476),(477,583),(584,628),(629,978),(979,1259),(1260,1469),(1470,1807),
        (1808,2173),(2174,2498),(2499,2811),(2812,3142),(3143,3472)]
out = []
for k,(a,b) in enumerate(SEGS, 1):
    n = f"s{k:02d}"; t0, t1 = a/30, (b+1)/30
    subprocess.run(["ffmpeg","-v","error","-y","-i","../../../UNICOS_HD/01.mp4","-filter_complex",
        f"[0:v]trim=start_frame={a}:end_frame={b+1},setpts=PTS-STARTPTS[v];[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-preset","slow","-pix_fmt","yuv420p","-r","30",
        "-c:a","aac","-b:a","192k",f"lipsync/pt_{n}.mp4"],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i","narracao_es.wav","-af",f"atrim={t0}:{t1},asetpts=PTS-STARTPTS",
        "-ac","1","-c:a","libmp3lame","-b:a","192k",f"lipsync/es_{n}.mp3"],check=True)
    out.append({"nome":n,"quadro_ini":a,"quadro_fim":b,"ini":round(t0,3),"fim":round(t1,3),"dur":round(t1-t0,3)})
json.dump({"fps":30,"nquadros_base":3473,"segmentos":out},open("segmentos.json","w"),indent=1)
print(sum(s["dur"] for s in out))
