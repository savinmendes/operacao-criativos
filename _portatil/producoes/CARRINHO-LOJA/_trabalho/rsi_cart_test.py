import json
from playwright.sync_api import sync_playwright
OUT = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\_trabalho"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
    pg.goto("https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml?preview_theme_id=167232798976", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(7000)
    pg.evaluate("""async () => { await fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:50570047258880,quantity:2},{id:50570136224000,quantity:1}]})}); }""")
    pg.wait_for_timeout(1000)
    r = pg.evaluate("""() => { try { _rsi.form.mode='normalCart'; _rsi.form.open(); return 'ok'; } catch(e) { return 'err ' + e; } }""")
    print(r)
    pg.wait_for_timeout(6000)
    pg.screenshot(path=OUT + r"\rsi_normalcart_test.png", full_page=False)
    print(pg.evaluate("() => { const m = document.querySelector('#_rsi-cod-form-modal'); return m ? (m.className + ' | ' + m.innerText.slice(0,1500)) : 'no modal'; }"))
    b.close()
