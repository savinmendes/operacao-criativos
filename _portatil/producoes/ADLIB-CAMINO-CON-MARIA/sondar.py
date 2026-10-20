# -*- coding: utf-8 -*-
import json, re, sys, time
from playwright.sync_api import sync_playwright
URL=sys.argv[1]
raw=[]
def on_resp(r):
    try:
        if "graphql" in r.url or "ads/library" in r.url: raw.append(r.text())
    except Exception: pass
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(locale="es-ES",viewport={"width":1400,"height":1000})
    pg.on("response",on_resp)
    pg.goto(URL,wait_until="domcontentloaded",timeout=90000); time.sleep(8)
    for k in range(30):
        pg.mouse.wheel(0,4000); time.sleep(2)
    raw.append(pg.content())
    open("_texto_pagina.txt","w",encoding="utf-8").write(pg.inner_text("body"))
    b.close()
open("_raw.txt","w",encoding="utf-8").write("\n\n=====\n\n".join(raw))
print("respostas",len(raw))
