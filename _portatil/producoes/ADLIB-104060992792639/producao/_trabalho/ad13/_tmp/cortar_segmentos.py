# corta os trechos de rosto falando da base_sem_legenda.mp4 e grava segmentos.json; gera tambem pt_<n>.mp4 (video + audio PT original)
import json, subprocess, sys
sys.path.insert(0, '.')
from segs import SEGS
FPS = 30
out = {"base": "base_sem_legenda.mp4", "fps": FPS, "resolucao": "720x1280", "duracao": round(3613 / FPS, 3), "segmentos": [],
       "fora_do_lipsync": [{"ini": 6.6, "fim": 7.033, "o_que": "transicao com glitch (Jesus -> mulher)"},
                           {"ini": 29.1, "fim": 33.433, "o_que": "b-roll da corda/no"},
                           {"ini": 43.567, "fim": 47.133, "o_que": "b-roll mulher na mesa"},
                           {"ini": 59.8, "fim": 63.633, "o_que": "b-roll esteira"},
                           {"ini": 83.9, "fim": 88.9, "o_que": "quarto com crucifixo (substitui a cena com pessoa parecida com apresentadora de TV)"}]}
for nome, quem, a, b in SEGS:
    seg = f"seg_{nome}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "base_sem_legenda.mp4", "-vf",
                    f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS", "-an", "-c:v", "libx264",
                    "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-r", "30", seg], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", seg, "-i", f"lipsync/pt_{nome}.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"lipsync/pt_{nome}.mp4"], check=True)
    out["segmentos"].append({"arquivo": seg, "personagem": quem, "ini": round(a / FPS, 3), "fim": round(b / FPS, 3),
                             "dur": round((b - a) / FPS, 3), "quadro_ini": a, "quadro_fim": b - 1})
json.dump(out, open("segmentos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(SEGS))
