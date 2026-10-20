import json, subprocess
FPS = 30
SEGS = [  # (arquivo, personagem, quadro inicial, quadro final inclusivo) no tempo final de base_sem_legenda.mp4
    ("seg_menina.mp4", "menina", 0, 264),
    ("seg_mulher_1.mp4", "mulher", 271, 358),
    ("seg_mulher_2.mp4", "mulher", 462, 935),
    ("seg_mulher_3.mp4", "mulher", 1138, 1860),
]
out = {"base": "base_sem_legenda.mp4", "fps": FPS, "resolucao": "720x1280", "duracao": round(1861 / FPS, 3),
       "segmentos": [], "fora_do_lipsync": [
           {"ini": 8.833, "fim": 9.033, "o_que": "transição com clarão (menina -> mulher)"},
           {"ini": 11.967, "fim": 15.4, "o_que": "zoom lento no olival (substitui as cédulas de R$ 100)"},
           {"ini": 31.2, "fim": 37.933, "o_que": "b-roll do supermercado (fusão + recorte com zoom)"}]}
for nome, quem, a, b in SEGS:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "base_sem_legenda.mp4", "-vf",
                    f"trim=start_frame={a}:end_frame={b + 1},setpts=PTS-STARTPTS", "-an", "-c:v", "libx264",
                    "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-r", "30", nome], check=True)
    out["segmentos"].append({"arquivo": nome, "personagem": quem, "ini": round(a / FPS, 3),
                             "fim": round((b + 1) / FPS, 3), "dur": round((b + 1 - a) / FPS, 3),
                             "quadro_ini": a, "quadro_fim": b})
json.dump(out, open("segmentos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(out["segmentos"], ensure_ascii=False, indent=1))
