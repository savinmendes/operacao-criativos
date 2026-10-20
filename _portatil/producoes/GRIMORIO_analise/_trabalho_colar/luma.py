import subprocess, numpy as np
O = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"; N = r"C:\Users\PICHAU\Downloads\GRIMORIO V2 - COLAR (VIDEO FICTICIO).mp4"
S = 101
def ymean(path, n):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"select=eq(n\,{n}),extractplanes=y", "-fps_mode", "passthrough",
                        "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8).reshape(1280, 720).astype(float)
    a[:30, 590:] = np.nan  # ignora o selo
    return np.nanmean(a)
for n in [100, 2000, 3700, 3771]:
    print("antes", n, round(ymean(O, n), 2), round(ymean(N, n), 2))
for n in [3779, 3800, 3850, 3900, 4200, 4600]:
    print("depois", n, "->", n + S, round(ymean(O, n), 2), round(ymean(N, n + S), 2))
