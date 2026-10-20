from playwright.sync_api import sync_playwright
OUT=r"C:/Users/PICHAU/Downloads/CARRINHO-LOJA/v2/ref-linfarele"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome"); pg=b.new_page()
    pg.goto("https://linfarele.com/products/drenante-linfatico",wait_until="domcontentloaded",timeout=90000); pg.wait_for_timeout(5000)
    h=pg.evaluate("document.querySelector('#lfs').closest('section').outerHTML")
    open(OUT+"/lfs_section.html","w",encoding="utf-8").write(h); print(len(h))
    b.close()
