# -*- coding: utf-8 -*-
"""Top N imagens (ordem da página = maiores impressões), sem repetidas (md5)."""
import json, re, sys, time, hashlib, os
import requests
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright
URL = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
ordem, ads = [], {}
def achar(o):
    if isinstance(o, dict):
        if "ad_archive_id" in o and "snapshot" in o: yield o
        for v in o.values(): yield from achar(v)
    elif isinstance(o, list):
        for v in o: yield from achar(v)
def processar(t):
    for linha in t.splitlines():
        if "ad_archive_id" not in linha: continue
        cands = [linha.strip()] if linha.strip().startswith("{") else re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', linha, re.S)
        for c in cands:
            if "ad_archive_id" not in c: continue
            try: o = json.loads(c)
            except Exception: continue
            for a in achar(o):
                aid = a["ad_archive_id"]; s = a.get("snapshot") or {}
                if aid in ads: continue
                imgs = [i.get("original_image_url") or i.get("resized_image_url") for i in (s.get("images") or [])]
                imgs += [c.get("original_image_url") or c.get("resized_image_url") for c in (s.get("cards") or []) if not (c.get("video_hd_url") or c.get("video_sd_url"))]
                body = (s.get("body") or {}).get("text") if isinstance(s.get("body"), dict) else s.get("body")
                ordem.append(aid)
                ads[aid] = {"inicio": a.get("start_date"), "variacoes": a.get("collation_count"), "texto": body, "titulo": s.get("title"),
                            "link": s.get("link_url"), "formato": s.get("display_format"), "imagens": [u for u in imgs if u]}
def on_resp(r):
    try:
        if "graphql" in r.url: processar(r.text())
    except Exception: pass
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(locale="en-US", viewport={"width": 1400, "height": 1000})
    pg.on("response", on_resp)
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000); time.sleep(8)
    processar(pg.content())
    for k in range(80):
        if sum(1 for a in ordem if ads[a]["imagens"]) >= N * 2: break
        pg.mouse.wheel(0, 5000); time.sleep(2)
    b.close()
print("anúncios lidos:", len(ordem), "| com imagem:", sum(1 for a in ordem if ads[a]["imagens"]))
os.makedirs("imagens", exist_ok=True)
vistos, lista, S = set(), [], requests.Session()
for aid in ordem:
    if len(lista) >= N: break
    for u in (ads[aid]["imagens"][:1] if ads[aid]["formato"] == "DPA" else ads[aid]["imagens"]):
        r = S.get(u, timeout=60); r.raise_for_status()
        h = hashlib.md5(r.content).hexdigest()
        if h in vistos: continue
        vistos.add(h)
        n = len(lista) + 1
        im = Image.open(BytesIO(r.content)).convert("RGB")
        fn = f"imagens/{n:02d}_{aid}.jpg"
        im.save(fn, quality=95)
        a = ads[aid]
        lista.append({"n": n, "arquivo": fn, "id": aid, "formato": a["formato"], "resolucao": f"{im.width}x{im.height}",
                      "inicio": time.strftime("%d/%m/%Y", time.localtime(a["inicio"])) if a["inicio"] else "", "variacoes": a["variacoes"],
                      "titulo": a["titulo"], "texto": a["texto"], "link": a["link"], "biblioteca": f"https://www.facebook.com/ads/library/?id={aid}"})
        print(f"[{n}/{N}] {fn} {im.width}x{im.height} {a['formato']}")
        if len(lista) >= N: break
json.dump(lista, open("imagens/indice_imagens.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
