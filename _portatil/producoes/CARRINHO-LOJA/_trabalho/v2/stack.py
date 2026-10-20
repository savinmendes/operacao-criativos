from playwright.sync_api import sync_playwright
T="167234765056"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    pg=b.new_page(viewport={"width":1440,"height":900})
    def onerr(e):
        if 'innerHTML' in str(e): print("STEP", step[0], "|", e.stack[:600] if hasattr(e,'stack') else e)
    step=["load"]
    pg.on("pageerror", onerr)
    pg.goto(f"https://chileverificada.com/collections/perfumes-arabes?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000)
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(5000)
    step[0]="addcard"; pg.locator(".cv-qa-btn").first.click(); pg.wait_for_timeout(4000)
    step[0]="esc"; pg.keyboard.press("Escape"); pg.wait_for_timeout(1000)
    step[0]="add2"; pg.locator(".cv-qa-btn").nth(1).click(); pg.wait_for_timeout(4000)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
    step[0]="rsi"; pg.evaluate("document.querySelectorAll('#product-grid ._rsi-buy-now-button')[2].click()"); pg.wait_for_timeout(5000)
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800)
    b.close()
