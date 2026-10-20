# -*- coding: utf-8 -*-
"""Máscara da mulher antiga (PiP) por quadro na base_limpa 0..N (mediapipe selfie_multiclass) -> w/velha.npy (N,1280,720) uint8.
Uso: python mascara_velha.py [N]"""
import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from pathlib import Path
AQ = Path(__file__).resolve().parent
BASE = AQ.parents[2] / "_trabalho" / "lama" / "base_limpa.mp4"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 86
X1, Y0, Y1 = 378, 380, 1220
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(AQ / "selfie_multiclass.tflite")), output_confidence_masks=True))
out = []
for q, f in enumerate(quadros(str(BASE), 0, N)):
    sub = np.ascontiguousarray(cv2.cvtColor(f[Y0:Y1, :X1], cv2.COLOR_BGR2RGB))
    r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=sub))
    bg = r.confidence_masks[0].numpy_view()
    m = (bg < 0.5).astype(np.uint8)
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    full = np.zeros((1280, 720), np.uint8); full[Y0:Y1, :X1] = m
    full[Y0:Y1, :X1][-40:] = 1                     # rodapé do PiP (mão/camisa) sempre
    out.append(full)
np.save(AQ / "w" / "velha.npy", np.array(out))
print(len(out))
