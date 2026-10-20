import cv2, numpy as np, sys
sys.path.insert(0, '_tmp'); from mascara import mascara, R0, R1
cap = cv2.VideoCapture('../../../UNICOS_HD/14.mp4'); outs = []
for t in [0.5, 2, 4, 6, 8, 9, 9.4, 9.6, 9.8]:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * 24)); ok, f = cap.read()
    m = mascara(f); g = f.copy(); band = g[R0:R1]; band[m > 0] = (0.5 * band[m > 0] + [0, 0, 127]).astype(np.uint8)
    outs.append(cv2.resize(g[600:1200], (240, 200)))
cv2.imwrite('../ad14/_tmp/teste_mask.jpg', np.vstack([np.hstack(outs[:5]), np.hstack(outs[5:] + [outs[0] * 0])]))
