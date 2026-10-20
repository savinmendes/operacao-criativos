# -*- coding: utf-8 -*-
"""Rastreia o rótulo do frasco (0–7,73 s) com LK + afim parcial encadeada a partir do quadro 0.
Saída: rastreio.json = [{"k":k, "M":[[..],[..]] (quadro0 -> quadro k) ou null, "n": inliers}]"""
import sys, json
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, str(Path(__file__).parent.parent / "comum"))
import texto as T
D = Path(__file__).parent
fr = T.ler_quadros(str(D / "orig.mp4"), t=7.75)
N = min(len(fr), 232)

def track(anchor, reg, ks):
    """matrizes quadro anchor -> k, seguindo a ordem de ks (cada um vizinho do anterior)"""
    M = np.float32([[1, 0, 0], [0, 1, 0]])
    res = {anchor: (M.tolist(), 999)}
    prev = cv2.cvtColor(fr[anchor], cv2.COLOR_RGB2GRAY)
    for k in ks:
        cur = cv2.cvtColor(fr[k], cv2.COLOR_RGB2GRAY)
        poly = cv2.transform(reg[None], M)[0]
        mask = np.zeros_like(prev); cv2.fillConvexPoly(mask, poly.astype(np.int32), 255)
        p0 = cv2.goodFeaturesToTrack(prev, 200, 0.01, 3, mask=mask)
        if p0 is None or len(p0) < 8: break
        p1, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, p0, None, winSize=(21, 21), maxLevel=3)
        pb, stb, _ = cv2.calcOpticalFlowPyrLK(cur, prev, p1, None, winSize=(21, 21), maxLevel=3)
        good = (st[:, 0] == 1) & (stb[:, 0] == 1) & (np.linalg.norm(pb - p0, axis=2)[:, 0] < 1.0)
        a, b = p0[good], p1[good]
        if len(a) < 8: break
        A, inl = cv2.estimateAffine2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=1.5)
        n = int(inl.sum()) if inl is not None else 0
        if A is None or n < 8: break
        M = (np.vstack([A, [0, 0, 1]]) @ np.vstack([M, [0, 0, 1]]))[:2].astype(np.float32)
        res[k] = (M.tolist(), n)
        prev = cur
    return res

R0 = np.float32([[183, 640], [279, 640], [279, 765], [183, 765]])
R1 = np.float32([[140, 676], [237, 676], [237, 780], [140, 780]])
a0 = track(0, R0, range(1, 100))
a1 = track(136, R1, range(135, 93, -1))
a1.update(track(136, R1, range(137, N)))
out = []
for k in range(N):
    if k < 96 and k in a0: out.append({"k": k, "a": 0, "M": a0[k][0], "n": a0[k][1]})
    elif k >= 96 and k in a1: out.append({"k": k, "a": 136, "M": a1[k][0], "n": a1[k][1]})
    else: out.append({"k": k, "a": None, "M": None, "n": 0})
(D / "rastreio.json").write_text(json.dumps(out), encoding="utf-8")
print("sem:", [o["k"] for o in out if o["M"] is None])
