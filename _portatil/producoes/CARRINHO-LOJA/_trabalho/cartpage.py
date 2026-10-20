from playwright.sync_api import sync_playwright
OUT = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
    pg.goto("https://chileverificada.com/products/perfume-arabe-lattafa-asad-100ml-edp-original?preview_theme_id=167232798976", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(4000)
    pg.evaluate("fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:50570136224000,quantity:1}]})})")
    pg.wait_for_timeout(1500)
    pg.goto("https://chileverificada.com/cart?preview_theme_id=167232798976", wait_until="domcontentloaded")
    pg.wait_for_timeout(6000)
    pg.click("#main-cart-footer [name='checkout'], .cart__footer [name='checkout'], main [name='checkout']")
    pg.wait_for_timeout(5000)
    print("url:", pg.url)
    print("modal aberto:", pg.evaluate("!!document.querySelector('#_rsi-cod-form-modal._rsi-cod-form-modal-open')"))
    pg.screenshot(path=OUT + r"\depois_8_pagina-cart-pagar-abre-cod_mobile.png")
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800)
    b.close()
