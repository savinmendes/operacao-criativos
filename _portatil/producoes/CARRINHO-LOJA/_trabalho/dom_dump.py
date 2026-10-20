from playwright.sync_api import sync_playwright
OUT = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\_trabalho"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto("https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml?preview_theme_id=167232798976", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(8000)
    html = pg.content()
    open(OUT + r"\produto_render.html", "w", encoding="utf-8").write(html)
    r = pg.evaluate("""() => {
      const o = s => { const e = document.querySelector(s); return e ? e.outerHTML.slice(0, 2500) : 'NONE ' + s; };
      const rsi = document.querySelector('#_rsi-buy-now-button');
      return [o('#cart-icon-bubble'), o('cart-drawer') .slice(0,800),
        'RSI PARENT: ' + (rsi ? rsi.parentElement.outerHTML.slice(0, 600) : 'none'),
        'RSI PREV: ' + (rsi && rsi.previousElementSibling ? rsi.previousElementSibling.outerHTML.slice(0,400) : 'none'),
        'RSI NEXT: ' + (rsi && rsi.nextElementSibling ? rsi.nextElementSibling.outerHTML.slice(0,600) : 'none'),
        'FORM: ' + (document.querySelector('product-form') ? document.querySelector('product-form').outerHTML.slice(0,3000) : 'none')
      ].join('\\n\\n-----\\n\\n');
    }""")
    print(r)
    b.close()
