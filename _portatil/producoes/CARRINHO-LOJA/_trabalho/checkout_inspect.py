import json
from playwright.sync_api import sync_playwright
OUT = r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    pg = b.new_page(viewport={"width": 1280, "height": 1000})
    pg.goto("https://chileverificada.com/products/kit-3-perfumes-arabes-mujer-yara-yara-moi-yara-elixir-lattafa-100ml", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(3000)
    pg.evaluate("""async () => { await fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:50570047258880,quantity:1}]})}); }""")
    pg.goto("https://chileverificada.com/checkout", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(12000)
    print(pg.url)
    pg.screenshot(path=OUT + r"\_trabalho\checkout_shopify.png", full_page=True)
    txt = pg.evaluate("() => document.body.innerText")
    i = txt.lower().find("pago")
    print(txt[:3000])
    b.close()
