import sys, glob, cv2, numpy as np, json
nomes = sys.argv[2:]; rows = []
for n in nomes:
    cap = cv2.VideoCapture(f"in/crop_{n}.mp4"); N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); ims = []
    for k in np.linspace(0, N - 1, 8).astype(int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, k); ok, f = cap.read(); f = cv2.resize(f, (135, 240))
        cv2.putText(f, f"{n}:{k}", (3, 14), 0, 0.45, (0, 255, 255), 1); ims.append(f)
    rows.append(np.hstack(ims))
cv2.imwrite(sys.argv[1], np.vstack(rows))
