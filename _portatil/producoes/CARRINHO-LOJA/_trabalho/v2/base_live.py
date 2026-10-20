import json
from playwright.sync_api import sync_playwright
UA_M = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    ctx = b.new_context(viewport={"width":390,"height":844}, is_mobile=True, has_touch=True, device_scale_factor=2, user_agent=UA_M)
    pg = ctx.new_page(); errs=[]
    pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
    pg.goto("https://chileverificada.com/collections/perfumes-arabes", wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(6000)
    print("theme:", pg.evaluate("Shopify.theme && [Shopify.theme.id, Shopify.theme.role]"))
    print("erros sem acao:", errs)
    pg.screenshot(path=r"C:\Users\PICHAU\Downloads\CARRINHO-LOJA\v2\0_antes_colecao_live_mobile.png")
    pg.evaluate("""fetch('/cart/clear.js',{method:'POST'}).then(()=>fetch('/products/lattafa.js')).then(r=>r.json()).then(p=>fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:p.variants[0].id,quantity:1}]})}))""")
    pg.wait_for_timeout(1500)
    pg.evaluate("document.querySelectorAll('#product-grid ._rsi-buy-now-button')[2].click()")
    pg.wait_for_selector("#_rsi-cod-form-modal._rsi-cod-form-modal-open", timeout=20000); pg.wait_for_timeout(2500)
    print("form live com 1 item no carrinho:", pg.evaluate("document.querySelector('#_rsi-cod-form-modal').innerText.slice(0,200)"))
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800)
    b.close()
