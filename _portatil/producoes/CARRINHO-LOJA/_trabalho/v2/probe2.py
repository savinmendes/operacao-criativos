from playwright.sync_api import sync_playwright
UA_M="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    ctx=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,user_agent=UA_M); pg=ctx.new_page()
    u="https://chileverificada.com/collections/perfumes-arabes?preview_theme_id=167234765056"
    r=pg.goto(u,wait_until="domcontentloaded",timeout=90000); pg.wait_for_timeout(3000)
    print("1",r.status,pg.url,pg.evaluate("!!document.querySelector('#product-grid')"))
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800)
    r=pg.goto(u,wait_until="domcontentloaded",timeout=90000); pg.wait_for_timeout(3000)
    print("2",r.status,pg.url,pg.evaluate("!!document.querySelector('#product-grid')"), pg.title(), pg.evaluate("document.body.innerText.slice(0,200)"))
    pg.screenshot(path="probe2.png")
    b.close()
