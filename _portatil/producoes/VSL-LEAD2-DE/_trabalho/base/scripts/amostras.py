import subprocess, numpy as np, cv2, os, sys
SRC = r"C:\Users\PICHAU\Downloads\Lead 2.mp4"; BASE = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
def q(p, t):
    b = subprocess.run(["ffmpeg","-v","error","-ss",f"{t}","-i",p,"-frames:v","1","-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(960,720,3)
T = [20.0, 310.0, 600.0, 1500.0, 2300.0, 2450.0]; lum = []
for t in T:
    a, b = q(SRC, t), q(BASE, t)
    ga, gb = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(float), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(float)
    lum.append((t, round(ga[100:600].mean(), 2), round(gb[100:600].mean(), 2)))
    z = lambda x: cv2.resize(x[0:900 if t < 210 else 920][-300:], None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    top = lambda x: cv2.resize(x[0:80, 0:300], None, fx=2.4, fy=2.4, interpolation=cv2.INTER_CUBIC)
    img = np.vstack([np.hstack([z(a), z(b)])])
    cv2.putText(img, f"ANTES {t:.0f}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2); cv2.putText(img, "DEPOIS", (1090, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imwrite(os.path.join(OUT, f"zoom_{int(t):04d}s.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 92])
    cv2.imwrite(os.path.join(OUT, f"selo_{int(t):04d}s.jpg"), np.hstack([top(a), top(b)]))
print("luma (t, original, base) fora da faixa:", lum)
