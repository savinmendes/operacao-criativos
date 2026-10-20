"""Trechos para o revisar_ad --lipsync (lote B): chk/full_<s> (base_lipsync + ES), chk/orig_<s> (17.mp4 + PT), chk/es_<s>.wav,
rosto = mediana das caixas (centro da boca mx,my e tamanho do rosto fw,fh). Grava chk/lipsync_arg.txt."""
import json, subprocess, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent; CFG = json.loads((AQ / "segs.json").read_text()); FPS = CFG["fps"]
ORIG = AD.parent.parent.parent / "UNICOS_HD" / "17.mp4"; itens = []
for s in CFG["segs"]:
    n, a, b = s["nome"], s["a"], s["b"]; t0, d = a / FPS, (b - a) / FPS
    C = np.load(AQ / s.get("cx", f"caixas_{n}.npy")); mx, my, fw, fh = np.median(C[:, 4:8], 0)
    ro = [int(mx - 0.65 * fw), int(my - 0.8 * fh), int(1.3 * fw), int(1.25 * fh)]
    full, orig, es = AQ / "chk" / f"full_{n}.mp4", AQ / "chk" / f"orig_{n}.mp4", AQ / "chk" / f"es_{n}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t0}","-t",f"{d}","-i",str(AD/"narracao_es.wav"),"-ac","1","-ar","48000",str(es)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"base_lipsync.mp4"),"-i",str(es),"-filter_complex",
        f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v]","-map","[v]","-map","1:a","-c:v","libx264","-crf","14","-c:a","aac",str(full)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(ORIG),"-i",str(AD/"_audio"/"orig.wav"),"-filter_complex",
        f"[0:v]fps=24,trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v];[1:a]atrim={t0}:{t0+d},asetpts=PTS-STARTPTS[a]","-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-c:a","aac",str(orig)],check=True)
    itens.append(f"lipsync/chk/full_{n}.mp4:lipsync/chk/es_{n}.wav:lipsync/chk/orig_{n}.mp4:{';'.join(map(str, ro))}")
(AQ / "chk" / "lipsync_arg.txt").write_text(",".join(itens), encoding="utf-8"); print(len(itens), "trechos")
