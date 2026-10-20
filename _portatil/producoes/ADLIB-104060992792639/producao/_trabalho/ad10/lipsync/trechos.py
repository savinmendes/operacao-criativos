"""Gera, por segmento, trechos para conferência: chk/full_<n>.mp4 (base_lipsync + ES), chk/orig_<n>.mp4 (original + PT),
chk/es_<n>.wav e rosto x,y,w,h (mediana da caixa do rosto). Imprime a string do --lipsync do revisar_ad.
Uso: python trechos.py NN segs.json [plano.json]"""
import sys, json, subprocess, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent; (AQ / "chk").mkdir(exist_ok=True)
NN = sys.argv[1]; CFG = json.load(open(AQ / sys.argv[2])); FPS = CFG["fps"]
PL = json.load(open(AQ / sys.argv[3])) if len(sys.argv) > 3 else None
ORIG = AD.parent.parent.parent / "UNICOS_HD" / f"{NN}.mp4"
itens = []
for sg in CFG["segs"]:
    n = sg["nome"]
    if PL is not None and n not in PL: continue
    a, b = sg["q"]; t0, d = a / FPS, (b - a + 1) / FPS
    bx = json.load(open(AQ / "boxes" / f"{n}.json"))
    F = np.median(np.array([x["face"] for x in bx["boxes"]]), 0); w, h = F[2] - F[0], F[3] - F[1]
    ro = [int(F[0] - 0.15 * w), int(F[1] - 0.1 * h), int(1.3 * w), int(1.25 * h)]
    full, orig, es = AQ / "chk" / f"full_{n}.mp4", AQ / "chk" / f"orig_{n}.mp4", AQ / "chk" / f"es_{n}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t0}","-t",f"{d}","-i",str(AD/"narracao_es.wav"),"-ac","1","-ar","48000",str(es)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"base_lipsync.mp4"),"-i",str(es),"-filter_complex",
        f"[0:v]trim=start_frame={a}:end_frame={b+1},setpts=PTS-STARTPTS[v]","-map","[v]","-map","1:a","-c:v","libx264","-crf","14","-c:a","aac",str(full)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(ORIG),"-i",str(AD/"_audio"/"orig.wav"),"-filter_complex",
        f"[0:v]trim=start_frame={a}:end_frame={b+1},setpts=PTS-STARTPTS[v];[1:a]atrim={t0}:{t0+d},asetpts=PTS-STARTPTS[a]","-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-c:a","aac",str(orig)],check=True)
    itens.append(f"lipsync/chk/full_{n}.mp4:lipsync/chk/es_{n}.wav:lipsync/chk/orig_{n}.mp4:{chr(59).join(map(str, ro))}")
    print(n, ro, flush=True)
(AQ / "chk" / "lipsync_arg.txt").write_text(",".join(itens), encoding="utf-8")
