import cv2, numpy as np, sys, json
fin, ori, out_b, out_c = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
segs = json.load(open(sys.argv[5]))["segs"]; fpsO = json.load(open(sys.argv[5]))["fps"]
F = cv2.VideoCapture(fin); O = cv2.VideoCapture(ori); ff = F.get(5)
def q(cap, t, fps):
    cap.set(1, int(round(t * fps))); ok, f = cap.read(); return f
# folha de boca: 3 tempos por trecho, final em cima / original embaixo, recorte no rosto
ims = []
for s in segs:
    C = np.load("lipsync/" + s.get("cx", f"caixas_{s['nome']}.npy"))
    for fr in np.linspace(0.15, 0.85, 3):
        k = int(fr * (s["b"] - s["a"])); t = (s["a"] + k) / fpsO
        if t > 99.9: continue
        x0, y0, w, h, mx, my, fw, fh = C[k]; L = int(fw * 1.3)
        cx, cy = int(mx), int(my - 0.2 * fh)
        a = q(F, t, ff); b = q(O, t, fpsO)
        def rc(f): return cv2.resize(f[max(0, cy - L // 2):cy + L // 2, max(0, cx - L // 2):cx + L // 2], (150, 150))
        z = np.vstack([rc(a), rc(b)]); cv2.putText(z, f"{t:.1f}", (3, 14), 0, 0.45, (0, 255, 255), 1); ims.append(z)
while len(ims) % 12: ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out_b, np.vstack([np.hstack(ims[i:i + 12]) for i in range(0, len(ims), 12)]))
# folha de cortes: 1 em 1 quadro (do final) em volta de cada corte (-3..+3)
rows = []
for s in segs[1:]:
    t0 = s["a"] / fpsO; k0 = int(round(t0 * ff)); r = []
    for k in range(k0 - 3, k0 + 4):
        F.set(1, k); ok, f = F.read()
        if not ok: continue
        f = cv2.resize(f, (108, 192)); cv2.putText(f, f"{k/ff:.2f}", (2, 12), 0, 0.38, (0, 255, 255), 1); r.append(f)
    if len(r) == 7: rows.append(np.hstack(r))
cv2.imwrite(out_c, np.vstack(rows))
