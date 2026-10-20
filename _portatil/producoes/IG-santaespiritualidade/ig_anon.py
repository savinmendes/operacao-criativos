import json, sys, time
from playwright.sync_api import sync_playwright
posts={}
def on_resp(r):
    if "graphql" in r.url or "web_profile_info" in r.url or "/feed/user" in r.url:
        try: t=r.text()
        except Exception: return
        open(f"resp_{len(posts)}_{int(time.time()*1000)}.json","w",encoding="utf-8").write(t)
        posts[r.url]=len(t)
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(locale="pt-BR",viewport={"width":1300,"height":1000})
    pg.on("response",on_resp)
    pg.goto("https://www.instagram.com/santaespiritualidade/",wait_until="domcontentloaded",timeout=90000); time.sleep(10)
    for k in range(5): pg.mouse.wheel(0,3000); time.sleep(3)
    pg.screenshot(path="tela.png")
    print(pg.title()); print(posts)
    b.close()
