from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    for T in ("167234765056","167236436224"):
        pg=b.new_page(viewport={"width":1440,"height":900})
        pg.goto(f"https://chileverificada.com/collections/all?preview_theme_id={T}",wait_until="domcontentloaded",timeout=90000); pg.wait_for_timeout(6000)
        print(T, pg.evaluate("({qa:document.querySelectorAll('.quick-add').length, btn:document.querySelectorAll('.cv-qa-btn').length, perf:[...document.querySelectorAll('a[href*=\"/products/kit-3\"]')].length})"))
        pg.close()
    b.close()
