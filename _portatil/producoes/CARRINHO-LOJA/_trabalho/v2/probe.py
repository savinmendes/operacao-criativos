from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome"); pg=b.new_page()
    r=pg.goto("https://chileverificada.com/collections/perfumes-arabes?preview_theme_id=167234765056",wait_until="domcontentloaded",timeout=90000)
    pg.wait_for_timeout(5000)
    print(r.status, pg.url, pg.title(), pg.evaluate("Shopify.theme && Shopify.theme.id"), pg.evaluate("!!document.querySelector('#product-grid')"), pg.evaluate("document.body.innerText.slice(0,300)"))
    b.close()
