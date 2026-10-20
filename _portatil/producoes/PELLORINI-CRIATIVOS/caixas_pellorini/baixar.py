# -*- coding: utf-8 -*-
"""Baixa os resultados do Flora (nome=url na linha de comando) e monta o comparativo antes x depois com zoom na tampa.

python baixar.py pelvini-milano_2=https://... [outros...]
"""
import os
import sys
from io import BytesIO

import requests
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(os.path.dirname(BASE), "fotos-loja")
os.makedirs(os.path.join(BASE, "pellorini"), exist_ok=True)

for arg in sys.argv[1:]:
    nome, url = arg.split("=", 1)
    im = Image.open(BytesIO(requests.get(url, timeout=120).content)).convert("RGB")
    im.save(os.path.join(BASE, "pellorini", f"{nome}.jpg"), quality=95)
    antes = Image.open(os.path.join(FOTOS, f"{nome}.jpg")).convert("RGB").resize((1000, 1000))
    depois = im.resize((1000, 1000))
    zoom_a = antes.crop((150, 0, 850, 450)).resize((1000, 643))
    zoom_d = depois.crop((150, 0, 850, 450)).resize((1000, 643))
    comp = Image.new("RGB", (2000, 1000 + 643 + 40), "white")
    comp.paste(antes, (0, 40))
    comp.paste(depois, (1000, 40))
    comp.paste(zoom_a, (0, 1040))
    comp.paste(zoom_d, (1000, 1040))
    d = ImageDraw.Draw(comp)
    d.text((10, 10), f"ANTES  {nome}", fill="black")
    d.text((1010, 10), "DEPOIS", fill="black")
    comp.save(os.path.join(BASE, f"comparar_{nome}.jpg"), quality=85)
    print("ok", nome, im.size)
