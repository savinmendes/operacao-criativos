# -*- coding: utf-8 -*-
"""Folha original (cima) x UK (baixo) nos quadros dados, recorte do rosto. Uso: python comparar.py orig uk saida.jpg x0,y0,x1,y1 q1 q2 ..."""
import sys, cv2, numpy as np
o, u, out = sys.argv[1], sys.argv[2], sys.argv[3]; x0, y0, x1, y1 = map(int, sys.argv[4].split(",")); qs = [int(q) for q in sys.argv[5:]]
def g(v):
    c = cv2.VideoCapture(v); r = []
    for q in qs:
        c.set(1, q); _, f = c.read(); f = f[y0:y1, x0:x1].copy()
        cv2.putText(f, str(q), (3, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2); r.append(f)
    return np.hstack(r)
cv2.imwrite(out, np.vstack([g(o), g(u)]))
