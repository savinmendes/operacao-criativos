import sys
from playwright.sync_api import sync_playwright
urls=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=False,args=["--window-position=-2400,-2400"])
    ctx=b.new_context(locale="es-CL")
    pg=ctx.new_page()
    for u in urls:
        try:
            pg.goto(u,wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(9000)
            print("=====",u); print(pg.inner_text("body")[:3500])
        except Exception as e: print("ERR",u,e)
    b.close()
