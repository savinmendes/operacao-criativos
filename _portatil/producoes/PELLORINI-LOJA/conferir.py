import re, html, sys
from playwright.sync_api import sync_playwright
T = "193568080148"
urls = {"produto": "https://essiora.com/products/vittorio", "carrinho": "https://essiora.com/cart"}
procurar = re.compile(r"pelvini|13,066|13066|100,000|5,900|5,000 orders|30-Day|UK|cleaning|home essentials|Pellorini|worldwide|90-Day", re.I)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1366, "height": 900})
    pg.goto(f"https://essiora.com/?preview_theme_id={T}", wait_until="domcontentloaded")
    for nome, u in urls.items():
        pg.goto(u + f"?preview_theme_id={T}", wait_until="load", timeout=90000); pg.wait_for_timeout(5000)
        txt = pg.evaluate("() => document.body.innerText")
        achados = sorted(set(l.strip()[:120] for l in txt.splitlines() if procurar.search(l)))
        print("=====", nome); [print("  ", a) for a in achados]
        pg.screenshot(path=f"prev_{nome}.png", full_page=False)
    b.close()
