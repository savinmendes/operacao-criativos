from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    for url in ["https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml",
                "https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml?preview_theme_id=167232798976"]:
        pg = b.new_page(); e = []
        pg.on("pageerror", lambda x: e.append((str(x)[:120], (x.stack or '')[:300].replace('\n',' | '))))
        pg.goto(url, wait_until="load", timeout=90000); pg.wait_for_timeout(6000)
        print(url[-30:], len(e)); [print("  ", x) for x in e if 'closest' in x[0] or 'Unexpected' in x[0]]
        pg.close()
    b.close()
