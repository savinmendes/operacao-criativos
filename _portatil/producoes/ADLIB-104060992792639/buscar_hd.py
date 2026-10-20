# -*- coding: utf-8 -*-
"""Abre a página de anúncios e captura, nas respostas de rede, os campos video_hd_url/video_sd_url por id da biblioteca."""
import json, re, sys, time
from playwright.sync_api import sync_playwright
URL = sys.argv[1]; OUT = sys.argv[2]
achados = {}
def on_resp(r):
    try:
        if "graphql" not in r.url and "ads/library" not in r.url: return
        t = r.text()
    except Exception: return
    for m in re.finditer(r'"ad_archive_id":"(\d+)"', t):
        pass
    # pega blocos com ad_archive_id + video_hd_url próximos
    for m in re.finditer(r'"ad_archive_id":"(\d+)".{0,20000}?(?="ad_archive_id"|$)', t, re.S):
        bloco = m.group(0); aid = m.group(1)
        hd = re.findall(r'"video_hd_url":"(https:[^"]+)"', bloco)
        sd = re.findall(r'"video_sd_url":"(https:[^"]+)"', bloco)
        if hd or sd:
            d = achados.setdefault(aid, {"hd": [], "sd": []})
            for u in hd:
                u = u.replace("\/", "/")
                if u not in d["hd"]: d["hd"].append(u)
            for u in sd:
                u = u.replace("\/", "/")
                if u not in d["sd"]: d["sd"].append(u)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(locale="pt-BR", viewport={"width": 1400, "height": 1000})
    pg.on("response", on_resp)
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000); time.sleep(8)
    # o HTML inicial também traz JSON embutido
    html = pg.content()
    class R:  # reaproveita o parser
        url = "ads/library"
        def text(self): return html
    on_resp(R())
    for k in range(25):
        pg.mouse.wheel(0, 4000); time.sleep(2)
    b.close()
json.dump(achados, open(OUT, "w", encoding="utf-8"), indent=1)
print(len(achados), "anúncios com URL de vídeo |", sum(1 for v in achados.values() if v["hd"]), "com HD")
