from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True, channel="chrome")
    pg=b.new_page(viewport={"width":1440,"height":900}); n=[0]
    pg.on("pageerror", lambda e: n.__setitem__(0, n[0]+('innerHTML' in str(e))))
    pg.goto("https://chileverificada.com/collections/perfumes-arabes",wait_until="domcontentloaded",timeout=90000); pg.wait_for_timeout(5000)
    pg.evaluate("""fetch('/cart/clear.js',{method:'POST'}).then(()=>fetch('/products/lattafa.js')).then(r=>r.json()).then(p=>fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:[{id:p.variants[0].id,quantity:1}]})}))"""); pg.wait_for_timeout(1500)
    print("antes rsi", n[0])
    pg.evaluate("document.querySelectorAll('#product-grid ._rsi-buy-now-button')[2].click()"); pg.wait_for_timeout(5000)
    print("live: erros innerHTML apos rsi:", n[0])
    pg.evaluate("fetch('/cart/clear.js',{method:'POST'})"); pg.wait_for_timeout(800); b.close()
