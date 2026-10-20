import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
vid = sys.argv[1]; aud = sys.argv[2]
fps, ab, _, _, _ = cl.series_video(__import__('pathlib').Path(vid), None)
n = len(ab)
env = cl.envelope(cl.ler_audio(aud), 16000, fps, n)
np.save('diag_ab.npy', ab); np.save('diag_env.npy', env)
print('fps', fps, 'n', n, 'ab pct', np.nanpercentile(ab, [5, 25, 50, 75, 95]))
for lag in range(-30, 31, 3):
    a = ab[max(0, lag):n + min(0, lag)]; e = env[max(0, -lag):n - max(0, lag)]
    m = np.isfinite(a) & np.isfinite(e)
    print(lag, round(np.corrcoef(a[m], e[m])[0, 1], 3))
