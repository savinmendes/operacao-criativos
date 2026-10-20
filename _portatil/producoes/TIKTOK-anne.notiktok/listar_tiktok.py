# -*- coding: utf-8 -*-
"""Abre o perfil do TikTok no Chrome (headless) e captura, nas respostas de rede, os vídeos com visualizações."""
import json, re, sys, time
from playwright.sync_api import sync_playwright

URL, OUT = sys.argv[1], sys.argv[2]
videos = {}

def guardar(item):
    vid = str(item.get("id") or "")
    st = item.get("stats") or item.get("statsV2") or {}
    if not vid or not st:
        return
    videos[vid] = {
        "id": vid,
        "plays": int(st.get("playCount") or 0),
        "likes": int(st.get("diggCount") or 0),
        "desc": item.get("desc", ""),
        "data": item.get("createTime"),
        "dur": (item.get("video") or {}).get("duration"),
    }

def on_resp(r):
    if "item_list" not in r.url:
        return
    try:
        d = r.json()
    except Exception:
        return
    for it in d.get("itemList") or []:
        guardar(it)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=False, args=["--start-minimized"])
    pg = b.new_page(locale="en-US", viewport={"width": 1300, "height": 1000})
    pg.on("response", on_resp)
    pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
    time.sleep(8)
    # JSON embutido no HTML (primeira página)
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', pg.content(), re.S)
    if m:
        try:
            u = json.loads(m.group(1))
            info = u["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
            print("perfil:", info["user"]["uniqueId"], "videos:", info["stats"].get("videoCount"))
        except Exception as e:
            print("sem userInfo", e)
    if len(sys.argv) > 3 and sys.argv[3] == "popular":
        try:
            pg.get_by_text("Popular", exact=True).first.click(timeout=15000)
            print("aba Popular clicada")
        except Exception as e:
            print("nao achei Popular", e)
        time.sleep(1)
        videos.clear()
        time.sleep(6)
    parado = 0
    for k in range(200):
        n = len(videos)
        pg.mouse.wheel(0, 5000)
        time.sleep(2.5)
        parado = parado + 1 if len(videos) == n else 0
        if parado >= 6:
            break
    b.close()

lst = sorted(videos.values(), key=lambda v: -v["plays"])
json.dump(lst, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("capturados:", len(lst))
