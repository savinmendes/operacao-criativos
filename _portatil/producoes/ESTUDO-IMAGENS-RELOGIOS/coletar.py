# -*- coding: utf-8 -*-
"""Coleta anúncios de uma busca na Biblioteca de Anúncios do Meta (respostas de rede) e salva JSON por loja."""
import json, re, sys, time
from playwright.sync_api import sync_playwright
NOME, Q, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
URL = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q={Q}&search_type=keyword_unordered"
ads = {}
def achar(o):
    if isinstance(o, dict):
        if "ad_archive_id" in o and "snapshot" in o:
            yield o
        for v in o.values(): yield from achar(v)
    elif isinstance(o, list):
        for v in o: yield from achar(v)
def processar(t):
    for linha in t.splitlines():
        linha = linha.strip()
        if "ad_archive_id" not in linha: continue
        cands = [linha]
        if not linha.startswith("{"):
            cands = re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', linha, re.S)
        for c in cands:
            if "ad_archive_id" not in c: continue
            try: o = json.loads(c)
            except Exception: continue
            for a in achar(o):
                s = a.get("snapshot") or {}
                aid = a["ad_archive_id"]
                imgs = [i.get("original_image_url") or i.get("resized_image_url") for i in (s.get("images") or [])]
                cards = s.get("cards") or []
                for cd in cards:
                    u = cd.get("original_image_url") or cd.get("resized_image_url")
                    if u: imgs.append(u)
                body = (s.get("body") or {}).get("text") if isinstance(s.get("body"), dict) else s.get("body")
                ads[aid] = {
                    "id": aid, "pagina": s.get("page_name") or a.get("page_name"),
                    "formato": s.get("display_format"), "ativo": a.get("is_active"),
                    "inicio": a.get("start_date"), "fim": a.get("end_date"),
                    "variacoes": a.get("collation_count"), "plataformas": a.get("publisher_platform"),
                    "texto": body, "titulo": s.get("title"), "link_desc": s.get("link_description"),
                    "cta": s.get("cta_text"), "link": s.get("link_url"),
                    "cards": [{"titulo": c.get("title"), "texto": c.get("body"), "img": c.get("original_image_url") or c.get("resized_image_url"), "video": bool(c.get("video_hd_url") or c.get("video_sd_url"))} for c in cards],
                    "imagens": [u for u in imgs if u],
                    "tem_video": bool(s.get("videos")) or any(c.get("video_hd_url") or c.get("video_sd_url") for c in cards),
                }
def on_resp(r):
    try:
        if "graphql" not in r.url: return
        processar(r.text())
    except Exception: pass
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(locale="en-US", viewport={"width": 1400, "height": 1000})
    pg.on("response", on_resp)
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000); time.sleep(8)
    processar(pg.content())
    antes, parado = 0, 0
    for k in range(250):
        pg.mouse.wheel(0, 5000); time.sleep(2)
        if len(ads) == antes: parado += 1
        else: parado = 0
        antes = len(ads)
        if parado >= 8 or len(ads) >= 1200: break
    b.close()
json.dump(list(ads.values()), open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(NOME, len(ads), "anúncios |", Counter(a["formato"] for a in ads.values()), "| páginas:", Counter(a["pagina"] for a in ads.values()).most_common(4))
