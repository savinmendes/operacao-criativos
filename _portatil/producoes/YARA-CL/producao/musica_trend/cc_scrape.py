import json, sys
from playwright.sync_api import sync_playwright
out=[]
urls=["https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en?region=CL&period=7",
      "https://ads.tiktok.com/business/creativecenter/music/pc/en?countryCode=CL&period=7"]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=False,args=["--window-position=-2400,-2400"])
    ctx=b.new_context(locale="en-US",user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
    pg=ctx.new_page()
    def on(r):
        if "creative_radar_api" in r.url:
            try: out.append({"url":r.url,"status":r.status,"body":r.json()})
            except Exception: out.append({"url":r.url,"status":r.status})
    pg.on("response",on)
    for u in urls:
        try:
            resp=pg.goto(u,wait_until="domcontentloaded",timeout=60000)
            print(u, resp.status if resp else None)
            pg.wait_for_timeout(12000)
            print(pg.inner_text("body")[:2500])
        except Exception as e: print("ERR",u,e)
    b.close()
json.dump(out,open(sys.argv[1],"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("api", [ (o["url"][:120],o["status"]) for o in out])
