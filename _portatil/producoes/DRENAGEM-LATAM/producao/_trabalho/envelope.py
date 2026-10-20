import subprocess, sys, numpy as np
src, de, ate = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(de), "-to", str(ate), "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(float); h = 800
for i in range(0, len(x) - h, h):
    r = 20 * np.log10(np.sqrt(np.mean(x[i:i + h] ** 2)) + 1)
    print(f"{de + i / 16000:.2f} {'#' * int(max(0, r - 30))}")
