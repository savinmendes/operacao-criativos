import json, re
from playwright.sync_api import sync_playwright
OUT=r"C:/Users/PICHAU/Downloads/CARRINHO-LOJA/v2/ref-linfarele"
UA_M="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    ctx=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=2,user_agent=UA_M)
    pg=ctx.new_page()
    pg.goto("https://linfarele.com/",wait_until="domcontentloaded",timeout=90000); pg.wait_for_timeout(7000)
    print("url",pg.url, "title", pg.title())
    pg.screenshot(path=OUT+"/01_home_mobile.png")
    scripts=pg.evaluate("[...document.scripts].map(s=>s.src).filter(Boolean)")
    print("\n".join(sorted(set(re.sub(r'\?.*','',s) for s in scripts))))
    links=pg.evaluate("[...new Set([...document.querySelectorAll('a[href*=\"/products/\"]')].map(a=>a.getAttribute('href')))].slice(0,10)")
    print("products", links)
    print("body text", pg.evaluate("document.body.innerText.slice(0,800)"))
    b.close()
