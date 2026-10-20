import json, subprocess
seg = json.load(open("../segmentos.json"))["segmentos"]
FIN = "../../../AD 01 - ORACION-TRES-BENDICIONES-ES-LATAM.mp4"
parts = []
for s in seg:
    a, b = s["quadro_ini"], min(s["quadro_fim"], 3464); n = s["nome"]
    for src, out in ((FIN, f"final/f_{n}.mp4"), ("../base_sem_legenda.mp4", f"final/o_{n}.mp4")):
        subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vf",f"trim=start_frame={a}:end_frame={b+1},setpts=PTS-STARTPTS",
            "-an","-c:v","libx264","-crf","14",out], check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i","../narracao_es.wav","-af",f"atrim={a/30}:{(b+1)/30},asetpts=PTS-STARTPTS",
        "-ac","1","-c:a","libmp3lame","-b:a","192k",f"final/e_{n}.mp3"], check=True)
    parts.append(f"f_{n}.mp4:e_{n}.mp3:o_{n}.mp4:330;280;200;260")
open("final/lipsync_arg.txt","w").write(",".join(parts)); print(len(parts))
