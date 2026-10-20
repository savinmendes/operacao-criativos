# entrada HeyGen: recorte 720x1280 da base_sem_legenda (cor fixa bt601) + audio PT original; ES separado
import json, sys, subprocess, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; PR = AQ.parent
sys.path.insert(0, str(PR)); from comum3 import quadros, ENC_VF, ENC_TAG
CH = json.load(open(PR / "chunks2.json")); alvo = set(sys.argv[1:])
def warp(f, x0, y0, w, h):
    M = np.float32([[720 / w, 0, -x0 * 720 / w], [0, 1280 / h, -y0 * 1280 / h]])
    return cv2.warpAffine(f, M, (720, 1280), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
for c in CH:
    nm, a, b = c["nome"], c["a"], c["b"]
    if alvo and nm not in alvo: continue
    n = b - a; npad = max(n, 92); C = np.load(AQ / f"caixas_{nm}.npy")
    tmp = AQ / "in" / f"_v_{nm}.mp4"
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",*ENC_VF,
        "-threads","3","-c:v","libx264","-crf","13","-preset","medium",*ENC_TAG,str(tmp)], stdin=subprocess.PIPE)
    last = None
    for k, f in enumerate(quadros(PR / "base_sem_legenda.mp4", a, n, 1080, 1920)):
        if nm.startswith("m01"):   # PiP da outra moça (canto inferior direito) borrado so na entrada do HeyGen
            f = f.copy(); f[1120:, 520:] = cv2.GaussianBlur(f[1120:, 520:], (0, 0), 40)
        last = warp(f, *C[k]); ff.stdin.write(last.tobytes())
    for k in range(npad - n): ff.stdin.write(last.tobytes())
    ff.stdin.close(); ff.wait()
    t0, d, dp = a / 30, n / 30, npad / 30
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(PR / "orig.wav"),"-filter_complex",
        f"[1:a]atrim={t0:.4f}:{t0+d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={dp:.4f}[a]","-map","0:v","-map","[a]",
        "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{dp:.4f}",str(AQ / "in" / f"pt_{nm}.mp4")], check=True)
    tmp.unlink()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(PR / "narr_es_raw.wav"),"-af",
        f"atrim={t0:.4f}:{t0+d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={dp:.4f}","-t",f"{dp:.4f}",
        "-ac","1","-ar","44100","-c:a","libmp3lame","-b:a","192k",str(AQ / "in" / f"es_{nm}.mp3")], check=True)
    print(nm, n, "->", npad, flush=True)
