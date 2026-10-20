# entradas do lipsync do comerciante: trecho da base EN (com o áudio ES ORIGINAL do mesmo trecho da fonte) + mp3 EN separado
import json, subprocess
SRC="C:/Users/PICHAU/Downloads/1-VIDEOS/AVATAR_REST.mp4"
T=json.load(open("timeline.json",encoding="utf-8")); seg={}
for c in T["cenas"]:
    if c["lipsync"]!="comerciante": continue
    nm=c["nome"]; a,b=c["out_ini"],c["out_fim"]; d=b-a
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.4f}","-t",f"{d:.4f}","-i","base_en.mp4",
        "-ss",f"{c['src_ini']:.4f}","-t",f"{c['src_dur']:.4f}","-i",SRC,"-map","0:v","-map","1:a",
        "-af",f"atempo={1/c['fator']:.5f},apad","-c:v","libx264","-crf","16","-preset","medium","-c:a","aac","-b:a","192k","-t",f"{d:.4f}",
        f"heygen_in/{nm}.mp4"],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{a:.4f}","-t",f"{d:.4f}","-i","audio/voz_en.wav","-ac","1","-c:a","libmp3lame","-b:a","192k",
        f"heygen_in/{nm}_en.mp3"],check=True)
    seg[nm]=[a,b]
    print(nm, subprocess.run(["ffprobe","-v","error","-show_entries","format=duration,size","-of","csv=p=0",f"heygen_in/{nm}.mp4"],capture_output=True,text=True).stdout.strip())
json.dump(seg,open("heygen_in/seg.json","w"))
